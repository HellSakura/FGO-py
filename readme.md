# "智能战斗不间断,不靠礼装不用拐"的FGO全自动脚本
改自版本[v4.0.3] 原readme见[这里](./doc/readme.md)
仅适用于命运-冠位指定安卓简体中文版本
适用系统 macOS
原GitHub项目地址:[https://github.com/hgjazhgj/FGO-py/](https://github.com/hgjazhgj/FGO-py/)
***
~~双击打开用就完了,本脚本几乎没有限制~~
自4.0.3版本后，原作者使用了win32api，而`pywin32`库无法在macOS系统中使用
加上macOS中相对好用且更新~~修BUG~~频繁的只有**网易MUMU模拟器**
而mumu模拟器不支持maxtouch,只能用minitouch
~~作为一个Python新手又怕改了Base类出现各种BUG~~
于是在此版本基础上进行魔改以加入原作者的新功能

UI在macOS下的显示效果
![ui](./doc/UI(mac).png)
## 使用说明 Instruction
* 首先你需要保证安装的Python版本在**3.7**版本以下
不然会各种花式无法安装`airtest`库
此处原因在于`airtest`库所使用的`opencv-contrib-python`版本需要小于等于3.4.2.17
而`opencv-contrib-python`的3.4.2.17版本仅支持到Python3.7
* 若更改过pip源可以去[pypi](https://pypi.org/project/opencv-contrib-python/3.4.2.17/#files)下载后手动安装
1. 所使用的库有`configParser` `PyQt5` `airtest` ，请手动使用`pip install`命令进行安装，报错也方便排查原因
2. 使用Homebrew安装adb ~~airtest自带macOS版的不能使用~~
    ```
    brew cask install android-platform-tools
    ```
    测试是否正常安装
    ```
    adb devices
    ```
3. 将使用Homebrew安装获得的adb替换掉airtest自带的adb
Homebrew安装的adb路径为
    ```
    /usr/local/Caskroom/android-platform-tools/30.0.0/platform-tools
    ```
    airtest自带的adb路径为
    ```
    /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/airtest/core/android/static/adb/mac
    ```
    请自行根据安装的版本微调位置

其余使用方式和原版本一致
## 当前加入的原版本功能
------
- [x] 4.9.0版本技能冷却及np条位置
- [x] 截止4.7.0版本 部分延时调整
- [x] 4.6.0版本 无限池抽取
- [x] 4.3.2版本 重新设计的选卡代码
- [x] 4.3.0版本 连续战斗功能

## 已知BUG
------
* 编队选取功能使用时报错，只能关闭选取编队功能
以下为错误报告，如果有解决方法请务必指点一下
```
[ERROR]<fgoGui> OpenCV(3.4.2) /Users/travis/build/skvark/opencv-python/opencv/modules/imgproc/src/templmatch.cpp:1102: error: (-215:Assertion failed) (depth == 0 || depth == 5) && type == _templ.type() && _img.dims() <= 2 in function 'matchTemplate'
Traceback (most recent call last):
  File "/Users/hellsakura/Documents/vscode/FGO-py/fgoGui.py", line 177, in f
    func(*args,**kwargs)
  File "/Users/hellsakura/Documents/vscode/FGO-py/fgoFunc.py", line 277, in main
    if partyIndex and check.getPartyIndex()!=partyIndex:doit(('\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79'[partyIndex-1],' '),(1000,400))
  File "/Users/hellsakura/Documents/vscode/FGO-py/fgoFunc.py", line 182, in getPartyIndex
    def getPartyIndex(self):return cv2.minMaxLoc(cv2.matchTemplate(self.im[58:92,768:1152],IMG_PARTYINDEX,cv2.TM_SQDIFF_NORMED))[2][0]//37+1
cv2.error: OpenCV(3.4.2) /Users/travis/build/skvark/opencv-python/opencv/modules/imgproc/src/templmatch.cpp:1102: error: (-215:Assertion failed) (depth == 0 || depth == 5) && type == _templ.type() && _img.dims() <= 2 in function 'matchTemplate'
```
------
* ~~考试完再想办法根据原作者的提示更改DirListener类~~
原作者提示在[这里](https://github.com/hgjazhgj/FGO-py#%E5%BF%AB%E9%80%9F%E6%9F%A5%E9%94%99%E5%BC%95%E5%AF%BC-when-error-occurred)
