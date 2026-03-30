#!/usr/bin/env python3
from pathlib import Path
from re import match

class NextflowSchema:

    def __init__(self, schema_file: Path | None = None, github_name: str | None = None) -> None:
        self._schema_file: Path | None = None
        self._github_name: str | None = None
        self._github_path: Path | None = None
        assert not (schema_file is None and github_name is None), 'Must provide one of `schema_file` or `github_name`'
        if schema_file is not None:
            assert isinstance(schema_file, Path), '`schema_file` must be a Path object'
            self._schema_file = schema_file
        else:
            assert isinstance(github_name, str), '`github_name` must be a string'
            assert match(r'^[\w\-\.]+/[\w\-\.]+$', github_name), '`github_name` must be a valid GitHub repository name of the structure "<organisation>/<repository>"'
            self._github_name = github_name

    def _pull_github(self) -> Path:
        pass

    def _get_github_path(self) -> Path:
        if self._github_path is None:
            self._github_path = self._pull_github()
        return self._github_path

    @property
    def schema_file(self) -> Path:
        if self._schema_file is not None:
            return self._schema_file
        elif self._github_name is not None:
            github_path = self._get_github_path()
            return github_path / 'assets/schema_input.json'