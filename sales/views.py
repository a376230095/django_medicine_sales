from django.http import HttpResponse

from common.models import Custom

html_template = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
table {
    border-collapse: collapse;
}
th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
</style>
</head>
    <body>
        <table>
        <tr>
        <th>id</th>
        <th>姓名</th>
        <th>电话号码</th>
        <th>地址</th>
        </tr>
        
       
        {% for customer in customers %}
            <tr>
            
            {% for name,value in customer.items %}
            <td>{{ value }}</td>
            {% endfor %}
            
            </tr>
        {% endfor %}
        
       


        </table>
    </body>
</html>
'''

# 导入模板引擎
from django.template import engines

# 定义django模板引擎
django_engine = engines['django']
# 模板就从html_template获取
template = django_engine.from_string(html_template)


def listcustomers(request):
    # 相当于select * from Custom这个表，字典保存，一行大字典，里面内嵌小字典
    qs = Custom.objects.values()
    # 相当于get请求的参数有phonenumber=xxx，如果找到，就返回值，找不到就返回None
    ph = request.GET.get("phonenumber", None)
    # 当电话号码存在的时候
    if ph:
        # 相当于select * from Custom where phonenumber=ph
        qs = qs.filter(phonenumber=ph)

    # 传入渲染模板需要的参数，这个参数是上面html的qs
    # 这个非常消耗后端的资源
    rendered = template.render({'customers': qs})

    # 最后的响应回我们要的信息,html_template有一个%s，刚刚好给table_content接收用到
    return HttpResponse(rendered)
