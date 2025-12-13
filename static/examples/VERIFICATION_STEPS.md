# Verification Steps for ROS 2 Code Examples

## Prerequisites
- ROS 2 Humble Hawksbill installed
- Python 3.8+ 
- rclpy package installed

## Publisher Example (ros2-publisher.py)
1. Make sure your ROS 2 environment is sourced:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

2. Run the publisher example:
   ```bash
   python3 ros2-publisher.py
   ```

3. In a separate terminal, check if messages are being published:
   ```bash
   source /opt/ros/humble/setup.bash
   ros2 topic echo /topic std_msgs/msg/String
   ```

4. You should see messages being published every 0.5 seconds in the format "Hello World: X" where X is an incrementing number.

## Subscriber Example (ros2-subscriber.py)
1. Make sure your ROS 2 environment is sourced:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

2. First run the publisher (in terminal 1):
   ```bash
   python3 ros2-publisher.py
   ```

3. In a separate terminal (terminal 2), run the subscriber:
   ```bash
   python3 ros2-subscriber.py
   ```

4. The subscriber should print "I heard: '[message]'" for each message published by the publisher.

## Service Example (Conceptual - ros2-service.py)
1. The code example demonstrates the server side of a ROS 2 service that adds two integers.
2. To test this, you would need a corresponding client that calls the 'add_two_ints' service.
3. Run the service server:
   ```bash
   python3 ros2-service.py
   ```
4. In a separate terminal, call the service:
   ```bash
   ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
   ```
5. The server should return a response with sum = 5.

## rclpy Integration Example (rclpy-integration.py)
1. This example demonstrates a simple AI agent that:
   - Subscribes to laser scan data on the 'scan' topic
   - Publishes velocity commands on the 'cmd_vel' topic
   - Implements basic obstacle avoidance logic

2. To verify:
   - Run the AI agent node:
     ```bash
     python3 rclpy-integration.py
     ```
   - In a separate terminal, publish mock laser scan data:
     ```bash
     ros2 topic pub /scan sensor_msgs/msg/LaserScan --field=ranges=[1.0,1.0,1.0,1.0,1.0]
     ```
   - Check that the agent publishes velocity commands to cmd_vel:
     ```bash
     ros2 topic echo /cmd_vel geometry_msgs/msg/Twist
     ```

## Expected Results for Success Criteria (SC-001)
- 85% of readers can successfully implement a publisher-subscriber example
- Both publisher and subscriber nodes run without errors
- Messages successfully pass from publisher to subscriber
- Verification steps confirm the communication works as expected