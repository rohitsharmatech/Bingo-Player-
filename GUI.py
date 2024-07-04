'''
THIS IS THE CODE FOR RUNNING GUI

You can also run this code on terminal by going to the end of run_on_terminal.py file
'''
from tkinter import *
import tkinter as tk
from tkinter import ttk
#Importing all the functions from logic_bingo.py file
from logic_bingo import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandastable import Table, TableModel
import matplotlib.pyplot as plt

'''
Making a root/window of the GUI
'''
root = Tk()
root.title("Bingo Card Generator and Analyzer") #This is the title of our user-window
root.geometry("1000x600")  # Window size

header_label = Label(root, text="Bingo Card Generator and Analyzer", font=("Helvetica", 16))
header_label.pack(pady=10)

#Asking user the number of cards to be generated
Label(text="Number of Cards:").pack() 
num_cards_entry1 = Entry(root)
num_cards_entry1.pack()

#Asking user the number of Simulations to be carried out
Label(text="Number of Simulations:").pack()
num_simulations_entry1 = Entry(root)
num_simulations_entry1.pack()

#Asking user the number of cards to be called
Label(text="Number of cards called:").pack()
num_cards_called1 = Entry(root)
num_cards_called1.pack()

analysis_frame = Frame(root)
analysis_frame.pack(side = RIGHT, fill="both", expand=True)

# Export Section
export_frame = LabelFrame(root, text="Export Options", padx=10, pady=10)
export_frame.pack(fill="x", padx=10, pady=10)

# Status Bar
status_bar = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
status_bar.pack(side="bottom", fill="x")

'''
The following function runs the simulations
'''
def run_simulations():
    num_cards_entry = num_cards_entry1.get()
    num_simulations_entry = num_simulations_entry1.get()
    num_cards_called = num_cards_called1.get()

    try:
    # Here we are checking whether the input provided by user is an integer or not.
        num_cards_entry_int = int(num_cards_entry)
        num_simulations_entry_int = int(num_simulations_entry)
        num_cards_called_int = int(num_cards_called)
    except ValueError:
    # If the input is not integer then we print "Invalid Input"
        print("Invalid input. Please enter an integer.")
    bingo_counts, fullhouse_counts, num_cards, cards_original = main_code(num_cards_entry, num_simulations_entry)
    
    
    status_bar.config(text="Generated Cards and simulations completed")
    return bingo_counts, fullhouse_counts, num_cards, cards_original
    
def run_analysis():
    # Placeholder for run analysis
    num_cards_entry = num_cards_entry1.get()
    num_simulations_entry = num_simulations_entry1.get()
    num_cards_called = num_cards_called1.get()

    try:
    # Here we are checking whether the input provided by user is an integer or not.
        num_cards_entry_int = int(num_cards_entry)
        num_simulations_entry_int = int(num_simulations_entry)
        num_cards_called_int = int(num_cards_called)
    except ValueError:
    # If the input is not integer then we print "Invalid Input"
        print("Invalid input. Please enter an integer.")
    global bingo_counts
    global fullhouse_counts
    global cards_original
    bingo_counts, fullhouse_counts, num_cards, cards_original = main_code(num_cards_entry_int,num_simulations_entry_int)
    fig = visualise_results(bingo_counts, fullhouse_counts)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side = LEFT)
    
    bingo_at_x,x,df = centrality_figures(num_cards_called_int, bingo_counts)
    fig1 = histo(bingo_at_x,x,df)
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side = RIGHT)
    status_bar.config(text="Analysis Displayed")

'''
The following function exports the cards to PDF when clicked on the button.
'''
def export_cards():
    cards_to_pdf(cards_original)
    #Placeholder for export results logic
    status_bar.config(text="Cards Exported")

'''
This function takes arrays of bingo counts and full houses for each simulation
It then makes a line graph for each of the bingo and full house counts at each number called
x axes consist of the number of numbers called and y axis consist of number of players
or bingo cards that reached bingo at each of the numbers called.
There is also minimum and maximum value for each of the bingo count and full house count at 
that particular number called.
'''

def visualise_results(bingo_counts, fullhouse_counts):    
    avg_bingo = bingo_counts.mean(axis=0)
    avg_fullhouse = fullhouse_counts.mean(axis=0)

    std_bingo = bingo_counts.std(axis=0)
    std_fullhouse = fullhouse_counts.std(axis=0)

    min_bingo = bingo_counts.min(axis=0)
    max_bingo = bingo_counts.max(axis=0)
    min_fullhouse = fullhouse_counts.min(axis=0)
    max_fullhouse = fullhouse_counts.max(axis=0)
    # Creating a simple Matplotlib plot
    fig = plt.Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    # Ploting the averages
    ax.plot(avg_bingo, label="Average BINGO")
    ax.plot(avg_fullhouse, label="Average Full-House")

    # Shading the area which shows standard deviations
    ax.fill_between(range(75), avg_bingo-std_bingo, avg_bingo+std_bingo, color='blue', alpha=0.2)
    ax.fill_between(range(75), avg_fullhouse-std_fullhouse, avg_fullhouse+std_fullhouse, color='orange', alpha=0.2)

    # Plotting min and max
    ax.plot(min_bingo, 'b--', label="Min BINGO")
    ax.plot(max_bingo, 'b--', label="Max BINGO")
    ax.plot(min_fullhouse, 'r--', label="Min Full-House")
    ax.plot(max_fullhouse, 'r--', label="Max Full-House")

    ax.set_xlabel("Number of numbers called")
    ax.set_ylabel("Number of cards")
    ax.legend()
    ax.set_title("Bingo and Full-House analysis over 100 simulations")
    #ax.grid(True)
    fig.patch.set_linewidth(3)
    fig.patch.set_edgecolor('pink')
    fig.tight_layout()

    return fig
    
#Buttons 
simulate_button = Button(analysis_frame, text="Play Bingo and Show Analysis", command=run_analysis) #Analysis report is displayed when user clicks on this button
export_button = Button(text="Export Cards as PDF", command=export_cards)  #A pdf of cards is generated when the user clicks on this button

simulate_button.pack()
export_button.pack()

root.mainloop()