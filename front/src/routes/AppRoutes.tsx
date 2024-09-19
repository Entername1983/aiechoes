import { About } from "@source/pages/About";
import { Contact } from "@source/pages/Contact";
import { type ReactElement, useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";

import { Layout } from "../common/layouts/Layout";
import { Home } from "../pages/Home";

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
  const usePageTitle = (): void => {
    const defaultTitle = "AI Story";

    const location = useLocation();
    useEffect(() => {
      const pageTitleMap: Record<string, string> = {
        "/": "Ai Story",
        "/about": "About - AI Story",
        "/contact": "Contact - AI Story",
        // Add more routes as needed
      };

      document.title = pageTitleMap[location.pathname] ?? defaultTitle;
    }, [location]);
  };

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
