---
title: Nav2 Path Planning
id: module-3-lesson-3-nav2-path-planning
sidebar_position: 3
---

# Nav2 Path Planning

## Overview
This lesson focuses on Nav2, the navigation stack for ROS 2. You'll learn to implement path planning algorithms for mobile robots, with special attention to bipedal humanoid movement challenges.

## Learning Objectives
- Configure Nav2 for different robot types and environments
- Implement global and local path planning algorithms
- Handle dynamic obstacles and replanning scenarios
- Adapt navigation for bipedal humanoid locomotion
- Integrate perception data with navigation decisions

## Nav2 Architecture
Nav2 is a behavior-based navigation system with configurable task servers, supporting multiple plugins for different navigation behaviors.

## Global vs. Local Planning
- **Global Planner**: Computes optimal path from start to goal using static map
- **Local Planner**: Executes path while avoiding dynamic obstacles and maintaining robot kinematics

## Bipedal Navigation Considerations
Humanoid robots have unique navigation challenges due to their bipedal locomotion, center of mass, and balance requirements.

## Components of Nav2
- Map Server
- Localization (AMCL)
- Global Planner
- Local Planner
- Controller
- Recovery Behaviors

## Practical Exercise
Configure Nav2 for a humanoid robot simulation, implementing path planning with appropriate parameters for bipedal locomotion.

## Next Steps
After learning path planning, you'll explore [Bipedal Locomotion](./lesson-4-bipedal-locomotion).