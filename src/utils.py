def clean_content(content: str) -> str:
    """
    Clean and normalize content by removing extra whitespace and line breaks.

    Args:
        content (str): Raw content from a file.

    Returns:
        str: Cleaned and normalized content.
    """
    return content.strip().replace("\n", " ").replace("\r", " ")
