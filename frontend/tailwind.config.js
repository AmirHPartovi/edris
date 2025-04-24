/** @type {import('tailwindcss').Config} */
module.exports = {
  // Ensure this covers your React component files (e.g., .js, .jsx, .ts, .tsx)
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    // Add any other paths where you use Tailwind classes
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
          light: '#eef2ff', // indigo-50
          dark: '#4f46e5', // indigo-600
          darker: '#4338ca', // indigo-700
          text: '#4f46e5', // indigo-600
          darkText: '#a5b4fc', // indigo-400
        },
         emerald: {
          DEFAULT: '#10b981',
          light: '#ecfdf5', // emerald-50
          dark: '#059669', // emerald-600
          darker: '#047857', // emerald-700
          text: '#059669', // emerald-600
          darkText: '#6ee7b7', // emerald-400
        },
        rose: {
          DEFAULT: '#f43f5e',
          light: '#fff1f2', // rose-50
          dark: '#e11d48', // rose-600
          darker: '#be123c', // rose-700
          text: '#e11d48', // rose-600
          darkText: '#fda4af', // rose-400
        },
        amber: {
          DEFAULT: '#f59e0b',
          light: '#fffbeb', // amber-50
          dark: '#d97706', // amber-600
          darker: '#b45309', // amber-700
          text: '#d97706', // amber-600
          darkText: '#fcd34d', // amber-400
        },
        blue: {
          DEFAULT: '#3b82f6',
          light: '#eff6ff', // blue-50
          dark: '#2563eb', // blue-600
          darker: '#1d4ed8', // blue-700
          text: '#2563eb', // blue-600
          darkText: '#93c5fd', // blue-400
        },
      },
      boxShadow: {
        // Neomorphic shadows
        'neumorphic-outset': '7px 7px 15px var(--tw-shadow-color-dark), -7px -7px 15px var(--tw-shadow-color-light)',
        'neumorphic-outset-hover': '4px 4px 10px var(--tw-shadow-color-dark), -4px -4px 10px var(--tw-shadow-color-light)',
        'neumorphic-inset': 'inset 5px 5px 10px var(--tw-shadow-color-dark), inset -5px -5px 10px var(--tw-shadow-color-light)',
        'neumorphic-inset-active': 'inset 3px 3px 7px var(--tw-shadow-color-dark), inset -3px -3px 7px var(--tw-shadow-color-light)',
        // Island shadow for the input area
        'island': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
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

