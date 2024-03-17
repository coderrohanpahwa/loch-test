import os
from dotenv import load_dotenv
load_dotenv()
DEBUG=True
PORT=5000

SQLALCHEMY_DATABASE_URI="sqlite:///loch.db"

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')

SHIFT_START_TIME="10:00"
SHIFT_END_TIME="19:00"

SLOT_BOOK_TIME=30