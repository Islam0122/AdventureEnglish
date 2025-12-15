from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Game,HangmanWord


@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if not Game.objects.exists():
        call_command('loaddata', 'apps/games/fixtures/initial_games.json')
    if not HangmanWord.objects.exists():
        call_command('loaddata', 'apps/games/fixtures/games.json')

