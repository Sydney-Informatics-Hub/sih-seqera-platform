#!/usr/bin/env python3
import argparse
import os
import yaml


VALID_ANALYSES = {
    'scrnaseq': {
        'standard': 'scRNAseq analysis (standard tier): genome alingment and cell counting.',
        'advanced': 'scRNAseq analysis (advanced tier): genome alignment, cell counting, quality control, filtering, cell annotation, differential expression and functional enrichment analysis.',
        'premium': 'scRNAseq analysis (premium tier): full custom single-cell RNAseq analysis.',
    },
    'germline': {
        'standard': 'Germline variant calling (standard tier): genome alignment, germline variant calling and annotation.',
    },
    'somatic': {
        'standard': 'Somatic variant calling (standard tier): genome alignment, somatic variant calling and annotation.',
    },
}

VALID_PIPELINES = {
    'nf-core/scrnaseq': {
        'description': 'The nf-core scrnaseq pipeline for scRNAseq alignment and counting.',
        'show_cols': [
            'sample',
            'fastq_1',
            'fastq_2',
            'expected_cells',
        ],
        'hide_cols': [],
    },
    'scrnavigator-nf': {
        'description': 'An SIH Nextflow pipeline for scRNAseq QC, annotation, differential expression, and functional enrichment analysis.',
        'show_cols': [],
        'hide_cols': [
            'rds',
            'min_ncount',
            'max_ncount',
            'min_nfeature',
            'max_nfeature',
            'min_mt_pct',
            'max_mt_pct',
            'cells_to_remove',
        ],
    },
}


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

    args = parser.parse_args()

    # Checks
    if args.command == 'generate':
        assert args.analysis_type in VALID_ANALYSES, 'Error: invalid analysis type supplied.'
        assert args.analysis_tier in VALID_ANALYSES[args.analysis_type], 'Error: invalid analysis tier supplied.'
        pipelines = args.pipelines.split(',')
        assert all([p in VALID_PIPELINES for p in pipelines]), 'Error: invalid pipeline supplied.'
        samplesheets = args.samplesheets.split(',')
        assert len(pipelines) == len(samplesheets), 'Error: number of pipelines differs from number of samplesheets.'
        assert all([os.path.isfile(f) for f in samplesheets]), 'Error: one or more samplesheets do not exist.'

    return args


def list_analyses():
    print('The following is a list of valid analyses and their associated tiers that can be included in the report:\n')
    for analysis in VALID_ANALYSES:
        print(f'\tAnalysis: {analysis}\n')
        for tier, description in VALID_ANALYSES[analysis].items():
            print(f'\t\t{tier}:\t{description}')
        print('')


def list_pipelines():
    print('The following is a list of valid pipelines that can be included in the report:\n')
    for pipeline in VALID_PIPELINES:
        description = VALID_PIPELINES[pipeline]['description']
        print(f'\t{pipeline}:\t{description}')
    print('')


def main(args):
    """Create the YAML config file for quarto"""
    config = {
        'contact_name': args.name,
        'data_type': args.data_type,
        'analysis_type': args.analysis_type,
        'service_tier': args.analysis_tier,
        'pipelines': []
    }
    pipelines = args.pipelines.split(',')
    samplesheets = args.samplesheets.split(',')
    for i, pipeline in enumerate(pipelines):
        samplesheet = samplesheets[i]
        show_cols = VALID_PIPELINES[pipeline]['show_cols']
        hide_cols = VALID_PIPELINES[pipeline]['hide_cols']
        pipeline_config = {
            'name': pipeline,
            'samplesheet': samplesheet,
        }
        if show_cols:
            pipeline_config['samplesheet_show_cols'] = show_cols
        if hide_cols:
            pipeline_config['samplesheet_hide_cols'] = hide_cols
        config['pipelines'].append(pipeline_config)
    with open('params.yaml', 'w') as f:
        yaml.dump(config, f)


if __name__ == '__main__':
    args = parse_args()
    # Check for --list_analyses or --list_pipelines flags
    if args.command == 'list':
        if args.analyses:
            list_analyses()
        elif args.pipelines:
            list_pipelines()
    elif args.command == 'generate':
        main(args)
