import csv
import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import ForeignKey, ManyToManyField, DateField
from reviews.models import Publisher, Contributor, Book, BookContributor, Review 

# Define the models and the specific field to use for human-readable linking
MODEL_EXPORT_CONFIG = {
    Publisher: {'link_field': 'name'},
    Book: {'link_field': 'title'},
    Contributor: {'link_field': 'email'},
    BookContributor: {'link_field': None}, 
    Review: {'link_field': None}
}

class Command(BaseCommand):
    help = 'Imports all model data into a single csv with section headers.'

    def handle(self, *args, **options):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f'ALL_MODELS_SECTIONAL_EXPORT_{timestamp}.csv'
        current_dir = Path(__file__).parent 
        file_path = current_dir / output_filename
        
        self.stdout.write(f"Starting sectional data export to {file_path}...")
        
        total_records = 0
        
        try:
            # Open the master file in write mode ('w')
            with open(file_path, 'w', newline='', encoding='utf-8') as master_file:
                
                for Model, config in MODEL_EXPORT_CONFIG.items():
                    # 1. Write the section header (e.g., content:Publisher)
                    master_file.write(f"\ncontent:{Model.__name__}\n")
                    
                    # 2. Write the CSV data for this model
                    total_records += self._write_model_section(master_file, Model, config['link_field'])
            
            self.stdout.write(self.style.SUCCESS(f'Data export complete! Total records: {total_records} 🎉'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))


    def _write_model_section(self, master_file, Model, link_field):
        """Fetches data for a single Model and writes its header and rows to the master file."""
        
        fields = [f for f in Model._meta.concrete_fields if not isinstance(f, ManyToManyField)]
        model_prefix = Model.__name__.lower() + '_'
        
        fk_fields = [f.name for f in fields if isinstance(f, ForeignKey)]
        queryset = Model.objects.all().select_related(*fk_fields)
        
        # 1. Define the prefixed header row (e.g., publisher_name, publisher_website)
        header_names = []
        for field in fields:
            name = field.name
            
            # Custom header for fields that link to a specific value (e.g., email or title)
            if link_field and field.related_model in MODEL_EXPORT_CONFIG:
                linked_attr = MODEL_EXPORT_CONFIG[field.related_model]['link_field']
                header_names.append(f'{model_prefix}{name}_{linked_attr}')
            # Custom header for BookContributor (using specific link fields)
            elif Model == BookContributor and name == 'contributor':
                header_names.append(f'{model_prefix}contributor_email')
            elif Model == Review and name == 'book':
                header_names.append(f'{model_prefix}book_title')
            else:
                header_names.append(f'{model_prefix}{name}')

        # 2. Write the header row to the file
        writer = csv.writer(master_file)
        writer.writerow(header_names)

        # 3. Write data rows
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field.name)

                if value is None:
                    row.append('')
                    continue
                
                # ForeignKey Handling (uses the explicit link_field, e.g., 'name' for Publisher)
                if isinstance(field, ForeignKey):
                    related_model = field.related_model
                    link_attr = MODEL_EXPORT_CONFIG.get(related_model, {}).get('link_field', None)
                    
                    # If the linked model has a specific attribute to display, use it
                    if link_attr and hasattr(value, link_attr):
                        readable_value = getattr(value, link_attr)
                    else:
                        readable_value = str(value)
                        
                # DateField Handling (YYYY/MM/DD)
                elif isinstance(field, DateField):
                    readable_value = value.strftime('%Y/%m/%d')
                
                # Choice Field Handling
                elif field.choices:
                    readable_value = getattr(obj, f'get_{field.name}_display')()

                else:
                    readable_value = value
                
                row.append(readable_value)
            
            writer.writerow(row)
            
        self.stdout.write(f"  - Wrote {queryset.count()} records for {Model.__name__}")
        return queryset.count()
