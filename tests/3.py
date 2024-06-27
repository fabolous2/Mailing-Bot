from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json

print(AsyncIOScheduler)
dict_sch = AsyncIOScheduler.__dict__
print(dict_sch.__init__)
# scheduler: AsyncIOScheduler = dict_sch['start']
# scheduler.print_jobs()