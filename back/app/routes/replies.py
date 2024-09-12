from app.dependencies.db import GetDb
from app.models.replies import Replies
from app.schemas.replies import RepliesResponse
from fastapi import APIRouter
from sqlalchemy import desc, select

replies_router = APIRouter()


async def get_replies_from_db(
    db: GetDb, page: int = 1, items: int = 10
) -> list[Replies]:
    query = (
        select(Replies)
        .order_by(desc(Replies.time_created))
        .limit(items)
        .offset((page - 1) * items)
    )
    result = await db.execute(query)
    list_replies = result.scalars().all()
    return list(list_replies)


@replies_router.get("/replies", response_model=RepliesResponse, tags=["replies"])
async def get_replies(db: GetDb, page: int = 1, items: int = 10):
    replies = await get_replies_from_db(db, page, items)
    list_replies = []
    for reply in replies:
        list_replies.append(reply.to_dict())
    print(list_replies)
    return {"replies_list": list_replies}


# replies_router = APIRouter()


# async def retrieve_replies(db, page, items_per_page) -> list[Replies]:
#     async with db() as session:
#         stmt = (
#             select(Replies)
#             .order_by(desc(Replies.time_created))
#             .limit(items_per_page)
#             .offset((page - 1) * items_per_page)
#         )
#         result = await session.execute(stmt)
#         replies = result.scalars().all()
#         return replies


# @replies_router.get("/replies", response_model=RepliesResponse, tags=["replies"])
# async def get_all_replies(db: GetDb, page: int = 1, items_per_page: int = 12):
#     replies = await retrieve_replies(db, page, items_per_page)
#     replies_list = []
#     for reply in replies:
#         replies = reply.to_dict()
#         replies_list.append(RepliesSchema(reply.to_dict()))

#     return RepliesResponse(replies_list=replies_list)
