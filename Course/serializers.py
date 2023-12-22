from rest_framework import serializers
from .models import Topic, Course, Chapter, UserTakeCourse


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic_name']


class CourseSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'author', 'author_username', 'topic', 'tittle', 'description', 'calification', 'number_of_chapters']
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        return Course.objects.create(**validated_data)
    
    def get_author_username(self, obj):
        return obj.author.username if obj.author else None

    def update(self, instance, validated_data):
        instance.topic = validated_data.get('topic', instance.topic)
        instance.tittle = validated_data.get('tittle', instance.tittle)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UserTakeCourseSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    class Meta:
        model = UserTakeCourse
        fields = ['id', 'user', 'user_username','course','course_title', 'number_of_chapter', 'calification']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        return UserTakeCourse.objects.create(**validated_data)
    
    def get_user_username(self, obj):
        return obj.user.username if obj.user else None
    
    def get_course_title(self, obj):
        return obj.course.tittle if obj.course else None

    def update(self, instance, validated_data):
        instance.calification = validated_data.get('calification', instance.calification)
        instance.save()
        return instance


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'course', 'tittle', 'content', 'number_of_chapter']

    def create(self, validated_data):
        course = Course.objects.get(id=validated_data.get('course').id)
        number_of_chapter = course.number_of_chapters + 1
        instance = Chapter.objects.create(**validated_data, number_of_chapter=number_of_chapter)
        course.set_number_of_chapters()
        course.save()
        return instance
        

    def update(self, instance, validated_data):
        instance.tittle = validated_data.get('tittle', instance.tittle)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
