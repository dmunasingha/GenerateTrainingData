import os
import json
import re
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import filedialog

# File extensions to include
VALID_EXTENSIONS = [".php", ".blade.php"]

# Initialize training data list
training_data = []

# Function to clean and normalize content


def clean_content(content: str) -> str:
    return content.strip().replace("\n", " ").replace("\r", " ")

# Function to extract detailed elements from content


def analyze_content(file_path: str, content: str) -> Dict:
    analysis = {
        "file_type": os.path.basename(os.path.dirname(file_path)),
        "keywords": [],
        "structures": [],
        "relationships": [],
        "examples": []
    }

    # Common Laravel patterns (same as before)
    if "routes/" in file_path:
        routes = re.findall(
            r"Route::[a-zA-Z]+\(['\"]([^'\"]+)['\"],? *\[?['\"]([^'\"]+)['\"]", content)
        controllers = re.findall(r"['\"]([^'\"]+)@([^'\"]+)['\"]", content)
        if routes:
            for route in routes:
                analysis["keywords"].append(route[0])
                analysis["structures"].append("route_definition")
                analysis["examples"].append(f"Route for {route[0]}")
        if controllers:
            for controller, method in controllers:
                analysis["keywords"].append(f"{controller}@{method}")
                analysis["relationships"].append(f"calls_controller_method")
                analysis["examples"].append(
                    f"Controller method {controller}@{method}")

    elif "Controllers/" in file_path:
        methods = re.findall(
            r"public function ([a-zA-Z]+)\s*\(([^)]*)\)", content)
        models = re.findall(r"new ([a-zA-Z]+)\s*\(", content)
        if methods:
            for method, params in methods:
                analysis["keywords"].append(method)
                analysis["structures"].append("controller_method")
                analysis["examples"].append(
                    f"Method {method} with params {params}")
        if models:
            analysis["keywords"].extend(models)
            analysis["relationships"].append("uses_model")
            analysis["examples"].extend([f"Model {m}" for m in models])

    elif "Models/" in file_path:
        classes = re.findall(r"class ([a-zA-Z]+)", content)
        relations = re.findall(
            r"function ([a-zA-Z]+)\(\)\s*{\s*return \$this->(belongsTo|hasMany|hasOne)\(", content)
        if classes:
            analysis["keywords"].extend(classes)
            analysis["structures"].append("model_definition")
        if relations:
            for rel_name, rel_type in relations:
                analysis["keywords"].append(rel_name)
                analysis["relationships"].append(f"{rel_type}_relationship")
                analysis["examples"].append(
                    f"Relationship {rel_name} as {rel_type}")

    elif "views/" in file_path:
        directives = re.findall(r"@([a-zA-Z]+)", content)
        variables = re.findall(r"{{\s*\$([a-zA-Z]+)\s*}}", content)
        if directives:
            analysis["keywords"].extend(directives)
            analysis["structures"].append("blade_directive")
            analysis["examples"].extend(
                [f"Directive @{d}" for d in directives])
        if variables:
            analysis["keywords"].extend(variables)
            analysis["structures"].append("blade_variable")
            analysis["examples"].extend([f"Variable ${v}" for v in variables])

    elif "migrations/" in file_path:
        tables = re.findall(r"Schema::create\(['\"]([^'\"]+)['\"]", content)
        columns = re.findall(r"->([a-zA-Z]+)\(['\"]([^'\"]+)['\"]", content)
        if tables:
            analysis["keywords"].extend(tables)
            analysis["structures"].append("migration_table")
            analysis["examples"].extend([f"Table {t}" for t in tables])
        if columns:
            for col_type, col_name in columns:
                analysis["keywords"].append(col_name)
                analysis["structures"].append("migration_column")
                analysis["examples"].append(f"Column {col_name} as {col_type}")

    return analysis

# Dynamic and precise question generator for code suggestions


def generate_precise_question(file_path: str, content: str, analysis: Dict) -> str:
    if not analysis["structures"]:
        return "How do I use this Laravel code in this file?"

    structure = analysis["structures"][0]
    keyword = analysis["keywords"][0] if analysis["keywords"] else "this component"
    example = analysis["examples"][0] if analysis["examples"] else "this code"

    question_templates = {
        "route_definition": "How would you complete or modify the route definition for '{keyword}' in Laravel to handle {example}?",
        "controller_method": "What code should be added to the '{keyword}' method in this controller to handle {example}?",
        "model_definition": "How would you define or extend the relationship for '{keyword}' in this model to include {example}?",
        "blade_directive": "How should the @{keyword} directive be used in this Blade template to display {example}?",
        "blade_variable": "What Laravel logic is needed to populate the '${keyword}' variable in this Blade template for {example}?",
        "migration_table": "How would you modify the migration for the '{keyword}' table to add or change {example}?",
        "migration_column": "What changes are needed in the migration to define or alter the '{keyword}' column for {example}?"
    }

    if structure in question_templates:
        return question_templates[structure].format(keyword=keyword, example=example)

    return f"How would you suggest completing or improving {example} in this {analysis['file_type']} file in Laravel?"

# Function to select project folder using file browser


def select_project_folder() -> str:
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_selected = filedialog.askdirectory(
        title="Select Laravel Project Folder")
    if not folder_selected:
        raise ValueError(
            "No folder selected. Please run the script again and select a folder.")

    return folder_selected

# Main extraction and generation logic


def process_laravel_project(project_path: str):
    # Define Laravel folders relative to project path
    LARAVEL_FOLDERS = [
        "routes", "app/Http/Controllers", "app/Models",
        "resources/views", "database/migrations", "config", "app/Services"
    ]

    global training_data
    training_data = []  # Reset training data

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
                            content = clean_content(f.read())

                        # Analyze content
                        analysis = analyze_content(file_path, content)

                        # Generate precise question
                        question = generate_precise_question(
                            file_path, content, analysis)
                        training_data.append(
                            {"input": question, "output": content})

                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
                        continue

    # Save as JSONL
    output_file = os.path.join(
        project_path, "training_data.jsonl")
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            for entry in training_data:
                json_file.write(json.dumps(entry) + "\n")
        print(
            f"✅ Laravel project converted to precise training data for code suggestions! Saved to {output_file}")
    except Exception as e:
        print(f"Error saving to JSONL: {str(e)}")


if __name__ == "__main__":
    try:
        project_path = select_project_folder()
        print(f"Selected project folder: {project_path}")
        process_laravel_project(project_path)
    except Exception as e:
        print(f"Error: {str(e)}")
