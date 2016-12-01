import os

from django.test import Client, TestCase
from django.urls import reverse

from about_me.models import Project, Technology


class ProjectsAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.projects_url = reverse('projects-api:projects-list')
        cls.technology_url = reverse('tech-api:technology-list')

    def test_technology_list_is_displayed(self):

        d1 = dict(name='unittest',
                  general_description='Python unit-testing framework',
                  mastery_level=Technology.INTERMEDIATE)

        d2 = dict(name='pytest',
                  general_description='Python unit-testing framework on steroids',
                  mastery_level=Technology.NOVICE)

        Technology.objects.create(**d1)
        Technology.objects.create(**d2)

        resp = self.client.get(self.technology_url)

        self.assertEqual(len(resp.data), 2)
        self.assertEqual(resp.data[0], d1)
        self.assertEqual(resp.data[1], d2)

    def test_project_list_is_displayed(self):

        d1 = dict(name='unittest',
                  general_description='Python unit-testing framework',
                  mastery_level=Technology.INTERMEDIATE)

        d2 = dict(name='pytest',
                  general_description='Python unit-testing framework on steroids',
                  mastery_level=Technology.NOVICE)

        t1 = Technology.objects.create(**d1)
        t2 = Technology.objects.create(**d2)
        p = Project.objects.create(title='MySuperProject',
                                   description='TBD')
        p.technologies = [t1, t2]
        p.save()
        resp = self.client.get(self.projects_url)

        self.assertEqual(len(resp.data), 1)

        project = resp.data[0]
        self.assertEqual(project['title'], 'MySuperProject')
        self.assertEqual(project['description'], 'TBD')
        self.assertIn("technologies", project)
        self.assertEqual(len(project['technologies']), 2)

        self.assertEqual(project['technologies'][0]['name'], "unittest")
        self.assertEqual(project['technologies'][1]['name'], "pytest")
