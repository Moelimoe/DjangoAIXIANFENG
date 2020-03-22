import os, random, time, string, io
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Wheel, Navigator, MustBuy, Commodity, GoodsOnSale, GoodsTypes, Goods, User, Trolley, Order
# from project import settings
from django.conf import settings
from .forms.login import LoginForm
from PIL import Image, ImageDraw, ImageFont


# Create your views here


# 测试页
def testpage(request, s1, d1, d2, d3):
    verify_msg = ''
    _captcha_submit = request.POST.get('verify_code').lower()
    # 注意这里提交的code需要小写，而服务器的code已经小写，这样分开做是为了避免当验证码过期了变为空值取不到session抛出异常
    _captcha_server = request.session.get('verify_code')
    if _captcha_server == _captcha_submit:
        return render(request, 'axf/test.html', {"msg": "验证成功"})
    else:
        verify_msg = '验证失败'
    return render(request, 'axf/test.html', {"msg": verify_msg, "名称": s1})


# 重定义字典方法，用于模板中
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


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
                                             "mustBuyList": mustBuyList, 'commodity1': commodity1,
                                             'commodity2': commodity2,
                                             'commodity3': commodity3, 'commodity4': commodity4, "mainList": mainList})


# 个人资料
def profile(request):
    print("进入profile验证userToken", request.session.get('userToken'))
    try:
        # 从服务器获取对应的user信息，自动登录
        token = request.session.get('userToken')
        user = User.objects.get(userToken=token)
        userName = user.userName
        userLevel = user.userLevel
        userProfile = user.userAccount + user.userImg
        # print(userProfile)
        return render(request, 'axf/profile.html', {"title": "我的", "userName": userName, "userLevel": userLevel,
                                                    'userProfile': userProfile})
    except User.DoesNotExist as e:
        return render(request, 'axf/profile.html', {"title": "我的"})


# 登录
def login(request):
    err_msg = ''
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            user = f.cleaned_data["username"]
            password = f.cleaned_data["password"]
            # 验证码进行比对，服务端的小写化再存入session时已执行
            captcha_submit = request.POST.get('verify_code').lower()
            captcha_server = request.session.get('verify_code')
            print(captcha_submit, captcha_server)
            if captcha_server == captcha_submit:
                try:
                    getuser = User.objects.get(userAccount=user, userPassword=password)
                    userName = getuser.userName
                    userLevel = getuser.userLevel
                    userProfile = getuser.userAccount + getuser.userImg
                    print("获取用户头像：", userProfile)
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


#  生成验证码，# 可以直接可以在html中的img引用
def captcha(request):
    # 定义背景颜色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    width = 100
    height = 50

    # 创建画面对象
    img = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(img)
    # 调用画笔的point()函数绘制验证码的干扰点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), 55)
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    _str = string.digits + string.ascii_letters
    # 随机取四个值作为验证码
    rand_codes = ''.join(random.sample(_str, 4))
    # 定义字体大小
    size = int(min(width / len(rand_codes), height))
    # 构造字体对象
    font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', size)
    # 构造字体颜色,四个字颜色不同
    for i in range(4):
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((i * 25, 2), rand_codes[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # # 将验证码缓存入session，后面做进一步验证，注意应该在这里存入的时候变为小写，
    # 否则验证码过期就变成了空，再进行lower()操作会抛出异常
    request.session['verify_code'] = rand_codes.lower()
    # 验证码有效时间60秒
    request.session.set_expiry(60)
    print("生成的验证码是：", rand_codes)
    print("它应该是与session存的验证码一样：", request.session['verify_code'])
    buf = io.BytesIO()
    img.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为png图片
    return HttpResponse(buf.getvalue(), 'image/jpg')
    # 这样也行
    # return HttpResponse(buf.getvalue(), 'jpg')


# 登出1
# 退出登录使用logout(request)，如果函数命名为logout()，则两则会冲突返回错误Maximum recursion depth exceeded
def signout(request):
    # logout冲突报错maximum recursion depth exceeded
    logout(request)
    return redirect('/profile/')


# 登出2
def logout(request):
    request.session.clear()
    return render(request, 'axf/profile.html')


# 注册
def register(request):
    register_failed = False
    if request.POST:
        try:
            userAccount = request.POST.get('userAccount')
            userPassword = request.POST.get('userPass')
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
                # 不使用.chunk()一块块传也没问题
                for info in userImg:
                    fp.write(info)
            userRegister = User.createuser(userAccount, userPassword, userName, userPhone,
                                           userAddress, userImg, userLevel, userToken)
            userRegister.save()
            # 注册成功就导航到profile登录
            return redirect('/profile/')
        except Exception:
            register_failed = True
            return render(request, 'axf/register.html', {"title": "注册", 'register_failed': register_failed})
    return render(request, 'axf/register.html', {"title": "注册", 'register_failed': register_failed})


# 检测注册账户是否已存在
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
    return render(request, 'axf/mall.html', {"title": "商城", 'leftBar': leftBar, 'productList': productList,
                                             "childList": childList, "categoryid": categoryid, "cid": cid,
                                             "item_info_Trolley": item_info_Trolley})


# 重定向回mall
def mall_redirect(request):
    return redirect('/mall/104749/0/0/')


# 购物车
def trolley(request):
    token = request.session.get("userToken")
    if not token:
        return redirect('/login/')
    user = User.objects.get(userToken=token)
    trolleyList = Trolley.objects.filter(userAccount=user.userAccount)
    return render(request, 'axf/trolley.html', {"title": "购物车", "userName": user.userName, "userPhone": user.userPhone,
                                                "userAddress": user.userAddress, "trolleyList": trolleyList})


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
        print("增加商品", "商品价格", add.productprice, "商品数量", add.productnum)
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
        print(f"选择物品改变前{chosen_item.isChose}")
        chosen_item.isChose = not chosen_item.isChose
        print(f"选择物品改变后{chosen_item.isChose}")
        chosen_item.save()
        choose = ''
        if chosen_item.isChose:
            choose = '√'
        return JsonResponse({"status": "success", "data": choose})
    # 全选购物车商品
    # elif flag == '3':
    #     chooseall = Trolley.objects.filter(userAccount=user.userAccount).all()
    #     print(chooseall)
    #     # for item in chooseall:
    #
    #     # chosen_item.isChose = not chosen_item.isChose
    #     #
    #     # chosen_item.save()
    #     # if chosen_item.isChose:
    #     #     choose = '√'
    #     # else:
    #     #     choose = ''
    #     return JsonResponse({"status": "success", "data": '√'})


def additems(user, product_id, stores, detail, user_trolley):
    try:
        # 如果存在购物车走下面
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
        # 如果购物车找不到对应商品
        print("窗口购物车")
        find = Trolley.createtrolley(user.userAccount, product_id, 1, detail.price, True, detail.productimg,
                                     detail.productlongname, False)
        find.save()
    print("最后走到这", "product_id:", product_id)
    return find


def subitems(product_id, user_trolley, detail):
    # 试图寻找用户购物车信息
    find = user_trolley.get(productid=product_id)
    print("find找到了")
    if find.productnum > 0:
        find.productnum -= 1
        print("商品减少之前的价格", find.productprice)
        find.productprice -= round(detail.price * 1, 2)  # 数量减一之后，总价等于当前总商品价格减去添加的数量*单价
        print("商品减少之后的价格", find.productprice)
        if find.productnum == 0:
            print("变为0要删除数据")
            find.delete()
        else:
            find.save()
            print("find保存了")
        return find
    # 如果数量等于0了购物车商品要删除，否则保存数据到购物车
    else:
        print("find为", find.productnum, "要删除了")
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
            print(orderid)
            # 将选中的集合
            item_list_to_order.append(Order.createorder(orderid=orderid, userid=user.userAccount, progress=0))
            # 将购物车对应物品删除，无需物理删除，因为日后可能还要查看记录
            print("删除商品信息前", item_info.isDelete)
            item_info.isDelete = True
            print("删除商品信息后", item_info.isDelete)
            item_info.save()
    # 将所有订单全部加入订单记录
    Order.objects.bulk_create(item_list_to_order)
    print("总价：", total_price)
    return JsonResponse({"status": "success", "data": total_price})




