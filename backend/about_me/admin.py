from django.contrib import admin

from about_me.models import Project, ProjectLink, Technology


class TechnologyAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


class ProjectLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProjectLink, ProjectLinkAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Project, ProjectAdmin)
