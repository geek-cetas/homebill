from django.contrib import admin
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls.defaults import patterns, url
from bills.models import *
from bills.forms import *

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

class UserAdmin(admin.ModelAdmin):
    def queryset(self, req):
        qs = super(UserAdmin, self).queryset(req)
        return qs.filter(User = req.user)

    def save_model(self, req, obj, form, change):
        obj.User = req.user
        super(UserAdmin, self).save_model(req, obj, form, change)

    def formfield_for_foreignkey(self, db_field, req, **kwargs):
        return super(UserAdmin, self).formfield_for_foreignkey(\
                                        db_field, req, **kwargs)

class BillAdmin(UserAdmin):
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

    def get_urls(self):
        urls = super(BillAdmin, self).get_urls()
        model_urls = patterns('',
            (r'(?P<obj_id>\d+)/files/(?P<filename>.*)/$',
                self.serve_file))
        return model_urls + urls

    def serve_file(self, req, obj_id, filename):
        return HttpResponseRedirect('/static/files/%s' % filename)

class TransactionAdmin(UserAdmin):
    list_display = ('bill_link', 'Amount', 'Type', 'Date', 'Description')
    list_filter = ('Type', 'Bill')
    fields = ('Amount', 'Date', 'Type', 'Description', 'Bill')
    readonly_fields = ('Amount', 'Date', 'Type', 'Bill')
    list_display_links = ('Amount',)

    def has_add_permission(self, req):
        return False

    def has_delete_permission(self, req, obj=None):
        return False

    def queryset(self, req):
        return Transaction.objects.filter(Bill__User = req.user)

class PeriodicalAdmin(UserAdmin):
    list_display = ('Title', 'billedon', 'dueby', 'duecount', 'bills')
    fields = ('Title', 'Description', 'Billingdate', 'Duedate', 'Bills')

    def queryset(self, req):
        qs = super(PeriodicalAdmin, self).queryset(req)
        return qs.filter(User = req.user)

class ReimbursementAdmin(UserAdmin):
    list_display = ('Title', 'Amount', 'bill_display')
    exclude = ('User',)

    def formfield_for_manytomany(self, db_field, req, **kwargs):
        if db_field.name == 'Bills':
            kwargs['queryset'] = Bill.objects.filter(User = req.user)
        return super(ReimbursementAdmin, self).\
                    formfield_for_manytomany(db_field, req, **kwargs)


admin.site.register(Bill, BillAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Periodical, PeriodicalAdmin)
admin.site.register(Reimbursement, ReimbursementAdmin)
