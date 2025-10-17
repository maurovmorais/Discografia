from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files import File

class Vinil(models.Model):
    """
    Representa um disco de vinil na coleção.
    """
    CONSERVACAO_CHOICES = [
        ('M', 'Mint (M)'),
        ('NM', 'Near Mint (NM or M-)'),
        ('VG+', 'Very Good Plus (VG+)'),
        ('VG', 'Very Good (VG)'),
        ('G+', 'Good Plus (G+)'),
        ('G', 'Good (G)'),
    ]

    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    ano_lancamento = models.PositiveIntegerField()
    descricao = models.TextField(blank=True, null=True)
    imagem_capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    para_troca = models.BooleanField(default=False)
    conservacao_disco = models.CharField(max_length=3, choices=CONSERVACAO_CHOICES, default='VG')
    conservacao_capa = models.CharField(max_length=3, choices=CONSERVACAO_CHOICES, default='VG')

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

    def save(self, *args, **kwargs):
        if self.imagem_capa and hasattr(self.imagem_capa, 'file'):
            try:
                # Abrir a imagem
                img = Image.open(self.imagem_capa)
                max_size = (300, 300)

                # Checar se a imagem precisa ser redimensionada
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Salvar a imagem redimensionada em um buffer de memória
                    thumb_io = BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(thumb_io, format=img_format, quality=85)
                    
                    # Criar um novo arquivo Django a partir do buffer
                    new_image = File(thumb_io, name=self.imagem_capa.name)
                    
                    # Atribuir a nova imagem ao campo
                    self.imagem_capa = new_image
            except Exception as e:
                # Em caso de erro (ex: arquivo não é imagem), não faz nada
                print(f"Erro ao redimensionar imagem: {e}")
                pass

        super().save(*args, **kwargs)

class Desejo(models.Model):
    """
    Representa um item na lista de desejos de vinis.
    """
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    ano_lancamento = models.PositiveIntegerField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    imagem_capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

    def save(self, *args, **kwargs):
        if self.imagem_capa and hasattr(self.imagem_capa, 'file'):
            try:
                # Abrir a imagem
                img = Image.open(self.imagem_capa)
                max_size = (300, 300)

                # Checar se a imagem precisa ser redimensionada
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Salvar a imagem redimensionada em um buffer de memória
                    thumb_io = BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(thumb_io, format=img_format, quality=85)
                    
                    # Criar um novo arquivo Django a partir do buffer
                    new_image = File(thumb_io, name=self.imagem_capa.name)
                    
                    # Atribuir a nova imagem ao campo
                    self.imagem_capa = new_image
            except Exception as e:
                # Em caso de erro (ex: arquivo não é imagem), não faz nada
                print(f"Erro ao redimensionar imagem: {e}")
                pass

        super().save(*args, **kwargs)