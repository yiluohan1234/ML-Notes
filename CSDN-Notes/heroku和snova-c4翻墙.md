## 一、snova-c4（翻墙软件）下载

下载列表

https://code.google.com/p/snova/downloads/list
服务端
https://snova.googlecode.com/files/snova-c4-java-server-0.22.0.war
客户端
https://snova.googlecode.com/files/gsnova_0.22.1_windows_386.zip

## 二、heroku.com部署snova-c4-java-server-0.22.0.war

```
heroku login
heroku plugins:install heroku-cli-deploy --只需执行一次，以后不用执行
heroku create <app_name> --此步创建一个app,名字为<app_name>
heroku deploy:war --war <path_to_war_file> --app <app_name>
```



输入域名https://<app_name>.herokuapp.com/，见下面页面，则说明部署成功。

![](./snova1.png)

## 三、解压gsnova_0.22.1_windows_386.zip

修改gsnova.conf

解压缩，修改 gsnova.conf 的以下部分

```
[GAE]
Enable=0

[C4]
Enable=1
WorkerNode[0]=<app_name>.herokuapp.com

[SPAC]
Enable=0

```

双击打开gsnova.exe可执行文件。

## 4.浏览器设置代理

google 就装switchysharp
代理设置端口时要与你在配置文件中设置的端口是一致的。
默认是127.0.0.1 端口48102

heroku为php添加扩展