#序言

这是一个在StuQ做分享时的讲稿。当然还有很大的改进空间，但我这会却没有什么劲头继续改进，既然这样就不如索性先发出来，先把它从脑袋清出来，把其它我更想做的事情做了，回头再看哪天想改了再回来改。

当然，大家有觉得不对的地方，随便批，我会当做问题之一，以后努力改进：）

#分享环节：

![00.jpg](http://upload-images.jianshu.io/upload_images/80690-1cf5e4989c5737f0.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

大家好，我是深圳平安科技的利炳根。网名：清醒疯子。主要研究iOS和ReactNative。
今天和大家分享的是我在ReactNative上的一些开发实践经验。请大家多多指教。

在ReactNative上的研究，我还是做得比较粗浅，有不对的地方，大家随便批，我多向大家学习。


![01.jpg](http://upload-images.jianshu.io/upload_images/80690-9ff6c26de48474a5.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
今天的内容分为四个部分。分别的ReactNative的开发环境搭建、JS/Bundle的管理、混编以及数据流的处理。


![3.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-cddf0a53814b93fe.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

ReactNative的开发环境搭建比较简单。只需要把node、watchman、flow通过brew安装完，通过npm把ReactNative命令行安装到全局，就可以用init命令创建ReactNative项目。

其中，node是node.js。它有非常好用的包管理工具npm。也可以拿来写后台。我自己经常拿来在本地快速写一些简单的后台辅助调试代码。

watchman是Facebook的开源项目，主要用来监视文件，记录文件的改动。React通过watchman来实现代码发生变化时完成相关的重建功能。

flow也是Facebook的开源项目，用来做JavaScript的静态类型检查。用来发现JS程序里的类型错误，提高编码效率和代码质量。包括前期错误检测、代码智能提示等。

安装ReactNative命令行的时候要注意加上-g这个参数，把RN命令行安装到全局，才方便我们在任何目录通过命令行创建ReactNative项目。

ReactNative项目创建的时候，会自动把一些需要用的库加到项目工程里，自动做好基本的依赖管理，并且自动生成最简Demo代码。创建完之后就可以运行一个最简单的Demo，方便大家体验ReactNative的编程。


![4.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-be5e02db48ff4492.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

目前，ReactNative还没有特别好用的开发工具。开发效率会稍微打点折扣。但利用现有的开发工具还是足够完成基本的开发任务的。

Nuclide是Facebook的开源项目，是与Ract配套的IDE。目前还在不断地完善当中。已经能实现基本的代码提示和静态类型检查。Nuclide目前还不是独立的IDE，需要作为Atom的包进行安装。

Atom和WebStorm都可以做到React的部分代码提示。对ReactNative的支持就相对差一些。主要还是针对JavaScript的支持而已。

ReactNative的JSX只是JavaScript的封装。一些在JavaScript上的打包工具，ReactNative也能用。比如Browserify和Webpack。

Browserify使用比较简单。指明入口点和出口点就可以打包。而Webpack则一般要写一个配置文件webpack.config.js指明打包细节。当然，Webpack的功能相对就更强大一些。

Nuclide的开源项目代码提交还是比较活跃的，对这方面有兴趣的朋友不妨关注一下，参与其中和大神一起做一个IDE也不失为一种相当不错的娱乐项目。



![5.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-bf53c1a76c2f336c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

虽然ReactNative最终会渲染成Native的View，但它只能通过浏览器调试。基本上就是用Chrome来做。

Chrome上有一个插件React Developer Tools，不过要翻墙才能装。

通过Chrome的consle可以打印变量。如果对这块不熟悉的话，可以先通过调用一个网络请求，打印返回的数据，并根据数据调整显示，来熟悉一下Chrome的调试过程。

在JavaScript代码中插入debugger;就可以作为调试过程中的断点。


![6.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-b934b4aacbef7fff.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在iOS平台上，ReactNative组件通过RCTRootView这个类接入到Native的视图层次里头。

RCTRootView初始化只需要提供两个参数，一个是JS包的路径，一个是模块的名称。

ReactNative的应用组件，最后渲染出来都是一个View的子类，都可以通过addSubView加到Native的视图层次上面。


![7.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-cf46e9933d6b1fb5.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

ReactNative可以实现动态编码。只需要在远端修改JS文件并保存，Native端无需重新编译，只需要Reload刷新一下，就可以更新APP视图和功能。

在设置RCTRootView的JS包地址时，设置为远端的JS文件资源网址，在引用时把文件后缀改为.bundle，即可以调用远端的ReactNative bundle命令，把对应的JS文件打包为可用的JS包文件，在Native端实现视图的渲染。

bundle命令有两个常用的参数。platform参数指定打包到iOS平台还是Android平台。dev参数指定是否开启开发选项以提供更多的调试信息。


![8.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-45baf40e9a1ffeff.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

调用远端JS文件打包的方式有一个缺点，打包过程导致视图初次加载比较慢，影响用户体验。可以过加载离线包的方式解决这个问题。

在设置RCTRootView的JS包地址时，设置为Native端沙盒内的jsbundle文件地址，ReactNative就可以从Native端加载渲染视图，速度有明显提升。

通过bundle命令，可以把JS文件打包成jsbundle包。bundle命令有三个常用参数。platform参数指定平台，entry-file参数指定入口文件，bundle-output参数指定出口文件。


![9.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-626888d2220b33e8.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过加载Native端离线包jsbundle文件，在提升加载速度的同时也让ReactNative失去了远端更新的能力。这样得不偿失。我们可以通过静默下载jsbundle文件替换Native端jsbundle文件的方式解决这个问题。

通过远端jsbundle文件资源网址，启动一个下载文件请求。在收到请求返回的时候设定文件路径。在收到返回数据时写文件。

写文件时，要注意先让写入点移动到文件末尾，再进行文件写入，避免覆盖之前接收到的数据。


![10.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-6a8bdda101d0cbe7.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

ReactNative因为技术发展不久，还有部分Native端的功能并没有完全实现。在项目开发过程中有可能需要在ReactNative项目里加入Native端的功能代码辅助。

ReactNative有一套机制实现。在Native端的类里引用RCTBridgeModule，并遵循RCTBridgeModule协议。通过宏RCT_EXPORT_MODULE向JS暴露Native端的类，通过宏RCT_EXPORT_METHOD暴露Native端的方法，通过RCTResponseSenderBlock实现JS端的回调。


![11.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-c0e7da1cdb60abcd.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

JS端的处理和Native端同样简单。在JS文件的开始引用NativeModules组件。通过NativeModules引用Native端指定类。由Native端指定的类就可以直接调用指定的方法并指定回调的实现。


![12.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-b98ff95d18fc43c8.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Native项目添加ReactNative模块稍微复杂一点。首先需要进行一些工程配置。把ReactNative需要的静态库加到工程里。在Build Settings里设置Other Linker Flags 和Header Search Paths。最后还要在Info.plist里设置App Transport Security Settings -> Allow Arbitrary Loads。


![13.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-20635f9f43bf0117.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在Native的类中引用RCTBridge和RCTEventDispatcher。通过bridge的eventDispatcher向JS端派发事件。派发事件的接口有5个，分别对应5个不同的事件类型。

这里要注意，不要在Native端的viewDidLoad方法里向JS发送事件消息，因为这个时候ReactNative组件还没有挂载出来，接收不到消息。


![14.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-9d2541db96f6d5de.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

JS端在文件一开始引用NativeAppEventEmitter组件。通过NativeAppEventEmitter组件的addListener方法监听Native端派发的事件消息。组件卸载时，通过NativeAppEventEmitter组件的removeAllListeners方法移除监听。


![15.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-6cf894d8032baed8.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

ReactNative的数据流处理，目前业内有4种方案。原生的ReactJS通过Props - States - Components的机制处理数据流。

缺点很多。扩展性差，增加新功能时，需要在每一个用到的组件里复制一遍代码。

可读性、可维护性差，代码量大，难以调试、测试。

可移值性差，代码耦合度高，视图、数据不分层。

违背单一数据层原则，在视图层直接进行数据操作。


![16.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-af187708ca38301b.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Facebook官方推荐的Flux，通过Actions - Dispatcher-Stores - Component的机制处理数据流。

代码冗长，Dispatcher和Store有很多重复烦琐的人工检查、定义。

多个Store中处理同一个Action，将产生大量的waitFor方法处理Store的先后逻辑。

多个Store间共享一个State，State有可能被分散到多个Store中，State的变化将变得不可控。

多个Store互相依赖，还有可能产生依赖循环。


![17.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-d4bfc50f347535e8.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Redux通过Actions -Store - Components的机制处理数据流。

Redux针对Flux做了不少优化。通过内部拓展actions的行为，移除了单例的dispatcher。stores可以监听actions的行为，无需进行冗杂的switch判断。

stores可以相互监听，可以进行进一步的数据聚合操作。waitFor方法被连续和平行的数据流所替代。

Redux也有自身的一些弊端。由于整个应用的数据都集中在1个Store里，数据和处理逻辑的复杂度将不可避免地变高。

因为语法相似，从ReactJS、Flux迁移到Redux成本较低，建议旧项目迁移采用Redux。


![18.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-ab2c8844c8c739a1.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Baobab通过Actions -Baobab Tree - Components的机制处理数据流。

Baobab的优点十分明显。应用所有状态都存在一棵数据树里。可以非常简单地实现数据域的切换。应用状态树的存在使得数据流管理变得非常简单，代码量少。

通过Baobab库创建状态树，数据以键值对的方式存储。

Baobab通过select方法直接切换数据节点，还可以通过cursors创建数据游标组，访问数据。

Baobab通过set方法修改数据。

如果项目新建，没有旧代码维护的包袱，个人建议采用Baobab来处理数据流，一定会更省事省力。

结束语：

我的分享到此结束，非常感谢大家今天来参加，希望上面分享的内容能对大家有所帮助。如果大家对ReactNative或者其它问题想跟我交流，欢迎到我的支付宝经费群来。


![19.pic.jpg](http://upload-images.jianshu.io/upload_images/80690-ce8d35e535d79178.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#问答环节：

1.能说说选择相较PhoneGap,ionic等些其他平台,为什么选择React么?
PhoneGap是比较早期的技术，一直以来，在性能上或者功能的覆盖上，大家都不够满意。尤其是性能。RN因为最终是渲染成Native的View ，体验上就好很多。同时呢，因为RN是Facebook在推，从Github上的Star，大家也可以看出业界还是对Facebook有很大的期待和信心的。

2.请问rn中的组件出现相互嵌套的问题可以怎么解决？即 a require b， b 也require a。当调用a时，就会b=null了。可以用es6的模块解决吗？
这就是涉及到数据流的处理。如果用原生的ReactJS去处理，是会非常麻烦的。Facebook希望Flux能解决这个问题，但实际下来，大家觉得满足不了需求。然后业界就有了Redux和Baobab两种方案。Baobab是最新的方案，解决方式也最优雅，大家有兴趣可以重点研究一下。

3.既然是在Mac下，为什么不用safari调试，当前safari调试窗口也是很棒的
在我自己这边主要是习惯问题。一直以来用的都是Chrome。因为很早之前调试API啊各种东西都是用Chrome搞。既然Chrome能搞定就懒得换了。

4.Native与js调用时，与hybrid方式的app有什么不同。
RN的双向通信还是做得比较好的，上面的分享也有讲到，实现起来非常简单。我在这上面多花了一点时间，也只是因为把发消息的代码放到了AppDelegate上，结果死活收不到。Hybrid，常见也是用Bridge。这块的麻烦是，需要HTML5的同事配合。

5.再请教一个问题。组建多层嵌套时，组建间该如何通信？特别是最底层跟顶层的通信，除了props之外，还有啥好办法吗
这个其实就是第四部分数据流的处理问题。Baobab可以把数据统一到一个地方，而且数据域切换非常方便，可以看看。

6.提问：React Native对安卓的支持情况，是否能兼容如此碎片化的安卓
目前，我们还没有去处理具体的适配。这块因为主要是Android的同事在研究，我也不大清楚。不过，既然很多大厂都有用RN，应该不会有太大问题。

8.没有ios经验，只有reactjs经验的，怎么上手xcode下react native开发配置呢，或者android下的
Native下的工作量是非常少的。基本上只要随便找几篇入门的文章看看，问题就不大了。遇到搞不定的问题多上stackoverflow搜搜。或者找我交流也可以：）

9.rn在开发团队中的分工如何，如界面，js，ios程序员如何合作
目前我们是1个iOS和1个Android，然后就是后端了。其实重点的开发量反而是JS上的。一旦把平台需要配合的东西摸清，剩下的主要工作量就是写JS了。两个平台的多数组件都是可以共用的，也就是很多代码只要写一份就可以了。

11.rn适合渲染view还是处理各种逻辑呢，有不如原生的地方吗
目前为止，我还是学习RN就算是View上也做得没有Native漂亮。如果逻辑比较复杂，是不是适合全部用RN来做，还有待考察。RN目前主要的针对点还是迭代比较快的相对轻一点的业务。反正熟悉之后，混编是非常简单的事情，大不了拿Native做一个复杂业务的API：）

问题回答完毕：）

#招聘环节

招聘：深圳平安科技移动开发架构师团队，iOS/Android/Java/HTML5/测试/运营都招。15薪，过节费丰厚，内部福利众多，欢迎大家自投或推荐。简历直接微信发给我就可以了，尽量用PDF文件。