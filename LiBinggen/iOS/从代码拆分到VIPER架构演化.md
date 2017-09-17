####减小焦点，叠加信息

《ViewController代码拆分实践》
http://www.jianshu.com/p/f30438b89bc6

上篇文章里，我们把ViewController按视图、网络请求、本地存储、页面跳转四层进行拆分。

拆分之后，ViewController的代码足够少，而因为是采用协议对象的方式进行拆分，后续的可维护性和可扩展性又足够高。

今天，我们多走一步：实现VIPER架构。

我们看看拆分代码后的ViewController.h。
```
#import "ViewInterface.h"
#import "APIInterface.h"
#import "StoreInterface.h"
#import "RouteInterface.h"

@interface ViewController : UIViewController<ViewInterface>

@property (nonatomic, weak) id<ViewInterface> viewModel;
@property (nonatomic, weak) id<APIInterface> apiHandle;
@property (nonatomic, weak) id<StoreInterface> storeHandle;
@property (nonatomic, weak) id<RouteInterface> routeHandle;
@end
```
引用4个Interface，声明了4个协议对象。把ViewControler里的4个层次的事件消息通过4个协议对象进行分发。

4个，我们还是嫌太多。如果只有1个就好了，这样我们做ViewController消息分发时就不用考虑向哪个协议对象分发了。

说干就干，把4个协议对象合成1个：

```
@interface ViewController : UIViewController<ViewInterface>

@property (nonatomic, weak) id<ViewInterface,APIInterface,StoreInterface,RouteInterface> eventHandle;
@end
```
把原来由4个协议对象分别引用方法的地方，全部改为由eventHandle引用。
```
self.hotList = [self.eventHandle unarchive];
[self.eventHandle loadData];
return [self.eventHandle configureWithCell:cell data:data];
[self.eventHandle pushDetailInterfaceFromViewController:self detailData:detailData];
[self.eventHandle archiveWithObject:self.hotList];
```
把4个Interface的引用，合并成一个：
```
#import <UIKit/UIKit.h>

#ifndef ViewControllerSplit_EventInterface_h
#define ViewControllerSplit_EventInterface_h
@protocol ViewInterface <NSObject>

@optional
- (void)hotListWtihData:(NSArray *)data;
- (UITableViewCell *)configureWithCell:(UITableViewCell *)cell data:(NSDictionary *)data;
@end

@protocol APIInterface <NSObject>

@optional
- (void)loadData;
@end

@protocol StoreInterface <NSObject>

@optional
- (id)unarchive;
- (void)archiveWithObject:(id)object;
@end

@protocol RouteInterface <NSObject>

@optional
- (void)pushDetailInterfaceFromViewController:(UIViewController *)viewController detailData:(NSDictionary *)detailData;
@end
#endif
```
于是ViewController.h被简化到了极致：
```
#import <UIKit/UIKit.h>
#import "EventInterface.h"

@interface ViewController : UIViewController<ViewInterface>

@property (nonatomic, weak) id<ViewInterface,APIInterface,StoreInterface,RouteInterface> eventHandle;
@end
```
我们新建一个实际处理四层消息的类，名字为Presenter：
```
#import <Foundation/Foundation.h>
#import "EventInterface.h"

@interface Presenter : NSObject<ViewInterface,APIInterface,StoreInterface,RouteInterface>
@end
```

至此，我们完成了土制代码拆分到高大上的VIPER架构演化的全部过程。

VIPER，无非是通过Presenter统一转发ViewController的消息，使ViewController从臃肿和紧耦合中解脱出来，让ViewController更小更少依赖，方便维护、复用。

Presenter收到ViewController转发过来的消息，分别向Interactor(API, Store)、WireFrame(View, Route)转发处理。

本质上都一样：通过消息转发，把代码扔出本类，进行黑箱复用。

####后记(下面以聊家常为主，没时间没兴趣的朋友请直接忽略)：
准确地说，我前天晚上非常开心。因为我从《无头骑士异闻录×2》想到了：只有深钻才能摆脱无聊。

我们很害怕生活很普通。普通得自己像没在这个世界存在过一样。但如果我们继续肤浅、表面地活着，不管我们多么有钱有势，还是无法摆脱恐怖的无聊感。

而那些但凡有任何一件事情可以去深钻的人，却不会有这样的无聊感，他们只有深钻精彩的忙碌感。只擅长这个啊。时间不够用不够用啊。

从此，我努去让自己把关注的焦点一再减少缩小，然后把所有时间精力人脉全部投入到这个足够小的点上。通过高强度的信息轰炸，消灭掉这一个点。彻底解决掉它。

随着我越钻越深，自然会有越来越多有趣的人和事会找到我。那时，我只需要随随便便地忙碌着，生活就会被得足够有趣。

我自己做了一家三口焦点表，没有这方面经验的朋友可以参考一下：

我：
老婆| 儿子| 健身| 读书| 编程
日语| 玩具| 腹腰| 算法| 项目

老婆：
老公| 儿子| 健身| 读书| 手工
日语| 玩具| 瑜珈| 天文| 科技

儿子：
妈妈| 爸爸| 健身| 读书| 外出
日语| 玩具| 跑步| 科技| 艺术

世界上的所有事情，无论什么基础，无论什么背景，无论什么环境，通通全部都必须按两步去解决：
1､减小焦点
2､叠加信息

今天想明白一件事情：粉丝群的功能。
粉丝群只有一个功能：粉丝帮助群主思考，粉丝帮助群主做事。

没错，我建粉丝群，不是为了帮任何人，而只是希望能得到别人的帮助。如果你觉得我值得你帮，欢迎进来。如果你只希望我或我的粉丝群友帮你，请你滚开，我踢不留情：）

iOS开发，读书狂魔
清醒疯子利炳根粉丝群:147043528

长久以来，我一直害怕别人觉得我是新手、太弱。其实没关系，我现在确实还很新手很菜很弱啊。但，不管怎么样，我会继续努力啦。

分享一部纪录片《中国的秘密》
http://qianmo.com/u/6292/5