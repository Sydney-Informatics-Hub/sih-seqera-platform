# Seqera base image
FROM public.cr.seqera.io/platform/data-studio-rstudio:4.4.1-u2-0.8.1 AS connect

RUN wget https://github.com/Sydney-Informatics-Hub/scrna-analysis/raw/refs/heads/main/install/install.R && \
    /opt/conda/bin/Rscript -e "install.packages('tidyverse', repos='https://cloud.r-project.org')" && \
    rm install.R

ENTRYPOINT ["/usr/bin/connect-client", "--entrypoint"]

CMD ["/usr/bin/bash", "-c", "/init"]