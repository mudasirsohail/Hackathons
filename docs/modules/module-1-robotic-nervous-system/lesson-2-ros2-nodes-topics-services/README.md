---
id: module-1-lesson-2-ros2-nodes-topics-services-readme
---

# Lesson 2: ROS 2 Nodes, Topics, and Services

## Overview
In this lesson, we'll explore the fundamental communication patterns in ROS 2: Nodes, Topics, and Services. These concepts form the backbone of how different parts of a robotic system interact with each other.

## Learning Objectives
By the end of this lesson, you will be able to:
- Understand the concept of a ROS 2 Node and its role
- Explain how Topics enable publisher-subscriber communication
- Describe the use of Services for request-response communication
- Compare when to use Topics vs Services for different communication needs

## ROS 2 Nodes
A **Node** is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 system - each node typically performs a specific task, such as controlling a motor, processing sensor data, or planning a path.

Multiple nodes work together to form a complete robotic application. Each node can communicate with other nodes by publishing and subscribing to topics, or by providing and using services.

## Topics and Publisher-Subscriber Pattern
**Topics** provide a way for nodes to communicate with each other using a publisher-subscriber model. This is an asynchronous communication method where:

- **Publishers** send data to a topic
- **Subscribers** receive data from a topic
- Multiple publishers and subscribers can use the same topic
- Communication is asynchronous - publishers and subscribers don't need to run simultaneously

This pattern is ideal for sensor data, robot state information, and other continuous data streams.

## Services and Client-Server Pattern
**Services** provide a synchronous request-response communication pattern:

- A **Service Server** provides a specific functionality
- A **Service Client** requests that functionality
- Communication is synchronous - the client waits for a response from the server
- Each service call is a discrete interaction

Services are ideal for actions that need a specific outcome, such as saving a map, executing a calibration sequence, or triggering a specific behavior.

## Code Example: Simple Publisher Node
Here's a basic example of a publisher node that sends "Hello" messages:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Code Example: Simple Subscriber Node
Here's a basic example of a subscriber node that receives messages:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## When to Use Topics vs Services
Use **Topics** when:
- You need continuous, asynchronous communication
- Multiple subscribers need the same data
- You need to broadcast information to many nodes
- The communication happens continuously over time

Use **Services** when:
- You need a specific action to be performed
- You need a response or result from the action
- The interaction is discrete and request-response in nature
- You need guaranteed delivery of a request and response

## Summary
In this lesson, we explored the three fundamental communication concepts in ROS 2: Nodes, Topics, and Services. These form the foundation for all robot communication in ROS 2. Nodes perform specific tasks, Topics enable asynchronous publisher-subscriber communication, and Services enable synchronous request-response communication.

## Previous Steps
Go back to [Lesson 1: Introduction to ROS 2](./lesson-1-introduction-to-ros2) to review the fundamentals of ROS 2.

## Next Steps
Continue to [Lesson 3: Bridging Python Agents](./lesson-3-bridging-python-agents) to learn about connecting Python-based AI agents with ROS controllers using rclpy.