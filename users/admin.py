from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Profile

# 

# Personalizamos el admin del modelo CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    
    # Para la edición del usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Rol del usuario', {'fields': ('role',)}),
    )

    # Para la creación del usuario (Add user)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol del usuario', {'fields': ('role',)}),
    )

# Registro del modelo de perfil
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar')
    search_fields = ('user__username',)