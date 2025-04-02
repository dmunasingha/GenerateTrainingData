from typing import Dict


def generate_precise_question(file_path: str, content: str, analysis: Dict) -> str:
    """
    Generate a precise question for code suggestions based on file analysis.

    Args:
        file_path (str): Path to the file being analyzed.
        content (str): Content of the file as a string.
        analysis (Dict): Analysis results from analyze_content.

    Returns:
        str: A precise question tailored to the file's content.
    """
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
