from django.contrib import admin
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from bills.models import *

class ProofInline(admin.TabularInline):
    model = Proof
    fields = ('File', 'Receiptno')
    raw_id_fields = ('Bill',)
    max_num = 5
    fk_name = 'Bill'
    extra = 2

class TranscationInline(admin.StackedInline):
    model = Transaction
    extra = 1

class BillAdmin(admin.ModelAdmin):
    list_filter = ('Merchant', 'Type')
    list_display = ('Merchant', 'transactions',
                    'attachments', 'Type')
    search_fields = ('Merchant',)

    fieldsets = (
        ('Organization', {
            'fields' : ('Merchant', 'BillId', 'Type')
            }),
        )
    inlines = [TranscationInline, ProofInline]

    def save_model(self, request, obj, form, change):
        obj.User = request.user
        super(BillAdmin, self).save_model(request, obj, form, change)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('bill_link', 'Amount', 'Type', 'Date', 'Description')
    list_filter = ('Type', 'Bill')
    fields = ('Amount', 'Date', 'Type', 'Description', 'Bill')
    readonly_fields = ('Amount', 'Date', 'Type', 'Bill')
    list_display_links = ('Amount',)

    def has_add_permission(self, req):
        return False

    def has_delete_permission(self, req, obj=None):
        return False

admin.site.register(Bill, BillAdmin)
admin.site.register(Transaction, TransactionAdmin)

