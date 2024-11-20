import csv
import os.path

from registry.models import University, Major
from main.models import Category, Collection

# python manage.py shell
# exec(open("registry/utils/load_data.py").read())

with open(os.path.abspath("utils/data/universities_Russia.csv")) as f:
    reader = csv.reader(f)
    for row in reader:
        if University.objects.filter(name=row[0]).exists():
            continue
        _, created = University.objects.get_or_create(
            name=row[0],
            city=row[1],
            country="Россия",
        )

with open(os.path.abspath("utils/data/majors_Russia.csv")) as f:
    reader = csv.reader(f)
    for row in reader:
        if Major.objects.filter(name=row[1]).exists():
            continue
        _, created = Major.objects.get_or_create(
            name=row[0],
            code=row[1],
        )

with open(os.path.abspath("utils/data/categories.csv")) as f:
    reader = csv.reader(f)
    for row in reader:
        if Category.objects.filter(name=row[0]).exists():
            continue
        _, created = Category.objects.get_or_create(
            name=row[0],
            description=row[1],
        )

with open(os.path.abspath("/utils/data/collections.csv")) as f:
    reader = csv.reader(f)
    for row in reader:
        if Collection.objects.filter(name=row[0]).exists():
            continue
        _, created = Collection.objects.get_or_create(
            name=row[0],
            description=row[1],
        )
