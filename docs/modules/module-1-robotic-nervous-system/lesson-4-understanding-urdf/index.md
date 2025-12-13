---
title: Understanding URDF
id: module-1-lesson-4-understanding-urdf
sidebar_position: 4
---

# Understanding URDF

## Overview
URDF (Unified Robot Description Format) is the standard for representing robot models in ROS. This lesson covers creating and working with URDF files to define robot kinematics, dynamics, and visual properties.

## Learning Objectives
- Create complete URDF files for humanoid robots
- Define robot geometry, materials, and collision properties
- Understand joints, links, and kinematic chains in URDF
- Visualize URDF models in RViz and Gazebo

## URDF Components
- **Links**: Rigid parts of the robot (e.g., arms, legs, torso)
- **Joints**: Connections between links with specific kinematic properties
- **Visual**: How the robot appears in visualization tools
- **Collision**: How the robot interacts with the environment in simulation
- **Inertial**: Dynamic properties for physics simulation

## Humanoid Robot Considerations
Humanoid robots require special attention to joint limits, center of mass, and balance. You'll learn to model the human-like structure with appropriate joint constraints.

## Practical Exercise
Create a URDF for a simple humanoid model with proper joint constraints and visual representations.

## Next Steps
After mastering URDF, you'll move to Module 2: [Digital Twin (Gazebo & Unity)](../../module-2-digital-twin/lesson-1-gazebo-simulation-basics).