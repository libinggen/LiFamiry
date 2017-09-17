​GAN应用集中在图像生成，NLP、Robt Learning也有拓展。类似于NLP中的Actor-Critic。 https://arxiv.org/pdf/1610.01945.pdf 。

Generative Adversarial Nets。构建两个网络，一个G生成网络，一个D区分网络。训练，G网络loss log(1-D(G(z)))，D网络loss -(log(D(x))+log(1-D(G(z)))，不是Cross Entropy。数据输入，G网络输入noise。D输入混合G输出数据及样本数据。

G网络训练，D(G(z))趋近于1,G loss最小。D网络训练 2分类，分清真实数据和生成数据，真实数据D输出趋近1,生成数据输出D(G(z))趋近0。

目标，生成数据分布和实际分布相同。D开始训练，分类能力有限，有波动，初步区分实际数据和生成数据。D训练较好，明显区分生成数据，生成数据概率下降。G网络提升，影响D分布。G网络不动，训练D，训练最优，Dg*(x)=pdata(x)/(pdata(x)+pg(x)) 。pg(x)趋近pdata(x),Dg*(x)趋近0.5,G网络、D网络处于平衡状态。网络训练最终收敛到pg(x)=pdata(x)。

G、D同步训练，G训练一次，D训练k次。D训练同量输入生成数据和样本数据计算loss(不是cross entropy分开计算)。cross entropy使D(G(z))为0,导致没有梯度，无法更新G。GAN D(G(z))最终收敛到0.5。G网络用RELU、sigmoid，D网络用Maxout和dropout。-log(D(G(z)))代替log(1-D(G(z)))，训练开始加大梯度信息，整个GAN不是完美零和博弈。

GAN可以任意采样，可以使用任意可微模型(任意神经网络)。GAN生成图像更Sharp，work更好，值得推广。不好训练。confitional GAN，半监督学习。

DCGAN，使用卷积神经网络，实现有效训练，拓展维度。去掉G网络D网络的pooling layer。在G网络D网络中使用Batch Normalization。去掉全连接隐藏层。G网络最后一层用Tanh，其它层用RELU。D网络每层用LeakyRELU。

DCGAN网络模型：G网络，100 z->fc layer->reshape->deconv+batchNorm+RELU(4)->tanh64X64。D网络，版本1，conv+batchNorm+leakyRELU(4)->reshape->fc layer 1->sigmoid。D网络，版本2，conv+batchNorm+leakyRELU(4)->reshape->fc layer 2->softmax。
G网络4层反卷积，D网络4层卷积。G网络D网络反结构。D网络最终输出，一种方法，sigmoid输出0到1间单值作概率；另一种方法softmax输出两个值，真概率、假概率。
https://github.com/carpedm20/DCGAN-tensorflow
https://github.com/sugyan/tf-dcgan

GAN训练后网络特征表达。DCGAN+SVM做fifar-10分类实验。D网络每层卷积通过4x4 grid max pooling 获取特征，连起来得28672向量，SVM，效果比K-means好。DCGAN用在SVHN门牌训练，效果不错。D网络无监督学习到有效特征信息。
G改变z向量，生成不同的图片。z向量线性加减，输出新图像。z向量对应特别特征。G网络无监督学习特征表达。
BEGAN生成超级逼真图像。

CGAN(Conditional Generative Adversarial Nets)。数字字段生成，输入数字，输出对应字体。G网络输入 z连接输入y。D网络输入 x连接y。minGmaxDV(D,G)=Ex~pdata[logD(x|y)]+Ez~pz(z)[log(1-D(G(z|y)))]。
GAN无监督变有监督，输入分类，输出图像。
MNIST字体生成，图像多标签。MNIST字体生成，输入数字，输出对应字体。数字one hot处理，5 对应one hot [0,0,0,0,0,1,0,0,0,0]。和100维z向量串联输入。训练调整z向量，改变输出，解决多种输出问题。输出不同形状字体。

InfoGAN，无监督CGAN。信息论，mutual information互信息。G网络输入z+c变量。c与G网络输出x 互信息最大化。神经网络训练c与输出关系。mutual information定义: I(c,G(z,c))=Ec~p(c),x~G(z,c)[logQ(c|X)]+H(c)。H为c的entropy熵，log(c)*c，Q网络基于X输出c。基于I，GAN训练目标：minGmaxDV(D,G)=λI(c,G(z,c))。网络改变：D网络输入只有x,不加c。Q网络D网络共享同一网络，最后一层独立输出。


参考资料：
https://zhuanlan.zhihu.com/p/27012520

欢迎付费咨询(150元每小时)，我的微信：qingxingfengzi

我创建GAN日报群，以每天各报各的进度为主。把正在研究GAN的人聚在一起，互相鼓励，一起前进。加我微信拉群，请注明：加入GAN日报群。