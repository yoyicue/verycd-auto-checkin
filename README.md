
## VeryCD Auto Checkin Tool
这又是一个很挫的脚本, 用来在 VeryCD 上自动登录并 [签到](http://game.verycd.com/) 领取每日1分经验, 积少成多 100 分之后可以铜光盘下载所有资源, 100天呐~~

### 依赖
原谅我没使用 urllib 来实现, 脚本依赖
[Requests](http://docs.python-requests.org/en/v1.0.0/)

### 安装
首先下载或者 Git 代码到本地  
然后用 `virtualenv` 创建环境并解决依赖.

```
git clone https://github.com/yoyicue/verycd-auto-checkin.git
virtualenv .env --distribute --no-site-packages
.env/bin/pip install requests==1.0.2 -i http://e.pypi.python.org/simple

```

### 使用
进入环境
```
. .env/bin/activate
```
登录并签到

```
./verycd.py checkin -u 'username,password'

```
仅签到

```
./verycd.py checkin

```
仅登录

```
./verycd.py login -u 'username,password'

```


### 自动化
使用 `crontab` 在服务器上每天自动领签到, 记得替换依赖 Requests 的 Pyhton 路径

```
TODO
```
另外, 可以蛋疼的使用 [Growl](http://growl.info/) 和管道, 可以发送 iOS 签到成功的消息.
