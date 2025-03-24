# import sys
# sys.path.append('/opt/ros/foxy/lib/python3.8/site-packages/rclpy')
import rclpy
import json
from rclpy.node import Node
from interfaces.msg import AutoaimData
# from autoaim_data.detect import detect

class NodePublisher(Node):
    def __init__(self):
        super().__init__('autoaim_publisher')
        self.publisher_ = self.create_publisher(
             AutoaimData, 
             'autoaim_topic', 
             10
             )
        self.timer = self.create_timer(1.0, self.timer_callback)  # 每秒发布一次
        self.get_logger().info('Autoaim Publisher Node started.')

    def timer_callback(self):
        """
        定时器回调函数
        """
        with open("/home/jetson/ros2/autoaim_ws/arc_values.json", "r") as f:
            data = json.load(f)

        msg = AutoaimData()
        msg.yaw_angle_diff = data["x_arc"] 
        msg.pitch_angle_diff = data["y_arc"]  
        msg.fire = data["is_fire"]  # 发射信号

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: yaw_angle_diff={msg.yaw_angle_diff}, pitch_angle_diff={msg.pitch_angle_diff}, fire={msg.fire}')

def main(args=None):
        rclpy.init(args=args) # 初始化rclpy
        node = NodePublisher()  # 新建一个节点
        rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
        rclpy.shutdown() # 关闭rclpy

if __name__ == '__main__':
    main()
