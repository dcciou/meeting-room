from django.contrib import admin

# Register your models here.


from .models import ConfeRoom, Order

# Register your models here.
admin.site.register(ConfeRoom)
admin.site.register(Order)