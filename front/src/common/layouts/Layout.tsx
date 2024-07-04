import React from "react";

interface LayoutProps {
  children: React.ReactNode;
}
const Layout: React.FC<LayoutProps> = ({ children }) => {
  return <div className=" mx-auto p-4"> {children} </div>;
};

export { Layout };
