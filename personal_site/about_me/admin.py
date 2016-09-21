from django.contrib import admin

from about_me.models import Project, Technology


class TechnologyAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Project, ProjectAdmin)
