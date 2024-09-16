import type { RepliesSchema } from "@source/client";
import { getIcon } from "@source/pages/Home/SingleReply";
import React from "react";

import { ModalWrapper } from "./ModalWrapper";

interface InfoModalProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  bgColor?: string;
  reply: RepliesSchema;
}

const InfoModal: React.FC<InfoModalProps> = ({
  isOpen,
  setIsOpen,
  bgColor,
  reply,
}) => {
  const Icon = getIcon(reply.model);
  return (
    <ModalWrapper isOpen={isOpen} setIsOpen={setIsOpen} bgColor={bgColor}>
      <div className={" p-[40px]"}>
        <h1 className="text-start text-2xl">
          {reply.model.charAt(0).toUpperCase() + reply.model.slice(1)}
        </h1>{" "}
        <div className="flex gap-2">
          <div className="rounded-xl border-2 border-paynesGray/50 p-2">
            <p>v: {reply.version} </p>
          </div>
          <Icon className="size-20" />
        </div>
      </div>
    </ModalWrapper>
  );
};

export { InfoModal };
