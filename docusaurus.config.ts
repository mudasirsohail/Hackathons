// import {themes as prismThemes} from 'prism-react-renderer';
// import type {Config} from '@docusaurus/types';
// import type * as Preset from '@docusaurus/preset-classic';

// // This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

// const config: Config = {
//   title: 'Physical AI & Humanoid Robotics',
//   tagline: 'A Comprehensive Guide to Robotics, AI, and Humanoid Systems',
//   favicon: 'img/favicon.ico',

//   // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
//   future: {
//     v4: true, // Improve compatibility with the upcoming Docusaurus v4
//   },

//   // Set the production url of your site here
//   url: 'https://your-organization.github.io',
//   // Set the /<baseUrl>/ pathname under which your site is served
//   // For GitHub pages deployment, it is often '/<org-name>/<repo-name>/'
//   baseUrl: '/physical-ai-humanoid-robotics/',

//   // GitHub pages deployment config.
//   organizationName: 'your-organization', // Usually your GitHub org/user name.
//   projectName: 'physical-ai-humanoid-robotics', // Usually your repo name.

//   onBrokenLinks: 'ignore',
//   onBrokenMarkdownLinks: 'ignore',

//   // Even if you don't use internationalization, you can use this field to set
//   // useful metadata like html lang. For example, if your site is Chinese, you
//   // may want to replace "en" with "zh-Hans".
//   i18n: {
//     defaultLocale: 'en',
//     locales: ['en'],
//   },

//   presets: [
//     [
//       'classic',
//       {
//         docs: {
//           sidebarPath: './sidebars.ts',
//           // Please change this to your repo.
//           // Remove this to remove the "edit this page" links.
//           editUrl:
//             'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
//         },
//         blog: {
//           showReadingTime: true,
//           // Please change this to your repo.
//           // Remove this to remove the "edit this page" links.
//           editUrl:
//             'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
//         },
//         theme: {
//           customCss: './src/css/custom.css',
//         },
//       } satisfies Preset.Options,
//     ],
//   ],

//   themeConfig: {
//     // Replace with your project's social card
//     image: 'img/docusaurus-social-card.jpg',
//     navbar: {
//       title: 'Physical AI & Humanoid Robotics',
//       logo: {
//         alt: 'Physical AI & Humanoid Robotics Logo',
//         src: 'img/logo.svg',
//       },
//       items: [
//         {
//           type: 'docSidebar',
//           sidebarId: 'tutorialSidebar',
//           position: 'left',
//           label: 'Book',
//         },
//         {
//           href: 'https://github.com/facebook/docusaurus',
//           label: 'GitHub',
//           position: 'right',
//         },
//       ],
//     },
//     // Add custom fonts via Google Fonts
//     metadata: [
//       {
//         name: 'google-fonts',
//         content: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
//       },
//     ],
//     footer: {
//       style: 'dark',
//       links: [
//         {
//           title: 'Docs',
//           items: [
//             {
//               label: 'Book',
//               to: '/docs/modules/module-1-robotic-nervous-system',
//             },
//           ],
//         },
//         {
//           title: 'Community',
//           items: [
//             {
//               label: 'Stack Overflow',
//               href: 'https://stackoverflow.com/questions/tagged/docusaurus',
//             },
//             {
//               label: 'Discord',
//               href: 'https://discordapp.com/invite/docusaurus',
//             },
//           ],
//         },
//         {
//           title: 'More',
//           items: [
//             {
//               label: 'GitHub',
//               href: 'https://github.com/facebook/docusaurus',
//             },
//           ],
//         },
//       ],
//       copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
//     },
//     prism: {
//       theme: prismThemes.github,
//       darkTheme: prismThemes.dracula,
//     },
//   } satisfies Preset.ThemeConfig,
// };

// export default config;




// @ts-check
// `@type` JSDoc annotations allow IDEs and type checkers to infer types
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
    // Plugin to add the chat widget to all pages
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
        injectHtmlTags() {
          return {
            postBodyTags: [
              `<script>
                // Global variable for API configuration
                window.API_CONFIG = {
                  baseUrl: 'https://mudasirsohail-physical-ai-backend-2edf874.hf.space'
                };
              </script>`,
            ],
          };
        },
      };
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      metadata: [
        {
          name: 'google-fonts',
          content: 'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&family=Lato:wght@400;500;600;700&display=swap',
        },
      ],
      colorMode: {
        defaultMode: 'light',
        disableSwitch: true,  // Disable dark mode to ensure consistent theme
        respectPrefersColorScheme: false,
      },
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
