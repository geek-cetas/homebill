from django.contrib import admin
from bills.models import *


class BillAdmin(admin.ModelAdmin):
    list_display = ('Company', 'Amount', 'Type', 'attachments')
    fieldsets = (
        ('Organization', {
            'fields' : ('Company', 'BillId')
            }),
        ('Payment', {
            'fields' : ('Amount', 'Type')
            }),
        ('Uploads', {
            'fields' : ('Proofs',)
            })
        )

    def save_model(self, request, obj, form, change):
        obj.User = request.user
        obj.save()

admin.site.register(Bill, BillAdmin)
