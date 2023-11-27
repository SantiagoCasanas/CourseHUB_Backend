from django.db import models
from statistics import mean
from User.models import User


class Topic(models.Model):
    topic_name = models.CharField('Topic', max_length=100, unique=True, null=False)

    def __str__(self):
        return self.topic_name


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    tittle = models.CharField('Tittle', max_length=200, unique=True, null=False)
    description = models.CharField('Description', max_length=200, null=False)
    calification = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    number_of_chapters =  models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tittle} - Rating: {self.calification}"

    def set_number_of_chapters(self):
        self.number_of_chapters = len(Chapter.objects.filter(course=self))
        self.save()
    
    def set_calification(self):
        ratings = UserTakeCourse.objects.filter(course=self)
        ratings_list = [rating.calification for rating in ratings if rating.calification != 0]
        ratings = mean(ratings_list)
        self.calification = ratings

    class Meta:
        ordering = ['calification']


class UserTakeCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Reader')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    number_of_chapter = models.IntegerField(default=0)
    calification = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    tittle = models.CharField('Tittle', max_length=200, null=False)
    content = models.TextField('Content', max_length=3750)
    number_of_chapter = models.PositiveIntegerField('Number of chapter', null=True)

    def __str__(self):
        return self.tittle
    
    class Meta:
        unique_together = ['course', 'tittle']
