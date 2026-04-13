from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page


class DemoStructBlock(blocks.StructBlock):
    """
    A StructBlock with one required and one optional CharBlock.

    When a user leaves ``optional_text`` empty in the Wagtail admin, the field
    is stored as JSON null, which becomes None in Python.  wagtail-localize's
    segment extractor does not guard against None for CharBlock, so submitting
    this page for translation raises:

        TypeError: `string` must be either a `StringValue` or a `str`.
                   Got `NoneType`
    """

    required_text = blocks.CharBlock(
        label="Required text",
    )
    optional_text = blocks.CharBlock(
        required=False,
        label="Optional text",
        help_text="Leave this empty, then submit the page for translation to trigger the bug.",
    )

    class Meta:
        icon = "pilcrow"
        label = "Demo block"


class DemoPage(Page):
    body = StreamField(
        [("demo_block", DemoStructBlock())],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Demo page"
