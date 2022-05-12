# SCAN
single cell allelic-specific copy number phasing

## Prerequisites

The following tools must be installed:
+ samtools: version > 1.13, which contains `samtools coverage` function
+ bedtools

## Call read binning

```
python binning.py --out_dir=test --ref_fn=hg19.fa --ref_type=hg19 --bam_dir=test_bam --bam_suffix=*sorted.bam --bin_size=500000 
```

Running this command will takes all bam files under `out_dir` directory with specified `bam_suffix` pattern as input, and calculate the read coverage with specified `bin_size`. It also calculates the mean coverage and total number of mapped reads for each chromosome. 
