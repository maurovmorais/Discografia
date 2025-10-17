from django.db import migrations

def update_user_emails(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    users = {
        'mauro': 'maurovmorais@gmail.com',
        'felipe': 'moraismauro1970@gmail.com',
    }
    for username, email in users.items():
        try:
            user = User.objects.get(username=username)
            user.email = email
            user.save()
        except User.DoesNotExist:
            pass

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_vinil_para_troca'),
    ]

    operations = [
        migrations.RunPython(update_user_emails),
    ]