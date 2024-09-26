import { MenuButton } from "@headlessui/react";
import React from "react";

interface ButtonProps {
  title: string;
  onClick?: () => void;
}

const DropdownButtonItem: React.FC<ButtonProps> = ({ title, onClick }) => {
  return (
    <div>
      <MenuButton
        className=" cursor-pointer px-2 py-1 text-ghostWhite hover:text-lightblue"
        onClick={onClick}
      >
        {title}
      </MenuButton>
    </div>
  );
};

export { DropdownButtonItem };
