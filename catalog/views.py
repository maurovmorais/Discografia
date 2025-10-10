from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .models import Vinil

class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class VinilListView(LoginRequiredMixin, ListView):
    model = Vinil
    context_object_name = 'vinis'

    def get_queryset(self):
        queryset = Vinil.objects.filter(usuario=self.request.user)
        
        # Filtrando os resultados
        artista = self.request.GET.get('artista')
        titulo = self.request.GET.get('titulo')
        ano = self.request.GET.get('ano')
        
        if artista:
            queryset = queryset.filter(artista=artista)
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if ano:
            queryset = queryset.filter(ano_lancamento=ano)
            
        return queryset.order_by('artista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_vinis = Vinil.objects.filter(usuario=self.request.user)
        context['artistas'] = user_vinis.values_list('artista', flat=True).distinct()
        context['total_vinis'] = user_vinis.count()
        return context

class VinilDetailView(LoginRequiredMixin, DetailView):
    model = Vinil
    context_object_name = 'vinil'

class VinilCreateView(LoginRequiredMixin, CreateView):
    model = Vinil
    fields = ['titulo', 'artista', 'ano_lancamento', 'descricao', 'imagem_capa']
    success_url = reverse_lazy('catalog:vinil_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class VinilUpdateView(LoginRequiredMixin, UpdateView):
    model = Vinil
    fields = ['titulo', 'artista', 'ano_lancamento', 'descricao', 'imagem_capa']
    success_url = reverse_lazy('catalog:vinil_list')

class VinilDeleteView(LoginRequiredMixin, DeleteView):
    model = Vinil
    context_object_name = 'vinil'
    success_url = reverse_lazy('catalog:vinil_list')