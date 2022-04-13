from django.contrib import admin
from main.models import *


# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)


class OverheadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Overhead, OverheadAdmin)


class ExpensesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Expenses, ExpensesAdmin)


class OverheadChargesAdmin(admin.ModelAdmin):
    pass


admin.site.register(OverheadCharges, OverheadChargesAdmin)


class PositionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Position, PositionAdmin)


class SiteUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteUser, SiteUserAdmin)





