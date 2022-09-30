from reminder_bot import ReminderBot
from datetime import datetime
import logging

now = datetime.now()
current_time = now.strftime("%D,  %H:%M:%S")

f = open("file.log", "a")
f.write(f"Executed file on: {current_time}, ")
f.close()
rb = ReminderBot()
rb.start_bot()
