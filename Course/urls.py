from django.urls import path
from .views import CustomListCreateCourseView, CreateTopic, CreateChapter, User_take_Course, UpdateUserTakeCourse

urlpatterns = [
    path('create_list_course/', CustomListCreateCourseView.as_view(), name='custom-course-list-create'),
    path('create_topic/', CreateTopic.as_view(), name='create-topic-view'),
    path('create_chapter/', CreateChapter.as_view(), name='create_chapter'),
    path('user_take_course/', User_take_Course.as_view(), name='user_take_course'),
    path('rate_course/', UpdateUserTakeCourse.as_view(), name='update_user_take_course'),
]