from django.contrib import admin;
from .models import Type, Permission, User, TypePermission;

admin.site.register(Type);
admin.site.register(Permission);
admin.site.register(User);
admin.site.register(TypePermission);

