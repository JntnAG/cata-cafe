from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app_cata', '0001_initial'),  # Asegúrate que esta sea tu migración anterior
    ]

    operations = [
        migrations.AddField(
            model_name='cata',
            name='tueste',
            field=models.CharField(default='medio', max_length=15, choices=[('claro', 'Claro'), ('medio', 'Medio'), ('medio_oscuro', 'Medio Oscuro'), ('oscuro', 'Oscuro')]),
        ),
    ]