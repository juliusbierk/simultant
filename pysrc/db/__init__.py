import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(dir_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from .db.models import Dataset, Model, Fit


__all__ = ['Dataset', 'Model', 'Fit']

if __name__ == '__main__':
    print(Dataset.objects.all())
