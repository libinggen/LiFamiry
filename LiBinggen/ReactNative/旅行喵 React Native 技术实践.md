![2.pic_hd.jpg](http://upload-images.jianshu.io/upload_images/80690-acb24c7bd68e4903.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

大家好，非常感谢大家百忙中抽时间来参加这次分享。也非常感谢XX的辛苦组织。
React Native，是这两年比较热的新技术。各大厂商纷纷专门安排团队接入。
我们非常幸运，这次用RN开发了一个完整的产品旅行喵，现在和大家分享一下我们这次的技术实践感受。欢迎大家后面积极参与一起讨论。向大家学习。

![3.pic_hd.jpg](http://upload-images.jianshu.io/upload_images/80690-b5eaff80f0bcad5c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

首先，简单地介绍一下我自己。
我在移动数据及监控组。以前一直做iOS开发，最近在做RN开发。
平时喜欢健身、看算法方面的书。欢迎大家找我一起健身和讨论算法相关的话题。

![4.pic_hd.jpg](http://upload-images.jianshu.io/upload_images/80690-6cd4c57094087ad6.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

旅行喵，是一款帮助用户快乐旅行的APP。
第一版的首打功能是行程定制，和景点信息介绍。大家可以在上面做非常简单的偏好选择，通过我们的智能算法生成适合自己的旅行路线。

![5.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-8c553d5228e26029.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为什么要用RN呢？
首先，相对于其它可以方便热更新的开发方式，RN在性能、可扩展性、代码维护上，有一定的优势。
其次，在人力资源利用上，相对于Native开发，也有一定的优势。我们最开始的时候只有3个人参与开发。后面为了让更多人熟悉RN这个技术，陆陆续续加了4､5个人进来。当然熟悉RN后又抽出去做其它项目了。基本上，新加进来的人，只要一周就可以独立开发。现在如果有一些简单的迭代，我自己一个人就可以快速完成iOS和Android两个端的维护。

![6.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-67c44e4df01e279c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

RN的高扩展性，得益于它可以同时复用JS组件和Native组件。这样一来，大家现在手头上比较成熟完善的Native已经实现的功能就只需要简单引用，不用重复开发。
对Native组件的复用，RN有两种形式，一种是不带UI的原生模块。使用过程非常简单。三步就完成Native端原生模块的暴露，两步就完成JS端模块方法的调用。

![7.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-d516c57942948477.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

另一种是带UI的原生UI组件。使用过程也十分简单。无非是在Native端增加一个View子类，和一个ViewManager子类。在JS端通常会把原生UI组件做成一个React组件再进行调用。

![8.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-d58a7a41cfb7fa0a.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

刚才大家看旅行喵的介绍，可能也能猜到，旅行喵上面有大量的图片。为了节省用户流量和提高图片加载速度，我们做了图片缓存的功能。在iOS和Android上分别通过原生UI组件的方式实现。
除了图片以外，我们还做了简单的数据缓存功能，主要用来存用户的登录信息，免除用户经常重复登录的麻烦。

![9.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-286c2d03d0763541.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

RN刚开始出来的时候，动画功能很弱。经过多个版本迭代以后，现在已经可以完成很多简单的动画。
RN有两个动画组件。Animated适合做比较精细的视图动画控制。LayoutAnimation比较适合做过场动画。

![10.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-f734fae39187719d.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们在开发过程中，碰到了一个比较麻烦的手势响应传递的问题。列表，本身是支持上下滚动手势的。但，当我们在单元格上增加了左右滑动的手势后，发现单元格的手势把列表的手势响应完全拦载了。
后来，我们把小于45度角的手势定义为左右滑动，交给单元格响应。大于45度角的手势定义为上下滚动，交给列表响应。解决手势响应冲突的问题。

![11.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-25bc3da6c8a9dec3.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

旅行相关APP，自然少不了地图。
我们把第三方地图SDK做成原生UI组件。然后在JS端做成React组件。
这样就可以非常方便地和RN的标准组件嵌套实现功能页面。

![12.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-9534a7f331210508.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为了更好地向用户展示景点信息。我们接入了RN视频组件react-native-video。
RN组件，使用非常方便，只需要一个命令就可以把它接入到工程。
我们在react-native-video的基础上，封装了加载视频预览图和播放按钮的功能。

![13.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-558b38055a9a3017.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

旅行喵的用户除了可以使用APP自带的头像以外，还可以自定义自己的个性化的头像。
为了实现这个功能，我们接了一个图像选择器组件。它具有拍照和访问手机相册的功能。

![14.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-29b259456d34091d.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


选完图片，我们还要上传到服务器。我们接了一个文件上传RN组件。大家可以浏览一下右边代码，使用非常简单。

![15.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-20d2e952bbabffd0.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

旅行喵为了最大限度地让用户尽可能无障碍体验APP的功能，我们绝大多数的操作，都不需要用户进行登录。那么用户在未登录状态下的操作，怎么在登录后和用户帐号绑定呢？
我们通过用户设备信息来进行绑定。
除了操作绑定以外，我们每个请求都会给后端带上用户设备信息，方便后台做相应的用户数据录入。

![16.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-22153aafe2d0c9e7.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

iOS平台不支持直接加载显示GIF图片，这导致RN在iOS平台也无法直接加载显示GIF图片。
我们在iOS平台上做了一个GIF加载原生UI组件。然后在JS端做成React组件。这样就可以非常方便地和RN的标准组件嵌套使用。

![17.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-ad11a068fa3e0637.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

除了前面讲到的比较大的功能，RN里面也有很多比较小的但非常实用的功能、UI组件。
比如可以做倒计时的Timer组件。用来做验证码发送倒计时啊，或者其它有时间限制的功能，都非常好用。

![18.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-d597b379a2a7691f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

RN刚开始出来的时候，很多人都担心屏幕适配方面会不会很麻烦。
我们开始做项目的时候，业界还没有什么成熟的方案提出来。
我们和设计师协商之后，决定以6 Plus为基准，通过一套机制把设计文档上标注的像素转换不同设备类型的像素点进行适配。

![19.pic_hd.jpg](http://upload-images.jianshu.io/upload_images/80690-6c32066180c6096b.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

旅行喵上面有大量的图片加载。有部分图片相对大一点，有时候会出现加载慢，甚至加载失败的情况。
我们通过Image组件的接口对图片加载过程进行的监控。实现了默认图片，开始加载，加载成功，加载结束，加载失败后的重新加载的自定义处理。提升了整个APP图片加载的体验。

![20.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-323deead21102995.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

RN最开始的版本，崩溃率特别高，动不动就红屏。当然，现在迭代了这么多个版本后，稳定了很多。
如果你不想让APP在用户面前出现红屏，可以使用异常捕获组件ErrorUtils暂时解决。当然，你应该建立一套异常记录和上报的机制，保证自己事后可以去跟踪解决问题。
在开发阶段，我们可以在一些不应该走的分支里通过throw new Error主动抛出异常，来避免写出不够健壮的代码。在提交代码前，要记得把相应的throw去掉。

![21.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-b7e16a436ed7daea.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在开发的过程中，必然需要对代码进行调试。RN的调试也非常方便，在开发者菜单上开启浏览器调试就可以输出相应的Log信息。
我们比较习惯在Chrome上调试，在Sourse标签可以看到源码和Log输出，也可以打印相关的对象和变量，还能设置断点和单步执行。非常方便。
除了用模拟器调试之外，我们还可以进行真机调试。要保证手机和JS的服务在同一个WIFI下。

![22.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-16028640139e1fb1.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

功能开发完了，除了在自己的开发机上运行测试。我们还可以给同事打个包，把JS文件安装到同事的手机上，让他们帮忙测试体验。
打离线包，只需要一个命令: react-natvie bundle。通过命令参数，指定入口文件、输出文件、平台、资源文件、是否开启开发模式。
打包过程非常快，旅行喵整个APP的JS文件，只需要18秒就可以打包完。

![23.pic_hd.jpg](http://upload-images.jianshu.io/upload_images/80690-f65586e16a69e510.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

给同事装上JS文件后，如果我们想更新，怎么办呢？
我们有一套热更新的方案。分三步走。
第一步，上传打包好的jsbundle文件，并设置对应的JS版本号。后端维护一个根据设备类型对应JS版本的表。包括设备类型、版本号、jsbundle文件下载地址。客户端维护一个.plist文件，里面存储JS版本号和对应的jsbundle文件本地路径，还有当前版本号、回滚版本号、版本黑名单等。
第二步，在APP每次启动，客户端加载当前版本号对应路径的jsbundle文件，并且提供设备类型、当前版本号发JS文件更新请求。后端返回设备支持的最新版本号及jsbundle文件下载地址。客户端检查最新版本信息，如果最新版本不在黑名单，把最新版号设置为当前版本号。
第三步，在下次启动APP的时候，客户端加载最新版本，完成更新。如果APP启动崩溃，把当前版本号加入到黑名单，并回滚版本。

![24.pic_hd.jpg](http://upload-images.jianshu.io/upload_images/80690-f44e4b089a1abbae.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

旅行喵的RN实践，大概就是前面讲的内容。这里面还有很多技术细节可以一起探讨交流，但时间有限，我就先分享到这里。欢迎大家随时找我和我们团队的人交流。
可能有些同事之前只是听说，但还没有怎么接触过RN。现在RN的资料比之前丰富了很多，大家可以看看相应的文档、书籍，就可以完成简单的RN开发。也可以去参加一些RN的技术社区和业界朋友交流互动。
最后，我们旅行喵项目开发积累了一些通用的功能组件，比如地图、视频、图片缓存等等，后面也会整理出来分享给大家。

![25.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-0bbe488a2d6e8463.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我的分享，到此结束，谢谢大家参与。
大家如果有什么疑问，欢迎提出来，我们一起探讨，互相学习。
谢谢！