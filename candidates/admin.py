from django.contrib import admin
from .models import (
    CandidateProfile, 
    Address, 
    Education, 
    Training, 
    Employment, 
    Skill, 
    ExtracurricularActivity, 
    Reference, 
    PortfolioPublicationProject
)

# Registering models so they show up in the Django admin panel
admin.site.register(CandidateProfile)
admin.site.register(Address)
admin.site.register(Education)
admin.site.register(Training)
admin.site.register(Employment)
admin.site.register(Skill)
admin.site.register(ExtracurricularActivity)
admin.site.register(Reference)
admin.site.register(PortfolioPublicationProject)