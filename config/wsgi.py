import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

current_path = Path(__file__).resolve().parent.parent
app_path = current_path / 'app'
sys.path.append(str(app_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
