from app.config.db import Base
from app.models.images import Images
from app.models.replies import Replies

print("Base", Base.metadata)
print("Images", Images.__table__)
print("Replies", Replies.__table__)
