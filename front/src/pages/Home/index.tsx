import React, { useEffect, useState } from "react";
import { RepliesSchema, RepliesService } from "../../client";
import { StoryBox } from "./StoryBox";

interface HomeProps {}
const Home: React.FC<HomeProps> = () => {
  const [replies, setReplies] = useState<RepliesSchema[]>([]);
  const [repliesLoaded, setRepliesLoaded] = useState<boolean>(false);
  const [pagesLoaded, setPagesLoaded] = useState<number>(1);

  const fetchReplies = async () => {
    const res = await RepliesService.getReplies();
    setReplies(res.repliesList);
    setRepliesLoaded(true);
  };

  const loadMore = async () => {
    const res = await RepliesService.getReplies(pagesLoaded + 1);
    setReplies([...replies, ...res.repliesList]);
    setRepliesLoaded(true);
  };

  useEffect(() => {
    if (repliesLoaded === false) {
      fetchReplies();
    }
  }, []);

  return (
    <>
      <div className="bg-blue-500">
        <div className="text-red-500 text-6xl">Home</div>
        <button onClick={loadMore}>Load More</button>
        {!repliesLoaded ? (
          <div>Loading...</div>
        ) : (
          <StoryBox replies={replies} />
        )}
      </div>
    </>
  );
};

export { Home };
