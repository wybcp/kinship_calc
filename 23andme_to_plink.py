#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pathlib

CHROMOSOME_TABLE = {'X': '23', 'Y': '24', 'XY': '25', 'MT': '26'}
GENDER_TABLE = {'male': '1', 'female': '2'}
PHENOTYPE = '-9'

# Determine the path and optionally the gender.
parser = argparse.ArgumentParser()
parser.add_argument('path', type = str)
parser.add_argument('--gender', type = str, nargs = '?')
args = parser.parse_args()

gender = GENDER_TABLE.get(args.gender, '0')


# Open the genome file for reading.
with open(args.path, 'r') as genome_file:
    # Create the PED file and write its header.
    root, _ = os.path.splitext(args.path)
    with open(root + '.ped', 'w') as ped_file:
        ped_file.write(
            '{0}_FAM {0} {0}_FATHER {0}_MOTHER {1} {2}'.
                format(root, gender, PHENOTYPE))

        # Create the map file.
        with open(root + '.map', 'w') as map_file:

            # Loop over every line of the genome file, skipping comments.
            for line in genome_file:
                if len(line) == 0 or line[0] == '#':
                    continue

                # Decompose the line, and transform the fields if necessary.
                rsid, chromosome, position, genotype = line.split()
                chromosome = CHROMOSOME_TABLE.get(chromosome, chromosome)
                genotype = genotype.ljust(2, genotype[0]).replace('-', '0')

                # Write the map and ped file data.
                map_file.write('{0}\t{1}\t0\t{2}\n'.format(chromosome, rsid, position))
                ped_file.write(' {0} {1}'.format(genotype[0], genotype[1]))
