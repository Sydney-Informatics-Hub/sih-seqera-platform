#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from pydantic import BaseModel, ConfigDict, ValidationError, ValidationInfo, field_validator


class MetadataQuestionnaireApp(App):
    """"A Textual app for collecting sample metadata and configuring Nextflow pipelines."""

    BINDINGS = [
        ('d', 'toggle_dark', 'Toggle dark mode'),
        ('q', 'quit', 'Quit'),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            'textual-dark' if self.theme == 'textual-light' else 'textual-light'
        )


if __name__ == '__main__':
    app = MetadataQuestionnaireApp()
    app.run()
