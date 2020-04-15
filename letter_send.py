#!/usr/bin/env python
from database import Database
database = Database()
database.connect()
database.send_out()
database.disconnect()
