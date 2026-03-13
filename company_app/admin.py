from django.contrib import admin

from company_app.models import WorkSpace, WorkSpaceUser, Project, Task
# Register your models here.
admin.site.register(WorkSpace)
admin.site.register(WorkSpaceUser)
admin.site.register(Project)
admin.site.register(Task)

