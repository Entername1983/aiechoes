import { ButtonMain } from "@source/common/Buttons/ButtonMain";
import React, { useEffect, useState } from "react";

import type { RepliesSchema } from "../../client";
import { Spinner } from "../../common/Spinner";
import { clearAllReplies, fetchReplies } from "../../store/replies/actions";
import { selectAllReplies } from "../../store/replies/repliesSlice";
import { useAppDispatch, useAppSelector } from "../../store/store";
import { StoryBox } from "./StoryBox";

// load in batches, need to seperate batches
// if we click top, load the 2 previous batches
// if we click to the beginning, load 2 first batches
// if we click bottom, load 2 next batches
// bottom button disabled if no more batches to load
// top button disabled if at the start of story

const Home: React.FC = () => {
  const [repliesLoaded, setRepliesLoaded] = useState<boolean>(false);
  const [batchOffset, setBatchOffset] = useState<number>(0);
  const dispatch = useAppDispatch();
  const allReplies = useAppSelector(selectAllReplies);
  const [highestBatchId, setHighestBatchId] = useState<number>(0);
  const [lowestBatchId, setLowestBatchId] = useState<number>(0);
  const [batches, setBatches] = useState<RepliesSchema[][]>([]);
  const [loadPreviousIsDisabled, setLoadPreviousIsDisabled] =
    useState<boolean>(false);
  const [loadNextIsDisabled, setLoadNextIsDisabled] = useState<boolean>(true);
  const dummyRef = React.useRef<HTMLDivElement>(null);
  const [scrollIntoView, setScrollIntoView] = useState<boolean>(false);
  const [title, setTitle] = useState<string>("The story so far...");

  useEffect(() => {
    if (batchOffset * 2 > highestBatchId + 1) {
      setLoadPreviousIsDisabled(true);
    }
    if (batchOffset < 0) {
      setLoadNextIsDisabled(true);
    }
  }, [batchOffset, highestBatchId]);

  const loadOnceUponATime = async (): Promise<void> => {
    void dispatch(clearAllReplies());
    setBatchOffset(Math.ceil(highestBatchId / 2) + 1);
    setRepliesLoaded(false);
    setLoadNextIsDisabled(false);
    setLoadPreviousIsDisabled(true);
    setTitle("Once upon a time...");
  };

  const loadTheStorySoFar = async (): Promise<void> => {
    void dispatch(clearAllReplies());
    setBatchOffset(0);
    setRepliesLoaded(false);
    setLoadPreviousIsDisabled(false);
    setLoadNextIsDisabled(true);
    setTitle("The story so far...");
  };

  const loadPreviousBatches = async (): Promise<void> => {
    setRepliesLoaded(false);
    setBatchOffset((prevOffset) => prevOffset + 2);
  };

  const loadNextBatches = async (): Promise<void> => {
    setRepliesLoaded(false);
    setBatchOffset((prevOffset) => prevOffset - 2);
    setScrollIntoView(true);
  };

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
      }, 1);
    }
  }, [allReplies, scrollIntoView]);

  useEffect(() => {
    if (!repliesLoaded) {
      void dispatch(
        fetchReplies({
          data: { batch_offset: batchOffset, qty_batches: 2 },
        })
      );
    }
    setRepliesLoaded(true);
  }, [batchOffset, dispatch, repliesLoaded]);

  useEffect(() => {
    const turnRepliesIntoBatchesUsingTheirBatchId = (): void => {
      const batches: RepliesSchema[][] = [];
      let highestBatchIdNumber = 0;
      let lowestBatchIdNumber = Infinity;
      allReplies.forEach((reply) => {
        if (batches[reply.batchId] !== undefined) {
          batches[reply.batchId].push(reply);
        } else {
          batches[reply.batchId] = [reply];
          if (reply.batchId > highestBatchIdNumber) {
            highestBatchIdNumber = reply.batchId;
          }
          if (reply.batchId < lowestBatchIdNumber) {
            lowestBatchIdNumber = reply.batchId;
          }
        }
      });
      setLowestBatchId(lowestBatchIdNumber);
      setHighestBatchId(highestBatchIdNumber);
      setBatches(batches);
    };
    turnRepliesIntoBatchesUsingTheirBatchId();
    setRepliesLoaded(true);
  }, [allReplies]);

  return (
    <div className=" ">
      <div className="px-4 py-2">
        <div className="flex justify-between pr-2">
          <h1 className="pl-10 pt-4 text-3xl text-ghostWhite">{title}</h1>
          <div className="flex flex-col gap-2 md:flex">
            {" "}
            <ButtonMain
              disabled={loadPreviousIsDisabled}
              onClick={loadOnceUponATime}
              text="Once upon a time..."
            />
            <ButtonMain
              disabled={loadNextIsDisabled}
              onClick={loadTheStorySoFar}
              text="The story so far..."
            />
          </div>
        </div>
        <div className="flex items-center justify-center ">
          {!repliesLoaded ? (
            <Spinner />
          ) : (
            <StoryBox
              loadPreviousBatches={loadPreviousBatches}
              loadNextBatches={loadNextBatches}
              loadPreviousIsDisabled={loadPreviousIsDisabled}
              loadNextIsDisabled={loadNextIsDisabled}
              batches={batches}
              dummyRef={dummyRef}
            />
          )}
        </div>
        <div className="flex justify-end pr-2"></div>
      </div>
    </div>
  );
};

export { Home };
