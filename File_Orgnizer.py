#!/usr/bin/env python
# coding: utf-8

# In[2]:


# version for execution in the desktop App called "file orgnizer"
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog
# ==========================
# Constants
# ==========================

CATEGORIES = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",

    ".pdf": "PDF",

    ".mp4": "Videos",

    ".mp3": "Music",

    ".docx": "Word",
    ".doc": "Word",

    ".xlsx": "Excel",
    ".xls": "Excel",

    ".exe": "Exe_files",
}

# ==========================
# Functions
# ==========================

# A function to select a folder
def browse_folder():            
    folder = filedialog.askdirectory() # To browse the folder
    if folder:
         # Clearing previous content
        entry_path.delete(0, tk.END)
        # Insert new content
        entry_path.insert(0,folder)
        label_display.config(text="")
        
        
# Function to check the uniqueness of transferred filenames 
def get_unique_filename(destination_folder: Path, file_name: str) -> Path:
    """
    If a file with the same name exists,
    it finds the first available name.
    This function ultimately returns an object of type Path.
    """

    original_file = destination_folder / file_name

    if not original_file.exists():        # If there is no file with the same name
        return original_file

    stem = original_file.stem
    suffix = original_file.suffix

    counter = 1

    while True:

        new_name = f"{stem} ({counter}){suffix}"
        new_path = destination_folder / new_name

        if not new_path.exists():
            return new_path

        counter += 1
        
# An intermediary function to convert the selected folder address into a Path type.        
def start_sorting():
    
    folder = Path(entry_path.get())

    sort_folder(folder) 
    
# Main folder sorting function    
def sort_folder(folder: Path) -> None:
    """
    Sorts the files in the folder by extension
    """

    total_files = 0

    for item in folder.iterdir():

        if not item.is_file():
            continue

        category = CATEGORIES.get(item.suffix.lower(), "Others")

        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination_file = get_unique_filename(
            destination_folder,
            item.name
        )

        try:
            shutil.move(item, destination_file)
            total_files += 1
            

            

        except Exception as e:
            print(f"✗ Error moving {item.name}")
            label_display.config(text=f"✗ Error moving {item.name}")
            print(e)
            
        label_display.config(text=f"Finished! {total_files} file(s) sorted.")
# ==========================
# Phase2 GUI & Window Structure
# ==========================
# Create a new window .
root = tk.Tk() 
# window title
root.title("File Organizer")
# window dimension
root.geometry("500x250")
# Create a label for showing the folder address
label_folder = tk.Label(root, text="Folder:")
# Entry to display the folder address
entry_path = tk.Entry(root, bd =5,width=50, justify=tk.LEFT,)
# Create a button called Browse for selectiong the folder for sorting
button_browse=tk.Button(root, text="Browse", command=browse_folder) 
# Create a button called Sort File for sorting the files in the selected folder 
button_sort=tk.Button(root, text="Sort Files", command=start_sorting)
# creating a label for Stautus bar
label_status = tk.Label(root, text="Status:")
# Creating a label for showng the ready or not
label_display = tk.Label(root, text="", bg="lightgray")

#  Arrange widgets using grid layout
label_folder.grid(row=0, column=0)
entry_path.grid(row=1, column=1)
button_browse.grid(row=1, column=2)
button_sort.grid(row=2, column=1 )
label_status.grid(row=3, column=0)
label_display.grid(row=3, column=1)

root.mainloop()

