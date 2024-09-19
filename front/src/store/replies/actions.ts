import { createAsyncThunk } from "@reduxjs/toolkit";

import { RepliesService } from "../../client/services/RepliesService";

interface IRepliesData {
  storyId: number;
  order: "latest" | "earliest";
  batchIds: number[];
}

export const fetchReplies = createAsyncThunk(
  "replies/fetchReplies",
  async ({ data }: { data: IRepliesData }) => {
    const res = await RepliesService.getRepliesForStory(
      data.storyId,
      data.order,
      data.batchIds
    );
    return {
      replies: res.repliesList,
      hasMoreNext: res.hasMoreNext,
      hasMorePrev: res.hasMorePrev,
    };
  }
);


export const setDirection = createAsyncThunk(
  "replies/setDirection",
  async (direction: "latest" | "earliest") => {
    return direction;
  }
);
export const setStoryId = createAsyncThunk(
  "replies/setStoryId",
  async (storyId: number) => {
    return storyId;
  }
);

export const clearAllReplies = createAsyncThunk(
  "replies/clearAllReplies",
  async () => {
    return [];
  }
);
