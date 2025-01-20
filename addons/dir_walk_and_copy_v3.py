import os
import argparse
import fnmatch

def should_exclude(item, is_dir=False):
    excluded_dirs = ['.git', 'node_modules', '.venv', 'venv', 'blender_venv', '__pycache__', 'data']
    excluded_files = ['README.md', 'package-lock.json', '__init__.py', 'diag_mapping.json', '*.log', '*key*', '*.png']
    print(f"Excluding directory: {item}") if is_dir else print(f"Excluding file: {item}")

    if is_dir:
        return item in excluded_dirs
    else:
        return any(fnmatch.fnmatch(item, pattern) for pattern in excluded_files)

def print_directory_structure(path, output_file, prefix=""):
    with open(output_file, 'a', encoding='utf-8') as outfile:
        if os.path.isdir(path):
            outfile.write(f"{prefix}{os.path.basename(path)}/\n")
            prefix += "│   "
            try:
                items = sorted([item for item in os.listdir(path) if not should_exclude(item, os.path.isdir(os.path.join(path, item)))])
            except PermissionError:
                items = []
            for index, item in enumerate(items):
                item_path = os.path.join(path, item)
                if index == len(items) - 1:
                    outfile.write(prefix[:-4] + "└── ")
                    if os.path.isdir(item_path):
                        print_directory_structure(item_path, output_file, prefix[:-4] + "    ")
                    else:
                        outfile.write(f"{item}\n")
                else:
                    outfile.write(prefix[:-4] + "├── ")
                    if os.path.isdir(item_path):
                        print_directory_structure(item_path, output_file, prefix)
                    else:
                        outfile.write(f"{item}\n")
        else:
            outfile.write(f"{os.path.basename(path)}\n")

def walk_and_copy(source_path, output_file):
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' does not exist.")
        return
    if not os.path.isdir(source_path):
        print(f"Error: '{source_path}' is not a directory.")
        return

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("Directory Structure:\n")
        outfile.write("===================\n\n")
    
    print_directory_structure(source_path, output_file)
    
    with open(output_file, 'a', encoding='utf-8') as outfile:
        outfile.write("\n\n")
        outfile.write("=" * 50 + "\n")
        outfile.write("File Contents:\n")
        outfile.write("=" * 50 + "\n\n")
        
        for root, dirs, files in os.walk(source_path):
            try:
                dirs[:] = [d for d in dirs if not should_exclude(d, True)]
            except PermissionError:
                continue  # Skip directories we can't access
            for file in files:
                if not should_exclude(file):
                    file_path = os.path.join(root, file)
                    outfile.write(f"File: {file_path}\n")
                    outfile.write("Contents:\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except UnicodeDecodeError:
                        with open(file_path, 'rb') as infile:
                            outfile.write(f"[Binary File Content - {file}]\n")
                    except Exception as e:
                        outfile.write(f"Error reading file: {str(e)}\n")
                    
                    outfile.write("\n\n")
                    outfile.write("=" * 50 + "\n\n")

def main():
    parser = argparse.ArgumentParser(description="Walk a directory, print its structure, and copy file paths and contents to a single file.")
    parser.add_argument("-s", "--source", help="Source directory path (e.g., /path/to/your/directory)")
    parser.add_argument("-o", "--output", help="Output file name (e.g., output.txt)")
    
    args = parser.parse_args()

    if not args.source:
        args.source = input("Enter the source directory path (e.g., /path/to/your/directory): ")
    
    if not args.output:
        args.output = input("Enter the output file name (e.g., output.txt): ")

    walk_and_copy(args.source, args.output)
    print(f"Directory structure, file paths, and contents have been copied to {args.output}")

if __name__ == "__main__":
    main()
