from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exist"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = 401
    detail = "Wrong password or Email"


class TokenExpireException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token doesn't exist"


class IncorrectTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token invalid"


class IncorrectRoleAdmin(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User is not admin"


class IncorrectRoleBoss(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User is not boss"


class RoomFullException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'No empty rooms'


class NotFoundException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Not found'


class UserNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User not found'


class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Cannot add test_db'


class CannotProcessCSV(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Cannot convert CSV'
