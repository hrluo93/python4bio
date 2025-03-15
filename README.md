# python4bio
1.selective-sweep-ggpopwind.py is used to identify selective sweep region using Fst+Pi_ratio and Dxy+Pi_ratio from https://github.com/simonhmartin/genomics_general popgenWindows.py output，note that the all-site vcf is needed.

Usage: python selective-sweep-ggpopwind.py -i popgenWindows-result.csv -o1 aares.csv -o2 popA-regionFstPi.csv -o3 popB-regionFstPi.csv -o4 popA-regiondxyPi.csv -o5 popB-regiondxyPi.csv 

2. Search false gene model in the longest protein Sequences from Gffread -y.
   
Usage: python false-gene-model.py -i input.longest.faa -o output.table

3. selective-sweep-vcftools.py is used to identify selective sweep region using Fst+Pi_ratio from the vcftools output.
   
   Before usage, covert negative Fst to 0 like "awk '{if($5<0) print $1"\t"$2"\t"$3"\t"0;else print $1"\t"$2"\t"$3"\t"$5}' XRT-MTS.windowed.weir.fst > XRT-MTS.windowed.weir.fst1" and change two Pi vcftools output files' line1 header col name PI to PIA and PIB (High pi ratio (low pi value) will be selected in PiB), respectively.

4. Ttest-Utest-permutation-bootstrap-pairedTtest.py

   T-test, U-test, permutation test, bootstrap test, and paired T-test all in one Python script.

5. sort_paml: Sort multiline (ParaAT) or interleaved paml.

6. gff_to_slim.py -i longest.transcipts.gff -g chrlen.g > gff.slim.input  (where -g chrlen.g from cut -f 1,2 genome.fai)
