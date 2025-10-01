import csv
import re
import csv
import re
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from reviews.models import Publisher, Contributor, Book, BookContributor, Review


class Command(BaseCommand):
    help = 'Load the reviews data from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str)

    @staticmethod
    def row_to_dict(row, header):
        if len(row) < len(header):
            row += [''] * (len(header) - len(row))
        return dict([(header[i], row[i]) for i, head in enumerate(header) if head])

    @transaction.atomic
    def handle(self, *args, **options):
        csv_path = options.get('csv')
        if not csv_path:
            raise CommandError('You must provide a --csv path to the CSV file.')

        model_section_regex = re.compile(r'content:(\w+)', re.IGNORECASE)
        header = None
        models_data = {}

        try:
            with open(csv_path, encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for i, row in enumerate(reader, start=1):
                    if not row:
                        continue

                    # Detect new model section
                    if row and model_section_regex.match(row[0]) and all(not cell.strip() for cell in row[1:]):
                        model_name = model_section_regex.match(row[0]).group(1)
                        models_data[model_name] = []
                        header = None
                        continue

                    # Header row
                    if header is None:
                        header = row
                        continue

                    # Data row
                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {''}:
                        continue

                    if model_name:
                        models_data[model_name].append(row_dict)

        except FileNotFoundError:
            raise CommandError(f'File "{csv_path}" does not exist.')
        except Exception as e:
            raise CommandError(f'Error reading file: {e}')

        # === CREATE PUBLISHERS ===
        for data in models_data.get('Publisher', []):
            try:
                publisher, created = Publisher.objects.get_or_create(
                    name=data['publisher_name'],
                    defaults={
                        'website': data['publisher_website'],
                        'email': data['publisher_email']
                    }
                )
                if created:
                    self.stdout.write(f'Created Publisher "{publisher.name}"')
            except Exception as e:
                self.stderr.write(f'Error creating Publisher {data}: {e}')

        # === CREATE BOOKS ===
        for data in models_data.get('Book', []):
            try:
                publisher = Publisher.objects.filter(name=data['book_publisher_name']).first()
                if not publisher:
                    self.stderr.write(f'Publisher not found: {data["book_publisher_name"]}')
                    continue

                pub_date = datetime.strptime(data['book_publication_date'], '%Y/%m/%d').date()

                book, created = Book.objects.get_or_create(
                    title=data['book_title'],
                    defaults={
                        'publication_date': pub_date,
                        'isbn': data['book_isbn'],
                        'publisher': publisher
                    }
                )
                if created:
                    self.stdout.write(f'Created Book "{book.title}"')
            except Exception as e:
                self.stderr.write(f'Error creating Book {data}: {e}')

        # === CREATE CONTRIBUTORS ===
        for data in models_data.get('Contributor', []):
            try:
                contributor, created = Contributor.objects.get_or_create(
                    first_names=data['contributor_first_names'],
                    last_names=data['contributor_last_names'],
                    email=data['contributor_email']
                )
                if created:
                    self.stdout.write(f'Created Contributor "{contributor.first_names} {contributor.last_names}"')
            except Exception as e:
                self.stderr.write(f'Error creating Contributor {data}: {e}')

        # === CREATE BOOK CONTRIBUTORS ===
        for data in models_data.get('BookContributor', []):
            try:
                book = Book.objects.filter(title=data['book_contributor_book']).first()
                contributor = Contributor.objects.filter(email=data['book_contributor_contributor']).first()

                if not book:
                    self.stderr.write(f'Book not found: {data["book_contributor_book"]}')
                    continue
                if not contributor:
                    self.stderr.write(f'Contributor not found: {data["book_contributor_contributor"]}')
                    continue

                bc, created = BookContributor.objects.get_or_create(
                    book=book,
                    contributor=contributor,
                    role=data['book_contributor_role']
                )
                if created:
                    self.stdout.write(f'Linked Contributor "{contributor.email}" to Book "{book.title}"')
            except Exception as e:
                self.stderr.write(f'Error linking BookContributor {data}: {e}')

        # === CREATE REVIEWS ===
        for data in models_data.get('Review', []):
            try:
                creator, _ = User.objects.get_or_create(
                    email=data['review_creator'],
                    defaults={'username': data['review_creator']}
                )

                book = Book.objects.filter(title=data['review_book']).first()
                if not book:
                    self.stderr.write(f'Book not found for review: {data["review_book"]}')
                    continue

                review, created = Review.objects.get_or_create(
                    content=data['review_content'],
                    book=book,
                    creator=creator,
                    defaults={
                        'rating': int(data['review_rating']),
                        'date_created': datetime.strptime(data['review_date_created'], '%Y-%m-%d'),
                        'date_edited': datetime.strptime(data['review_date_edited'], '%Y-%m-%d'),
                    }
                )

                if created:
                    self.stdout.write(f'Created Review on "{book.title}" by "{creator.email}"')
            except Exception as e:
                self.stderr.write(f'Error creating Review {data}: {e}')

        self.stdout.write(self.style.SUCCESS("✅ Import complete"))

