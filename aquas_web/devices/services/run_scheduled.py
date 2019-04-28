from django.utils import timezone

from .logger import get_console_logger
from .save_scheduled_tasks import save_scheduled_tasks
from ..services.sprinkle import scheduled_sprinkle
from ..models import SprinkleSchedule

SPRINKLE_SCHEDULE_MIN = 5

logger = get_console_logger(__name__)


def run_scheduled_sprinkle():
    """
    Default python datetime management is not enough considering timezones.

    A possible approach is to generate a list of the next scheduled events
    and modify SprinkleSchedule to store user's timezone.

    I will hard code a timezone right now.

    :return:
    """
    logger.info('Running scheduled sprinkles')
    now = timezone.now()
    scheduled_devices = SprinkleSchedule.objects.filter(next_schedule__lte=now)
    run_success = scheduled_sprinkle(scheduled_devices)
    save_scheduled_tasks(run_success)
    logger.info('run_success')
    SprinkleSchedule.objects.filter(id__in=[run['device'] for run in run_success]).update(last_run=now)

