# ziroom_watcher

监视自如房源，当状态更新时获得邮件更新

## 安装

`pip install ziroom_watcher`

## 用法

```py
from ziroom_watcher import Watcher

watcher = Watcher('http://www.ziroom.com/z/vr/1234567.html')
watcher.config({
    'username': '*****@qq.com',
    'password': '********',
})
watcher.watch()
```