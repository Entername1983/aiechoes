import SampleStoryImage from "@assets/SampleStoryImage.png";
import React from "react";

import type { RepliesSchema } from "../../client";
import { SingleReply } from "./SingleReply";
interface ReplyBatchProps {
  batch: RepliesSchema[];
}

const ReplyBatch: React.FC<ReplyBatchProps> = ({ batch }) => {
  const reversed = batch[0].batchId % 2 === 0;
  const reversedBatch = [...batch].reverse();

  const batchFull = batch.length === 5;
  return (
    <div
      className={`flex gap-4 ${
        reversed ? "flex-col md:flex-row-reverse" : "flex-col  md:flex-row"
      } `}
    >
      <div className=" flex items-center  justify-center rounded-xl bg-paynesGray p-2">
        <img src={SampleStoryImage} alt="up" />
      </div>
      <div
        className={`flex flex-1 flex-col rounded-xl bg-paynesGray p-2 ${
          batchFull ? "" : "justify-start"
        }`}
      >
        {reversedBatch.map((reply, index) => (
          <div className={`p-1 ${batchFull ? "grow" : ""}`} key={index}>
            <SingleReply reply={reply} />
          </div>
        ))}
      </div>
    </div>
  );
};

export { ReplyBatch };
