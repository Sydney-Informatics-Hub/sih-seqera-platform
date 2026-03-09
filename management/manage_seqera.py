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


def construct_auth_header(token):
    return {
        'Authorization': f'Bearer {token}',
    }


def get_all_orgs(token):
    endpoint = f'{BASE_URL}/orgs'
    r = requests.get(endpoint, headers=construct_auth_header(token))
    if r.status_code != 200:
        raise ValueError('Error in fetching organisation list.')
    return r.json()


def get_orgid(token, org_id_or_name):
    all_orgs = get_all_orgs(token)
    for org in all_orgs['organizations']:
        if org_id_or_name == org['orgId']:
            return org_id_or_name
        elif org_id_or_name in [org['name'], org['fullName']]:
            return org['orgId']
    return None


def get_all_workspaces(token, org_id_or_name):
    orgid = get_orgid(token, org_id_or_name)
    if not orgid:
        return None
    endpoint = f'{BASE_URL}/orgs/{orgid}/workspaces'
    r = requests.get(endpoint, headers=construct_auth_header(token))
    if r.status_code != 200:
        raise ValueError('Error in fetching workspace list.')
    return r.json()


def get_workspace_id(token, org_id_or_name, workspace_id_or_name):
    orgid = get_orgid(token, org_id_or_name)
    all_workspaces = get_all_workspaces(token, orgid)
    if not all_workspaces:
        return None
    for workspace in all_workspaces['workspaces']:
        if workspace_id_or_name == workspace['id']:
            return workspace_id_or_name
        elif workspace_id_or_name in [workspace['name'], workspace['fullName']]:
            return workspace['id']
    return None


def get_all_workflows(token, org_id_or_name, workspace_id_or_name):
    workspaceid = None
    if workspace_id_or_name:
        workspaceid = get_workspace_id(token, org_id_or_name, workspace_id_or_name)
    endpoint = f'{BASE_URL}/pipelines'
    if workspaceid:
        endpoint =f'{endpoint}?workspaceId={workspaceid}'
    r = requests.get(endpoint, headers=construct_auth_header(token))
    if r.status_code != 200:
        raise ValueError('Error in fetching workflow list.')
    return r.json()


def get_token(token_path):
    with open(token_path, 'r') as f:
        token = f.readline().strip()
    return token


def main(args):
    token = get_token(args.token)
    if args.subcommand == 'list':
        if args.list_subcommand == 'workflows':
            workflows = get_all_workflows(token, args.org, args.workspace)
            print(workflows)
        elif args.list_subcommand == 'workspaces':
            workspaces = get_all_workspaces(token, args.org)
            print(workspaces)
        elif args.list_subcommand == 'orgs':
            orgs = get_all_orgs(token)
            print(orgs)


if __name__ == '__main__':
    args = parse_args()
    main(args)