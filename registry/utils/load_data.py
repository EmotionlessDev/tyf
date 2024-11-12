import csv
import os.path

from registry.models import University, Major

# python manage.py shell
# exec(open("registry/utils/load_data.py").read())

with open(os.path.abspath("registry/utils/data/universities_Russia.csv")) as f:
    reader = csv.reader(f)
    for row in reader:
        if University.objects.filter(name=row[0]).exists():
            continue
        _, created = University.objects.get_or_create(
            name=row[0],
            city=row[1],
            country="Россия",
        )

with open(os.path.abspath("registry/utils/data/majors_Russia.csv")) as f:
    reader = csv.reader(f)
    for row in reader:
        if Major.objects.filter(name=row[1]).exists():
            continue
        _, created = Major.objects.get_or_create(
            name=row[0],
            code=row[1],
        )
