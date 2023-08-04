import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User

model_csv_equal = {
    "static/data/category.csv": Category,
    "static/data/genre.csv": Genre,
    "static/data/titles.csv": Title,
    "static/data/genre_title.csv": TitleGenre,
    "static/data/users.csv": User,
    "static/data/review.csv": Review,
    "static/data/comments.csv": Comment,
}


class Command(BaseCommand):
    """Django's management command for importing data from csv files to DB.
    Usage: python3 manage.py import_csv
    """

    help = "CSV data import to the app database"

    def _create_correct_row_fields(self, row):
        try:
            if row.get("author"):
                row["author"] = User.objects.get(pk=row["author"])
            if row.get("review_id"):
                row["review"] = Review.objects.get(pk=row["review_id"])
            if row.get("title_id"):
                row["title"] = Title.objects.get(pk=row["title_id"])
            if row.get("category"):
                row["category"] = Category.objects.get(pk=row["category"])
            if row.get("genre"):
                row["genre"] = Genre.objects.get(pk=row["genre"])
        except Exception as error:
            self.stdout.write(
                f'Error in row {row.get("id")}.\nError: - {error}'
            )
        return row

    def handle(self, *args, **options):
        """Command body"""
        for i in model_csv_equal.items():
            path, model = i
            rows = 0
            successful = 0
            self.stdout.write(f"Importing data for model {model.__name__}")
            with open(path, encoding="utf-8", mode="r") as file:
                csv_read = csv.DictReader(file)
                for row in csv_read:
                    rows += 1
                    row = self._create_correct_row_fields(row)
                    try:
                        model.objects.get_or_create(**row)
                        successful += 1
                    except Exception as error:
                        self.stdout.write(
                            f'Error in row {row.get("id")}.\n'
                            f"Error: - {error}"
                        )
            self.stdout.write(
                f"Finished importing data for model {model.__name__}\n"
                f"Total rows: {rows}. Imported successfully: {successful}."
            )
