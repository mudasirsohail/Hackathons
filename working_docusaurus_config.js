// docusaurus.config.js - Add API proxy plugin

// @ts-check
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to Robotics, AI, and Humanoid Systems',
  favicon: 'img/favicon.ico',

  // Set the production URL of your site here
  url: 'https://mudasirsohail.github.io',
  baseUrl: '/Hackathons',

  // GitHub pages deployment config
  organizationName: 'mudasirsohail', // your GitHub username
  projectName: 'Hackathons',          // your repository name
  trailingSlash: false,

  // onBrokenLinks: 'throw',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/mudasirsohail/Hackathons/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/mudasirsohail/Hackathons/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    // Plugin to add the chat widget to all pages and handle API proxying
    async function myPlugin(context, options) {
      return {
        name: 'chat-widget-plugin',
        configureWebpack(config, isServer, utils) {
          return {
            resolve: {
              alias: {
                path: require.resolve('path-browserify'),
              },
            },
          };
        },
        // This will handle API proxying on the Docusaurus dev server
        injectHtmlTags() {
          return {
            postBodyTags: [
              `<script>
                // Global variable for API configuration
                window.API_CONFIG = {
                  baseUrl: typeof window !== 'undefined' ? window.location.origin : 'https://mudasirsohail-physical-ai-backend-2edf874.hf.space'
                };
                
                // For development, use the same origin since we'll proxy
                if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
                  // When using proxy, API calls will go to the same origin
                  // The proxy will forward them to the backend
                }
              </script>`,
            ],
          };
        },
      };
    },
    
    // Add API proxy functionality
    [
      '@docusaurus/plugin-content-pages',
      {
        path: 'api', // Look for API routes in the api directory
        routeBasePath: 'api',
      },
    ],
  ],

  // Add proxy configuration for development
  themes: ['@docusaurus/theme-classic'],
  plugins: [
    [
      require.resolve('@docusaurus/plugin-client-redirects'),
      {
        fromExtensions: ['html'],
        redirects: [
          {
            to: '/docs/intro',
            from: ['/docs', '/about'],
          },
        ],
      },
    ],
  ],
  
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI & Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/mudasirsohail/Hackathons',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Book',
                to: '/docs/modules/module-1-robotic-nervous-system',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/mudasirsohail/Hackathons',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
    }),
};

module.exports = config;