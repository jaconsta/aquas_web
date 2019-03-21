# Generated by Django 2.0.9 on 2019-03-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20190213_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceheartbeat',
            name='heartbeat_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='deviceheartbeat',
            name='connection_status',
            field=models.CharField(choices=[('sprinkle', 'sprinkle_ok'), ('error', 'sprinkle_error'), ('heartbeat', 'ping')], default='heartbeat', max_length=15),
        ),
    ]