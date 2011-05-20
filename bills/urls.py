from django.conf.urls.defaults import patterns, url
from bills.views import *

urlpatterns = patterns('bills.views',
    url(r'reimbursement/(?P<id>\d+)/', modify_reimbursement),
    )
