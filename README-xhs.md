### 如何操作
docker镜像被封了之后，可以本地构建镜像
```
docker build -t my-xhs-api:tag .
```
然后启动镜像
```
docker run -it -d -p 5005:5005 my-xhs-api:tag
```
把日志中输出的 `a1` 复制到已经登陆的小红书首页，（通过EditThisCookie），然后导出，粘贴到‘basic_sign.py’中。  
在linux中，需要把启动参数改为True（因为linux没有可视界面）
```
browser = chromium.launch(headless=True)
```
需要注意如果sealth.js的路径不正确，也会报错。
