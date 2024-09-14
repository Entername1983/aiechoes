import React from "react";

interface ButtonMainProps {
  onClick: () => void;
  disabled?: boolean;
  text: string;
  type?: "button" | "submit" | "reset";
}

const ButtonMain: React.FC<ButtonMainProps> = ({
  onClick,
  disabled = false,
  text,
  type = "button",
}) => {
  return (
    <button
      type={type}
      className={`bg-charcoal  border-[2px] border-lightblue rounded-xl py-2 px-4 text-xl text-center hover:bg-paynesGray hover:text-ghostWhite
        
        ${
          disabled
            ? "cursor-not-allowed bg-charcoal text-lightblue/20 border-lightblue/20"
            : "cursor-pointer  text-lightblue border-lightblue"
        }`}
      disabled={disabled}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export { ButtonMain };
