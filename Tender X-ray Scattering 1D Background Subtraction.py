# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:47:38 2024

@author: Yunfei Wang & Ka Hung Chan

"""



################################################################################################################################################
###                                                                                                                                          ###
###   This code is used to loop through subtraction factors during SAXS background subtraction.                                              ###
###   It can subtract the background for all samples simultaneously. The results for each sample will be saved in its respective folder.     ###
###   The sections of the code that need revision for your specific background subtraction tasks are clearly labeled.                        ###
###   (numbered, totally 5 steps).                                                                                                           ###
###                                                                                                                                          ###
################################################################################################################################################


import matplotlib.pyplot as plt
import numpy as np
import os


"""
load raw 1D data for samples and background

"""

##   Step 1. revise here for data path 
############################################################################################################################################
raw_1d_file_path = r'C:\Users\ywang14\Dropbox\Yunfei Wang\1-Research\#4_solution_tender_x-ray\beamtime 20220717\Solution tender\309388_Wang_07\900KW\processed'  #Path for all raw 1d data, including sample and background
subtraction_path = r'C:\Users\ywang14\Dropbox\Yunfei Wang\1-Research\#4_solution_tender_x-ray\beamtime 20220717\Solution tender\309388_Wang_07\900KW\processed\test' #Path for saving subtracted results 
############################################################################################################################################


### Step 2.revise here to pick up sample ###
############################################################################################################################################
raw_1d_files = [f for f in sorted(os.listdir(raw_1d_file_path)) if 'PffBT4T1_TMB_1' in f and f.endswith('.txt')]  
############################################################################################################################################


### Step 3. revise here to pick up bkg profile ###
############################################################################################################################################
bkg_1D = 'YW_TMB1_2_2460.00eV_temp055.6degC_wa00.0_sdd8.3m_i_1D_data.txt' # Define the background 1D file (Solvent profile here)
############################################################################################################################################

def load_1d_data(file_path):
    return np.loadtxt(file_path, unpack=True)

bkg_1D_path = os.path.join(raw_1d_file_path, bkg_1D)
q2, I2 = load_1d_data(bkg_1D_path)
os.makedirs(subtraction_path, exist_ok=True)


file_path = os.path.join(raw_1d_file_path, bkg_1D)
print(file_path)
print(os.path.exists(file_path))

"""
Loop background subtraction factors

"""

for i, sample in enumerate(raw_1d_files):
    print(i)
    if sample == bkg_1D:
        continue
    
    sample_path = os.path.join(raw_1d_file_path, sample)
    q1, I1 = load_1d_data(sample_path)

    if not np.array_equal(q1, q2):  
        raise ValueError(f"The q-values in the two files do not match: {sample} and {bkg_1D}")        # Ensure the q-values match


    
    sample_folder = os.path.join(subtraction_path, f'{os.path.splitext(sample)[0]}_results') # Create a new directory for each file1 inside the subtraction path
    os.makedirs(sample_folder, exist_ok=True)


### Step 4. revise here to pick up range of bkg subtraction factors. 
############################################################################################################################################
    factors = np.arange(0.01, 0.5, 0.05)  # Perform the subtraction with diffe"rent factors
############################################################################################################################################


    I_diff_factors = {factor: I1 - factor * I2 for factor in factors}

    for factor in factors:      # Save the subtracted 1D data individually
        output_subtracted_file = os.path.join(sample_folder, f'subtracted_1D_data_{factor:.2f}.txt')
        np.savetxt(output_subtracted_file, np.column_stack((q1, I_diff_factors[factor])), header='q (A^{-1})    Intensity (a.u.)')
        print(f"Subtracted 1D data saved as {output_subtracted_file}")
        
        
    plt.figure(figsize=(16, 10))  # Increase the figure size
    plt.plot(q1, I1, label=f'Sample: {sample}', color='blue')
    plt.plot(q2, I2, label=f'background: {bkg_1D}', color='green')
    colors = plt.cm.viridis(np.linspace(0, 1, len(factors)))  # Use a colormap for different colors
    for factor, color in zip(factors, colors):
        plt.plot(q1, I_diff_factors[factor], label=f'Subtraction factor: {factor:.2f}; sample - {factor:.2f} * background', color=color)

### Step 5. revise here to change x range and y range during plotting. ###
############################################################################################################################################
    plt.xlim(0.004, 2)
    plt.ylim(1E1, 1E8)
############################################################################################################################################


    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('q (A^{-1})')
    plt.ylabel('Intensity (a.u.)')
    plt.legend()
    plt.title(f'Comparison of 1D Data and Subtraction Results: {sample} vs {bkg_1D}')
    plt.tight_layout()
    plt.show()
    output_combined_file = os.path.join(sample_folder, f'subtracted_1D_data_{factor:.2f}.png')
    plt.savefig(output_combined_file, dpi=300, bbox_inches='tight')
    print(f"Combined 1D plot {output_combined_file}")
#   plt.close()

print('Done')
