import codecs
import csv
from typing import Literal

from fastapi import APIRouter, Depends, UploadFile, status

from app.exceptions import CannotAddDataToDatabase, CannotProcessCSV

from .utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format
from ..user.dependencies import get_current_user

router = APIRouter(
    prefix='/import',
    tags=['import']
)


@router.post(
    '/{table_name}',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def import_data_to_table(
        file: UploadFile,
        table_name: Literal['hotels', 'rooms', 'bookings', 'users']
):
    """Import test_data to db."""
    ModelService = TABLE_MODEL_MAP[table_name]
    csvreader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'), delimiter=';'
    )
    data = convert_csv_to_postgres_format(csvreader)
    file.file.close()
    if not data:
        raise CannotProcessCSV
    added_data = await ModelService.add_objects(data)
    if not added_data:
        raise CannotAddDataToDatabase
    return 'Success.'
