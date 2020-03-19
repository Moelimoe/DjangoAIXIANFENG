from django.db import models


# Create your models here.


class ItemsManager(models.Manager):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    track_id = models.CharField(max_length=20)
    isDelete = models.BooleanField(null=True)

    # 用于重写查询方法
    def getqueryset(self):
        # super(StudentsManager, self).get_queryset()就是原始查询集，filter过滤后就是把isDelete是False的留下
        return super(ItemsManager, self).get_queryset()

    # def alterAttribution(self, img, name, track_id, isDelete):
    #     attr = self.model()
    #     attr.img = img
    #     attr.name = name
    #     attr.track_id = track_id
    #     attr.isDelete = isDelete


class Wheel(models.Model):
    objects = ItemsManager()
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    track_id = models.CharField(max_length=20)
    isDelete = models.BooleanField(null=True)


class Navigator(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    track_id = models.CharField(max_length=20)
    isDelete = models.BooleanField(null=True)


class MustBuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    track_id = models.CharField(max_length=20)
    isDelete = models.BooleanField(null=True)


class Commodity(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    track_id = models.CharField(max_length=20)
    isDelete = models.BooleanField(null=True)


class GoodsOnSale(models.Model):
    track_id = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=50)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=50)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=50)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)


# 分类模型
class GoodsTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)


# 商品模型类
class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=150)
    # 商品名称
    productname = models.CharField(max_length=50)
    # 商品长名称
    productlongname = models.CharField(max_length=100)
    # 是否精选
    isxf = models.NullBooleanField(default=False)
    # 是否买一赠一
    pmdesc = models.CharField(max_length=10)
    # 规格
    specifics = models.CharField(max_length=20)
    # 价格
    price = models.FloatField(max_length=10)
    # 超市价格
    marketprice = models.FloatField(max_length=10)
    # 组id
    categoryid = models.CharField(max_length=10)
    # 子类组id
    childcid = models.CharField(max_length=10)
    # 子类组名称
    childcidname = models.CharField(max_length=10)
    # 详情页id
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()


# 用户模型类
class User(models.Model):
    # 用户账号，要唯一
    userAccount = models.CharField(max_length=20, unique=True)
    # 密码
    userPassword = models.CharField(max_length=20)
    # 昵称
    userName = models.CharField(max_length=20)
    # 手机号
    userPhone = models.CharField(max_length=20)
    # 地址
    userAddress = models.CharField(max_length=100)
    # 头像路径
    userImg = models.CharField(max_length=150)
    # 等级
    userRank = models.IntegerField()
    # token验证值，每次登陆之后都会更新
    userToken = models.CharField(max_length=50)

    @classmethod
    def createuser(cls, account, password, name, phone, address, img, rank, token):
        u = cls(userAccount=account, userPassword=password, userName=name, userPhone=phone, userAddress=address,
                userImg=img, userRank=rank, userToken=token)
        return u


class TrolleyManager1(models.Manager):
    def get_queryset(self):
        return super(TrolleyManager1, self).get_queryset().filter(isDelete=False)


class TrolleyManager2(models.Manager):
    def get_queryset(self):
        return super(TrolleyManager2, self).get_queryset().filter(isDelete=True)


class Trolley(models.Model):
    userAccount = models.CharField(max_length=20)
    productid = models.CharField(max_length=10)
    productnum = models.IntegerField()
    productprice = models.CharField(max_length=10)
    isChose = models.BooleanField(default=True)
    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=100)
    orderid = models.CharField(max_length=20, default="0")
    isDelete = models.BooleanField(default=False)
    objects = TrolleyManager1()
    obj2 = TrolleyManager2()

    @classmethod
    def createtrolley(cls, userAccount, productid, productnum, productprice, isChose, productimg, productname, isDelete):
        c = cls(userAccount=userAccount, productid=productid, productnum=productnum, productprice=productprice,
                isChose=isChose, productimg=productimg, productname=productname, isDelete=isDelete)
        return c


class Order(models.Model):
    orderid = models.CharField(max_length=20)
    userid = models.CharField(max_length=20)
    progress = models.IntegerField()

    @classmethod
    def createorder(cls, orderid, userid, progress):
        o = cls(orderid=orderid, userid=userid, progress=progress)
        return o
