from Lib.receiver.core.supports import EuroSupport
from monitoring.models import AdenaLog

__author__ = 'bulat.fattahov'
from Lib.receiver.lineage2.L2AdminFacade import L2AdminFacade
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            support = EuroSupport(login='bulat.fattahov', password='1qaz2wsx')
            l2_facade = L2AdminFacade(support)

            adena = l2_facade.get_adena(71)
            adenaLog = AdenaLog.objects.create(value=adena, server=71)
            adenaLog.save()
            self.stdout.write('Adena count successfully logged "%s"' % adena)
        except Exception as er:
            self.stderr.write(er.message)

