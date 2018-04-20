# Generated by Django 2.0.3 on 2018-04-18 01:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('act', 'active'), ('dis', 'disabled')], default='act', max_length=5)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceConnections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_time', models.DateTimeField(auto_now_add=True)),
                ('connection_status', models.CharField(choices=[('spr_ok', 'sprinkle_ok'), ('spr_err', 'sprinkle_error'), ('hb', 'ping')], default='hb', max_length=15)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
            ],
        ),
        migrations.CreateModel(
            name='SprinkleSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(23)])),
                ('minute', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(59)])),
                ('am_pm', models.CharField(choices=[('am', 'am'), ('pm', 'pm')], default='am', max_length=15)),
                ('on_monday', models.BooleanField(default=False)),
                ('on_tuesday', models.BooleanField(default=False)),
                ('on_wednesday', models.BooleanField(default=False)),
                ('on_thursday', models.BooleanField(default=False)),
                ('on_friday', models.BooleanField(default=False)),
                ('on_saturday', models.BooleanField(default=False)),
                ('on_sunday', models.BooleanField(default=False)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
            ],
        ),
    ]
