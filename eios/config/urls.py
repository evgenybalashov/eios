from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from core.views import HomeView, UserListView
from education.views import StudentListView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('profiles.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^users/$', login_required(UserListView.as_view()), name='users'),
    url(r'^students/(?P<type>[GBMS])/$', login_required(StudentListView.as_view()), name='students'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
