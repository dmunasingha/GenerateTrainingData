# Python Laravel Analyzer

This project is a Python script that analyzes Laravel projects to generate training data for fine-tuning AI models. It dynamically selects a Laravel project folder via a file browser, processes PHP and Blade files, and creates precise questions and corresponding code snippets for code suggestion tasks.

## Features
- Dynamic folder selection using a GUI file browser.
- Analysis of Laravel routes, controllers, models, views, and migrations.
- Generation of precise questions for code completion and modification.
- Output saved as JSONL for easy integration with machine learning models.

## Prerequisites
- Python 3.x
- No external dependencies required (uses built-in `tkinter`).

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/dmunasingha/GenerateTrainingData
   ```
   ```
   cd GenerateTrainingData
   ```
2. Ensure Python is installed on your system.

## Usage
1. Run the script:
   ```
   python main.py
   ```

2. Use the file browser to select your Laravel project folder (e.g., "D:/AjanthaPayrollSystem").
3. The script will process the files and save the training data as `model_training_data.jsonl` in the selected folder.

## Project Structure
- `src/`: Contains core modules for analysis, question generation, and file handling.
- `main.py`: Entry point with file browser.
- `requirements.txt`: Dependency list (currently empty).
- `.gitignore`: Ignores compiled files and generated data.
- `README.md`: This file.
- `LICENSE`: License information.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please open an issue or pull request on GitHub.