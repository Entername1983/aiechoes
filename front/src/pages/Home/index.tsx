import React, { useEffect, useState } from "react";
import { RepliesSchema } from "../../client";
import { StoryBox } from "./StoryBox";
import { Spinner } from "../../common/Spinner";
import { selectAllReplies } from "../../store/replies/repliesSlice";
import { useAppDispatch, useAppSelector } from "../../store/store";
import { clearAllReplies, fetchReplies } from "../../store/replies/actions";
import { ButtonMain } from "@source/common/Buttons/ButtonMain";

// load in batches, need to seperate batches
// if we click top, load the 2 previous batches
// if we click to the beginning, load 2 first batches
// if we click bottom, load 2 next batches
// bottom button disabled if no more batches to load
// top button disabled if at the start of story

interface HomeProps {}
const Home: React.FC<HomeProps> = () => {
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

  useEffect(() => {
    if (batchOffset * 2 > highestBatchId + 1) {
      setLoadPreviousIsDisabled(true);
    }
  }, [batchOffset]);

  const loadOnceUponATime = async () => {
    dispatch(clearAllReplies());
    console.log("highestBatchId", highestBatchId);
    setBatchOffset(Math.ceil(highestBatchId / 2) + 1);
    setRepliesLoaded(false);
    setLoadNextIsDisabled(false);
  };

  const loadTheStorySoFar = async () => {
    dispatch(clearAllReplies());
    setBatchOffset(0);
    setRepliesLoaded(false);
    setLoadPreviousIsDisabled(false);
  };

  const loadPreviousBatches = async () => {
    setRepliesLoaded(false);
    setBatchOffset((prevOffset) => prevOffset + 2);
  };

  const loadNextBatches = async () => {
    setRepliesLoaded(false);
    setBatchOffset((prevOffset) => prevOffset - 2);
    setScrollIntoView(true);
  };

  useEffect(() => {
    console.log("in useEffect, scrollintoView", scrollIntoView);
    if (scrollIntoView) {
      setTimeout(() => {
        if (dummyRef.current) {
          dummyRef.current.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
          });
        }
        setScrollIntoView(false);
      }, 1);
    }
  }, [allReplies]);

  useEffect(() => {
    if (repliesLoaded === false) {
      dispatch(
        fetchReplies({
          data: { batch_offset: batchOffset, qty_batches: 2 },
        })
      );
    }
    setRepliesLoaded(true);
  }, [batchOffset]);

  useEffect(() => {
    const turnRepliesIntoBatchesUsingTheirBatchId = () => {
      const batches: RepliesSchema[][] = [];
      let highestBatchIdNumber = 0;
      let lowestBatchIdNumber = Infinity;
      allReplies.forEach((reply) => {
        if (batches[reply.batchId]) {
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
      <div className="p-4">
        <div className="flex justify-end pr-2">
          <ButtonMain
            disabled={loadPreviousIsDisabled}
            onClick={loadOnceUponATime}
            text="Once upon a time..."
          />
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
        <div className="flex justify-end pr-2">
          <ButtonMain
            disabled={loadNextIsDisabled}
            onClick={loadTheStorySoFar}
            text="The story so far..."
          />
        </div>
      </div>
    </div>
  );
};

export { Home };
