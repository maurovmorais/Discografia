from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.VinilListView.as_view(), name='vinil_list'),
    path('vinil/<int:pk>/', views.VinilDetailView.as_view(), name='vinil_detail'),
    path('vinil/novo/', views.VinilCreateView.as_view(), name='vinil_create'),
    path('vinil/<int:pk>/editar/', views.VinilUpdateView.as_view(), name='vinil_update'),
    path('vinil/<int:pk>/excluir/', views.VinilDeleteView.as_view(), name='vinil_delete'),
    path('vinil/<int:pk>/toggle-troca/', views.toggle_troca, name='toggle_troca'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('desejos/', views.DesejoListView.as_view(), name='desejo_list'),
    path('desejo/<int:pk>/', views.DesejoDetailView.as_view(), name='desejo_detail'),
    path('desejo/novo/', views.DesejoCreateView.as_view(), name='desejo_create'),
    path('desejo/<int:pk>/editar/', views.DesejoUpdateView.as_view(), name='desejo_update'),
    path('desejo/<int:pk>/excluir/', views.DesejoDeleteView.as_view(), name='desejo_delete'),
    path('desejo/<int:pk>/transferir/', views.transfer_desejo, name='transfer_desejo'),
    path('trocas/', views.TrocaListView.as_view(), name='troca_list'),
]
