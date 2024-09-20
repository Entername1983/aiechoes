from app.config.db import Base
from app.models.images import Images
from app.models.replies import Replies
from app.models.stories import Stories
from app.models.story_context import StoryContexts

print("Base", Base.metadata)
print("Images", Images.__table__)
print("Replies", Replies.__table__)
print("Stories", Stories.__table__)
print("Story_contexts", StoryContexts.__table__)
