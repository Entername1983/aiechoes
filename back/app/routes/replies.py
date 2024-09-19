from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import desc, func, select

from app.dependencies.db import GetDb
from app.models.images import Images
from app.models.replies import Replies
from app.s3.storage_manager import StorageManager
from app.schemas.replies import PreSignedUrlResponse, RepliesResponse

replies_router = APIRouter()
NUMBER_OF_REPLIES_IN_2_BATCHES = 10


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


## get replies, params: story_id, latest or earliest, batch_ids,


@replies_router.get("/replies/{story_id}", response_model=RepliesResponse, tags=["replies"])
async def get_replies_for_story(
    db: GetDb,
    story_id: int,
    order: Optional[str] = Query(None, description="Order of replies: 'latest' or 'earliest'"),
    batch_ids: list[int] = Query(None, description="List of batch IDs"),
) -> dict:
    if batch_ids:
        return await return_batch_ids(db, story_id, batch_ids)
    if order == "latest":
        return await return_latest_replies(db, story_id)
    if order == "earliest":
        return await return_earliest_replies(db, story_id)

    raise HTTPException(status_code=400, detail="Invalid order parameter")


async def return_earliest_replies(db: GetDb, story_id: int) -> dict:
    query = (
        select(Replies)
        .filter(Replies.story_id == story_id)
        .order_by(Replies.time_created)
        .limit(10)
    )
    result = await db.execute(query)
    replies = result.scalars().all()
    return {
        "replies_list": [reply.to_dict() for reply in replies],
        "has_more_prev": False,
        "has_more_next": True,
    }


async def return_latest_replies(db: GetDb, story_id: int) -> dict:
    subquery = (
        select(Replies.batch_id)
        .filter(Replies.story_id == story_id)
        .group_by(Replies.batch_id)
        .order_by(desc(func.max(Replies.time_created)))
        .limit(2)
        .scalar_subquery()
    )
    query = (
        select(Replies)
        .filter(Replies.story_id == story_id, Replies.batch_id.in_(subquery))
        .order_by(desc(Replies.time_created))
    )
    result = await db.execute(query)
    replies = result.scalars().all()
    return {
        "replies_list": [reply.to_dict() for reply in replies],
        "has_more_prev": True,
        "has_more_next": False,
    }


async def return_batch_ids(db: GetDb, story_id: int, batch_ids: list[int]) -> dict:
    ## get replies for batch_ids
    query = (
        select(Replies).filter(Replies.story_id == story_id).filter(Replies.batch_id.in_(batch_ids))
    )
    result = await db.execute(query)
    replies = result.scalars().all()
    has_more_prev = True
    has_more_next = True
    if len(replies) < NUMBER_OF_REPLIES_IN_2_BATCHES:
        has_more_next = False
    if 0 in batch_ids:
        has_more_prev = False
    return {
        "replies_list": [reply.to_dict() for reply in replies],
        "has_more_prev": has_more_prev,
        "has_more_next": has_more_next,
    }


@replies_router.get("/image", response_model=PreSignedUrlResponse, tags=["image"])
async def get_image_for_batch(db: GetDb, batch_id: int) -> dict:
    image_entry = await get_db_entry_from_db(db, batch_id)
    if image_entry is None:
        raise HTTPException(status_code=404, detail="Image not found")
    pre_signed_url = await StorageManager.create_presigned_url(image_entry.image_url)
    return {"images_list": [{"id": batch_id, "url": pre_signed_url}]}


async def get_db_entry_from_db(db: GetDb, batch_id: int) -> Images:
    query = select(Images).filter(Images.batch_id == batch_id)
    result = await db.execute(query)
    return result.scalar()


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
