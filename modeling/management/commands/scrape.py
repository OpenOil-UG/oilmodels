from django.core.management.base import BaseCommand
from optparse import make_option
from modeling.importscripts import tunisia
    
class Command(BaseCommand):
    args = 'scrape <source>'


    def handle(self, source, **kwargs):
        if source == 'tunisia':
            tunisia.importall()
        else:
            print("nope")

        
