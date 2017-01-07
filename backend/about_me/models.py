from django.db import models


class Technology(models.Model):
    """Model, representing single technology or skill"""

    class Meta:
        verbose_name_plural = 'technologies'

    NOVICE = 1
    INTERMEDIATE = 2
    ADVANCED = 3

    MASTERY_CHOICES = (
        (NOVICE, 'Novice'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced')
    )

    name = models.CharField(max_length=120)
    general_description = models.TextField()
    mastery_level = models.IntegerField(choices=MASTERY_CHOICES,
                                        default=NOVICE)

    def __str__(self):
        return '<Skill: "{}">'.format(self.name)


class Project(models.Model):
    """Model, representing single project,
    with a list of technologies used and appropriate
    links
    """
    title = models.CharField(max_length=200)
    description = models.TextField()

    technologies = models.ManyToManyField(Technology)

    def __str__(self):
        return '<Project "{}"'.format(self.title)


class ProjectLink(models.Model):
    """Model, representing single link of the project"""
    link = models.URLField()
    name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='links')

    def __str__(self):
        return '<Project: {} - {}>'.format(self.project, self.link)
