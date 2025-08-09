from rest_framework import serializers


class TechniquePreviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    names = serializers.DictField(child=serializers.CharField(), allow_empty=True)
    category = serializers.CharField()
    min_belt = serializers.IntegerField()


class TulPreviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    belt = serializers.IntegerField()


class SearchResponseSerializer(serializers.Serializer):
    results = serializers.ListField(child=serializers.DictField())

