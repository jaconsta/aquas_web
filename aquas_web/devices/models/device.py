from django.db import models
from django.contrib.auth.models import User

from devices.utils import id_generator


class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=50, unique=True)

    # Friendly name
    name = models.CharField(max_length=150)

    ACTIVE = 'act'
    DISABLED = 'dis'
    status_choices = (
        (ACTIVE, 'active'),
        (DISABLED, 'disabled')
    )
    status = models.CharField(max_length=5, choices=status_choices, default=ACTIVE)

    register_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#{id}.UUID {unique_id}, status: {status}, owner: {owner}".format(
            id=self.id,
            unique_id=self.unique_id,
            status=self.status,
            owner=self.owner.email
        )

    @classmethod
    def createDevice(cls, user, name):
        unique_id = id_generator()
        device = cls(owner=user, unique_id=unique_id, name=name)
        device.save()
        return device


    @classmethod
    def get_by_id(cls, pk):
        return cls.objects.get(id=pk)
