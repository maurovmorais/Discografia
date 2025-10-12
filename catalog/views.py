from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .models import Vinil, Desejo
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def transfer_desejo(request, pk):
    desejo = get_object_or_404(Desejo, pk=pk, usuario=request.user)
    
    # Create a new Vinil object
    Vinil.objects.create(
        titulo=desejo.titulo,
        artista=desejo.artista,
        ano_lancamento=desejo.ano_lancamento,
        descricao=desejo.descricao,
        imagem_capa=desejo.imagem_capa,
        usuario=request.user
    )
    
    # Delete the Desejo object
    desejo.delete()
    
    return redirect('catalog:vinil_list')

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

class DesejoListView(LoginRequiredMixin, ListView):
    model = Desejo
    context_object_name = 'desejos'
    template_name = 'catalog/desejo_list.html'

    def get_queryset(self):
        return Desejo.objects.filter(usuario=self.request.user).order_by('artista')

class DesejoDetailView(LoginRequiredMixin, DetailView):
    model = Desejo
    context_object_name = 'desejo'
    template_name = 'catalog/desejo_detail.html'

class DesejoCreateView(LoginRequiredMixin, CreateView):
    model = Desejo
    fields = ['titulo', 'artista', 'ano_lancamento', 'descricao', 'imagem_capa']
    template_name = 'catalog/desejo_form.html'
    success_url = reverse_lazy('catalog:desejo_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class DesejoUpdateView(LoginRequiredMixin, UpdateView):
    model = Desejo
    fields = ['titulo', 'artista', 'ano_lancamento', 'descricao', 'imagem_capa']
    template_name = 'catalog/desejo_form.html'
    success_url = reverse_lazy('catalog:desejo_list')

class DesejoDeleteView(LoginRequiredMixin, DeleteView):
    model = Desejo
    context_object_name = 'desejo'
    template_name = 'catalog/desejo_confirm_delete.html'
    success_url = reverse_lazy('catalog:desejo_list')