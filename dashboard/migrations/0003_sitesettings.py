from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('dashboard', '0002_alter_page_content'),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.CreateModel(
			name='SiteConfiguration',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('site_title', models.CharField(blank=True, max_length=150)),
				('site_description', models.TextField(blank=True)),
				('default_theme', models.CharField(choices=[('minimal', 'Minimal'), ('classic', 'Classic')], default='minimal', max_length=20)),
				('updated_at', models.DateTimeField(auto_now=True)),
				('featured_page', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='featured_on_configs', to='dashboard.page')),
				('user', models.OneToOneField(on_delete=models.deletion.CASCADE, related_name='site_configuration', to=settings.AUTH_USER_MODEL)),
			],
		),
	]
