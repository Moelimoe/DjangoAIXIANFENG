import os, random, time, string, io
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Wheel, Navigator, MustBuy, Commodity, GoodsOnSale, GoodsTypes, Goods, User, Trolley, Order
# from project import settings  # 效果同下一条
from django.conf import settings
from .forms.login import LoginForm
from .forms.register import RegisterForm
from PIL import Image, ImageDraw, ImageFont
from django.template.defaulttags import register


# 测试页
def testpage(request):
    verify_msg = ''
    if request.POST:
        _captcha_submit = request.POST.get('verify_code').lower()
        # 注意这里提交的验证码需要小写，服务器的验证码生成时已经小写，这样分开做是为了避免当验证码过期了再使用lower()函数而报错
        _captcha_server = request.session.get('verify_code')
        if _captcha_server == _captcha_submit:
            verify_msg = '验证成功'
        else:
            verify_msg = '验证失败'
    return render(request, 'axf/test.html', {"msg": verify_msg})


# 重定义字典方法，方便模板中使用字典
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# 主页
def home(request):
    in_home = True
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
                                             "mustBuyList": mustBuyList, 'commodity1': commodity1,
                                             'commodity2': commodity2, 'commodity3': commodity3,
                                             'commodity4': commodity4, "mainList": mainList,
                                             "in_home": in_home})


# 个人资料
def profile(request):
    in_profile = True
    print("进入profile验证userToken", request.session.get('userToken'))
    # 尝试获取用户登录信息
    try:
        # 从服务器获取对应的user信息，自动登录
        token = request.session.get('userToken')
        user = User.objects.get(userToken=token)
        userName = user.userName
        userLevel = user.userLevel
        userProfile = user.userAccount + user.userImg
        # print(userProfile)
        return render(request, 'axf/profile.html', {"title": "我的", "userName": userName, "userLevel": userLevel,
                                                    'userProfile': userProfile, "in_profile": in_profile})
    except User.DoesNotExist as e:
        return render(request, 'axf/profile.html', {"title": "我的", "in_profile": in_profile})


# 登录
def login(request):
    err_msg = ''
    # 判断是否提交POST进行登录
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            user = f.cleaned_data["username"]
            password = f.cleaned_data["password"]
            # 验证码进行比对，服务端的验证码小写化在存入session时已执行过
            captcha_submit = request.POST.get('verify_code').lower()
            captcha_server = request.session.get('verify_code')
            print(captcha_submit, captcha_server)
            if captcha_server == captcha_submit:
                try:
                    getuser = User.objects.get(userAccount=user, userPassword=password)
                    userName = getuser.userName
                    userLevel = getuser.userLevel
                    userProfile = getuser.userAccount + getuser.userImg
                    print("获取用户头像文件路径：", userProfile)
                    # 创建本次登录的userToken，并保存到数据库
                    userToken = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + \
                                time.strftime("%H%M%S", time.localtime())
                    getuser.userToken = userToken
                    getuser.save()
                    # 创建session中token，设置过期时间
                    request.session["userToken"] = userToken
                    # 关闭浏览器账号就过期（0）或其他时间（秒），或者时间对象
                    request.session.set_expiry(0)
                    return render(request, 'axf/profile.html', {"userName": userName, "userLevel": userLevel,
                                                                "userProfile": userProfile})
                except User.DoesNotExist as e:
                    err_msg = '账号或密码错误'
            else:
                err_msg = '验证码错误'
    # 点击未登录，加载登录表单
    f = LoginForm()
    print("未登录时走这里登录", err_msg)
    return render(request, 'axf/login.html', {"title": "登录", "form": f, 'error': err_msg})


#  生成验证码，可直接使用HttpResponse返回到html中，然后在img引用生成的验证码，实现及时性
def captcha(request):
    # 定义背景颜色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画布
    img = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(img)
    # 调用画笔的point()函数绘制验证码的干扰点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), 55)
        draw.point(xy, fill=fill)
    # 定义验证码的备选值————取所有字母和数字的组合
    _str = string.digits + string.ascii_letters
    # 随机在其中取四个值作为验证码
    rand_codes = ''.join(random.sample(_str, 4))
    # 定义字体大小
    size = int(min(width / len(rand_codes), height))
    # 构造字体对象
    font = ImageFont.truetype(r'http://moelimoe.fun/wp-content/uploads/2020/%E5%AD%97%E4%BD%93/arial/arial.ttf', size)
    # 构造字体颜色,四个字颜色不同
    for i in range(4):
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((i * 25, 2), rand_codes[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # # 将验证码缓存入session，后面做进一步验证，注意应该在这里存入的时候变为小写，
    # 否则验证码过期就变成了空，再进行lower()操作会抛出异常
    request.session['verify_code'] = rand_codes.lower()
    # 设置验证码有效时间(秒)
    request.session.set_expiry(60)
    # BytesIO()可以实现在内存中读写bytes
    buf = io.BytesIO()
    img.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，在html的img中引用src="/captcha/"即可
    return HttpResponse(buf.getvalue(), 'image/jpg')
    # png也行
    # return HttpResponse(buf.getvalue(), 'png')


# 登出1
# 1、退出登录使用logout(request)，函数需使用不同的名字
# 注意：如果函数命名为logout()则会和登出函数logout()重名，会导致冲突返回错误Maximum recursion depth exceeded
def signout(request):
    logout(request)
    return redirect('/profile/')


# 登出2
# 使用clear()清除session实现登出
def logout(request):
    request.session.clear()
    return render(request, 'axf/profile.html')


# 注册
def register(request):
    get_registered = ''
    if request.POST:
        f = RegisterForm(request.POST)
        if f.is_valid():
            try:
                userAccount = request.POST.get('username')  # name为"username"，再register.py中RegisterForm里
                userPassword = request.POST.get('password')  # 同上
                userName = request.POST.get('userName')
                userPhone = request.POST.get('userPhone')
                userAddress = request.POST.get('userAddress')
                userLevel = 0
                # 生成token值注册成功就会自动登录
                userToken = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + \
                            time.strftime("%H%M%S", time.localtime())
                userImg = request.FILES['userImg']
                request.session['userToken'] = userToken
                # 使用用户的账户拼接，以确保文件名不重复
                filePath = os.path.join(settings.MEDIA_ROOT, userAccount + userImg.name)
                with open(filePath, 'wb') as fp:
                    # for info in userImg.chunk():
                    for info in userImg:
                        fp.write(info)
                userRegister = User.createuser(userAccount, userPassword, userName, userPhone,
                                               userAddress, userImg, userLevel, userToken)
                userRegister.save()
                # 注册成功就导航到profile登录
                return redirect('/profile/')
            except Exception as e:
                get_registered = "注册失败，请检查你填写的信息是否正确"
                print("表单验证失败，错误信息：", e)
    # 未提交POST信息，刚进入页面则get_registered为空，否则提示注册失败
    f = RegisterForm()
    return render(request, 'axf/register.html', {"title": "注册", "form": f, 'get_registered': get_registered})


# 检测注册账户是否已存在，返回Json响应提示并阻断用户提交注册
def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({"data": "该用户名已被注册", "status": "error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data": "注册成功", "status": "success"})


# 商城
def mall(request, categoryid, cid, sortid):
    '''categoryid为产品大分类；cid为产品小分类，用于查询；sortid为排序id；'''
    in_mall = True
    order_dict = {'0': "综合排序", '1': "销量排序", '2': "价格最低", '3': "价格最高"}

    leftBar = GoodsTypes.objects.all()
    # 展示mall页面所有商品信息
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
    token = request.session.get("userToken")  # token是userToken
    # （如果已登录）取出用户购物车对应商品的数量，加载到mall页面
    print("useToken", token)
    item_info_Trolley = {}  # 储存用户购物车的物品
    if token:
        user = User.objects.get(userToken=token)
        user_Trolley = Trolley.objects.filter(userAccount=user.userAccount)  # 获取用户的trolley，而后返回其productnum作为默认值显示在mall页面
        for item in user_Trolley:
            item_info_Trolley[item.productid] = item.productnum
    print("排序方式：", sortid)

    return render(request, 'axf/mall.html', {"title": "商城", 'leftBar': leftBar, 'productList': productList,
                                             "childList": childList, "categoryid": categoryid, "cid": cid,
                                             "item_info_Trolley": item_info_Trolley, "sortid": sortid, "order_dict": order_dict,
                                             "in_mall": in_mall})


# 重定向回mall
def mall_redirect(request):
    return redirect('/mall/104749/0/0/')


# 购物车
def trolley(request):
    in_trolley = True
    token = request.session.get("userToken")
    if not token:
        return redirect('/login/')
    user = User.objects.get(userToken=token)
    trolleyList = Trolley.objects.filter(userAccount=user.userAccount)
    return render(request, 'axf/trolley.html', {"title": "购物车", "userName": user.userName, "userPhone": user.userPhone,
                                                "userAddress": user.userAddress, "trolleyList": trolleyList,
                                                "in_trolley": in_trolley})


# 修改购物车商品
def changetrolley(request, flag):
    token = request.session.get('userToken')
    # 使用了ajax则无法使用redirect重定向，只能使用JsonResponse
    # 如果没登录，返回错误信息给js
    if not token:
        return JsonResponse({"data": -1, "status": "error"})
    # 如果已登录
    # 加入的商品id
    product_id = request.POST.get("productid")
    # 获取用户信息
    user = User.objects.get(userToken=token)
    # 匹配用户购物车
    user_trolley = Trolley.objects.filter(userAccount=user.userAccount)
    # 匹配商品信息，如果存在重复id会报错，一般来说不应该有重复的id
    detail = Goods.objects.get(productid=product_id)
    # 取当前库存数值
    stores = detail.storenums
    # 添加商品0/
    if flag == '0':
        add = additems(user, product_id, stores, detail, user_trolley)
        return JsonResponse({"data": add.productnum, "totalPrice": add.productprice, "status": "success"})
    # 减少商品1/
    elif flag == '1':
        try:
            sub = subitems(product_id, user_trolley, detail)
            return JsonResponse({"data": sub.productnum, "totalPrice": sub.productprice, "status": "success"})
        except Trolley.DoesNotExist as e:
            print("购物车是空")
            return JsonResponse({"data": 0, "status": "error"})
        except AttributeError as a:
            print("购物车物品数量为0")
            return JsonResponse({"data": 0, "status": "error"})
    # 单选购物车商品
    elif flag == '2':
        chosen_item = Trolley.objects.filter(userAccount=user.userAccount).get(productid=product_id)
        chosen_item.isChose = not chosen_item.isChose
        chosen_item.save()
        choose = ''
        if chosen_item.isChose:
            choose = '√'
        return JsonResponse({"status": "success", "data": choose})
    # 全选购物车商品
    elif flag == '3':
        all_goods = Trolley.objects.filter(userAccount=user.userAccount).all()
        print("所有购物车商品：", all_goods)
        # 传入购物车所有商品
        return JsonResponse({"status": "success", "data": all_goods})


def additems(user, product_id, stores, detail, user_trolley):
    try:
        # 尝试拉取用户购物车数据
        find = user_trolley.get(productid=product_id)
        # 判断库存数量是否大于购物车对应商品数量
        if stores - find.productnum > 0:
            print("库存大于加入数量", find.productprice)
            find.productnum += 1
            find.productprice += round(detail.price * 1, 2)  # 数量加一之后总价等于当前购物车价格加上添加的数量*单价
            find.save()
        else:
            print("库存比数量还少了")
            pass
    except Trolley.DoesNotExist as e:
        # 购物车找不到对应商品
        find = Trolley.createtrolley(user.userAccount, product_id, 1, detail.price, True, detail.productimg,
                                     detail.productlongname, False)
        find.save()
    return find


def subitems(product_id, user_trolley, detail):
    # 在数据库拉取用户购物车信息
    find = user_trolley.get(productid=product_id)
    if find.productnum > 0:
        find.productnum -= 1
        find.productprice -= round(detail.price * 1, 2)  # 数量减一之后，总价等于当前总商品价格减去添加的数量*单价
        if find.productnum == 0:
            find.delete()
        else:
            find.save()
        return find
    # 如果数量等于0了购物车商品要删除，否则保存数据到购物车
    else:
        find.delete()
        find.save()


# 提交订单
def submitorder(request):
    token = request.session.get("userToken")
    user = User.objects.get(userToken=token)
    user_Trolley = Trolley.objects.filter(userAccount=user.userAccount)
    total_price = 0
    item_list_to_order = []
    for item_info in user_Trolley:
        if item_info.isChose:
            # 总价
            total_price += item_info.productnum * item_info.productprice
            # print(生成用户订单)
            orderid = ''.join(random.sample(string.ascii_letters + string.digits, 8)) \
                      + time.strftime("%Y%m%d%H%M", time.localtime())
            # 将选中的集合
            item_list_to_order.append(Order.createorder(orderid=orderid, userid=user.userAccount, progress=0))
            # 将购物车对应物品删除，无需物理删除，因为日后可能还要查看记录
            item_info.isDelete = True
            item_info.save()
    # 将所有订单全部加入订单记录
    Order.objects.bulk_create(item_list_to_order)
    print("总价：", total_price)
    return JsonResponse({"status": "success", "data": total_price})




