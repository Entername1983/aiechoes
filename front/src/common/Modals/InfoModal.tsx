import ThumbsDown from "@assets/icons/Thumbsdown.svg?react";
import ThumbsUp from "@assets/icons/Thumbsup.svg?react";
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
      <div className={" p-[20px]"}>
        <h1 className="text-start text-2xl">
          {reply.model.charAt(0).toUpperCase() + reply.model.slice(1)}
        </h1>
        <div className="flex gap-2">
          <div className="rounded-xl border-2 border-paynesGray/50 p-2">
            <p>v: {reply.version} </p>
          </div>
          <div className="flex flex-col items-center justify-center ">
            <Icon className="size-20" />
            <div className=" bottom-0 right-0 flex items-center justify-center gap-1  p-1">
              <ThumbsDown className="size-6 cursor-pointer stroke-paynesGray hover:stroke-lightblue" />
              <ThumbsUp className="size-6 cursor-pointer  stroke-paynesGray hover:stroke-lightblue" />
            </div>
          </div>
        </div>
      </div>
    </ModalWrapper>
  );
};

export { InfoModal };
