#!/usr/bin/env python3
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static


class StartScreen(Screen):
    """"An initial start screen for the app."""

    BINDINGS = [
        ('n', 'next_screen', 'Next'),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Static("Start of questionnaire")

    def action_next_screen(self) -> None:
        """Proceed to the next screen."""
        self.parent.push_screen('select_pipeline')
