"""
Sets up everything needed to observe the wagtail-localize None CharBlock bug:

  - Creates a superuser (admin / admin)
  - Creates a French locale
  - Creates a DemoPage whose ``optional_text`` CharBlock is stored as null

After running this command, start the server and follow the steps in README.md.
"""

import uuid

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from wagtail.blocks import StreamValue
from wagtail.models import Locale, Page

from demo.home.models import DemoPage


class Command(BaseCommand):
    help = "Create demo content for the wagtail-localize None CharBlock bug"

    def handle(self, *args, **options):
        self._create_superuser()
        self._create_french_locale()
        self._create_demo_page()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Setup complete."))
        self.stdout.write("")
        self.stdout.write("Next steps:")
        self.stdout.write("  python manage.py runserver")
        self.stdout.write("  Open http://localhost:8000/admin/")
        self.stdout.write("  Log in as admin / admin")
        self.stdout.write("  Pages → Demo Bug Page → ⋮ menu → Translate")
        self.stdout.write("  Select French → Submit")
        self.stdout.write("  → TypeError appears in the server console")

    def _create_superuser(self):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write("  Created superuser: admin / admin")
        else:
            self.stdout.write("  Superuser already exists")

    def _create_french_locale(self):
        _, created = Locale.objects.get_or_create(language_code="fr")
        if created:
            self.stdout.write("  Created French locale")
        else:
            self.stdout.write("  French locale already exists")

    def _create_demo_page(self):
        if DemoPage.objects.filter(slug="demo-bug-page").exists():
            self.stdout.write("  Demo page already exists")
            return

        try:
            parent = Page.objects.get(depth=2)
        except Page.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                "No root page found — did you run 'python manage.py migrate'?"
            ))
            return
        except Page.MultipleObjectsReturned:
            parent = Page.objects.filter(depth=2).first()

        # optional_text is None here, matching what the Wagtail admin stores
        # when a user leaves a CharBlock(required=False) field empty.
        stream_data = [
            {
                "type": "demo_block",
                "id": str(uuid.uuid4()),
                "value": {
                    "required_text": "This field has content",
                    "optional_text": None,
                },
            }
        ]

        demo_page = DemoPage(
            title="Demo Bug Page",
            slug="demo-bug-page",
            body=StreamValue(
                DemoPage.body.field.stream_block,
                stream_data,
                is_lazy=True,
            ),
        )
        parent.add_child(instance=demo_page)
        demo_page.save_revision().publish()
        self.stdout.write(f"  Created demo page: {demo_page.title!r}")
