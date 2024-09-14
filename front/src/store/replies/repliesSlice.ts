import {
  createEntityAdapter,
  createSlice,
  type EntityState,
} from "@reduxjs/toolkit";

import type { RepliesSchema } from "../../client/models/RepliesSchema";
import type { RootState } from "../store";
import { clearAllReplies, fetchReplies } from "./actions";

const repliesAdapter = createEntityAdapter<RepliesSchema>({
  sortComparer: (a: RepliesSchema, b: RepliesSchema) => b.id - a.id,
});

export interface RepliesSliceState extends EntityState<RepliesSchema, number> {
  repliesLoaded: number[];
  error: string | null;
  status: "idle" | "loading" | "failed" | "succeeded";
}

const initialState: RepliesSliceState = repliesAdapter.getInitialState({
  repliesLoaded: [],
  error: null,
  status: "idle",
});

const repliesSlice = createSlice({
  name: "replies",
  initialState,
  reducers: {},

  extraReducers: (builder) => {
    builder.addCase(fetchReplies.pending, (state) => {
      state.status = "loading";
    });
    builder.addCase(fetchReplies.fulfilled, (state, action) => {
      state.status = "succeeded";
      repliesAdapter.upsertMany(state, action.payload);
    });
    builder.addCase(fetchReplies.rejected, (state, action) => {
      state.status = "failed";
      state.error = action.error.message ?? "An error occurred.";
    });
    builder.addCase(clearAllReplies.fulfilled, (state) => {
      repliesAdapter.removeAll(state);
    });
  },
});

export default repliesSlice.reducer;

export const {
  selectAll: selectAllReplies,
  selectById: selectRepliesById,
  selectIds: selectRepliesIds,
} = repliesAdapter.getSelectors((state: RootState) => state.replies);
