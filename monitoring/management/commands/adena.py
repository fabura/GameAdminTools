from Lib.receiver.core.supports import EuroSupport, RuSupport
from monitoring.models import AdenaLog, Server

__author__ = 'bulat.fattahov'
from Lib.receiver.lineage2.L2AdminFacade import L2AdminFacade
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
#            support = EuroSupport(login='bulat.fattahov', password='1qaz2wsx')
            support = RuSupport(login='bulat.fattahov', password='1qaz2wsx')
            l2_facade = L2AdminFacade(support)

            servers = Server.objects.filter(support = 1)
            for server in servers:
                server_id = server.id
                adena = l2_facade.get_adena(server_id)
                adenaLog = AdenaLog.objects.create(value=adena, server=server)
                adenaLog.save()
                self.stdout.write("\nServer: %s" % server.name)
                self.stdout.write('\nAdena : %s' % adena)
        except Exception as er:
            self.stderr.write(er.message)
