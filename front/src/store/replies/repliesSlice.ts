import {
  createEntityAdapter,
  createSlice,
  type EntityState,
} from "@reduxjs/toolkit";

import type { RepliesSchema } from "../../client/models/RepliesSchema";
import type { RootState } from "../store";
import {
  clearAllReplies,
  fetchReplies,
  setDirection,
  setStoryId,
} from "./actions";

const repliesAdapter = createEntityAdapter<RepliesSchema>({
  sortComparer: (a: RepliesSchema, b: RepliesSchema) => b.id - a.id,
});

export interface RepliesSliceState extends EntityState<RepliesSchema, number> {
  repliesLoaded: number[];
  batchesLoaded: number[];
  error: string | null;
  status: "idle" | "loading" | "failed" | "succeeded";
  storyId: number | null;
  direction: "latest" | "earliest";
  hasMorePrev: boolean;
  hasMoreNext: boolean;
}

const addUniqueItems = <T>(existing: T[], newItems: T[]): T[] => {
  return Array.from(new Set([...existing, ...newItems]));
};

const initialState: RepliesSliceState = repliesAdapter.getInitialState({
  repliesLoaded: [],
  batchesLoaded: [],
  error: null,
  status: "idle",
  storyId: null,
  direction: "latest",
  hasMorePrev: true,
  hasMoreNext: false,
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
      state.hasMorePrev = action.payload.hasMorePrev;
      state.hasMoreNext = action.payload.hasMoreNext;
      const repliesToAdd = action.payload.replies.map((reply) => reply.batchId);
      state.batchesLoaded = addUniqueItems(state.batchesLoaded, repliesToAdd);
      const repliesLoadedToAdd = action.payload.replies.map(
        (reply) => reply.id
      );
      state.repliesLoaded = addUniqueItems(
        state.repliesLoaded,
        repliesLoadedToAdd
      );
      repliesAdapter.upsertMany(state, action.payload.replies);
    });
    builder.addCase(fetchReplies.rejected, (state, action) => {
      state.status = "failed";
      state.error = action.error.message ?? "An error occurred.";
    });
    builder.addCase(clearAllReplies.fulfilled, (state) => {
      repliesAdapter.removeAll(state);
      state.repliesLoaded = [];
      state.batchesLoaded = [];
    });
    builder.addCase(setDirection.fulfilled, (state, action) => {
      state.direction = action.payload;
    });
    builder.addCase(setStoryId.fulfilled, (state, action) => {
      state.storyId = action.payload;
    });
  },
});

export default repliesSlice.reducer;

export const {
  selectAll: selectAllReplies,
  selectById: selectRepliesById,
  selectIds: selectRepliesIds,
} = repliesAdapter.getSelectors((state: RootState) => state.replies);

export const selectRepliesLoaded = (state: RootState): number[] =>
  state.replies.repliesLoaded;
export const selectBatchesLoaded = (state: RootState): number[] =>
  state.replies.batchesLoaded;
export const selectRepliesStatus = (state: RootState): string =>
  state.replies.status;
export const selectStoryId = (state: RootState): number | null =>
  state.replies.storyId;
export const selectDirection = (state: RootState): "latest" | "earliest" =>
  state.replies.direction;
export const selectHasMorePrev = (state: RootState): boolean =>
  state.replies.hasMorePrev;
export const selectHasMoreNext = (state: RootState): boolean =>
  state.replies.hasMoreNext;
