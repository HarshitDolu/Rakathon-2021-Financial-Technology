from django.contrib import admin

# Register your models here.
from .models import User, AccountDetails, UserAddress,Payment



admin.site.register(AccountDetails)
admin.site.register(UserAddress)
admin.site.register(Payment)
