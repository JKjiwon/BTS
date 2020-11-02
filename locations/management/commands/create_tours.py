import random
import csv
from django.core.management.base import BaseCommand
from locations.models import Location, Photo


class Command(BaseCommand):
    help = "This command creates locations"

    def handle(self, *args, **options):
        f = open("tour.csv", "r", encoding="utf-8-sig")
        rdf = csv.DictReader(f)
        rdf_line = 0

        for line in rdf:
            rdf_line += 1

            Location.objects.create(
                name=line["name"],
                lat=float(line["lat"]),
                lon=float(line["lon"]),
                city=line["city"],
                description=line["description"],
                category=line["category"],
                address=line["address"],
                creator_id=1,
                # description=line["description"],
            )

        locations = Location.objects.all()
        for location in locations:
            for i in range(5):
                Photo.objects.create(
                    location=location,
                    image=f"tour/{location.name}{i}.jpg",
                )
        self.stdout.write(self.style.SUCCESS(f"{rdf_line} locations created"))
        f.close()
