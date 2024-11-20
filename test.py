import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import mplcursors

# Initialize a global DataFrame
df = None

def open_file():
    global df
    # Get the current working directory (project's directory)
    project_dir = os.getcwd()
    
    # Open file dialog starting in the project directory
    file_path = filedialog.askopenfilename(
        title="Select a file",
        initialdir=project_dir,
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    
    if file_path:
        # Load the selected file into a DataFrame
        df = pd.read_csv(file_path,skiprows=5)
        print("File loaded successfully!")
        print("Headers:", df.columns.tolist())
        
        # Update the dropdown menu with the column headers
        update_dropdown()

def update_dropdown():
    # Clear existing options in the dropdown
    dropdown.delete(0, tk.END)
    for col in df.columns:
        dropdown.insert(tk.END, col)  # Add columns to Listbox
    dropdown.select_set(0)  # Set default selection

def select_columns():
    # Get the selected columns from the Listbox
    selected_columns = [dropdown.get(i) for i in dropdown.curselection()]
    if selected_columns:
        print(f"Selected columns: {selected_columns}")
        plot_column(selected_columns)

def plot_column(column_names):
    # Clear the plot area if a plot already exists
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 4))

    # Loop through the selected columns and plot them
    for column_name in column_names:
        ax.plot(df[column_name], linestyle='-', linewidth=1, label=column_name)  # Plot each column
    
    # Set plot title and labels
    ax.set_title("Interactive Plot of Selected Columns")
    ax.set_xlabel("Index")
    ax.set_ylabel("Values")
    ax.legend()  # Show legend with column names
    
    # Add interactivity with mplcursors (hover over points to see values)
    mplcursors.cursor(ax, hover=True)
    
    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    
    toolbar = NavigationToolbar2Tk(canvas, plot_frame)
    toolbar.update()
    toolbar.pack()

# Create the main application window
app = tk.Tk()
app.title("File Opener and Column Selector")
app.geometry("800x600")  # Set a larger default size for the window

# Add a button to open the file dialog
open_button = tk.Button(app, text="Open File", command=open_file)
open_button.pack(pady=10)

# Add a Listbox (with multiple selection) for column selection
dropdown = tk.Listbox(app, selectmode=tk.MULTIPLE, height=5)
dropdown.pack(pady=10)

# Add a button to select columns and plot them
select_button = tk.Button(app, text="Select Columns and Plot", command=select_columns)
select_button.pack(pady=10)

# Add a frame to display the plot
plot_frame = tk.Frame(app)
plot_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Run the application
app.mainloop()