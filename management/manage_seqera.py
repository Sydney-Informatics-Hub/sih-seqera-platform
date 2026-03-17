#!/usr/bin/env python3
import requests
import argparse
from pathlib import Path
from enum import StrEnum


BASE_URL = 'https://seqera.services.biocommons.org.au/api'


class Endpoints(StrEnum):
    LIST_WORKFLOWS = 'pipelines'
    LIST_WORKSPACES = 'orgs/'

    @property
    def full(self):
        return f'{BASE_URL}/{self.value}'


def parse_args():
    parser = argparse.ArgumentParser(
        description="Manage the SIH bioinformatics Seqera platform."
    )
    parser.add_argument('-t', '--token', help='Path to a file containing your bearer token.', type=str, default=(Path.home() / '.tower/token'))
    parser.add_argument('-o', '--org', help='Organisation ID or name', type=str, default='')
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand help.')
    list_parser = subparsers.add_parser('list', help='List objects on Seqera.')
    list_subparsers = list_parser.add_subparsers(dest='list_subcommand', help="list subcommand help.")
    list_orgs = list_subparsers.add_parser('orgs', help='List available organisations.')
    list_workspaces = list_subparsers.add_parser('workspaces', help='List available workspaces.')
    list_workflows = list_subparsers.add_parser('workflows', help='List available workflows.')
    list_workflows.add_argument('-w', '--workspace', help='Workspace ID', type=str, default='')

    args = parser.parse_args()

    # Checks
    assert Path(args.token).is_file(), f'Error: bearer token file does not exist: {args.token}'

    return args


class SeqeraApi:

    def __init__(self, token_path, org_id_or_name=None, workspace_id_or_name=None, workflow=None):
        self.token = self._get_token(token_path)
        self.auth_header = { 'Authorization': f'Bearer {self.token}' }
        self.all_orgs = self._get_all_orgs()
        self.set_org(org_id_or_name=org_id_or_name)
        self.all_workspaces = self._get_all_workspaces()
        self.set_workspace(workspace_id_or_name=workspace_id_or_name)
        self.all_workflows = self._get_all_workflows()

    def set_org(self, org_id_or_name):
        self.org_id_or_name = org_id_or_name
        self.org = self._get_orgid()

    def set_workspace(self, workspace_id_or_name):
        self.workspace_id_or_name = workspace_id_or_name
        self.workspace = self._get_workspace_id()

    def _get_token(self, token_path):
        with open(token_path, 'r') as f:
            token = f.readline().strip()
        return token

    def _get_all_orgs(self):
        endpoint = f'{BASE_URL}/orgs'
        r = requests.get(endpoint, headers=self.auth_header)
        if r.status_code != 200:
            raise ValueError('Error in fetching organisation list.')
        return r.json()

    def _get_orgid(self):
        if not self.all_orgs or not self.org_id_or_name:
            return None
        for org in self.all_orgs['organizations']:
            if self.org_id_or_name == org['orgId']:
                return self.org_id_or_name
            elif self.org_id_or_name in [org['name'], org['fullName']]:
                return org['orgId']
        return None

    def _get_all_workspaces(self):
        if not self.org:
            return {}
        endpoint = f'{BASE_URL}/orgs/{self.org}/workspaces'
        r = requests.get(endpoint, headers=self.auth_header)
        if r.status_code != 200:
            raise ValueError('Error in fetching workspace list.')
        return r.json()

    def _get_workspace_id(self):
        if not self.all_workspaces or not self.workspace_id_or_name:
            return None
        for workspace in self.all_workspaces['workspaces']:
            if self.workspace_id_or_name == workspace['id']:
                return self.workspace_id_or_name
            elif self.workspace_id_or_name in [workspace['name'], workspace['fullName']]:
                return workspace['id']
        return None

    def _get_all_workflows(self):
        endpoint = f'{BASE_URL}/pipelines'
        if self.workspace:
            endpoint =f'{endpoint}?workspaceId={self.workspace}'
        r = requests.get(endpoint, headers=self.auth_header)
        if r.status_code != 200:
            raise ValueError('Error in fetching workflow list.')
        return r.json()

    def _list_orgs(self):
        orgs = []
        for org in self.all_orgs['organizations']:
            orgs.append((org['orgId'], org['name']))
        return orgs
    
    def print_orgs(self):
        for id, name in self._list_orgs():
            print(f'{name}:\t{id}')

    def _list_workspaces(self):
        workspaces = []
        for workspace in self.all_workspaces['workspaces']:
            workspaces.append((workspace['id'], workspace['name']))
        return workspaces

    def print_workspaces(self):
        for id, name in self._list_workspaces():
            print(f'{name}:\t{id}')

    def _list_workflows(self):
        workflows = []
        for workflow in self.all_workflows['pipelines']:
            workflows.append((workflow['pipelineId'], workflow['name']))
        return workflows

    def print_workflows(self):
        for id, name in self._list_workflows():
            print(f'{name}:\t{id}')


def main(args):
    token = args.token
    org = args.org
    workspace = args.workspace if hasattr(args, 'workspace') else None
    api = SeqeraApi(token_path=token, org_id_or_name=org, workspace_id_or_name=workspace)
    if args.subcommand == 'list':
        if args.list_subcommand == 'orgs':
            api.print_orgs()
        elif args.list_subcommand == 'workspaces':
            api.print_workspaces()
        elif args.list_subcommand == 'workflows':
            api.print_workflows()


if __name__ == '__main__':
    args = parse_args()
    main(args)