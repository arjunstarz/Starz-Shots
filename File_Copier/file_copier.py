#!/usr/bin/env python3
"""
File Copier GUI Application

A portable GUI application that copies files from a source directory to a destination directory
based on a reference file containing the list of files to copy.

Features:
- Modern GUI interface with file/folder selection buttons
- Progress bar showing copy completion percentage
- Searches for files in source directory and subdirectories
- Handles file conflicts and errors gracefully
- Detailed logging in the application window
- Portable - no external dependencies required
"""

import os
import shutil
import sys
import threading
import time
import zipfile
from pathlib import Path
from typing import List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext


class StarzShotsApp:
    def __init__(self):
        # File Copier variables
        self.source_dir = ""
        self.dest_dir = ""
        self.reference_file = ""
        self.files_to_copy = []
        self.found_files = {}
        self.copied_count = 0
        self.total_files = 0
        self.is_copying = False

        # Reference Builder variables
        self.zip_files = []
        self.output_dir = ""
        self.is_building = False

        # Create main window
        self.root = tk.Tk()
        self.root.title("*** Starz Shots Helper ***")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface with tabs."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text=" Starz Shots Helper ",
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.setup_file_copier_tab()
        self.setup_reference_builder_tab()

    def setup_file_copier_tab(self):
        """Setup the File Copier tab."""
        # Create file copier frame
        copier_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(copier_frame, text="File Copier")

        # Configure grid weights
        copier_frame.columnconfigure(1, weight=1)
        copier_frame.rowconfigure(5, weight=1)

        # Source directory selection
        ttk.Label(copier_frame, text="Source Directory:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        self.source_entry = ttk.Entry(copier_frame, textvariable=self.source_var, width=50)
        self.source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(copier_frame, text="Browse", command=self.browse_source_dir).grid(
            row=0, column=2, pady=5)

        # Destination directory selection
        ttk.Label(copier_frame, text="Destination Directory:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_entry = ttk.Entry(copier_frame, textvariable=self.dest_var, width=50)
        self.dest_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(copier_frame, text="Browse", command=self.browse_dest_dir).grid(
            row=1, column=2, pady=5)

        # Reference file selection
        ttk.Label(copier_frame, text="Reference File:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.ref_var = tk.StringVar()
        self.ref_entry = ttk.Entry(copier_frame, textvariable=self.ref_var, width=50)
        self.ref_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(copier_frame, text="Browse", command=self.browse_reference_file).grid(
            row=2, column=2, pady=5)

        # Control buttons frame
        button_frame = ttk.Frame(copier_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        self.start_button = ttk.Button(button_frame, text="Start Copying",
                                      command=self.start_copy_process, style='Accent.TButton')
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_copier_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Progress frame
        progress_frame = ttk.LabelFrame(copier_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="Ready to start...")
        self.progress_label.grid(row=1, column=0, pady=5)

        # Log frame
        log_frame = ttk.LabelFrame(copier_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def setup_reference_builder_tab(self):
        """Setup the Reference Builder tab."""
        # Create reference builder frame
        builder_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(builder_frame, text="Reference File Builder")

        # Configure grid weights
        builder_frame.columnconfigure(1, weight=1)
        builder_frame.rowconfigure(4, weight=1)

        # Header
        header_label = ttk.Label(builder_frame, text="** Reference file builder **",
                                font=('Arial', 13, 'bold'))
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Zip files selection
        ttk.Label(builder_frame, text="Zip Files:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)

        # Frame for zip files list and buttons
        zip_frame = ttk.Frame(builder_frame)
        zip_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        zip_frame.columnconfigure(0, weight=1)

        # Zip files listbox with scrollbar
        zip_list_frame = ttk.Frame(zip_frame)
        zip_list_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        zip_list_frame.columnconfigure(0, weight=1)

        self.zip_listbox = tk.Listbox(zip_list_frame, height=4)
        self.zip_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))

        zip_scrollbar = ttk.Scrollbar(zip_list_frame, orient="vertical", command=self.zip_listbox.yview)
        zip_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.zip_listbox.configure(yscrollcommand=zip_scrollbar.set)

        # Zip file buttons
        ttk.Button(zip_frame, text="Add Zip Files", command=self.add_zip_files).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        ttk.Button(zip_frame, text="Remove Selected", command=self.remove_zip_file).grid(
            row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Output directory selection
        ttk.Label(builder_frame, text="Output Directory:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(builder_frame, textvariable=self.output_var, width=50)
        self.output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(builder_frame, text="Browse", command=self.browse_output_dir).grid(
            row=2, column=2, pady=5)

        # Control buttons frame for builder
        builder_button_frame = ttk.Frame(builder_frame)
        builder_button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        self.build_button = ttk.Button(builder_button_frame, text="Build Reference File",
                                      command=self.start_build_process, style='Accent.TButton')
        self.build_button.pack(side=tk.LEFT, padx=5)

        self.clear_builder_button = ttk.Button(builder_button_frame, text="Clear All",
                                              command=self.clear_builder_fields)
        self.clear_builder_button.pack(side=tk.LEFT, padx=5)

        # Builder log frame
        builder_log_frame = ttk.LabelFrame(builder_frame, text="Log", padding="10")
        builder_log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        builder_log_frame.columnconfigure(0, weight=1)
        builder_log_frame.rowconfigure(0, weight=1)

        # Builder log text area
        self.builder_log_text = scrolledtext.ScrolledText(builder_log_frame, height=12, width=80)
        self.builder_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def log_message(self, message: str):
        """Add a message to the log area."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def builder_log_message(self, message: str):
        """Add a message to the builder log area."""
        self.builder_log_text.insert(tk.END, f"{message}\n")
        self.builder_log_text.see(tk.END)
        self.root.update_idletasks()

    def browse_source_dir(self):
        """Browse for source directory."""
        directory = filedialog.askdirectory(title="Select Source Directory")
        if directory:
            self.source_var.set(directory)
            self.source_dir = directory
            self.log_message(f"Source directory selected: {directory}")

    def browse_dest_dir(self):
        """Browse for destination directory."""
        directory = filedialog.askdirectory(title="Select Destination Directory")
        if directory:
            self.dest_var.set(directory)
            self.dest_dir = directory
            self.log_message(f"Destination directory selected: {directory}")

    def browse_reference_file(self):
        """Browse for reference file."""
        file_path = filedialog.askopenfilename(
            title="Select Reference File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.ref_var.set(file_path)
            self.reference_file = file_path
            self.log_message(f"Reference file selected: {file_path}")

    # Reference Builder Methods
    def add_zip_files(self):
        """Add zip files to the list."""
        file_paths = filedialog.askopenfilenames(
            title="Select Zip Files",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        for file_path in file_paths:
            if file_path not in self.zip_files:
                self.zip_files.append(file_path)
                self.zip_listbox.insert(tk.END, Path(file_path).name)
                self.builder_log_message(f"Added zip file: {Path(file_path).name}")

    def remove_zip_file(self):
        """Remove selected zip file from the list."""
        selection = self.zip_listbox.curselection()
        if selection:
            index = selection[0]
            removed_file = self.zip_files.pop(index)
            self.zip_listbox.delete(index)
            self.builder_log_message(f"Removed zip file: {Path(removed_file).name}")

    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
            self.output_dir = directory
            self.builder_log_message(f"Output directory selected: {directory}")

    def clear_copier_fields(self):
        """Clear all file copier inputs and reset the tab."""
        self.source_var.set("")
        self.dest_var.set("")
        self.ref_var.set("")
        self.source_dir = ""
        self.dest_dir = ""
        self.reference_file = ""
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to start...")
        self.log_text.delete(1.0, tk.END)
        self.start_button.config(state='normal')
        self.log_message("All fields cleared.")

    def clear_builder_fields(self):
        """Clear all reference builder inputs and reset the tab."""
        self.zip_files.clear()
        self.zip_listbox.delete(0, tk.END)
        self.output_var.set("")
        self.output_dir = ""
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to start...")
        self.builder_log_text.delete(1.0, tk.END)
        self.build_button.config(state='normal')
        self.builder_log_message("All fields cleared.")

    def start_build_process(self):
        """Start the reference file building process."""
        if not self.validate_builder_inputs():
            return

        if self.is_building:
            messagebox.showwarning("Warning", "Build operation is already in progress.")
            return

        # Disable build button during building
        self.build_button.config(state='disabled')
        self.is_building = True

        # Start building in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self.build_reference_file_thread)
        thread.daemon = True
        thread.start()

    def validate_builder_inputs(self) -> bool:
        """Validate reference builder inputs."""
        if not self.zip_files:
            messagebox.showerror("Error", "Please select at least one zip file.")
            return False

        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return False

        # Validate zip files exist
        for zip_file in self.zip_files:
            if not Path(zip_file).exists():
                messagebox.showerror("Error", f"Zip file does not exist: {zip_file}")
                return False

        # Validate output directory exists
        if not Path(self.output_dir).exists():
            messagebox.showerror("Error", f"Output directory does not exist: {self.output_dir}")
            return False

        return True

    def build_reference_file_thread(self):
        """Thread function for building reference file."""
        try:
            self.builder_log_message("Starting reference file building process...")
            self.progress_var.set(0)
            self.progress_label.config(text="Building reference file...")

            all_files = []
            total_zips = len(self.zip_files)

            # Process each zip file
            for i, zip_file_path in enumerate(self.zip_files):
                try:
                    self.builder_log_message(f"Processing: {Path(zip_file_path).name}")

                    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                        # Get all file names in the zip
                        file_names = zip_file.namelist()

                        # Filter out directories (they end with '/')
                        file_names = [name for name in file_names if not name.endswith('/')]

                        # Extract just the filename (not the full path)
                        for file_name in file_names:
                            # Get just the filename without directory path
                            filename_only = Path(file_name).name
                            if filename_only:  # Skip empty names
                                all_files.append(filename_only)

                        self.builder_log_message(f"Found {len(file_names)} files in {Path(zip_file_path).name}")

                    # Update progress
                    progress = ((i + 1) / total_zips) * 80  # Use 80% for processing zips
                    self.progress_var.set(progress)
                    self.root.update_idletasks()

                except Exception as e:
                    self.builder_log_message(f"Error processing {Path(zip_file_path).name}: {e}")

            # Remove duplicates while preserving order
            unique_files = []
            seen = set()
            for file_name in all_files:
                if file_name not in seen:
                    unique_files.append(file_name)
                    seen.add(file_name)

            self.builder_log_message(f"Total unique files found: {len(unique_files)}")

            # Write to reference file
            output_file_path = Path(self.output_dir) / "stz_ref.txt"

            self.progress_var.set(90)
            self.progress_label.config(text="Writing reference file...")
            self.root.update_idletasks()

            with open(output_file_path, 'w', encoding='utf-8') as ref_file:
                for file_name in unique_files:
                    ref_file.write(f"{file_name}\n")

            self.progress_var.set(100)
            self.progress_label.config(text="Reference file created successfully!")

            self.builder_log_message("-" * 50)
            self.builder_log_message(f"Reference file created: {output_file_path}")
            self.builder_log_message(f"Total files listed: {len(unique_files)}")
            self.builder_log_message("Build process completed successfully!")

            # Show completion message
            messagebox.showinfo("Success",
                              f"Reference file created successfully!\n\n"
                              f"Location: {output_file_path}\n"
                              f"Total files: {len(unique_files)}")

        except Exception as e:
            self.builder_log_message(f"Error during build process: {e}")
            messagebox.showerror("Error", f"An error occurred during build: {e}")
        finally:
            self.is_building = False
            self.build_button.config(state='normal')

    def validate_inputs(self) -> bool:
        """Validate all user inputs."""
        if not self.source_dir:
            messagebox.showerror("Error", "Please select a source directory.")
            return False

        if not self.dest_dir:
            messagebox.showerror("Error", "Please select a destination directory.")
            return False

        if not self.reference_file:
            messagebox.showerror("Error", "Please select a reference file.")
            return False

        # Validate source directory exists
        if not Path(self.source_dir).exists():
            messagebox.showerror("Error", f"Source directory does not exist: {self.source_dir}")
            return False

        # Validate reference file exists
        if not Path(self.reference_file).exists():
            messagebox.showerror("Error", f"Reference file does not exist: {self.reference_file}")
            return False

        return True

    def start_copy_process(self):
        """Start the file copying process."""
        if not self.validate_inputs():
            return

        if self.is_copying:
            messagebox.showwarning("Warning", "Copy operation is already in progress.")
            return

        # Disable start button during copying
        self.start_button.config(state='disabled')
        self.is_copying = True

        # Start copying in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self.copy_files_thread)
        thread.daemon = True
        thread.start()

    def copy_files_thread(self):
        """Thread function for copying files."""
        try:
            # Read reference file
            if not self.read_reference_file():
                return

            # Find files in source directory
            self.find_files_in_source()

            # Copy files
            self.copy_files()

        except Exception as e:
            self.log_message(f"Error during copy operation: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.is_copying = False
            self.start_button.config(state='normal')

    def read_reference_file(self) -> bool:
        """Read the reference file and extract file names."""
        try:
            with open(self.reference_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Clean up file names (remove whitespace and empty lines)
            self.files_to_copy = []
            for line in lines:
                filename = line.strip()
                if filename and not filename.startswith('#'):  # Skip empty lines and comments
                    self.files_to_copy.append(filename)

            self.total_files = len(self.files_to_copy)

            if self.total_files == 0:
                self.log_message("Error: No valid file names found in reference file.")
                messagebox.showerror("Error", "No valid file names found in reference file.")
                return False

            self.log_message(f"Found {self.total_files} files to copy in reference file.")
            return True

        except Exception as e:
            self.log_message(f"Error reading reference file: {e}")
            messagebox.showerror("Error", f"Error reading reference file: {e}")
            return False
    
    def find_files_in_source(self) -> None:
        """Find all specified files in source directory and subdirectories."""
        self.log_message(f"Searching for files in '{self.source_dir}'...")
        self.progress_label.config(text="Searching for files...")

        self.found_files = {}
        source_path = Path(self.source_dir)

        # Walk through all subdirectories
        for i, file_to_find in enumerate(self.files_to_copy):
            found = False

            # Update progress during search
            search_progress = (i / self.total_files) * 30  # Use 30% for search phase
            self.progress_var.set(search_progress)
            self.root.update_idletasks()

            # Search in source directory and all subdirectories
            for file_path in source_path.rglob(file_to_find):
                if file_path.is_file():
                    self.found_files[file_to_find] = str(file_path)
                    found = True
                    break  # Take the first match found

            if not found:
                self.log_message(f"Warning: File '{file_to_find}' not found in source directory.")

        found_count = len(self.found_files)
        self.log_message(f"Found {found_count} out of {self.total_files} files in source directory.")

        if found_count == 0:
            messagebox.showwarning("Warning", "No files found in source directory!")
            return

    def copy_files(self) -> None:
        """Copy found files to destination directory with progress tracking."""
        if not self.found_files:
            self.log_message("No files to copy.")
            return

        # Create destination directory if it doesn't exist
        dest_path_obj = Path(self.dest_dir)
        if not dest_path_obj.exists():
            try:
                dest_path_obj.mkdir(parents=True, exist_ok=True)
                self.log_message(f"Created destination directory: {self.dest_dir}")
            except Exception as e:
                self.log_message(f"Error creating destination directory: {e}")
                messagebox.showerror("Error", f"Could not create destination directory: {e}")
                return

        self.log_message(f"Starting file copy operation...")
        self.log_message(f"Source: {self.source_dir}")
        self.log_message(f"Destination: {self.dest_dir}")
        self.log_message("-" * 50)

        self.copied_count = 0
        total_to_copy = len(self.found_files)

        for filename, source_path in self.found_files.items():
            try:
                # Create destination file path
                dest_path = Path(self.dest_dir) / filename

                # Check if file already exists
                if dest_path.exists():
                    self.log_message(f"Warning: '{filename}' already exists in destination. Overwriting...")

                # Copy the file
                shutil.copy2(source_path, dest_path)
                self.copied_count += 1

                # Calculate and display progress
                copy_progress = 30 + (self.copied_count / total_to_copy) * 70  # 30% for search, 70% for copy
                self.progress_var.set(copy_progress)
                progress_percent = (self.copied_count / total_to_copy) * 100
                self.progress_label.config(text=f"Copying files... {self.copied_count}/{total_to_copy} ({progress_percent:.1f}%)")
                self.log_message(f"[{progress_percent:6.1f}%] Copied: {filename}")

                # Update UI
                self.root.update_idletasks()

            except Exception as e:
                self.log_message(f"Error copying '{filename}': {e}")

        self.log_message("-" * 50)
        self.log_message(f"Copy operation completed!")
        self.log_message(f"Successfully copied {self.copied_count} out of {total_to_copy} files.")

        # Final progress update
        self.progress_var.set(100)
        self.progress_label.config(text=f"Completed! {self.copied_count}/{total_to_copy} files copied.")

        # Show completion message
        messagebox.showinfo("Success", f"Copy operation completed!\nSuccessfully copied {self.copied_count} out of {total_to_copy} files.")

    def run(self):
        """Run the GUI application."""
        self.log_message("Starz Shots File Copier started.")
        self.log_message("Please select source directory, destination directory, and reference file.")
        self.builder_log_message("Starz Shots reference file builder ready.")
        self.builder_log_message("Please select zip files and output directory.")
        self.root.mainloop()


def main():
    """Main function to run the Starz Shots application."""
    try:
        app = StarzShotsApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Error starting application: {e}")


if __name__ == "__main__":
    main()
