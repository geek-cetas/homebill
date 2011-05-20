from django import forms
from django.forms.widgets import *
from django.utils.safestring import mark_safe
from threading import local
from bills.models import Reimbursement, Bill, Periodical

_thread_locals = local()

class ReimbursementForm(forms.ModelForm):
    class Meta:
        model = Reimbursement

class TestWidget(Widget):
    def render(self, name, value, attrs=None, **kwargs):
        print name, value, attrs, kwargs
        return mark_safe(u"<label>Kailash</label>")

class PeriodicalForm(forms.ModelForm):
    class Meta:
        model = Periodical
