from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^$', views.landingPageAlumnos_view, name='landingpagealumnos'),
    url(r'^coevaluacionAlumnos/', views.coevaluacionAlumnos_view, name='coevaluacionAlumnos')
]
