from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Add an IP to the blacklist"

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str)

    def handle(self, *args, **options):
        ip = options['ip']
        BlockedIP.objects.get_or_create(ip_address=ip)
        self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP {ip}'))
