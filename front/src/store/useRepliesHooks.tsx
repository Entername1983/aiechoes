import type { RepliesSchema } from "@source/client/models/RepliesSchema";
import React, { useEffect, useState } from "react";

import {
  clearAllReplies,
  fetchReplies,
  setDirection,
  setStoryId,
} from "./replies/actions";
import {
  selectAllReplies,
  selectBatchesLoaded,
  selectDirection,
  selectHasMoreNext,
  selectHasMorePrev,
  selectStoryId,
} from "./replies/repliesSlice";
import { useAppDispatch, useAppSelector } from "./store";

interface useRepliesResponse {
  direction: "latest" | "earliest";
  allReplies: RepliesSchema[];
  actionHandlers: {
    loadOnceUponATime: () => Promise<void>;
    loadTheStorySoFar: () => Promise<void>;
    loadPreviousBatches: () => Promise<void>;
    loadNextBatches: () => Promise<void>;
  };
  updateStoryId: (storyId: number) => void;
  storyId: number | null;
  hasMore: {
    next: boolean;
    prev: boolean;
  };
  batches: RepliesSchema[][];
  title: string;
  dummyRef: React.RefObject<HTMLDivElement>;
}

const useReplies = (): useRepliesResponse => {
  const dispatch = useAppDispatch();
  const allReplies = useAppSelector(selectAllReplies);
  const [batchIdsToFetch, setBatchIdsToFetch] = useState<number[]>([]);
  const direction = useAppSelector(selectDirection);
  const storyId = useAppSelector(selectStoryId);
  const hasMorePrev = useAppSelector(selectHasMorePrev);
  const hasMoreNext = useAppSelector(selectHasMoreNext);
  const [batches, setBatches] = useState<RepliesSchema[][]>([]);
  const [title, setTitle] = useState<string>("The story so far...");
  const dummyRef = React.useRef<HTMLDivElement>(null);
  const [scrollIntoView, setScrollIntoView] = useState<boolean>(false);
  const batchesLoaded = useAppSelector(selectBatchesLoaded);

  useEffect(() => {
    if (storyId === null) return;
    void dispatch(
      fetchReplies({
        data: { storyId, order: direction, batchIds: batchIdsToFetch },
      })
    );
  }, [batchIdsToFetch, dispatch, direction, storyId]);

  const loadOnceUponATime = async (): Promise<void> => {
    setTitle("Once upon a time...");
    void dispatch(clearAllReplies());
    void dispatch(setDirection("earliest"));
  };

  const loadTheStorySoFar = async (): Promise<void> => {
    setTitle("The story so far...");
    void dispatch(clearAllReplies());
    void dispatch(setDirection("latest"));
  };

  const loadPreviousBatches = async (): Promise<void> => {
    setBatchIdsToFetch(() => {
      return [Math.min(...batchesLoaded) - 1, Math.min(...batchesLoaded) - 2];
    });
  };
  const loadNextBatches = async (): Promise<void> => {
    setBatchIdsToFetch(() => {
      return [Math.max(...batchesLoaded) + 1, Math.max(...batchesLoaded) + 2];
    });
    setScrollIntoView(true);
  };

  const updateStoryId = (storyId: number): void => {
    void dispatch(setStoryId(storyId));
  };

  const actionHandlers = {
    loadOnceUponATime,
    loadTheStorySoFar,
    loadPreviousBatches,
    loadNextBatches,
  };

  const hasMore = {
    next: hasMoreNext,
    prev: hasMorePrev,
  };

  useEffect(() => {
    const turnRepliesIntoBatchesUsingTheirBatchId = (): void => {
      const batches: RepliesSchema[][] = [];
      allReplies.forEach((reply) => {
        if (batches[reply.batchId] !== undefined) {
          batches[reply.batchId].push(reply);
        } else {
          batches[reply.batchId] = [reply];
        }
      });
      setBatches(batches);
    };
    turnRepliesIntoBatchesUsingTheirBatchId();
  }, [allReplies]);

  useEffect(() => {
    if (scrollIntoView) {
      setTimeout(() => {
        if (dummyRef.current !== null) {
          dummyRef.current.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
          });
        }
        setScrollIntoView(false);
      }, 100);
    }
  }, [allReplies, scrollIntoView]);

  return {
    direction,
    allReplies,
    actionHandlers,
    updateStoryId,
    storyId,
    hasMore,
    batches,
    title,
    dummyRef,
  };
};

export { useReplies };
