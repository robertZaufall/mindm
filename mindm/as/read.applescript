use scripting additions

property SCRIPT_EDITOR_MODE : false
property parent : me

on run argv
	try
		return my handleCommand(argv)
	on error errMsg number errNum
		local basicEscapedMsg
		try
			set basicEscapedMsg to my escapeJSON(errMsg as text)
		on error
			set basicEscapedMsg to "Error message could not be escaped."
		end try
		return "{ \"error\": \"Top-level script error: " & basicEscapedMsg & " (Code: " & errNum & ")\" }"
	end try
end run

on handleCommand(argv)
	if (count of argv) is 0 then
		if SCRIPT_EDITOR_MODE then
			-- set testResult to my handleCommand({"getSelection"})
			set testResult to my handleCommand({"getTree", ""})
			-- set testResult to my handleCommand({"getTree", "5C9B484E-3AAF-914B-A721-3BD81BA790CF"})
			-- set testResult to my handleCommand({"getListProperties", "5C9B484E-3AAF-914B-A721-3BD81BA790CF", "9C0E27E6-BC9C-7546-93E9-617B79C9ACA1"})
			-- set testResult to my handleCommand({"getSingleProperties", "87189219-194F-A549-AE08-BF94E1BF590A"})
			return testResult
		else
			return "{ \"error\": \"No operation mode specified.\" }"
		end if
	end if
	
	set operationMode to item 1 of argv
	set operationArgs to rest of argv
	
	if operationMode is "getSingleProperties" or operationMode is "getTree" or operationMode is "getListProperties" or operationMode is "getSelection" then
		try
			tell application "MindManager"
				if not running then error "MindManager application is not running." number -1708
				if (count of documents) is 0 then error "No MindManager document is open."
			end tell
		on error checkErr number checkErrNum
			return "{ \"error\": \"MindManager Access Check Failed: " & my escapeJSON(checkErr) & " (Code: " & checkErrNum & ")\" }"
		end try
	end if
	
	try
		if operationMode is "getSingleProperties" then
			if (count of operationArgs) is not 1 then return "{ \"error\": \"Mode 'getSingleProperties' requires exactly 1 argument (topicID).\" }"
			set topicID to item 1 of operationArgs
			return my doGetSingleProperties(topicID)

		else if operationMode is "getSelection" then
			if (count of operationArgs) is not 0 then return "{ \"error\": \"Mode 'getSelection' does not require any arguments.\" }"
			return my doGetSelection()

		else if operationMode is "getTree" then
			local startTopicID, theStartTopic
			if (count of operationArgs) is 0 or item 1 of operationArgs is "" or item 1 of operationArgs is " " then
				set theStartTopic to my _getCentralTopic()
				if theStartTopic is missing value then return "{ \"error\": \"Could not retrieve the central topic.\" }"
			else
				if (count of operationArgs) is not 1 then return "{ \"error\": \"Mode 'getTree' requires 0 or 1 argument (optional topicID).\" }" # Corrected error message
				set startTopicID to item 1 of operationArgs
				set theStartTopic to my _findTopicByID(startTopicID)
				if theStartTopic is missing value then return "{ \"error\": \"Starting topic for tree not found with ID: " & my escapeJSON(startTopicID) & "\" }"
			end if
			return my doGetTree(theStartTopic)
			
		else if operationMode is "getListProperties" then
			if (count of operationArgs) is 0 then return "{ \"error\": \"Mode 'getListProperties' requires at least 1 argument (topicID list).\" }"
			return my doGetListProperties(operationArgs)
		else
			return "{ \"error\": \"Unknown operation mode: " & my escapeJSON(operationMode) & "\" }"
		end if
		
	on error errMsg number errNum
		return "{ \"error\": \"Execution failed for mode '" & my escapeJSON(operationMode) & "': " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end handleCommand

on doGetSelection()
    -- ask once, outside the repeat, for performance and to keep the
    -- try/on?error scope tight
    try
        tell application "MindManager"
            set selItems to selection of document 1 -- this is a LIST
        end tell
    on error errMsg number errNum
        return "{\"error\":\"Could not fetch selection: " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\"}"
    end try
    
    if selItems is {} then return "[]" -- nothing is highlighted
    
    set jsonObjects to {}
    repeat with oneItem in selItems
        try
            -- will raise an error if oneItem is not a topic
            set end of jsonObjects to my doGetSingleProperties(id of oneItem)
        end try
    end repeat
    
    -- build the JSON array
    set AppleScript's text item delimiters to ","
    set finalJSON to "[" & (jsonObjects as text) & "]"
    set AppleScript's text item delimiters to ""
    return finalJSON
end doGetSelection

-- Mode 1: Get properties for a single topic ID
on doGetSingleProperties(topicID as string)
	if topicID is "" then return "{ \"error\": \"Empty topic ID provided.\" }"
	
	set theTopic to my _findTopicByID(topicID)
	if theTopic is missing value then
		return "{ \"error\": \"Topic with ID '" & my escapeJSON(topicID) & "' not found.\" }"
	end if
	
	try
		set propertiesRecord to my _get_topic_properties_record(theTopic, topicID)
		if errorStatus of propertiesRecord is true then
			return "{ \"error\": \"Error fetching properties for ID '" & my escapeJSON(topicID) & "': " & my escapeJSON(errorMsg of propertiesRecord) & "\" }"
		end if
		
		set escapedID to my escapeJSON(topicID)
		set escapedName to my escapeJSON(propName of propertiesRecord)
		set escapedNotes to my escapeJSON(propNotes of propertiesRecord)
		set propLevel to propLevel of propertiesRecord
		
		return "{\"guid\":\"" & escapedID & "\", \"text\":\"" & escapedName & "\", \"level\":" & propLevel & ", \"notes\":\"" & escapedNotes & "\"}"
	on error errMsg number errNum
		return "{ \"guid\":\"" & my escapeJSON(topicID) & "\", \"error\": \"Unexpected error in doGetSingleProperties: " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end doGetSingleProperties

-- Mode 2: Get the topic tree starting from a specific topic
on doGetTree(startTopic)
	try
		return my _buildTreeRecursive(startTopic)
	on error errMsg number errNum
		local startTopicID
		try
			tell application "MindManager" to set startTopicID to id of startTopic
		on error
			set startTopicID to "[unknown]"
		end try
		return "{ \"error\": \"Error building tree starting from topic " & startTopicID & ": " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end doGetTree

-- Mode 3: Get properties for a list of topic IDs
on doGetListProperties(topicIDList as list)
	set resultsList to {}
	set errorsEncountered to {}
	
	set oldTID to AppleScript's text item delimiters
	set AppleScript's text item delimiters to "," 
	
	repeat with currentTopicID in topicIDList
		set currentTopicID_str to ""
		try
			set currentTopicID_str to currentTopicID as string
			if currentTopicID_str is "" then
				error "Empty topic ID encountered in list."
			end if
			
			set theTopic to my _findTopicByID(currentTopicID_str)
			
			if theTopic is missing value then
				set end of errorsEncountered to "Topic ID '" & my escapeJSON(currentTopicID_str) & "' not found."
			else
				try
					set propertiesRecord to my _get_topic_properties_record(theTopic, currentTopicID_str)
					if errorStatus of propertiesRecord is true then
						set end of errorsEncountered to "Error fetching properties for ID '" & my escapeJSON(currentTopicID_str) & "': " & my escapeJSON(errorMsg of propertiesRecord)
					else
						set escapedID to my escapeJSON(currentTopicID_str)
						set escapedName to my escapeJSON(propName of propertiesRecord)
						set escapedNotes to my escapeJSON(propNotes of propertiesRecord)
						set propLevel to propLevel of propertiesRecord
						set jsonObject to "{\"guid\":\"" & escapedID & "\", \"text\":\"" & escapedName & "\", \"level\":" & propLevel & ", \"notes\":\"" & escapedNotes & "\"}"
						set end of resultsList to jsonObject
					end if
				on error errMsg number errNum
					set end of errorsEncountered to "Error processing topic ID '" & my escapeJSON(currentTopicID_str) & "': " & my escapeJSON(errMsg) & " (Code: " & errNum & ")"
				end try
			end if
			
		on error errItemMsg number errItemNum
			local nonStringErr
			try
				set nonStringErr to class of currentTopicID
			on error
				set nonStringErr to "unknown type"
			end try
			if currentTopicID_str is "" and errItemMsg contains "Cannot make" then
				set end of errorsEncountered to "Invalid item in topic ID list (not text, type: " & nonStringErr & ", value: " & (currentTopicID as text) & ")"
			else
				set end of errorsEncountered to errItemMsg & " (Code: " & errItemNum & ")"
			end if
		end try
	end repeat
	
	set finalJSON to "[" & (resultsList as text) & "]"
	set AppleScript's text item delimiters to oldTID
	
	if (count of errorsEncountered) > 0 then
		log "--- Errors encountered during getListProperties ---"
		repeat with errItem in errorsEncountered
			log errItem
		end repeat
		log "--- End Errors ---"
	end if
	
	return finalJSON
end doGetListProperties


on _buildTreeRecursive(aTopic)
	local topicID, propertiesRecord, tID_escaped, tName_escaped, tLevel, tNotes_escaped, childJSONs, childTopicObjects, childTopic, jsonText, oldTID, idErr, childErr
	
	set topicID to missing value
	try
		tell application "MindManager" to set topicID to id of aTopic
	on error idErr
		log "Critical Error: Failed to get ID for a topic object during tree build: " & (idErr as text)
		return "{ \"error\": \"Failed to get ID for a topic object. Cannot proceed with this branch.\" }"
	end try
	
	set propertiesRecord to my _get_topic_properties_record(aTopic, topicID)
	
	set tID_escaped to my escapeJSON(topicID)
	if errorStatus of propertiesRecord is true then
		set tName_escaped to "\"<Error fetching name>\""
		set tLevel to -1
		set tNotes_escaped to my escapeJSON("Property Error: " & (errorMsg of propertiesRecord))
		log "Warning: Properties fetch failed for topic " & topicID & " during tree build: " & errorMsg of propertiesRecord
	else
		set tName_escaped to my escapeJSON(propName of propertiesRecord)
		set tLevel to propLevel of propertiesRecord
		set tNotes_escaped to my escapeJSON(propNotes of propertiesRecord)
	end if
	
	set childJSONs to {}
	set childTopicObjects to my _get_subtopics_objects(aTopic, topicID)
	if childTopicObjects is not missing value then
		repeat with childTopic in childTopicObjects
			try
				set end of childJSONs to my _buildTreeRecursive(childTopic)
			on error childErr number childErrNum
				log "Error processing child during recursion for parent " & topicID & ": " & childErr & " (" & childErrNum & ")"
				set end of childJSONs to "{ \"error\": \"Error processing child topic: " & my escapeJSON(childErr as text) & "\" }"
			end try
		end repeat
	else
		set childJSONs to {"{ \"error\": \"Could not retrieve subtopics for topic " & tID_escaped & "\" }"}
	end if
	
	set oldTID to AppleScript's text item delimiters
	set AppleScript's text item delimiters to ","
	set jsonText to "{\"guid\":\"" & tID_escaped & "\", \"text\":\"" & tName_escaped & "\", \"level\":" & tLevel & ", \"notes\":\"" & tNotes_escaped & "\", \"subtopics\":[" & (childJSONs as text) & "]}"
	set AppleScript's text item delimiters to oldTID
	
	return jsonText
end _buildTreeRecursive

on _get_topic_properties_record(theTopic, topicIDForError)
	local propName, propLevel, propNotesText, mainErr, levelErr, notesErr, nameErr
	
	set propName to "[Name Error]"
	set propLevel to -1
	set propNotesText to ""
	set errorStatus to false
	set errorMsg to ""
	
	try
		if theTopic is missing value then error "Invalid topic object provided."
		
		tell application "MindManager"
			try
				set propName to name of theTopic
			on error nameErr
				set errorStatus to true
				set errorMsg to errorMsg & "Failed to get name. "
				log "Warning (_get_topic_properties_record): Could not get name for topic " & topicIDForError & ": " & (nameErr as rich text)
			end try
			
			try
				set propLevel to level of theTopic
			on error levelErr
				set errorStatus to true
				set errorMsg to errorMsg & "Failed to get level. "
				log "Warning (_get_topic_properties_record): Could not get level for topic " & topicIDForError & ": " & (levelErr as rich text)
			end try
			
			try
				set propNotesText to notes of theTopic as rich text
			on error notesErr
				set propNotesText to ""
				set errorMsg to errorMsg & "Failed to get notes. "
				log "Warning (_get_topic_properties_record): Could not get notes for topic " & topicIDForError & ": " & (notesErr as rich text) & " (" & (number of notesErr) & ")"
			end try
		end tell
		
		if errorStatus then
			return {errorStatus:true, errorMsg:errorMsg, propName:propName, propLevel:propLevel, propNotes:propNotesText}
		else
			return {errorStatus:false, propName:propName, propLevel:propLevel, propNotes:propNotesText}
		end if
		
	on error mainErr number mainErrNum
		return {errorStatus:true, errorMsg:"Unexpected error in _get_topic_properties_record for " & topicIDForError & ": " & (mainErr as text) & " (Code: " & mainErrNum & ")", propName:"", propLevel:-1, propNotes:""}
	end try
end _get_topic_properties_record

on _get_subtopics_objects(parentTopic, parentIDForLog)
	local childList, childErr, attempt
	set childList to missing value
	try
		if parentTopic is missing value then error "Invalid parent topic object provided."
		tell application "MindManager"
			tell parentTopic
				try
					set childList to every subtopic
					return childList
				on error childErr
					log "Info (" & parentIDForLog & "): _get_subtopics_objects ('every subtopic') failed: " & (childErr as rich text)
				end try
			end tell
		end tell
		if childList is missing value then
			log "Error getting subtopics for topic ID '" & parentIDForLog & "': All attempts failed."
			return missing value
		else
			log "Warning (" & parentIDForLog & "): Reached end of _get_subtopics_objects unexpectedly. Returning empty list."
			return {}
		end if
	on error mainErr number mainErrNum
		log "Critical error in _get_subtopics_objects for topic ID '" & parentIDForLog & "': " & (mainErr as text) & " (Code: " & mainErrNum & ")"
		return missing value
	end try
end _get_subtopics_objects

on _findTopicByID(targetID as string)
	if targetID is "" then return missing value
	try
		tell application "MindManager"
			tell document 1
				if id of central topic is targetID then return central topic
				try
					set foundTopics to (every topic whose id is targetID)
					if (count of foundTopics) > 0 then
						return item 1 of foundTopics
					else
						return missing value
					end if
				on error findErr number findErrNum
					if findErrNum is -1728 then
						return missing value
					else
						log "Error using 'whose' clause in _findTopicByID for ID " & targetID & ": " & findErr & " (" & findErrNum & ")"
						error "MindManager search failed unexpectedly." number findErrNum
					end if
				end try
			end tell
		end tell
	on error errMsg number errNum
		log "Error in _findTopicByID searching for " & targetID & ": " & (errMsg as text) & " (Code: " & errNum & ")"
		return missing value
	end try
end _findTopicByID

on _getCentralTopic()
	try
		tell application "MindManager"
			if not running or (count of documents) is 0 then return missing value
			return central topic of document 1
		end tell
	on error errMsg number errNum
		log "Error getting central topic: " & errMsg & " (" & errNum & ")"
		return missing value
	end try
end _getCentralTopic

on escapeJSON(txt)
	local originalDelimiters, textItems, theClass
	try
		set theClass to class of txt
		if theClass is not text and theClass is not string then
			set txt to txt as text
		end if
	on error
		if txt is missing value then return ""
		log "Warning: escapeJSON received non-text data: " & (txt as text)
		return "[Error: Non-text data]"
	end try
	set originalDelimiters to AppleScript's text item delimiters
	try
		set AppleScript's text item delimiters to "\\"
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\\\"
		set txt to textItems as text
		set AppleScript's text item delimiters to "\""
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\\""
		set txt to textItems as text
		set AppleScript's text item delimiters to "/"
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\/"
		set txt to textItems as text
		set AppleScript's text item delimiters to return & linefeed
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\n"
		set txt to textItems as text
		set AppleScript's text item delimiters to return
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\n"
		set txt to textItems as text
		set AppleScript's text item delimiters to linefeed
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\n"
		set txt to textItems as text
		set AppleScript's text item delimiters to tab
		set textItems to text items of txt
		set AppleScript's text item delimiters to "\\t"
		set txt to textItems as text
		set AppleScript's text item delimiters to originalDelimiters
		return txt
	on error e
		set AppleScript's text item delimiters to originalDelimiters
		return "[\"Error during JSON escaping: " & (e as text) & "\"]"
	end try
end escapeJSON
