from django.db import models
from oauth2_provider.models import AbstractApplication, Application
from django.core.management.base import BaseCommand, CommandError

import os

class Command(BaseCommand):
	help = 'Grants Application permissions'

#	def add_arguments(self, parser):
#	        parser.add_argument('application_name', nargs='+', type=str)

	def handle(self, **kwargs):

		try:
			application = Application.objects.get(name='restapiApp')
		except Application.DoesNotExist:
			application = Application(name='restapiApp', client_type=AbstractApplication.CLIENT_CONFIDENTIAL, authorization_grant_type = AbstractApplication.GRANT_PASSWORD)
			application.save()
		config_file = os.environ.get('REGISTRY_ENV', '../config/cactus/application_env')
		with open(config_file, 'w') as env:
			env.write('CLIENT_ID=' + application.client_id + '\n')
			env.write('CLIENT_SECRET=' + application.client_secret + '\n')
		self.stdout.write(self.style.SUCCESS('Successfully registered as restapiApp. Check it on oauth'))
