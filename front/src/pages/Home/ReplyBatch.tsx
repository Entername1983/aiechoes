import React from "react";
import { RepliesSchema } from "../../client";
import { SingleReply } from "./SingleReply";
import SampleStoryImage from "@assets/SampleStoryImage.png";
interface ReplyBatchProps {
  batch: RepliesSchema[];
}

const ReplyBatch: React.FC<ReplyBatchProps> = ({ batch }) => {
  const reversed = batch[0].batchId % 2 === 0;
  const reversedBatch = [...batch].reverse();
  return (
    <div
      className={`flex gap-4 ${
        reversed ? "md:flex-row-reverse flex-col" : "   flex-col  md:flex-row"
      } `}
    >
      <div className=" bg-paynesGray rounded-xl  p-2 items-center justify-center flex">
        <img src={SampleStoryImage} alt="up" />
      </div>
      <div className={`flex bg-paynesGray p-2 rounded-xl  flex-col flex-1`}>
        {reversedBatch.map((reply, index) => (
          <div className="p-1 flex-1" key={index}>
            <SingleReply reply={reply} />
          </div>
        ))}
      </div>
    </div>
  );
};

export { ReplyBatch };
