from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

# Model Serializer

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        excluse = ('watchlist', )
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
# Costom Serializers
#     len_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
# Costom Serializers
#     len_name = serializers.SerializerMethodField()
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"



#     def get_len_name(self, object):
#         length = len(object.name)
#         return length
#
#     def validate(self, data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("title and description cannot be the same!")
#         return data
#
#     def validate_name(self, value):
#         if(len(value)<2):
#             raise serializers.ValidationError("Name is too small!")
#         else:
#             return value

# def name_length(value):
#     if(len(value)<2):
#         raise serializers.ValidationError("Name is too small!")
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
# # Object level validators
#     def validate(self, data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("title and description cannot be the same!")
#         return data

# Field level validators

#     def validate_name(self, value):
#         if(len(value)<2):
#             raise serializers.ValidationError("Name is too small!")
#         else:
#             return value