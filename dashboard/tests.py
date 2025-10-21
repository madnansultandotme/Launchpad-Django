from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Page, SiteConfiguration


class SiteSettingsViewTests(TestCase):
	def setUp(self) -> None:
		self.user = User.objects.create_user(username='alice', password='test-pass-123')
		self.url = reverse('site_settings')

	def test_get_creates_configuration(self) -> None:
		self.client.login(username='alice', password='test-pass-123')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(SiteConfiguration.objects.filter(user=self.user).exists())

	def test_post_updates_configuration(self) -> None:
		page = Page.objects.create(
			user=self.user,
			title='Launch Update',
			slug='launch-update',
			content='Initial content',
			is_published=True,
		)
		self.client.login(username='alice', password='test-pass-123')
		payload = {
			'featured_page': str(page.pk),
			'site_title': 'Alice HQ',
			'site_description': 'Building the next big thing.',
			'default_theme': SiteConfiguration.THEME_CLASSIC,
		}
		response = self.client.post(self.url, payload, follow=True)
		self.assertRedirects(response, self.url)
		config = SiteConfiguration.objects.get(user=self.user)
		self.assertEqual(config.site_title, 'Alice HQ')
		self.assertEqual(config.site_description, 'Building the next big thing.')
		self.assertEqual(config.default_theme, SiteConfiguration.THEME_CLASSIC)
		self.assertEqual(config.featured_page, page)


class PublishedPagesViewTests(TestCase):
	def setUp(self) -> None:
		self.user = User.objects.create_user(username='bob', password='test-pass-456')

	def test_page_uses_site_configuration(self) -> None:
		page = Page.objects.create(
			user=self.user,
			title='Roadmap',
			slug='roadmap',
			content='Upcoming milestones',
			is_published=True,
		)
		SiteConfiguration.objects.create(
			user=self.user,
			site_title='Bob Ventures',
			site_description='Tech investor and builder.',
			default_theme=SiteConfiguration.THEME_MINIMAL,
			featured_page=page,
		)
		response = self.client.get(reverse('published_pages', args=[self.user.username]))
		self.assertContains(response, 'Bob Ventures')
		self.assertContains(response, 'Tech investor and builder.')
		self.assertContains(response, 'Featured Page')
