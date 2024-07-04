const path = require("path");

module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  settings: {
    react: {
      version: "detect",
    },
    tailwindcss: {
      config: path.join(__dirname, "./tailwind.config.js"),
    },
  },
  extends: [
    "standard-with-typescript",
    "plugin:react/recommended",
    "plugin:tailwindcss/recommended",
    "plugin:react-hooks/recommended",
    "prettier",
  ],
  overrides: [
    {
      env: {
        browser: true,
      },
      files: [".eslintrc.{js,cjs}"],
      parserOptions: {
        sourceType: "script",
      },
    },
  ],
  parserOptions: {
    semi: ["error", "always"],
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react", "simple-import-sort", "eslint-plugin-tailwindcss"],

  rules: {
    "no-console": "warn",
    semi: ["error", "always"],
    "react/jsx-uses-react": "off",
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "simple-import-sort/imports": "error",
    "simple-import-sort/exports": "error",
    "import/newline-after-import": "error",
    "tailwindcss/classnames-order": "warn",
    "@typescript-eslint/no-misused-promises": "off",
  },
  ignorePatterns: ["src/client/*"],
};
