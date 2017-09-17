参考文档:http://camsong.github.io/redux-in-chinese/index.html
参考Demo:https://github.com/alinz/example-react-native-redux

ReactNative 架构Redux研究
http://www.jianshu.com/p/14933fd9c312

下载Github的Demo后

进项目目录

npm install 装Node_module

LiBinggentekiMacBook-Air:~ libinggen$ cd /Users/libinggen/Downloads/example-react-native-redux-master/Counter 
LiBinggentekiMacBook-Air:Counter libinggen$ npm install

速度慢的话，自己开个Lantern


如果卡在莫名莫妙的地方，可以control+c，取消它再重新来


报警告，我们先不理它。。。[糗大了]



它告诉你，它下了一堆东西，请原谅它的龟速。。。

然后我们先Run一下看会不会红屏

因为家里机子没装Android Studio，我就不展示Android端了哈，大家见谅





我们Run这一下



会弹一个这种东西出来，它告诉你，它正在跑服务



如果没有什么幺蛾子，它会开始打包JS文件



我们只有一个JS文件，很快就打包完



这就是Demo跑起来的样子



点一下两个按钮，看看功能是否正常

好了，下面我们开始看源码



iOS的代码基本不用看，因为里面压根没什么东西

jsCodeLocation = [NSURL URLWithString:@"http://localhost:8081/index.ios.bundle?platform=ios&dev=true"];

这是说，JS文件在哪里，然后打个包

// jsCodeLocation = [[NSBundle mainBundle] URLForResource:@"main" withExtension:@"jsbundle"];

这里把JS文件打包到iPhone里的时候用的

RCTRootView *rootView = [[RCTRootView alloc] initWithBundleURL:jsCodeLocation
moduleName:@"Counter"
initialProperties:nil
launchOptions:launchOptions];

这里的关键是moduleName

它告诉程序哪个JS组件是第一个页面

这里是@"Counter"



对应到index.ios.js里的最后一行代码

AppRegistry.registerComponent('Counter', () =&gt; App);

里的'Counter'



那后面的APP是什么呢？

大家可以看到，它是对应到import App from './app/containers/app';这里的APP

APP还是BPP，还是LIBINGGEN，都无所谓

只要'Counter'这个和iOS里的ModulName对得上就行

现在我们当然是去看看APP这个组件，看看它干了什么



app.js在这里



代码也是老简单

先是一堆import引用

然后是几个const常量

然后就是定义了一个组件 class App 继承自 Component

组件里通过render方法把组件渲染出来

Provider这个组件，把整个应用唯一的放数据的store，和应用主组件CounterApp绑定在一起



这个唯一的store，把根reducer绑定



这里的reducer其实只有一个，就是counter.js

我们看年counter.js这个reducer在干嘛



其实它没干什么

reducer里面有一个状态对象



定义了我们这个App需要的数据对象

这里是count



然后counter作为一个函数，接收两个参数，状态state和行为action

里面就是一个switch语句

根据行为的不同类型，对数据对象里的count做不同的处理

那么，行为有哪些类型呢？

是通过这里引入的：
import * as types from '../actions/actionTypes';




这里只定义了2个行为类型

Provider组件里绑定的整个App唯一的store，以及里面的reducer，就是这个样子而已

下面看看Provider 所包含的子组件，也就是我们整个App的实际根组件CounterApp又干了些什么



CounterApp在这里



首先又是一堆引用



然后定义了一个叫CounterApp的组件，继承自Component



第一件是构造函数，拿到父组件调用此组件时拿过来的属性



然后是渲染函数



从属性里面，分别拿到状态state和行为actions



调用Counter组件，并且把状态里的count值和行为传递给Counter组件



下面还有一个connect组件，它把store的分发函数与CounterApp组件的状态和行为连接在一起

而作为根子组件，Counter组件，又做了什么呢？



Counter组件在这里



先是引用了常用的RN组件



然后定义了一个布局的CSS

styles

这是Demo的源码，懒得改了：）反正不难明白，切换也没什么障碍，自己找相应的文档看看就行了：）



然后就是定义了Counter组件，继承自Component RN组件

里面还是老两件：



构造函数



渲染函数



从属性里拿到数据、行为

哦，漏了一个地方没讲

这两个行为哪里来的？

前面CounterApp组件里的connect组件绑定的







我们先看看都绑定了什么行为



代码在这里



action和reducer都是纯函数

counterActions.js里定义了两个函数，它们分别代表了两个行为

所谓的行为，其实只是一个JS对象，键值对



对象里，定义了一个"type"键，对应的值是types.INCREMENT

这里定义了两个函数，我们称之为两个行为，分别是increment和decrement，它们都只是简单地返回了一个JS对象





counter组件里的两个属性就是这么来的



然后只需要在点击组件(按钮)里，把行为(函数)传给相应的onPress属性，就可以在用户点击里发出对应的行为

reducer在收到行为后，会根据行为的类型，对App 数据counter作相应的修改

如果要在点击事件里传值



只需要在行为里添加相应的键，并把相应的值传过去就可以了



然后在reducer里写好对相应键值的处理

OK，完了

这就是Redux的使用

Redux的源码，我没看，不过网上有博客有讲Redux的源码，大家有兴趣可以看看，或者自己啃也行：）

谢谢大家参与：）