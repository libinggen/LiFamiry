Ian J. Goodfellow 论文：https://arxiv.org/abs/1406.2661

两个网络：G(Generator)，生成网络，接收随机噪声Z，通过噪声生成样本，G(z)。D(Dicriminator)，判别网络，判别样本是否真实，输入样本x，输出D(x)代表x真实概率，如果1,100%真实样本，如果0,代表不可能是真实样本。

训练过程，生成网络G尽量生成真实样本欺骗判别网络D，判别网络D尽量把G生成样本和真实样本分别开。理想状态下，G生成样本G(z)，使D难以判断真假，D(G(z))=0.5。此时，生成模型G，可以用来生成样本。

数学公式：minG maxDV(D,G)=Ex~pdata(x)[logD(x)]+Ez~pz(z)[log(1-D(G(z)))]
二项式。x真实样本，z输入G网噪声，G(z) G网生成样本。D(x) D网判断真实样本是否真实概率，越接近1越好。D(G(z)) D网判断G网生成样本真实概率。G网，D(G(z))尽可能大，V(D,G)变小，min_G。D网，D(x)越大，D(G(x))越小，V(D,G)越大，max_D。
1､x sampled from data -> Differentiable function D -> D(x) tries to be near 1
2､Input noise z -> Differntiable function G -> x sampled from model -> D -> D tries to make D(G(z)) near 0,G tries to make D(G(z)) near 1

随机梯度下降法训练D、G。

    Algorithm 1 Minibatch stochastic gradient descent training of genegative adversarial nets. The number of steps to apply to the discriminator,k,is a hyperparameter, we used k = 1,the least expensive option, in our experiments.
    for number of training iterations do
        for k steps do
            Sample minibatch of m noise samples {z(1),...,z(m)} from noise prior pg(z)
            Sample minibatch of m examples {x(1),...,x(m)} from data generating distribution pdata(x)
            Update the discriminator by ascending its stochastic gradient:
        end for
        Sample mninbatch of m noise samples {z(1),...,z(m)} from noise prior pg(z)
        Update the generator by descending its stochastic gradient:
    end for
    The gradient-based updates can use any standard gradient-based learning rule.We used momenttum in our experiments.
第一步训练D,V(G,D)越大越好，上升(增加)梯度(ascending)。第二步训练G，V(G,D)越小越好，下降(减少)梯度(descending)。交替进行。

DCGAN原理。https://arxiv.org/abs/1511.06434 。Alec Radford, Luke Metz, Soumith Chintala，《Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks》。G、D换成卷积神经网络(CNN)。取消所有pooling层。G网络使用转置卷积(transposed convolutional layer)上采样，D网络加入stride卷积代替pooling。D、G都batch normalization。去掉FC层，全卷积网络。G网用ReLU激活函数，最后一层用tanh。D网用LeakyRelu激活函数。

G网络。Project reshape 100 z -> 4X4X1024 ->  8X8X512 ->  16X16X256 ->  32X32X128 -> 64X64X3

用DCGAN生成动漫人物头像：
http://qiita.com/mattya/items/e5bfe5e04b9d2f0bbd47 。

原始数据搜集。http://safebooru.donmai.us 。http://konachan.net 。
爬虫代码：

    import requests
    from bs4 import BeautifulSoup
    import os
    import traceback
    def download(url, filename):
        if os.path.exists(filename):
            print('file exists!')
            return
        try:
            r = requests.get(url, stream=True, timeout=60)
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            return filename
        except KeyboardInterrupt:
            if os.path.exists(filename):
                os.remove(filename)
            raise KeyboardInterrupt
        except Exception:
            traceback.print_exc()
            if os.path.exists(filename):
                os.remove(filename)
    if os.path.exists('imgs') is False:
        os.makedirs('imgs')
    start = 1
    end = 8000
    for i in range(start, end + 1):
        url = 'http://konachan.net/post?page=%d&tags=' % i
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        for img in soup.find_all('img', class_="preview"):
            target_url = 'http:' + img['src']
            filename = os.path.join('imgs', target_url.split('/')[-1])
            download(target_url, filename)
        print('%d / %d' % (i, end))

头像截取：
https://github.com/nagadomi/lbpcascade_animeface 。
封装：

    import cv2
    import sys
    import os.path
    from glob import glob
    def detect(filename, cascade_file="lbpcascade_animeface.xml"):
        if not os.path.isfile(cascade_file):
            raise RuntimeError("%s: not found" % cascade_file)
        cascade = cv2.CascadeClassifier(cascade_file)
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(48, 48))
        for i, (x, y, w, h) in enumerate(faces):
            face = image[y: y + h, x:x + w, :]
            face = cv2.resize(face, (96, 96))
            save_filename = '%s-%d.jpg' % (os.path.basename(filename).split('.')[0], i)
            cv2.imwrite("faces/" + save_filename, face)
    if __name__ == '__main__':
        if os.path.exists('faces') is False:
            os.makedirs('faces')
        file_list = glob('imgs/*.jpg')
        for filename in file_list:
            detect(filename)

训练：
https://github.com/carpedm20/DCGAN-tensorflow 。
model.py：

    if config.dataset == 'mnist':
               data_X, data_y = self.load_mnist()
           else:
               data = glob(os.path.join("./data", config.dataset, "*.jpg"))
data文件夹新建anime文件夹放图片，运行时指定 --dataset anime。

    python main.py --image_size 96 --output_size 48 --dataset anime --is_crop True --is_train True --epoch 300 --input_fname_pattern "*.jpg"

GAN论文：https://github.com/zhangqianhui/AdversarialNetsPapers 。

SGD优化。目标函数(objective function)判断、监视学习成果。J(D) 判别网络目标函数，交叉熵(cross entropy)函数。左边D判别真实数据，右边D判别G生成噪音数据。J(G) 生成网络目标函数。
最小最大博弈，minimax game。均衡点(纳什均衡)，J(D)鞍点(saddle point)。
真实数据(data)和模型生成伪数据(model distribution z映射)。 学习D，区分data、model分布。data、model分布相加做分母，分子是真实data分布。目标，D无限接近常数1/2.Pmodel、Pdata无限相似。生成模型与源数据拟合后，无法再学习，常数y=1/2求导永远0。
非饱和博弈(Non-Saturating)。G伪装成功率表示目标函数，均衡不由损失(loss)决定。D完美后，G还可以继续优化。
DCGAN(深度卷积生成对抗网络 Deep Convolutional Generative Adversarial Network)，反向CNN。
卷积神经网络原理，convolutinoal filter 卷积过滤器(滤镜)，把图片过滤(转化)成各种样式。不同过滤器，把图片转化成不同样式。不同样式为原图片不同特征表达。特征学习。
DCGAN创造图片。把一组特征值慢慢恢复成一张图片。
每一个滤镜层，CNN把大图片重要特征提取出来，一步一步减小图片尺寸。DCGAN把小图片(小数组)特征放大，排列成新图片。DCGAN输入最初小数据是噪声数据。图片RGB矩阵，可以向量加减。戴墨镜的男人-不戴墨镜的男人+不戴墨镜的女人=戴墨镜的女人。NLP，word2vec，king-man+woman=queen。向量/矩阵加减后，还原成“图义”代表的图片。NLP，word2vec，向量对应有意义的词；DCGAN，矩阵对应有意义的图片。
统计学科，JS距离(minimax)，KL距离，散度(divergence)方程。创造目标函数。DKL(P||Q)=S∞-∞p(x)log(p(x)/q(x))dx 。
GAN 神经网络构造，通过类SGD方法优化模型。目标函数重要。Q噪声数据分布。P目标分布。求最大似然(Maximum Likelihood)，使KL距离最小化。
KL[P||Q]=SPlog(P/Q)dx=SPlogPdx-SPlogQdx
P、Q都以x为变量，P是真实数据分类。SPlogPdx 是常数。SPlogQdx 只有logQ是变量。正比于-logQ。
KL[P||Q]=-常数-S另一常数·logQdx
Q，P(x|θ)。P模型，θ参数。负的最大似然。
类GAN算法最小化任何f-divergence方程。
面对无限多数据，都可以学到真实数据分布P。现实，数据有限。KL公式理论，KL(P||Q)，Q拟合真实数据P，极大解释全部P内涵(overgeneralization)。多模态(multimodal)，数据不够多，KL(P||Q)覆盖不完整。KL(Q||P)，undergeneralization 。先覆盖较大，再覆盖较小。
G目标函数改造成最大似然。J(G)求导，得到最大似然表达形式。Maximal Likelihood跑得最快。
GAN，生成(复刻)样本，还可以转为强化学习模型(Reinforcement Learning)。上海交大 SeqGAN[Yu et al. 2016]论文。
把数据标签给GAN。学习条件概率p(y|x)远比单独p(x)容易。部分有标签就能大幅提升GAN训练效果，半监督(semi-supervising)学习。半监督学习，三类数据，真实无标签数据，有标签数据，噪音生成数据。目标函数，监督方法和无监督方法结合。标签平滑(smooth)，把0､1离散标签，转变成更加平滑的0.1(beta)､0.9(alpha)等。分子混进beta系数假数据分布。假数据建议保留标签0,一个平滑，另一个不平滑，one-sided label amoothing(单边标签平滑)。平滑，GAN判别函数不会给出太大梯度信号(gradient signal)，防止算法走向极端样本陷阱。
Batch Norm，取一批数据，规范化(normalise,减平均值，除以标准差)。数据更集中，不太大太小，学习效率更高。同一批(batch)数据太相似，无监督GAN，容易被带偏，认为数据都一样，最终生成模型混杂很多其它特征。
Reference Batch Norm，取一批数据(固定)作参照数据集R，新数据batch依据r平均值、标准差规范化。R取得不好，效果也不会好，或R过拟合。
Virtual Batch Norm，取R，新数据x规范化，x加入R形成virtual batch V，用V的平均值、标准差来标准化x，极大减少R风险。
平衡好G、D。通常对抗网络，判别模型D赢，D比G深。用非饱和(non-saturating)博弈写目标函数，保证D学完后，G可以继续学习。
GAN问题。不收敛(non-convergence)，容易只找到局部最优点，非全局最优点，或根本无法收敛。模式崩溃(mode collapse)，minmaxV(G,D)不等于maxminV(G,D)，如果maxD放在内圈，算法可以收敛到应有位置，如果maxG放在内圈，算法扑向聚集区，看不到全局分布。Reverse KL，保守损失(loss)。
Minibatch GAN，原数据分成小batch，保证太相惟数据样本不被放到一个小batch，数据足够多样，避免模式崩溃。
空间理解错误。图片用2D表示3D。图片样本生成图片，空间表达不好。
Unrolled(不滚) GAN，每一步不把判别模型D滚起，把K次D存起，根据损失(loss)选择最好。
无法科学评估，无法量化标准。
离散输出，无法微分(differentiate)。Williams(1992) REINFORCE。Jang et al.(2016) Gumbel-softmax。用连续数值训练，框定范围，输出离散值。
强化学习连接，无法收敛，有限步数，穷举更简单粗暴效果好。
PPGN(Plug and Play Generative Models 即插即用生成模型)，Nguten et al,2016。生成模型领域新State-of-the-art(当前最佳)。
GAN用可以利用监督学习估测复杂目标函数生成模型，GAN内部自己拿真假样本对照。高维连续非凸找纳什均衡，有待研究。

参考资料：
https://zhuanlan.zhihu.com/p/24767059
http://www.sohu.com/a/121189842_465975

欢迎付费咨询(150元每小时)，我的微信：qingxingfengzi

群体经过适当组织，可以互相促进。我一直相，信良性互动可以使彼此更快速地成长，帮助更多人进入自己感兴趣的领域。我在创建一个一起学习GAN的微信群，我们以每天各报各的学习进度为主。加我微信，我会把你拉进群里，加的时候请注明：加入GAN日报群。