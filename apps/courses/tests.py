from django.test import TestCase
from django.urls import reverse
from .models import Course, Category, Language

class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Category.objects.create(name='Programming', description='Courses related to programming')
        Language.objects.create(name='Python')
        cls.course = Course.objects.create(
            title='Django for Beginners',
            description='Learn Django',
            category=Category.objects.get(name='Programming'),
            language=Language.objects.get(name='Python'),
            start_date='2022-01-01',
            end_date='2022-03-01'
        )

    def test_course_content(self):
        course = Course.objects.get(id=1)
        self.assertEqual(f'{course.title}', 'Django for Beginners')
        self.assertEqual(f'{course.description}', 'Learn Django')
        self.assertEqual(course.category.name, 'Programming')
        self.assertEqual(course.language.name, 'Python')

class CourseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 10 courses for pagination tests
        number_of_courses = 10
        for course_num in range(number_of_courses):
            Course.objects.create(
                title=f'Course {course_num}',
                description=f'Description {course_num}',
                # Assume the existence of one category and one language for simplicity
                category=Category.objects.get(id=1),
                language=Language.objects.get(id=1),
                start_date='2022-01-01',
                end_date='2022-03-01'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['course_list']) == 10)

from .forms import CourseForm

class CourseFormTest(TestCase):
    def test_course_form_valid_data(self):
        form = CourseForm(data={
            'title': 'New Course',
            'description': 'A new course description',
            'category': 1,  # Assuming a category with ID 1 exists
            'language': 1,  # Assuming a language with ID 1 exists
            'start_date': '2023-01-01',
            'end_date': '2023-03-01',
        })
        self.assertTrue(form.is_valid())

    def test_course_form_invalid_data(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # Assuming all fields are required

class CourseCreateViewTest(TestCase):
    def test_course_create_view_get(self):
        response = self.client.get(reverse('courses:add_course'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Course')
        self.assertTemplateUsed(response, 'courses/add_course.html')

    def test_course_create_view_post(self):
        # Assuming a category with ID 1 and a language with ID 1 exist
        response = self.client.post(reverse('courses:add_course'), {
            'title': 'Test Course',
            'description': 'Test description',
            'category': 1,
            'language': 1,
            'start_date': '2023-01-01',
            'end_date': '2023-03-01',
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Course.objects.exists())
