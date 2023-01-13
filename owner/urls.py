from django.urls import path
from owner import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('register',views.SignUpView.as_view()),
    path('home', views.HomeView.as_view()),
    path('login', views.SignInView.as_view()),
    path('products/add',views.ProductAddView.as_view())

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)