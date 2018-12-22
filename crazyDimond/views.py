from rest_framework import viewsets
from .models import *
from .serilizers import *
from rest_framework.views import APIView
from rest_framework.views import Response
from .extra import Reserializer
from .extra import UserInfoVerification
from .paginations import FilePagination
from rest_framework.decorators import action
from crazyDimond.task import sendMail
from .authenticators import LoginAuthticator
from .authenticators import Up2Down


# Create your views here.


class Articles(viewsets.ModelViewSet):

    @action(methods=["get"], detail=False)
    def retrieve(self, request, *args, **kwargs):
        aid = request.path.split("/")[2]
        res = {"code": -1}
        if aid.isdigit():
            content_set = Article.objects.select_related("articledetail").filter(pk=aid).first()
            if content_set:
                category_id = Category.objects.filter(article__pk=aid).first().pk
                article_set = Article.objects.filter(pk=aid).first()
                article_set.count_read += 1
                article_set.save()
                content = content_set.articledetail.content
                article = ArticleSerializer(article_set, many=False)
                res = article.data
                res["category_id"] = category_id
                res["content"] = content
                return Response(res)
        return Response(res)


class Categories(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Files(viewsets.ModelViewSet):
    """
    归档
    """
    pagination_class = FilePagination

    def list(self, request, *args, **kwargs):
        # total_article = Article.objects.count()
        # if total_article > 5:
        #     total_article += 1
        # date_group_set = Article.objects.all().values("pk", "title", "create_date").order_by("-create_date")[1:total_article]
        # date_group = FileSerializer(date_group_set, many=True).data
        # res = Reserializer(date_group).fileReserializer()
        # return Response(res)

        date_group_set = Article.objects.all().values("pk", "title", "create_date").order_by("-create_date", "pk")
        fp = FilePagination()
        temp_set = fp.paginate_queryset(date_group_set, request)
        date_group = FileSerializer(temp_set, many=True).data
        year_group = FileSerializer(date_group_set, many=True).data
        years = list(set(year.split("-")[0] for year in [years.get("create_date") for years in year_group]))
        res = Reserializer(date_group).fileReserializer(years)
        return fp.get_paginated_response(res)
        # 生成的上一页/下一页链接要加apis/不然不走接口


class Tags(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class Cat4Art(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        get_type = request.path.split("/")[3]
        aid = request.path.split("/")[4]
        if aid.isdigit() and get_type in ["cat4art", "tag4art"]:
            if get_type == "cat4art":
                category_set = Category.objects.filter(pk=aid).first()
                item_name = CategorySerializer(category_set, many=False)
                flag = True
                article_set = Article.objects.filter(category_id=aid).values("pk", "title", "create_date").order_by("-create_date", "pk")
            else:
                tag_set = Tag.objects.filter(pk=aid).first()
                item_name = TagSerializer(tag_set, many=False)
                flag = False
                article_set = Article.objects.filter(article2tag__tag__pk=aid).values("pk", "title", "create_date").order_by("-create_date", "pk")
            fp = FilePagination()
            temp_set = fp.paginate_queryset(article_set, request)
            article_group = FileSerializer(temp_set, many=True).data
            res = Reserializer(article_group).cat4ArtReserializer(item_name.data, flag=flag)
            if len(res) != 0:
                return fp.get_paginated_response(res)
        return Response({"code": -1})


class TagsAndCats(viewsets.ModelViewSet):
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        tags = Tag.objects.count()
        cats = Category.objects.count()
        res = Reserializer.tagAndCatReserializer(catnum=cats, tagnum=tags)
        return Response(res)


class UserSubmit(APIView):

    def post(self, request, *args, **kwargs):
        """
        邮箱验证成功, 然后才.save()
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_name = request.data.get("username")
        account = request.data.get("email")
        ip_addr = request.META.get("REMOTE_ADDR")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        auth_code = request.data.get("authcode")
        u = UserInfoVerification(user_name=user_name,account=account,password=password,
                                   authcode=auth_code, confirm_pass=confirm_password, ip_addr=ip_addr)
        res = u.verify() # 返回user对象或错误信息
        if hasattr(res, "save"):
            res.save()
            return Response({})
        else:
            return Response(res)


class SendMail(APIView):
    def get(self, request):
        email = request.GET.get("email")
        sendMail.delay(email)
        return Response({"msg": "1"})


class UserLogin(APIView):
    authentication_classes = [LoginAuthticator]

    def post(self, request):
        username = request.user.user_name
        token = request.auth
        # res = Response({"username": username})
        # res.set_cookie("username", username)
        """
        本意：
            通过写一个叫username的cookie， 在点赞或评论的时候
            就能找到是哪个用户进行的操作。
        问题：
            这样不安全， 可以通过修改cookie来伪造身份
        解决：
            写到session里
        """
        res = Response({"username": username})
        res.set_cookie("token", token)
        res.set_cookie("username", username)
        return res

class UpDown(viewsets.ModelViewSet):
    """
    根据login设置的cookie(token),在进行操作时验证浏览器的token和数据库的token是否一致
    没有token: 未登录
    有token:
        先去cache中验证, 失败再去mysql中验证, 再失败就说明存在异常登录
        此版本先当作未登录处理, 后续版本再进行优化
        cookie ---> token
        session ---> account && username
        cache ---> {account: token}

        cookie的token和cache中的token比对
        session的username用来确定哪个用户进行的操作
        session的account用来给cache找token
    """
    authentication_classes = [Up2Down]
    queryset = Article.objects.all()

    @action(methods=["patch"], detail=True)
    def partial_update(self, request, *args, **kwargs):
        article = self.get_object()
        if request.data.get("data"):
            article.count_up += 1
            status = 1
        else:
            article.count_down += 1
            status = 0
        # print(article)
        # print(request.user)
        try:
            uod = UporDown.objects.create(status=status, user=request.user, article=article)
            uod.save()
        except Exception as e:
            return Response({"code": 0})
        else:
            article.save()
        return Response({"code": 1})
