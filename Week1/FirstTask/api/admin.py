from django.contrib import admin
from .models import Company, Review


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'title', 'title', 'summary', 'ip_address', 'submission_date', 'company', 'reviewer')
    list_display_links = ('id', 'rating', 'title', 'title', 'summary', 'ip_address', 'submission_date', 'company', 'reviewer')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Review, ReviewAdmin)
