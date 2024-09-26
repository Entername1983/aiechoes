import type { RepliesSchema } from "@source/client/models/RepliesSchema";
import { StoriesService } from "@source/client/services/StoriesService";
import type { IDropdownItems } from "@source/common/Dropdown";
import React, { useCallback, useEffect, useState } from "react";

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
  storyId: number | null;
  hasMore: {
    next: boolean;
    prev: boolean;
  };
  batches: RepliesSchema[][];
  title: string;
  dummyRef: React.RefObject<HTMLDivElement>;
  storiesList: IDropdownItems[];
  storyTitle: string;
  dropdownChange: (value: { id: number; label: string }) => void;
}

const useReplies = (): useRepliesResponse => {
  const dispatch = useAppDispatch();
  const allReplies = useAppSelector(selectAllReplies);
  const [storyTitle, setStoryTitle] = useState<string>("Story 1");
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
  const [storiesList, setStoriesList] = useState<IDropdownItems[]>([]);

  useEffect(() => {
    if (storyId === null) {
      void dispatch(setStoryId(1));
      return;
    }
    void dispatch(
      fetchReplies({
        data: { storyId, order: direction, batchIds: batchIdsToFetch },
      })
    );
  }, [batchIdsToFetch, dispatch, direction, storyId]);

  useEffect(() => {
    const fetchStoriesList = async (): Promise<void> => {
      const res = await StoriesService.getListAllStories();
      const stories = res.storiesList.map((story) => {
        return {
          label: story.title,
          id: story.id,
        };
      });
      setStoriesList(stories);
    };
    if (storiesList.length === 0) {
      void fetchStoriesList();
    }
  }, [dispatch, storiesList, storyId]);

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
  const updateStoryId = useCallback(
    (storyId: number): void => {
      console.log("IN UPDATE STORY ID CALLBACK");
      void dispatch(setStoryId(storyId));
      setStoryTitle(
        storiesList.find((story) => story.id === storyId)?.label ?? ""
      );
    },
    [dispatch, storiesList]
  );
  // useEffect(() => {
  //   if (storyId != null) updateStoryId(storyId);
  //   if (storyId === null) {
  //     updateStoryId(1);
  //   }
  // }, [storyId, dispatch, storiesList, updateStoryId]);

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
  const dropdownChange = (value: { id: number; label: string }) => {
    console.log("VALLUE", value);
    console.log("Dropdown Change", value);
    console.log("Dropdown Change ID", value.id);
    updateStoryId(value.id);
  };
  return {
    direction,
    allReplies,
    actionHandlers,
    storyId,
    hasMore,
    batches,
    storyTitle,
    title,
    dummyRef,
    storiesList,
    dropdownChange,
  };
};

export { useReplies };
