#!/usr/bin/env python3
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create the YAML config file for quarto."
    )
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands.')
    parser_list = subparsers.add_parser('list', help='List valid arguments to parameters.')
    parser_list.add_argument('-a', '--analyses', action='store_true', help='List all valid analyses and their associated tiers.')
    parser_list.add_argument('-p', '--pipelines', action='store_true', help='List all valid pipelines.')
    parser_generate = subparsers.add_parser('generate', help='Generate the YAML config file.')
    parser_generate.add_argument('-n', '--name', type=str, required=True, help='Name of the recipient.')
    parser_generate.add_argument('-d', '--data_type', type=str, required=True, help='Data type that was processed.')
    parser_generate.add_argument('-a', '--analysis_type', type=str, required=True, help='Analysis type that was requested. Run ./generate_report_config.py --list_analyses to get a list of valid analyses and associated tiers.')
    parser_generate.add_argument('-t', '--analysis_tier', type=str, required=True, help='Analysis tier that was requested. Run ./generate_report_config.py --list_analyses to get a list of valid analyses and associated tiers.')
    parser_generate.add_argument('-p', '--pipelines', type=str, required=True, help='All pipelines that were run. Comma-delimited list of pipelines. Run ./generate_report_config.py --list_pipelines to get a list of valid pipelines.')
    parser_generate.add_argument('-s', '--samplesheets', type=str, required=True, help='Samplesheets for each pipeline that was run. Comma-delimited list of samplesheets. Must be in the same order and the same length as the list of pipelines supplied to --pipelines.')
    return parser.parse_args()


def list_analyses():
    pass


def list_pipelines():
    pass


def main(args):
    """Create the YAML config file for quarto"""
    pass


if __name__ == '__main__':
    args = parse_args()
    # Check for --list_analyses or --list_pipelines flags
    if args.command == 'list':
        if args.analyses:
            pass
        elif args.pipelines:
            pass
    elif args.command == 'generate':
        main(args)
