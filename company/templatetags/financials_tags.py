from django import template
from ..models import Company

register = template.Library()

@register.filter
def get_year(self, year):
	return "value." + year 
    
