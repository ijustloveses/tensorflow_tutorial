介绍
=====
这个项目的前 11 章其实是[Tensorflow-Tutorial](https://github.com/Hvass-Labs/TensorFlow-Tutorials/)的实践，加入了我个人的理解和注释

环境搭建
=========
使用 tensorflow 的 Docker 容器
```
docker pull tensorflow/tensorflow
```
但是发现该 Docker image 没有安装 scikit-learn，故此在容器中运行
```
pip install scikit-learn
pip install pandas
```
然后提交新的镜像
```
docker commit 82fc7ba8fd60 tensorflow/tensorflow_and_other
```
再次运行
```
docker run -it -p 8888:8888 --rm tensorflow/tensorflow_and_other
```
可以在 ${ip}:8888 中看到 jupyter 正常运行

