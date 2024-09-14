import React from "react";
import { Navbar } from "../Navbar";
import { Footer } from "../Footer";

interface LayoutProps {
  children: React.ReactNode;
}
const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className={` h-max min-h-screen  bg-offBlack`}>
      <Navbar />
      {children}
      <Footer />
    </div>
  );
};

export { Layout };
