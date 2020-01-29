from django import forms
import django_filters
from .models import BugTrackerReport, MyResultQuote


class ReportForm(forms.ModelForm):
    class Meta:
        model = BugTrackerReport
        fields = ['product', 'title', 'description', 'playback_steps', 'expected_result', 'factual_result',
                  'type_report', 'tags', 'priority', 'screenshot']


class ReportParamForm(django_filters.FilterSet):
    class Meta:
        model = BugTrackerReport
        fields = ['product', 'title', 'type_report', 'tags', 'priority', 'status']


class MyResultQuoteForm(django_filters.FilterSet):
    class Meta:
        model = MyResultQuote
        fields = ['result', 'amount']
