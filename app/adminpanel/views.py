from sqladmin import ModelView

from app.models.models import BookingModel, HotelModel, RoomModel, UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.email] + [UserModel.bookings]
    column_details_exclude_list = [UserModel.hashed_password]
    can_delete = False
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-user'


class BookingAdmin(ModelView, model=BookingModel):
    column_list = [c.name for c in BookingModel.__table__.c] + [BookingModel.user]
    name = 'Booking'
    name_plural = 'Bookings'
    icon = 'fa-solid fa-book'


class RoomAdmin(ModelView, model=RoomModel):
    column_list = [c.name for c in RoomModel.__table__.c] + [RoomModel.hotel, RoomModel.bookings]
    name = 'Room # '
    name_plural = 'Rooms'
    icon = 'fa-solid fa-bed'


class HotelAdmin(ModelView, model=HotelModel):
    column_list = [c.name for c in HotelModel.__table__.c] + [HotelModel.rooms]
    name = 'Hotel'
    name_plural = 'Hotels'
    icon = 'fa-solid fa-hotel'
