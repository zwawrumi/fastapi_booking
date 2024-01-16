import time
import sentry_sdk

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from app.logger import logger
from app.adminpanel.auth_admin import authentication_backend
from app.adminpanel.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.booking.router import router as booking_router
from app.database import engine
from app.hotels.rooms.router import router as room_router
from app.hotels.router import router as hotel_router
from app.images.router import router as image_router
from app.pages.router import router as pages_router
from app.user.router import router as user_router
from app.test_data.router import router as test_data_router
from config import settings

app = FastAPI()

sentry_sdk.init(
    dsn="https://23f5a81de2611de1357e8c787950d5a7@o4506490099924992.ingest.sentry.io/4506490104643584",
    enable_tracing=True,
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin.*', '/metrics'],
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin', 'Authorization'
    ],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info('Request execution time', extra={
        'process_time': round(process_time, 4)
    })
    return response


app.include_router(router=user_router)
app.include_router(router=booking_router)
app.include_router(router=room_router)
app.include_router(router=hotel_router)
app.include_router(router=pages_router)
app.include_router(router=image_router)
app.include_router(router=test_data_router)


@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


def startup_event():
    async def startup():
        #      async with lifespan():
        redis = aioredis.from_url(settings.CELERY_URL)
        FastAPICache.init(RedisBackend(redis), prefix="cache")

    return startup


app.add_event_handler("startup", startup_event())
