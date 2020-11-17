import json
from django.http import HttpResponse, JsonResponse
# Create your views here.
from common.models import Custom


def dispatcher(request):
    # 判断请求中的session_id，获取session_data，看看有没有usertype这个key
    # 如果没有就表示用户没有登录，不能查看，跳转到登录界面
    if "usertype" not in request.session:
        return JsonResponse({"ret":1,"msg":"请登录","redirect":"/mgr/sign.html"}
                            ,status=302)
    # 登录了之后，如果usertype不是mgr的管理者，说明不是管理者用户，也跳转到登录界面
    if request.session["usertype"] != "mgr":
        return JsonResponse({"ret":1,"msg":"请登录管理者用户","redirect":"/mgr/sign.html"})

    # 如果是get的请求，把请求的参数都放到请求参数中
    if request.method == "GET":
        request.params = request.GET
    # 如果是put、delete、post请求，请求的参数存放请求体，并转化成python字典的形式
    elif request.method in ["PUT", "DELETE", "POST"]:
        request.params = json.loads(request.body)

    # 接口文档中，action在get中是参数，在其他请求方式是请求体，但都转化成参数了使用了，上一句代码
    action = request.params["action"]
    # 当action为以下的，就让下面的函数去处理我们的请求，dispatcher负责分发请求方式
    if action == "list_customer":
        return list_customer(request)
    elif action == "add_customer":
        return add_customer(request)
    elif action == "modify_customer":
        return modify_customer(request)
    elif action == "del_customer":
        return del_customer(request)

    # 当请求方式不在这里面，就返回响应：不支持的请求方式
    else:
        return JsonResponse({"ret": 1, "msg": "不支持的请求方式"})


# 获取所有联系人信息
def list_customer(request):
    # 通过数据库先获取所有的数据，需要返回数据
    qs = Custom.objects.values()
    # qs是query队列的类型，可以直接用list转化成列表嵌套字典的类型，符合我们retlist的返回方法
    res_list = list(qs)
    """
    {"ret": 0,
    "retlist": [
        {
            "address": "江苏省常州武进市白云街44号",
            "id": 1,
            "name": "武进市 袁腾飞",
            "phonenumber": "13886666666"
        },      
        {
            "address": "北京海淀区",
            "id": 4,
            "name": "北京海淀区代理 蔡国庆",
            "phonenumber": "13990123456"
        }]}
    """
    # 返回接口文档要求返回的内容，转化成json的格式
    return JsonResponse({"ret": 0, "retlist": res_list})


# 增加联系人
def add_customer(request):
    # 通过请求的参数拿到请求的数据，字典类型
    data = request.params["data"]

    # 把请求的数据写入到数据库中
    record = Custom.objects.create(name=data["name"],
                                   phonenumber=data["phonenumber"],
                                   address=data["address"])
    # 返回接口文档要求返回的内容，转化成json的格式
    return JsonResponse({"ret": 0, "id": record.id})


# 修改联系人
def modify_customer(request):
    # 拿到我们的id数据和修改的请求参数的数据
    req_id = request.params["id"]
    new_data = request.params["newdata"]

    # 如果id不存在，获取的数据库也没有，就会跳转到客户id不存在的响应了
    try:
        customer = Custom.objects.get(id=req_id)
    except:
        return JsonResponse({"ret": 1, "msg": f"客户id{req_id}不存在"})

    # 这里的if是做判断，万一请求传的不对，就不用更新数据了，orm获取一行数据，属性就是列名了
    if "name" in new_data:
        customer.name = new_data["name"]
    if "phonenumber" in new_data:
        customer.phonenumber = new_data["phonenumber"]
    if "address" in new_data:
        customer.address = new_data["address"]

    # 修改数据库的内容需要save保存，新增数据不用哦
    customer.save()
    return JsonResponse({"ret": 0})

# 删除联系人
def del_customer(request):
    # 获取要删除的id
    req_id = request.params["id"]
    # 如果id不存在，也就返回id不存在了
    try:
        customer = Custom.objects.get(id=req_id)
    except:
        return JsonResponse({"ret": 0, "msg": f"客户id{req_id}不存在"})

    # 删除一行数据需要用delete
    customer.delete()
    return JsonResponse({"ret": 0})
