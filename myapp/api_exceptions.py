from rest_framework.exceptions import APIException
from rest_framework import status

# I wrote this code -------------------------- Start
class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'
    default_code = 'bad_request'

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not Found'
    default_code = 'not_found'

class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Conflict'
    default_code = 'conflict'
# I wrote this code -------------------------- End