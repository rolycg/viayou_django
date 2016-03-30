from django.contrib import admin
from .models import KeyWord, Travels, User, ContainedIn, Categories, Cities, Countries
from parler.admin import TranslatableAdmin, TranslatableStackedInline
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import gettext_lazy as _


class KeywordAdmin(TranslatableAdmin):
    list_display = ['keywords']


class TravelsAdmin(AdminImageMixin, admin.ModelAdmin):
    filter_horizontal = ['users']
    list_display = ['__str__', 'date', 'origin_code', 'destination_code', 'grade']
    list_filter = ['grade', 'origin_code', 'destination_code', 'date']
    search_fields = ['grade', 'origin_code', 'destination_code', 'date']
    list_editable = ['grade']


class UserAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


class CategoriesAdmin(TranslatableAdmin):
    filter_horizontal = ['travels']
    list_display = ['name']


class ContainedInAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


class CitiesAdmin(TranslatableStackedInline):
    model = Cities
    extra = 3


class CoutryAdmin(TranslatableAdmin):
    list_display = ['name']
    inlines = [CitiesAdmin]


admin.site.register(KeyWord, KeywordAdmin)
admin.site.register(Travels, TravelsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ContainedIn, ContainedInAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Countries, CoutryAdmin)
