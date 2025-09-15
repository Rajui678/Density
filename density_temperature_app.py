import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
from typing import Optional, Tuple

class DensityTemperatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Density-Temperature Lookup Application")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.data = None
        self.file_path = None
        
        # Create the main interface
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Density-Temperature Lookup Application", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # File upload section
        self.create_file_upload_section()
        
        # Data input section
        self.create_input_section()
        
        # Results section
        self.create_results_section()
        
        # Data display section
        self.create_data_display_section()
        
    def create_file_upload_section(self):
        # File upload frame
        upload_frame = tk.Frame(self.root, bg='#f0f0f0')
        upload_frame.pack(pady=10, padx=20, fill='x')
        
        # Upload button
        upload_btn = tk.Button(
            upload_frame,
            text="Upload Excel File",
            command=self.upload_file,
            bg='#3498db',
            fg='white',
            font=("Arial", 12),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        upload_btn.pack(side='left')
        
        # File path label
        self.file_path_label = tk.Label(
            upload_frame,
            text="No file selected",
            bg='#f0f0f0',
            fg='#7f8c8d',
            font=("Arial", 10)
        )
        self.file_path_label.pack(side='left', padx=(20, 0))
        
    def create_input_section(self):
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=20, padx=20, fill='x')
        
        # Measured Density input
        density_frame = tk.Frame(input_frame, bg='#f0f0f0')
        density_frame.pack(fill='x', pady=5)
        
        tk.Label(
            density_frame,
            text="Measured Density:",
            bg='#f0f0f0',
            font=("Arial", 12, "bold")
        ).pack(side='left')
        
        self.density_entry = tk.Entry(
            density_frame,
            font=("Arial", 12),
            width=20,
            relief='solid',
            bd=1
        )
        self.density_entry.pack(side='right')
        
        # Observed Temperature input
        temp_frame = tk.Frame(input_frame, bg='#f0f0f0')
        temp_frame.pack(fill='x', pady=5)
        
        tk.Label(
            temp_frame,
            text="Observed Temperature:",
            bg='#f0f0f0',
            font=("Arial", 12, "bold")
        ).pack(side='left')
        
        self.temp_entry = tk.Entry(
            temp_frame,
            font=("Arial", 12),
            width=20,
            relief='solid',
            bd=1
        )
        self.temp_entry.pack(side='right')
        
        # Lookup button
        lookup_btn = tk.Button(
            input_frame,
            text="Find Corresponding Density",
            command=self.find_corresponding_density,
            bg='#27ae60',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        lookup_btn.pack(pady=20)
        
    def create_results_section(self):
        # Results frame
        results_frame = tk.Frame(self.root, bg='#f0f0f0')
        results_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            results_frame,
            text="Result:",
            bg='#f0f0f0',
            font=("Arial", 12, "bold")
        ).pack(anchor='w')
        
        self.result_label = tk.Label(
            results_frame,
            text="Enter values and click 'Find Corresponding Density'",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=("Arial", 12),
            relief='solid',
            bd=1,
            padx=10,
            pady=10,
            anchor='w'
        )
        self.result_label.pack(fill='x', pady=5)
        
    def create_data_display_section(self):
        # Data display frame
        display_frame = tk.Frame(self.root, bg='#f0f0f0')
        display_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        tk.Label(
            display_frame,
            text="Uploaded Data Preview:",
            bg='#f0f0f0',
            font=("Arial", 12, "bold")
        ).pack(anchor='w')
        
        # Treeview for data display
        self.tree = ttk.Treeview(display_frame, height=10)
        self.tree.pack(fill='both', expand=True, pady=5)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(display_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def upload_file(self):
        """Upload and load Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Load Excel file
                self.data = pd.read_excel(file_path)
                self.file_path = file_path
                
                # Update file path label
                filename = file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]
                self.file_path_label.config(text=f"Loaded: {filename}")
                
                # Validate data structure
                if self.validate_data_structure():
                    self.display_data()
                    messagebox.showinfo("Success", "File loaded successfully!")
                else:
                    messagebox.showerror("Error", 
                        "Invalid data structure. Please ensure your Excel file has columns:\n"
                        "'Measured Density', 'Observed Temperature', 'Corresponding Density'")
                    self.data = None
                    self.file_path = None
                    self.file_path_label.config(text="No file selected")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.data = None
                self.file_path = None
                self.file_path_label.config(text="No file selected")
    
    def validate_data_structure(self):
        """Validate that the data has the required columns"""
        if self.data is None:
            return False
            
        required_columns = ['Measured Density', 'Observed Temperature', 'Corresponding Density']
        return all(col in self.data.columns for col in required_columns)
    
    def display_data(self):
        """Display the loaded data in the treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.data is not None:
            # Set up columns
            columns = list(self.data.columns)
            self.tree['columns'] = columns
            self.tree['show'] = 'headings'
            
            # Configure column headings
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor='center')
            
            # Insert data
            for index, row in self.data.iterrows():
                values = [str(row[col]) for col in columns]
                self.tree.insert('', 'end', values=values)
    
    def find_corresponding_density(self):
        """Find corresponding density based on measured density and observed temperature"""
        if self.data is None:
            messagebox.showerror("Error", "Please upload an Excel file first!")
            return
        
        try:
            # Get input values
            measured_density = float(self.density_entry.get().strip())
            observed_temp = float(self.temp_entry.get().strip())
            
            # Find the closest match
            result = self.find_closest_match(measured_density, observed_temp)
            
            if result is not None:
                corresponding_density, distance = result
                self.result_label.config(
                    text=f"Corresponding Density: {corresponding_density:.4f} (Distance: {distance:.4f})",
                    fg='#27ae60'
                )
            else:
                self.result_label.config(
                    text="No matching data found for the given inputs",
                    fg='#e74c3c'
                )
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for both fields!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def find_closest_match(self, measured_density: float, observed_temp: float) -> Optional[Tuple[float, float]]:
        """Find the closest match based on Euclidean distance"""
        if self.data is None:
            return None
        
        # Calculate distances
        distances = np.sqrt(
            (self.data['Measured Density'] - measured_density)**2 + 
            (self.data['Observed Temperature'] - observed_temp)**2
        )
        
        # Find minimum distance
        min_idx = distances.idxmin()
        min_distance = distances.iloc[min_idx]
        
        # Return corresponding density and distance
        corresponding_density = self.data.loc[min_idx, 'Corresponding Density']
        return corresponding_density, min_distance

def main():
    root = tk.Tk()
    app = DensityTemperatureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
