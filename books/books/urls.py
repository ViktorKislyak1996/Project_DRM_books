from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, BookRelationViewSet
from store.views import auth

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book-relation', BookRelationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth)
]

urlpatterns += router.urls
