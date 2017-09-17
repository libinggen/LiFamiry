三种组件类型，View视图，Text文本，Image图片，其它类型的组件如果需要创建动画，可以使用 Animated.createAnimatedComponent 方法实现。

两个值方法, Value处理单个值(一维)，ValueXY处理向量值(二维)。ValueXY包含两个Animated.Value实例包装。

三个动画方法，spring（弹跳，friction磨擦力默认7, tension张力默认40），decay(衰减，velocity起始速度必填， deceleration速度衰减比例默认为0.997)，timing（时间， duration持续的时间单位毫秒默认500, easing定义曲线渐变函数，delay:延迟执行时间单位毫秒默认为0）。

Animated只关注动画输入输出声明。在Animated里建立可配置变化函数，使用start/stop方法控制动画执行。

单个动画：

1.创建动画值。
2.创建动画组件。
3.绑定动画值：组件样式属性/props，手势／事件。
4.设置动画值插值，输入区间，映射到输出区间，可以定义多个区间段落，支持Easing类渐变函数，支持限制输出区间。
5.toValue可以设置成动态值／插值／动画值。
6.设置动画值的初始值。
7.选择动画类型，选择动画值，设置目标值和参数，执行动画(回调函数({finished: true}))。

组合动画：
分为parallel（同时执行），sequence（顺序执行），stagger（错开执行），delay（延迟执行）。接受动画数组，自动调用start/stop。一个动画停止，其它动画也停止。Parallel的stopTogether属性设false可以禁用自动停止。

Animated.event，手势或其它事件绑定动态值。映射语法解开事件对象值。第一层是数组，可以同时映射多个值。数组元素是嵌套的事件对象。

可以通过回调函数响应当前动画值。
.stopAnimation(callback)，停止动画把最终值传递给回调函数callback。
spring.addListener(callback)， 动画执行过程中异步调用callback回调函数，提供最近值作为参数。

Animated.Value.addListene，可能会有性能问题。
Animated做好序列化配置，在高优先级线程执行动画。比调setState重新渲染更高效。

手Q的TAT.will有篇文章写得非常好，大家可以去看看：）
http://www.alloyteam.com/2016/01/reactnative-animated/
ReactNative Animated动画详解

欢迎加我微信交流：qingxingfengzi