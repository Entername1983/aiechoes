import React from "react";
import AiStorytellersLightBlue64 from "@assets/AiStorytellersLightBlue64.png";

const Navbar: React.FC = ({}) => {
  return (
    <div className="bg-ghostWhite  flex justify-between w-full h-20 px-4">
      <div className="flex justify-center items-center gap-4">
        <img src={AiStorytellersLightBlue64} alt="aistorytellers" />
        <h1 className="text-2xl font-bold">AI Storytellers</h1>
      </div>
      <div className="flex items-center justify-center gap-4 text-2xl">
        <button className="hover:text-paynesGray">About</button>
        <button className="hover:text-paynesGray">Contact</button>
      </div>
    </div>
  );
};

export { Navbar };
