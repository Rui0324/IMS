from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('skills', models.CharField(blank=True, max_length=200)),
                ('interests', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_info', to='accounts.user')),
            ],
        ),
    ]
