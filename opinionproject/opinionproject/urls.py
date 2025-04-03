"""
URL configuration for opinionproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path , include
from opinionapp.views import home , opinion, login, signup, like_opinion, comment_opinion , reply_comment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home,name='home'),
    path('opinion/', opinion,name='opinion'),
    path('like/<int:opinion_id>/', like_opinion, name='like_opinion'),
    path('comment/<int:opinion_id>/', comment_opinion, name='comment_opinion'),
    path('reply/<int:comment_id>/', reply_comment, name='reply_comment'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('login/', login,name='login'),
    path('signup/', signup,name='signup')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
