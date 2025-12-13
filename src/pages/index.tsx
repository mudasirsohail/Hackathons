import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">A Comprehensive Guide to Robotics, AI, and Humanoid Systems</p>
        <div className="hero-divider" style={{
          height: '3px',
          width: '100px',
          backgroundColor: '#4B0082',
          margin: '20px auto',
          borderRadius: '2px'
        }}></div>
        <div className="feature-strip" style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '30px',
          margin: '25px 0',
          flexWrap: 'wrap'
        }}>
          <div className="feature-item" style={{
            textAlign: 'center',
            padding: '10px 15px',
            borderRadius: '8px',
            backgroundColor: '#f9f1ff',
            color: '#4B0082',
            fontWeight: '500'
          }}>
            ROS 2
          </div>
          <div className="feature-item" style={{
            textAlign: 'center',
            padding: '10px 15px',
            borderRadius: '8px',
            backgroundColor: '#f9f1ff',
            color: '#4B0082',
            fontWeight: '500'
          }}>
            Digital Twin
          </div>
          <div className="feature-item" style={{
            textAlign: 'center',
            padding: '10px 15px',
            borderRadius: '8px',
            backgroundColor: '#f9f1ff',
            color: '#4B0082',
            fontWeight: '500'
          }}>
            Humanoid AI
          </div>
        </div>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/docs">
            Start Learning
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/docs">
            Explore Modules
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
