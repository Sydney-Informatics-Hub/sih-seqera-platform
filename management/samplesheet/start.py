#!/usr/bin/env python3
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Button


MARKDOWN = """\
# SIH bioinformatics service samplesheet generator.

Welcome to the samplesheet generator!

This app will guide you through setting up a samplesheet for a pipeline.

**Note** that this app requires that you have a valid
[samplesheet schema JSON file](https://nextflow-io.github.io/nf-schema/latest/nextflow_schema/sample_sheet_schema_examples/)
for your pipeline.

All nf-core pipelines define an `assets/schema_input.json` file for this purpose.
If you are configuring a custom pipeline, this app will look for a similar schema file at the same location in that pipeline.
Alternatively, if you have a valid schema file with an alternate name, you can provide its path directly.
"""


class StartScreen(Screen):
    """"SIH bioinformatics service samplesheet generator."""

    BINDINGS = [
        ('n', 'next_screen', 'Next'),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Markdown(MARKDOWN)
        yield Button(
            label='Start!',
            variant='default',
            id='start_button',
            action='next_screen'
        )

    def action_next_screen(self) -> None:
        """Proceed to the next screen."""
        self.app.push_screen('select_pipeline')
