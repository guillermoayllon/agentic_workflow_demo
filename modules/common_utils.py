import os

import yaml


def save_dict_to_yaml(dictionary, file_path):
    """
    Saves a dictionary to a YAML file. Creates the file if it does not exist.

    Args:
        dictionary (dict): The dictionary to be saved.
        file_path (str): The path to the output YAML file.
    """
    with open(file_path, "w", encoding="UTF-8") as yaml_file:
        yaml.dump(dictionary, yaml_file)


def save_to_markdown(content, filename):
    """
    Saves the given content to a markdown file with the specified filename.

    Args:
        content (str): The content to be saved.
        filename (str): The name of the markdown file (not including the .md extension).

    Returns:
        None
    """
    try:
        with open(filename + ".md", "w", encoding="UTF-8") as f:
            f.write(content)
        print(f"Content saved to {filename} successfully.")
    except Exception as e:
        print(f"Error saving content to {filename}: {e}")


def delete_files_in_directory(directory_path):
    try:
        # Get a list of all files in the directory
        files = os.listdir(directory_path)

        # Iterate over each file and delete it
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")
        print("All files in the directory have been deleted.")
    except Exception as e:
        print(f"Error deleting files: {e}")
