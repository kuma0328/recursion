from enum import Enum
from sre_constants import SUCCESS
from xmlrpc.client import SERVER_ERROR

class Operation(Enum):
  CREATE_ROOM = 1
  JOIN_ROOM = 2

class State(Enum):
  INIT = 1
  ACKNOWLEDGED = 2
  COMPLETED = 3

class StatusCodes(Enum):
  SUCCESS = 200
  INVALID_ROOM_NAME = 400
  INVALID_TOKEN = 401
  ROOM_NOT_FOUND = 404
  SERVER_ERROR = 500

TCP_HEADER_SIZE = 32
MAX_ROOM_NAME_SIZE = 28
MAX_PAYLOAD_SIZE = 229
MAX_TOKEN_SIZE = 255
MAX_UDP_PACKET_SIZE = 4096

