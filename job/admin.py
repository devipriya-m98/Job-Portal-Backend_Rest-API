from django.contrib import admin


from .models import User, Candidate, Job, Application


# Register your models here.
# admin - job


class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_by']
    

class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'candidate_name',
        'job_title',
        'job_id',
        'recruiter_name',
        'status',
        'applied_at',
    )
    list_select_related = ('candidate', 'job', 'job__created_by')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__name', 'job__title', 'job__created_by__username')

    @admin.display(description='Application ID', ordering='id')
    def application_id(self, obj):
        return obj.id

    @admin.display(description='Candidate Name', ordering='candidate__name')
    def candidate_name(self, obj):
        return obj.candidate.name

    @admin.display(description='Job Title', ordering='job__title')
    def job_title(self, obj):
        return obj.job.title

    @admin.display(description='Job ID', ordering='job__id')
    def job_id(self, obj):
        return obj.job.id

    @admin.display(description='Recruiter', ordering='job__created_by__username')
    def recruiter_name(self, obj):
        return obj.job.created_by.username if obj.job.created_by else '-'

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)