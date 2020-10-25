import random
import csv
from django.core.management.base import BaseCommand
from locations.models import Location, Photo


class Command(BaseCommand):
    help = "This command creates locations"

    def handle(self, *args, **options):
        description = "월미도는 효종4년(1653)에 월미도에 행궁을 설치했다는 기록 외에는 조선조 말기까지 역사에 등장하는 일이 거의 없었다. 행궁의 위치는 동쪽해안에 있던 임해사터라고 되어 있으나 지금으로서는 확인할 길이 없다. 1920년대 후반부터 1930년대까지가 월미도 유원지의 전성기였다. 당시 조선인과 일본인 남녀노소를 가릴 것 없이 월미도의 이름을 모르는 사람이 없을 정도였다 한다. 1989년 7월 문화의 거리가 조성된 이래 문화예술의 장, 만남과 교환의 장 그리고 공연놀이 마당 등으로도 알려지기 시작한 월미도는 인천하면 떠올릴 만큼 유명한 곳으로 자리잡고 있다."
        f = open("tour.csv", "r", encoding="utf-8-sig")
        rdf = csv.DictReader(f)
        rdf_line = 0

        for line in rdf:
            rdf_line += 1

            Location.objects.create(
                name=line["name"],
                lat=float(line["lat"]),
                lon=float(line["lon"]),
                city=line["city"][:2],
                description=description,
                category=line["category"],
                address=line["address"],
                creator_id=1,
                # description=line["description"],
            )

        locations = Location.objects.all()
        for location in locations:
            for i in range(random.randint(3, 5)):
                Photo.objects.create(s
                    location=location,
                    image=f"location_photos/{random.randint(1, 30)}.jpg",
                )

        self.stdout.write(self.style.SUCCESS(f"{rdf_line} locations created"))
        f.close()
