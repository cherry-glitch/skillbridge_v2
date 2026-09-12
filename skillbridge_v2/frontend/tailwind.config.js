/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#F3F5F7',
        surface: '#FFFFFF',
        ink: '#1A2233',
        line: '#DDE3EA',
        brand: '#1B5E4F',
        'brand-dark': '#144539',
        brandlight: '#E4F0EC',
        accent: '#C9622B',
      },
      fontFamily: {
        display: ['"Fraunces"', 'serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
