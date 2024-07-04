import React from "react";
import { RepliesSchema } from "../../client";

interface StoryBoxProps {
  replies: RepliesSchema[];
}
const StoryBox: React.FC<StoryBoxProps> = ({ replies }) => {
  return (
    <div className="p-2">
      {replies.map((reply) => (
        <div key={reply.id}>
          <div className="text-lg">{reply.reply}</div>
        </div>
      ))}
    </div>
  );
};

export { StoryBox };
