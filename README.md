# MyCloud
 
 基于Flask框架的云计算管理平台，其中虚拟化管理接口使用libvirt，图形界面使用NoVNC（开源的VNC客户端）。
 
 
 
 
## 开发环境
环境 | 版本
---|---
操作系统 | Ubuntu 14.04 x86_64
数据库 | MySQL 5.7.16
虚拟化 | QEMU(Libvirt)
开发语言 | Python 2.7.4
后端框架 | Flask 0.12
前端框架 | Bootstrap 3.0

 
## 使用方法

 1、安装环境依赖包（不同版本操作系统安装方法有差异，见网上具体解决方案）：<pre><code>pip install -r requirements.txt</code></pre>
Linux下可以直接运行shell脚本：<pre><code>bash env_config.sh</code></pre>

 2、安装MySQL数据库（需要在MyCloud/mycloud/config.py修改配置文件）：

 ```python
 # -*- coding: utf-8 -*-
import os

class DefaultConfig(object):  
    # 默认配置类，由app.py的configure_app(app, config)函数调用对Flask应用app进行配置

    ...
    
    SQLALCHEMY_DATABASE_URI = "mysql://MySQL用户名:密码@ip（或域名）/数据库名"
```

 3、MyCloud/images目录添加下载好的系统镜像文件（为方便测试推荐使用较小型的系统如TinyLinux等）。
 
 4、项目目录下运行：<pre><code>python manage.py run</code></pre>

 5、浏览器下访问：<pre><code>127.0.0.1:8000</code></pre>


## 运行效果

 ![Alt text](https://github.com/yipwinghong/MyCloud/blob/master/Screenshots/1.jpg)
 ![Alt text](https://github.com/yipwinghong/MyCloud/blob/master/Screenshots/2.jpg)

