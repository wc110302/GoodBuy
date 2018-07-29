# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminUser(models.Model):
    username = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_user'


class Brand(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brand'


class Classification(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classification'


class Comments(models.Model):
    content = models.CharField(max_length=1024, blank=True, null=True)
    score = models.SmallIntegerField(blank=True, null=True)
    image = models.CharField(max_length=128, blank=True, null=True)
    create_time = models.DateField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    goods = models.ForeignKey('Goods', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Focus(models.Model):
    goods = models.ForeignKey('Goods', models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'focus'
        unique_together = (('goods', 'user'),)


class Goods(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    c_price = models.FloatField(blank=True, null=True)
    image = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    comments_amount = models.IntegerField(blank=True, null=True)
    sales_number = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=64, blank=True, null=True)
    subclassification = models.ForeignKey('Subclassification', models.DO_NOTHING, blank=True, null=True)
    brand = models.ForeignKey(Brand, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods'


class HistoryPrice(models.Model):
    price = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    good = models.ForeignKey(Goods, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history_price'


class Hot(models.Model):
    word = models.CharField(max_length=64, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hot'


class Subclassification(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)
    classification = models.ForeignKey(Classification, models.DO_NOTHING, blank=True, null=True)
    brand = models.ManyToManyField(Brand, through='SubclassificationBrand')

    class Meta:
        managed = False
        db_table = 'subclassification'


class SubclassificationBrand(models.Model):
    brand = models.ForeignKey(Brand, models.DO_NOTHING, primary_key=True)
    subclassification = models.ForeignKey(Subclassification, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subclassification_brand'
        unique_together = (('brand', 'subclassification'),)


class User(models.Model):
    username = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=512, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    icon = models.ImageField(upload_to='icons')
    goods = models.ManyToManyField(Goods, through='Focus')

    class Meta:
        managed = False
        db_table = 'user'


class UserTicket(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    ticket = models.CharField(max_length=256)
    out_time = models.DateTimeField()

    class Meta:
        db_table = 'user_ticket'
