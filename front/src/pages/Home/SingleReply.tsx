// import ClozeCardIcon from '../assets/cardTypeIcons/CardTypeCloze.svg?react'
import Claude from "@assets/Claude.svg?react";
import Gemini from "@assets/Gemini.svg?react";
import ThumbsDown from "@assets/icons/Thumbsdown.svg?react";
import ThumbsUp from "@assets/icons/Thumbsup.svg?react";
import Meta from "@assets/Meta.svg?react";
import Mistral from "@assets/Mistral.svg?react";
import OpenAi from "@assets/OpenAi.svg?react";
import type { RepliesSchema } from "@source/client/models/RepliesSchema";
import { InfoModal } from "@source/common/Modals/InfoModal";
import React from "react";

export function getIcon(
  model: string
): React.FC<React.SVGProps<SVGSVGElement>> {
  switch (model) {
    case "claude":
      return Claude;
    case "gemini":
      return Gemini;
    case "llama":
      return Meta;
    case "mistral":
      return Mistral;
    case "gpt":
      return OpenAi;
    default:
      return Claude;
  }
}

interface SingleReplyProps {
  reply: RepliesSchema;
}

const SingleReply: React.FC<SingleReplyProps> = ({ reply }) => {
  const Icon = getIcon(reply.model);
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  return (
    <div className="relative flex justify-between rounded-xl bg-ghostWhite px-2 py-1">
      <div className="flex gap-2">
        <Icon
          className="size-8 cursor-pointer hover:scale-105 "
          onClick={() => {
            setIsOpen(true);
          }}
        />
        <p className="text-lg">
          {reply.id}
          {reply.reply}
        </p>
      </div>
      <div className=" bottom-0 right-0 flex items-center gap-1  p-1">
        <ThumbsDown className="size-6 cursor-pointer stroke-paynesGray hover:stroke-lightblue" />
        <ThumbsUp className="size-6 cursor-pointer  stroke-paynesGray hover:stroke-lightblue" />
      </div>
      <InfoModal
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        reply={reply}
        Icon={Icon}
      />
    </div>
  );
};

export { SingleReply };
