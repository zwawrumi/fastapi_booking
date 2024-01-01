from fastapi import APIRouter, UploadFile
from PIL import Image

from app.tasks.tasks import process_img

router = APIRouter(prefix='/images', tags=['Upload images'])


@router.post('/hotels')
async def add_hotel_images(name: int, file: UploadFile):
    img_path = f'app/static/images/{name}.webp'
    with open(img_path, 'wb+') as file_object:
        image = Image.open(file.file)

        new_size = (300, 300)
        resized_image = image.resize(new_size)

        resized_image.save(file_object, 'WEBP')
    process_img.delay(img_path)
