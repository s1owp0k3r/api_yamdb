import os
import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Genre, Title, TitleGenre, Review, Comment
from users.models import User


MODEL_MAPPING = {
    'category': Category,
    'genre': Genre,
    'title': Title,
    'titlegenre': TitleGenre,
    'review': Review,
    'comment': Comment,
    'user': User,
}


class Command(BaseCommand):

    help = 'Import data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csvfile',
            type=str,
            help='Specify the CSV file path.'
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Specify the Django model to import data into.'
        )

    def _create_correct_row_fields(self, row):
        try:
            if row.get('author'):
                row['author'] = User.objects.get(pk=row['author'])
            if row.get('review_id'):
                row['review'] = Review.objects.get(pk=row['review_id'])
            if row.get('title_id'):
                row['title'] = Title.objects.get(pk=row['title_id'])
            if row.get('category'):
                row['category'] = Category.objects.get(pk=row['category'])
            if row.get('genre'):
                row['genre'] = Genre.objects.get(pk=row['genre'])
        except Exception as error:
            self.stdout.write(
                f'Error in row {row.get("id")}.\nError: - {error}'
            )
        return row

    def handle(self, *args, **options):

        path = options['csvfile']
        model = MODEL_MAPPING.get(options['model'].lower())

        if not os.path.exists(path):
            raise CommandError(
                self.stdout.write(
                    self.style.ERROR(f'File {path} does not exist.')
                )
            )

        if not model:
            raise CommandError(
                self.stdout.write(
                    self.style.ERROR(f'Model {model} does not exist.')
                )
            )

        rows = 0
        successful = 0
        self.stdout.write(f'Importing data for model {model.__name__}')

        with open(path, encoding='utf-8', mode='r') as file:
            csv_read = csv.DictReader(file)
            for row in csv_read:
                rows += 1
                row = self._create_correct_row_fields(row)
                try:
                    model.objects.get_or_create(**row)
                    successful += 1
                except Exception as error:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error in row {row.get("id")}.\n'
                            f'Error: - {error}'
                        )
                    )
        self.stdout.write(
            self.style.SUCCESS(
                f'Finished importing data for model {model.__name__}\n'
                f'Total rows: {rows}. '
                f'Successful: {successful}. '
                f'Failed: {abs(rows - successful)}.'
            )
        )
