from django.contrib import admin
from .models import TrackingHistory, Vocab, Vocab_Category
# Register your models here.

class VocabAdmin(admin.ModelAdmin):
    

    search_fields = ('term', )

admin.site.register(TrackingHistory)
admin.site.register(Vocab_Category)
admin.site.register(Vocab, VocabAdmin)


