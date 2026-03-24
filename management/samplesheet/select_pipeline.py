#!/usr/bin/env python3
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Select, Input, Static, Pretty
from textual.containers import Vertical
from textual import on
from textual.events import Mount, ScreenResume
from textual.validation import Validator, ValidationResult, Function
from enum import Enum
from pathlib import Path
from re import match


class ValidPipelineTypes(Enum):
    NFCORE = 'nf-core pipeline'
    CUSTOM = 'Custom pipeline'
    JSON = 'Schema JSON file only'


MARKDOWN_1_INPUT_TYPE = f"""\
## Pipeline selection

Use the following drop-down box to select the type of pipeline you are configuring.

- If you are configuring an nf-core pipeline, select "{ValidPipelineTypes.NFCORE.value}".
- If you are configuring a custom pipeline that has a valid schema JSON file defined, select "{ValidPipelineTypes.CUSTOM.value}".
- If you just want to provide an existing schema JSON file, select "{ValidPipelineTypes.JSON.value}.

### What kind of pipeline are you configuring?
"""

MARKDOWN_2_NFCORE_INPUT = """\
### What is the name of the nf-core pipeline you are configuring?
"""

MARKDOWN_3_CUSTOM_PIPELINE_INPUT = """\
### What is the GitHub name or local file path of your custom pipeline?
"""

MARKDOWN_4_SCHEMA_INPUT = """\
### What is the path to your schema JSON file?
"""


class SelectPipeline(Screen):
    """"Select a pipeline or schema file."""

    BINDINGS = [
        ('b', 'previous_screen', 'Back'),
        ('n', 'next_screen', 'Next'),
    ]

    def __init__(self):
        super().__init__()
        self.errors = {}
        self.no_input = True

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Markdown(MARKDOWN_1_INPUT_TYPE)
        yield Select(
            options=((t.value, t.name) for t in ValidPipelineTypes),
            id='pipeline_select',
            allow_blank=False,
            value=ValidPipelineTypes.NFCORE.name
        )
        with Vertical(id='nfcore_pipeline_section'):
            # nf-core pipeline selection
            yield Markdown(MARKDOWN_2_NFCORE_INPUT)
            yield Input(
                '',
                'scrnaseq',
                id='nfcore_pipeline_input',
                validators=[
                    NfCorePipeline(),
                ]
            )
        with Vertical(id='custom_pipeline_section'):
            # Custom pipeline selection
            yield Markdown(MARKDOWN_3_CUSTOM_PIPELINE_INPUT)
            yield Input(
                '',
                'Sydney-Informatics-Hub/scrnavigator-nf OR /path/to/custom/pipeline',
                id='custom_pipeline_input',
                validators=[
                    CustomPipeline(),
                ]
            )
        with Vertical(id='schema_file_section'):
            # Schema selection
            yield Markdown(MARKDOWN_4_SCHEMA_INPUT)
            yield Input(
                '',
                'path/to/schema_input.json',
                id='schema_input',
                validators=[
                    SchemaJSONPath(),
                ]
            )
        err_msg = Static(
            '',
            id='error_messages',
            classes='error',
        )
        err_msg.visible = False
        yield err_msg


    def action_next_screen(self) -> None:
        """Proceed to the next screen."""
        if not self.no_input and not self.errors:
            pipeline_select_mode = self.query_one('#pipeline_select').value
            self.app.PIPELINE_TYPE = ValidPipelineTypes[pipeline_select_mode]
            self.app.PIPELINE_SCHEMA = None
            self.app.PIPELINE_GITHUB = None
            if pipeline_select_mode == ValidPipelineTypes.NFCORE.name:
                nf_core_pipeline = self.query_one('#nfcore_pipeline_input').value
                self.app.PIPELINE_GITHUB = f'nf-core/{nf_core_pipeline}'
            elif pipeline_select_mode == ValidPipelineTypes.CUSTOM.name:
                pipeline = self.query_one('#custom_pipeline_input').value
                schema = Path(pipeline) / 'assets/schema_input.json'
                if schema.is_file:
                    self.app.PIPELINE_SCHEMA = schema
                else:
                    self.app.PIPELINE_GITHUB = pipeline
            elif pipeline_select_mode == ValidPipelineTypes.JSON.name:
                schema = Path(self.query_one('#schema_input').value)
                self.app.PIPELINE_SCHEMA = schema
            self.app.push_screen('template_screen')

    def action_previous_screen(self) -> None:
        """Move back to the previous screen."""
        self.app.pop_screen()

    @on(Select.Changed, '#pipeline_select')
    @on(Mount)
    @on(ScreenResume)
    def show_hide_inputs(self):
        """Show or hide inputs based on selection."""
        pipeline_select_mode = self.query_one('#pipeline_select').value
        nfcore_section = self.query_one('#nfcore_pipeline_section')
        custom_section = self.query_one('#custom_pipeline_section')
        json_section = self.query_one('#schema_file_section')
        if pipeline_select_mode == ValidPipelineTypes.NFCORE.name:
            nfcore_section.display = True
            custom_section.display = False
            json_section.display = False
        elif pipeline_select_mode == ValidPipelineTypes.CUSTOM.name:
            nfcore_section.display = False
            custom_section.display = True
            json_section.display = False
        elif pipeline_select_mode == ValidPipelineTypes.JSON.name:
            nfcore_section.display = False
            custom_section.display = False
            json_section.display = True

    @on(Input.Changed)
    def register_input(self, event: Input.Changed) -> None:
        self.no_input = False

    @on(Input.Changed)
    @on(Input.Blurred)
    def show_invalid_reasons(self, event: Input.Changed | Input.Blurred) -> None:
        err_msg = self.query_one(Static)
        if not event.validation_result.is_valid:
            self.errors[event.input.id] = event.validation_result.failure_descriptions
            err_msg.visible = True
        else:
            self.errors.pop(event.input.id, None)
            err_msg.visible = False
        if self.errors[event.input.id]:
            msg = 'Errors: ' + '; '.join(self.errors[event.input.id])
            err_msg.update(msg)
        else:
            err_msg.update(None)


class NfCorePipeline(Validator):

    def validate(self, value: str) -> ValidationResult:
        """Check that a string represents an nf-core pipeline name."""
        if not isinstance(value, str):
            return self.failure('Input must be a string.')
        if not bool(value):
            return self.failure('Input cannot be empty.')
        if not match(r'^[\w\-\.]+$', value):
            return self.failure(f'Invalid characters found in pipeline name: {value}')
        return self.success()


class CustomPipeline(Validator):

    def validate(self, value: str) -> ValidationResult:
        """Check that a string represents either a local pipeline path or a GitHub repo name."""
        if not isinstance(value, str):
            return self.failure('Input must be a string.')
        if not bool(value):
            return self.failure('Input cannot be empty.')
        schema_exists = (Path(value) / 'assets/schema_input.json').is_file()
        is_valid_github_name = match(r'^[\w\-\.]+/[\w\-\.]+$', value)
        if not schema_exists and not is_valid_github_name:
            return self.failure(f'Input is not an existing directory and is not a valid GitHub name: {value}')
        return self.success()


class SchemaJSONPath(Validator):

    def validate(self, value: str) -> ValidationResult:
        """Check that a string represents a real, existing path to a JSON file."""
        if not isinstance(value, str):
            return self.failure('Input must be a string.')
        if not bool(value):
            return self.failure('Input cannot be empty.')
        p = Path(value)
        if not p.is_file():
            return self.failure(f'File does not exist: {value}')
        if not p.suffix == '.json':
            return self.failure(f'File is not a JSON file: {value}')
        return self.success()