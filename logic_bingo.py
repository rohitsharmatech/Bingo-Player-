'''
THIS IS THE CODE WITH BINGO LOGIC

If you want to play bingo on GUI, then run the GUI.py file
'''

#Importing libraries
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats
from tabulate import tabulate
from scipy.stats import skew, kurtosis
import tkinter as tk  
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Generating a single bingo card with 5 rows and columns
def generate_card():
    card = []
    # Number generation for each column
    for i in range(5):
        start, end = i * 15 + 1, (i + 1) * 15  #To ensure that first column has numbers between 1 to 15 and so on
        col = random.sample(range(start, end+1), 5)  #Randomly assignming the numbers
        card.append(col)
    # Making the middle cell "FREE"
    card[2][2] = "FREE"
    card = [list(l) for l in zip(*card)] #To make sure that every card in the list is zipped
    return card
    
def card_to_string(card):
    #Checking whether a card is unique by converting it into string.
    return "\n".join(["\t".join(map(str, row)) for row in card])
    
''' This function will generate n unique Bingo cards.
    Input = number of cards to be generated
    Output = Cards generated
'''
def generate_n_unique_cards(n):
    cards = set()
    while len(cards) < int(n):
        card = generate_card()
        card_str = card_to_string(card)
        card_str = card_str.replace("FREE","101")
        if card_str not in cards:
            cards.add(card_str)

    # Converting the set of strings back to list of cards
    return [list(map(lambda x: list(map(int, x.split("\t"))) if "FREE" not in x.split("\t") else ["FREE"], card.split("\n"))) for card in cards]

#Simulation
#This function checks if after each turn, they have a bingo
def check_bingo(card):
    # Check rows
    c = 0
    for i in range(5):
        for cell in card[i]:
            if cell == 'FREE':
                c += 1    
        if c%5 == 0 and c > 0:
            return True
        else:
            c = 0
              
    #Check Columns
    for i in range(5):
        for j in range(5):
            if card[j][i] == 'FREE':
                c+=1
        if c%5 == 0 and c > 0:
            return True
        else: 
            c = 0
            
    # Check diagonals
    for i in range(5):
        if card[i][i] == 'FREE':
            c+=1
        if c%5 == 0 and c > 0:
            return True
        else: 
            c = 0
    
    #For second diagonal
    for i in range(5):
        if card[i][4-i] == 'FREE':
            c+=1
        if c%5 == 0 and c > 0:
            return True
        else: 
            return False        
            
            
'''Function to make dummy cards
The purpose of this function is to make the same number 
of dummy cards as the number chosen by the user.

This is to keep the original cards intact throughout
the number of simulations as chosen by the user'''

def generate_dummy_cards(num):
    dummy_cards = []
    for i in range(num):
        base = [0,0,0,0,0]
        dummy_card=[]
        for i in range(5):
            dummy_card.append(base)
        dummy_card = [list(base) for base in zip(*dummy_card)]
        dummy_card[2][2] = "FREE"
        dummy_cards.append(dummy_card)
    return dummy_cards
    
'''This function checks the number of fullhouse'''    
def check_fullhouse(card):
    return sum([1 for row in card for cell in row if isinstance(cell, int)]) == 0
    
'''
This function runs a simulation.
Input: the bingo cards and number of cards in total
Output: two lists with number of bingos and full houses at every number called
'''
def simulate_game(cards, nums):
    numbers = list(range(1, 76))
    random.shuffle(numbers)
    bingo_count = [0] * 75      #Making a row for bingo counts
    fullhouse_count = [0] * 75  #Making a row for full house counts
    bingo_dict = {}             #dictionary for bingo cards
    fullhouse_dict = {}         #dictionary for full house cards
    
    
    dummy_cards = generate_dummy_cards(nums) #Making dummy cards to keep original cards intact
    for i in range(0,nums):
        bingo_dict[str(i)] = 0
        fullhouse_dict[str(i)] = 0
    idx = 0     #checker for rows
    for num in numbers:
        idy = 0 #checker for columns
        for card in cards:
            card_dummy = dummy_cards[idy]
            for i in range(5):
                for j in range(5):
                    if card[i][j] == num:
                        card_dummy[i][j] = "FREE"
                        if check_bingo(card_dummy):
                            bingo_dict[str(idy)] = 1
                        if check_fullhouse(card_dummy):
                            fullhouse_dict[str(idy)] = 1
            idy+=1
        bingo_count[idx] = sum(bingo_dict.values())
        fullhouse_count[idx] = sum(fullhouse_dict.values())
        idx+=1
                           
    return bingo_count, fullhouse_count
    
'''Checking if the inputted number is an integer or not '''
def check_num(num):
    if num.isdigit():
        num = int(num)
        if num <= 75 and num >= 0:
            return True
    else:
        print("Enter a valid number")
        return False
        
''' This function takes input as number of cards and
number of simulations and returns numpy array of each
simulation as well as original cards
'''        
def main_code(n_cards, n_simulation):    
    bingo_counts = []
    fullhouse_counts = []
    
    n_cards = int(n_cards)
    cards_original = generate_n_unique_cards(n_cards)    #Generating number of cards chosen by the user
    
    #Making the middle cell FREE
    for c in cards_original:
        c[2][2] = "FREE"
    n_simulation = int(n_simulation)
    
    #Sending the cards for simulation
    for i in range(n_simulation): 
        cards_copy = [card.copy() for card in cards_original]
        bingo_count, fullhouse_count = simulate_game(cards_copy,n_cards)  #Getting the results for each simulation
        bingo_counts.append(bingo_count)                                  #For every simulation a new list is added with count of bingo at each turn
        fullhouse_counts.append(fullhouse_count)
    #Converting both lists into a numpy array
    bingo_counts = np.array(bingo_counts)
    fullhouse_counts = np.array(fullhouse_counts)
    return bingo_counts, fullhouse_counts, n_cards, cards_original
def visualise_results(bingo_counts, fullhouse_counts):    
    # PART 3: Analyze and visualize

    avg_bingo = bingo_counts.mean(axis=0)
    avg_fullhouse = fullhouse_counts.mean(axis=0)

    std_bingo = bingo_counts.std(axis=0)
    std_fullhouse = fullhouse_counts.std(axis=0)

    min_bingo = bingo_counts.min(axis=0)
    max_bingo = bingo_counts.max(axis=0)
    min_fullhouse = fullhouse_counts.min(axis=0)
    max_fullhouse = fullhouse_counts.max(axis=0)

    plt.figure(figsize=(12, 6))

    # Plot averages
    plt.plot(avg_bingo, label="Average BINGO")
    plt.plot(avg_fullhouse, label="Average Full-House")

    # Shade standard deviations
    plt.fill_between(range(75), avg_bingo-std_bingo, avg_bingo+std_bingo, color='blue', alpha=0.2)
    plt.fill_between(range(75), avg_fullhouse-std_fullhouse, avg_fullhouse+std_fullhouse, color='orange', alpha=0.2)

    # Plot min and max
    plt.plot(min_bingo, 'b--', label="Min BINGO")
    plt.plot(max_bingo, 'b--', label="Max BINGO")
    plt.plot(min_fullhouse, 'r--', label="Min Full-House")
    plt.plot(max_fullhouse, 'r--', label="Max Full-House")

    plt.xlabel("Number of numbers called")
    plt.ylabel("Number of cards")
    plt.legend()
    plt.title("Bingo and Full-House analysis over 100 simulations")
    plt.tight_layout()
    plt.show()

#For data handling, we check if the input is integer and within the specified range 
def check_number_called(num):
    if num.isdigit():
        num = int(num)
        if num <= 75 and num >= 0:
            return True
        else:
            print("Enter a number between 0 and 75")
            return False
    else:
        print("Enter a valid number")
        return False
   
''' This function generates a dataframe of centrality figures
Input: number of numbers called, array of all bingo counts at each number called
Output: dataframe with centrality figures'''   
def centrality_figures(number_called, bingo_counts):
    bingo_at_number_called = bingo_counts[:, number_called]
    df = pd.DataFrame.from_dict({'Centrality Figure':['Median','25th Percentile','75th Percentile','Skewness','Excess Kurtosis','Mode','Data Range','Data Variance','Data Std Dev'], 'Value': [ np.median(bingo_at_number_called),np.percentile(bingo_at_number_called, 25),np.percentile(bingo_at_number_called, 75),skew(bingo_at_number_called),kurtosis(bingo_at_number_called),stats.mode(bingo_at_number_called),np.ptp(bingo_at_number_called),np.var(bingo_at_number_called),np.std(bingo_at_number_called)] })
    return bingo_at_number_called,number_called,df

# Creating a Histogram
def histo(bingo_at_number_called,number_called,df):
    fig, ax = plt.subplots(2)
    
    ax[0].hist(bingo_at_number_called, bins=20, edgecolor="k", alpha=0.7)
    ax[0].set_title(f"Histogram of BINGOs after {number_called} numbers called")
    ax[0].set_xlabel("Number of BINGOs")
    ax[0].set_ylabel("Frequency")

# hide axes
    ax[1].table(cellText=df.values, colLabels=df.columns, loc='center')
    fig.patch.set_linewidth(3)
    fig.patch.set_edgecolor('cornflowerblue')
    fig.tight_layout()
    return fig 
    
#Generating PDF of Cards
from fpdf import FPDF

def cards_to_pdf(cards):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for card in cards:
        pdf.add_page()
        for row in card:
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=" | ".join(map(str, row)), ln=True, align="C")
    pdf.output('new_file.pdf')


def run_on_terminal():
    n_cards = input("HOW MANY CARDS?")
    while check_num(n_cards) ==False:
        n_cards = input("HOW MANY CARDS?")
        
    n_simulation = input("HOW MANY SIMULATIONS?")
    while check_num(n_simulation) ==False:
        n_simulation = input("HOW MANY SIMULATIONS?")

    bingo_counts, fullhouse_counts, n_cards, cards_original = main_code(n_cards,n_simulation)
    visualise_results(bingo_counts,fullhouse_counts)
    
    number_called = input("HOW MANY NUMBERS CALLED?")
    while check_number_called(number_called) ==False:
        number_called = input("Enter a valid number")
    number_called = int(number_called)
    
    bingo_at_number_called,number_called,df = centrality_figures(number_called, bingo_counts)
    
    fig = histo(bingo_at_number_called,number_called,df)
    fig.show()
    plt.pause(5)