from django.core.management import BaseCommand
from egl_rest.api.egl import EGL_API


class Command(BaseCommand):
    help = 'execute recon_chewbacca and update the sites database'

    def handle(self, *args, **options):
        recon_output = EGL_API().recon_chewbacca.instance.hunt_for_updates()
        self.stdout.write(self.style.SUCCESS(recon_output))
