# SCAN


## Call CNV read binning

### Prerequisites

The following tools must be installed:
+ samtools: version > 1.13, which contains `samtools coverage` function
+ bedtools

Please call CNV read binning for all normal and tumor samples.

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

Running this command will take all bam files under `out_dir` directory with specified `bam_pattern` pattern as input, and calculate the read coverage with specified `bin_size`. It also calculates the mean coverage and total number of mapped reads for each chromosome. 

## Call somatic SV

### Prerequisites

The following tools must be installed:
+ svaba, https://github.com/walaj/svaba
+ manta, https://github.com/Illumina/manta

Call somatic sv from svaba
```
wget "https://data.broadinstitute.org/snowman/dbsnp_indel.vcf" ## get a DBSNP known indel file
DBSNP=dbsnp_indel.vcf
CORES=8 ## set any number of cores
REF=/seq/references/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta
## -a is any string you like, which gives the run a unique ID
svaba run -t $TUM_BAM -n $NORM_BAM -p $CORES -D $DBSNP -a somatic_run -G $REF
```

Please keep all output from svaba, then run `parse_svaba.py` for all vcf file.
```
parse_svaba.py call --sv_fn=sv_vcf_file
```

Call somatic sv from manta
```
python configManta.py \
--normalBam ${data_dir}/NG19-GXH0818-gDNA.sorted.bam \
--tumorBam ${data_dir}/NG19-GXH0818-FFPE.sorted.bam \
--referenceFasta ${ref} \
--runDir ${work_dir}
```
Please keep all output from manta, then run `parse_manta.py` for all vcf file.
```
parse_manta.py call --sv_fn=sv_vcf_file
```

Cluster SVs based on breakpoint distance, and divide SV information into different groups.

``` 
python ~/Ambigram/script/bfb_scripts.py cluster_sv -sv [path to SV file]
```
Generate segments according to SV breakpoints, and extract coverage depth of segments from the corresponding BAM file.

``` 
python ~/Ambigram/script/bfb_scripts.py generate_seg -sv [path to SV file] -bam [path to BAM file] 
```

Given a set of regions, call coverage depth of each base from a BAM file for drawing a cvoerage distribution plot.
``` 
python ~/Ambigram/script/bfb_scripts.py call_depth -seg [path to SEG file] -bam [path to BAM file] 
```
Generate the input file (.lh file) of Ambigram by integrating sv.txt and seg.txt files. (to be updated under Ambigram/script)
``` 
python ~/SVAS/scripts/csv_sv.py call --sv_fn=[path to SV file] --seg_fn=[path to SEG file] --seg_only=1 --bfb_sv=1 
```
Install Ambigram and run the program with .lh file to reconstruct BFB haplotypes. Please refer to https://github.com/deepomicslab/Ambigram.
