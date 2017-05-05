#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libvirt
import sys
import os
import xml.etree.ElementTree
import random

class VM_Assistant(object):

    def __init__(self, VMName, CPU = 0, Memory = 0, Disk = 0, ImagePath='', Host='127.0.0.1'):
        self.VMName = VMName
        self.CPU = CPU
        self.Memory = Memory
        self.Disk = Disk
        self.ImagePath = ImagePath
        self.MAC = self.Rand_Mac()
        self.DiskPath = '/root/workspace/MyCloud/disks/' + self.VMName + '.qcow2'
        self.ConfigFile1 = '/root/workspace/MyCloud/mycloud/virtscripts/base1.xml'
        self.ConfigFile2 = '/root/workspace/MyCloud/mycloud/virtscripts/base2.xml'
        self.HostURI = 'qemu+ssh://root@%s/system'%(Host)

    def Rand_Mac(self):
        MACList = []
        for i in range(1,7):
            RANDSTR = ''.join(random.sample('0123456789abcdef',2))
            MACList.append(RANDSTR)
        MAC = ':'.join(MACList)
        return MAC


    def Link(self):
        try:
            host = libvirt.open(self.HostURI)
        except Exception:
            print 'Error, Open virtual machine link failed.'
            return False
        else:
            return host
        finally:
            pass

    def Config_VM1(self, s):
        if not s: return False
        s = s.replace('<name>', '<name>%s'%self.VMName)
        s = s.replace('<vcpu>', '<vcpu>%s'%self.CPU)
        s = s.replace('<memory>', '<memory>%s'%self.Memory)
        s = s.replace('<source file=\'', '<source file=\'%s'%self.DiskPath)
        return s

    def Config_VM2(self, s):
        if not s: return False
        s = s.replace('<source file=\'', '<source file=\'%s'%self.ImagePath)
        return s

    def CreateVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        os.system('qemu-img create -f qcow2 %s %s'%(self.DiskPath, self.Disk))
        f1 = file(self.ConfigFile1, 'rb')
        XMLString1 = self.Config_VM1(f1.read())
        f1.close()
        f2 = file(self.ConfigFile2, 'rb')
        XMLString2 = self.Config_VM2(f2.read())
        f2.close()
        XMLString = XMLString1 + XMLString2
        domain = host.defineXML(XMLString)
        state = domain.state()[0]
        if state == libvirt.VIR_DOMAIN_RUNNING: return True
        else: return False

    def LaunchVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        domain.create()
        state = domain.state()[0]
        if state == libvirt.VIR_DOMAIN_RUNNING: return True
        else: return False

    def ShutdownVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        domain.destroy()
        return True

    def SuspendVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        domain.suspend()
        return True

    def ResumeVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        domain.resume()
        return True    

    def RebootVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        domain.reboot()
        return True

    def DeleteVM(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        try:
            domain.destroy()
        except:
            pass
        finally:
            domain.undefine()
            return True

    def GetVNCPort(self):
        host = self.Link()
        if not host:
            sys.exit()
        domain = host.lookupByName(self.VMName)
        XMLString = domain.XMLDesc()
        root = xml.etree.ElementTree.fromstring(XMLString)
        nodes = root.getiterator('graphics')
        for node in nodes:
            for key,value in node.items():
                if key == 'port':
                    return value
        return False

