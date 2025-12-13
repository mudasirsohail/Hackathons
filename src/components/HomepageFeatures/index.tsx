import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

type ModuleFeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
  to: string;
};

const ModuleFeatureList: ModuleFeatureItem[] = [
  {
    title: 'Module 1: Robotic Nervous System (ROS 2)',
    Svg: require('@site/static/img/robot-nervous-system.svg').default,
    description: (
      <>
        Master the middleware for robot control. Learn ROS 2 Nodes, Topics, Services, bridging Python Agents to ROS controllers,
        and understanding URDF for humanoids.
      </>
    ),
    to: '/docs/modules/module-1-robotic-nervous-system',
  },
  {
    title: 'Module 2: Digital Twin (Gazebo & Unity)',
    Svg: require('@site/static/img/digital-twin.svg').default,
    description: (
      <>
        Simulate physics, gravity, and collisions in Gazebo. Explore high-fidelity rendering in Unity and simulate various sensors like LiDAR and IMUs.
      </>
    ),
    to: '/docs/modules/module-2-digital-twin',
  },
  {
    title: 'Module 3: AI-Robot Brain (NVIDIA Isaac™)',
    Svg: require('@site/static/img/ai-brain.svg').default,
    description: (
      <>
        Advanced perception using NVIDIA Isaac Sim for photorealistic simulation, Isaac ROS for hardware-accelerated VSLAM,
        and Nav2 for path planning for bipedal movement.
      </>
    ),
    to: '/docs/modules/module-3-ai-robot-brain',
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    Svg: require('@site/static/img/vision-language-action.svg').default,
    description: (
      <>
        Convergence of LLMs and Robotics: voice-to-action using OpenAI Whisper, cognitive planning using LLMs to translate
        natural language into ROS 2 actions.
      </>
    ),
    to: '/docs/modules/module-4-vision-language-action',
  },
  {
    title: 'Capstone Project',
    Svg: require('@site/static/img/ai-brain.svg').default,
    description: (
      <>
        Integrate everything you've learned in the Autonomous Humanoid project, combining all modules for a complete robot system.
      </>
    ),
    to: '/docs/modules/module-4-vision-language-action/lesson-4-capstone-autonomous-humanoid',
  },
  {
    title: 'Industry-Aligned',
    Svg: require('@site/static/img/robot-nervous-system.svg').default,
    description: (
      <>
        Curriculum designed with industry standards in mind, using tools and technologies employed by robotics companies worldwide.
      </>
    ),
    to: '/docs',
  },
];

function Feature({title, Svg, description, to}: ModuleFeatureItem) {
  return (
    <Link to={to} className={clsx('col col--4 padding--md', styles.featureLink)}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </Link>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {ModuleFeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}