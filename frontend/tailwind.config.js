/** @type {import('tailwindcss').Config} */
module.exports = {
  // Ensure this covers your React component files (e.g., .js, .jsx, .ts, .tsx)
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    // Add any other paths where you use Tailwind classes
    './src/**/*.{html,js}', // Ensure this matches your file structure
  ],
  darkMode: 'class', // This enables dark mode based on the 'dark' class
  theme: {
    extend: {
      colors: {
        // Define your theme colors, including light and dark variations
        // These will be used with classes like bg-light-background, text-dark-text, etc.
        light: {
          background: '#e0e0e0',
          surface: '#f0f0f0',
          text: '#333',
          primary: '#007bff', // Example primary color
          input: '#ebecf0', // Input background in light mode
        },
        dark: {
          background: '#1e1e1e',
          surface: '#2b2b2b',
          text: '#e0e0e0',
          primary: '#00bcd4', // Example primary color in dark mode
          input: '#3a3a3a', // Input background in dark mode
        },
        // You can define specific colors for your theme palettes here if needed
        // For example, for your themeColors object in React
        indigo: {
          DEFAULT: '#6366f1',
          light: '#e0e7ff',
          dark: '#4f46e5',
          darker: '#4338ca',
          text: '#4f46e5',
          darkText: '#e0e7ff',
        },
        emerald: {
          DEFAULT: '#10b981',
          light: '#d1fae5',
          dark: '#059669',
          darker: '#047857',
          text: '#059669',
          darkText: '#d1fae5',
        },
        rose: {
          DEFAULT: '#f43f5e',
          light: '#ffe4e6',
          dark: '#e11d48',
          darker: '#be123c',
          text: '#e11d48',
          darkText: '#ffe4e6',
        },
        amber: {
          DEFAULT: '#f59e0b',
          light: '#fef3c7',
          dark: '#d97706',
          darker: '#b45309',
          text: '#d97706',
          darkText: '#fef3c7',
        },
        blue: {
          DEFAULT: '#3b82f6',
          light: '#dbeafe',
          dark: '#2563eb',
          darker: '#1d4ed8',
          text: '#2563eb',
          darkText: '#dbeafe',
        },
        'light-background': '#f8f9fa', // Replace with your desired color
        'dark-background': '#343a40', // Add dark-background if needed
        'light-text': '#212529',
        'dark-text': '#f8f9fa',
      },
      boxShadow: {
        // Neomorphic shadows
        'neumorphic-outset': '5px 5px 10px #bebebe, -5px -5px 10px #ffffff',
        'neumorphic-outset-hover': '7px 7px 14px #bebebe, -7px -7px 14px #ffffff',
        'neumorphic-inset': 'inset 5px 5px 10px #bebebe, inset -5px -5px 10px #ffffff',
        'neumorphic-inset-active': 'inset 3px 3px 7px var(--tw-shadow-color-dark), inset -3px -3px 7px var(--tw-shadow-color-light)',
        // Island shadow for the input area
        'island': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
      // Define CSS variables for shadow colors, these will be set in your CSS file
      colors: {
         // ... existing colors
         'shadow-color-light': 'var(--shadow-light)',
         'shadow-color-dark': 'var(--shadow-dark)',
      }
    },
  },
  plugins: [],
}

