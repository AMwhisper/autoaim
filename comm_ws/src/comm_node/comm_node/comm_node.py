import rclpy
import serial
from rclpy.node import Node
from comm_node.pack import pack_autoaim_data
from interfaces.msg import AutoaimData

class AutoAimSender(Node):
    def __init__(self):
        super().__init__('autoaim_sender')
        self.serial_port = serial.Serial(
            port='/dev/ttyACM0',  
            baudrate=115200,
            timeout=0.1
        ) # 打开串口 

        self.subscription = self.create_subscription(
            AutoaimData,
            'autoaim_topic',  
            self.autoaim_callback,
            10
        ) # 订阅自瞄解算数据
        
        self.seq = 0
        self.last_data = None  # 存储最近一次数据
        self.timer = self.create_timer(0.05, self.send_last_autoaim_data)  # 20Hz 

    def autoaim_callback(self, msg):
        yaw_angle_diff = round(msg.yaw_angle_diff, 6)
        pitch_angle_diff = round(msg.pitch_angle_diff, 6)
        fire = msg.fire
        
        self.last_data = (yaw_angle_diff, pitch_angle_diff, fire)
        self.get_logger().info(f'收到[{yaw_angle_diff:.6f},{pitch_angle_diff:.6f},{fire}]')

    def send_last_autoaim_data(self):
        if self.last_data is not None:
            yaw_angle_diff, pitch_angle_diff, fire = self.last_data
            self.send_autoaim_data(yaw_angle_diff, pitch_angle_diff, fire)
        else:
            self.get_logger().warn("No data to send yet.")

    def send_autoaim_data(self, yaw_angle_diff, pitch_angle_diff, fire):
        packet = pack_autoaim_data(yaw_angle_diff, pitch_angle_diff, fire, self.seq)
        self.seq = (self.seq + 1) % 256  
        
        try:
            self.serial_port.write(packet)
            self.get_logger().info(f'Sent autoaim data: yaw_angle_diff={yaw_angle_diff:.6f}, pitch_angle_diff={pitch_angle_diff:.6f}, fire={fire}, packet={packet.hex()}')
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to send data: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = AutoAimSender()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
