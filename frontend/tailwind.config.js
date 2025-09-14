/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      colors: {
        // Neo-brutalism color palette
        'neo-black': '#0a0a0a',
        'neo-white': '#ffffff',
        'neo-gray': {
          100: '#f8f9fa',
          200: '#e9ecef',
          300: '#dee2e6',
          400: '#ced4da',
          500: '#6b7280',
          600: '#495057',
          700: '#343a40',
          800: '#212529',
          900: '#161618',
        },
        // Accent colors for interactive elements
        'accent': {
          'blue': '#3b82f6',
          'green': '#10b981',
          'red': '#ef4444',
          'yellow': '#f59e0b',
        }
      },
      borderWidth: {
        '3': '3px',
        '4': '4px',
        '6': '6px',
      },
      boxShadow: {
        'neo': '4px 4px 0px 0px #0a0a0a',
        'neo-lg': '8px 8px 0px 0px #0a0a0a',
        'neo-hover': '6px 6px 0px 0px #0a0a0a',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-in': 'slideIn 0.2s ease-out',
        'bounce-gentle': 'bounceGentle 0.6s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-10px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },
    },
  },
  plugins: [],
}