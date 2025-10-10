from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.VinilListView.as_view(), name='vinil_list'),
    path('vinil/<int:pk>/', views.VinilDetailView.as_view(), name='vinil_detail'),
    path('vinil/novo/', views.VinilCreateView.as_view(), name='vinil_create'),
    path('vinil/<int:pk>/editar/', views.VinilUpdateView.as_view(), name='vinil_update'),
    path('vinil/<int:pk>/excluir/', views.VinilDeleteView.as_view(), name='vinil_delete'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
