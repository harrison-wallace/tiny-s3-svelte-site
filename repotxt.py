import os
import git
from pathlib import Path
from datetime import datetime
import fnmatch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def generate_shallow_file_tree(root_path, out_file, exclude_dirs, exclude_files):
    """Generate a shallow tree diagram, excluding specified directories and files."""
    tree = "Repository Tree (Shallow):\n"
    for root, dirs, files in os.walk(root_path, topdown=True):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = root.replace(root_path, "").count(os.sep)
        indent = "  " * level
        dir_name = os.path.basename(root)

        # Only show the directory name if it's not excluded at level 0 or 1
        if level == 0 or (level == 1 and dir_name not in exclude_dirs):
            tree += f"{indent}{dir_name}/\n"

            # If at the top level or in an included directory, list non-excluded files
            if level == 0 or dir_name in ['src', 'terraform', 'public', 'static']:
                for file in files:
                    if not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_files):
                        tree += f"{indent}  {file}\n"

    out_file.write(tree + "\n" + "=" * 50 + "\n\n")

def compile_repo_to_file():
    try:
        # Get the current working directory
        repo_path = os.getcwd()
        folder_name = os.path.basename(repo_path)
        current_time = datetime.now().strftime("%d-%m-%y-%H-%M")
        output_file = f"{folder_name}{current_time}.txt"

        # Initialize git repo object
        repo = git.Repo(repo_path)
        logging.info(f"Processing repository at: {repo_path}")

        # Get gitignore patterns
        gitignore_patterns = []
        gitignore_file = os.path.join(repo_path, '.gitignore')
        if os.path.exists(gitignore_file):
            with open(gitignore_file, 'r') as f:
                gitignore_patterns = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith('#')
                ]
            logging.info(f"Found .gitignore patterns: {gitignore_patterns}")

        # Directories to exclude
        exclude_dirs = ['.git', 'node_modules', '.svelte-kit', 'build']

        # Files to exclude (patterns)
        exclude_files = [
            '*.lock',
            'package-lock.json',
            '*.txt',
            'repoToText.py',
        ]

        # Combine .gitignore patterns with our explicit exclude_files
        # if you want them all treated equally:
        all_exclude_patterns = gitignore_patterns + exclude_files

        with open(output_file, 'w', encoding='utf-8') as out_file:
            # Add shallow tree diagram
            generate_shallow_file_tree(repo_path, out_file, exclude_dirs, exclude_files)

            # Write header with timestamp
            out_file.write(f"Repository Compilation - {repo_path}\n")
            out_file.write(f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
            out_file.write("=" * 50 + "\n\n")

            # Walk through all files in the repo
            for root, dirs, files in os.walk(repo_path):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                if '.git' in root:
                    continue

                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, repo_path)
                    logging.info(f"Processing: {relative_path}")

                    # Determine if the file should be excluded
                    if any(
                        fnmatch.fnmatch(relative_path, pattern) or
                        fnmatch.fnmatch(file_name, pattern)
                        for pattern in all_exclude_patterns
                    ):
                        logging.info(f"Skipping ignored file: {relative_path}")
                        continue

                    # Write file information
                    out_file.write(f"File: {relative_path}\n")
                    out_file.write("-" * 50 + "\n")

                    # Try to read and write file contents with fallback encoding
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            out_file.write(content)
                    except UnicodeDecodeError:
                        out_file.write("[Binary file or could not decode with UTF-8]\n")
                    except IOError as e:
                        out_file.write(f"[IOError: Could not read file - {str(e)}]\n")
                    except Exception as e:
                        out_file.write(f"[Error: {str(e)}]\n")

                    out_file.write("\n" + "=" * 50 + "\n\n")

        logging.info(f"Repository contents compiled to {output_file}")

    except git.exc.InvalidGitRepositoryError:
        logging.error("Error: Current directory is not a git repository")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    compile_repo_to_file()
