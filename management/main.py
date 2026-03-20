#!/usr/bin/env python3
import argparse
from pathlib import Path
from manage_seqera import SeqeraApi
from samplesheet.app import MyApp


def parse_args():
    parser = argparse.ArgumentParser(
        description='Manage the SIH bioinformatics Seqera platform.'
    )
    parser.add_argument('-t', '--token', help='Path to a file containing your bearer token.', type=str, default=(Path.home() / '.tower/token'))
    parser.add_argument('-o', '--org', help='Organisation ID or name', type=str, default='')
    parser.add_argument('-w', '--workspace', help='Workspace ID', type=str, default='')
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand help.')
    list_parser = subparsers.add_parser('list', help='List objects on Seqera.')
    list_subparsers = list_parser.add_subparsers(dest='list_subcommand', help='list subcommand help.')
    list_orgs = list_subparsers.add_parser('orgs', help='List available organisations.')
    list_workspaces = list_subparsers.add_parser('workspaces', help='List available workspaces.')
    list_workflows = list_subparsers.add_parser('workflows', help='List available workflows.')
    list_runs = list_subparsers.add_parser('runs', help='List all runs in the workspace.')
    list_datasets = list_subparsers.add_parser('datasets', help='List all available datasets.')
    dataset_parser = subparsers.add_parser('dataset', help='Manage Seqera datasets.')
    dataset_subparsers = dataset_parser.add_subparsers(dest='dataset_subcommand', help='dataset subcommand help.')
    dataset_download = dataset_subparsers.add_parser('download', help='Download a dataset.')
    dataset_download.add_argument('-i', '--id', help='Dataset ID', type=str)
    dataset_download.add_argument('-n', '--name', help='Dataset name', type=str)
    dataset_create = dataset_subparsers.add_parser('create', help='Create a new dataset.')
    dataset_create.add_argument('-f', '--file', help='Path to file to upload', type=str, required=True)
    dataset_create.add_argument('-n', '--name', help='Dataset name', type=str, required=True)
    dataset_create.add_argument('-d', '--description', help='Dataset description', type=str, default='')
    dataset_update = dataset_subparsers.add_parser('update', help='Update an existing dataset.')
    dataset_update.add_argument('-f', '--file', help='Path to file to upload', type=str, required=True)
    dataset_update.add_argument('-n', '--name', help='Dataset name', type=str)
    dataset_update.add_argument('-i', '--id', help='Dataset ID', type=str)
    samplesheet_parser = subparsers.add_parser('samplesheet', help='Manage samplesheets.')
    samplesheet_subparsers = samplesheet_parser.add_subparsers(dest='samplesheet_subcommand', help='samplesheet subcommand help.')
    samplesheet_create = samplesheet_subparsers.add_parser('create', help='Create a new samplesheet.')

    args = parser.parse_args()

    # Checks
    assert Path(args.token).is_file(), f'Error: bearer token file does not exist: {args.token}'
    if args.subcommand == 'dataset':
        assert args.org, 'Error: must provide an organisation ID or name to manage datasets.'
        if args.dataset_subcommand in ['download', 'update']:
            assert args.id or args.name, 'Error: either --id or --name must be provided to dataset download command.'

    return args


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
        elif args.list_subcommand == 'runs':
            api.print_runs()
        elif args.list_subcommand == 'datasets':
            api.print_datasets()
    elif args.subcommand == 'dataset':
        if args.dataset_subcommand == 'download':
            print(api.datasets.get_dataset_content(id=args.id, name=args.name).decode('utf-8'))
        elif args.dataset_subcommand == 'create':
            api.datasets.create_new_dataset(args.file, args.name, args.description)
        elif args.dataset_subcommand == 'update':
            api.datasets.upload_dataset(args.file, args.id, args.name)
    elif args.subcommand == 'samplesheet':
        if args.samplesheet_subcommand == 'create':
            app = MyApp()
            app.run()


if __name__ == '__main__':
    args = parse_args()
    main(args)
