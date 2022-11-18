from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('docs/', views.get_docs),
    path('docs/latest/', views.latest_doc),
    path('docs/create/', views.create_doc),
    path('docs/<str:pk>/update', views.update_doc),
    path('docs/<str:pk>/delete', views.delete_doc),
    path('docs/<str:pk>/convert', views.convert_doc),
    path('docs/<str:pk>/', views.get_doc),
]