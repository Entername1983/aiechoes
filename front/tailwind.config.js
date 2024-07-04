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
      display: ["responsive"], // Moved from inner extend to here
      colors: {
        "electric-violet": {
          DEFAULT: "#6019FF",
          200: "#BC8BFB",
          500: "#9F96FF",
          700: "#9747FF",
          900: "#4E26A5",
        },
        "blaze-orange": {
          DEFAULT: "#FF6E0B",
          100: "#FFBD66",
          900: "#D45400",
        },
        "mariana-blue": {
          DEFAULT: "#260078",
          100: "#3821AA",
        },
        tolopea: {
          DEFAULT: "#190042",
        },
        aquamarine: {
          DEFAULT: "#54FFF1",
          100: "#B0FFF8",
          900: "#5AE6DA",
        },
        shell: {
          DEFAULT: "#F2F2F2",
        },
        "black-white": {
          DEFAULT: "#FFFFFD",
        },
        "black-russian": {
          DEFAULT: "#13002A",
        },
      },
      dropShadow: {
        inputDropShadow: "0 1px 2px #0F172A0D",
        inputDropShadowFocus: ["0 1px 2px 0px #0F172A0D", "0 0 0 40px #E2E8F8"],
        "4xl": [
          "0 35px 35px rgba(0, 0, 0, 0.25)",
          "0 45px 65px rgba(0, 0, 0, 0.15)",
        ],
      },
      boxShadow: {
        iconBoxShadowAqua: " 0 0 0 2px #54FFF1",
      },
      backgroundImage: {
        "game-lobby": "url('/src/assets/GameLobbyBg.png')",
        playground: "url('/src/assets/PlaygroundBg.png')",
        confetti: "url('/src/assets/confeties.png')",
        "gradient-circle": "linear-gradient(180deg, #6019FF 0%, #4211B0 100%)",
      },
    },
  },
  plugins: [], // Moved outside of theme
};
