from django.db import models


# Create your models here.
# 继承models.Model
# 创建Custom表格
class Custom(models.Model):
    # 客户名字
    name = models.CharField(max_length=100)
    # 客户电话
    phonenumber = models.CharField(max_length=100)
    # 客户地址
    address = models.CharField(max_length=100)


# 药品表
class Medicine(models.Model):
    # 药品名称
    name = models.CharField(max_length=200)
    # 药品编号
    sn = models.CharField(max_length=200)
    # 描述
    desc = models.CharField(max_length=200)


# 订单表
import datetime


class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200)
    # 创建日期
    create_time = models.DateTimeField(default=datetime.datetime.now)
    # 客户
    customer = models.ForeignKey(Custom, on_delete=models.PROTECT)
    # 订单购买的药品，和Medicine表是多对多的关系
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    # 订单中药品的数量
    amount = models.PositiveIntegerField()


class Country(models.Model):
    name = models.CharField(max_length=100)


class Student(models.Model):
    name=models.CharField(max_length=100)
    grade=models.CharField(max_length=100)
    country=models.ForeignKey(Country,on_delete=models.PROTECT)














