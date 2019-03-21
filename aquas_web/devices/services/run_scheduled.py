import datetime

from ..services.sprinkle import scheduled_sprinkle
from ..models import SprinkleSchedule

SPRINKLE_SCHEDULE_MIN = 5


def run_scheduled_sprinkle():
    """
    Default python datetime management is not enough considering timezones.

    A possible approach is to generate a list of the next scheduled events
    and modify SprinkleSchedule to store user's timezone.

    I will hard code a timezone right now.

    :return:
    """
    days = [
        'on_monday',
        'on_tuesday',
        'on_wednesday',
        'on_thursday',
        'on_friday',
        'on_saturday',
        'on_sunday'
    ]
    gmt_m_5 = datetime.timedelta(hours=-5)
    offset = datetime.timedelta(minutes=SPRINKLE_SCHEDULE_MIN*2)
    now = datetime.datetime.today() + gmt_m_5
    now_day = days[now.weekday()]
    now_hour = now.hour if now.hour < 12 else now.hour - 12
    now_minute = now.minute
    start = now - offset
    start_day = days[start.weekday()]
    start_hour = start.hour if start.hour < 12 else start.hour - 12
    start_minute = start.minute
    days = {now_day: True, start_day: True}
    am_pm = SprinkleSchedule.AM if start.hour < 12 else SprinkleSchedule.PM
    scheduled_devices = SprinkleSchedule.objects.filter(
        hour__gte=start_hour,
        hour__lte=now_hour,
        minute__gte=start_minute,
        minute__lt=now_minute,
        am_pm=am_pm,
        **days
    )
    if not scheduled_devices.exists():
        print('{now} no device scheduled.'.format(now=now))
        return
    scheduled_sprinkle(scheduled_devices)
