from django.contrib import admin
from .models import LaserSession, Procedure, ProcedureType

admin.site.register(ProcedureType)
admin.site.register(Procedure)
admin.site.register(LaserSession)
