import { ArrowDownIcon, ArrowUpIcon } from "@heroicons/react/16/solid";
import { AnimatePresence, motion } from "framer-motion";
import React from "react";

import type { RepliesSchema } from "../../client";
import { ReplyBatch } from "./ReplyBatch";

interface StoryBoxProps {
  batches: RepliesSchema[][];

  actionHandlers: {
    loadOnceUponATime: () => Promise<void>;
    loadTheStorySoFar: () => Promise<void>;
    loadPreviousBatches: () => Promise<void>;
    loadNextBatches: () => Promise<void>;
  };
  hasMore: {
    next: boolean;
    prev: boolean;
  };
  dummyRef: React.RefObject<HTMLDivElement>;
}
const StoryBox: React.FC<StoryBoxProps> = ({
  batches,
  actionHandlers,
  hasMore,
  dummyRef,
}) => {
  return (
    <div className="  flex justify-center md:w-[90vw]  md:gap-4 md:p-2 ">
      <div className="relative  z-10 overflow-hidden rounded-2xl p-2 md:w-[85vw]">
        <div className="max-h-[75vh] overflow-y-auto rounded-2xl px-1  md:px-2">
          <AnimatePresence>
            {batches.map((batch, index) => (
              <motion.div
                initial={{ opacity: 0, y: 0 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 100 }}
                transition={{
                  delay: 0.1,
                  ease: "easeOut",
                }}
                key={index}
                className=" px-2"
              >
                <div className=" py-2">
                  <ReplyBatch batch={batch} />
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={dummyRef}></div>
        </div>
        <div className="pointer-events-none absolute inset-x-0 top-0 z-10 h-12">
          <div className="size-full bg-gradient-to-b from-offBlack to-transparent"></div>
        </div>
        <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-12">
          <div className="size-full bg-gradient-to-t from-offBlack to-transparent"></div>
        </div>
      </div>

      <div className=" flex flex-col justify-between py-4">
        <button
          onClick={actionHandlers.loadPreviousBatches}
          disabled={!hasMore.prev}
        >
          <ArrowUpIcon
            className={`size-6 fill-paynesGray hover:fill-lightblue  md:size-8  ${
              !hasMore.prev
                ? "hidden cursor-not-allowed"
                : "cursor-pointer fill-paynesGray "
            }`}
          />
        </button>
        <button
          onClick={actionHandlers.loadNextBatches}
          disabled={!hasMore.next}
        >
          <ArrowDownIcon
            className={`size-6 fill-paynesGray hover:fill-lightblue  md:size-8  ${
              !hasMore.next
                ? "hidden cursor-not-allowed"
                : "cursor-pointer fill-paynesGray "
            }`}
          />
        </button>
      </div>
    </div>
  );
};

export { StoryBox };
