from django.contrib import admin
from .models import Document, Author, Department, Team, Profile
from django.utils.html import format_html

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager')
    search_fields = ('name', 'manager__username')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department__name')
    list_filter = ('department',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'department', 'team', 'is_manager', 'is_approved', 'status', 'user_is_active')
    search_fields = ('user__username', 'full_name', 'department__name', 'team__name')
    list_filter = ('department', 'team', 'is_manager', 'is_approved', 'status', 'user__is_active')
    actions = ['activate_users', 'deactivate_users']

    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.boolean = True
    user_is_active.short_description = 'User Active'
    user_is_active.admin_order_field = 'user__is_active'

    def activate_users(self, request, queryset):
        queryset.update(is_approved=True, status='approved')
        for profile in queryset:
            profile.user.is_active = True
            profile.user.save()
    activate_users.short_description = "Kích hoạt và phê duyệt người dùng đã chọn"

    def deactivate_users(self, request, queryset):
        for profile in queryset:
            profile.user.is_active = False
            profile.user.save()
    deactivate_users.short_description = "Vô hiệu hóa người dùng đã chọn"

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Profile, ProfileAdmin)