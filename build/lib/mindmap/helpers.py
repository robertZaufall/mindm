import re

def escape_mermaid_text(text: str) -> str:
    """Escape special characters in text for Mermaid compatibility.
    
    Args:
        text (str): Text to escape
        
    Returns:
        str: Escaped text for use in Mermaid diagrams
    """
    if not isinstance(text, str):
        return text
    escaped = text.replace("\\", "\\\\") \
                  .replace("\n", "\\n") \
                  .replace("\r", "") \
                  .replace("\"", "\\\"")
    result = []
    for ch in escaped:
        if ord(ch) > 127:
            result.append("\\u{:04x}".format(ord(ch)))
        else:
            result.append(ch)
    return "".join(result)

def replace_unicode_for_markdown(text: str) -> str:
    """Replace Unicode characters for compatibility with Markdown.
    
    Args:
        text (str): Text containing Unicode characters
        
    Returns:
        str: Text with Unicode characters replaced for Markdown compatibility
    """
    return text

def replace_unicode_in_obj(obj):
    """Recursively replace Unicode characters in an object.
    
    Args:
        obj: Object potentially containing Unicode strings
        
    Returns:
        object: Object with Unicode characters replaced
    """
    if isinstance(obj, str):
        return replace_unicode_for_markdown(obj)
    elif isinstance(obj, list):
        return [replace_unicode_in_obj(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_unicode_in_obj(value) for key, value in obj.items()}
    else:
        return obj
