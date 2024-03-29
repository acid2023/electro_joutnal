from django.contrib import admin

from network.models import SocialUser
# Register your models here.


@admin.register(SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'avatar', 'username', 'password')
