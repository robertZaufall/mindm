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

def serialize_topic_attributes(topic, guid_mapping, ignore_rtf=True):
    """Extract and serialize the attributes of a MindmapTopic.
    
    Args:
        topic (MindmapTopic): The topic to serialize
        guid_mapping (dict): Dictionary mapping GUIDs to numeric IDs
        
    Returns:
        dict: Dictionary containing serialized topic attributes
    """
    d = {}
    d["id"] = guid_mapping.get(topic.guid, topic.guid)
    d["text"] = topic.text
    if topic.rtf != topic.text and not ignore_rtf == True:
        d["rtf"] = topic.rtf
    d["selected"] = topic.selected
    if topic.links:
        d["links"] = []
        for link in topic.links:
            l = {}
            if link.text:
                l["text"] = link.text
            if link.url:
                l["url"] = link.url
            if link.guid:
                l["id"] = guid_mapping.get(link.guid, link.guid)
            d["links"].append(l)
    if topic.image:
        d["image"] = {"text": topic.image.text}
    if topic.icons:
        d["icons"] = []
        for icon in topic.icons:
            i = {}
            if icon.text:
                i["text"] = icon.text
            if icon.is_stock_icon is not None:
                i["is_stock_icon"] = icon.is_stock_icon
            if icon.index is not None:
                i["index"] = icon.index
            if icon.signature:
                i["signature"] = icon.signature
            if icon.path:
                i["path"] = icon.path
            if icon.group:
                i["group"] = icon.group
            d["icons"].append(i)
    if topic.notes and (topic.notes.text or topic.notes.xhtml or topic.notes.rtf):
        notes = {}
        if topic.notes.text:
            notes["text"] = topic.notes.text
        if topic.notes.xhtml:
            notes["xhtml"] = topic.notes.xhtml
        if topic.notes.rtf:
            notes["rtf"] = topic.notes.rtf
        d["notes"] = notes
    if topic.tags:
        d["tags"] = [tag.text for tag in topic.tags]
    if topic.references:
        d["references"] = []
        for ref in topic.references:
            r = {}
            if ref.guid_1:
                r["id_1"] = guid_mapping.get(ref.guid_1, ref.guid_1)
            if ref.guid_2:
                r["id_2"] = guid_mapping.get(ref.guid_2, ref.guid_2)
            if ref.direction:
                r["direction"] = ref.direction
            if ref.label:
                r["label"] = ref.label
            d["references"].append(r)
    d = replace_unicode_in_obj(d)
    return d
