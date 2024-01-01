from datetime import date
from enum import Enum
from typing import Optional

from sqlalchemy import (JSON, Column, Computed, Date, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PortalRole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_BOSS = "ROLE_BOSS"


class BookingModel(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    user: Mapped["UserModel"] = relationship(back_populates="bookings")
    room: Mapped["RoomModel"] = relationship(back_populates="bookings")

    def __str__(self):
        return f'Booking #{self.id}'


class RoomModel(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel: Mapped["HotelModel"] = relationship(back_populates="rooms")
    bookings: Mapped[list["BookingModel"]] = relationship(back_populates="room")

    def __str__(self):
        return f"№ {self.id}"


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    roles: Mapped[list[str]] = Column(ARRAY(String), nullable=False)

    bookings: Mapped[list["BookingModel"]] = relationship(back_populates="user")

    @property
    def is_boss(self) -> bool:
        return PortalRole.ROLE_BOSS in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_ADMIN in self.roles

    def add_admin_privilege(self):
        if not self.is_admin:
            return self.roles + [PortalRole.ROLE_ADMIN]

    def remove_admin_privilege(self):
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_ADMIN}

    def __str__(self):
        return f'User: {self.email}'


class HotelModel(Base):
    __tablename__ = "hotel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="hotel")

    def __str__(self):
        return f'Hotel {self.name} {self.location[:30]}'
