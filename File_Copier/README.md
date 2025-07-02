# Starz Shots File Copier

A portable GUI application that copies files from a source directory to a destination directory based on a reference file containing the list of files to copy.

## Features

- **Modern GUI Interface**: Easy-to-use graphical interface with browse buttons
- **Portable Application**: Can be built as a standalone executable (.exe)
- **Progress Bar**: Visual progress tracking during file copying
- **Real-time Logging**: Live log display showing operation details
- **Recursive Search**: Searches for files in source directory and all subdirectories
- **Error Handling**: Gracefully handles missing files, permission errors, and other issues
- **File Validation**: Validates all paths and creates destination directory if needed
- **Threaded Operations**: Non-blocking UI during file operations

## Usage

### Option 1: Run as Python Script
1. **Run the program**:
   ```bash
   python file_copier.py
   ```

2. **Use the GUI interface**:
   - Click **"Browse"** next to "Source Directory" to select where your files are located
   - Click **"Browse"** next to "Destination Directory" to select where files should be copied
   - Click **"Browse"** next to "Reference File" to select your text file with the list of files
   - Click **"Start Copying"** to begin the operation
   - Monitor progress in the progress bar and log area

### Option 2: Build Portable Executable
1. **Build the executable**:
   ```bash
   python build_portable.py
   ```
   Or double-click `build_portable.bat` on Windows

2. **Use the portable app**:
   - Copy `dist/StarzShotsFileCopier.exe` to any Windows computer
   - Double-click to run (no Python installation required)
   - Use the same GUI interface as described above

## Reference File Format

The reference file should be a plain text file (.txt) with one filename per line:

```
document1.pdf
image.jpg
data.csv
# This is a comment and will be ignored
report.docx
config.json
```

- Lines starting with `#` are treated as comments and ignored
- Empty lines are ignored
- Whitespace around filenames is automatically trimmed

## Example

1. Create a reference file (`files_to_copy.txt`):
   ```
   important_document.pdf
   data_analysis.xlsx
   project_report.docx
   ```

2. Run the program:
   ```bash
   python file_copier.py
   ```

3. Enter the paths when prompted:
   ```
   Enter the source directory path: /path/to/source/folder
   Enter the destination directory path: /path/to/destination/folder
   Enter the reference file path: files_to_copy.txt
   ```

4. The program will:
   - Search for the files in the source directory and subdirectories
   - Show you what files were found
   - Ask for confirmation
   - Copy the files with progress updates

## Sample Output

```
=== File Copier Program ===

Enter the source directory path: ./source_files
Enter the destination directory path: ./copied_files
Enter the reference file path: sample_reference.txt

Found 8 files to copy in reference file.

Searching for files in './source_files'...
Found 6 out of 8 files in source directory.
Warning: File 'missing_file1.txt' not found in source directory.
Warning: File 'missing_file2.pdf' not found in source directory.

Ready to copy 6 files.
Proceed with copying? (y/n): y

Starting file copy operation...
Source: ./source_files
Destination: ./copied_files
--------------------------------------------------
[ 16.7%] Copied: document1.pdf
[ 33.3%] Copied: image.jpg
[ 50.0%] Copied: data.csv
[ 66.7%] Copied: report.docx
[ 83.3%] Copied: config.json
[100.0%] Copied: readme.txt
--------------------------------------------------
Copy operation completed!
Successfully copied 6 out of 6 files.
```

## Requirements

- Python 3.6 or higher
- No additional dependencies required (uses only standard library)

## Error Handling

The program handles various error scenarios:
- Non-existent source or destination directories
- Invalid file paths
- Permission errors
- Files that don't exist in the source directory
- Disk space issues

## Notes

- If a file with the same name already exists in the destination, it will be overwritten
- The program preserves file metadata (timestamps, permissions) when copying
- Large files are copied efficiently using Python's `shutil.copy2()` function
