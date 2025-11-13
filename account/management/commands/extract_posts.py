import csv
from account.models import *
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('account/project_dataset_sp2020_v1.1/Posts_Comments.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # skip header

            for row in reader:
                offerings = Offering.objects.filter(section__course__number=row[0])
                for offering in offerings:
                    offering.section.drop_deadline = parse_date(row[1])
                    offering.section.save()

                    # ✅ Prevent UNIQUE constraint error
                    forum, _ = Forum.objects.get_or_create(offering=offering)

                    if row[2]:
                        try:
                            user = User.objects.get(email=row[3])
                            post = Post.objects.create(
                                forum=forum,
                                auth_user=user,
                                text=row[2],
                            )
                        except User.DoesNotExist:
                            continue  # skip missing users

                        if row[4]:
                            try:
                                comment_user = User.objects.get(email=row[5])
                                Comment.objects.create(
                                    auth_user=comment_user,
                                    text=row[4],
                                    post=post
                                )
                            except User.DoesNotExist:
                                continue
