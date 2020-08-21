import django_filters
from django_filters import CharFilter

from .models import *

class DictionarySearchFilter(django_filters.FilterSet):
	term = CharFilter(field_name='term', lookup_expr='icontains')
	class Meta:
		model = Vocab
		fields = '__all__'
		exclude = ['definition','useful_example']
