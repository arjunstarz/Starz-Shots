import os
import shutil
from pathlib import Path


def read_file_list(input_file):
    """Read the list of file names from the input text file."""
    try:
        with open(input_file, 'r') as file:
            # Read lines, strip whitespace, and ignore empty lines
            file_list = [line.strip() for line in file if line.strip()]
        return file_list
    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
        return []
    except Exception as e:
        print(f"Error reading input file: {e}")
        return []


def search_and_copy_files(file_list, search_dir, output_dir):
    """Search for files in search_dir and copy them to output_dir with metadata."""
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    found_files = 0
    not_found_files = []

    # Walk through the search directory and its subfolders
    for root, _, files in os.walk(search_dir):
        for file_name in file_list:
            if file_name in files:
                source_path = Path(root) / file_name
                dest_path = Path(output_dir) / file_name

                try:
                    # Copy file with metadata (preserves timestamps)
                    shutil.copy2(source_path, dest_path)
                    print(f"Copied: {file_name} to {output_dir}")
                    found_files += 1
                except Exception as e:
                    print(f"Error copying {file_name}: {e}")

    # Track files that weren't found
    for file_name in file_list:
        if not any(file_name in files for _, _, files in os.walk(search_dir)):
            not_found_files.append(file_name)

    return found_files, not_found_files


def main():
    # Get inputs from user
    input_file = input("Enter the path to the text file containing the list of files: ")
    search_dir = input("Enter the path to the search directory: ")
    output_dir = input("Enter the path to the output directory: ")

    # Validate inputs
    if not Path(input_file).is_file():
        print("Error: Input file does not exist.")
        return
    if not Path(search_dir).is_dir():
        print("Error: Search directory does not exist.")
        return

    # Read the file list
    file_list = read_file_list(input_file)
    if not file_list:
        print("No files to process.")
        return

    # Search and copy files
    found_files, not_found_files = search_and_copy_files(file_list, search_dir, output_dir)

    # Print summary
    print("\nSummary:")
    print(f"Files found and copied: {found_files}")
    if not_found_files:
        print("Files not found:")
        for file in not_found_files:
            print(f"  {file}")
    else:
        print("All files were found and copied.")


if __name__ == "__main__":
    main()
