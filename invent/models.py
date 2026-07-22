from django.db import models

class  InventoryCodes (models.Model):
    art = models.CharField(max_length=150, blank=False, default="None")
    cis = models.CharField(max_length=150, blank=False, default="None")
    gtin = models.CharField(max_length=150, blank=False, default="None")
    productName = models.CharField(max_length=150, blank=False, default="None")
    applicationDate = models.CharField(max_length=150, blank=False, default="None")
    introducedDate = models.CharField(max_length=150, blank=False, default="None")
    manufacturerInn = models.CharField(max_length=150, blank=False, default="None")
    manufacturerName = models.CharField(max_length=150, blank=False, default="None")
    requestedCis = models.CharField(max_length=150, blank=False, default="None")
    tnVedEaes = models.CharField(max_length=150, blank=False, default="None")
    tnVedEaesGroup = models.CharField(max_length=150, blank=False, default="None")
    productGroupId = models.IntegerField(blank=False, default=0)
    productGroup = models.CharField(max_length=150, blank=False, default="None")
    brand = models.CharField(max_length=150, blank=False, default="None")
    producedDate = models.CharField(max_length=150, blank=False, default="None")
    emissionDate = models.CharField(max_length=150, blank=False, default="None")
    emissionType = models.CharField(max_length=150, blank=False, default="None")
    packageType = models.CharField(max_length=150, blank=False, default="None")
    generalPackageType = models.CharField(max_length=150, blank=False, default="None")
    child = models.CharField( blank=False, default="None")
    ownerInn = models.CharField(max_length=150, blank=False, default="None")
    ownerName = models.CharField(max_length=150, blank=False, default="None")
    status = models.CharField(max_length=150, blank=False, default="None")
    statusEx = models.CharField(max_length=150, blank=False, default="None")
    producerInn = models.CharField(max_length=150, blank=False, default="None")
    producerName = models.CharField(max_length=150, blank=False, default="None")
    expirationDate = models.CharField(max_length=150, blank=False, default="None")



    def __str__(self):
        return f'{self.art} | {self.gtin} {self.cis} ({self.productName})'