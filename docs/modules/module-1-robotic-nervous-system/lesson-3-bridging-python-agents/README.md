---
id: module-1-lesson-3-bridging-python-agents-readme
---

# Lesson 3: Bridging Python Agents to ROS Controllers using rclpy

## Overview
In this lesson, we'll explore how to bridge Python-based AI agents with ROS controllers using rclpy, the Python client library for ROS 2. This integration is crucial for creating intelligent robotic systems where AI agents make decisions that control robot behavior.

## Learning Objectives
By the end of this lesson, you will be able to:
- Understand the role of rclpy in bridging Python agents and ROS systems
- Create ROS nodes that interface with external Python code
- Implement message passing between AI agents and ROS controllers
- Design a simple AI agent that controls a robot via ROS topics/services

## The Bridge Between AI and Robotics
Modern robotics increasingly relies on AI for perception, decision-making, and planning. Python is a popular language for AI development due to its rich ecosystem of libraries like TensorFlow, PyTorch, and scikit-learn. rclpy serves as the bridge between these AI capabilities and the ROS control systems.

## Understanding rclpy
rclpy is the Python client library for ROS 2. It provides Python bindings for the ROS 2 client library, allowing Python programs to:
- Create and manage ROS nodes
- Publish and subscribe to topics
- Create and use services
- Work with parameters and actions

## Code Example: AI Agent Node
Here's an example of a simple AI agent node that processes sensor data and sends commands to control a robot:

```python
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
```

## Code Example: AI Agent with Service Call
Here's an example of an AI agent that uses a service to request specific robot actions:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from std_srvs.srv import SetBool
import random


class ServiceBasedAIAgent(Node):
    def __init__(self):
        super().__init__('service_based_ai_agent')
        
        # Create client for a hypothetical navigation service
        self.nav_service_client = self.create_client(SetBool, 'navigation_service')
        
        # Wait for service to be available
        while not self.nav_service_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Navigation service not available, waiting again...')
        
        # Timer to periodically trigger AI decisions
        self.timer = self.create_timer(5.0, self.make_decision)
    
    def make_decision(self):
        # Simple AI decision making
        action = random.choice(['move_forward', 'turn_left', 'turn_right', 'stop'])
        
        self.get_logger().info(f'AI decision: {action}')
        
        # Call navigation service based on decision
        future = self.nav_service_client.call_async(self.create_service_request(action))
        future.add_done_callback(self.service_callback)
    
    def create_service_request(self, action):
        request = SetBool.Request()
        # Encode action in the request (simplified for example)
        request.data = action == 'move_forward'  # Example mapping
        return request
    
    def service_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('Navigation command executed successfully')
            else:
                self.get_logger().info(f'Navigation command failed: {response.message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    ai_agent = ServiceBasedAIAgent()
    
    try:
        rclpy.spin(ai_agent)
    except KeyboardInterrupt:
        pass
    finally:
        ai_agent.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Best Practices for AI-ROS Integration
- Keep AI processing separate from critical safety functions when possible
- Implement proper error handling and fallback behaviors
- Use appropriate QoS settings for different types of data
- Consider computational requirements when deploying on robot platforms
- Log AI decisions and robot responses for debugging and training

## Summary
In this lesson, we explored how to bridge Python-based AI agents with ROS controllers using rclpy. We created examples of AI agents that process sensor data to control robot movement and demonstrated how to integrate AI decision-making with ROS services. This integration is fundamental to creating intelligent robotic systems.

## Previous Steps
Go back to [Lesson 2: ROS 2 Nodes, Topics, and Services](./lesson-2-ros2-nodes-topics-services) to review the fundamental communication patterns in ROS 2.

## Next Steps
Continue to [Lesson 4: Understanding URDF](./lesson-4-understanding-urdf) to learn about the Unified Robot Description Format for describing humanoid robots.