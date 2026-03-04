# How to prepare a pipeline for Seqera Platform

**Requirements**

* A functional pipeline with all parameters defined in config files.

**Overview**

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


## References

* https://docs.seqera.io/platform-cloud/pipeline-schema/overview
* https://nf-co.re/docs/nf-core-tools/pipelines/schema
* https://nf-co.re/docs/nf-core-tools/installation