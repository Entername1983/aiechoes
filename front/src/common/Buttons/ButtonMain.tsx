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
      className={`rounded-xl  border-2 border-lightblue bg-charcoal px-4 py-2 text-center text-xl hover:bg-paynesGray hover:text-ghostWhite
        
        ${
          disabled
            ? "cursor-not-allowed border-lightblue/20 bg-charcoal text-lightblue/20"
            : "cursor-pointer  border-lightblue text-lightblue"
        }`}
      disabled={disabled}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export { ButtonMain };
