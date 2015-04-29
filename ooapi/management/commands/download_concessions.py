from django.core.management.base import BaseCommand
import os
from os.path import dirname

class Command(BaseCommand):
    args = 'download'

    def handle(self, *args, **kwargs):
        s3source = 's3://downloads.openoil.net/concessions/'
        destination_dir = dirname(dirname(dirname(__file__))) + '/data/concessions'
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        cmd = 'aws s3 sync --region eu-west-1 %s %s' % (s3source, destination_dir)
        os.system(cmd)
        print('concessions downloaded to %s' % destination_dir)
