import { About } from "@source/pages/About";
import { Contact } from "@source/pages/Contact";
import { type ReactElement, useEffect } from "react";
import React from "react";
import { Route, Routes, useLocation } from "react-router-dom";

import { Layout } from "../common/layouts/Layout";
import { Home } from "../pages/Home";

const usePageTitle = (): void => {
  const defaultTitle = "AIEchoes";

  const location = useLocation();
  useEffect(() => {
    const pageTitleMap: Record<string, string> = {
      // Add index signature
      "/": "AIEchoes",
    };

    document.title = pageTitleMap[location.pathname] ?? defaultTitle;
  }, [location]);
};

const PublicRoutePaths = [
  {
    path: "/",
    element: (
      <Layout>
        <Home />
      </Layout>
    ),
  },
  {
    path: "/about",
    element: (
      <Layout>
        <About />
      </Layout>
    ),
  },
  {
    path: "/contact",
    element: (
      <Layout>
        <Contact />
      </Layout>
    ),
  },
];

const AppRoutes = (): ReactElement => {
  usePageTitle();
  return (
    <Routes>
      {PublicRoutePaths.map((route) => (
        <Route key={route.path} path={route.path} element={route.element} />
      ))}
    </Routes>
  );
};

export { AppRoutes };
