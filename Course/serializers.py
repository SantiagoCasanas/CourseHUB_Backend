from rest_framework import serializers
from .models import Topic, Course, Chapter, User_take_Course


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic_name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'author', 'topic', 'tittle', 'description', 'calification']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.topic = validated_data.get('topic', instance.topic)
        instance.tittle = validated_data.get('tittle', instance.tittle)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UserTakeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_take_Course
        fields = ['id', 'user', 'course', 'number_of_chapter', 'calification']

    def create(self, validated_data):
        return User_take_Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.calification = validated_data.get('calification', instance.calification)
        instance.save()
        return instance


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'course', 'tittle', 'content', 'number_of_chapter']

    def create(self, validated_data):
        return Chapter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tittle = validated_data.get('tittle', instance.tittle)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
