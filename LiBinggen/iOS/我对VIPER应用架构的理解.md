1、VC里除了View的相关逻辑，所有逻辑处理通过Presenter转发。﻿

2、VC间的跳转由Ｗireframe/Route完成。﻿

3、Presenter把视图相关逻辑转给Route，把(数据)模型相关逻辑转给Interactor。﻿

4、Interactor通过DataManager管理数据实体，回调通过Presenter转发。﻿

5、DataManager管理数据实体、本地数据库和获取网络数据。