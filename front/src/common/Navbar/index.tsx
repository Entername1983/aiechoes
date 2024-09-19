import AiStorytellersLightBlue64 from "@assets/AiStorytellersLightBlue64.png";
import { Bars3Icon } from "@heroicons/react/16/solid";
import React from "react";
import { useNavigate } from "react-router";

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const [menuIsOpen, setMenuIsOpen] = React.useState(false);
  return (
    <div className="flex h-20 w-full justify-between bg-ghostWhite px-4">
      <div
        className="flex cursor-pointer items-center justify-center gap-4"
        onClick={() => {
          navigate("/");
        }}
      >
        <img
          className="size-12"
          src={AiStorytellersLightBlue64}
          alt="aistorytellers"
        />
        <h1 className="hidden font-bold md:block md:text-2xl ">
          AI Storytellers
        </h1>
      </div>
      <div className="flex items-center justify-center text-2xl">
        <div className="hidden md:block">
          <a href="/about" className="px-2 hover:text-paynesGray">
            About
          </a>
          <a href="/contact" className="px-2 hover:text-paynesGray">
            Contact
          </a>
        </div>
      </div>
      <div className="relative flex items-center justify-center md:hidden">
        <button
          className="size-8"
          onClick={() => {
            setMenuIsOpen(!menuIsOpen);
          }}
        >
          <Bars3Icon className="   fill-paynesGray hover:fill-lightblue" />
        </button>
        <div
          className={`transition-duration-500   absolute right-5 top-[60px] z-50 transition ease-in-out ${
            menuIsOpen ? "" : "hidden"
          }`}
        >
          <div className=" flex  flex-col rounded-md border border-ghostWhite bg-paynesGray py-2 text-xl text-ghostWhite">
            <div className="px-2 hover:bg-charcoal">
              <a href="/about" className="hover:text-paynesGray">
                About
              </a>
            </div>
            <div className="px-2 hover:bg-charcoal">
              <a href="/contact" className="hover:text-paynesGray">
                Contact
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export { Navbar };
