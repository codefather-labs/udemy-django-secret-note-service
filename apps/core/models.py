import uuid

from django.db import models


class AppConfig(models.Model):
    session_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=False
    )

    api_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=False,
        help_text='getting from https://my.telegram.org/auth'
    )

    api_hash = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=False,
        help_text='getting from https://my.telegram.org/auth'
    )

    is_active = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text='non active config is not working'
    )

    is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='select if you want to use bot account for this config'
    )

    bot_token = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        help_text='required if you use bot account.'
                  'use @botfather for create a bot or get token for available bot.'
    )

    timestamp = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'config'
        verbose_name_plural = 'configs'

    def __str__(self):
        return f"ID:{self.id}, Is active:{self.is_active}"


class Message(models.Model):
    text = models.TextField(
        default=None,
        null=True,
        blank=False,
    )

    access_token = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
    )

    is_viewed = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"ID:{self.id}, Is viewed:{self.is_viewed}"

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = f"{uuid.uuid1().hex}:{uuid.uuid4().hex}"

        if self.is_viewed:
            return self.delete()

        return super(Message, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
