# Autoaim and Communication to STM32
本工程包括autoaim_ws 和 comm_ws两个文件夹。下面会分别介绍。
## autoaim_ws
这是一个自瞄算法，通过运行detect.py 文件获得yaw轴转动角度、pitch轴转动角度以及是否开火，并将其存储在arc_values.json文件内。  
在启动时添加启动项可以更改权重文件等。
## comm_ws
这是一个基于ros2的上下位机通讯包，用于通过串口发布自瞄数据到STM32。  
数据结构根据下位机结构体调整，采用USART发送，波特率115200。  
下载源码后先编译：  
```
cd /comm_ws
colcon build
```
然后运行autoaim_data 和 comm_node 两个包：
```
source install.setup.bash
ros2 run autoaim_data autoaim_data
```
新开一个终端：
```
source install.setup.bash
ros2 run comm_node comm_node
```
运行后可以看到输出的日志。
## requirement.txt
本工程基于python3.8构建，强烈建议在**虚拟环境**中进行！  
因为jetson orin nano 的cpu为ARM架构，本requirement.txt仅提供对照参考，有问题可以根据此来对比。    
所以在配环境时**不要**
```
pip install -r requirement.txt
```
有些包需要上开源社区找资源，例如pytorch。  
**安装pytorch请不要使用**  
```
pip install torch torchvision
```
请前往Nvidia官网Pytorch for jetson 寻找对应版本。torchvision根据torch版本选择, Instructions一栏有版本对应关系。
> https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048

