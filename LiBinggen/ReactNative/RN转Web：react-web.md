​1．安装ReactWeb命令行工具：npm install react-web-cli -g
2．在RN工程的上级目录执行命令：react-web init <ProjectName>
3．提示已经存在目录，输入 yes ，继续安装执行
4．进入工程目录，安装 react-dom ,  npm install react-dom –save
5．本地图片的加载处理。安装  file-loader : npm install --save file-loader
6．在 web/webpack.config.js 文件里面，加入代码：
{
       test: /\.(eot|otf|svg|ttf|woff|woff2|png|jpg|gif)\w*/,
       loader: 'file'
}
7．修改web/webpack.config.js 的开发选项设置：devtool: false
8．在RN入口文件index.ios.js头部引用Platform，并在末尾加入代码：
if(Platform.OS == 'web'){
  varapp = document.createElement('div');
 document.body.appendChild(app);
 AppRegistry.runApplication('moduleName', {
   rootTag: app
  });
}
9．运行打包命令react-web bundle，在web/output目录下生成了Web版文件，打开index.html就可以看到程序运行效果。
10．退回工程目录，运行命令react-web start，可以在浏览器输入localhost:3000 进行访问。