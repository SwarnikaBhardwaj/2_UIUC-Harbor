from django.contrib import admin
from .models import Student, Category, Listing


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'university_email', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['first_name', 'last_name', 'university_email']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'description']
    list_filter = ['category_type']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']


