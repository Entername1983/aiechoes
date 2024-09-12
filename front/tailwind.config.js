/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/pages/**/*.{js,jsx,ts,tsx}",
    "./src/routes/**/*.{js,jsx,ts,tsx}",

    "./src/common/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      display: ["responsive"], 
      colors: {
        charcoal: {
          DEFAULT: "2F4550",
        },
        paynesGray: {
          DEFAULT: "586F7C",
        },
        lightblue: {
          DEFAULT: "B8DBD9",
        },
        ghostWhite: {
          DEFAULT: "F4F4F9",
        },
        dropShadow: {
          inputDropShadow: "0 1px 2px #0F172A0D",
          inputDropShadowFocus: [
            "0 1px 2px 0px #0F172A0D",
            "0 0 0 40px #E2E8F8",
          ],
          "4xl": [
            "0 35px 35px rgba(0, 0, 0, 0.25)",
            "0 45px 65px rgba(0, 0, 0, 0.15)",
          ],
        },
        boxShadow: {},
        backgroundImage: {},
      },
    },
  },
  plugins: [], // Moved outside of theme
};
