"""
MacOS-specific implementation of the Mindmanager interface.
This class implementation uses the native AppleScript approach.

This module provides MacOS platform-specific implementation for interacting
with MindManager application, including functionality for manipulating topics,
properties, relationships, and document structure.
"""

import os
import sys
import json
import subprocess

from mindmap.mindmap import (
    MindmapLink,
    MindmapImage,
    MindmapNotes,
    MindmapIcon,
    MindmapTag,
    MindmapReference,
    MindmapTopic,
)
import mindmap.serialization as mms

APPLESCRIPT_READ = os.path.join(os.path.dirname(__file__), "as", "read.scpt")
APPLESCRIPT_WRITE = os.path.join(os.path.dirname(__file__), "as", "write.scpt")

def _run_applescript(script: str, args: list = None) -> str:
    if args is None:
        args = []
    
    command = ["osascript", "-e", script] + args
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"AppleScript error: {e.stderr}")
        return ""

def _run_compiled_applescript(script_path: str, args: list = None) -> str:
    if args is None:
        args = []
    
    command = ["osascript", script_path] + (args or [])
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("osascript returned", e.returncode)
        print("--- stdout ---\n", e.stdout)
        print("--- stderr ---\n", e.stderr)
        return ""
    
class Mindmanager:

    MACOS_MERGE_ALL_WINDOWS = False
    MACOS_LIBRARY_FOLDER = os.path.join(
        os.path.expanduser("~"), 
        "Library", 
        "Application Support", 
        "Mindjet", 
        "MindManager", 
        "XX", 
        "English", 
        "Library"
    )

    def __init__(self, charttype):
        self._charttype = charttype

        # Get version from MindManager
        script = 'tell application "MindManager" to return version'
        version_str = _run_applescript(script)
        if version_str:
            self._version = version_str.split('.')[0]
        else:
            self._version = "0"

        self._library_folder = self.MACOS_LIBRARY_FOLDER.replace("XX", self._version)
        if self._version == '24':
            orgchart_template_path = os.path.join(self._library_folder, "Templates", "Blank Templates", "Organization Chart.mmat")
        else:
            orgchart_template_path = os.path.join(self._library_folder, "Templates", "Blank Templates", "Org-Chart Map.mmat")
        self._orgchart_template = orgchart_template_path
        self._radial_template = os.path.join(self._library_folder, "Templates", "Blank Templates", "Radial Map.mmat")

    def _read(self, modus, arguments = None) -> list['MindmapTopic']:
        if arguments:
             script_args = [modus] + arguments
        else:
            script_args = [modus]

        json_string = _run_compiled_applescript(APPLESCRIPT_READ, script_args)
    
        if not json_string:
            return None  # no data returned
        try:
            jsonObject = json.loads(json_string)
            if isinstance(jsonObject, dict):
                # It's a single tree structure
                topic = self._dict_to_mindmap_topic(jsonObject)
                return [topic] if topic else None
            elif isinstance(jsonObject, list):
                # It's a list of topic structures
                topics = []
                for item in jsonObject:
                    if isinstance(item, dict):
                        topic = self._dict_to_mindmap_topic(item)
                        if topic:
                            topics.append(topic)
                return topics
            else:
                # Unexpected format
                print(f"Unexpected JSON format received: {type(jsonObject)}")
                return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from AppleScript: {e}")
            return None
    
    def _write(self, modus, mindmap_topic):
        json_string = json.dumps(mms.serialize_object_simple(mindmap_topic))
        script_args = [modus] + [json_string]
        result = _run_compiled_applescript(APPLESCRIPT_WRITE, script_args)
        return result

    def _dict_to_mindmap_topic(self, node_dict: dict) -> 'MindmapTopic':
        """
        Helper to recursively convert a dict of the form:
        { "guid": ..., "text": ..., "level": ..., "notes": ..., "subtopics": [ ... ] }
        into a MindmapTopic object with subtopics.
        """
        notes_obj = None
        if node_dict.get("notes"):
            notes_obj = MindmapNotes(text=node_dict["notes"])
        references = []
        for ref in node_dict.get("references", []) or []:
            if not isinstance(ref, dict):
                continue
            direction = 0
            try:
                direction = int(ref.get("direction", 0) or 0)
            except (TypeError, ValueError):
                direction = 0
            references.append(
                MindmapReference(
                    direction=direction,
                    guid_1=ref.get("guid_1", ""),
                    guid_2=ref.get("guid_2", ""),
                )
            )
        tags = []
        for tag in node_dict.get("tags", []) or []:
            if isinstance(tag, dict):
                text_val = tag.get("text", "")
            else:
                text_val = tag
            if text_val:
                tags.append(MindmapTag(text=text_val))
        topic = MindmapTopic(
            guid=node_dict.get("guid", ""),
            text=node_dict.get("text", ""),
            level=int(node_dict.get("level", 0)),
            notes=notes_obj,
            tags=tags,
            references=references,
        )
        subtopics = node_dict.get("subtopics", [])
        for child_dict in subtopics:
            child_topic = self._dict_to_mindmap_topic(child_dict)
            if child_topic:
                topic.subtopics.append(child_topic)
                child_topic.parent = topic

        return topic
    
    def get_mindmanager_object(self):
        return None

    def get_active_document_object(self):
        """
        Return 'document 1' if a document is open, else None.
        """
        return "document 1" if self.document_exists() else None

    def get_library_folder(self):
        return self._library_folder

    def get_version(self):
        return self._version

    def set_document_background_image(self, path):
        pass

    def document_exists(self):
        """
        Returns True if there's at least one open document in MindManager.
        """
        script = '''
            tell application "MindManager"
                if (count of documents) > 0 then
                    return "true"
                else
                    return "false"
                end if
            end tell
        '''
        result = _run_applescript(script)
        return (result == "true")

    def get_central_topic(self) -> 'MindmapTopic':
        """
        Return the central topic's ID or None if not found.
        """
        result = self._read("getTree")
        return result[0] if result else None

    def get_mindmaptopic_from_topic(self, topic_id) -> 'MindmapTopic':
        """
        Returns a MindmapTopic with guid, text, rtf and level,
        all retrieved via a single AppleScript call.
        """
        if not topic_id:
            return None

        # Single AppleScript to grab all basic properties at once:
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set theGUID to id of theTopic
                    set theName to name of theTopic
                    set theTitle to title of theTopic
                    set theLevel to level of theTopic
                    return theGUID & "%%" & theName & "%%" & theTitle & "%%" & (theLevel as text)
                on error
                    return ""
                end try
            end tell
        '''
        result = _run_applescript(script)
        if not result:
            return None  # topic not found or error

        parts = result.split("%%", 3)  # we expect exactly 4 parts
        if len(parts) < 4:
            return None

        theGUID, theName, theTitle, theLevelStr = parts

        # Convert level to integer if possible
        try:
            theLevel = int(theLevelStr)
        except ValueError:
            theLevel = None

        # Clean up the text property so it mimics your old replacements
        theName = theName.replace('"', '`').replace("'", "`").replace("\r", "").replace("\n", "")

        # Construct and return the MindmapTopic
        return MindmapTopic(
            guid=theGUID,
            text=theName,
            rtf=theTitle,
            level=theLevel,
        )

    def get_mindmaptopic_from_topic_content(self, topic_id) -> 'MindmapTopic':
        """
        Returns a MindmapTopic with guid, text, rtf, level, and notes,
        all retrieved via a single AppleScript call.
        """
        if not topic_id:
            return None

        # Single AppleScript to grab all basic properties at once:
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set theGUID to id of theTopic
                    set theName to name of theTopic
                    set theTitle to title of theTopic
                    set theLevel to level of theTopic
                    set theNotes to notes of theTopic
                    return theGUID & "%%" & theName & "%%" & theTitle & "%%" & (theLevel as text) & "%%" & theNotes
                on error
                    return ""
                end try
            end tell
        '''
        result = _run_applescript(script)
        if not result:
            return None  # topic not found or error

        parts = result.split("%%", 4)  # we expect exactly 5 parts
        if len(parts) < 5:
            return None

        theGUID, theName, theTitle, theLevelStr, theNotes = parts

        # Convert level to integer if possible
        try:
            theLevel = int(theLevelStr)
        except ValueError:
            theLevel = None

        # Clean up the text property so it mimics your old replacements
        theName = theName.replace('"', '`').replace("'", "`").replace("\r", "").replace("\n", "")

        # Build the MindmapNotes object if notes are non-empty
        notes_obj = MindmapNotes(text=theNotes) if theNotes else None

        # Construct and return the MindmapTopic
        return MindmapTopic(
            guid=theGUID,
            text=theName,
            rtf=theTitle,
            level=theLevel,
            notes=notes_obj,
        )

    def get_mindmaptopic_from_topic_full(self, topic_id) -> 'MindmapTopic':
        """
        Returns a MindmapTopic with guid, text, rtf, level, notes, and references,
        all via one AppleScript call. (links/icons/tags/image remain unimplemented.)
        """
        if not topic_id:
            return None

        # Single AppleScript to grab all properties + references
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set theGUID to id of theTopic
                    set theName to name of theTopic
                    set theTitle to title of theTopic
                    set theLevel to level of theTopic
                    set theNotes to notes of theTopic
                    set rels to relationships of theTopic
                    set referencesString to ""
                    repeat with r in rels
                        set sLoc to id of (starting location of r)
                        set eLoc to id of (ending location of r)
                        set referencesString to referencesString & sLoc & "||" & eLoc & "||--||"
                    end repeat
                    return theGUID & "%%" & theName & "%%" & theTitle & "%%" & (theLevel as text) & "%%" & theNotes & "%%" & referencesString
                on error
                    return ""
                end try
            end tell
        '''
        result = _run_applescript(script)
        if not result:
            return None

        # We expect 6 parts: guid, name, title, level, notes, referencesString
        parts = result.split("%%", 5)
        if len(parts) < 6:
            return None

        theGUID, theName, theTitle, theLevelStr, theNotes, referencesRaw = parts

        # Convert level to integer if possible
        try:
            theLevel = int(theLevelStr)
        except ValueError:
            theLevel = None

        # Clean up the text property
        theName = theName.replace('"', '`').replace("'", "`").replace("\r", "").replace("\n", "")

        # Build the MindmapNotes object if notes are non-empty
        notes_obj = MindmapNotes(text=theNotes) if theNotes else None

        # Parse references:
        # referencesRaw might look like "GUID1||GUID2||--||GUID3||GUID4||--||"
        references = []
        if referencesRaw:
            rel_chunks = referencesRaw.split("||--||")
            for chunk in rel_chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue
                pair = chunk.split("||")
                if len(pair) == 2:
                    sLoc, eLoc = pair
                    if sLoc == theGUID:  # If it matches the old pattern
                        references.append(
                            MindmapReference(direction=1, guid_1=sLoc, guid_2=eLoc)
                        )
                    else:
                        # Or handle direction=2 or other logic if needed
                        pass

        # For now, links, icons, tags, image remain unimplemented => empty
        links = []
        icons = []
        tags = []
        image = None

        return MindmapTopic(
            guid=theGUID,
            text=theName,
            rtf=theTitle,
            level=theLevel,
            notes=notes_obj,
            links=links,
            image=image,
            icons=icons,
            tags=tags,
            references=references,
        )
    
    def get_topic_by_id(self, topic_id):
        return topic_id

    def get_selection(self):
        """
        Return a list of topic IDs in the current selection.
        """
        result = self._read("getSelection")
        return result

    def get_level_from_topic(self, topic_id):
        if not topic_id:
            return None
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    return level of theTopic
                on error
                    return ""
                end try
            end tell
        '''
        level_str = _run_applescript(script)
        return int(level_str) if level_str.isdigit() else None

    def get_text_from_topic(self, topic_id):
        if not topic_id:
            return ""
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    return name of theTopic
                on error
                    return ""
                end try
            end tell
        '''
        text = _run_applescript(script)
        # Replace certain characters (as in original code)
        text = text.replace('"', '`').replace("'", "`").replace("\r", "").replace("\n", "")
        return text

    def get_title_from_topic(self, topic_id):
        if not topic_id:
            return ""
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    return title of theTopic
                on error
                    return ""
                end try
            end tell
        '''
        return _run_applescript(script)

    def get_subtopics_from_topic(self, topic_id):
        """
        Return a list of subtopic IDs.
        """
        if not topic_id:
            return []
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set subTs to subtopics of theTopic
                    set output to ""
                    repeat with t in subTs
                        set output to output & (id of t) & linefeed
                    end repeat
                    return output
                on error
                    return ""
                end try
            end tell
        '''
        raw = _run_applescript(script)
        return [x.strip() for x in raw.splitlines() if x.strip()]

    def get_links_from_topic(self, topic_id) -> list[MindmapLink]:
        return []

    def get_image_from_topic(self, topic_id) -> MindmapImage:
        return None

    def get_icons_from_topic(self, topic_id) -> list[MindmapIcon]:
        return []

    def get_notes_from_topic(self, topic_id) -> MindmapNotes:
        """
        Return MindmapNotes or None.
        """
        if not topic_id:
            return None
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    return notes of theTopic
                on error
                    return ""
                end try
            end tell
        '''
        notes_text = _run_applescript(script)
        if notes_text:
            return MindmapNotes(text=notes_text)
        return None

    def get_tags_from_topic(self, topic_id) -> list[MindmapTag]:
        return []

    def get_references_from_topic(self, topic_id) -> list[MindmapReference]:
        """
        Return a list of MindmapReference objects for the given topic.
        """
        references = []
        if not topic_id:
            return references

        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set rels to relationships of theTopic
                    if (count of rels) = 0 then
                        return ""
                    end if
                    set outList to ""
                    repeat with r in rels
                        set sLoc to id of (starting location of r)
                        set eLoc to id of (ending location of r)
                        set outList to outList & sLoc & "||" & eLoc & linefeed
                    end repeat
                    return outList
                on error
                    return ""
                end try
            end tell
        '''
        raw = _run_applescript(script)
        for line in raw.splitlines():
            parts = line.split("||")
            if len(parts) == 2:
                sLoc, eLoc = parts
                if sLoc == topic_id:
                    references.append(
                        MindmapReference(
                            direction=1,
                            guid_1=sLoc,
                            guid_2=eLoc
                        )
                    )
        return references

    def get_guid_from_topic(self, topic_id) -> str:
        return topic_id if topic_id else ""

    def add_subtopic_to_topic(self, topic_id, topic_text):
        """
        Create a new subtopic under `topic_id` with `topic_text`.
        Return the new subtopic's ID or None on failure.
        """
        if not topic_id:
            return None
        safe_text = topic_text.replace('"', '\\"')
        script = f'''
            tell application "MindManager"
                try
                    set parentTopic to first topic of document 1 whose id is "{topic_id}"
                    set newT to make new topic at end of subtopics of parentTopic with properties {{name:"{safe_text}"}}
                    return id of newT
                on error
                    return ""
                end try
            end tell
        '''
        new_id = _run_applescript(script)
        return new_id if new_id else None

    def get_parent_from_topic(self, topic_id):
        """
        Return the parent's ID or None if there is no parent or the topic doesn't exist.
        """
        if not topic_id:
            return None
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set p to parent of theTopic
                    if p is not missing value then
                        return id of p
                    else
                        return ""
                    end if
                on error
                    return ""
                end try
            end tell
        '''
        result = _run_applescript(script)
        return result if result else None

    def set_text_to_topic(self, topic_id, topic_text):
        """
        Set the topic's text (equivalent to topic.name.set).
        """
        if not topic_id:
            return
        safe_text = topic_text.replace('"', '\\"')
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set name of theTopic to "{safe_text}"
                end try
            end tell
        '''
        _run_applescript(script)

    def set_title_to_topic(self, topic_id, topic_rtf):
        """
        Set the topic's title (equivalent to topic.title.set).
        """
        if not topic_id:
            return
        safe_text = topic_rtf.replace('"', '\\"')
        script = f'''
            tell application "MindManager"
                try
                    set theTopic to first topic of document 1 whose id is "{topic_id}"
                    set title of theTopic to "{safe_text}"
                end try
            end tell
        '''
        _run_applescript(script)

    def add_tag_to_topic(self, topic_id, tag_text, topic_guid):
        pass

    def set_topic_from_mindmap_topic(self, topic_id, mindmap_topic, map_icons):
        """
        Updates the topic's text, RTF title, and notes from `mindmap_topic` 
        via a single AppleScript call. 
        Returns (refreshed_topic_id, original_topic_id).
        """
        if not topic_id and not mindmap_topic:
            return None, None
        
        if not topic_id:
            try:
                self._write("writeTree", mindmap_topic)
                return None, None

            except Exception as e:
                print(f"Error in set_topic_from_mindmap_topic: {e}")
                return None, None
        else:
            try:
                script_lines = []
                script_lines.append('tell application "MindManager"')
                script_lines.append('    try')
                script_lines.append(f'        set theTopic to first topic of document 1 whose id is "{topic_id}"')
                safe_text = (mindmap_topic.text or "").replace('"', '\\"')
                script_lines.append(f'        set name of theTopic to "{safe_text}"')
                if mindmap_topic.rtf:
                    safe_rtf = mindmap_topic.rtf.replace('"', '\\"')
                    script_lines.append(f'        set title of theTopic to "{safe_rtf}"')
                if mindmap_topic.notes:
                    safe_notes = (mindmap_topic.notes.text or "").replace('"', '\\"')
                    script_lines.append(f'        set notes of theTopic to "{safe_notes}"')
                script_lines.append('        return id of theTopic')
                script_lines.append('    on error errMsg')
                script_lines.append('        return ""')
                script_lines.append('    end try')
                script_lines.append('end tell')
                full_script = "\n".join(script_lines)
                refreshed_id = _run_applescript(full_script)
                if not refreshed_id:
                    return None, None
                return refreshed_id, topic_id

            except Exception as e:
                print(f"Error in set_topic_from_mindmap_topic: {e}")
                return None, None

    def create_map_icons(self, map_icons):
        pass

    def create_tags(self, tags: list[str], DUPLICATED_TAG: str):
        pass

    def add_relationship(self, guid1, guid2, label=''):
        if not guid1 or not guid2:
            print("Error in add_relationship: One or both topic IDs missing.")
            return
        script = f'''
            tell application "MindManager"
                try
                    set t1 to first topic of document 1 whose id is "{guid1}"
                    set t2 to first topic of document 1 whose id is "{guid2}"
                    if t1 is not missing value and t2 is not missing value then
                        make new relationship with properties {{starting location:t1, ending location:t2}}
                    end if
                on error errMsg
                    return ""
                end try
            end tell
        '''
        _run_applescript(script)

    def add_topic_link(self, guid1, guid2, label=''):
        pass

    def add_document(self, max_topic_level):
        """
        Opens the correct template based on charttype and subtopic counts.
        """
        if not self.document_exists():
            cnt_subtopics = 0
        else:
            script_count = '''
                tell application "MindManager"
                    set c to count of subtopics of central topic of document 1
                    return c
                end tell
            '''
            res = _run_applescript(script_count)
            try:
                cnt_subtopics = int(res)
            except:
                cnt_subtopics = 0

        if self._charttype == "orgchart":
            template_alias = self._orgchart_template
        elif self._charttype == "radial":
            template_alias = self._radial_template
        else:
            # "auto"
            if max_topic_level > 2 and cnt_subtopics > 4:
                template_alias = self._orgchart_template
            else:
                template_alias = self._radial_template

        safe_path = template_alias.replace('"', '\\"')
        script_open = f'''
            tell application "MindManager"
                open POSIX file "{safe_path}"
            end tell
        '''
        _run_applescript(script_open)

    def finalize(self, max_topic_level):
        """
        Balance the map, activate MindManager, optionally merge windows, and clean up.
        """
        if not self.document_exists():
            return

        # Balance map
        script_balance = '''
            tell application "MindManager"
                try
                    balance map of document 1
                end try
            end tell
        '''
        _run_applescript(script_balance)

        # Activate MindManager
        script_activate = '''
            tell application "MindManager"
                activate
            end tell
        '''
        _run_applescript(script_activate)

        # Optionally merge all windows
        if self.MACOS_MERGE_ALL_WINDOWS:
            self.merge_windows()

        # No persistent object references to clear
        pass
