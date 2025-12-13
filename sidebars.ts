import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'index',
    {
      type: 'category',
      label: 'Module 1: Robotic Nervous System (ROS 2)',
      items: [
        'modules/module-1-robotic-nervous-system/index',
        {
          type: 'category',
          label: 'Lessons',
          items: [
            'modules/module-1-robotic-nervous-system/lesson-1-introduction-to-ros2/module-1-lesson-1-introduction-to-ros2',
            'modules/module-1-robotic-nervous-system/lesson-2-ros2-nodes-topics-services/module-1-lesson-2-ros2-nodes-topics-services',
            'modules/module-1-robotic-nervous-system/lesson-3-bridging-python-agents/module-1-lesson-3-bridging-python-agents',
            'modules/module-1-robotic-nervous-system/lesson-4-understanding-urdf/module-1-lesson-4-understanding-urdf'
          ]
        }
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin (Gazebo & Unity)',
      items: [
        'modules/module-2-digital-twin/index',
        {
          type: 'category',
          label: 'Lessons',
          items: [
            'modules/module-2-digital-twin/lesson-1-gazebo-simulation-basics/module-2-lesson-1-gazebo-simulation-basics',
            'modules/module-2-digital-twin/lesson-2-unity-high-fidelity-rendering/module-2-lesson-2-unity-high-fidelity-rendering',
            'modules/module-2-digital-twin/lesson-3-sensor-simulation/module-2-lesson-3-sensor-simulation',
            'modules/module-2-digital-twin/lesson-4-physics-modeling/module-2-lesson-4-physics-modeling'
          ]
        }
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'modules/module-3-ai-robot-brain/index',
        {
          type: 'category',
          label: 'Lessons',
          items: [
            'modules/module-3-ai-robot-brain/lesson-1-nvidia-isaac-sim/module-3-lesson-1-nvidia-isaac-sim',
            'modules/module-3-ai-robot-brain/lesson-2-isaac-ros-vslam/module-3-lesson-2-isaac-ros-vslam',
            'modules/module-3-ai-robot-brain/lesson-3-nav2-path-planning/module-3-lesson-3-nav2-path-planning',
            'modules/module-3-ai-robot-brain/lesson-4-bipedal-locomotion/module-3-lesson-4-bipedal-locomotion'
          ]
        }
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'modules/module-4-vision-language-action/index',
        {
          type: 'category',
          label: 'Lessons',
          items: [
            'modules/module-4-vision-language-action/lesson-1-voice-to-action-whisper/module-4-lesson-1-voice-to-action-whisper',
            'modules/module-4-vision-language-action/lesson-2-cognitive-planning-llms/module-4-lesson-2-cognitive-planning-llms',
            'modules/module-4-vision-language-action/lesson-3-integration-examples/module-4-lesson-3-integration-examples',
            'modules/module-4-vision-language-action/lesson-4-capstone-autonomous-humanoid/module-4-lesson-4-capstone-autonomous-humanoid'
          ]
        }
      ],
    }
  ],
};

export default sidebars;
