from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^$', views.landingPageAlumnos_view, name='landingpagealumnos'),
    url(r'^coevaluacionAlumnos/', views.coevaluacionAlumnos_view, name='coevaluacionAlumnos'),
    url(r'^perfil/', views.perfil_view, name='perfil'),
    url(r'^curso-alumno/', views.curso_alumno, name='cursoAlumnos')#falta agregarle el curso_id, no se como hacerlo con url(), con path() si
]
