# Example of rclpy integration with a simple AI agent concept
# This demonstrates how to bridge AI agents with ROS controllers

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np


class SimpleAIAgent(Node):
    def __init__(self):
        super().__init__('simple_ai_agent')
        
        # Create subscription to laser scan data
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10)
        
        # Create publisher for velocity commands
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.get_logger().info('AI Agent initialized')

    def laser_callback(self, msg):
        # Simple AI logic to process laser data and decide on movement
        # This is a basic algorithm to avoid obstacles
        
        # Get the range data from laser scan
        ranges = np.array(msg.ranges)
        
        # Remove invalid measurements (inf, nan) and get minimum distance
        valid_ranges = ranges[np.isfinite(ranges)]
        if len(valid_ranges) > 0:
            min_distance = np.min(valid_ranges)
        else:
            min_distance = float('inf')
        
        # Create Twist message for robot movement
        cmd = Twist()
        
        # Simple logic: if obstacle is close, turn; otherwise move forward
        if min_distance < 1.0:  # obstacle within 1 meter
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5  # turn right
        else:
            cmd.linear.x = 0.5  # move forward
            cmd.angular.z = 0.0
        
        # Publish the command
        self.publisher.publish(cmd)
        self.get_logger().info(f'Published command: linear={cmd.linear.x}, angular={cmd.angular.z}')


def main(args=None):
    rclpy.init(args=args)
    ai_agent = SimpleAIAgent()
    
    try:
        rclpy.spin(ai_agent)
    except KeyboardInterrupt:
        pass
    finally:
        ai_agent.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()