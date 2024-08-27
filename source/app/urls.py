from django.contrib import admin
# from django.contrib.auth.urls import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from main import views
from main.views import IndexPageView, ChangeLanguageView, page_view
# from main.realtor_dashboard import realtor_views

app_name = "accounts"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexPageView.as_view(), name='index'), 
    
    # path('', include('main.urls')), 
    path('home1/', IndexPageView.as_view(), name='home1'),
    # path('', views.IndexPageView.as_view(), name='home1'),
    # path('login/', views.user_login, name='log-in'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='log-out'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logged_out.html'), name='logout'),

    
    
    path('page/', page_view, name = 'page'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),
    # path('signup/', )
    path('accounts/', include('accounts.urls')),
    path('realtor/', views.realtor, name='realtor'),
    path('realtor_login/', views.realtor_login, name='realtor_login'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('customer/', views.customer, name='customer'),

#testing phase
    path("accounts/", include("django.contrib.auth.urls")),
#chatbot url 
    path('chat/', views.chat, name='chat'),
    #path('main/', include('main.urls')),  #Add if needed
    path('get/', views.get_response, name='get_response'),

    # path('realtor_login/', views.realtor_notification, name='realtor_login'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

