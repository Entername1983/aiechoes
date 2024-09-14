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
      colors: {
        charcoal: {
          DEFAULT: "#2F4550",
        },
        paynesGray: {
          DEFAULT: "#586F7C",
        },
        lightblue: {
          DEFAULT: "#B8DBD9",
        },
        ghostWhite: {
          DEFAULT: "#F4F4F9",
        },
        offBlack: {
          DEFAULT: "#1D1B20",
        },
        backgroundImage: {},
      },
      boxShadow: (theme) => ({
        "inner-custom": `inset 0 0 10px ${theme("colors.offBlack.DEFAULT")}`, // Using offBlack color
        "inner-charcoal-blur": `inset 0 0 30px ${theme(
          //box-shadow: [inset] <offset-x> <offset-y> <blur-radius> [<spread-radius>] <color>;
          "colors.charcoal.DEFAULT"
        )}`, // Corrected key name
      }),
      display: ["responsive"],
    },
  },
  plugins: [],
};
