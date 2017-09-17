我只是实现了，没时间优化。大家随便看看，如有需要，请自行优化。

1､集成百度地图，很简单，自己到网上搜。实在搞不定，找百度客服。

2､建一个View类，一个ViewManager类。

![44.RCTBaiduMap.h.jpg](http://upload-images.jianshu.io/upload_images/80690-831ab243e73374ff.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![46.RCTBaiduMap.m.jpg](http://upload-images.jianshu.io/upload_images/80690-58f2996df3543da5.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![45.RCTBaiduMapManager.h.jpg](http://upload-images.jianshu.io/upload_images/80690-48454dc70a71bdc5.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![47.RCTBaiduMapManager.m.jpg](http://upload-images.jianshu.io/upload_images/80690-1598cfdcdb5d4d32.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、建一个ReactNative的JS类，把原生的百度地图UI组件作为JS组件使用。

![48.BaiduMapView.ios.js.jpg](http://upload-images.jianshu.io/upload_images/80690-0b3ff8f2b60018ca.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4､在任何ReactNative组件中引入JS组件，即可实现与原生百度地图SDK的交互。


![49.TravelMapView.ios.js.jpg](http://upload-images.jianshu.io/upload_images/80690-b132ee4131ebe890.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

完。
PS：经过几天和老婆的深入讨论，我们决定最近会把所有空余时间用来一起学习算法：）

![1.微信群.jpg](http://upload-images.jianshu.io/upload_images/80690-10d313bcd9894ee6.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![2.支付宝群.jpg](http://upload-images.jianshu.io/upload_images/80690-16bfafe40835624f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)