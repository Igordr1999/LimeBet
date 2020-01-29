from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
import uuid
from django.utils.translation import ugettext_lazy as _
from data.models import Result, Event
from django.core.validators import MaxValueValidator, MinValueValidator


class BugTrackerProduct(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bug Tracker Product')
        verbose_name_plural = _('Bug Tracker Products')
        ordering = ["name"]


class BugTrackerTag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bug tracker tag')
        verbose_name_plural = _('Bug tracker tags')
        ordering = ["name"]


class BugTrackerType(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bug tracker type')
        verbose_name_plural = _('Bug tracker type')
        ordering = ["name"]


class BugTrackerPriority(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bug tracker priority')
        verbose_name_plural = _('Bug tracker priorities')
        ordering = ["name"]


class BugTrackerStatus(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bug tracker status')
        verbose_name_plural = _('Bug tracker statuses')
        ordering = ["name"]


class BugTrackerReport(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Owner'))
    product = models.ForeignKey(BugTrackerProduct, on_delete=models.CASCADE, verbose_name=_('Product'))
    title = models.CharField(max_length=64, verbose_name=_('Title'))
    description = models.CharField(max_length=64, verbose_name=_('Description'))
    playback_steps = models.TextField(max_length=128, verbose_name=_('Playback steps'))
    expected_result = models.CharField(max_length=128, verbose_name=_('Expected Result'))
    factual_result = models.CharField(max_length=128, verbose_name=_('Factual Result'))
    type_report = models.ForeignKey(BugTrackerType, on_delete=models.CASCADE, verbose_name=_('Type report'))
    tags = models.ManyToManyField(BugTrackerTag, verbose_name=_('Tags'))
    priority = models.ForeignKey(BugTrackerPriority, on_delete=models.CASCADE, verbose_name=_('Priority'))
    screenshot = ProcessedImageField(upload_to='pages/bugtracker/screenshot/',
                                     format='PNG',
                                     options={'quality': 60},
                                     null=True,
                                     blank=True,
                                     verbose_name=_('Screenshot'))
    status = models.ForeignKey(BugTrackerStatus, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Status'))
    admin_answer = models.TextField(max_length=512, null=True, blank=True, verbose_name=_('Admin answer'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))
    create_time = models.DateTimeField(verbose_name=_('Create time'), null=True, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=_('Update time'), null=True, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Bug tracker report')
        verbose_name_plural = _('Bug tracker reports')
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if self.screenshot:
            random_name = uuid.uuid4().hex + ".png"
            self.screenshot.save(random_name, self.screenshot, save=False)
        super(BugTrackerReport, self).save(*args, **kwargs)


class MyResultQuote(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Owner'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_('Event'))
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name=_('Result'))
    quote_value = models.FloatField(verbose_name=_('Quote value'))
    amount = models.FloatField(verbose_name=_('Amount'),
                               validators=[MinValueValidator(10.0), MaxValueValidator(100.0)],)

    def __str__(self):
        return str("{}, {}, {}".format(self.result.period_number, self.result.quote_name, self.quote_value))

    class Meta:
        verbose_name = _('My result quote')
        verbose_name_plural = _('My result quotes')
        ordering = ["amount"]
