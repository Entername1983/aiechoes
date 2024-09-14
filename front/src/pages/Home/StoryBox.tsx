import React from "react";
import { RepliesSchema } from "../../client";
import { ReplyBatch } from "./ReplyBatch";
import { ArrowDownIcon, ArrowUpIcon } from "@heroicons/react/16/solid";

interface StoryBoxProps {
  batches: RepliesSchema[][];
  loadPreviousBatches: () => void;
  loadNextBatches: () => void;
  loadPreviousIsDisabled: boolean;
  loadNextIsDisabled: boolean;
  dummyRef: React.RefObject<HTMLDivElement>;
}
const StoryBox: React.FC<StoryBoxProps> = ({
  batches,
  loadPreviousBatches,
  loadNextBatches,
  loadPreviousIsDisabled,
  loadNextIsDisabled,
  dummyRef,
}) => {
  return (
    <div className="  flex gap-4  p-2  ">
      <div className="relative  p-2  z-10 rounded-2xl overflow-hidden">
        <div className="max-h-[80vh] overflow-y-auto rounded-2xl px-2 ">
          {batches.map((batch, index) => (
            <div className=" py-2" key={index}>
              <ReplyBatch batch={batch} />
            </div>
          ))}
          <div ref={dummyRef}></div>
        </div>
        <div className="absolute top-0 left-0 right-0 h-12 pointer-events-none z-10">
          <div className="w-full h-full bg-gradient-to-b from-offBlack to-transparent"></div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-12 pointer-events-none z-10">
          <div className="w-full h-full bg-gradient-to-t from-offBlack to-transparent"></div>
        </div>
      </div>

      <div className=" flex flex-col justify-between py-4">
        <button onClick={loadPreviousBatches} disabled={loadPreviousIsDisabled}>
          <ArrowUpIcon
            className={`h-8 w-8  hover:fill-lightblue fill-paynesGray  ${
              loadPreviousIsDisabled
                ? "cursor-not-allowed fill-charcoal"
                : "cursor-pointer fill-paynesGray "
            }`}
          />
        </button>
        <button onClick={loadNextBatches} disabled={loadNextIsDisabled}>
          <ArrowDownIcon
            className={`h-8 w-8  hover:fill-lightblue fill-paynesGray  ${
              loadNextIsDisabled
                ? "cursor-not-allowed fill-charcoal"
                : "cursor-pointer fill-paynesGray "
            }`}
          />
        </button>
      </div>
    </div>
  );
};

export { StoryBox };
