# SCAN
single cell allelic-specific copy number phasing

## Prerequisites

The following tools must be installed:
+ samtools: version > 1.13, which contains `samtools coverage` function
+ bedtools

## Call read binning

```
$python binning.py -h
Coverage binning.

Usage:
    binning.py --bam_dir=DIR --bam_pattern=STR [--bin_size=INT] [--ref=STR] --out_dir=DIR
    binning.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --bam_dir=DIR       The path of directory of bam files.
    --bam_pattern=STR   The pattern of bam files, i.g., *sorted.bam
    --bin_size=INT      The size of bin. [default: 500000]
    --ref=STR           The reference version (hg19 or hg38). [default: hg38]
    --out_dir=DIR       The path of output files.
```

Running this command will takes all bam files under `out_dir` directory with specified `bam_pattern` pattern as input, and calculate the read coverage with specified `bin_size`. It also calculates the mean coverage and total number of mapped reads for each chromosome. 
