import SampleStoryImage from "@assets/SampleStoryImage.png";
import { fetchImageUrl } from "@source/store/images/actions";
import { selectimagesById } from "@source/store/images/imagesSlice";
import {
  type RootState,
  useAppDispatch,
  useAppSelector,
} from "@source/store/store";
import React, { useEffect } from "react";

import type { RepliesSchema } from "../../client";
import { SingleReply } from "./SingleReply";
interface ReplyBatchProps {
  batch: RepliesSchema[];
}

const ReplyBatch: React.FC<ReplyBatchProps> = ({ batch }) => {
  const reversed = batch[0].batchId % 2 === 0;
  const reversedBatch = [...batch].reverse();
  const dispatch = useAppDispatch();
  const image = useAppSelector((state: RootState) =>
    selectimagesById(state, batch[0].batchId)
  );

  useEffect(() => {
    if (image == null) {
      void dispatch(fetchImageUrl({ data: { batch_id: batch[0].batchId } }));
    }
  }, [dispatch, image, batch]);

  const imageToUse = image != null ? image.url : SampleStoryImage;

  const batchFull = batch.length === 5;
  return (
    <div
      className={`flex gap-4 ${
        reversed ? "flex-col md:flex-row-reverse" : "flex-col  md:flex-row"
      } `}
    >
      <div className=" flex items-center  justify-center rounded-xl bg-paynesGray p-2">
        <img className="rounded-xl" src={imageToUse} alt="up" />
      </div>
      <div
        className={`flex flex-1 flex-col rounded-xl bg-paynesGray p-2 ${
          batchFull ? "" : "justify-start"
        }`}
      >
        {reversedBatch.map((reply, index) => (
          <div className={`p-1 ${batchFull ? "grow" : ""}`} key={index}>
            <SingleReply reply={reply} />
          </div>
        ))}
      </div>
    </div>
  );
};

export { ReplyBatch };
