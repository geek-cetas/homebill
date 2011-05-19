from django.db import models
from django.contrib.auth.models import User

PAYMENT_TYPES = (
    ('C', 'Credit card'),
    ('D', 'Debit card'),
    ('N', 'Net banking'),
    ('R', 'Direct cash')
    )
BILL_TYPE = (
    ('M', 'Medical'),
    ('T', 'Telephone'),
    ('G', 'Grossary'),
    ('H', 'Household'),
    ('R', 'Rent'),
    ('I', 'Miscellaneous')
    )

class Bill(models.Model):
    Merchant = models.CharField(max_length=100)
    BillId = models.CharField(max_length=100,
                                verbose_name='Bill no')
    Type = models.CharField(max_length=1, choices=BILL_TYPE,
                            default='I')
    User = models.ForeignKey(User)

    def __str__(self):
        return self.Merchant

    def transactions(self):
        transactions = Transaction.objects.filter(Bill=self)
        text = ""
        for trans in transactions:
            text += "%s<br/>" % trans.link()
        return text

    transactions.short_description = 'Transactions'
    transactions.allow_tags = True
    transactions.is_active_filter = True

    def attachments(self):
        proofs = Proof.objects.filter(Bill=self)
        display_html = ''
        for proof in proofs:
            display_html += "%s<br/>" % proof.get_display_html()

        return display_html

    attachments.short_description = 'Proofs'
    attachments.allow_tags = True

class Transaction(models.Model):
    Bill = models.ForeignKey(Bill, verbose_name = 'Merchant')
    Amount = models.FloatField()
    Date = models.DateField()
    Type = models.CharField(max_length=1, choices=PAYMENT_TYPES,
                            default='C')
    Description = models.TextField(null=True, blank=True)

    def bill_link(self):
        bill_url =  '<a href="../bill/%(billid)d">%(merchant)s</a>'
        return bill_url % {'billid' : self.Bill.id,
                            'merchant' : self.Bill.Merchant}
    bill_link.allow_tags = True
    bill_link.short_description = 'Merchant'
    bill_link.admin_order_field = 'Bill'

    def link(self):
        url = '<a href="../transaction/%(transid)d">%(type)s : ' \
                '%(amount)0.2f</a>'
        return url % {'transid' : self.id, 
                        'type' : self.get_Type_display(),
                        'amount' : self.Amount}

    def __str__(self):
        transaction_template = "Amount : %(amount)0.2f, Type : %(type)s"
        return transaction_template % {'amount' : self.Amount, 
                                        'type' : self.get_Type_display()}

    def __unicode__(self):
        return self.__str__()

class Proof(models.Model):
    Bill = models.ForeignKey(Bill)
    File = models.FileField(null=True, upload_to='files')

    def get_display_html(self):
        filename = self.File.name.split('/')[-1]
        url = self.File.url
        anchor = '<a href="/static/%(url)s"> %(img)s %(link)s </a>'
        img = '<img src="/static/images/icons/%s.gif" />' % \
                    filename[-3:].lower()
        return anchor % {'url' : url, 'img' : img,
                            'link' : filename}

