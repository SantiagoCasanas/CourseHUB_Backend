from django.contrib import admin
from Course.models import Course, Topic, UserTakeCourse, Chapter

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(UserTakeCourse)
admin.site.register(Chapter)
