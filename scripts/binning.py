#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Coverage binning.

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
"""

import docopt
import os
import subprocess

hg19_chrom_size = '''
chr1,249250621
chr2,243199373
chr3,198022430
chr4,191154276
chr5,180915260
chr6,171115067
chr7,159138663
chr8,146364022
chr9,141213431
chr10,135534747
chr11,135006516
chr12,133851895
chr13,115169878
chr14,107349540
chr15,102531392
chr16,90354753
chr17,81195210
chr18,78077248
chr19,59128983
chr20,63025520
chr21,48129895
chr22,51304566
chrX,155270560
chrY,59373566
chrM,16571
'''

hg38_chrom_size = '''
chr1,248956422
chr2,242193529
chr3,198295559
chr4,190214555
chr5,181538259
chr6,170805979
chr7,159345973
chr8,145138636
chr9,138394717
chr10,133797422
chr11,135086622
chr12,133275309
chr13,114364328
chr14,107043718
chr15,101991189
chr16,90338345
chr17,83257441
chr18,80373285
chr19,58617616
chr20,64444167
chr21,46709983
chr22,50818468
chrX,156040895
chrY,57227415
chrM,16569
'''


def get_bin(ref, bin_size, bin_fn):
    print("---start getting genome-wide bins---")

    if ref == 'hg19':
        chrom_size = hg19_chrom_size
    else:
        chrom_size = hg38_chrom_size

    with open(bin_fn, 'w') as bin_f:
        bin_i = 0
        for line in chrom_size.split('\n'):
            if not line:
                continue
            chrom, size = line.split(',')
            size = int(size)
            if chrom not in chrs:
                continue
            for i in range(int(size/bin_size)+1):
                start = i*bin_size + 1
                end = start + bin_size - 1
                if end > size:
                    end = size
                bin_i += 1
                bin_f.write('{}\t{}\t{}\tbin_{}\n'.format(chrom, start, end, bin_i))


def get_bin_coverage(bam_fn, bam_fns, bin_fn, out_dir):
    print("---start getting bin coverage---")

    cov_bed_fn = os.path.join(out_dir, "bedtools_cov.bed")
    coverage_fn = os.path.join(out_dir, "bedtools_cov.tsv")

    # mapping quality
    cmd = 'bedtools multicov -bams {} -bed {} -q 60 > {}'.format(' '.join(bam_fns), bin_fn, cov_bed_fn)
    subprocess.call(cmd, shell=True)
    cmd = '(echo "chrom\tstart\tend\t{}"; cat {}) > {}'.format('\t'.join(bam_fns), cov_bed_fn, coverage_fn)
    subprocess.call(cmd, shell=True)
    cmd = 'rm {}'.format(cov_bed_fn)
    subprocess.call(cmd, shell=True)

    cov_bed_fn = os.path.join(out_dir, "samtools_cov.bed")
    coverage_fn = os.path.join(out_dir, "samtools_cov.tsv")

    # mapping quality
    cmd = 'samtools bedcov -Q 60 -j {} {} > {}'.format(bin_fn, bam_fn, cov_bed_fn)
    subprocess.call(cmd, shell=True)
    cmd = '(echo "chrom\tstart\tend\t{}"; cat {}) > {}'.format('\t'.join(bam_fns), cov_bed_fn, coverage_fn)
    subprocess.call(cmd, shell=True)
    cmd = 'rm {}'.format(cov_bed_fn)
    subprocess.call(cmd, shell=True)


def get_chrom_coverage(bam_fns, out_dir):
    print("---start getting chromsome coverage---")
    for bam_fn in bam_fns:
        _, fn = os.path.split(bam_fn)
        chrom_cov_fn = os.path.join(out_dir, fn + '.cov.tsv')
        # mapping quality
        cmd = 'samtools coverage -q 60 {} -o {}'.format(bam_fn, chrom_cov_fn)
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    out_dir = args['--out_dir']
    bam_fn = os.path.join(args['--bam_dir'], args['--bam_pattern'])
    bin_size = int(args['--bin_size'])
    ref = args['--ref']

    chrs = ['chr{}'.format(x) for x in range(22, 23)]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    bin_fn = os.path.join(out_dir, "bin.bed")
    res = subprocess.run('ls {}'.format(bam_fn), shell=True, stdout=subprocess.PIPE)
    bam_fns = res.stdout.decode().split('\n')[:-1]
    get_bin(ref, bin_size, bin_fn)
    get_bin_coverage(bam_fn, bam_fns, bin_fn, out_dir)
    get_chrom_coverage(bam_fns, out_dir)
