# Notes on Docker usage on nmgtm  cluster

- Let say we want to use FASTQC in docker: https://hub.docker.com/r/biocontainers/fastqc/tags
- pull it by ```docker pull biocontainers/fastqc:v0.11.9_cv8 ```
- Run it locally:

```
docker run -v /home/jakub/Desktop/sample_app/docker_on_cluster/data:/data_folder \
 -v /home/jakub/Desktop/sample_app/docker_on_cluster/output:/output biocontainers/fastqc:v0.11.9_cv8 /bin/sh -c "fastqc -t 3 -o /output /data_folder/example_3.fastq; chmod 777 -R /output"
```

- Scripts I use to run it on cluster:
    - Script to run the job for one file:

```
#!/bin/bash

#SBATCH --account=jkoubele
#SBATCH --job-name=FASTQ_QC
#SBATCH --error=/data/public/jkoubele/cluster_logs/fastq_qc.log

cell_file_prefix="/cellfile/datapublic"
file=${1:-"no003-1_OA3_R1.fastq.gz"}
run_on_cluster=${2:-false}

if $run_on_cluster; then
  cell_file_prefix="/data/public"
  docker load -i $cell_file_prefix/jkoubele/docker_images/fastqc.tar
fi

docker run -v $cell_file_prefix/jkoubele/FLI_total_RNA/20240219_866_YC:/data_folder \
 -v $cell_file_prefix/jkoubele/FLI_total_RNA/QC:/QC biocontainers/fastqc:v0.11.9_cv8 /bin/sh -c "fastqc -t 3 -o /QC /data_folder/$file; chmod 777 -R /QC"
```

- Script to submit multiple jobs:

```
for file in /cellfile/datapublic/jkoubele/FLI_total_RNA/20240219_866_YC/*fastq.gz; do
  file_name=$(basename "$file")
  sbatch -x beyer-n03 /data/public/jkoubele/FLI_total_RNA/fli-total-rna-seq-analysis/fastq_quality_control.sh $file_name true
done
```