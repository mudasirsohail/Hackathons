---
title: ROS 2 Nodes, Topics, and Services
id: module-1-lesson-2-ros2-nodes-topics-services
sidebar_position: 2
---

# ROS 2 Nodes, Topics, and Services

## Overview
This lesson focuses on the fundamental communication patterns in ROS 2: Nodes, Topics, and Services. Understanding these concepts is crucial for developing distributed robot applications.

## Learning Objectives
- Implement ROS 2 nodes in Python and C++
- Create publishers and subscribers for topic-based communication
- Develop services for request/response communication
- Use command-line tools to introspect ROS 2 communication

## Nodes
Nodes are the fundamental building blocks of ROS 2 applications. Each node performs a specific task and communicates with other nodes through topics, services, or actions.

## Topics and Publishers/Subscribers
Topics allow for asynchronous, decoupled communication using a publish-subscribe model. Publishers send messages to topics, and subscribers receive messages from topics.

## Services
Services provide synchronous request-response communication between nodes. When a client sends a request, the service processes it and returns a response.

## Practical Example
In this lesson, you'll create a simple publisher-subscriber pair that exchanges sensor data and a service that performs a simple calculation.

## Next Steps
After mastering these communication patterns, you'll learn about [Bridging Python Agents](./lesson-3-bridging-python-agents).