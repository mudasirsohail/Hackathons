---
id: module-2-lesson-1-gazebo-simulation-basics-readme
---

# Lesson 1: Gazebo Simulation Basics

## Overview
In this lesson, we'll introduce Gazebo, a powerful physics simulation environment used extensively in robotics. You'll learn the basics of setting up and working with Gazebo for robotics applications, including how to create basic robot models and environments.

## Learning Objectives
By the end of this lesson, you will be able to:
- Understand the role and capabilities of Gazebo in robotics simulation
- Set up a basic Gazebo environment
- Load and manipulate simple robot models in Gazebo
- Configure basic physics properties like gravity and collisions
- Interact with the Gazebo GUI and understand its main components

## What is Gazebo?
Gazebo is a 3D dynamic simulator with the ability to accurately and efficiently simulate populations of robots in complex indoor and outdoor environments. It provides:

- High-fidelity physics simulation based on ODE (Open Dynamics Engine)
- High-quality graphics rendering using OGRE
- Support for various sensors including cameras, LiDAR, IMU, GPS, and more
- Plugins system for custom robot and sensor models
- Integration with ROS/ROS2 for realistic robot simulation

## Installing and Setting Up Gazebo
Gazebo Garden is the recommended version for ROS 2 Humble. Installation typically involves:

```bash
sudo apt install ros-humble-gazebo-ros-pkgs
```

## Basic Gazebo Components
- **World Files**: XML files that define the simulation environment including models, lighting, and physics properties
- **Model Files**: URDF or SDF files that describe robot and object models
- **GUI**: The graphical user interface for interacting with the simulation
- **Server**: The headless backend that runs the physics simulation

## Launching Gazebo
You can launch Gazebo with a default empty world:

```bash
gz sim (for Garden version)
# or for older versions:
gazebo
```

## Basic World File Example
Here's a minimal Gazebo world file:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="default">
    <light name="sun" type="directional">
      <cast_shadows>1</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.6 0.4 -0.8</direction>
    </light>
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.8 0.8 0.8 1</specular>
          </material>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

## Loading Models in Gazebo
Models can be loaded into Gazebo in several ways:
- Through the GUI insert tab
- Defined in world files
- Spawned programmatically via ROS services

## Basic Robot Model Example (SDF)
Simple robot model in SDF format:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_box_robot">
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.083</ixx>
          <iyy>0.083</iyy>
          <izz>0.083</izz>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyz>0</iyz>
        </inertia>
      </inertial>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.2 0.2 0.2</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.2 0.2 0.2</size>
          </box>
        </geometry>
        <material>
          <ambient>0.8 0.2 0.2 1</ambient>
          <diffuse>0.8 0.2 0.2 1</diffuse>
        </material>
      </visual>
    </link>
  </model>
</sdf>
```

## Gazebo Tools and Controls
- **Play/Pause**: Control the simulation time
- **Reset**: Reset the simulation to initial state
- **Step**: Advance simulation by one time step
- **Translate/Rotate**: Move models in the environment
- **Layers**: Show/hide different elements

## Summary
This lesson introduced Gazebo as a physics simulation environment for robotics. We covered the basic components, how to set up and run Gazebo, and how to define simple worlds and models. In the next lesson, we'll explore Unity for high-fidelity rendering and human-robot interaction.

## Next Steps
Continue to [Lesson 2: Unity High Fidelity Rendering](./lesson-2-unity-high-fidelity-rendering) to learn about Unity for robotics applications.