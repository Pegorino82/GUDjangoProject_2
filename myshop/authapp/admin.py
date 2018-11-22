from django.contrib import admin

from authapp import models


class AuthappAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'logup',
        'login',
        'logout',
    )
    readonly_fields = (
        'user',
        'logup',
        'login',
        'logout',
    )

    list_filter = (
        'user',
    )

    search_fields = (
        'user',
    )


admin.site.register(models.AuthApp, AuthappAdmin)
