import os
from uuid import uuid4
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from db.models import Dataset

__all__ = ['Dataset']


def main():
    print(Dataset.objects.all())
    d = Dataset(uid=str(uuid4()), info="whatever")
    d.save()
    print(d)


if __name__ == '__main__':
    main()
