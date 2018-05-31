# Cblog

一个基于 Flask 的博客系统


## 部署

创建镜像

    docker build -f dockerfile -t cblog:0.6 .  

由于我使用的是 sqlite 所以要新建数据库和添加角色

    docker run -itd -p 0.0.0.0:8000:8000 -v /docker_cblog:/data --restart=always IMAGE ID

用于启动容器，并且添加自启

```
server {
        listen 80;
        server_name  cblog.copie.cn;  
        
        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_redirect     off;
                proxy_set_header   Host                 $http_host;
                proxy_set_header   X-Real-IP            $remote_addr;
                proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Proto    $scheme;
    }
}
```
添加以上配置文件到 nginx。