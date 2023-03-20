import tkinter as tk
from tkinter import filedialog, ttk
from utils.SysmacData import SysmacData


class SysmacDataGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Sysmac Data Converter')

        self.file_name = tk.StringVar()

        self.select_file_button = tk.Button(self.master, text='Select File', command=self.select_file)
        self.select_file_button.grid(row=0, column=0, padx=5, pady=5)

        self.file_label = tk.Label(self.master, textvariable=self.file_name)
        self.file_label.grid(row=0, column=1, padx=5, pady=5)

        self.xml_to_csv_button = tk.Button(self.master, text='Convert XML to CSV', command=self.xml_to_csv)
        self.xml_to_csv_button.grid(row=1, column=0, padx=5, pady=5)

        self.csv_to_xml_button = tk.Button(self.master, text='Convert CSV to XML', command=self.csv_to_xml)
        self.csv_to_xml_button.grid(row=1, column=1, padx=5, pady=5)

        self.status_label = tk.Label(self.master, text='Status: Idle')
        self.status_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(self.master, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.file_name.set(file_path)

    def xml_to_csv(self):
        if self.file_name.get():
            sysmac_data = SysmacData(self.file_name.get()[:-4])

            # Set the progress bar value to 0
            self.progress_bar['value'] = 0

            # Update the progress bar after each step
            self.progress_bar['value'] += 25
            self.master.update_idletasks()

            sysmac_data.save_to_csv()

            self.progress_bar['value'] += 50
            self.master.update_idletasks()

            self.status_label.config(text=f'Status: Converted {self.file_name.get()} to CSV')

            self.progress_bar['value'] = 100
            self.master.update_idletasks()
        else:
            self.status_label.config(text='Status: No file selected')

    def csv_to_xml(self):
        if self.file_name.get():
            sysmac_data = SysmacData(self.file_name.get()[:-4])

            # Set the progress bar value to 0
            self.progress_bar['value'] = 0

            # Update the progress bar after each step
            self.progress_bar['value'] += 25
            self.master.update_idletasks()

            sysmac_data.csv_to_xml()

            self.progress_bar['value'] += 50
            self.master.update_idletasks()

            self.status_label.config(text=f'Status: Converted {self.file_name.get()} to XML')

            self.progress_bar['value'] = 100
            self.master.update_idletasks()
        else:
            self.status_label.config(text='Status: No file selected')


if __name__ == '__main__':
    root = tk.Tk()
    gui = SysmacDataGUI(root)
    root.mainloop()
