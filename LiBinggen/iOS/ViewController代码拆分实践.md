####日常里的异常，人生至乐！

如果你才刚刚接触iOS开发，可以先看看我写的另一篇文章《从零开始学iOS开发的15条建议》http://www.jianshu.com/p/8472ba0f2bb6

首先，创建一个Single View Application。
![Single View Application](http://upload-images.jianshu.io/upload_images/80690-c2d5bde9cd47b61d.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 接着，找来一个数据API，这里以V2EX的公开API为例：
https://www.v2ex.com/p/7v9TEc53

我们只拿其中一个API:首页右侧的 10 大每天的内容。
https://www.v2ex.com/api/topics/hot.json

AppDelegate.m
```
@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {

    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    self.window.backgroundColor = [UIColor whiteColor];

    ViewController *viewController = [[ViewController alloc] init];
    UINavigationController *navigationController = [[UINavigationController alloc]initWithRootViewController:viewController];
    self.window.rootViewController = navigationController;

    [self.window makeKeyAndVisible];

    return YES;
}
```
ViewController.m
```
@interface ViewController ()<NSURLConnectionDataDelegate,UITableViewDataSource,UITableViewDelegate>

@property (nonatomic, strong) NSMutableData *receiveData;
@property (nonatomic, strong) NSArray *hotList;

@property (nonatomic, strong) UITableView *tableView;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.hotList = [NSKeyedUnarchiver unarchiveObjectWithFile:[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0] stringByAppendingPathComponent:@".hotListArchiver"]];
    [self.tableView reloadData];

    self.receiveData = [[NSMutableData alloc]init];
    NSURL *url = [[NSURL alloc]initWithString:@"https://www.v2ex.com/api/topics/hot.json"];
    NSURLRequest *request = [[NSURLRequest alloc]initWithURL:url];
    NSURLConnection *connection = [[NSURLConnection alloc]initWithRequest:request delegate:self];
    
    CGRect frame = [[UIScreen mainScreen]bounds];
    self.tableView = [[UITableView alloc]initWithFrame:frame];
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    [self.view addSubview:self.tableView];
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return self.hotList.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *cellIdentifier = @"cellIdentifier";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:cellIdentifier];
    if (!cell) {
        cell = [[UITableViewCell alloc]initWithStyle:UITableViewCellStyleValue1 reuseIdentifier:cellIdentifier];
    }
    
    cell.textLabel.text = self.hotList[indexPath.row][@"title"];
    cell.imageView.image = [UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:[NSString stringWithFormat:@"http:%@",self.hotList[indexPath.row][@"member"][@"avatar_mini"]]]]];
    return cell;
}


- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
    [self.receiveData appendData:data];
}

- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    NSError *error = nil;
    self.hotList = [NSJSONSerialization JSONObjectWithData:self.receiveData options:NSJSONReadingAllowFragments error:&error];
    [self.tableView reloadData];

    NSLog(@"hotList\n%@",self.hotList);
    [NSKeyedArchiver archiveRootObject:self.hotList toFile:[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0] stringByAppendingPathComponent:@".hotListArchiver"]];
}
```
DetailViewController.h
```
@interface DetailViewController : UIViewController

@property (nonatomic, strong) NSDictionary *detailData;
@end
```
DetailViewController.m
```
@implementation DetailViewController

-(void)viewDidLoad
{
    self.title = self.detailData[@"title"];
}

@end
```
代码运行效果：
![ViewController](http://upload-images.jianshu.io/upload_images/80690-01522cf1b55d892c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![DetailViewController](http://upload-images.jianshu.io/upload_images/80690-b887727fd7bb2a46.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面，我们开始拆。

首先，创建接口 Interface。

![创建接口 Interface](http://upload-images.jianshu.io/upload_images/80690-a00b8367ad26b371.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后，创建相应的类。

![创建相应的类](http://upload-images.jianshu.io/upload_images/80690-58794b262f0535e3.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

把代码移到相应的类里：
ViewController.h
```
@interface ViewController : UIViewController

@property (nonatomic, weak) id<ViewInterface> viewModel;
@property (nonatomic, weak) id<APIInterface> apiHandle;
@property (nonatomic, weak) id<StoreInterface> storeHandle;
@property (nonatomic, weak) id<RouteInterface> routeHandle;
@end
```
ViewController.m
```
@interface ViewController ()<UITableViewDataSource,UITableViewDelegate>

@property (nonatomic, strong) NSMutableData *receiveData;
@property (nonatomic, strong) NSArray *hotList;

@property (nonatomic, strong) UITableView *tableView;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self initUI];
    self.hotList = [self.storeHandle unarchive];
    [self tableViewReloadData];
    [self.apiHandle loadData];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
}

-(void)initUI
{
    self.title = @"最热10条";
    CGRect frame = [[UIScreen mainScreen]bounds];
    self.tableView = [[UITableView alloc]initWithFrame:frame];
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    [self.view addSubview:self.tableView];
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return self.hotList.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *cellIdentifier = @"cellIdentifier";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:cellIdentifier];
    if (!cell) {
        cell = [[UITableViewCell alloc]initWithStyle:UITableViewCellStyleValue1 reuseIdentifier:cellIdentifier];
    }
    NSDictionary * data =self.hotList[indexPath.row];
    
    return [self.viewModel configureWithCell:cell data:data];
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    NSDictionary *detailData = self.hotList[indexPath.row];
    [self.routeHandle pushDetailInterfaceFromViewController:self detailData:detailData];
}

- (void)tableViewReloadData
{
    [self.tableView reloadData];
}

- (void)hotListWtihData:(NSArray *)data
{
    self.hotList = data;
    
    [self tableViewReloadData];
    [self.storeHandle archiveWithObject:self.hotList];
}
@end
```

ViewModel.m
```
@implementation ViewModel

- (UITableViewCell *)configureWithCell:(UITableViewCell *)cell data:(NSDictionary *)data
{
    cell.textLabel.text = data[@"title"];
    cell.imageView.image = [UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:[NSString stringWithFormat:@"http:%@",data[@"member"][@"avatar_mini"]]]]];
    return cell;
}
@end
```
APIHandle.h
```
@interface APIHandle : NSObject<APIInterface>
@property (nonatomic, weak) id<ViewInterface> viewModel;
@end
```
APIHandle.m
```
@interface APIHandle()<NSURLConnectionDataDelegate>

@property (nonatomic, strong) NSMutableData *receiveData;
@end

@implementation APIHandle

- (void)loadData
{
    self.receiveData = [[NSMutableData alloc]init];
    NSURL *url = [[NSURL alloc]initWithString:@"https://www.v2ex.com/api/topics/hot.json"];
    NSURLRequest *request = [[NSURLRequest alloc]initWithURL:url];
    NSURLConnection *connection = [[NSURLConnection alloc]initWithRequest:request delegate:self];
}

- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
    [self.receiveData appendData:data];
}

- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    NSError *error = nil;
    id data = [NSJSONSerialization JSONObjectWithData:self.receiveData options:NSJSONReadingAllowFragments error:&error];
    NSLog(@"data\n%@",data);
    
    [self.viewModel hotListWtihData:data];
}
@end
```
StoreHandle.m
```
@implementation StoreHandle

- (id)unarchive
{
    return [NSKeyedUnarchiver unarchiveObjectWithFile:[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0] stringByAppendingPathComponent:@".hotListArchiver"]];
}

- (void)archiveWithObject:(id)object
{
    [NSKeyedArchiver archiveRootObject:object toFile:[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0] stringByAppendingPathComponent:@".hotListArchiver"]];
}
@end
```
RouteHandle.m
```
#import "DetailViewController.h"

@implementation RouteHandle

- (void)pushDetailInterfaceFromViewController:(UIViewController *)viewController detailData:(NSDictionary *)detailData
{
    DetailViewController *detailViewController = [[DetailViewController alloc]init];
    detailViewController.detailData = detailData;
    [viewController.navigationController pushViewController:detailViewController animated:YES];
}
@end
```
AppDelegate.m
```
#import "ViewModel.h"
#import "APIHandle.h"
#import "StoreHandle.h"
#import "RouteHandle.h"

@interface AppDelegate ()
@property (nonatomic, strong) ViewModel *viewModel;
@property (nonatomic, strong) APIHandle *apiHandle;
@property (nonatomic, strong) StoreHandle *storeHandle;
@property (nonatomic, strong) RouteHandle *routeHandle;
@end

@implementation AppDelegate


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    self.window.backgroundColor = [UIColor whiteColor];
    
    ViewController *viewController = [[ViewController alloc] init];
    viewController.viewModel = self.viewModel;
    self.apiHandle.viewModel = viewController;
    viewController.apiHandle = self.apiHandle;
    viewController.storeHandle = self.storeHandle;
    viewController.routeHandle = self.routeHandle;
    
    UINavigationController *navigationController = [[UINavigationController alloc]initWithRootViewController:viewController];
    self.window.rootViewController = navigationController;
    
    [self.window makeKeyAndVisible];

    return YES;
}

- (ViewModel *)viewModel
{
    if(!_viewModel)
    {
        _viewModel= [[ViewModel alloc] init];
    }
    return _viewModel;
}

- (APIHandle *)apiHandle
{
    if(!_apiHandle)
    {
        _apiHandle= [[APIHandle alloc] init];
    }
    return _apiHandle;
}

- (StoreHandle *)storeHandle
{
    if(!_storeHandle)
    {
        _storeHandle= [[StoreHandle alloc] init];
    }
    return _storeHandle;
}

- (RouteHandle *)routeHandle
{
    if(!_routeHandle)
    {
        _routeHandle= [[RouteHandle alloc] init];
    }
    return _routeHandle;
}
```

####后记(下面以聊家常为主，没时间没兴趣的朋友请直接忽略)：
在日常中积累越多的人，生活越感无聊，虽然在外人看来顺风顺水。
在异常中辛苦存活的人，生活快感无比，虽然在外人看来非常凶险。
人活一辈子，究竟为了什么呢？：）终究难逃一死啊。或快又或慢。
这是一个非常有意思的问题。有意思的根本在于这一个问题的残酷。
因为，追问之下，多数人都只能回答：我一直不知道！！！！！！！
不要那么笃定啊！不要逃避不确定性啊！人生摇摆中存活才会有趣！

我一直以为，我需要异常来让自己觉得自己是生物而不是死物。
但，真正的异常在哪里呢？最大的异常在哪里呢？
最大的异常，在日常里。
让日常变得异常。
日常非常美丽。整整齐齐，稳稳当当。
如果，日常可以异化，异化成另一种整整齐齐、稳稳当当，那就太好玩了。
如果，可以让这个世界异化成另一种日常。让人们习惯异化，就太好玩了。

寻找日常里的可异化的点，用尽一生去把它异化成日常，那就会太好玩了。

这次找到了一个点：）
递减：）

长久以来，我们被教导要去追求多样性，要丰富。
这是最大的陷阱。
因为，我们会被个体的多样性削弱群体的多样性。
相反，如果我们能回归个人的单一性却可以创造出最广泛的群体多样性。

所以，我们要放弃扩张，而是尽自己一切的努力去收缩。
把触角收缩到以自我为中心的极致小的那个点。
那个，除了自己，任何人都不可能有的点。
当，我们都能找到自己的点，这个世界就有70个点。
相反，看看我们身边的这个世界，不停地扩张、积累，最好大家都在吃一样的食物，穿一样的衣服，看一样的娱乐，过一样的人生。
看似极大丰富，实则是极尽无聊。

不外寻，只自问。
通过永不停止的递减，以退为进，找到自己那唯一的点。
不要再被这个世界繁杂所拖累了。

####回归本心，重新出发。
####深挖日常！向日常深处进军！
####日常深处有无尽的独一异常！