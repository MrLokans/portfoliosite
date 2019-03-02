from django.db import models
from django.db.models import Case, When, Value, CharField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable


class TechnologyManager(models.Manager):
    def get_queryset(self):
        # Yes, this could have been done in a more simple
        # manner, I just wanted to play around with model managers
        return (
            super()
            .get_queryset()
            .annotate(
                mastery_description=Case(
                    When(mastery_level=self.model.NOVICE, then=Value("Novice")),
                    When(
                        mastery_level=self.model.INTERMEDIATE,
                        then=Value("Intermediate"),
                    ),
                    When(mastery_level=self.model.ADVANCED, then=Value("Advanced")),
                    default=Value("Unspecified"),
                    output_field=CharField(),
                )
            )
            .order_by("-mastery_level")
        )


class ProjectQuerySet(models.QuerySet):
    def fully_joined(self):
        return self.prefetch_related("links").prefetch_related("technologies")


class Technology(models.Model):
    """Model, representing single technology or skill"""

    class Meta:
        verbose_name_plural = "technologies"

    NOVICE = 1
    INTERMEDIATE = 2
    ADVANCED = 3

    MASTERY_CHOICES = (
        (NOVICE, "Novice"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    name = models.CharField(max_length=120)
    general_description = models.TextField()
    mastery_level = models.IntegerField(choices=MASTERY_CHOICES, default=NOVICE)

    objects = TechnologyManager()

    def __str__(self):
        return '<Skill: "{}">'.format(self.name)


class Project(models.Model):
    """Model, representing single project,
    with a list of technologies used and appropriate
    links
    """

    OPEN_SOURCE = 1
    VOLUNTEER = 2
    ENTERPRISE = 3

    PROJECT_TYPE_CHOICES = (
        (OPEN_SOURCE, "open_source"),
        (VOLUNTEER, "volunteer"),
        (ENTERPRISE, "enterprise"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.PositiveIntegerField(
        choices=PROJECT_TYPE_CHOICES, blank=True, null=True
    )
    technologies = models.ManyToManyField(Technology)

    objects = ProjectQuerySet.as_manager()

    def __str__(self):
        return '<Project "{}"'.format(self.title)


class ProjectLink(models.Model):
    """Model, representing single link of the project"""

    link = models.URLField()
    name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return "<Project: {} - {}>".format(self.project, self.link)


class ConferenceTalkPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
        InlinePanel("video_links", label="Video links"),
    ]


class ConferenceVideoLink(Orderable):
    page = ParentalKey(
        ConferenceTalkPage, on_delete=models.CASCADE, related_name="video_links"
    )
    short_description = models.TextField()
    video_url = models.URLField()
    presentation_url = models.URLField()

    panels = [
        FieldPanel("short_description"),
        FieldPanel("video_url"),
        FieldPanel("presentation_url"),
    ]
