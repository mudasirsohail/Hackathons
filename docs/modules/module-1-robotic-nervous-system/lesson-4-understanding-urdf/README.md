---
id: module-1-lesson-4-understanding-urdf-readme
---

# Lesson 4: Understanding URDF (Unified Robot Description Format)

## Overview
In this lesson, we'll explore URDF (Unified Robot Description Format), which is used to describe robots in ROS. URDF allows you to define the physical and visual properties of a robot, which is essential for simulation and planning, particularly for humanoid robots.

## Learning Objectives
By the end of this lesson, you will be able to:
- Understand the purpose and structure of URDF files
- Define robot links and joints in URDF
- Describe visual and collision properties of robot components
- Create a simple URDF model for a humanoid robot
- Load and visualize a URDF model in ROS

## What is URDF?
URDF (Unified Robot Description Format) is an XML format used in ROS to describe the physical properties of a robot. It contains information about the robot's:
- Kinematic structure (links and joints)
- Visual appearance (meshes, colors, and materials)
- Collision properties (collision geometry)
- Inertial properties (mass, center of mass, inertia tensor)

## URDF Structure: Links and Joints
Every robot model in URDF consists of two main elements:

### Links
- **Links** are rigid, unmovable parts of the robot
- Each link has properties like visual appearance, collision properties, and inertial characteristics
- Examples: robot base, arm segments, wheels

### Joints
- **Joints** connect links and define how they can move relative to each other
- Each joint has a type (fixed, revolute, continuous, prismatic, etc.) and limits
- Examples: rotational joints in robot arms, prismatic joints in linear actuators

## Basic URDF Example
Here is a simple URDF file for a basic robot:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Link for the first joint -->
  <link name="link1">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.2"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>

  <!-- Joint connecting base_link to link1 -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>
</robot>
```

## URDF for Humanoid Robots
Humanoid robots require special attention in their URDF descriptions:

### Key Components
- **Trunk/Torso**: The main body of the robot
- **Head**: With sensors like cameras and IMUs
- **Arms**: With multiple joints for manipulation
- **Legs**: With joints enabling bipedal locomotion
- **Hands/End Effectors**: For grasping and manipulation

### Special Considerations
- **Center of Mass**: Critical for stability in bipedal robots
- **Degrees of Freedom**: Humanoid robots typically have many joints
- **Kinematic Chains**: Multiple interconnected chains (arms, legs)

## Code Example: URDF for a Simple Humanoid Torso
Here's a URDF model for a simple humanoid torso with head:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid_torso">
  <!-- Base of the robot -->
  <link name="base_link">
    <inertial>
      <mass value="0.1"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Torso of the humanoid -->
  <link name="torso">
    <visual>
      <origin xyz="0 0 0.5"/>
      <geometry>
        <box size="0.3 0.3 1.0"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.5"/>
      <geometry>
        <box size="0.3 0.3 1.0"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0.5"/>
      <inertia ixx="0.3333" ixy="0.0" ixz="0.0" iyy="0.3333" iyz="0.0" izz="0.1666"/>
    </inertial>
  </link>

  <!-- Connection between base and torso -->
  <joint name="torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0"/>
  </joint>

  <!-- Head of the humanoid -->
  <link name="head">
    <visual>
      <origin xyz="0 0 0.15"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
      <material name="skin">
        <color rgba="0.8 0.6 0.4 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.15"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0.15"/>
      <inertia ixx="0.009" ixy="0.0" ixz="0.0" iyy="0.009" iyz="0.0" izz="0.009"/>
    </inertial>
  </link>

  <!-- Joint connecting torso to head -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 1.0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="10" velocity="2"/>
  </joint>

  <!-- Mounting point for sensors -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.1 0 0.1" rpy="0 0 0"/>
  </joint>
</robot>
```

## Visualization and Validation
Once you've created a URDF file, you can:
- Visualize it using RViz
- Check for errors with `check_urdf`
- Test kinematics with `urdf_to_graphiz`
- Simulate it in Gazebo

## Robot State Publisher
To properly display the robot in RViz, ROS uses the `robot_state_publisher` node to publish the robot's joint states and TF transforms.

## Summary
In this lesson, we explored URDF (Unified Robot Description Format), which is essential for describing robots in ROS. We learned about links and joints, the structure of URDF files, and how to create models for humanoid robots. URDF is crucial for simulation, visualization, and planning tasks in robotics.

## Previous Steps
Go back to [Lesson 3: Bridging Python Agents](./lesson-3-bridging-python-agents) to review how to connect Python-based AI agents with ROS controllers using rclpy.

## Next Steps
With Module 1 complete, you now have a solid foundation in ROS 2 fundamentals. You can continue with [Module 2: Digital Twin (Gazebo & Unity)](../../module-2-digital-twin/lesson-1-gazebo-simulation-basics) to learn about simulation environments.