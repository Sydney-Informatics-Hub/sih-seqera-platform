#!/usr/bin/env python3
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, Select
from enum import Enum


class ValidPipelines(Enum):
    SCRNASEQ = 'nf-core/scrnaseq'
    SCRNAVIGATOR = 'scrnavigator-nf'


class SelectPipeline(Screen):
    """"An initial start screen for the app."""

    BINDINGS = [
        ('b', 'previous_screen', 'Back'),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Static("What pipeline do you want to configure?")
        yield Select((p.value, p.name) for p in ValidPipelines)

    def action_previous_screen(self) -> None:
        self.parent.pop_screen()
