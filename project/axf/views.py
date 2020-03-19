from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Wheel, Navigator, MustBuy, Commodity, GoodsOnSale, GoodsTypes, Goods, User

# Create your views here

# 测试页
def testpage(request):
    nav = Navigator.objects.all()
    return HttpResponse(f"测试页面完成~{nav.name}")


# 主页
def home(request):
    wheelsList = Wheel.objects.all()
    navList = Navigator.objects.all()
    mustBuyList = MustBuy.objects.all()
    commodityList = Commodity.objects.all()

    commodity1 = commodityList[0]
    commodity2 = commodityList[1:3]
    commodity3 = commodityList[3:7]
    commodity4 = commodityList[7:11]

    mainList = GoodsOnSale.objects.all()
    return render(request, 'axf/home.html', {"title": "主页", "wheelsList": wheelsList, "navList": navList,
                                             "mustBuyList": mustBuyList, 'commodity1': commodity1, 'commodity2': commodity2,
                                             'commodity3': commodity3, 'commodity4': commodity4, "mainList": mainList})


# 个人资料
def profile(request):
    return render(request, 'axf/profile.html', {"title": "我的"})


# 登录
from .forms.login import LoginForm
def login(request):
    # 此种表单写法不能使用ajax实现
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
        #     changed_data为用户提交的内容
            user = f.cleaned_data["username"]
            password = f.cleaned_data["password"]
            # print(user, password)
            # return HttpResponse("登录测试")
            return render(request, 'axf/login.html', {"username": user, "password": password})
        else:
            return render(request, 'axf/login.html', {"title": "登录", "form": f, "error": f.errors})
    # 点击未登录，加载登录表单
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {"title": "登录", "form": f})


# 注册
def register(request):
    return render(request, 'axf/register.html', {"title": "注册"})


# 检测注册账户是否已存在
def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount=userid)
        # 返回的第一个参数被register.js中函数的data接收，第二个参数为status
        return JsonResponse({"data": "该用户名已被注册", "status": "error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data": "注册成功", "status": "success"})


# 商城
def mall(request, categoryid, cid, sortid):
    '''categoryid默认为热销榜；cid为子组id，用于查询；sortid为排序id；'''
    leftBar = GoodsTypes.objects.all()
    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid, childId=cid)  # 两个条件同时满足
    group = leftBar.get(typeid=categoryid)
    # 分割数据：全部分类:0#进口水果:103534#国产水果:103533
    # 定义闪购页面上方分类功能
    childList = []
    childtypes = group.childtypenames.split("#")
    for s in childtypes:
        arr = s.split(":")
        obj = {"childName": arr[0], "childId": arr[1]}
        childList.append(obj)
    # 定义闪购页面排序功能，排序使用order_by()
    if sortid == '1':
        productList = productList.order_by('productnum')
    elif sortid == '2':
        productList = productList.order_by('price')
    elif sortid == '3':
        productList = productList.order_by('-price')

    return render(request, 'axf/mall.html', {"title": "商城", 'leftBar': leftBar, 'productList': productList,
                                             "childList": childList, "categoryid": categoryid, "cid": cid})


# 重定向mall
def mall_redirect(request):
    return redirect('/mall/')


# 购物租车
def trolley(request):
    return render(request, 'axf/trolley.html', {"title": "购物车"})

