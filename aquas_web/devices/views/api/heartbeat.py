import datetime

from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from django.db.models import Count, DateField, Max, Q
from django.db.models.functions import Cast


from devices.serializers import DeviceHeartbeatSerializer
from devices.models import DeviceHeartbeat


def days_till_today():
    now = datetime.datetime.now()
    progress = now + datetime.timedelta(days=-30)
    step = datetime.timedelta(days=1)

    while progress <= now:
        yield progress.strftime('%Y-%m-%d')
        progress += step


class DeviceHeartbeatViewSet(GenericViewSet):
    queryset = DeviceHeartbeat.objects.all()
    serializer_class = DeviceHeartbeatSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        :param request:
        :return:
        """
        query = self.get_queryset()\
            .filter(device__owner=request.user)\
            .filter(Q(resolved=True) | Q(connection_status__in=[DeviceHeartbeat.HEARTBEAT, DeviceHeartbeat.DEVICE_ON]))\
            .values('device', 'connection_status')\
            .annotate(connection_time=Max('connection_time'))
        return JsonResponse(list(query), safe=False)

    @action(detail=False, methods=['get'])
    def daily_sprinkles(self, request):
        """
        list(DeviceHeartbeat.objects.filter(connection_status='sprinkle').annotate(conn_time=Cast('connection_time', DateField())).values('conn_time').annotate(Count('device')))


        select DATE(connection_time) as conn_day, COUNT(DATE(connection_time)) as total from devices_deviceheartbeat where connection_status = "sprinkle" group by conn_day ORDER BY conn_day DESC;


        Migration query
        INSERT INTO devices_deviceheartbeat
         (connection_time, connection_status, device_id, heartbeat_code, resolved)
        SELECT updated_at, task_type, device_id, code,resolved
        FROM devices_scheduledtasks
        where resolved=1


        Expected postgres
        Select calendar, count("apis"."created_at") as total
          from generate_series('2019-05-01', date_trunc('day', CURRENT_DATE), interval '1 day') calendar
        left join "public"."devices_deviceheartbeat" hb on "hb"."connection_time"::date==calendar
        group by 1
        order by 1 ASC

        :param request:
        :return:
        """
        devices_count = list(
            DeviceHeartbeat.objects
            .filter(connection_status='sprinkle', resolved=True)
            .annotate(conn_time=Cast('connection_time', DateField()))
            .values('conn_time')
            .annotate(sprinkles=Count('device'))
        )

        sprinkles = [{'day': date, 'sprinkles': next(filter(lambda x: x['conn_time'].strftime('%Y-%m-%d') == date, devices_count), {}).get('sprinkles', 0)} for date in days_till_today()]

        return JsonResponse({'devices_count': sprinkles}, safe=False)

    @action(detail=False, methods=['get'])
    def active_devices(self, request):
        now = datetime.datetime.now()
        progress = now - datetime.timedelta(minutes=10)
        active_count = DeviceHeartbeat.objects\
            .filter(connection_status__in=[DeviceHeartbeat.HEARTBEAT, DeviceHeartbeat.DEVICE_ON], connection_time__gte=progress)\
            .values('device')\
            .annotate(connection_time=Max('connection_time'))\
            .count()

        return JsonResponse({'active_devices': active_count})
