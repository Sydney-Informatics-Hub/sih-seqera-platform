#!/usr/bin/env python3
import requests
from pathlib import Path
import re
import json


class SeqeraApiBase:

    def __init__(self, token_path: str, endpoint: str) -> None:
        self.base_url = 'https://seqera.services.biocommons.org.au/api'
        self.token = self._get_token(token_path)
        self.auth_header = { 'Authorization': f'Bearer {self.token}' }
        self.url = self._get_api_url(endpoint)
        self.api_response = self._get_response(self.url, self.auth_header)
        self.json = self.api_response.json() if self.api_response else None

    def _get_token(self, token_path: str) -> str:
        with open(token_path, 'r') as f:
            token = f.readline().strip()
        return token

    def _get_api_url(self, endpoint: str) -> str:
        base_url = str(self.base_url)
        if base_url.endswith('/'):
            base_url = re.sub(r'/$', '', base_url)
        clean_endpoint = str(endpoint)
        if not clean_endpoint.startswith('/'):
            clean_endpoint = f'/{clean_endpoint}'
        return f'{self.base_url}{clean_endpoint}'

    def _get_response(self, url: str, auth_header: dict) -> None | requests.Response:
        if not url or not auth_header:
            return None
        r = requests.get(url=url, headers=auth_header)
        if r.status_code != 200:
            raise ValueError('Error in API request.')
        return r

    def _get_response_json(self, url: str, auth_header: dict) -> None | dict | list:
        r = self._get_response(url, auth_header)
        return r.json() if r is not None else None

    def _get_response_txt(self, url: str, auth_header: dict) -> None | str:
        r = self._get_response(url, auth_header)
        return r.text if r is not None else None

    def _post_json(self, url: str, auth_header: dict, content: dict = {}) -> None | requests.Response:
        headers = auth_header.copy()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.dumps(content)
        r = requests.post(url=url, headers=headers, data=payload)
        if r.status_code != 200:
            raise ValueError('Error in API request.')
        return r

    def _post_file(self, url: str, auth_header: dict, file_path: str) -> None | requests.Response:
        headers = auth_header.copy()
        headers['Accept'] = 'application/json'
        file_data = open(file_path, 'rb')
        filename = Path(file_path).name
        data_type = None
        if filename.endswith('csv'):
            data_type = 'text/csv'
        elif filename.endswith('tsv'):
            data_type = 'text/tab-separated-values'
        else:
            raise ValueError('Invalid file type - must be CSV or TSV.')
        files = {'file': (filename, file_data, data_type)}
        r = requests.post(url=url, headers=headers, files=files)
        if r.status_code != 200:
            raise ValueError('Error in API request.')
        return r


class SeqeraOrg:

    fields = ['Name', 'Full Name', 'Org ID']

    def __init__(self, id: str, name: str, full_name: str) -> None:
        self.id = id
        self.name = name
        self.full_name = full_name
    
    def as_list(self) -> list:
        return [self.name, self.full_name, self.id]


class SeqeraOrgs(SeqeraApiBase):

    def __init__(self, token_path: str) -> None:
        endpoint = '/orgs'
        super().__init__(token_path, endpoint)
        self.orgs = self._parse_orgs()
        self.id_lookup = self._get_org_id_lookup()
        self.active_org_id = None
        self.active_org = None

    def _parse_orgs(self) -> dict:
        assert self.json, 'Error: SeqeraOrgs object has not been properly initialised.'
        orgs = {}
        for org in self.json['organizations']:
            id = str(org['orgId'])
            name = str(org['name'])
            full_name = str(org['fullName'])
            orgs[id] = SeqeraOrg(id, name, full_name)
        return orgs

    def _get_org_id_lookup(self) -> dict:
        lookup = {}
        for org in self.orgs.values():
            id = org.id
            name = org.name
            full_name = org.full_name
            lookup[id] = id
            lookup[name] = id
            lookup[full_name] = id
        return lookup

    def set_org(self, org_id_or_name: str) -> None:
        self.active_org_id = self.id_lookup.get(org_id_or_name, None)
        self.active_org = self.orgs[self.active_org_id]

    def as_list(self) -> list:
        return [org.as_list() for org in self.orgs.values()]


class SeqeraWorkspace:

    fields = ['Name', 'Workspace ID']

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name
    
    def as_list(self) -> list:
        return [self.name, self.id]


class SeqeraWorkspaces(SeqeraApiBase):

    def __init__(self, token_path: str, org: SeqeraOrg) -> None:
        endpoint = f'/orgs/{org.id}/workspaces'
        super().__init__(token_path, endpoint)
        self.workspaces = self._parse_workspaces()
        self.id_lookup = self._get_workspaces_id_lookup()
        self.active_workspace_id = None
        self.active_workspace = None

    def _parse_workspaces(self) -> dict:
        assert self.json, 'Error: SeqeraWorkspaces object has not been properly initialised.'
        workspaces = {}
        for workspace in self.json['workspaces']:
            id = str(workspace['id'])
            name = str(workspace['name'])
            workspaces[id] = SeqeraWorkspace(id, name)
        return workspaces

    def _get_workspaces_id_lookup(self) -> dict:
        lookup = {}
        for workspace in self.workspaces.values():
            id = workspace.id
            name = workspace.name
            lookup[id] = id
            lookup[name] = id
        return lookup

    def set_workspace(self, workspace_id_or_name: str) -> None:
        self.active_workspace_id = self.id_lookup.get(workspace_id_or_name, None)
        self.active_workspace = self.workspaces[self.active_workspace_id]

    def as_list(self) -> list:
        return [workspace.as_list() for workspace in self.workspaces.values()]


class SeqeraWorkflow:

    fields = ['Name', 'Repository', 'Workflow ID', 'Deleted']

    def __init__(self, id: str, name: str, repo: str, deleted: bool = False) -> None:
        self.id = id
        self.name = name
        self.repo = repo
        self.deleted = deleted

    def as_list(self) -> list:
        return [self.name, self.repo, self.id, self.deleted]


class SeqeraWorkflows(SeqeraApiBase):

    def __init__(self, token_path: str, org: SeqeraOrg, workspace: SeqeraWorkspace | None = None) -> None:
        endpoint = f'/pipelines'
        if workspace:
            endpoint = f'{endpoint}?workspaceId={workspace.id}'
        super().__init__(token_path, endpoint)
        self.workflows = self._parse_workflows()

    def _parse_workflows(self) -> dict:
        assert self.json, 'Error: SeqeraWorkflows object has not been properly initialised.'
        workflows = {}
        for workflow in self.json['pipelines']:
            id = str(workflow['pipelineId'])
            name = str(workflow['name'])
            repo = str(workflow['repository'])
            workflows[id] = SeqeraWorkflow(id, name, repo)
        return workflows

    def as_list(self) -> list:
        return [workflow.as_list() for workflow in self.workflows.values()]


class SeqeraRun:

    fields = ['Run ID', 'Run Name', 'Launch ID', *SeqeraWorkflow.fields]

    def __init__(self, id: str, name: str, launch_id: str, workflow: SeqeraWorkflow):
        self.id = id
        self.name = name
        self.launch_id = launch_id
        self.workflow = workflow

    def as_list(self) -> list:
        workflow_fields = ['NA'] * len(SeqeraWorkflow.fields)
        if self.workflow:
            workflow_fields = self.workflow.as_list()
        return [self.id, self.name, self.launch_id, *workflow_fields]


class SeqeraLaunch:

    fields = ['Launch ID', 'Run ID', 'Workflow ID']

    def __init__(self, id: str, run_id: str, workflow_id: str | None):
        self.id = id
        self.run_id = run_id
        self.workflow_id = workflow_id

    def as_list(self) -> list:
        return [self.id, self.run_id, self.workflow_id]


class SeqeraRuns(SeqeraApiBase):

    def __init__(self, token_path: str, org: SeqeraOrg, workflows: SeqeraWorkflows, workspace: SeqeraWorkspace | None = None) -> None:
        endpoint = '/workflow'
        if workspace:
            endpoint = f'{endpoint}?workspaceId={workspace.id}'
        super().__init__(token_path, endpoint)
        self.workflows = workflows
        self.deleted_workflow_info = {}
        self.launches_json = self._get_launches(workspace)
        self.launches = self._parse_launches()
        self.runs = self._parse_runs(workspace)

    def _get_launches(self, workspace: SeqeraWorkspace | None = None) -> dict:
        assert self.json, 'Error: SeqeraRuns object has not been properly initialised.'
        launches = {}
        for run in self.json['workflows']:
            run_id = run['workflow']['id']
            launch_endpoint = f'/workflow/{run_id}/launch'
            if workspace:
                launch_endpoint = f'{launch_endpoint}?workspaceId={workspace.id}'
            launch_url = self._get_api_url(launch_endpoint)
            launch = self._get_response_json(launch_url, self.auth_header)
            launches[run_id] = launch
        return launches

    def _get_deleted_workflow_info(self, workflow_id: str, workspace: SeqeraWorkspace | None = None) -> SeqeraWorkflow:
        if workflow_id not in self.deleted_workflow_info:
            endpoint = f'/pipelines/{workflow_id}'
            if workspace:
                endpoint = f'{endpoint}?workspaceId={workspace.id}'
            url = self._get_api_url(endpoint)
            workflow_json = self._get_response_json(url, self.auth_header)
            workflow_info = workflow_json['pipeline']
            name = workflow_info['name']
            repo = workflow_info['repository']
            self.deleted_workflow_info[workflow_id] = SeqeraWorkflow(workflow_id, name, repo, deleted=True)
        return self.deleted_workflow_info[workflow_id]

    def _parse_launches(self) -> dict:
        assert self.launches_json, 'Error: SeqeraRuns object has not been properly initialised.'
        launches = {}
        for run_id, launch in self.launches_json.items():
            launch_info = launch['launch']
            launch_id = str(launch_info['id'])
            workflow_id = str(launch_info['pipelineId']) if launch_info['pipelineId'] else None
            launches[launch_id] = SeqeraLaunch(launch_id, run_id, workflow_id)
        return launches

    def _parse_runs(self, workspace: SeqeraWorkspace | None = None) -> dict:
        assert self.json and self.launches, 'Error: SeqeraRuns object has not been properly initialised.'
        runs = {}
        for run in self.json['workflows']:
            workflow = run['workflow']
            run_id = str(workflow['id'])
            run_name = str(workflow['runName'])
            launch_id = str(workflow['launchId'])
            launch_info = self.launches[launch_id]
            if not launch_info.workflow_id:
                workflow_info = SeqeraWorkflow('NA', 'NA', 'NA', True)
            else:
                workflow_id = str(launch_info.workflow_id)
                workflow_info = self.workflows.workflows.get(workflow_id, None)
                if not workflow_info:
                    workflow_info = self._get_deleted_workflow_info(workflow_id, workspace)
            runs[run_id] = SeqeraRun(run_id, run_name, launch_id, workflow_info)
        return runs

    def as_list(self) -> list:
        return [run.as_list() for run in self.runs.values()]


class SeqeraDataset:

    fields = ['Name', 'File Name', 'Dataset ID', 'Version', 'Description']

    def __init__(self, id: str, name: str, filename: str, version: str, description: str = '', content: bytes = b''):
        self.id = id
        self.name = name
        self.filename = filename
        self.version = version
        self.description = description
        assert isinstance(content, bytes), 'Error: dataset content must be a bytes object.'
        self.content = content

    def set_content(self, content: bytes = b'') -> None:
        assert isinstance(content, bytes), 'Error: dataset content must be a bytes object.'
        self.content = content

    def get_content(self, decode: bool = False):
        if decode:
            return self.content.decode()
        else:
            return self.content

    def as_list(self) -> list:
        return [self.name, self.filename, self.id, self.version, self.description]


class SeqeraDatasets(SeqeraApiBase):

    def __init__(self, token_path: str, workspace: SeqeraWorkspace | None = None) -> None:
        endpoint = '/datasets/versions'
        self.workspace = workspace
        if self.workspace:
            endpoint = f'{endpoint}?workspaceId={self.workspace.id}'
        super().__init__(token_path, endpoint)
        self.datasets = self._parse_datasets()

    def _parse_datasets(self) -> dict:
        assert self.json, 'Error: SeqeraDatasets object has not been properly initialised.'
        datasets = {}
        for dataset in self.json['versions']:
            id = str(dataset['datasetId'])
            name = str(dataset['datasetName'])
            description = str(dataset['datasetDescription'])
            filename = str(dataset['fileName'])
            version = str(dataset['version'])
            datasets[id] = SeqeraDataset(id, name, filename, version, description)
        return datasets

    def _get_dataset_id(self, id: str, name: str) -> str:
        dataset_id = None
        assert self.datasets, 'Error: SeqeraDatasets object has not been properly initialised.'
        assert name or id, 'Error: must supply a valid dataset name or ID.'
        if id:
            assert id in self.datasets, 'Error: must supply a valid dataset ID'
            dataset_id = id
        else:
            for dataset in self.datasets.values():
                if dataset.name == name:
                    dataset_id = dataset.id
                    break
            assert dataset_id is not None, f'Error: no matching dataset name found: {name}'
        return str(dataset_id)

    def get_dataset_content(self, id: str, name: str) -> str:
        dataset_id = self._get_dataset_id(id, name)
        dataset = self.datasets[dataset_id]
        existing_content = dataset.get_content()
        if existing_content:
            return existing_content
        version = dataset.version
        filename = dataset.filename
        endpoint = f'/datasets/{dataset_id}/v/{version}/n/{filename}'
        if self.workspace:
            endpoint = f'{endpoint}?workspaceId={self.workspace.id}'
        url = self._get_api_url(endpoint)
        dataset_response = self._get_response(url, self.auth_header)
        dataset_bytes = dataset_response.content
        dataset.set_content(dataset_bytes)
        return dataset_bytes

    def _create_dataset(self, filename: str, name: str, description: str = '') -> SeqeraDataset:
        endpoint = '/datasets'
        if self.workspace:
            endpoint = f'{endpoint}?workspaceId={self.workspace.id}'
        payload = {
            'name': name,
            'description': description,
        }
        url = self._get_api_url(endpoint)
        post_request = self._post_json(url, self.auth_header, payload)
        post_response_json = post_request.json()
        dataset_info = post_response_json['dataset']
        new_id = dataset_info['id']
        version = dataset_info['version']
        new_dataset = SeqeraDataset(new_id, name, filename, version, description)
        return new_dataset

    def _upload_dataset(self, file_path: str, dataset: SeqeraDataset) -> SeqeraDataset:
        dataset_id = dataset.id
        endpoint = f'/datasets/{dataset_id}/upload'
        if self.workspace:
            endpoint = f'{endpoint}?workspaceId={self.workspace.id}'
        url = self._get_api_url(endpoint)
        post_request = self._post_file(url, self.auth_header, file_path)
        post_response_json = post_request.json()
        dataset_info = post_response_json['version']
        version = dataset_info['version']
        # dataset.set_content(file_data)
        dataset.version = str(version)
        return dataset

    def create_new_dataset(self, file_path: str, name: str, description: str = '') -> SeqeraDataset:
        filename = Path(file_path).name
        new_dataset = self._create_dataset(filename, name, description)
        new_dataset = self._upload_dataset(file_path, new_dataset)
        dataset_id = new_dataset.id
        self.datasets[dataset_id] = new_dataset
        return new_dataset

    def upload_dataset(self, file_path: str, id: str, name: str) -> SeqeraDataset:
        dataset_id = self._get_dataset_id(id, name)
        dataset = self.datasets[dataset_id]
        updated_dataset = self._upload_dataset(file_path, dataset)
        return updated_dataset

    def as_list(self) -> list:
        return [dataset.as_list() for dataset in self.datasets.values()]


class SeqeraApi:

    def __init__(self, token_path: str, org_id_or_name: None | str = None, workspace_id_or_name: None | str = None):
        self.orgs = SeqeraOrgs(token_path)
        self.workspaces = None
        self.workflows = None
        self.runs = None
        self.datasets = None
        if org_id_or_name:
            self.orgs.set_org(org_id_or_name)
            self.workspaces = SeqeraWorkspaces(token_path, self.orgs.active_org)
            if workspace_id_or_name:
                self.workspaces.set_workspace(workspace_id_or_name)
            self.workflows = SeqeraWorkflows(token_path, self.orgs.active_org, self.workspaces.active_workspace)
            self.runs = SeqeraRuns(token_path, self.orgs.active_org, self.workflows, self.workspaces.active_workspace)
            self.datasets = SeqeraDatasets(token_path, self.workspaces.active_workspace)

    def _print(self, header_list, body_list):
        header_len = len(header_list)
        full_list = [header_list, *body_list]
        col_widths = [0] * header_len
        for row in full_list:
            assert len(row) == header_len, 'Error: inconsistent row lengths found.'
            for i, elem in enumerate(row):
                if len(str(elem)) > col_widths[i]:
                    col_widths[i] = len(str(elem))
        sep_row = ['-' * w for w in col_widths]
        full_list = [header_list, sep_row, *body_list]
        for row in full_list:
            formatted_row = [
                str(elem) + ' ' * (col_widths[i] - len(str(elem)))
                for i, elem in enumerate(row)
            ]
            formatted_row = ' | '.join(formatted_row)
            formatted_row = re.sub(r'\s+$', '', formatted_row)
            print(formatted_row)

    def print_orgs(self):
        header = SeqeraOrg.fields
        body = self.orgs.as_list()
        self._print(header, body)

    def print_workspaces(self):
        header = SeqeraWorkspace.fields
        body = self.workspaces.as_list() if self.workspaces else []
        self._print(header, body)

    def print_workflows(self):
        header = SeqeraWorkflow.fields
        body = self.workflows.as_list() if self.workflows else []
        self._print(header, body)

    def print_runs(self):
        header = SeqeraRun.fields
        body = self.runs.as_list() if self.runs else []
        self._print(header, body)

    def print_datasets(self):
        header = SeqeraDataset.fields
        body = self.datasets.as_list() if self.datasets else []
        self._print(header, body)
