from django.core.management.base import BaseCommand
import glob
import os
from os.path import dirname
import ooapi.util

class Command(BaseCommand):
    args = 'import_concessions'

    def handle(self, *args, **kwargs):
        destination_dir = dirname(dirname(dirname(__file__))) + '/data/concessions'
        for fname in glob.glob('%s/*' % destination_dir):
            ooapi.util.concession_from_csv(fname)

            

