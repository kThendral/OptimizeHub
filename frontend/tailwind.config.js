/** @type {import('tailwindcss').Config} */
  import react from '@vitejs/plugin-react';
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.8s ease-out forwards',
        'fade-in-right': 'fadeInRight 0.8s ease-out forwards',
        'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'floatDelayed 7s ease-in-out infinite',
        'float-slow': 'floatSlow 8s ease-in-out infinite',
        'gradient-shift': 'gradientShift 4s ease infinite',
        'glow-pulse': 'glowPulse 2.5s ease-in-out infinite',
        'bar-grow': 'barGrow 1.2s ease-out forwards',
        'scale-pulse': 'scalePulse 2s ease-in-out infinite',
        'slide-in-left': 'slideInLeft 0.6s ease-out',
        'slide-in-up': 'slideInUp 0.6s ease-out',
      },
      keyframes: {
        fadeIn: {
          'from': {
            'opacity': '0',
            'transform': 'translateY(20px)',
          },
          'to': {
            'opacity': '1',
            'transform': 'translateY(0)',
          },
        },
        fadeInRight: {
          'from': {
            'opacity': '0',
            'transform': 'translateX(40px)',
          },
          'to': {
            'opacity': '1',
            'transform': 'translateX(0)',
          },
        },
        fadeInUp: {
          'from': {
            'opacity': '0',
            'transform': 'translateY(40px)',
          },
          'to': {
            'opacity': '1',
            'transform': 'translateY(0)',
          },
        },
        float: {
          '0%, 100%': {
            'transform': 'translateY(0px) translateX(0px)',
          },
          '33%': {
            'transform': 'translateY(-20px) translateX(10px)',
          },
          '66%': {
            'transform': 'translateY(-10px) translateX(-10px)',
          },
        },
        floatDelayed: {
          '0%, 100%': {
            'transform': 'translateY(0px) translateX(0px)',
          },
          '33%': {
            'transform': 'translateY(25px) translateX(-15px)',
          },
          '66%': {
            'transform': 'translateY(10px) translateX(15px)',
          },
        },
        floatSlow: {
          '0%, 100%': {
            'transform': 'translateY(0px)',
          },
          '50%': {
            'transform': 'translateY(-30px)',
          },
        },
        gradientShift: {
          '0%': {
            'background-position': '0% 50%',
          },
          '50%': {
            'background-position': '100% 50%',
          },
          '100%': {
            'background-position': '0% 50%',
          },
        },
        glowPulse: {
          '0%, 100%': {
            'filter': 'drop-shadow(0 0 8px rgba(6, 182, 212, 0.6))',
          },
          '50%': {
            'filter': 'drop-shadow(0 0 16px rgba(6, 182, 212, 0.9))',
          },
        },
        barGrow: {
          'from': {
            'height': '0',
          },
          'to': {
            'height': '170px',
          },
        },
        scalePulse: {
          '0%, 100%': {
            'transform': 'scale(1)',
          },
          '50%': {
            'transform': 'scale(1.05)',
          },
        },
        slideInLeft: {
          'from': {
            'opacity': '0',
            'transform': 'translateX(-40px)',
          },
          'to': {
            'opacity': '1',
            'transform': 'translateX(0)',
          },
        },
        slideInUp: {
          'from': {
            'opacity': '0',
            'transform': 'translateY(40px)',
          },
          'to': {
            'opacity': '1',
            'transform': 'translateY(0)',
          },
        },
      },
    },
  },
  plugins: [],
};
