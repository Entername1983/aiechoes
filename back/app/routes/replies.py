from fastapi import APIRouter
from sqlalchemy import desc, select

from app.dependencies.db import GetDb
from app.models.replies import Replies
from app.schemas.replies import RepliesResponse

replies_router = APIRouter()


async def get_replies_from_db(
    db: GetDb,
    page: int = 1,
    items: int = 10,
) -> list[Replies]:
    query = (
        select(Replies).order_by(desc(Replies.time_created)).limit(items).offset((page - 1) * items)
    )
    result = await db.execute(query)
    list_replies = result.scalars().all()
    return list(list_replies)


async def get_top_batch_ids_from_db(
    db: GetDb,
    qty_batches: int = 1,
) -> list[int]:
    query = select(Replies.batch_id).distinct().order_by(desc(Replies.batch_id)).limit(qty_batches)
    result = await db.execute(query)
    list_batch_ids = result.scalars().all()
    return list(list_batch_ids)


async def get_next_two_batches_of_replies_from_db(
    db: GetDb,
    batch_offset: int = 0,
    qty_batches: int = 2,
) -> list[Replies]:
    batch_ids = await get_top_batch_ids_from_db(db, qty_batches)
    offset_batch_ids = [batch_id - batch_offset for batch_id in batch_ids]
    query = (
        select(Replies)
        .filter(Replies.batch_id.in_(offset_batch_ids))
        .order_by(Replies.time_created)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


@replies_router.get("/replies", response_model=RepliesResponse, tags=["replies"])
async def get_replies(db: GetDb, batch_offset: int = 0, qty_batches: int = 2) -> dict:
    replies = await get_next_two_batches_of_replies_from_db(db, batch_offset, qty_batches)
    list_replies = [reply.to_dict() for reply in replies]
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
