/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f8e8',
          100: '#e1f2d1',
          200: '#c3e5a4',
          300: '#a4d876',
          400: '#86cb49',
          500: '#4a7c59',
          600: '#2d5016',
          700: '#254012',
          800: '#1d300e',
          900: '#16200a',
        },
        secondary: {
          50: '#fef7e6',
          100: '#fdefcd',
          200: '#fbdf9b',
          300: '#f9cf69',
          400: '#f7bf37',
          500: '#daa520',
          600: '#ae841a',
          700: '#826313',
          800: '#56420d',
          900: '#2a2106',
        },
        earth: {
          50: '#f5f1ed',
          100: '#ebe3db',
          200: '#d7c7b7',
          300: '#c3ab93',
          400: '#af8f6f',
          500: '#8b4513',
          600: '#6f370f',
          700: '#53290b',
          800: '#371b08',
          900: '#1b0d04',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}