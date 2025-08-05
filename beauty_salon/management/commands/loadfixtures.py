# Standard library imports
import os

# Django imports
from django.core.management import call_command
from django.core.management.base import BaseCommand

# A custom management command to load initial data.
class Command(BaseCommand):
    
    # Help message displayed when the command is run with --help.
    help = "Initializes the database with project fixtures."

    # The main logic of the command.
    def handle(self, *args, **options):
        
        # Display a warning before running migrations.
        self.stdout.write(self.style.WARNING("Running makemigrations and migrate..."))
        # Attempt to run migrations.
        try:
            # Runs Django's makemigrations command.
            call_command("makemigrations")
            # Runs Django's migrate command.
            call_command("migrate")
            # Display a success message.
            self.stdout.write(self.style.SUCCESS("Migrations applied successfully!"))
        # Catch any errors during migration.
        except Exception as e:
            # Display an error message and exit.
            self.stdout.write(self.style.ERROR(f"Error running migrations: {e}"))
            return

        # Display a warning before loading fixtures.
        self.stdout.write(self.style.WARNING("Loading fixtures..."))

        # Root directory where fixture files are located.
        fixture_directory = 'beauty_salon/fixtures'

        # List of fixture files to be loaded in the correct order.
        fixture_files = [
            "client.json",      
            "employee.json",   
            "salon_service.json",     
            "scheduling.json"   
        ]

        # Iterate over each fixture file.
        for fixture_name in fixture_files:
            # Attempt to load each fixture.
            try:
                # Display a message before loading a specific fixture.
                self.stdout.write(self.style.WARNING(f"Loading fixture: {fixture_name}"))

                # Construct the full path to the fixture file.
                fixture_path = os.path.join(fixture_directory, fixture_name)
                
                # Execute the loaddata command with the full path.
                call_command("loaddata", fixture_path)
                
                # Display a success message for the loaded fixture.
                self.stdout.write(self.style.SUCCESS(f"Fixture '{fixture_name}' loaded successfully."))
            # Catch any errors during fixture loading.
            except Exception as e:
                # Display an error message and exit.
                self.stdout.write(self.style.ERROR(f"Error loading fixture '{fixture_name}': {e}"))
                return

        # Display a final success message.
        self.stdout.write(self.style.SUCCESS("Database initialization process completed."))