# How to prepare a pipeline for Seqera Platform

Pipelines require a schema file before they can be compatible for use on 
Seqera Platform.

A schema file serves multiple purposes such as:

* Allow for automated validation of inputs when running the pipeline
* Used to generate command line help
* **Used to build interfaces to launch pipelines**

The schema must be called `nextflow_schema.json` and live in the top directory
of your pipeline repository, where Nextflow and interfaces like Seqera Platform
will automatically look for it.

Note: `nf-core` pipelines all have schemas already and are ready for use on
Seqera Platforms.

## How to setup `nf-core tools` 

**Requirements**

* A functional pipeline with all parameters defined in config files.
* Access to Gadi and a project

**Steps:**

1. Install `nf-core/tools`. On Gadi:

```bash
module load python3/3.12.1 # Change to a supported version of your choice
python3 -m pip install nf-core
```

2. Confirm the install worked by running `nf-core`. You should see a similar output:

INSERT SCREENSHOT

3. Change directories to the pipeline you need to create a schema for. e.g. `cd /scratch/er01/my_pipeline`.
4. Build the initial schema:

```bash
module load nextflow
nf-core pipelines schema build
```

INSERT SCREENSHOT

5. If prompted with `✨ Default for 'params.<name>' is not in schema (def='<value>'). Update pipeline schema? [y/n]:`, enter **y**. This ensures all parameters are captured in the schema correctly.
6. When prompted with `🚀  Launch web builder for customisation and editing? [y/n]:`, enter **y**.
7. A browser tab will open to edit schema graphically.

You are now ready to develop the details of your schema.

## How to populate a schema with the web editor

There are two types of fields you can complete in the schema:

1. **Parameter** - entry for each `params.<name>` in your pipeline.
2. **Group** - an optional field you can use to group related parameters together.

**Requirements**

* A functional pipeline with all parameters defined in config files.
* Access to Gadi and a project.
* `nf-core tools` installed and be able to access web interface for schema development.

**Steps:**

When first opening the web editor, the parameter IDs will be pre-filled.

1. For each parameter, add a text **Description** that briefly outline what the parameter does or what the user needs to provide.
2. Optionally, add additional **Help text**. You can provide additional information such as how the parameter value (such as paths) should be formatted, or what an input file should contain (such as columns in a samplesheet).
3. Select the correct **Type** - this describes what type of value this parametmer accepts. Some examples:

| Type    | Description                                                                                                                                                                                                                        | Examples                                                                                       |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| string  | Text inputs such as directory or file paths, names, Gadi project/storage codes.                                                                                                                                                    | `--input path/to/samplesheet.csv`, `--gadi_storage scratch/er01+gdata/er01`, `--cohort cohort` |
| number  | A non-integer number such as parameter thresholds, clustering resolutions. It can also accept integers.                                                                                                                            | `--threshold 0.1`, `--p_value 0.05`, `--cluster_resolution 1.8`                                |
| integer | A number that must always be an integer, such as the number of CPUs, cells or samples                                                                                                                                              | `--min_samples 3`, `--num_threads 2`                                                           |
| boolean | A parameter that doesn't take any value, but triggers behaviour when included. Such as showing the help message, or to download a database. Nextflow will interpret the parameter as `true` if included, otherwise `false` if not. | `--help`, `--download_db`                                                                      |

4. Enter a default value for the parameter if required. Leave blank for a `null` value.
5. If the parameter must always be provided per run, **Select Required**.
6. If the parameter should not be presented to users, **Select Hide**. This can useful for parameters with default values that stay the same across runs, or for developer settings. For example, `--multiqc_config assets/multiqc_config.yml` will unlikely change.
7. Optionally, you can configure additional rules under **Open settings**, such as accepting specific file extensions for strings, or accepting a minimum and/or maximum number or integer.
8. With your parameter now defined, select an icon that represents that parameter!
9. Once all parameters are configured in the schema, we recommend creating **Groups** to organise them. Meaningful groupings could be parameters related to the pipeline input and outputs, or a specific analysis step. For example:

| Group                | Parameters                                          |
| -------------------- | --------------------------------------------------- |
| Input/output options | `samplesheet`, `outdir`, `reference`                |
| Configuration        | `gadi_account`, `gadi_storage`                      |
| Annotation           | `download_vep_cache`, `vep_species`, `vep_assembly` |
| Clustering           | `cluster_resolutions`, `clustering_method`          |
| Other                | All other miscellaneous or secondary parameters.    | 

10. Similar to parameters, populate the Group fields: **Title**, **Description**, **Help text** (optional), **Hide**.
11. Reorganise your groups and parameters as required.
12. When your schema is completed, select the **Finished** button. This will save your changes into `nextflow_schema.json`.
13. Return to your editor, you should see a similar message to `INFO     Writing schema with <N> params: 'nextflow_schema.json'.`

You have sucessfully created a schema for your pipeline! Your pipeline is now ready to be added to Seqera Platform.

## Tips

* See exisitng example schemas from SIH pipelines and nf-core:
    * SIH: [Parabricks-Genomics-nf](https://github.com/Sydney-Informatics-Hub/Parabricks-Genomics-nf/blob/main/nextflow_schema.json)
    * SIH: [scrnavigator-nf](https://github.com/Sydney-Informatics-Hub/scrnavigator-nf/blob/dev/nextflow_schema.json)
    * nf-core: [nf-core/sarek](https://nf-co.re/sarek/3.8.1/parameters/)
* Running `nf-core pipelines schema docs` will give you tables you can copy and paste into a markdown file (e.g. `README.md`) for documentation.

## References

* https://docs.seqera.io/platform-cloud/pipeline-schema/overview
* https://nf-co.re/docs/nf-core-tools/pipelines/schema
* https://nf-co.re/docs/nf-core-tools/installation