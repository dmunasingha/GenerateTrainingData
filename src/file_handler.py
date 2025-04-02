import os
import json
from .analyzer import analyze_content
from .questions_generator import generate_precise_question


def process_laravel_project(project_path: str):
    """
    Process a Laravel project to generate training data from its files.

    Args:
        project_path (str): Path to the Laravel project folder.
    """
    LARAVEL_FOLDERS = [
        "routes", "app/Http/Controllers", "app/Models",
        "resources/views", "database/migrations", "config", "app/Services"
    ]
    VALID_EXTENSIONS = [".php", ".blade.php"]
    training_data = []

    for folder in LARAVEL_FOLDERS:
        full_path = os.path.join(project_path, folder)

        if not os.path.exists(full_path):
            print(f"Warning: Folder {full_path} not found, skipping...")
            continue

        for root, _, files in os.walk(full_path):
            for file in files:
                if any(file.endswith(ext) for ext in VALID_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().strip().replace("\n", " ").replace("\r", " ")

                        analysis = analyze_content(file_path, content)
                        question = generate_precise_question(
                            file_path, content, analysis)
                        training_data.append(
                            {"input": question, "output": content})

                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
                        continue

    output_file = os.path.join(
        project_path, "model_training_data.jsonl")
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            for entry in training_data:
                json_file.write(json.dumps(entry) + "\n")
        print(
            f"✅ Laravel project converted to precise training data! Saved to {output_file}")
    except Exception as e:
        print(f"Error saving to JSONL: {str(e)}")
