import tkinter as tk
from tkcalendar import Calendar
from tkinter import simpledialog
import os
import Browser as robo_browswer
import datetime

def show_input_box():
    ROOT = tk.Tk()
    ROOT.withdraw()  # Hide the Tkinter root window
    # The input dialog
    user_input = simpledialog.askstring(title="Input Box",
                                        prompt="Type a topic to investigate:")
    
    print(f"You entered: {user_input}")
    return user_input
class CalendarDialog(simpledialog.Dialog):
    def body(self, master):
        self.calendar = Calendar(master)
        self.calendar.pack()
    
    def apply(self):
        self.result = self.calendar.get_date()

def show_calendar_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    dialog = CalendarDialog(root, title="Select Date")
    return dialog.result


def create_folder_with_date(search_text):
    # Format the current date as YYYY-MM-DD
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    # Combine search_text and date to create a folder name
    folder_name = f"{search_text}_{date_str}"
    # Create the folder
    os.makedirs(folder_name, exist_ok=True)
    print(f"Folder '{folder_name}' created.")

if __name__ == '__main__':
    robo_browswer.Browser()
    
    

