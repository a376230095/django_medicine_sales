import json

from django.db import transaction
from django.http.response import JsonResponse
from common.models import Order, OrderMedicine
from django.db.models import F


def dispatcher(request):
    if "usertype" not in request.session:
        return JsonResponse({"ret": 1, "msg": "请登录", "redirect": "/mgr/sign.html"}
                            , status=302)
    if request.session["usertype"] != "mgr":
        return JsonResponse({"ret": 1, "msg": "请登录", "redirect": "/mgr/sign.html"}
                            , status=302)

    if request.method == "GET":
        request.params = request.GET

    if request.method in ["PUT", "POST", "DELETE"]:
        request.params = json.loads(request.body)

    if request.params["action"] == "add_order":
        return add_order(request)
    if request.params["action"] == "list_order":
        return list_order(request)


def add_order(request):
    # 提取新增的数据
    data = request.params["data"]
    # 提取新增药品的列表
    medicine_list = data["medicineids"]
    # 订单表增加
    # 开启事务
    with transaction.atomic():
        # 订单表的新增
        new_order = Order.objects.create(name=data["name"],
                                         customer_id=data["customerid"])
        # 一个列表生成式，生成不同的《订单药品》的表
        all = [OrderMedicine(order_id=new_order.id, medicine_id=medicine_id, amount=1)
               for medicine_id in medicine_list]
        # bulk_create可以批量新增数据
        OrderMedicine.objects.bulk_create(all)
    return JsonResponse({"ret": 0, "id": new_order.id})


def list_order(request):
    # 获取订单，订单是主表，因为返回的数据要与前端要保持一致，所以要改名
    # 强大的djgano，一个表__列名就可以获取外键，或者有关联的表数据，牛逼
    qs=Order.objects.annotate(customer_name=F("customer__name"),medicines_name=F("medicines__name")).\
        values("id","name","create_time","customer_name","medicines_name")
    # qs=Order.objects.annotate(customer_name=F("customer__name")).values("id","name","create_time","customer__name")
    qs_list=list(qs)
    return JsonResponse({"ret":0,"retlist":qs_list})
