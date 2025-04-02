import re
from typing import Dict
import os


def analyze_content(file_path: str, content: str) -> Dict:
    """
    Analyze Laravel file content to extract key structures and keywords for training data.

    Args:
        file_path (str): Path to the file being analyzed.
        content (str): Content of the file as a string.

    Returns:
        Dict: Analysis results including file type, keywords, structures, relationships, and examples.
    """
    analysis = {
        "file_type": os.path.basename(os.path.dirname(file_path)),
        "keywords": [],
        "structures": [],
        "relationships": [],
        "examples": []
    }

    if "routes/" in file_path:
        routes_pattern = r"Route::[a-zA-Z]+\(['\"]([^'\"]+)['\"],? *\[?['\"]([^'\"]+)['\"]"
        routes = re.findall(routes_pattern, content)
        for route_uri, controller in routes:
            analysis["keywords"].append(route_uri)
            analysis["structures"].append("route_definition")
            analysis["examples"].append(f"Route for {route_uri}")

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
