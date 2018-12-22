from django.db import models
import time


# Create your models here.

#============================================================================

class Article(models.Model):
    title = models.CharField(max_length=64, verbose_name="标题")
    summary = models.CharField(max_length=255, verbose_name="摘要")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    create_date = models.DateField(db_index=True, auto_now_add=True, verbose_name="创建日期")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    count_comment = models.IntegerField(default=0, verbose_name="评论数")
    count_up = models.IntegerField(default=0, verbose_name="点赞数")
    count_down = models.IntegerField(default=0, verbose_name="被踩数")
    author_name = models.ForeignKey(to="Author", to_field="author_name", null=True, on_delete=models.SET_NULL, verbose_name="作者名")
    category = models.ForeignKey(to="Category", null=True, on_delete=models.CASCADE, verbose_name="分类")
    count_read = models.IntegerField(default=0, verbose_name="阅读量")
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2tag",
        through_fields=("article", "tag"),
    )

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    is_delete = models.IntegerField(default=0, verbose_name="是否逻辑删除")

    class Meta:
        db_table = "s-articles"
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class ArticleDetail(models.Model):
    content = models.TextField()
    article = models.OneToOneField(to="Article", on_delete=models.CASCADE)

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = "s-article_detail"
        verbose_name = "文章细节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article.title

class Comment(models.Model):
    comment = models.CharField(max_length=255, unique=True, verbose_name="评论内容")
    ip_addr = models.CharField(max_length=20, verbose_name="评论时ip地址")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    user = models.ForeignKey(to="User")

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = "s-comment"
        verbose_name = "评论"
        verbose_name_plural = verbose_name

class User(models.Model):
    user_name = models.CharField(max_length=64, unique=True, verbose_name="用户名")
    account = models.CharField(max_length=64, unique=True, verbose_name="账号")
    password = models.CharField(max_length=64, verbose_name="密码")
    ip_addr = models.CharField(max_length=20, verbose_name="登录地ip")
    token = models.CharField(max_length=100, null=True, verbose_name="令牌")
    is_blocked = models.IntegerField(default=0, verbose_name="是否被封号")
    is_delete = models.IntegerField(default=0, verbose_name="是否逻辑删除")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建日期")
    update_time = models.DateField(auto_now=True, verbose_name="更新时间")


    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = "s-user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

class UporDown(models.Model):
    status = models.IntegerField(default=0, verbose_name="赞/踩")
    user = models.ForeignKey(to="User",)
    article = models.ForeignKey(to="Article",)

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        unique_together = (("user", "article"),)
        db_table = "s-upordown"
        verbose_name = "赞/踩"
        verbose_name_plural = verbose_name

class Author(models.Model):
    author_name = models.CharField(max_length=64, db_index=True, unique=True, verbose_name="作者名")
    account = models.CharField(max_length=64, verbose_name="账号")
    password = models.CharField(max_length=64, verbose_name="密码")

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = "s-author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=64, verbose_name="标签名")

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = "s-tag"
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name

class Article2tag(models.Model):
    article = models.ForeignKey(to="Article")
    tag = models.ForeignKey(to="Tag")

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        unique_together = (("article", "tag"),)
        db_table = "s-article_2_tag"
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "文章:{} ,标签:{}".format(self.article.title ,self.tag.tag_name)

class Category(models.Model):

    title = models.CharField(max_length=32, verbose_name="分类", unique=True)  # 分类标题

    back_up01 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up02 = models.CharField(max_length=255, null=True, blank=True, default=None)
    back_up03 = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = "s-category"
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title