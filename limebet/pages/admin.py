from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import BugTrackerType, BugTrackerTag, BugTrackerPriority, BugTrackerStatus, BugTrackerReport, \
    BugTrackerProduct


@admin.register(BugTrackerType)
class BugTrackerTypeAdmin(TranslationAdmin):
    list_display = ['name_en']


@admin.register(BugTrackerTag)
class BugTrackerTagAdmin(TranslationAdmin):
    list_display = ['name_en']


@admin.register(BugTrackerPriority)
class BugTrackerPriorityAdmin(TranslationAdmin):
    list_display = ['name_en']


@admin.register(BugTrackerStatus)
class BugTrackerStatusAdmin(TranslationAdmin):
    list_display = ['name_en']


@admin.register(BugTrackerProduct)
class BugTrackerProductAdmin(TranslationAdmin):
    list_display = ['name_en']


@admin.register(BugTrackerReport)
class BugTrackerReportAdmin(admin.ModelAdmin):
    list_display = ['title']
