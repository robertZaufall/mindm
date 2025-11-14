use framework "Foundation"
use scripting additions

property SCRIPT_EDITOR_MODE : false
property parent : me
property NSString : a reference to current application's NSString
property NSJSONSerialization : a reference to current application's NSJSONSerialization
property NSNull : a reference to current application's NSNull
property NSArray : a reference to current application's NSArray
property NSDictionary : a reference to current application's NSDictionary
property NSUTF8StringEncoding : a reference to current application's NSUTF8StringEncoding

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
			set testResult to my handleCommand({"writeTree", "{\"guid\": \"F35D6F0A-916B-4BD4-B6C5-6FD3B8873421\", \"text\": \"Creating an AI startup\", \"subtopics\": [{\"guid\": \"AABE2CFB-E72E-47DB-8358-FEDF652384AF\", \"text\": \"Vision & Strategy\", \"subtopics\": [{\"guid\": \"6EC7E029-8AAF-4F95-A4F7-2DF9FC9C274E\", \"text\": \"Mission & Value\", \"subtopics\": [{\"guid\": \"62753394-43CF-4EA4-9D11-32A0B01B2316\", \"text\": \"Problem Statement\"}, {\"guid\": \"3702BC7C-F340-4915-9B9C-EA7723168674\", \"text\": \"Value Proposition\"}, {\"guid\": \"2B1EABD7-8DA6-477D-9066-26E33AD8465E\", \"text\": \"Target Outcomes\"}]}, {\"guid\": \"BE661CA1-ADC8-42F4-AC12-2F86ABC965CB\", \"text\": \"Market Positioning\", \"subtopics\": [{\"guid\": \"63B699E2-743E-4586-87E6-ABD87D6486BE\", \"text\": \"Differentiation\"}, {\"guid\": \"02033FA2-8748-4B88-9D75-9D2913781E55\", \"text\": \"Target Segments\"}, {\"guid\": \"369BD38C-859B-4FCF-8AFA-8D1529E3659A\", \"text\": \"Competitive Edge\"}]}, {\"guid\": \"ECE4A5EA-883F-43FA-AAD8-DF7A8DE9A6EF\", \"text\": \"Roadmap Planning\", \"subtopics\": [{\"guid\": \"348D9A7A-F46B-40ED-A484-5481831CFBF3\", \"text\": \"Milestones\"}, {\"guid\": \"5E54DBFF-924D-494E-B792-48C27C78A67A\", \"text\": \"Success Metrics\"}]}]}, {\"guid\": \"012909AC-7D04-4066-84BF-DA1F34F50A27\", \"text\": \"Product Development\", \"subtopics\": [{\"guid\": \"BC2B8FF2-40D1-4298-8874-F6CD74BF6830\", \"text\": \"MVP Design\", \"subtopics\": [{\"guid\": \"8131DB69-6557-426F-8F2D-634CEB5563F9\", \"text\": \"Core Features\"}, {\"guid\": \"141446D1-9C6B-4810-B20B-D90E90B6CCBD\", \"text\": \"User Flows\"}, {\"guid\": \"F1F35599-2CFB-4F53-948C-158A9D7FE4EC\", \"text\": \"Success Criteria\"}]}, {\"guid\": \"833ECBF0-448B-40CC-BF87-DD4924A3FEAA\", \"text\": \"Data Strategy\", \"subtopics\": [{\"guid\": \"E11F6404-22D2-4D60-AB3D-F52898F088F5\", \"text\": \"Data Sources\"}, {\"guid\": \"19D2CDBD-6EEA-408D-A2E1-BF96E9E1E7C1\", \"text\": \"Labeling Plan\"}, {\"guid\": \"55D19F0B-1792-49FF-8A75-1DCFFAC1428A\", \"text\": \"Privacy Controls\"}]}, {\"guid\": \"3DD1CAEA-3B37-43E7-87C1-C3DFA22B3723\", \"text\": \"Model Lifecycle\", \"subtopics\": [{\"guid\": \"526F23CC-C658-4A9F-A894-76689A3B7CDB\", \"text\": \"Training Pipeline\"}, {\"guid\": \"46541951-9D8D-43A3-8246-5204F973B2F8\", \"text\": \"Evaluation Metrics\"}, {\"guid\": \"82A7CF2A-8D63-4A3B-9D54-4ADA1AB6FBEF\", \"text\": \"Iteration Plan\"}]}]}, {\"guid\": \"57DC272F-01E9-4B2A-B527-BE09A4380656\", \"text\": \"Team & Hiring\", \"subtopics\": [{\"guid\": \"9B3F327D-D163-4D6B-BE58-2F48C95D70D8\", \"text\": \"Founding Roles\", \"subtopics\": [{\"guid\": \"84D826FD-0439-4830-B00F-94CDD66D3BD0\", \"text\": \"CEO Responsibilities\"}, {\"guid\": \"6684A509-97EA-4458-9E10-60269A49389A\", \"text\": \"CTO Responsibilities\"}, {\"guid\": \"7B0D894C-36B1-49FB-8087-FB1C2EB5DD30\", \"text\": \"Product Lead Duties\"}]}, {\"guid\": \"E02B460A-02C1-4806-92DF-60FA8A1D96FA\", \"text\": \"Recruiting Plan\", \"subtopics\": [{\"guid\": \"888565DE-8B5C-4CE9-8CF3-5D7D1F7EF59B\", \"text\": \"Hiring Channels\"}, {\"guid\": \"4C4556A4-CC61-44F3-8BED-642DD034D2DA\", \"text\": \"Interview Process\"}]}, {\"guid\": \"89A17160-7CE0-460B-AAC0-E5D34C3D1CC0\", \"text\": \"Culture & Ops\", \"subtopics\": [{\"guid\": \"7CA6AC28-CC46-4290-A2C4-58221AA8DC92\", \"text\": \"Remote Policies\"}, {\"guid\": \"23A9F25C-4DD6-42DA-BEE7-02D542A88B95\", \"text\": \"Performance Reviews\"}]}]}, {\"guid\": \"33B58ECF-87BB-4A55-A1DF-0B9B8BFAB28C\", \"text\": \"Fundraising\", \"subtopics\": [{\"guid\": \"AF86A2B5-24AD-4C5B-9A47-B989B95D7DAB\", \"text\": \"Funding Strategy\", \"subtopics\": [{\"guid\": \"74CDCA7A-4FD5-4582-B3AB-0AD31EC3D9F3\", \"text\": \"Bootstrapping Plan\"}, {\"guid\": \"B8259997-4415-4E28-A22A-F7A7A50C3723\", \"text\": \"VC Pitch Focus\"}, {\"guid\": \"1F1F0714-4563-4A0E-8A23-05A5959F10FB\", \"text\": \"Angel Outreach\"}]}, {\"guid\": \"C088D7C0-536C-4D74-B0F8-411A70715A8F\", \"text\": \"Financial Planning\", \"subtopics\": [{\"guid\": \"0A837281-42C0-454B-80A7-E5D6009200BE\", \"text\": \"Burn Rate\"}, {\"guid\": \"56A17032-929C-4879-AAEC-2AEB56CECE45\", \"text\": \"Runway Management\"}, {\"guid\": \"26737FCB-647C-4919-8C1E-CF04DB82798A\", \"text\": \"Forecasts\"}]}, {\"guid\": \"B2040CFC-9B8A-4A81-AFB2-77ABA252AFD8\", \"text\": \"Investor Relations\", \"subtopics\": [{\"guid\": \"02F5F4D1-6333-491D-8473-7DA8CC17063F\", \"text\": \"Cap Table Management\"}, {\"guid\": \"854288EC-E443-4488-8EEC-E9266B3C764B\", \"text\": \"Demo Day Prep\"}]}]}, {\"guid\": \"00DCEE21-DF78-4994-B54A-719E34711383\", \"text\": \"Go-to-Market\", \"subtopics\": [{\"guid\": \"3F5AA657-3BC4-4A73-A808-76E497A6A350\", \"text\": \"Pricing Model\", \"subtopics\": [{\"guid\": \"AC53DAE8-4833-4A61-B6D6-DC0E3E8EBAC6\", \"text\": \"Subscription Plans\"}, {\"guid\": \"14430046-C744-4BBC-8EDA-563C18645FB1\", \"text\": \"Enterprise Pricing\"}]}, {\"guid\": \"CDF9F7D0-19B0-421D-ABD4-88BBB6FD1A16\", \"text\": \"Sales Strategy\", \"subtopics\": [{\"guid\": \"2909B9F8-6702-4F13-8E0E-4607077D3456\", \"text\": \"ICP Definition\"}, {\"guid\": \"070070AE-E98B-4F62-84EE-78958ED33CFE\", \"text\": \"Pipeline Management\"}, {\"guid\": \"F4E18FB4-CD26-4EDB-B5BC-158BBB526A64\", \"text\": \"Sales Hiring\"}]}, {\"guid\": \"F917AFF5-A2B7-4945-A0CD-E6229A8F5B5E\", \"text\": \"Marketing Plan\", \"subtopics\": [{\"guid\": \"A97358A2-D7DE-49F6-B511-4DAF6FAFB0D4\", \"text\": \"Content Strategy\"}, {\"guid\": \"63711491-91BB-4C68-A723-FCD075536FD1\", \"text\": \"Demand Gen Channels\"}, {\"guid\": \"AAC055E2-6CED-47F1-8B48-5E568858DFBA\", \"text\": \"PR & Partnerships\"}]}]}]}"})
			-- set testResult to my handleCommand({"writeTree", "{\"guid\":\"test-guid\", \"text\":\"Test Topic\", \"level\":0, \"notes\":\"Test notes\", \"subtopics\":[]}"})
			-- set testResult to my handleCommand({"setProperties", "{\"guid\":\"existing-guid\", \"text\":\"Updated Text\", \"level\":1, \"notes\":\"Updated notes\"}"})
			return testResult
		else
			return "{ \"error\": \"No operation mode specified.\" }"
		end if
	end if

	set operationMode to item 1 of argv
	set operationArgs to rest of argv

	if operationMode is "writeTree" or operationMode is "writeFragment" or operationMode is "setProperties" then
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
		if operationMode is "writeTree" then
			if (count of operationArgs) is not 1 then return "{ \"error\": \"Mode 'writeTree' requires exactly 1 argument (JSON data).\" }"
			set jsonData to item 1 of operationArgs
			return my doWriteTree(jsonData)
			
		else if operationMode is "writeFragment" then
			if (count of operationArgs) is not 1 then return "{ \"error\": \"Mode 'writeFragment' requires exactly 1 argument (JSON data).\" }"
			set jsonData to item 1 of operationArgs
			return my doWriteFragment(jsonData)
			
		else if operationMode is "setProperties" then
			if (count of operationArgs) is not 1 then return "{ \"error\": \"Mode 'setProperties' requires exactly 1 argument (JSON data).\" }"
			set jsonData to item 1 of operationArgs
			return my doSetProperties(jsonData)
			
		else
			return "{ \"error\": \"Unknown operation mode: " & my escapeJSON(operationMode) & "\" }"
		end if
		
	on error errMsg number errNum
		return "{ \"error\": \"Execution failed for mode '" & my escapeJSON(operationMode) & "': " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end handleCommand

on doWriteTree(jsonData)
	try
		-- Parse the JSON and create a new document with the tree structure
		set parsedData to my parseTopicJSON(jsonData)
		if errorStatus of parsedData is true then
			return "{ \"error\": \"JSON parsing failed: " & my escapeJSON(errorMsg of parsedData) & "\" }"
		end if
		
		tell application "MindManager"
			-- Create new document or clear existing one
			if (count of documents) > 0 then
				tell document 1
					set name of central topic to topicText of parsedData
					if topicNotes of parsedData is not "" then
						set notes of central topic to topicNotes of parsedData
					end if
					-- Remove existing subtopics
					delete every subtopic of central topic
				end tell
			else
				make new document
				tell document 1
					set name of central topic to topicText of parsedData
					if topicNotes of parsedData is not "" then
						set notes of central topic to topicNotes of parsedData
					end if
				end tell
			end if
			
			-- Build the tree structure recursively
			set result to my buildTreeFromJSON(central topic of document 1, topicSubtopics of parsedData)
			if result contains "error" then
				return result
			end if
		end tell
		
		return "{ \"success\": \"Tree written successfully\" }"
		
	on error errMsg number errNum
		return "{ \"error\": \"Error in doWriteTree: " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end doWriteTree

on doWriteFragment(jsonData)
	try
		-- Parse the JSON and add fragment to current selection or central topic
		set parsedData to my parseTopicJSON(jsonData)
		if errorStatus of parsedData is true then
			return "{ \"error\": \"JSON parsing failed: " & my escapeJSON(errorMsg of parsedData) & "\" }"
		end if
		
		tell application "MindManager"
			tell document 1
				set selItems to selection
				set targetTopic to missing value
				
				if (count of selItems) > 0 then
					set targetTopic to item 1 of selItems
				else
					set targetTopic to central topic
				end if
				
				-- Create the fragment as a subtopic
				set newSubtopic to make new subtopic at end of subtopics of targetTopic
				set name of newSubtopic to topicText of parsedData
				if topicNotes of parsedData is not "" then
					set notes of newSubtopic to topicNotes of parsedData
				end if
				
				-- Build subtopics recursively
				set result to my buildTreeFromJSON(newSubtopic, topicSubtopics of parsedData)
				if result contains "error" then
					return result
				end if
			end tell
		end tell
		
		return "{ \"success\": \"Fragment written successfully\" }"
		
	on error errMsg number errNum
		return "{ \"error\": \"Error in doWriteFragment: " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end doWriteFragment

on doSetProperties(jsonData)
	try
		-- Parse the JSON and update properties of existing topic
		set parsedData to my parseTopicJSON(jsonData)
		if errorStatus of parsedData is true then
			return "{ \"error\": \"JSON parsing failed: " & my escapeJSON(errorMsg of parsedData) & "\" }"
		end if
		
		set targetGuid to topicGuid of parsedData
		if targetGuid is "" then
			return "{ \"error\": \"GUID is required for setProperties operation\" }"
		end if
		
		set targetTopic to my _findTopicByID(targetGuid)
		if targetTopic is missing value then
			return "{ \"error\": \"Topic with GUID '" & my escapeJSON(targetGuid) & "' not found\" }"
		end if
		
		tell application "MindManager"
			tell targetTopic
				if topicText of parsedData is not "" then
					set name to topicText of parsedData
				end if
				if topicNotes of parsedData is not "" then
					set notes to topicNotes of parsedData
				end if
			end tell
		end tell
		
		return "{ \"success\": \"Properties updated successfully\" }"
		
	on error errMsg number errNum
		return "{ \"error\": \"Error in doSetProperties: " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end doSetProperties

on buildTreeFromJSON(parentTopic, subtopicsData)
	try
		repeat with subtopicData in subtopicsData
			set parsedSubtopic to contents of subtopicData
			
			if class of parsedSubtopic is not record then
				set parsedSubtopic to my parseTopicJSON(parsedSubtopic)
			end if
			
			if class of parsedSubtopic is not record then
				return "{ \"error\": \"Error parsing subtopic: Unsupported data type\" }"
			end if
			
			if errorStatus of parsedSubtopic is true then
				return "{ \"error\": \"Error parsing subtopic: " & my escapeJSON(errorMsg of parsedSubtopic) & "\" }"
			end if
			
			tell application "MindManager"
				tell parentTopic
					set newSubtopic to make new subtopic at end of subtopics
					set name of newSubtopic to topicText of parsedSubtopic
					if topicNotes of parsedSubtopic is not "" then
						set notes of newSubtopic to topicNotes of parsedSubtopic
					end if
				end tell
			end tell
			
			-- Recursively build subtopics
			if (count of topicSubtopics of parsedSubtopic) > 0 then
				set result to my buildTreeFromJSON(newSubtopic, topicSubtopics of parsedSubtopic)
				if result contains "error" then
					return result
				end if
			end if
		end repeat
		
		return "success"
		
	on error errMsg number errNum
		return "{ \"error\": \"Error building tree: " & my escapeJSON(errMsg) & " (Code: " & errNum & ")\" }"
	end try
end buildTreeFromJSON

on parseTopicJSON(jsonInput)
	-- Parse JSON topic data into a normalized record using Foundation
	try
		if class of jsonInput is not text and class of jsonInput is not string then
			set jsonString to jsonInput as text
		else
			set jsonString to jsonInput as text
		end if
		
		set nsString to (NSString's stringWithString:jsonString)
		set jsonData to (nsString's dataUsingEncoding:NSUTF8StringEncoding)
		if jsonData is missing value then error "Unable to encode JSON text as UTF-8."
		
			set parsedObject to (NSJSONSerialization's JSONObjectWithData:jsonData options:0 |error|:(missing value))
			if parsedObject is missing value then
				set errorText to "Unable to parse JSON payload."
				return {errorStatus:true, errorMsg:errorText, topicGuid:"", topicText:"", topicLevel:0, topicNotes:"", topicSubtopics:{}}
			end if
			
			if ((parsedObject's isKindOfClass:NSDictionary) as boolean) is false then
			return {errorStatus:true, errorMsg:"JSON root is not an object.", topicGuid:"", topicText:"", topicLevel:0, topicNotes:"", topicSubtopics:{}}
		end if
		
		return my _dictionaryToTopicRecord(parsedObject)
		
	on error errMsg number errNum
		return {errorStatus:true, errorMsg:"JSON parsing error: " & errMsg & " (Code: " & errNum & ")", topicGuid:"", topicText:"", topicLevel:0, topicNotes:"", topicSubtopics:{}}
	end try
end parseTopicJSON

on _dictionaryToTopicRecord(topicDict)
	set topicGuid to my _coerceToText((topicDict's objectForKey_("guid")))
	set topicText to my _coerceToText((topicDict's objectForKey_("text")))
	set topicNotes to my _coerceToText((topicDict's objectForKey_("notes")))
	
	set rawLevel to (topicDict's objectForKey_("level"))
	set topicLevel to 0
	if rawLevel is not missing value then
		try
			if ((rawLevel's isKindOfClass:NSNull) as boolean) is false then
				try
					set topicLevel to rawLevel as integer
				end try
			end if
		end try
	end if
	
	set subtopicRecords to {}
	set rawSubtopics to (topicDict's objectForKey_("subtopics"))
	if rawSubtopics is not missing value then
		try
			if ((rawSubtopics's isKindOfClass:NSArray) as boolean) is true then
				set subtopicCount to ((rawSubtopics's |count|()) as integer)
				if subtopicCount > 0 then
					repeat with i from 0 to (subtopicCount - 1)
						set subtopicDict to (rawSubtopics's objectAtIndex:i)
						if ((subtopicDict's isKindOfClass:NSDictionary) as boolean) is true then
							set end of subtopicRecords to my _dictionaryToTopicRecord(subtopicDict)
						end if
					end repeat
				end if
			end if
		end try
	end if
	
	return {errorStatus:false, errorMsg:"", topicGuid:topicGuid, topicText:topicText, topicLevel:topicLevel, topicNotes:topicNotes, topicSubtopics:subtopicRecords}
end _dictionaryToTopicRecord

on _coerceToText(valueToCoerce)
	if valueToCoerce is missing value then return ""
	try
		if (valueToCoerce's isKindOfClass:NSNull) as boolean then return ""
	on error
		-- Value is not an Objective-C object; continue
	end try
	try
		return valueToCoerce as text
	on error
		try
			if (valueToCoerce's respondsToSelector:"stringValue") as boolean then
				return valueToCoerce's stringValue() as text
			else if (valueToCoerce's respondsToSelector:"description") as boolean then
				return valueToCoerce's description() as text
			else
				return ""
			end if
		on error
			return ""
		end try
	end try
end _coerceToText

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
