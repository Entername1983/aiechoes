import { createAsyncThunk } from "@reduxjs/toolkit";
import { ImageService } from "@source/client";

interface IImagesData {
  story_id: number;
  batch_id: number;
}

export const fetchImageUrl = createAsyncThunk(
  "images/fetchImageUrl",
  async ({ data }: { data: IImagesData }) => {
    const res = await ImageService.getImageForBatch(
      data.story_id,
      data.batch_id
    );
    return res.imagesList;
  }
);
