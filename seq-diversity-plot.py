"""
Author: Priyanshu R Gupta
Date: 06/13/2024

Description:
This script reads in a fasta file containing the sequences generated using ProteinMPNN (or any other fasta dataset) 
and plots a heatmap showing the frequency of each amino acid at each position in the sequences.

Usage:
python3 seq-diversity-plot.py <filename>

Example:
python3 seq-diversity-plot.py sequences.fasta

Dependencies:
numpy, pandas, matplotlib, seaborn, questionary, os, argparse
"""

# IMPORTING DEPENDENCIES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import questionary
import os
import argparse


# DEFINING THE DRIVER FUNCTIONS
def read_fasta(filename):
    with open(filename,"r") as file:
        lines = file.readlines()
    return lines

def get_sequences(lines):
    sequences = []
    for line in lines:
        if line[0] != ">":
            sequences.append(line.strip())
    sequence_length = len(sequences[0])
    return sequences, sequence_length

def defining_amino_acids():
    amino_acids = list("ACDEFGHIKLMNPQRSTVWY")
    return amino_acids

def get_occurences_in_a_dataframe(sequences, sequence_length, amino_acids):
    df = pd.DataFrame([list(seq) for seq in sequences])
    occurrences = pd.DataFrame(0, index=amino_acids, columns=range(sequence_length))
    for i in range(sequence_length):
        occurrences[i] = df[i].value_counts()
    return occurrences

def plot_heatmap(occurrences):
   # Plotting the heatmap
    plt.figure(figsize=(15, 8))
    sns.heatmap(occurrences, cmap='viridis', cbar=True, linewidths=.5, linecolor='black')
    plt.title('Frequency of Amino Acids at Each Position in Sequences')
    plt.xlabel('Index Position')
    plt.ylabel('Amino Acid')
    plt.show()
    answer = questionary.confirm("Do you want to save the plot?").ask()
    if answer:
        path = questionary.path("Enter the path to save the plot. Press ENTER to for default. [default = './heatmap.png']").ask()
        if os.path.isdir(path):
            print(f"Path exists. Saving the plot to '{path}/heatmap.png'")
            plt.savefig(f"{path}/heatmap.png")
        else:
            print(f"Path does not exist. Saving the plot to '{os.getcwd()}/heatmap.png'")
            plt.savefig("heatmap.png")

# MAIN FUNCTION
def main():
    parser = argparse.ArgumentParser(description='Process a filename.')
    parser.add_argument('filename', type=str, help='Name of the file to process')
    args = parser.parse_args()    
    filename = args.filename
    lines = read_fasta(filename)
    sequences, sequence_length = get_sequences(lines)
    list_of_amino_acids = defining_amino_acids()
    occurences = get_occurences_in_a_dataframe(sequences, sequence_length, list_of_amino_acids)
    plot_heatmap(occurences)


if __name__ == "__main__":
    main()
