from datetime import date

from sqlalchemy import and_, between, delete, func, insert, or_, select

from app.database import async_session_maker, engine
from app.models.models import BookingModel, RoomModel
from app.service.base import BaseService


class BookingService(BaseService):
    model = BookingModel

    @classmethod
    async def find_free_by_id(cls, room_id, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = (
                select(func.count())
                .where(
                    and_(
                        cls.model.room_id == room_id,
                        cls.model.date_from < date_to,
                        cls.model.date_to > date_from,
                        or_(
                            between(date_to, cls.model.date_from, cls.model.date_to),
                            between(date_from, cls.model.date_from, cls.model.date_to),
                            between(cls.model.date_from, date_from, date_to),
                            between(cls.model.date_to, date_from, date_to),
                        ),
                    )
                )
                .scalar_subquery()
            )
            get_rooms_left = select(
                func.coalesce(RoomModel.quantity - booked_rooms, RoomModel.quantity)
            ).where(RoomModel.id == room_id)
            result = await session.execute(get_rooms_left)
            return result.scalar()

    @classmethod
    async def add(cls, user_id, room_id, date_from, date_to):
        rooms_left: int = await BookingService.find_free_by_id(
            room_id, date_from, date_to
        )
        async with async_session_maker() as session:
            if rooms_left > 0:
                get_price = select(RoomModel.price).filter_by(id=room_id)
                result = await session.execute(get_price)
                price: int = result.scalar()
                add_booking = (
                    insert(cls.model)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(cls.model)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete(cls, current_user, booking_id: int):
        async with async_session_maker() as session:
            delete_query = (
                delete(cls.model)
                .where(
                    and_(
                        cls.model.id == booking_id, cls.model.user_id == current_user.id
                    )
                )
                .returning(cls.model.id)
            )
            delete_booking = await session.execute(delete_query)
            await session.commit()
            return delete_booking.scalar()

    # @classmethod
    # async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
    #    async with async_session_maker() as session:
    #        booked_rooms = select(BookingModel).where(
    #            and_(
    #                BookingModel.room_id == room_id,
    #                or_(
    #                    and_(
    #                        BookingModel.date_from >= date_from,
    #                        BookingModel.date_from <= date_to
    #                    ),
    #                    and_(
    #                        BookingModel.date_from <= date_from,
    #                        BookingModel.date_to > date_from
    #                    )
    #                )
    #            )
    #        ).cte('booked_rooms')


#
#        get_room_left = select(
#            RoomModel.quantity - func.count(booked_rooms.c.room_id)
#        ).where(
#            and_(
#                RoomModel.id == room_id,
#                booked_rooms.c.room_id == RoomModel.id
#            )
#        ).group_by(
#            RoomModel.quantity, booked_rooms.c.room_id
#        )
#
#        print(get_room_left.compile(engine, compile_kwargs={'literal_binds': True}))
#        rooms_left = await session.execute(get_room_left)
#        rooms_left = rooms_left.scalar()
#
#        # if rooms_left is not None:
#        #     print(f'rooms_left: {rooms_left}')
#
#        get_price = select(RoomModel.price).filter_by(id=room_id)
#        price = await session.execute(get_price)
#        price = price.scalar()
#
#        add_booking = insert(BookingModel).values(
#            room_id=room_id,
#            user_id=user_id,
#            date_from=date_from,
#            date_to=date_to,
#            price=price,
#        ).returning(BookingModel)
#
#        new_booking = await session.execute(add_booking)
#        await session.commit()
#
#        return new_booking.scalar()
