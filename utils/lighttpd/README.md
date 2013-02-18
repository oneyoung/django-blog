
## 依赖
Django上使用FastCGI需要`flup`库依赖:
```bash
pip install flup
```

## 使用
### 目录
我这里使用的目录是: `/www/django-blog/`
请根据自己配置，自行修改`run_server.sh` 和`lighttpd.conf`对应的内容．

### Django Server
运行`run_server.sh`, 就可以建立一个fastcgi server, 地址:127.0.0.1:3033

### lighttpd 配置
将lighttpd.conf 内容添加到 /etc/lighttpd/lighttpd.conf
然后，重启server
```bash
service lighttpd restart
```
