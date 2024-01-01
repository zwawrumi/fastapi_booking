from datetime import datetime

import pytest
from httpx import AsyncClient

from app.booking.service import BookingService


@pytest.mark.asyncio
async def test_add_and_get_booking(async_client: AsyncClient, prepare_db):
    response = await BookingService.add(
        room_id=7,
        user_id=2,
        date_from=datetime.strptime('2023-06-25', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-07-10', '%Y-%m-%d'),
    )

    assert response.user_id == 2

    new_booking = await BookingService.find_by_id(response.id)
    assert new_booking is not None

