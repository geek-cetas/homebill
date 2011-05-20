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
    ('T', 'Telephone/Broadband'),
    ('G', 'Groceries'),
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
        trans = Transaction.objects.get(Bill=self)
        date = trans.Date.strftime("%d/%m/%Y")
        return "%(merchant)s - %(date)s" % {'merchant' : self.Merchant,
                                            'date' : date}

    def get_link(self, date=False):
        bill_url =  '<a href="../bill/%(billid)d">%(merchant)s ' \
                    '%(date)s</a>'
        return bill_url % {'billid' : self.id,
                            'merchant' : self.Merchant,
                            'date' : self.date.strftime("%d/%m/%Y") \
                                if date else ''}

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
        return self.Bill.get_link()
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
    Receiptno = models.CharField(max_length=35, blank=True, null=True)
    File = models.FileField(null=True, upload_to='files')

    def get_display_html(self):
        filename = self.File.name.split('/')[-1]
        url = self.File.url
        anchor = '<a href="/static/%(url)s"> %(img)s %(link)s </a>'
        img = '<img src="/static/images/icons/%s.gif" />' % \
                    filename[-3:].lower()
        return anchor % {'url' : url, 'img' : img,
                            'link' : filename}

class Periodical(models.Model):
    User = models.ForeignKey(User)
    Title = models.CharField(max_length=50)
    Description = models.TextField(null=True, blank=True)
    Billingdate = models.DateField()
    Duedate = models.DateField()
    Bills = models.ManyToManyField(Bill, null=True, blank=True)

    def billedon(self):
        return self.Billingdate.strftime("%d")

    def dueby(self):
        return self.Duedate.strftime("%d")

    def duecount(self):
        bills = self.Bills.all()
        count = 0
        for bill in bills:
            trans = Transaction.objects.get(Bill=bill)
            if trans:
                if self.Duedate < trans.Date:
                    count += 1
        return count

    def bills(self):
        bills = self.Bills.all()
        html = "<ul>%(items)s</ul>"
        items = []
        for bill in bills:
            items.append("<li>%(link)s</li>" % {'link' : bill.get_link()})
        items = reduce(lambda l1, l2 : l1 + l2, items)
        return html % {'items' : items}
    bills.allow_tags = True

class Reimbursement(models.Model):
    Bills = models.ManyToManyField(Bill, null=True, blank=True)
    User = models.ForeignKey(User)
    Amount = models.FloatField(null=True, blank=True,
                                help_text="Amount to be reimbursed")

    def bill_display(self):
        bills = self.Bills.all()
        html = "<a href='../bill/?id__in=%(ids)s'>Total : %(count)d</a>"
        ids = map(lambda obj1 : "%s" % (obj1.id), bills)
        return html % {'ids' : reduce(lambda x, y : "%s,%s" % (x, y),
                        ids),
                        'count' : len(bills) }
    bill_display.allow_tags = True
    bill_display.short_description = 'Bills'
