from django.urls import path
from .views import CustomListCreateCourseView, CreateTopic

urlpatterns = [
    path('create_list_course/', CustomListCreateCourseView.as_view(), name='custom-course-list-create'),
    path('create_topic/', CreateTopic.as_view(), name='create-topic-view')
]