from apscheduler.schedulers.background import BackgroundScheduler

from .services.run_scheduled import run_scheduled_sprinkle


def run_schedule_sprinkles():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scheduled_sprinkle, 'interval', minutes=5)
    scheduler.start()


def run_workers():
    run_schedule_sprinkles()
