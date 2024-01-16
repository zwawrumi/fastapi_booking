import json
from datetime import datetime
from typing import Iterable

from app.hotels.service import HotelService, RoomService, BaseService
from app.logger import logger
from app.user.service import UserService

TABLE_MODEL_MAP = {
    'hotels': HotelService,
    'rooms': RoomService,
    'bookings': BaseService,
    'users': UserService
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    """CSV to POSTGRESQL."""
    try:
        data = []
        for row in csv_iterable:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif key == 'services':
                    row[key] = json.loads(value.replace("'", '"'))
                elif 'date' in key:
                    row[key] = datetime.strptime(value, '%Y-%m-%d')
            data.append(row)
        return data
    except Exception as e:
        logger.error('Error converting CSV to PostgreSQL format', exc_info=True)
        raise e
