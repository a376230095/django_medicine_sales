from django.http import JsonResponse
# 导入djgano登录和登出方法
from django.contrib.auth import authenticate, login, logout

def sign_login(request):
    # 获取post请求的username
    username=request.POST.get("username")
    # 获取post请求的password
    password=request.POST.get("password")
    # 这里直接做用户名和密码的校验，登录成功后，就拥有了user表的一行记录了
    user=authenticate(username=username,password=password)

    # 检查登录是不是成功了
    if user is not None:
        # is_active表示用户是否已经激活了
        if user.is_active:
            # 检查是否是超级用户
            if user.is_superuser:
                # 如果是超级用户，就执行登录操作
                login(request,user)
                # 登录成功，把session表添加usertype=mgr的key-value的值，保存在session_value中
                # 未来只要是管理者用户，才有权限，通过这个session来校验
                request.session['usertype'] = 'mgr'
                # 返回登录成功的响应
                return JsonResponse({"ret": 0, "msg": "登录成功"})
            else:
                # 返回不是管理者用户的响应
                return JsonResponse({"ret":1,"msg":"请使用管理员账号登录"})
        else:
            # 返回用户没有激活的响应
            return JsonResponse({"ret":1,"msg":"用户还没激活"})
    else:
        # 返回密码错误或者用户错误的响应
        return JsonResponse({"ret":1,"msg":"用户名密码错误"})

# 登出的函数
def sign_out(request):
    # 直接登出
    logout(request)
    # 返回登出成功
    return JsonResponse({"ret":0,"msg":"登出成功"})

