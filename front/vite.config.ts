import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { sentryVitePlugin } from "@sentry/vite-plugin";
import svgr from "vite-plugin-svgr";
import tailwindcss from "tailwindcss";
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    svgr({ include: "**/*.svg?react" }),
    sentryVitePlugin({
      org: "cephadex",
      project: "aiechoes",
    }),
  ],
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/*": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/openapi.json/, "/openapi.json"),
      },
    },
    watch: {
      usePolling: true,
    },
  },
  resolve: {
    alias: {
      "@source": path.resolve(__dirname, "src"),
      "@assets": path.resolve(__dirname, "src/assets"),
      "@pages": path.resolve(__dirname, "src/pages"),
      "@utils": path.resolve(__dirname, "src/lib/utils"),
      "@contexts": path.resolve(__dirname, "src/lib/contexts"),
      "@services": path.resolve(__dirname, "src/lib/services"),
      "@hooks": path.resolve(__dirname, "src/lib/hooks"),
      "@store": path.resolve(__dirname, "src/lib/store"),
      "@common": path.resolve(__dirname, "src/common"),
      "@customTypes": path.resolve(__dirname, "src/types"),
      "@routes": path.resolve(__dirname, "src/routes"),
      "@client": path.resolve(__dirname, "src/client"),
    },
  },

  build: {
    sourcemap: true,
  },
});
