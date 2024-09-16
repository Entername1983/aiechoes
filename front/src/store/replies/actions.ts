import { createAsyncThunk } from "@reduxjs/toolkit";

import { RepliesService } from "../../client/services/RepliesService";

interface IRepliesData {
  batch_offset: number;
  qty_batches: number;
}

export const fetchReplies = createAsyncThunk(
  "replies/fetchReplies",
  async ({ data }: { data: IRepliesData }) => {
    const res = await RepliesService.getReplies(
      data.batch_offset,
      data.qty_batches
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
