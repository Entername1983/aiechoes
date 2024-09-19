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
    return res.repliesList;
  }
);

export const clearAllReplies = createAsyncThunk(
  "replies/clearAllReplies",
  async () => {
    return [];
  }
);
