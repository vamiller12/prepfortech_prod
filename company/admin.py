from django.contrib import admin
from .models import TrackingHistory, Vocab, Vocab_Category, Company, Business_Type
# Register your models here.

class VocabAdmin(admin.ModelAdmin):
    

    search_fields = ('term', )

admin.site.register(TrackingHistory)
admin.site.register(Vocab_Category)
admin.site.register(Vocab, VocabAdmin)
admin.site.register(Company)
admin.site.register(Business_Type)



