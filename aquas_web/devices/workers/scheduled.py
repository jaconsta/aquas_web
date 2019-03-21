from apscheduler.schedulers.background import BlockingScheduler
from devices.workers.django_setup import django_setup


def run_schedule_sprinkles():
    from devices.services.run_scheduled import run_scheduled_sprinkle

    scheduler = BlockingScheduler()
    scheduler.add_job(run_scheduled_sprinkle, 'interval', minutes=5)
    scheduler.start()


def run_workers():
    run_schedule_sprinkles()


if __name__ == '__main__':
    django_setup()
    run_workers()
