## We use this file for re-exporting all sql models in app, otherwise creates issues

from app.config.db import Base
from app.models.images import Images
from app.models.replies import Replies
from app.models.stories import Stories
from app.models.story_context import StoryContexts

print("Base", Base.metadata)  # noqa: T201
print("Images", Images.__table__)  # noqa: T201
print("Replies", Replies.__table__)  # noqa: T201
print("Stories", Stories.__table__)  # noqa: T201
print("Story_contexts", StoryContexts.__table__)  # noqa: T201
