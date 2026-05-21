/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../*.html",
    "../services/*.html",
    "../projects/*.html",
  ],
  theme: {
    extend: {
      colors: {
        burgundy: {
          50: "#fbf1f1",
          100: "#f6dddd",
          200: "#ecb0b0",
          500: "#a32626",
          600: "#8a1e1e",
          700: "#7a1c1c",
          800: "#5a1414",
          900: "#3a0d0d",
        },
        gold: {
          300: "#e8c475",
          400: "#d9ae4e",
          500: "#c9983a",
          600: "#ad7f2a",
        },
        char: {
          950: "#0a0807",
          900: "#14110f",
          800: "#1f1b17",
          700: "#2b2620",
        },
        cream: "#f5efe2",
      },
      fontFamily: {
        display: ["Anton", "Impact", "sans-serif"],
        sport: ["Oswald", "sans-serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
