from django.test import TestCase
from django.urls import reverse

from .models import Project, Technology


class ProjectsAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.projects_url = reverse('about_me:projects-list')
        cls.technology_url = reverse('about_me:technology-list')

    def _get_technologies_count(self):
        return Technology.objects.count()

    def _get_projects_count(self):
        return Project.objects.count()

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
        self.assertEqual(len(resp.data['results']),
                         self._get_technologies_count())
        self.assertEqual(resp.data['results'][0], d1)
        self.assertEqual(resp.data['results'][1], d2)

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
        p.technologies.set([t1, t2])
        p.save()
        resp = self.client.get(self.projects_url)

        self.assertEqual(len(resp.data['results']), 1)

        project = resp.data['results'][0]
        self.assertEqual(project['title'], 'MySuperProject')
        self.assertEqual(project['description'], 'TBD')
        self.assertIn("technologies", project)
        self.assertEqual(len(project['technologies']), 2)

        self.assertEqual(project['technologies'][0]['name'], "unittest")
        self.assertEqual(project['technologies'][1]['name'], "pytest")
