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


class PipelineState:

    def __init__(self, type: ValidPipelineTypes | None = None, input: str | None = None) -> None:
        self.type = type
        self.input = input

    def get_type(self) -> ValidPipelineTypes | None:
        return self.type

    def set_type(self, type: ValidPipelineTypes) -> None:
        self.type = type

    def get_input(self) -> str | None:
        return self.input

    def set_input(self, input: str) -> None:
        self.input = input


class SelectPipeline(Screen):
    """"Select a pipeline or schema file."""

    BINDINGS = [
        ('b', 'previous_screen', 'Back'),
        ('n', 'next_screen', 'Next'),
    ]

    def __init__(self):
        super().__init__()
        self.errors = {}
        # self.no_input = True
        self.state: PipelineState = PipelineState()

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
                    NfCorePipeline(self.state),
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
                    CustomPipeline(self.state),
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
                    SchemaJSONPath(self.state),
                ]
            )
        yield Static(
            '',
            id='error_messages',
            classes='error',
        )

    def action_next_screen(self) -> None:
        """Proceed to the next screen."""
        pipeline_select_mode = self.state.get_type()
        if pipeline_select_mode == ValidPipelineTypes.NFCORE:
            nf_core_pipeline = self.query_one('#nfcore_pipeline_input').value
            if not nf_core_pipeline:
                return None
            self.app.PIPELINE_GITHUB = f'nf-core/{nf_core_pipeline}'
            self.app.PIPELINE_SCHEMA = None
        elif pipeline_select_mode == ValidPipelineTypes.CUSTOM:
            pipeline = self.query_one('#custom_pipeline_input').value
            if not pipeline:
                return None
            schema = Path(pipeline) / 'assets/schema_input.json'
            if schema.is_file:
                self.app.PIPELINE_SCHEMA = schema
                self.app.PIPELINE_GITHUB = None
            else:
                self.app.PIPELINE_GITHUB = pipeline
                self.app.PIPELINE_SCHEMA = None
        elif pipeline_select_mode == ValidPipelineTypes.JSON:
            schema = Path(self.query_one('#schema_input').value)
            if not schema:
                return None
            self.app.PIPELINE_SCHEMA = schema
        else:
            return None
        self.app.PIPELINE_TYPE = pipeline_select_mode
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
        self.state.set_type(ValidPipelineTypes[pipeline_select_mode])

    @on(Input.Changed)
    @on(Input.Blurred)
    def get_invalid_reasons(self, event: Input.Changed | Input.Blurred) -> None:
        err_msg = self.query_one('#error_messages')
        if not event.validation_result.is_valid:
            self.errors[event.input.id] = event.validation_result.failure_descriptions
        else:
            self.errors.pop(event.input.id, None)

    @on(Select.Changed, '#pipeline_select')
    @on(Mount)
    @on(ScreenResume)
    @on(Input.Changed)
    @on(Input.Blurred)
    def show_invalid_reasons(self) -> None:
        pipeline_select_mode = self.query_one('#pipeline_select').value
        err_msg = self.query_one('#error_messages')
        text_input_id = None
        if pipeline_select_mode == ValidPipelineTypes.NFCORE.name:
            text_input_id = 'nfcore_pipeline_input'
        elif pipeline_select_mode == ValidPipelineTypes.CUSTOM.name:
            text_input_id = 'custom_pipeline_input'
        elif pipeline_select_mode == ValidPipelineTypes.JSON.name:
            text_input_id = 'schema_input'
        if not text_input_id:
            return None
        errors = self.errors.get(text_input_id, None)
        if errors:
            msg = 'Errors: ' + '; '.join(errors)
            err_msg.update(msg)
        else:
            err_msg.update('')


class NfCorePipeline(Validator):

    def __init__(self, state: PipelineState) -> None:
        super().__init__()
        self.state = state

    def validate(self, value: str) -> ValidationResult:
        """Check that a string represents an nf-core pipeline name."""
        if self.state.get_type() != ValidPipelineTypes.NFCORE:
            return self.success()
        if not isinstance(value, str):
            return self.failure('Input must be a string.')
        if not bool(value):
            return self.failure('Input cannot be empty.')
        if not match(r'^[\w\-\.]+$', value):
            return self.failure(f'Invalid characters found in pipeline name: {value}')
        return self.success()


class CustomPipeline(Validator):

    def __init__(self, state: PipelineState) -> None:
        super().__init__()
        self.state = state

    def validate(self, value: str) -> ValidationResult:
        """Check that a string represents either a local pipeline path or a GitHub repo name."""
        if self.state.get_type() != ValidPipelineTypes.CUSTOM:
            return self.success()
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

    def __init__(self, state: PipelineState) -> None:
        super().__init__()
        self.state = state

    def validate(self, value: str) -> ValidationResult:
        """Check that a string represents a real, existing path to a JSON file."""
        if self.state.get_type() != ValidPipelineTypes.JSON:
            return self.success()
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