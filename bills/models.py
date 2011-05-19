from django.db import models
from django.contrib.auth.models import User

PAYMENT_TYPES = (
    ('C', 'Credit card'),
    ('D', 'Debit card'),
    ('N', 'Net banking'),
    ('R', 'Direct cash')
    )

class Bill(models.Model):
    Company = models.CharField(max_length=100)
    BillId = models.CharField(max_length=100)
    Amount = models.FloatField()
    User = models.ForeignKey(User)
    Type = models.CharField(max_length=1, choices = PAYMENT_TYPES,
                            verbose_name = 'Payment type',
                            default = 'C')
    Proofs = models.FileField(null = True, upload_to = 'files')

    def attachments(self):
        url = str(self.Proofs)
        filename = url.split('/')[-1]
        anchor = '<a href="/static/%(url)s"> %(img)s %(link)s </a>'
        img = '<img src="/static/images/icons/%s.gif" />' % \
                filename[-3:]
                
        return anchor % {'url' : url, 'img' : img,
                            'link' : filename}

    attachments.short_description = 'Proofs'
    attachments.allow_tags = True

