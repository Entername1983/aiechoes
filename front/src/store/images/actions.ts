import { createAsyncThunk } from "@reduxjs/toolkit";
import { ImageService } from "@source/client";

interface IImagesData {
  batch_id: number;
}

export const fetchImageUrl = createAsyncThunk(
  "images/fetchImageUrl",
  async ({ data }: { data: IImagesData }) => {
    const res = await ImageService.getImageForBatch(data.batch_id);
    return res.imagesList;
  }
);
