"""ltl_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from company import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^company/$', views.company_research_board, name='company_research_board'),
	url(r'^company/(?P<pk>\d+)/$', views.company_specific, name='company_specific'),
    url(r'^company/(?P<pk>\d+)/overview/$', views.company_overview, name='company_overview'),
    url(r'^company/(?P<pk>\d+)/stockchart/$', views.stock_chart, name='stock_chart'),
    url(r'^company/(?P<pk>\d+)/annualreports/$', views.financials_annual_reports, name='annual_reports'),
    url(r'^company/(?P<pk>\d+)/ratios/$', views.fin_ratios, name='fin_ratios'),
    url(r'^company/(?P<pk>\d+)/trends/$', views.fin_trends, name='fin_trends'),
    url(r'^company/(?P<pk>\d+)/product/$', views.product_lines, name='product_line'),
    url(r'^company/(?P<pk>\d+)/catalog/$', views.product_spec, name='product_spec'),
    url(r'^company/(?P<pk>\d+)/productflashcards/$', views.productflashcards, name='productflashcards'),
    url(r'^company/(?P<pk>\d+)/productflashcards/flash/(?P<pl>\d+)/$', views.flash, name='flash'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^reset/$',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),
    
    url(r'^reset/done/$',
    auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
    name='password_reset_done'),
    
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    name='password_reset_confirm'),
    
    url(r'^reset/complete/$',
    auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
    url(r'^dictionary/', views.dictionary, name='dictionary'),
    url(r'^eli5/$', views.eli5, name='explained'),
    url(r'^eli5/eli5-server', views.eli5server, name='eli5server'),
	url(r'^eli5/eli5-xaas', views.eli5xaas, name='eli5xaas'),
    url(r'^eli5/eli5-thecloud', views.eli5thecloud, name='eli5thecloud'),
    url(r'^eli5/eli5-nosql-vs-sql', views.eli5nosqlvsql, name='eli5nosqlvssql'),
    url(r'^eli5/eli5-4G-to-5G', views.eli54Gto5G, name='eli54Gto5G'),
    url(r'^eli5/eli5-it_infrastructure', views.eliinfrastructure, name='eli_infras'),

    url(r'^eli5/eli5-storage', views.elistorage, name='eli_storage'),
    url(r'^eli5/eli5-switches', views.eliswitches, name='eli_switches'),
    url(r'^eli5/eli5-routers', views.elirouters, name='eli_routers'),
    url(r'^eli5/eli5-middleware', views.elimiddleware, name='eli_middleware'),
    url(r'^eli5/eli5-operating-systems', views.eliopssys, name='eli_opssys'),
    url(r'^eli5/eli5-security-systems', views.elisecsys, name='eli_secsys'),
    url(r'^eli5/eli5-containers', views.elicontainers, name='eli_containers'),
    url(r'^eli5/eli5-hci_v_ci', views.elihcivci, name='eli_hcivci'),
    url(r'^eli5/eli5-storage-types', views.elistoragetypes, name='eli_storage_types'),
    url(r'^eli5/eli5-virtualization', views.elivirtualization, name='eli_virt'),

    url(r'^privacy-policy', views.privacy, name='privacy'),
    url(r'^terms-of-service', views.termsofservice, name='termsofservice'),
    url(r'^acknowledgements', views.ack, name='ack'),
    path('thingstochange/', admin.site.urls),

]
