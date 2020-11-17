import json
from django.http import HttpResponse, JsonResponse
# Create your views here.
from common.models import Medicine


def dispatcher(request):
    # 权限问题，登录的
    if "usertype" not in request.session:
        return JsonResponse({"ret": 1, "mgs": "请登录", "redirect": "/mgr/sign.html"}
                            , status=302)

    if request.session["usertype"] != "mgr":
        return JsonResponse({"ret": 1, "mgs": "不是管理者用户，请登录管理者用户", "redirect": "/mgr/sign.html"}
                            , status=302)

    # 把参数都存在请求参数中，开始分离get和post了
    if request.method == "GET":
        request.params = request.GET

    if request.method in ["POST", "PUT", "DELETE"]:
        request.params = json.loads(request.body)

    if request.params["action"] == "list_medicine":
        return list_medicine(request)
    if request.params["action"] == "add_medicine":
        return add_medicine(request)
    if request.params["action"] == "modify_medicine":
        return modify_medicine(request)
    if request.params["action"] == "del_medicine":
        return del_medicine(request)


def list_medicine(request):
    qs=Medicine.objects.values()
    qs_list=list(qs)
    return JsonResponse({"ret":0,"retlist":qs_list})


def add_medicine(request):
    res_site=[]
    data=request.params["data"]
    try:
        Medicine.objects.get(name=data["name"])
        res_site.append("name")
    except:
        pass
    try:
        Medicine.objects.get(sn=data["sn"])
        res_site.append("sn")
    except:
        pass
    if ["name","sn"] == res_site:
        return JsonResponse({"ret": 1, "msg": "sn和name存在，无法添加"})

    elif "name" in res_site:
        return JsonResponse({"ret": 1, "msg": "name名存在，无法添加"})
    elif "sn" in res_site:
        return JsonResponse({"ret":1,"msg":"sn名存在，无法添加"})

    record=Medicine.objects.create(desc=data["desc"],
                                   name=data["name"],
                                   sn=data["sn"])

    return JsonResponse({"ret":0,"id":record.id})


def modify_medicine(request):
    res_id=request.params["id"]
    newdata=request.params["newdata"]

    try:
        modify=Medicine.objects.get(id=res_id)
    except:
        return JsonResponse({"ret":1,"mgs":"id没有找到，无法修改"})
    if "name" in newdata:
        modify.name=newdata["name"]
    if "sn" in newdata:
        modify.name=newdata["sn"]
    if "desc" in newdata:
        modify.name=newdata["desc"]
    modify.save()
    return JsonResponse({"ret":0,"msg":"订单修改成功"})


def del_medicine(request):
    res_id=request.params["id"]

    try:
        delete = Medicine.objects.get(id=res_id)
    except:
        return JsonResponse({"ret": 1, "mgs": f"id{res_id}没有找到，无法删除"})

    delete.delete()
    return JsonResponse({"ret":0,"msg":f"id{res_id}删除成功"})

