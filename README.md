# python4bio
1.selective-sweep-ggpopwind.py is used to identify selective sweep region using Fst+Pi_ratio and Dxy+Pi_ratio from https://github.com/simonhmartin/genomics_general popgenWindows.py output，note that the all-site vcf is needed.

Usage: python selective-sweep-ggpopwind.py -i popgenWindows-result.csv -o1 aares.csv -o2 popA-regionFstPi.csv -o3 popB-regionFstPi.csv -o4 popA-regiondxyPi.csv -o5 popB-regiondxyPi.csv 

2. Search false gene model in the longest protein Sequences from Gffread.
   
Usage: python false-gene-model.py -i input.longest.faa -o output.table
