from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "summary", "category",
                  "create_time", "update_time", "count_comment",
                  "count_up", "count_down", "author_name", "count_read", "tags"]

    category = serializers.CharField(source="category.title")
    tags = serializers.SerializerMethodField()
    def get_tags(self, obj):
        res = Tag.objects.filter(article__title=obj)
        res_list = []
        for i in res:
            res_list.append({"tag_id":i.pk, "tag_name": i.tag_name})
        return res_list

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["pk", "create_date", "title"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["pk", "tag_name"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_name", "account", 'password', 'ip_addr', 'token', 'is_blocked', 'is_delete']


class UporDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = UporDown
        fields = ["status", "user", "article"]