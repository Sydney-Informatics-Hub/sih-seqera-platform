#!/usr/bin/env python3
import requests
import argparse
from pathlib import Path
from enum import StrEnum


BASE_URL = 'https://seqera.services.biocommons.org.au/api'


class Endpoints(StrEnum):
    LIST_WORKFLOWS = 'workflow'
    @property
    def full(self):
        return f'{BASE_URL}/{self.value}'


def parse_args():
    parser = argparse.ArgumentParser(
        description="Manage the SIH bioinformatics Seqera platform."
    )
    parser.add_argument('-t', '--token', help='Path to a file containing your bearer token.', type=str, default=(Path.home() / '.tower/token'))
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand help.')
    list_workflows = subparsers.add_parser('list', help='List available workflows.')

    args = parser.parse_args()

    # Checks
    assert Path(args.token).is_file(), f'Error: bearer token file does not exist: {args.token}'

    return args


def construct_auth_header(token):
    return {
        'Authorization': f'Bearer {token}',
    }


def list_workflows(token):
    endpoint = Endpoints.LIST_WORKFLOWS.full
    print(endpoint)
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
        workflows = list_workflows(token)
        if len(workflows['workflows']) > 0:
            print(workflows['workflows'][0])


if __name__ == '__main__':
    args = parse_args()
    main(args)