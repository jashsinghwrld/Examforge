/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary:   'var(--bg-primary)',
          secondary: 'var(--bg-secondary)',
          elevated:  'var(--bg-elevated)',
          card:      'var(--bg-card)',
          hover:     'var(--bg-hover)',
          border:    'var(--bg-border)',
        },
        text: {
          primary:   'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted:     'var(--text-muted)',
          accent:    'var(--accent-blue)',
        },
        accent: {
          blue:      'var(--accent-blue)',
          blueHover: 'var(--accent-blue-hover)',
          purple:    'var(--accent-purple)',
          cyan:      'var(--accent-cyan)',
          green:     'var(--accent-green)',
          yellow:    'var(--accent-yellow)',
          red:       'var(--accent-red)',
        },
      },
      fontFamily: {
        sans: ['DM Sans', 'system-ui', 'sans-serif'],
        serif: ['Fraunces', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        display: ['2.5rem', { lineHeight: '1.12', letterSpacing: '-0.03em', fontWeight: '600' }],
        heading: ['1.25rem', { lineHeight: '1.35', fontWeight: '600' }],
      },
      boxShadow: {
        card:       'var(--shadow-card)',
        'card-hover': 'var(--shadow-card-hover)',
        nav:        'var(--shadow-nav)',
      },
      animation: {
        'fade-in':    'fadeIn 0.35s ease-out',
        'slide-up':   'slideUp 0.45s cubic-bezier(0.22, 1, 0.36, 1)',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow':  'spin 2s linear infinite',
        shimmer:      'shimmer 1.4s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '200% 0' },
          '100%': { backgroundPosition: '-200% 0' },
        },
      },
    },
  },
  plugins: [],
}
