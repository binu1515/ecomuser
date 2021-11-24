from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.static import serve

from klog.models import Cartitems
from . import views 
app_name = 'klog'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup',views.signup, name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.Logout,name='logout'),
    path('cart',views.cart,name='cart'),
    path('<int:category_id>/item/<int:product_id>/', views.detail, name='detail'),
    path('<int:product_id>/cartdelete',views.cartdelete,name='cartdelete'),
    path('<int:category_id>/item/<int:product_id>/', views.detail, name='detail'),
    path('item-added/<int:product_id>/', views.add_to_cart, name='item-added'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
	url(r'^remove/(?P<product_id>\d+)/$', views.cartdelete, name='cart_remove'),
    path('cartitems',views.cartitems,name='cartitems'),
    path('<int:id>/', views.checkout, name='checkout'),
    url(r'^create/$', views.order_create, name='order_create'),
    path('payment',views.payment,name='payment'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL ,document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)