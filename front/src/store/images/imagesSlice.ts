import {
  createEntityAdapter,
  createSlice,
  type EntityState,
} from "@reduxjs/toolkit";
import type { SimpleImagesSchema } from "@source/client/models/SimpleImagesSchema";

import type { RootState } from "../store";
import { fetchImageUrl } from "./actions";

const imagesAdapter = createEntityAdapter<SimpleImagesSchema>({
  sortComparer: (a: SimpleImagesSchema, b: SimpleImagesSchema) => b.id - a.id,
});

export interface imagesSliceState
  extends EntityState<SimpleImagesSchema, number> {
  imagesLoaded: number[];
  error: string | null;
  status: "idle" | "loading" | "failed" | "succeeded";
}

const initialState: imagesSliceState = imagesAdapter.getInitialState({
  imagesLoaded: [],
  error: null,
  status: "idle",
});

const imagesSlice = createSlice({
  name: "images",
  initialState,
  reducers: {},

  extraReducers: (builder) => {
    builder.addCase(fetchImageUrl.fulfilled, (state, action) => {
      if (action.payload.length === 0) {
        state.status = "failed";
        state.error = "No images found";
        return;
      }
      const newImageUrl = action.payload[0];

      imagesAdapter.upsertOne(state, newImageUrl);
    });
  },
});

export default imagesSlice.reducer;

export const {
  selectAll: selectAllimages,
  selectById: selectimagesById,
  selectIds: selectimagesIds,
} = imagesAdapter.getSelectors((state: RootState) => state.images);
