# 一、简介
  本项目为战云智能交通检测系统，前端为Detector_client，部署于智能检测的交通摄像机边缘端，由于模型经过模型压缩，参数量小，可实现实时的违章检测，完成车辆识别、行人识别、交通灯识别、闯红灯、不礼让行人、车流检测等功能，并识别违章车辆的车牌号与记录截图，传入后端数据库。后端部分由两部分组成：Front_web与Back_web.
# 二、环境安装
  ## 1. 安装miniconda后，建立并激活虚拟环境traffic_detection:
  ```
  conda create -n traffic_detection python=3.6
  # 查看存在的虚拟环境
  conda env list
  conda activate traffic_detection
  ```
  ## 2. 安装依赖
  （推荐）安装完conda后，因为已将环境导入traffic_detection.yaml文件中，所以只需执行以下脚本可完成虚拟环境的配置：
  ```
  conda env create -f traffic_detection.yaml
  ```
  如果不习惯以上安装习惯，也在三个子项目文件夹下检查所需环境并运行:
  ```
  pip install -r requirement.txt
  ```
  对于Detector_client需要安装Tensorflow 开发扩展包：object_detection
# Detector_client
  此文件夹包含前端检测程序，配置依赖无误后运行以下脚本:
  ```
  python VehicleMonitor.py
  ```
# Front_web
  此文件夹包含后端服务器中用于界面展示与相关统计的程序，配置依赖无误后运行以下脚本:
  ```
  python app.py
  ```
# Back_web
 此文件夹包含后端服务器中用于管理员后台数据管理与修改统计的程序，配置依赖无误后运行以下脚本:
  ```
  python run.py
  ```
数据库采用Sqlite3, Ubuntu 20.04LTS中默认安装，无需单独安装，文件位置为./Back_web/app.db