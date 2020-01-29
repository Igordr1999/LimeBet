from modeltranslation.translator import TranslationOptions, translator

from .models import BugTrackerProduct, BugTrackerType, BugTrackerTag, BugTrackerPriority, BugTrackerStatus


class BugTrackerProductTranslationOptions(TranslationOptions):
    fields = ('name',)


class BugTrackerTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


class BugTrackerTagTranslationOptions(TranslationOptions):
    fields = ('name',)


class BugTrackerPriorityTranslationOptions(TranslationOptions):
    fields = ('name',)


class BugTrackerStatusTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(BugTrackerProduct, BugTrackerProductTranslationOptions)
translator.register(BugTrackerType, BugTrackerTypeTranslationOptions)
translator.register(BugTrackerTag, BugTrackerTagTranslationOptions)
translator.register(BugTrackerPriority, BugTrackerPriorityTranslationOptions)
translator.register(BugTrackerStatus, BugTrackerStatusTranslationOptions)
