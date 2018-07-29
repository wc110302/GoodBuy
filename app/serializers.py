from rest_framework import serializers
from app.models import Goods, HistoryPrice, Comments


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ['id', 'name', 'c_price', 'image',
                  'description', 'comments_amount',
                  'sales_number', 'source',
                  'subclassification_id', 'brand_id']


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoryPrice
        fields = ['id', 'price', 'date', 'good']


class CommentsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(allow_null=True)
    goods_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Comments
        fields = ['id', 'content', 'score', 'image', 'create_time', 'user_id', 'goods_id']

    def to_representation(self, instance):

        data = super().to_representation(instance)
        try:
            data['c_username'] = instance.user.username
            data['c_icon'] = instance.user.icon
            data['stars'] = 'star%s' % instance.score
        except Exception as e:
            data['c_username'] = ''
            data['c_icon'] = ''
        return data
