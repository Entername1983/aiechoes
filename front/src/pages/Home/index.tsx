import { ButtonMain } from "@source/common/Buttons/ButtonMain";
import { useReplies } from "@source/store/useRepliesHooks";
import React, { useEffect } from "react";

import { Spinner } from "../../common/Spinner";
import { StoryBox } from "./StoryBox";

const Home: React.FC = () => {
  const {
    direction,
    allReplies,
    actionHandlers,
    updateStoryId,
    storyId,
    hasMore,
    batches,
    dummyRef,
    title,
  } = useReplies();

  useEffect(() => {
    if (storyId !== 1) updateStoryId(1);
  }, [storyId, updateStoryId]);

  return (
    <div className=" ">
      <div className="px-2 py-1 md:px-4 md:py-2">
        <div className="flex pr-2 md:justify-between">
          <h1 className="hidden pl-10 pt-4 text-3xl text-ghostWhite md:block">
            {title}
          </h1>
          <div className=" flex gap-2 ">
            {" "}
            <ButtonMain
              disabled={direction === "earliest"}
              onClick={actionHandlers.loadOnceUponATime}
              text="Once upon a time..."
            />
            <ButtonMain
              disabled={direction === "latest"}
              onClick={actionHandlers.loadTheStorySoFar}
              text="The story so far..."
            />
          </div>
        </div>
        <div className="flex items-center justify-center ">
          {allReplies.length === 0 ? (
            <Spinner />
          ) : (
            <StoryBox
              hasMore={hasMore}
              actionHandlers={actionHandlers}
              batches={batches}
              dummyRef={dummyRef}
            />
          )}
        </div>
        <div className="flex justify-end pr-2"></div>
      </div>
    </div>
  );
};

export { Home };
