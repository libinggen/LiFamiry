Scipy 高端科学计算:http://blog.chinaunix.net/uid-21633169-id-4437868.html

    import os #引用操作系统函数文件
    import scipy.misc #引用scipy包misc模块 图像形式存取数组
    import numpy as np #引用numpy包 矩阵计算
    from model import DCGAN #引用model文件DCGAN类
    from utils import pp, visualize, to_json, show_all_variables #引用utils文件pp对象，visualize, to_json, show_all_variables方法
    import tensorflow as tf #引用tensorflow
    flags = tf.app.flags #接受命令行传递参数，相当于接受argv。第一个是参数名称，第二个参数是默认值，第三个是参数描述
    flags.DEFINE_integer("epoch", 25, "Epoch to train [25]") #训练轮数 25
    flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]") #adam优化器 学习速率 0.0002
    flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]") #adam优化器 动量(参数移动平均数) 0.5
    flags.DEFINE_integer("train_size", np.inf, "The size of train images [np.inf]") #训练画像尺寸，默认无限大正数
    flags.DEFINE_integer("batch_size", 64, "The size of batch images [64]") #图像批大小 64
    flags.DEFINE_integer("input_height", 108, "The size of image to use (will be center cropped). [108]") #输入图像高度 108 均衡的缩放图像（保持图像原始比例），使图片的两个坐标（宽、高）都大于等于 相应的视图坐标（负的内边距）。图像则位于视图的中央。
    flags.DEFINE_integer("input_width", None, "The size of image to use (will be center cropped). If None, same value as input_height [None]") #输入图像宽度，None与高度相同
    flags.DEFINE_integer("output_height", 64, "The size of the output images to produce [64]") #输出图像高度 64
    flags.DEFINE_integer("output_width", None, "The size of the output images to produce. If None, same value as output_height [None]") #输出图像宽度，None与高度相同
    flags.DEFINE_string("dataset", "celebA", "The name of dataset [celebA, mnist, lsun]") #数据集名称 celebA mnist lsun
    flags.DEFINE_string("input_fname_pattern", "*.jpg", "Glob pattern of filename of input images [*]") #图片文件名的搜索扩展名
    flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]") #检查点目录名
    flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]") #图片样本保存目录名
    flags.DEFINE_boolean("train", False, "True for training, False for testing [False]") #训练流程开关
    flags.DEFINE_boolean("crop", False, "True for training, False for testing [False]") #训练流程开关
    flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]") #可视化开关
    FLAGS = flags.FLAGS
    def main(_): #主程序
      pp.pprint(flags.FLAGS.__flags) #打印命令行参数
         if FLAGS.input_width is None: #如果没有配置输入图像宽度
        FLAGS.input_width = FLAGS.input_height #把输入图像高度作为宽度
      if FLAGS.output_width is None: #如果没有配置输出图像宽度
        FLAGS.output_width = FLAGS.output_height #把输出图像高度作为宽度
      if not os.path.exists(FLAGS.checkpoint_dir): #如果检查点目录不存在
        os.makedirs(FLAGS.checkpoint_dir) #创建检查点目录
      if not os.path.exists(FLAGS.sample_dir): #如果样本目录不存在
        os.makedirs(FLAGS.sample_dir) #创建样本目录
      #gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333) #设置GPU显存占用比例
      run_config = tf.ConfigProto() #获取配置对象
      run_config.gpu_options.allow_growth = True #GPU显存占用按需增加
      with tf.Session(config=run_config) as sess: #指定配置构建会话
        if FLAGS.dataset == 'mnist': #如果指定数据集为mnist
          dcgan = DCGAN( #构建DCGAN
              sess, #提定会话
              input_width=FLAGS.input_width,
              input_height=FLAGS.input_height,
              output_width=FLAGS.output_width,
              output_height=FLAGS.output_height,
              batch_size=FLAGS.batch_size,
              sample_num=FLAGS.batch_size,
              y_dim=10, #标签维度为10
              dataset_name=FLAGS.dataset,
              input_fname_pattern=FLAGS.input_fname_pattern,
              crop=FLAGS.crop,
              checkpoint_dir=FLAGS.checkpoint_dir,
              sample_dir=FLAGS.sample_dir)
        else:
          dcgan = DCGAN( #构建DCGAN,不指定标签维度
              sess,
              input_width=FLAGS.input_width,
              input_height=FLAGS.input_height,
              output_width=FLAGS.output_width,
              output_height=FLAGS.output_height,
              batch_size=FLAGS.batch_size,
              sample_num=FLAGS.batch_size,
              dataset_name=FLAGS.dataset,
              input_fname_pattern=FLAGS.input_fname_pattern,
              crop=FLAGS.crop,
              checkpoint_dir=FLAGS.checkpoint_dir,
              sample_dir=FLAGS.sample_dir)
        show_all_variables() #显示所有参数
        if FLAGS.train: #如果是训练
          dcgan.train(FLAGS) #指定参数执行构建DCGAN 训练方法
        else: #如果是测试
          if not dcgan.load(FLAGS.checkpoint_dir)[0]: #在检查点目录没有检查点文件，即没有已训练好的模型
            raise Exception("[!] Train a model first, then run test mode") #抛出异常：请先训练模型再执行测试
      
        # to_json("./web/js/layers.js", [dcgan.h0_w, dcgan.h0_b, dcgan.g_bn0], #JSON格式化：w,b,gbn
        #                 [dcgan.h1_w, dcgan.h1_b, dcgan.g_bn1],
        #                 [dcgan.h2_w, dcgan.h2_b, dcgan.g_bn2],
        #                 [dcgan.h3_w, dcgan.h3_b, dcgan.g_bn3],
        #                 [dcgan.h4_w, dcgan.h4_b, None])
        # Below is codes for visualization
        OPTION = 1
        visualize(sess, dcgan, FLAGS, OPTION) #执行可视化方法，传入会话、DCGAN、配置参数，选项
    if __name__ == '__main__': #如果直接执行本脚本文件，运行以下代码，一般作调试用。如果作为其它脚本模块引入，则不执行以下代码
      tf.app.run() #运行APP.run 解析FLAGS，执行main方法

欢迎付费咨询(150元每小时)，我的微信：qingxingfengzi

我创建GAN日报群，以每天各报各的进度为主。把正在研究GAN的人聚在一起，互相鼓励，一起前进。加我微信拉群，请注明：加入GAN日报群。

![](http://upload-images.jianshu.io/upload_images/80690-0210d23e28f48235?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)