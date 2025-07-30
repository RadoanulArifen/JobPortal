from django.contrib import admin
from django.contrib import messages
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Profile, Job, Application

# Inline Application Admin
class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ('applicant', 'applied_at', 'cover_letter', 'resume')
    fields = ('applicant', 'applied_at', 'cover_letter', 'resume')
    
    def has_add_permission(self, request, obj=None):
        return False

# Custom admin for Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_email', 'user_date_joined')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'role')
    list_editable = ('role',)
    actions = ['make_employee', 'make_applicant']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def user_date_joined(self, obj):
        return obj.user.date_joined.strftime('%Y-%m-%d')
    user_date_joined.short_description = 'Joined'
    
    def make_employee(self, request, queryset):
        updated = queryset.update(role='employee')
        self.message_user(request, f'{updated} user(s) were successfully assigned employee role.', messages.SUCCESS)
    make_employee.short_description = "Assign employee role to selected users"
    
    def make_applicant(self, request, queryset):
        updated = queryset.update(role='applicant')
        self.message_user(request, f'{updated} user(s) were successfully assigned applicant role.', messages.SUCCESS)
    make_applicant.short_description = "Assign applicant role to selected users"

# Custom admin for Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'posted_by', 'created_at', 'applications_count', 'view_applications_link')
    search_fields = ('title', 'company_name', 'location')
    list_filter = ('company_name', 'location', 'created_at')
    date_hierarchy = 'created_at'
    inlines = [ApplicationInline]
    readonly_fields = ('created_at', 'applications_summary', 'view_applications_button')
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'company_name', 'location', 'description', 'posted_by', 'created_at')
        }),
        ('Applications', {
            'fields': ('applications_summary', 'view_applications_button'),
            'classes': ('collapse',)
        }),
    )
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:job_id>/applications/',
                self.admin_site.admin_view(self.view_job_applications),
                name='job_applications',
            ),
        ]
        return custom_urls + urls
    
    def applications_count(self, obj):
        count = obj.applications.count()
        return f"{count} application{'s' if count != 1 else ''}"
    applications_count.short_description = 'Applications'
    
    def view_applications_link(self, obj):
        count = obj.applications.count()
        if count > 0:
            url = reverse('admin:job_applications', args=[obj.id])
            return format_html('<a href="{}" class="button">View {} Application{}</a>', 
                             url, count, 's' if count != 1 else '')
        return "No applications"
    view_applications_link.short_description = 'View Applications'
    view_applications_link.allow_tags = True
    
    def applications_summary(self, obj):
        count = obj.applications.count()
        if count > 0:
            return format_html(
                '<p><strong>Total Applications:</strong> {}</p>'
                '<p><strong>Latest Application:</strong> {}</p>',
                count,
                obj.applications.order_by('-applied_at').first().applied_at.strftime('%B %d, %Y at %I:%M %p')
            )
        return "No applications yet"
    applications_summary.short_description = 'Applications Summary'
    
    def view_applications_button(self, obj):
        count = obj.applications.count()
        if count > 0:
            url = reverse('admin:job_applications', args=[obj.id])
            return format_html(
                '<a href="{}" class="button" style="background: #007cba; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">'
                '📋 View All {} Application{}</a>',
                url, count, 's' if count != 1 else ''
            )
        return "No applications to view"
    view_applications_button.short_description = 'View Applications'
    
    def view_job_applications(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        applications = job.applications.all().order_by('-applied_at')
        
        context = {
            'title': f'Applications for "{job.title}"',
            'job': job,
            'applications': applications,
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request),
        }
        
        return TemplateResponse(request, 'admin/job_app/job/applications.html', context)

# Custom admin for Application
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at', 'resume_link')
    search_fields = ('job__title', 'applicant__username', 'applicant__email')
    list_filter = ('applied_at', 'job__company_name')
    date_hierarchy = 'applied_at'
    readonly_fields = ('applied_at',)
    
    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return "No resume"
    resume_link.short_description = 'Resume'
    resume_link.allow_tags = True
