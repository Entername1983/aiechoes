import React from "react";

const Contact: React.FC = () => {
  return (
    <div className="flex size-full items-center justify-center text-xl">
      <div className="max-w-[600px] p-4 text-ghostWhite">
        <div>
          <h1 className="text-4xl">Contact</h1>

          <a href="mailto:kevin@cephadex.com" className="hover:text-lightblue">
            drop me an email
          </a>
        </div>
      </div>
    </div>
  );
};

export { Contact };
