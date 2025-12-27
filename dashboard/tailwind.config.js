/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: '#6366f1', // Indigo 500 - Modern Primary
        secondary: '#ec4899', // Pink 500 - Vibrant Secondary
        background: '#f8fafc', // Slate 50
        surface: '#ffffff', // White
        'surface-highlight': '#f1f5f9', // Slate 100
        muted: '#64748b', // Slate 500
        border: '#e2e8f0', // Slate 200
        success: '#10b981', // Emerald 500
        danger: '#ef4444', // Red 500
        warning: '#f59e0b', // Amber 500
        info: '#3b82f6', // Blue 500
      },
      fontFamily: {
        display: ['Inter', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        DEFAULT: '0.75rem', // 12px
        lg: '1rem',
        xl: '1.5rem',
        '2xl': '2rem',
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(15, 23, 42, 0.05)', // Subtle shadow for cards
        'glow-primary': '0 0 20px rgba(99, 102, 241, 0.2)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.05)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}
