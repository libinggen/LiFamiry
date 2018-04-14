TensorFlow对Android、iOS、树莓派都提供移动端支持。

移动端应用原理。移动端、嵌入式设备应用深度学习方式，一模型运行在云端服务器，向服务器发送请求，接收服务器响应；二在本地运行模型，PC训练模型，放到移动端预测。向服务端请求数据可行性差，移动端资源稀缺。本地运行实时性更好。加速计算，内存空间和速度优化。精简模型，节省内存空间，加快计算速度。加快框架执行速度，优化模型复杂度和每步计算速度。
精简模型，用更低权得精度，量化(quantization)、权重剪枝(weight pruning，剪小权重连接，把所有权值连接低于阈值的从网络移除)。加速框架执行，优化矩阵通用乘法(GEMM)运算，影响卷积层(先数据im2col运行，再GEMM运算)和全连接层。im2col，索引图像块重排列为矩阵列。先将大矩阵重叠划分多个子矩阵，每个子矩阵序列化成向量，得到另一个矩阵。

量化(quantitative)。《How to Quantize Neural Networks with TensorFlow》https://www.tensorflow.org/performance/quantization 。离散化。用比32位浮点数更少空间存储、运行模型，TensorFlow量化实现屏蔽存储、运行细节。神经网络预测，浮点影响速度，量化加快速度，保持较高精度。减小模型文件大小。存储模型用8位整数，加载模型运算转换回32位浮点数。降低预测过程计算资源。神经网络噪声健壮笥强，量化精度损失不会危害整体准确度。训练，反向传播需要计算梯度，不能用低精度格式直接训练。PC训练浮点数模型，转8位，移动端用8位模型预测。
量化示例。GoogleNet模型转8位模型例子。下载训练好GoogleNet模型，http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz 。

    bazel build tensorflow/tools/quantization:quantization_graph
    bazel-bin/tensorflow/tools/quantization/quantization_graph \
    --input=/tmp/classify_image_graph_def.pb \
    --output_node_names="softmax" --output=/tmp/quantized_graph.pb \
    --mode=eightbit

生成量化后模型大小只有原来的1/4。执行：

    bazel build tensorflow/examples/label_image:label_image
    bazel-bin/tensorflow/examples/label_image/label_image \
    --image=/tmp/cropped_panda.jpg \
    --graph=/tmp/quantized_graph.pb \
    --labels=/tmp/imagenet_synset_to_human_label_map.txt \
    --input_width=299 \
    --input_height=299 \
    --input_mean=128 \
    --input_std=128 \
    --input_layer="Mul:0" \
    --output_layer="softmax:0"

量化过程实现。预测操作转换成等价8位版本操作实现。原始Relu操作，输入、输出浮点数。量化Relu操作，根据输入浮点数计算最大值、最小值，进入量化(Quantize)操作输入数据转换8位。保证输出层输入数据准确性，需要反量化(Dequantize)操作，权重转回32位精度，保证预测准确性。整个模型前向传播用8位整数支行，最后一层加反量化层，8位转回32位输出层输入。每个量化操作后执行反量化操作。

量化数据表示。浮点数转8位表示，是压缩问题。权重、经过激活函数处理上层输出，是分布在一个范围内的值。量化过程，找出最大值、最小值，将浮点数线性分布，做线性扩展。

优化矩阵乘法运算。谷歌开源小型独立低精度通用矩阵乘法(General Matrix to Matrix Multiplication,GEMM)库 gemmlowp。https://github.com/google/gemmlowp 。

iOS系统实践。

环境准备。操作系统Mac OS X，集成开发工具Xcode 7.3以上版本。编译TensorFlow核心静态库。tensorflow/contrib/makefiles/download_depencies.sh 。依赖库下载到tensorflow/contrib/makefile/downloads目录。eigen #C++开源矩阵计算工具。gemmlowp #小型独立低精度通用矩阵乘法(GEMM)库。googletest #谷歌开源C++测试框架。protobuf #谷歌开源数据交换格式协议。re2 #谷歌开源正则表达式库。

编译演示程度，运行。tensorflow/contrib/makefile/build_all_iso.sh。编译生成静态库，tensorflow/contrib/makefile/gen/lib：ios_ARM64、ios_ARMV7、ios_ARMV7S、ios_I386、ios_X86_64、libtensorflow-core.a。Xcode模拟器或iOS设备运行APP预测示例。TensorFlow iOS示例。https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/ios/ 。3个目录。benchmark目录是预测基准示例。simple目录是图片预测示例。camera目录是视频流实时预测示例。下载Inception V1模型，能识别1000类图片，https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip 。解压模型，复制到benchmark、simple、camera的data目录。运行目录下xcodeproj文件。选择iPhone 7 Plus模拟器，点击运行标志，编译完成点击Run Model按钮。预测结果见Xcode 控制台。

自定义模型编译、运行。https://github.com/tensorflow/tensorflow/blob/15b1cf025da5c6ac2bcf4d4878ee222fca3aec4a/tensorflow/docs_src/tutorials/image_retraining.md 。下载花卉数据 http://download.tensorflow.org/example_images/flower_photos.tgz 。郁金香(tulips)、玫瑰(roses)、浦公英(dandelion)、向日葵(sunflowers)、雏菊(daisy)5种花卉文件目录，各800张图片。
训练原始模型。下载预训练Inception V3模型 http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz 。

    python tensorflow/examples/image_retraining/retrain.py \
    --bottlenectk_dir=/tmp/bottlenecks/ \
    --how_many_training_steps 10 \
    --model_dir=/tmp/inception \
    --output_graph=/tmp/retrained_graph.pb \
    --output_labels=/tmp/retrained_labels.txt \
    --image_dir /tmp/flower_photos

训练完成，/tmp目录有模型文件retrained_graph.pb、标签文件上retrained_labels.txt。“瓶颈”(bottlenecks)文件，描述实际分类最终输出层前一层(倒数第二层)。倒数第二层训练很好，瓶颈值是有意义紧凑图像摘要，包含足够信息使分类选择。第一次训练，retrain.py文件代码先分析所有图片，计算每张图片瓶颈值存储下来。每张图片被使用多次，不必重复计算。

编译iOS支持模型。https://petewarden.com/2016/09/27/tensorflow-for-mobile-poets/ 。原始模型到iOS模型，先去掉iOS系统不支持操作，优化模型，再将模型量化，权重变8位常数，缩小模型，最后模型内存映射。
去掉iOS系统不支持操作，优化模型。iOS版本TensorFlow仅支持预测阶段常见没有大外部依赖关系操作。支持操作列表：https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/makefile/tf_op_files.txt 。DecodeJpeg不支持，JPEG格式图片解码，依赖libjpeg。从摄像头实时识别花卉种类，直接处理相机图像缓冲区，不存JPEG文件再解码。预训练模型Inception V3 从图片数据集训练，包含DecodeJpeg操作。输入数据直接提供(feed)Decode后Mul操作，绕过Decode操作。优化加速预测，显式批处理规范化(explicit batch normalization)操作合并到卷积权重，减少计算次数。

    bazel build tensorflow/python/tools:optimize_for_inference
    bazel-bin/tensorflow/python/tools/optimize_for_inference \
    --input=/tmp/retrained_graph.pb \
    --output=/tmp/optimized_graph.pb \
    --input_names=Mul \
    --output_names=final_result \

label_image命令预测：

    bazel-bin/tensorflow/examples/label_image/label_image \
    --output_layer=final_result \
    --labels=/tmp/output_labels.txt \
    --image=/tmp/flower_photos/daisy/5547758_eea9edfd54_n.jpg
    --graph=/tmp/output_graph.pb \
    --input_layer=Mul \
    --input_mean=128 \
    --input_std=128 \

量化模型。苹果系统在.ipa包分发应用程度，所有应用程度资源都用zip压缩。模型权重从浮点数转整数(范围0~255)，损失准确度，小于1%。

    bazel build tensorflow/tools/quantization:quantization_graph
    bazel-bin/tensorflow/tools/quantization/quantization_graph \
    --input=/tmp/optimized_graph.pb \
    --output=/tmp/rounded_graph.pb \
    --output_node_names=final_result \
    --mode=weights_rounded

内存映射 memory mapping。物理内存映射到进程地址空间内，应用程序直接用输入/输出地址空间，提高读写效率。模型全部一次性加载到内存缓冲区，会对iOS RAM施加过大压力，操作系统会杀死内存占用过多程序。模型权值缓冲区只读，可映射到内存。重新排列模型，权重分部分逐块从主GraphDef加载到内存。

    bazel build tensorflow/contrib/util:convert_graphdef_memmapped_format
    bazel-bin/tensorflow/contrib/util/convert_graphdef_memmapped_format \
    --in_graph=/tmp/rounded_graph.pb \
    --out_graph=/tmp/mmapped_graph.pb

生成iOS工程文件运行。视频流实进预测演示程序例子。https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/ios/camera 。模型文件、标记文件复制到data目录。修改CameraExampleViewController.mm，更改加载模型文件名称、输入图片尺寸、操作节点名字、缩放像素大小。

    #import <AssertMacros.h>
    #import <AssetsLibrary/AssetsLibrary.h>
    #import <CoreImage/CoreImage.h>
    #import <ImageIO/ImageIO.h>
    #import "CameraExampleViewController.h"
    #include <sys/time.h>
    #include "tensorflow_utils.h"
    // If you have your own model, modify this to the file name, and make sure
    // you've added the file to your app resources too.
    static NSString* model_file_name = @"tensorflow_inception_graph";
    static NSString* model_file_type = @"pb";
    // This controls whether we'll be loading a plain GraphDef proto, or a
    // file created by the convert_graphdef_memmapped_format utility that wraps a
    // GraphDef and parameter file that can be mapped into memory from file to
    // reduce overall memory usage.
    const bool model_uses_memory_mapping = false;
    // If you have your own model, point this to the labels file.
    static NSString* labels_file_name = @"imagenet_comp_graph_label_strings";
    static NSString* labels_file_type = @"txt";
    // These dimensions need to match those the model was trained with.
    // 以下尺寸需要和模型训练时相匹配
    const int wanted_input_width =299;// 224;
    const int wanted_input_height = 299;//224;
    const int wanted_input_channels = 3;
    const float input_mean = 128.0f;//117.0f;
    const float input_std = 128.0f;//1.0f;
    const std::string input_layer_name = "Mul";//"input";
    const std::string output_layer_name = "final_result";//"softmax1";
    static void *AVCaptureStillImageIsCapturingStillImageContext =
        &AVCaptureStillImageIsCapturingStillImageContext;
    @interface CameraExampleViewController (InternalMethods)
    - (void)setupAVCapture;
    - (void)teardownAVCapture;
    @end
    @implementation CameraExampleViewController
    - (void)setupAVCapture {
      NSError *error = nil;
      session = [AVCaptureSession new];
      if ([[UIDevice currentDevice] userInterfaceIdiom] ==
          UIUserInterfaceIdiomPhone)
        [session setSessionPreset:AVCaptureSessionPreset640x480];
      else
        [session setSessionPreset:AVCaptureSessionPresetPhoto];
      AVCaptureDevice *device =
          [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
      AVCaptureDeviceInput *deviceInput =
          [AVCaptureDeviceInput deviceInputWithDevice:device error:&error];
      assert(error == nil);
      isUsingFrontFacingCamera = NO;
      if ([session canAddInput:deviceInput]) [session addInput:deviceInput];
      stillImageOutput = [AVCaptureStillImageOutput new];
      [stillImageOutput
          addObserver:self
           forKeyPath:@"capturingStillImage"
              options:NSKeyValueObservingOptionNew
              context:(void *)(AVCaptureStillImageIsCapturingStillImageContext)];
      if ([session canAddOutput:stillImageOutput])
        [session addOutput:stillImageOutput];
      videoDataOutput = [AVCaptureVideoDataOutput new];
      NSDictionary *rgbOutputSettings = [NSDictionary
          dictionaryWithObject:[NSNumber numberWithInt:kCMPixelFormat_32BGRA]
                        forKey:(id)kCVPixelBufferPixelFormatTypeKey];
      [videoDataOutput setVideoSettings:rgbOutputSettings];
      [videoDataOutput setAlwaysDiscardsLateVideoFrames:YES];
      videoDataOutputQueue =
          dispatch_queue_create("VideoDataOutputQueue", DISPATCH_QUEUE_SERIAL);
      [videoDataOutput setSampleBufferDelegate:self queue:videoDataOutputQueue];
      if ([session canAddOutput:videoDataOutput])
        [session addOutput:videoDataOutput];
      [[videoDataOutput connectionWithMediaType:AVMediaTypeVideo] setEnabled:YES];
      previewLayer = [[AVCaptureVideoPreviewLayer alloc] initWithSession:session];
      [previewLayer setBackgroundColor:[[UIColor blackColor] CGColor]];
      [previewLayer setVideoGravity:AVLayerVideoGravityResizeAspect];
      CALayer *rootLayer = [previewView layer];
      [rootLayer setMasksToBounds:YES];
      [previewLayer setFrame:[rootLayer bounds]];
      [rootLayer addSublayer:previewLayer];
      [session startRunning];
      if (error) {
        NSString *title = [NSString stringWithFormat:@"Failed with error %d", (int)[error code]];
        UIAlertController *alertController =
            [UIAlertController alertControllerWithTitle:title
                                                message:[error localizedDescription]
                                         preferredStyle:UIAlertControllerStyleAlert];
        UIAlertAction *dismiss =
            [UIAlertAction actionWithTitle:@"Dismiss" style:UIAlertActionStyleDefault handler:nil];
        [alertController addAction:dismiss];
        [self presentViewController:alertController animated:YES completion:nil];
        [self teardownAVCapture];
      }
    }
    - (void)teardownAVCapture {
      [stillImageOutput removeObserver:self forKeyPath:@"isCapturingStillImage"];
      [previewLayer removeFromSuperlayer];
    }
    - (void)observeValueForKeyPath:(NSString *)keyPath
                          ofObject:(id)object
                            change:(NSDictionary *)change
                           context:(void *)context {
      if (context == AVCaptureStillImageIsCapturingStillImageContext) {
        BOOL isCapturingStillImage =
            [[change objectForKey:NSKeyValueChangeNewKey] boolValue];
        if (isCapturingStillImage) {
          // do flash bulb like animation
          flashView = [[UIView alloc] initWithFrame:[previewView frame]];
          [flashView setBackgroundColor:[UIColor whiteColor]];
          [flashView setAlpha:0.f];
          [[[self view] window] addSubview:flashView];
          [UIView animateWithDuration:.4f
                           animations:^{
                             [flashView setAlpha:1.f];
                           }];
        } else {
          [UIView animateWithDuration:.4f
              animations:^{
                [flashView setAlpha:0.f];
              }
              completion:^(BOOL finished) {
               [flashView removeFromSuperview];
                flashView = nil;
              }];
        }
      }
    }
    - (AVCaptureVideoOrientation)avOrientationForDeviceOrientation:
        (UIDeviceOrientation)deviceOrientation {
      AVCaptureVideoOrientation result =
          (AVCaptureVideoOrientation)(deviceOrientation);
      if (deviceOrientation == UIDeviceOrientationLandscapeLeft)
        result = AVCaptureVideoOrientationLandscapeRight;
      else if (deviceOrientation == UIDeviceOrientationLandscapeRight)
        result = AVCaptureVideoOrientationLandscapeLeft;
      return result;
    }
    - (IBAction)takePicture:(id)sender {
      if ([session isRunning]) {
        [session stopRunning];
        [sender setTitle:@"Continue" forState:UIControlStateNormal];
        flashView = [[UIView alloc] initWithFrame:[previewView frame]];
        [flashView setBackgroundColor:[UIColor whiteColor]];
        [flashView setAlpha:0.f];
        [[[self view] window] addSubview:flashView];
        [UIView animateWithDuration:.2f
            animations:^{
              [flashView setAlpha:1.f];
            }
            completion:^(BOOL finished) {
              [UIView animateWithDuration:.2f
                  animations:^{
                    [flashView setAlpha:0.f];
                  }
                  completion:^(BOOL finished) {
                    [flashView removeFromSuperview];
                    flashView = nil;
                  }];
            }];
      } else {
        [session startRunning];
        [sender setTitle:@"Freeze Frame" forState:UIControlStateNormal];
      }
    }
    + (CGRect)videoPreviewBoxForGravity:(NSString *)gravity
                              frameSize:(CGSize)frameSize
                           apertureSize:(CGSize)apertureSize {
      CGFloat apertureRatio = apertureSize.height / apertureSize.width;
      CGFloat viewRatio = frameSize.width / frameSize.height;
      CGSize size = CGSizeZero;
      if ([gravity isEqualToString:AVLayerVideoGravityResizeAspectFill]) {
        if (viewRatio > apertureRatio) {
          size.width = frameSize.width;
          size.height =
              apertureSize.width * (frameSize.width / apertureSize.height);
        } else {
          size.width =
              apertureSize.height * (frameSize.height / apertureSize.width);
          size.height = frameSize.height;
       }
      } else if ([gravity isEqualToString:AVLayerVideoGravityResizeAspect]) {
        if (viewRatio > apertureRatio) {
          size.width =
              apertureSize.height * (frameSize.height / apertureSize.width);
          size.height = frameSize.height;
        } else {
          size.width = frameSize.width;
          size.height =
              apertureSize.width * (frameSize.width / apertureSize.height);
        }
      } else if ([gravity isEqualToString:AVLayerVideoGravityResize]) {
        size.width = frameSize.width;
        size.height = frameSize.height;
      }
      CGRect videoBox;
      videoBox.size = size;
      if (size.width < frameSize.width)
        videoBox.origin.x = (frameSize.width - size.width) / 2;
      else
        videoBox.origin.x = (size.width - frameSize.width) / 2;
      if (size.height < frameSize.height)
        videoBox.origin.y = (frameSize.height - size.height) / 2;
      else
        videoBox.origin.y = (size.height - frameSize.height) / 2;
      return videoBox;
    }
    - (void)captureOutput:(AVCaptureOutput *)captureOutput
    didOutputSampleBuffer:(CMSampleBufferRef)sampleBuffer
           fromConnection:(AVCaptureConnection *)connection {
      CVPixelBufferRef pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer);
      CFRetain(pixelBuffer);
      [self runCNNOnFrame:pixelBuffer];
      CFRelease(pixelBuffer);
    }
    - (void)runCNNOnFrame:(CVPixelBufferRef)pixelBuffer {
      assert(pixelBuffer != NULL);
      OSType sourcePixelFormat = CVPixelBufferGetPixelFormatType(pixelBuffer);
      int doReverseChannels;
      if (kCVPixelFormatType_32ARGB == sourcePixelFormat) {
        doReverseChannels = 1;
      } else if (kCVPixelFormatType_32BGRA == sourcePixelFormat) {
        doReverseChannels = 0;
      } else {
        assert(false);  // Unknown source format
      }
      const int sourceRowBytes = (int)CVPixelBufferGetBytesPerRow(pixelBuffer);
      const int image_width = (int)CVPixelBufferGetWidth(pixelBuffer);
      const int fullHeight = (int)CVPixelBufferGetHeight(pixelBuffer);
      CVPixelBufferLockFlags unlockFlags = kNilOptions;
      CVPixelBufferLockBaseAddress(pixelBuffer, unlockFlags);
      unsigned char *sourceBaseAddr =
          (unsigned char *)(CVPixelBufferGetBaseAddress(pixelBuffer));
      int image_height;
      unsigned char *sourceStartAddr;
      if (fullHeight <= image_width) {
        image_height = fullHeight;
        sourceStartAddr = sourceBaseAddr;
      } else {
        image_height = image_width;
        const int marginY = ((fullHeight - image_width) / 2);
        sourceStartAddr = (sourceBaseAddr + (marginY * sourceRowBytes));
      }
      const int image_channels = 4;
      assert(image_channels >= wanted_input_channels);
      tensorflow::Tensor image_tensor(
          tensorflow::DT_FLOAT,
          tensorflow::TensorShape(
              {1, wanted_input_height, wanted_input_width, wanted_input_channels}));
      auto image_tensor_mapped = image_tensor.tensor<float, 4>();
      tensorflow::uint8 *in = sourceStartAddr;
      float *out = image_tensor_mapped.data();
      for (int y = 0; y < wanted_input_height; ++y) {
        float *out_row = out + (y * wanted_input_width * wanted_input_channels);
        for (int x = 0; x < wanted_input_width; ++x) {
          const int in_x = (y * image_width) / wanted_input_width;
          const int in_y = (x * image_height) / wanted_input_height;
          tensorflow::uint8 *in_pixel =
              in + (in_y * image_width * image_channels) + (in_x * image_channels);
          float *out_pixel = out_row + (x * wanted_input_channels);
          for (int c = 0; c < wanted_input_channels; ++c) {
            out_pixel[c] = (in_pixel[c] - input_mean) / input_std;
          }
        }
      }
      CVPixelBufferUnlockBaseAddress(pixelBuffer, unlockFlags);
      if (tf_session.get()) {
        std::vector<tensorflow::Tensor> outputs;
        tensorflow::Status run_status = tf_session->Run(
            {{input_layer_name, image_tensor}}, {output_layer_name}, {}, &outputs);
        if (!run_status.ok()) {
          LOG(ERROR) << "Running model failed:" << run_status;
        } else {
          tensorflow::Tensor *output = &outputs[0];
          auto predictions = output->flat<float>();
          NSMutableDictionary *newValues = [NSMutableDictionary dictionary];
          for (int index = 0; index < predictions.size(); index += 1) {
            const float predictionValue = predictions(index);
            if (predictionValue > 0.05f) {
              std::string label = labels[index % predictions.size()];
              NSString *labelObject = [NSString stringWithUTF8String:label.c_str()];
              NSNumber *valueObject = [NSNumber numberWithFloat:predictionValue];
              [newValues setObject:valueObject forKey:labelObject];
            }
          }
          dispatch_async(dispatch_get_main_queue(), ^(void) {
            [self setPredictionValues:newValues];
          });
        }
      }
      CVPixelBufferUnlockBaseAddress(pixelBuffer, 0);
    }
    - (void)dealloc {
      [self teardownAVCapture];
    }
    // use front/back camera
    - (IBAction)switchCameras:(id)sender {
      AVCaptureDevicePosition desiredPosition;
      if (isUsingFrontFacingCamera)
        desiredPosition = AVCaptureDevicePositionBack;
      else
        desiredPosition = AVCaptureDevicePositionFront;
      for (AVCaptureDevice *d in
           [AVCaptureDevice devicesWithMediaType:AVMediaTypeVideo]) {
        if ([d position] == desiredPosition) {
          [[previewLayer session] beginConfiguration];
          AVCaptureDeviceInput *input =
              [AVCaptureDeviceInput deviceInputWithDevice:d error:nil];
          for (AVCaptureInput *oldInput in [[previewLayer session] inputs]) {
            [[previewLayer session] removeInput:oldInput];
          }
          [[previewLayer session] addInput:input];
          [[previewLayer session] commitConfiguration];
          break;
        }
      }
      isUsingFrontFacingCamera = !isUsingFrontFacingCamera;
    }
    - (void)didReceiveMemoryWarning {
      [super didReceiveMemoryWarning];
    }
    - (void)viewDidLoad {
      [super viewDidLoad];
      square = [UIImage imageNamed:@"squarePNG"];
      synth = [[AVSpeechSynthesizer alloc] init];
      labelLayers = [[NSMutableArray alloc] init];
      oldPredictionValues = [[NSMutableDictionary alloc] init];
      tensorflow::Status load_status;
      if (model_uses_memory_mapping) {
        load_status = LoadMemoryMappedModel(
            model_file_name, model_file_type, &tf_session, &tf_memmapped_env);
      } else {
        load_status = LoadModel(model_file_name, model_file_type, &tf_session);
      }
      if (!load_status.ok()) {
        LOG(FATAL) << "Couldn't load model: " << load_status;
      }
      tensorflow::Status labels_status =
          LoadLabels(labels_file_name, labels_file_type, &labels);
      if (!labels_status.ok()) {
        LOG(FATAL) << "Couldn't load labels: " << labels_status;
      }
      [self setupAVCapture];
    }
    - (void)viewDidUnload {
      [super viewDidUnload];
    }
    - (void)viewWillAppear:(BOOL)animated {
      [super viewWillAppear:animated];
    }
    - (void)viewDidAppear:(BOOL)animated {
      [super viewDidAppear:animated];
    }
    - (void)viewWillDisappear:(BOOL)animated {
      [super viewWillDisappear:animated];
    }
    - (void)viewDidDisappear:(BOOL)animated {
      [super viewDidDisappear:animated];
    }
    - (BOOL)shouldAutorotateToInterfaceOrientation:
        (UIInterfaceOrientation)interfaceOrientation {
      return (interfaceOrientation == UIInterfaceOrientationPortrait);
    }
    - (BOOL)prefersStatusBarHidden {
      return YES;
    }
    - (void)setPredictionValues:(NSDictionary *)newValues {
      const float decayValue = 0.75f;
      const float updateValue = 0.25f;
      const float minimumThreshold = 0.01f;
      NSMutableDictionary *decayedPredictionValues =
          [[NSMutableDictionary alloc] init];
      for (NSString *label in oldPredictionValues) {
        NSNumber *oldPredictionValueObject =
            [oldPredictionValues objectForKey:label];
        const float oldPredictionValue = [oldPredictionValueObject floatValue];
        const float decayedPredictionValue = (oldPredictionValue * decayValue);
        if (decayedPredictionValue > minimumThreshold) {
          NSNumber *decayedPredictionValueObject =
              [NSNumber numberWithFloat:decayedPredictionValue];
          [decayedPredictionValues setObject:decayedPredictionValueObject
                                      forKey:label];
        }
      }
      oldPredictionValues = decayedPredictionValues;
      for (NSString *label in newValues) {
        NSNumber *newPredictionValueObject = [newValues objectForKey:label];
        NSNumber *oldPredictionValueObject =
            [oldPredictionValues objectForKey:label];
        if (!oldPredictionValueObject) {
          oldPredictionValueObject = [NSNumber numberWithFloat:0.0f];
        }
        const float newPredictionValue = [newPredictionValueObject floatValue];
        const float oldPredictionValue = [oldPredictionValueObject floatValue];
        const float updatedPredictionValue =
            (oldPredictionValue + (newPredictionValue * updateValue));
        NSNumber *updatedPredictionValueObject =
            [NSNumber numberWithFloat:updatedPredictionValue];
        [oldPredictionValues setObject:updatedPredictionValueObject forKey:label];
      }
      NSArray *candidateLabels = [NSMutableArray array];
      for (NSString *label in oldPredictionValues) {
        NSNumber *oldPredictionValueObject =
            [oldPredictionValues objectForKey:label];
        const float oldPredictionValue = [oldPredictionValueObject floatValue];
        if (oldPredictionValue > 0.05f) {
          NSDictionary *entry = @{
            @"label" : label,
            @"value" : oldPredictionValueObject
          };
          candidateLabels = [candidateLabels arrayByAddingObject:entry];
        }
      }
      NSSortDescriptor *sort =
          [NSSortDescriptor sortDescriptorWithKey:@"value" ascending:NO];
      NSArray *sortedLabels = [candidateLabels
          sortedArrayUsingDescriptors:[NSArray arrayWithObject:sort]];
      const float leftMargin = 10.0f;
      const float topMargin = 10.0f;
      const float valueWidth = 48.0f;
      const float valueHeight = 26.0f;
      const float labelWidth = 246.0f;
      const float labelHeight = 26.0f;
      const float labelMarginX = 5.0f;
      const float labelMarginY = 5.0f;
      [self removeAllLabelLayers];
      int labelCount = 0;
      for (NSDictionary *entry in sortedLabels) {
        NSString *label = [entry objectForKey:@"label"];
        NSNumber *valueObject = [entry objectForKey:@"value"];
        const float value = [valueObject floatValue];
        const float originY =
            (topMargin + ((labelHeight + labelMarginY) * labelCount));
        const int valuePercentage = (int)roundf(value * 100.0f);
        const float valueOriginX = leftMargin;
        NSString *valueText = [NSString stringWithFormat:@"%d%%", valuePercentage];
        [self addLabelLayerWithText:valueText
                            originX:valueOriginX
                            originY:originY
                              width:valueWidth
                             height:valueHeight
                          alignment:kCAAlignmentRight];
        const float labelOriginX = (leftMargin + valueWidth + labelMarginX);
        [self addLabelLayerWithText:[label capitalizedString]
                            originX:labelOriginX
                            originY:originY
                              width:labelWidth
                             height:labelHeight
                          alignment:kCAAlignmentLeft];
        if ((labelCount == 0) && (value > 0.5f)) {
          [self speak:[label capitalizedString]];
        }
        labelCount += 1;
        if (labelCount > 4) {
          break;
        }
      }
    }
    - (void)removeAllLabelLayers {
      for (CATextLayer *layer in labelLayers) {
        [layer removeFromSuperlayer];
      }
      [labelLayers removeAllObjects];
    }
    - (void)addLabelLayerWithText:(NSString *)text
                          originX:(float)originX
                          originY:(float)originY
                            width:(float)width
                           height:(float)height
                        alignment:(NSString *)alignment {
      CFTypeRef font = (CFTypeRef) @"Menlo-Regular";
      const float fontSize = 20.0f;
      const float marginSizeX = 5.0f;
      const float marginSizeY = 2.0f;
      const CGRect backgroundBounds = CGRectMake(originX, originY, width, height);
      const CGRect textBounds =
          CGRectMake((originX + marginSizeX), (originY + marginSizeY),
                     (width - (marginSizeX * 2)), (height - (marginSizeY * 2)));
      CATextLayer *background = [CATextLayer layer];
      [background setBackgroundColor:[UIColor blackColor].CGColor];
      [background setOpacity:0.5f];
      [background setFrame:backgroundBounds];
      background.cornerRadius = 5.0f;
      [[self.view layer] addSublayer:background];
      [labelLayers addObject:background];
      CATextLayer *layer = [CATextLayer layer];
      [layer setForegroundColor:[UIColor whiteColor].CGColor];
      [layer setFrame:textBounds];
      [layer setAlignmentMode:alignment];
      [layer setWrapped:YES];
      [layer setFont:font];
      [layer setFontSize:fontSize];
      layer.contentsScale = [[UIScreen mainScreen] scale];
      [layer setString:text];
      [[self.view layer] addSublayer:layer];
      [labelLayers addObject:layer];
    }
    - (void)setPredictionText:(NSString *)text withDuration:(float)duration {
      if (duration > 0.0) {
        CABasicAnimation *colorAnimation =
            [CABasicAnimation animationWithKeyPath:@"foregroundColor"];
        colorAnimation.duration = duration;
        colorAnimation.fillMode = kCAFillModeForwards;
        colorAnimation.removedOnCompletion = NO;
        colorAnimation.fromValue = (id)[UIColor darkGrayColor].CGColor;
        colorAnimation.toValue = (id)[UIColor whiteColor].CGColor;
        colorAnimation.timingFunction =
            [CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionLinear];
        [self.predictionTextLayer addAnimation:colorAnimation
                                        forKey:@"colorAnimation"];
      } else {
        self.predictionTextLayer.foregroundColor = [UIColor whiteColor].CGColor;
      }
      [self.predictionTextLayer removeFromSuperlayer];
      [[self.view layer] addSublayer:self.predictionTextLayer];
      [self.predictionTextLayer setString:text];
    }
    - (void)speak:(NSString *)words {
      if ([synth isSpeaking]) {
        return;
      }
      AVSpeechUtterance *utterance =
          [AVSpeechUtterance speechUtteranceWithString:words];
      utterance.voice = [AVSpeechSynthesisVoice voiceWithLanguage:@"en-US"];
      utterance.rate = 0.75 * AVSpeechUtteranceDefaultSpeechRate;
      [synth speakUtterance:utterance];
    }
    @end

连上iPhone手机，双击tensorflow/contrib/ios_examples/camera/camera_example.xcodeproj编译运行。手机安装好APP，打开APP，找到玫瑰花识别。训练迭代次数10000次后，识别率99%以上。模拟器打包，生成打包工程文件位于/Users/libinggen/Library/Developer/Xcode/DeriveData/camera_example-dhfdsdfesfmrwtfb1fpfkfjsdfhdskf/Build/Products/Debug-iphoneos。打开CameraExample.app，有可执行文件CameraExample、资源文件模型文件mmapped_graph.pb、标记文件retrained_labels.txt。

Android系统实践。

环境准备。MacBook Pro。Oracle官网下载JDK1.8版本。http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html 。jdk-8u111-macosx-x64.dmg。双击安装。设置Java环境变量：

    JAVA_HOME='/usr/libexec/java_home'
    export JAVA_HOME

搭建Android SDK环境。Android官网下载Android SDK，https://developer.android.com 。25.0.2版本。android-sdk_r25.0.2-macosx.zip。解压到~/Library/Android/sdk目录。build-tools、extras、patcher、platform-tools #各版本SDK 根据API Level划分SDK版本、platforms、sources、system-images、temp #临时文件夹 在SDK更新安装时用到、tools #各版本通用SDK工具 有adb、aapt、aidl、dx文件。
搭建Android NDK环境。Android官网下载Android NDK Mac OS X版本，https://developer.android.com/ndk/downloads/index.html 。android-ndk-r13b-darwin-x86_64.zip文件。解压，CHANGELOG.md、build、ndk-build、ndk-depends、ndk-gdb、ndk-stack、ndk-which、platforms、prebuilt、python-packages、shader-tools、simpleperf、source.properties、sources、toolchains。搭建Bazel。brew安装bazel:

    brew install bazel

更新bazel:

    brew upgrade bazel

编译演示程序运行。修改tensorflow-1.1.0根目录WORKSPACE文件。android_sdk_repository、android_ndk_repository配置改为用户自己安装目录、版本。

    android_sdk_repository(
        name = "androidsdk",
        api_level = 25,
        build_tools_version = "25.0.2",
        # Replace with path to Android SDK on your system
        path = "~/Library/Android/sdk"
    )
    android_ndk_repository(
        name = "androidndk",
        api_level = 23,
        path = "~/Downloads/android-ndk-r13b"
    )

在根目录用bazel构建：

    bazel build // tensorflow/examples/android:tensorflow_demo

编译成功，默认在tensorflow-1.1.0/bazel-bin/tensorflow/examples/android目录生成TensorFlow演示程序。
运行。生成apk文件传输到手机，手机摄像头看效果。Android 6.0.1。开启“开发者模式”。手机用数据线与计算机相连，进入SDK所在目录，进入platform-tools文件夹，找到adb命令，执行：

    ./adb install tensorflow-0.12/bazel-bin/tensorflow/examples/android/tensorflow_demo.apk

tensorflow_demo.apk自动安装到手机。打开TF Detec App。App 调起手机摄像头，摄像头返回数据流实时监测。

自定义模型编译运行。训练原始模型、编译Android系统支持模型、生成Android apk文件运行。
训练原始模型、编译Android系统支持模型。用项目根目录tensorflow/python/tools/optimize_for_inference.py、tensorflow/tools/quantization/quantize_graph.py、tensorflow/contrib/util/convert_graphdef_memmapped_format.cc对模型优化。将第一步生成原始模型文件retrained_graph.pb、标记文件retrained_labels.txt放在tensorflow/examples/android/assets目录。修改tensorflow/examples/android/src/org/tensorflow/demo/TensorFlowImageClassifier.java要加载模型文件名称，输入图片尺寸、操作节点名字、缩放像素大小。

    package org.tensorflow.demo;
    import android.content.res.AssetManager;
    import android.graphics.Bitmap;
    import android.os.Trace;
    import android.util.Log;
    import java.io.BufferedReader;
    import java.io.IOException;
    import java.io.InputStreamReader;
    import java.util.ArrayList;
    import java.util.Comparator;
    import java.util.List;
    import java.util.PriorityQueue;
    import java.util.Vector;
    import org.tensorflow.Operation;
    import org.tensorflow.contrib.android.TensorFlowInferenceInterface;
    /** A classifier specialized to label images using TensorFlow. */
    public class TensorFlowImageClassifier implements Classifier {
      private static final String TAG = "TensorFlowImageClassifier";
      // Only return this many results with at least this confidence.
      private static final int MAX_RESULTS = 3;
      private static final float THRESHOLD = 0.1f;
      // Config values.
      private String inputName;
      private String outputName;
      private int inputSize;
      private int imageMean;
      private float imageStd;
      // Pre-allocated buffers.
      private Vector<String> labels = new Vector<String>();
      private int[] intValues;
      private float[] floatValues;
      private float[] outputs;
      private String[] outputNames;
      private boolean logStats = false;
      private TensorFlowInferenceInterface inferenceInterface;
      private TensorFlowImageClassifier() {}
      /**
       * Initializes a native TensorFlow session for classifying images.
       *
       * @param assetManager The asset manager to be used to load assets.
       * @param modelFilename The filepath of the model GraphDef protocol buffer.
       * @param labelFilename The filepath of label file for classes.
       * @param inputSize The input size. A square image of inputSize x inputSize is assumed.
       * @param imageMean The assumed mean of the image values.
       * @param imageStd The assumed std of the image values.
       * @param inputName The label of the image input node.
       * @param outputName The label of the output node.
       * @throws IOException
       */
      public static Classifier create(
          AssetManager assetManager,
          String modelFilename,
          String labelFilename,
          int inputSize,
          int imageMean,
          float imageStd,
          String inputName,
          String outputName) {
        TensorFlowImageClassifier c = new TensorFlowImageClassifier();
        c.inputName = inputName;
        c.outputName = outputName;
        // Read the label names into memory.
        // TODO(andrewharp): make this handle non-assets.
        String actualFilename = labelFilename.split("file:///android_asset/")[1];
        Log.i(TAG, "Reading labels from: " + actualFilename);
        BufferedReader br = null;
        try {
          br = new BufferedReader(new InputStreamReader(assetManager.open(actualFilename)));
          String line;
          while ((line = br.readLine()) != null) {
            c.labels.add(line);
          }
          br.close();
        } catch (IOException e) {
          throw new RuntimeException("Problem reading label file!" , e);
        }
        c.inferenceInterface = new TensorFlowInferenceInterface(assetManager, modelFilename);
        // The shape of the output is [N, NUM_CLASSES], where N is the batch size.
        final Operation operation = c.inferenceInterface.graphOperation(outputName);
        final int numClasses = (int) operation.output(0).shape().size(1);
        Log.i(TAG, "Read " + c.labels.size() + " labels, output layer size is " + numClasses);
        // Ideally, inputSize could have been retrieved from the shape of the input operation.  Alas,
        // the placeholder node for input in the graphdef typically used does not specify a shape, so it
        // must be passed in as a parameter.
        c.inputSize = inputSize;
        c.imageMean = imageMean;
        c.imageStd = imageStd;
        // Pre-allocate buffers.
        c.outputNames = new String[] {outputName};
        c.intValues = new int[inputSize * inputSize];
        c.floatValues = new float[inputSize * inputSize * 3];
        c.outputs = new float[numClasses];
        return c;
      }
      @Override
      public List<Recognition> recognizeImage(final Bitmap bitmap) {
        // Log this method so that it can be analyzed with systrace.
        Trace.beginSection("recognizeImage");
        Trace.beginSection("preprocessBitmap");
        // Preprocess the image data from 0-255 int to normalized float based
        // on the provided parameters.
        bitmap.getPixels(intValues, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());
        for (int i = 0; i < intValues.length; ++i) {
          final int val = intValues[i];
          floatValues[i * 3 + 0] = (((val >> 16) & 0xFF) - imageMean) / imageStd;
          floatValues[i * 3 + 1] = (((val >> 8) & 0xFF) - imageMean) / imageStd;
          floatValues[i * 3 + 2] = ((val & 0xFF) - imageMean) / imageStd;
        }
        Trace.endSection();
        // Copy the input data into TensorFlow.
        Trace.beginSection("feed");
        inferenceInterface.feed(inputName, floatValues, 1, inputSize, inputSize, 3);
        Trace.endSection();
        // Run the inference call.
        Trace.beginSection("run");
        inferenceInterface.run(outputNames, logStats);
        Trace.endSection();
        // Copy the output Tensor back into the output array.
        Trace.beginSection("fetch");
        inferenceInterface.fetch(outputName, outputs);
        Trace.endSection();
        // Find the best classifications.
        PriorityQueue<Recognition> pq =
            new PriorityQueue<Recognition>(
                3,
                new Comparator<Recognition>() {
                  @Override
                  public int compare(Recognition lhs, Recognition rhs) {
                    // Intentionally reversed to put high confidence at the head of the queue.
                    return Float.compare(rhs.getConfidence(), lhs.getConfidence());
                  }
                });
        for (int i = 0; i < outputs.length; ++i) {
          if (outputs[i] > THRESHOLD) {
            pq.add(
                new Recognition(
                    "" + i, labels.size() > i ? labels.get(i) : "unknown", outputs[i], null));
          }
        }
        final ArrayList<Recognition> recognitions = new ArrayList<Recognition>();
        int recognitionsSize = Math.min(pq.size(), MAX_RESULTS);
        for (int i = 0; i < recognitionsSize; ++i) {
          recognitions.add(pq.poll());
        }
        Trace.endSection(); // "recognizeImage"
        return recognitions;
      }
      @Override
      public void enableStatLogging(boolean logStats) {
        this.logStats = logStats;
      }
      @Override
      public String getStatString() {
        return inferenceInterface.getStatString();
      }
      @Override
      public void close() {
        inferenceInterface.close();
      }
    }

重新编译apk，连接Android手机，安装apk：

    bazel buld //tensorflow/examples/android:tensorflow_demo
    adb install -r -g bazel-bin/tensorflow/examples/android/tensorflow_demo.apk

树莓派实践。

Tensorflow可以在树莓派(Raspberry Pi)运行。树莓派，只有信用卡大小微型电脑，系统基于Linux，有音频、视频功能。应用，输入1万张自己的面部图片，在树莓派训练人脸识别模型，教会它认识你，你进入家门后，帮你开灯、播放音乐各种功能。树莓派编译方法和直接在Linux环境上用相似。

参考资料：
《TensorFlow技术解析与实战》

欢迎推荐上海机器学习工作机会，我的微信：qingxingfengzi