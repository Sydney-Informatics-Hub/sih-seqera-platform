#!/usr/bin/env python3
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, Select
from enum import Enum


class ValidOptions(Enum):
    OPT1 = 'Some option'
    OPT2 = 'Another option'


class TemplateScreen(Screen):
    """"A template screen."""

    BINDINGS = [
        ('b', 'previous_screen', 'Back'),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Static("Make a selection:")
        yield Select((p.value, p.name) for p in ValidOptions)

    def action_previous_screen(self) -> None:
        self.app.pop_screen()
