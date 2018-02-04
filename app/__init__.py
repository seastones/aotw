from flask import Flask
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
import app.database as database

def sched_test():
    print("sched works")
    
sched = BackgroundScheduler(daemon=True)
sched.add_jobstore('redis',host=Config.redis_host,port=Config.redis_port)
#sched.add_job(database.set_current_album,'cron',day_of_week=0)
sched.add_job(database.set_current_album,'interval',seconds=90)
sched.start()

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
