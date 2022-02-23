from django.contrib import admin
from polls.models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Countries)
admin.site.register(Cities)
admin.site.register(SalesProduct)
admin.site.register(Product)