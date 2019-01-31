from django.db import models
from oauth2_provider.models import AbstractApplication, Application
from django.core.management.base import BaseCommand, CommandError

import os

class Command(BaseCommand):
        help = 'Grants Application permissions'

        def add_arguments(self, parser):
                parser.add_argument('-p', '--path', nargs=1, type=str, dest='path', help='Path to the environment secrets file')
                parser.add_argument('-f', '--force', action='store_true', dest='force', help='Creates config file if does not exist')
                parser.add_argument('-b', '--blank', action='store_true', dest='blank', help='Creates blank config file at path or environment')
                parser.add_argument('-n', '--name', nargs=1, type=str, dest='name', help='Application name to grant permission. Default: restapiApp')

        def handle(self, *args, **options):

                if options['path']:
                        config_file = options['path'][0]
                else:
                        config_file = os.environ.get('REGISTRY_ENV', '../config/cactus/application_env')

               if not os.path.exists(os.path.dirname(config_file)):
                        if not options['force']:
                                raise CommandError('No config file found at %s' % config_file)
                        else:
                                try:
                                        os.makedirs(os.path.dirname(config_file))
                                except OSError as exc:
                                        raise CommandError('Can\'t create file %s' % config_file)
                if options['name']:
                        appgrant = options['name'][0]
                else:
                        appgrant = 'restapiApp'
                if options['blank']:
                        client_id=''
                        client_secret=''
                else:
                        try:
                                application = Application.objects.get(name=appgrant)
                        except Application.DoesNotExist:
                                application = Application(name=appgrant, client_type=AbstractApplication.CLIENT_CONFIDENTIAL, authorization_grant_type = AbstractApplication.GRANT_PASSWORD)
                                application.save()
                        client_id = application.client_id
                        client_secret = application.client_secret

                with open(config_file, 'w') as env:
                        env.write('CLIENT_ID=' + client_id + '\n')
                        env.write('CLIENT_SECRET=' + client_secret + '\n')
                self.stdout.write(self.style.SUCCESS('Successfully registered as %s. Check it on oauth' % appgrant))
