import { RepliesSchema } from "@source/client/models/RepliesSchema";
import React from "react";
// import ClozeCardIcon from '../assets/cardTypeIcons/CardTypeCloze.svg?react'

import Claude from "@assets/Claude.svg?react";
import Gemini from "@assets/Gemini.svg?react";
import Meta from "@assets/Meta.svg?react";
import Mistral from "@assets/Mistral.svg?react";
import OpenAi from "@assets/OpenAi.svg?react";
import ThumbsUp from "@assets/icons/Thumbsup.svg?react";
import ThumbsDown from "@assets/icons/Thumbsdown.svg?react";
function getIcon(model: string) {
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

  return (
    <div className="relative bg-ghostWhite px-2 py-1 rounded-xl flex justify-between">
      <div className="flex gap-2">
        <Icon className="h-8 w-8 cursor-pointer hover:scale-105 " />
        <p className="text-lg">
          {reply.id}
          {reply.reply}
        </p>
      </div>
      <div className=" bottom-0 right-0 flex gap-1 p-1  items-center">
        <ThumbsDown className="h-6 w-6 stroke-paynesGray hover:stroke-lightblue cursor-pointer" />
        <ThumbsUp className="h-6 w-6  stroke-paynesGray hover:stroke-lightblue cursor-pointer" />
      </div>
    </div>
  );
};

export { SingleReply };
