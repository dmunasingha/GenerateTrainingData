import tkinter as tk
from tkinter import filedialog
from src.file_handler import process_laravel_project


def select_project_folder() -> str:
    """
    Open a file browser to select the Laravel project folder.

    Returns:
        str: Path to the selected folder.

    Raises:
        ValueError: If no folder is selected.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_selected = filedialog.askdirectory(
        title="Select Laravel Project Folder")
    if not folder_selected:
        raise ValueError(
            "No folder selected. Please run the script again and select a folder.")

    return folder_selected


if __name__ == "__main__":
    try:
        project_path = select_project_folder()
        print(f"Selected project folder: {project_path}")
        process_laravel_project(project_path)
    except Exception as e:
        print(f"Error: {str(e)}")
