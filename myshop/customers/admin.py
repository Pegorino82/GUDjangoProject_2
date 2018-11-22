from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from customers import models

@admin.register(models.Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Extra', {
                'fields': ('_avatar', 'birth_date')
            },
        ),
    )


# class CustomerAdmin(admin.ModelAdmin):
#     list_display = [
#         'username',
#         'first_name',
#         'last_name',
#         'is_staff'
#     ]
#
#     list_filter = [
#         'is_staff',
#         'is_active',
#         'last_login',
#         'birth_date',
#     ]
#
#     search_fields = [
#         'username',
#         'first_name',
#         'last_name',
#     ]
#
#
# admin.site.register(models.Customer, CustomerAdmin)
