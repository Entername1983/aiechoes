// import ClozeCardIcon from '../assets/cardTypeIcons/CardTypeCloze.svg?react'
import Claude from "@assets/Claude.svg?react";
import Gemini from "@assets/Gemini.svg?react";
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
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  return (
    <div
      className="relative flex cursor-pointer justify-between rounded-xl bg-ghostWhite/90 px-2 py-1 hover:bg-ghostWhite "
      onClick={() => {
        setIsOpen(true);
      }}
    >
      <div className="flex  gap-2">
        <p className="text-lg">{reply.reply}</p>
      </div>
      <InfoModal isOpen={isOpen} setIsOpen={setIsOpen} reply={reply} />
    </div>
  );
};

export { SingleReply };
