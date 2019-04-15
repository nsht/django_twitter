from django.contrib import admin
from .models import Tweet, FollowerRelations

# Register your models here.


admin.site.register(Tweet)
admin.site.register(FollowerRelations)
