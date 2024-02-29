import argparse
import pandas as pd

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input popgenWindows file path')
parser.add_argument('-o1', '--output_file1', help='Output file path for merged dataframe')
parser.add_argument('-o2', '--output_file2', help='Output file path for populationA selected regions(Fst)')
parser.add_argument('-o3', '--output_file3', help='Output file path for populationB selected regions(Fst)')
parser.add_argument('-o4', '--output_file4', help='Output file path for populationA selected regions(Dxy)')
parser.add_argument('-o5', '--output_file5', help='Output file path for populationB selected regions(Dxy)')
args = parser.parse_args()

#scaffold	start	end	mid	sites	pi_popA	pi_popB	dxy_popA_popB	Fst_popA_popB
# Input the merged dataframe
merged_df = pd.read_csv(args.input, sep=',', header=1, names=['scaffold', 'start', 'end', 'mid', 'sites', 'pi_popA','pi_popB', 'dxy_popA_popB', 'Fst_popA_popB'])

# Calculate the pi ratio
merged_df['pi_Ratio'] = merged_df['pi_popA'] / merged_df['pi_popB']

# Rearrange the columns in the merged dataframe
merged_df = merged_df[['scaffold', 'start', 'end', 'mid', 'sites', 'pi_popA','pi_popB', 'dxy_popA_popB', 'Fst_popA_popB', 'pi_Ratio']]

# Write the merged dataframe to the output file
merged_df.to_csv(args.output_file1, sep=',', index=False)



# Filter the dataframe based on top 5% WEIGHTED_FST and top 5% pi_Ratio
top_fst_threshold = merged_df['Fst_popA_popB'].quantile(0.95)
top_pi_ratio_threshold = merged_df['pi_Ratio'].quantile(0.95)
filteredB_df = merged_df[(merged_df['Fst_popA_popB'] >= top_fst_threshold) & (merged_df['pi_Ratio'] >= top_pi_ratio_threshold)]

# Filter the dataframe based on top 5% WEIGHTED_FST and low 5% pi_Ratio
low_pi_ratio_threshold = merged_df['pi_Ratio'].quantile(0.05)
filteredA_df = merged_df[(merged_df['Fst_popA_popB'] >= top_fst_threshold) & (merged_df['pi_Ratio'] <= low_pi_ratio_threshold)]

# Write the filtered dataframe to the output file
filteredA_df.to_csv(args.output_file2, sep=',', index=False)
filteredB_df.to_csv(args.output_file3, sep=',', index=False)

#top 5% Dxy
top_dxy_threshold = merged_df['dxy_popA_popB'].quantile(0.95)

# Filter the dataframe based on top 5% Dxy and top 5% pi_Ratio
filteredBdxy_df = merged_df[(merged_df['dxy_popA_popB'] >= top_dxy_threshold) & (merged_df['pi_Ratio'] >= top_pi_ratio_threshold)]

# Filter the dataframe based on top 5% Dxy and low 5% pi_Ratio
filteredAdxy_df = merged_df[(merged_df['dxy_popA_popB'] >= top_dxy_threshold) & (merged_df['pi_Ratio'] <= low_pi_ratio_threshold)]

# Write the filtered dataframe to the output file
filteredAdxy_df.to_csv(args.output_file4, sep=',', index=False)
filteredBdxy_df.to_csv(args.output_file5, sep=',', index=False)

print("Top 5% FST threshold value:", top_fst_threshold)
print("Top 5% Dxy threshold value:", top_dxy_threshold)
print("Low 5% pi_Ratio threshold value(for populationA):", low_pi_ratio_threshold)
print("Top 5% pi_Ratio threshold value(for populationB):", top_pi_ratio_threshold)

