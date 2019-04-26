使用说明:
ftp_server文件夹,bin目录下ftp_server.py,运行服务端;
ftp_client文件夹,bin目录下start_client.py,运行客户端;
之后在客户端中进行操作,先登录
用户名 :a ,密码:1
登陆成功后会自动创建一个文件夹,文件夹名为用户名
然后是客户端的操作: 要求 输入
client 输入格式:   操作|文件
操作有 : put 和 get ,分别是 上传和下载
示例: put|up.jpg       get|down.jpg

文件说明:
up.jpg为要上传的图片,存在client文件夹的db中
上传完成之后,到server文件夹的cloud文件夹中
down.jpg 为要下载的文件,存在server文件夹的home中,
下载完成之后,到client文件夹的用户文件夹中,这里就是会生成一个 a 文件夹


总结:这次写的很乱,没用socketserver,感觉还是没太搞明白.没有模拟Linux,
已完成的功能:面向对象,基本的上传/下载,用户登录,创建文件夹