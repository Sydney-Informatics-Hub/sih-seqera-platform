#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from pydantic import BaseModel, ConfigDict, ValidationError, ValidationInfo, field_validator
from .start import StartScreen
from .template_screen import TemplateScreen


class MyApp(App):
    """"A Textual app."""

    BINDINGS = [
        ('d', 'toggle_dark', 'Toggle dark mode'),
        ('q', 'quit', 'Quit'),
    ]

    SCREENS = {
        'start': StartScreen,
        'template_screen': TemplateScreen,
    }

    def on_mount(self) -> None:
        """Push the start screen on mount."""
        self.push_screen('start')

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            'textual-dark' if self.theme == 'textual-light' else 'textual-light'
        )
