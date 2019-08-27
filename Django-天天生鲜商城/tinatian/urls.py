from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from tinatian import settings


urlpatterns = [
    # 后台路由
    path('admin/', admin.site.urls),
    path('user/', include(('user.urls', 'user'), namespace='users')),
    path('goods/', include(('goods.urls', 'goods'), namespace='goods')),
    path('cart/', include(('cart.urls', 'goods'), namespace='cart')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# handler404 = utils.
