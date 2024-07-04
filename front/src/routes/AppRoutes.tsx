import { ReactElement, useEffect } from "react";
import { Layout } from "../common/layouts/Layout";
import { Route, Routes, useLocation } from "react-router-dom";
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
