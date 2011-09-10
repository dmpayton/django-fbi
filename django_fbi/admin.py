from django import forms
from django.contrib import admin
from django_fbi.forms import FacebookAppAdminForm
from django_fbi.models import FacebookApp, FacebookAccount

class FacebookAccountAdmin(admin.ModelAdmin):
    list_display = ('facebook_id', 'facebook_email', 'connected')
    list_filter = ('user__is_staff', 'user__is_superuser', 'user__is_active', 'user__date_joined',)

    def connected(self, instance):
        return bool(instance.connected)
    connected.boolean = True

class FacebookAppAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('namespace', 'connect')
        }),
        ('App Credentials', {
            'fields': ('app_id', 'app_secret', 'scope')
        }),
        ('Canvas Page', {
            'fields': ('canvas_template', 'canvas_content')
        }),
        ('Tab Page', {
            'fields': ('tab_template', 'tab_content')
        }),
    )
    form = FacebookAppAdminForm
    list_display = ('namespace', 'app_id', 'connect')
    list_editable = ('connect',)

admin.site.register(FacebookApp, FacebookAppAdmin)
admin.site.register(FacebookAccount, FacebookAccountAdmin)
