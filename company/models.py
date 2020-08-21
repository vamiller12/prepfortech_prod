from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
	companyName = models.CharField(max_length=100, unique=True)
	industry = models.CharField(max_length=100)
	headquarters = models.CharField(max_length=100, default='Palo Alto, CA')
	employee_count = models.CharField(max_length=100, default='0')
	ownership = models.CharField(max_length=100, default='public')
	companyURL = models.CharField(max_length=100, default='www.google.com')
	competitors = models.CharField(max_length=100, default='Red Hat')
	is_draft = models.BooleanField(default=True)
	fiscal_year_end = models.CharField(max_length=100, default='Jan 1 2020')
	overview = models.CharField(max_length=1000, default='Red Hat')

	def __str__(self):
        	return self.name

class Financials_StockChart(models.Model):
	company_name = models.ForeignKey(Company, related_name='company_chart', on_delete=models.CASCADE)
	chartURL = models.CharField(max_length=1000, default='www.google.com') 

	def __str__(self):
        	return self.name


class Financial_Trends(models.Model):
	company_fin_trends_name = models.ForeignKey(Company, related_name='fin_trends', on_delete=models.CASCADE)
	ratio_name = models.CharField(max_length=1000) 
	FY2020 = models.DecimalField(max_digits= 12, decimal_places=4)
	FY2019 = models.DecimalField(max_digits= 12, decimal_places=4)
	FY2018 = models.DecimalField(max_digits= 12, decimal_places=4)
	

class Financial_Ratios(models.Model):
	company_fin_ratios_name = models.ForeignKey(Company, related_name='fin_ratios', on_delete=models.CASCADE)
	ratio_name = models.CharField(max_length=1000) 
	FY2020 = models.DecimalField(max_digits= 12, decimal_places=4)
	FY2019 = models.DecimalField(max_digits= 12, decimal_places=4)
	FY2018 = models.DecimalField(max_digits= 12, decimal_places=4)

class Fin_Trends(models.Model):
	parent_company = models.ForeignKey(Company, related_name='financial_trends', on_delete=models.CASCADE)
	ratio = models.CharField(max_length=1000) 
	value = models.DecimalField(max_digits= 12, decimal_places=4)
	fiscal_year = models.IntegerField() 

class Fin_Ratios(models.Model):
	parent_company = models.ForeignKey(Company, related_name='financial_ratios', on_delete=models.CASCADE)
	ratio = models.CharField(max_length=1000) 
	value = models.DecimalField(max_digits= 12, decimal_places=4)
	fiscal_year = models.IntegerField() 

class Twitter(models.Model):
	company_trends_name = models.ForeignKey(Company, related_name='twitter', on_delete=models.CASCADE)
	twitterURL = models.CharField(max_length=1000) 

class Product_Lines(models.Model):
	company_main = models.ForeignKey(Company, related_name='company_products', on_delete=models.CASCADE)
	product_line = models.CharField(max_length=500)
	company_desc = models.CharField(max_length=1000)
	friendly_desc = models.CharField(max_length=1000)
	explainations = models.CharField(max_length=1000)

class ProductSpecific(models.Model):
	parent_company = models.ForeignKey(Company, related_name='company_ind_products', on_delete=models.CASCADE)
	parent_product_line = models.ForeignKey(Product_Lines, related_name='prod_lines', on_delete=models.CASCADE)
	product_line2 = models.CharField(max_length=500)
	product_name = models.CharField(max_length=500)
	company_desc = models.CharField(max_length=1000)
	friendly_desc = models.CharField(max_length=1000)
	
class Vocab(models.Model):
	term = models.CharField(max_length=200, unique=True)
	definition = models.CharField(max_length=1000)
	useful_example = models.CharField(max_length=1000)

class Product_Spec_Vocab(models.Model):
	specific_product = models.ForeignKey(Product_Lines, related_name='prod_spec_vocab', on_delete=models.CASCADE)
	term = models.ForeignKey(Vocab, related_name='vocab_term_id', on_delete=models.CASCADE)

class Product_Line_Vocab(models.Model):
	product_line = models.ForeignKey(Product_Lines, related_name='prod_line_vocab', on_delete=models.CASCADE)
	term = models.ForeignKey(Vocab, related_name='vocab_id', on_delete=models.CASCADE)

class Company_Newsfeed(models.Model):
	parent_company = models.ForeignKey(Company, related_name='company_news', on_delete=models.CASCADE)
	rsslink = models.CharField(max_length=1000) 
