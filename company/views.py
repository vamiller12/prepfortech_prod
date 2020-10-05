from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Company, Financials_StockChart, Financial_Ratios, Product_Lines, Financial_Trends, ProductSpecific, Product_Line_Vocab,Product_Spec_Vocab, Vocab, Fin_Trends, Fin_Ratios, Company_Newsfeed
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
import feedparser
from .signals import object_viewed_signal
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel('299d24197987c4f83080961a8aa854b5')

# Create your views here.
@login_required
def home(request):
    mp.track("Homepage Viewed",{"UserID": request.user.pk}) 
    return render(request, "home.html", {})

@login_required
def company_board(request):
    companies = Company.objects.all()
    company_names = list()
    for name in companies:
        company_names.append(name.companyName)
    response_html = '<br>'.join(company_names)
    return HttpResponse(response_html)

@login_required
def company_research_board(request):
    company = Company.objects.order_by('companyName')
    
    company_search = request.GET.get('company_search')
    if company_search != '' and company_search is not None:
        company = company.filter(companyName__icontains=company_search)  

    page = request.GET.get('page', 1)
    
    paginator = Paginator(company, 8)
    
    try: 
        company = paginator.page(page)
    except PageNotAnInteger:
        company = paginator.page(1)
    except EmptyPage:
        company = paginator.page(paginator.num_pages)

    mp.track("Company Research Viewed", {"Company Research": "Page Viewed"}) 

    return render(request, "company_research_board.html", {'company': company})

@login_required
def company_specific(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'company_landing_page.html', {'company': company})

@login_required
def company_overview(request, pk):
    company = get_object_or_404(Company, pk=pk)  
    news = Company_Newsfeed.objects.filter(parent_company_id=pk).values()
    
    for row in news:
        url = row['rsslink']
    feed = feedparser.parse(url) 

    object_viewed_signal.send(company.__class__, instance=company, request=request)
    
    mp.track("Company Viewed",{"Company Name": company.companyName}) 
    mp.track("Company Viewed",{"Company Name": company.companyName, "UserID": request.user.pk}) 
    return render(request, 'company_overview.html', {"company": company, 'news':news, 'feed':feed, 'url':url} )

@login_required
def stock_chart(request, pk):
    company = get_object_or_404(Company, pk=pk)
    stock_chart = get_object_or_404(Financials_StockChart, company_name_id=pk)
    
    mp.track("Stock Chart Viewed",{"Stock Chart": company.companyName})
    mp.track("Stock Chart Viewed",{"Stock Chart": company.companyName, "UserID": request.user.pk})
    
    object_viewed_signal.send(stock_chart.__class__, instance=stock_chart, request=request)
    
    return render(request, 'stock_chart.html', {"company": company, "stock_chart":stock_chart} )  

@login_required
def financials_annual_reports(request, pk):
    company = get_object_or_404(Company, pk=pk)
    mp.track("Annual Report Viewed",{"Annual Report": company.companyName, "UserID": request.user.pk})
    return render(request, 'financials_annual_reports.html', {"company": company} )  

@login_required
def standard_ratios(request, pk):
    company = get_object_or_404(Company, pk=pk)
    fin_ratios = Financial_Ratios.objects.filter(company_fin_ratios_name_id=pk)
    return render(request, 'standard_ratios.html', {"company": company, "fin_ratios":fin_ratios} ) 

@login_required
def financial_trends(request, pk):
    company = get_object_or_404(Company, pk=pk)
    fin_trends = Financial_Trends.objects.filter(company_fin_trends_name_id=pk)
    return render(request, 'financial_trends.html', {"company": company, "fin_trends":fin_trends} ) 

@login_required
def fin_trends(request, pk):
    company = get_object_or_404(Company, pk=pk)
    trends = list(Fin_Trends.objects.filter(parent_company_id=pk).values())
    ratio_table = {}
    for row in trends:
        ratio_table.setdefault(row['ratio'], {}).update({row['fiscal_year']: row['value']})
    return render(request, 'fin_trends.html', {"company": company, "trends":trends, "ratio_table": ratio_table} ) 

@login_required
def fin_ratios(request, pk):
    company = get_object_or_404(Company, pk=pk)
    ratios = list(Fin_Ratios.objects.filter(parent_company_id=pk).values())
    ratio_table = {}
    for row in ratios:
        ratio_table.setdefault(row['ratio'], {}).update({row['fiscal_year']: row['value']})
    return render(request, 'fin_ratios.html', {"company": company, "ratios":ratios, "ratio_table": ratio_table} ) 

@login_required
def product_lines(request, pk):
    company = get_object_or_404(Company, pk=pk)
    prod_lines = Product_Lines.objects.filter(company_main_id=pk).order_by('id')
    prod_lines_vocab = Product_Line_Vocab.objects.filter(product_line__company_main_id =pk).values('term__term','term__definition','product_line__product_line')

    first = Product_Lines.objects.filter(company_main_id=pk).first()
    get_obj = get_object_or_404(Product_Lines, pk=first.id)
    object_viewed_signal.send(get_obj.__class__, instance=get_obj, request=request)

    mp.track("Product Line Viewed",{"Product Line": company.companyName, "UserID": request.user.pk})
    
    return render(request, 'product_line.html', {"company": company, "prod_lines":prod_lines, "prod_lines_vocab":prod_lines_vocab} )

@login_required
def product_spec(request, pk):
    company = get_object_or_404(Company, pk=pk)
    prod_lines = Product_Lines.objects.filter(company_main_id=pk).order_by('id')
    prod_spec = ProductSpecific.objects.filter(parent_company_id=pk).values('product_name','parent_product_line__product_line','product_line2','company_desc','friendly_desc' )
    prod_spec_vocab = Product_Spec_Vocab.objects.filter(specific_product__company_main_id =pk).values('term__term','term__definition','specific_product__product_line')
    
    first = ProductSpecific.objects.filter(parent_company_id=pk).first()
    get_obj = get_object_or_404(ProductSpecific, pk=first.id)
    object_viewed_signal.send(get_obj.__class__, instance=get_obj, request=request)

    mp.track("Specific Products Viewed",{"Specific Products": company.companyName, "UserID": request.user.pk})

    return render(request, 'product_specific.html', {"company": company, "prod_spec":prod_spec, "prod_lines":prod_lines, "prod_spec_vocab":prod_spec_vocab} )

@login_required
def productflashcards(request, pk):
    company = get_object_or_404(Company, pk=pk)
    prod_lines = Product_Lines.objects.filter(company_main_id=pk).order_by('id')
    prod_spec = ProductSpecific.objects.filter(parent_company_id=pk).values('product_name','parent_product_line__product_line','product_line2','company_desc','friendly_desc' )
    categories = Product_Spec_Vocab.objects.filter(specific_product__company_main_id =pk).values('term__term','term__definition','specific_product__product_line')
    
    mp.track("Flash Cards Page Viewed",{"Flash Cards Page": company.companyName, "UserID": request.user.pk})

    return render(request, "productflashcards.html", {'company':company, 'prod_lines': prod_lines})

@login_required
def flash(request, pk, pl):
    company = get_object_or_404(Company, pk=pk)
    prod_lines = Product_Lines.objects.filter(pk=pl)
    prod_spec = ProductSpecific.objects.filter(parent_company_id=pk).values('product_name','parent_product_line__product_line','product_line2','company_desc','friendly_desc' )
    categories = Product_Spec_Vocab.objects.filter(specific_product__pk =pl).values('term__term','term__definition','specific_product__product_line')
    
    first = Product_Lines.objects.filter(pk=pl).first()
    get_obj = get_object_or_404(Product_Lines, pk=first.id)
    object_viewed_signal.send(get_obj.__class__, instance=get_obj, request=request)

    mp.track("Flash Cards Set Viewed",{"Flash Cards Set": company.companyName, "Products Viewed": first.product_line, "UserID": request.user.pk})

    return render(request, "flash.html", {'company':company, 'prod_lines':prod_lines, 'categories':categories})

@login_required
def dictionary(request):
    dictionary = Vocab.objects.all()
    term_search = request.GET.get('term_search')
    if term_search != '' and term_search is not None:
        dictionary = (dictionary.filter(term__icontains=term_search) ) | (dictionary.filter(definition__icontains=term_search))

    mp.track("Dictionary Page Viewed",{"Lookup Value": term_search, "UserID": request.user.pk})

    return render(request, "dictionary.html", {'dictionary':dictionary})

@login_required
def eli5(request):
    mp.track("Explained Section Viewed",{"UserID": request.user.pk})
    return render(request, "eli5.html", {})

@login_required
def eli5server(request):
    mp.track("Explained Servers Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-server.html", {})

@login_required
def eli5xaas(request):
    mp.track("Explained XaSS  Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-xaas.html", {})

@login_required
def eli5thecloud(request):
    mp.track("Explained The Cloud  Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-thecloud.html", {})

@login_required
def eli5nosqlvsql(request):
    mp.track("Explained NoSQL v SQL Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-nosql-vs-sql.html", {})

@login_required
def eli54Gto5G(request):
    mp.track("Explained 4G to 5G Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-4G-to-5G.html", {})

@login_required
def eliinfrastructure(request):
    mp.track("Explained Infrastructure Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-it_infrastructure.html", {})

@login_required
def elistorage(request):
    mp.track("Explained Storage Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-storage.html", {})

@login_required
def eliswitches(request):
    mp.track("Explained Switches Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-switches.html", {})

@login_required
def elirouters(request):
    mp.track("Explained Routers Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-routers.html", {})
@login_required
def elimiddleware(request):
    mp.track("Explained Middleware Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-middleware.html", {})
@login_required
def eliopssys(request):
    mp.track("Explained Oper. Sys. Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-operating-systems.html", {})
@login_required
def elisecsys(request):
    mp.track("Explained Security Sys. Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-security-systems.html", {})
@login_required
def elicontainers(request):
    mp.track("Explained Containers Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-containers.html", {})

@login_required
def elivirtualization(request):
    mp.track("Explained Virt. Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-virtualization.html", {})

@login_required
def elihcivci(request):
    mp.track("Explained HCI v CI Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-hcivci.html", {})

@login_required
def elistoragetypes(request):
    mp.track("Explained Storage Types Viewed",{"UserID": request.user.pk})
    return render(request, "eli5-storage-types.html", {})

def privacy(request):
    return render(request, "privacy-policy.html", {})

def termsofservice(request):
    return render(request, "terms-of-service.html", {})

def ack(request):
    return render(request, "acknowledgements.html", {})