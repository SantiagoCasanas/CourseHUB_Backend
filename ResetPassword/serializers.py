from rest_framework import serializers

class GetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()