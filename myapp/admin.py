from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(complain)
admin.site.register(Station)
admin.site.register(Police)
admin.site.register(Review)
admin.site.register(UserToken)
admin.site.register(Criminal_Record)


