from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CourseSerializer, TopicSerializer, UserTakeCourseSerializer, ChapterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Course, Topic, Chapter, UserTakeCourse


class CustomListCreateCourseView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tittle', 'topic', 'calification']
    ordering_fields = ['calification', 'number_of_chapters']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

class CreateTopic(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAdminUser]

class ListTopic(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['topic_name']
    ordering_fields = ['topic_name']
    permission_classes = [permissions.IsAuthenticated]

class CreateChapter(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]

class User_take_Course(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = UserTakeCourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateUserTakeCourse(generics.UpdateAPIView):
    queryset = UserTakeCourse.objects.all()
    serializer_class = UserTakeCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.request.data.get('user')
        course_id = self.request.data.get('course')
        course = Course.objects.get(pk=course_id)
        course.set_calification()
        course.save()
        return self.queryset.get(user_id=user_id, course_id=course_id)
