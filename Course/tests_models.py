from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Topic, Course, Chapter, UserTakeCourse
from User.models import User

class TopicModelTestCase(TestCase):
    def test_create_valid_topic(self):
        topic = Topic(topic_name="Valid Topic")
        topic.full_clean()
        topic.save()
        self.assertEqual(Topic.objects.count(), 1)

    def test_create_duplicate_topic(self):
        topic = Topic(topic_name="Duplicate Topic")
        topic.full_clean()
        topic.save()

        duplicate_topic = Topic(topic_name="Duplicate Topic")
        with self.assertRaises(ValidationError):
            duplicate_topic.full_clean()

    def test_create_topic_no_name(self):
        topic = Topic(topic_name="")
        with self.assertRaises(ValidationError):
            topic.full_clean()
    

class CourseModelTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(topic_name="Test Topic")
        self.author = User.objects.create(username="testauthor", email="testauthor@example.com", password="testpassword")

    def test_create_valid_course(self):
        course = Course(
            author=self.author,
            topic=self.topic,
            tittle="Valid Course",
            description="A valid course",
            calification=4,
            number_of_chapters=5
        )
        course.full_clean()
        course.save()
        self.assertEqual(Course.objects.count(), 1)

    def test_create_course_with_invalid_calification(self):
        course = Course(
            author=self.author,
            topic=self.topic,
            tittle="Invalid Course",
            description="An invalid course",
            calification=7,
            number_of_chapters=5
        )
        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_create_course_no_title(self):
        course = Course(
            author=self.author,
            topic=self.topic,
            description="A course with no title",
            calification=4,
            number_of_chapters=5
        )
        with self.assertRaises(ValidationError):
            course.full_clean()  

    def test_set_number_of_chapters(self):
        course = Course(
            author=self.author,
            topic=self.topic,
            tittle="Course with Chapters",
            description="A course with chapters",
            calification=4,
            number_of_chapters=0
        )
        course.save()

        for i in range(5):
            Chapter.objects.create(course=course, tittle=f"Chapter {i}", content=f"Content for Chapter {i}", number_of_chapter=i)

        course.set_number_of_chapters()
        self.assertEqual(course.number_of_chapters, 5)

    def test_set_calification(self):
        course = Course(
            author=self.author,
            topic=self.topic,
            tittle="Course with Ratings",
            description="A course with ratings",
            calification=0,
            number_of_chapters=5
        )
        course.save()

        for i in range(5):
            UserTakeCourse.objects.create(user=self.author, course=course, number_of_chapter=1, calification=i + 1)

        course.set_calification()
        self.assertEqual(course.calification, 3.0)


class ChapterModelTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(topic_name="Test Topic")
        self.author = User.objects.create(username="testauthor", email="testauthor@example.com", password="testpassword")
        self.course = Course.objects.create(author=self.author, topic=self.topic, tittle="Test Course", description="Test Description", calification=4, number_of_chapters=0)

    def test_create_valid_chapter(self):
        chapter = Chapter(
            course=self.course,
            tittle="Valid Chapter",
            content="Valid chapter content",
            number_of_chapter=1
        )
        chapter.full_clean()
        chapter.save()
        self.assertEqual(Chapter.objects.count(), 1)

    def test_create_chapter_with_no_title(self):
        chapter = Chapter(
            course=self.course,
            content="Chapter with no title",
            number_of_chapter=2
        )
        with self.assertRaises(ValidationError):
            chapter.full_clean()

    def test_create_chapter_with_duplicate_title_in_same_course(self):
        chapter1 = Chapter(
            course=self.course,
            tittle="Chapter Title",
            content="Chapter content 1",
            number_of_chapter=3
        )
        chapter1.save()

        chapter2 = Chapter(
            course=self.course,
            tittle="Chapter Title",
            content="Chapter content 2",
            number_of_chapter=4
        )
        with self.assertRaises(ValidationError):
            chapter2.full_clean()