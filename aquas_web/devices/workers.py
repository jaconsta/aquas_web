from apscheduler.schedulers.background import BackgroundScheduler

from .services.sprinkle import water_now
from .models.device import Device


def run_watering():
    device = Device.objects.get(pk=1)
    water_now(device)


def run_schedule_sprinkles():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_watering, 'interval', minutes=5)
    scheduler.start()


def run_workers():
    run_schedule_sprinkles()