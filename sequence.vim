"So this file contains utility-functions for generated json-sequence,
"and accompaning ascii-graph.
"
"It has functions to load in the json-config,
"and color the different components
"and add commands to be used on different components


function ExecuteCommandOnCoord(commandName)
	"Execute a command with commandName = watevs. set in
	"vim -> commands -> <target> -> <cmd> 
	"Depending on where we are, and also if the command is defined

	
	let commandName = a:commandName

	let pos = getcurpos()

	" Becuz coords in the list are 0-counted (as god intended), 
	" but lines and cols are 1-counted (the work of the devil)
	" We must do a little decrementolino
	let x = pos[2] - 1
	let y = pos[1] - 1

	if has_key(g:sequence, "vim")
		let sequenceVimConfig = g:sequence["vim"]
		
		if has_key(sequenceVimConfig, "commands")
			let commands = sequenceVimConfig["commands"]

			if has_key(commands, commandName)
				for coordList in commands[commandName] 
					let startCoord = coordList[0][0]
					let endCoord = coordList[0][1]
					
					if y >= startCoord[1] && y <= endCoord[1] 
						if x >= startCoord[0] && x < endCoord[0] 
							let commandString = coordList[1]
							execute(commandString)
							return
						endif
					endif
				endfor
			endif
		endif
	endif
endfunction


function LoadSequence(fileName)
	"Load in the sequence. It will be stored in a global variable
	"Not very nice solution, but hey...    just hey.
	
	let g:sequence = json_decode(join(readfile(a:fileName), "\n"))

endfunction


function CreateHighlight(name, colorConfig)
	"Apply colors found in colorConfig to highlight with name
	"General way of applying color, hopefully :)

	let colorString = ""

	if has_key(a:colorConfig, "fg")
		let colorString = colorString . " ctermfg=" . a:colorConfig["fg"]
	endif

	if has_key(a:colorConfig, "bg")
		let colorString = colorString . " ctermbg=" . a:colorConfig["bg"]
	endif

	execute "highlight " . a:name . colorString 
endfunction


function ApplySyntaxOnCoordinates(coordinateList, highlightName)
	"coordinateList is a list of coordinate lists: [[x0, y0], [x1, y0]]
	for range in a:coordinateList 
		
		let start = "\\%" . (range[0][1] + 1) . "l" . "\\%" . (range[0][0] + 1) . "c"
		let end   = "\\%" . (range[1][1] + 1) . "l" . "\\%" . (range[1][0] + 1) . "c"

		let syntaxCommand = "syntax region " . a:highlightName . " start=\"" . start . "\" end=\"" . end . "\""
		
		"echom syntaxCommand

		execute syntaxCommand 
	endfor
endfunction


function ApplyTimeLineColor(item, highlightName)
	"Apply the color to the timeLine for this item (entity)
	"Note it gets the same color as border as it is called now. Not good.
	"Should be changed
	for coord in a:item["timeLineCoordinateList"]
		let start = "\\%" . (coord[1] + 1) . "l" . "\\%" . (coord[0] + 1) . "c"
		let end   = "\\%" . (coord[1] + 1) . "l" . "\\%" . (coord[0] + 2) . "c"

		let syntaxCommand = "syntax region " . a:highlightName . " start=\"" . start . "\" end=\"" . end . "\""

		"echom syntaxCommand

		execute syntaxCommand 
	endfor
endfunction


function ApplyBorderColor(item, itemVimConfig, runningItemNum)
	"Apply any border colors if any exists
	
	if has_key(a:itemVimConfig, "style")
		let styleConfig = a:itemVimConfig["style"]

		if has_key(styleConfig, "color")
			let colorConfig = styleConfig["color"]

			if has_key(colorConfig, "border")
				let borderColorConfig = colorConfig["border"]

				let item_border_highlight_name = "thing_" . a:runningItemNum . "_border_color"

				call CreateHighlight(item_border_highlight_name, borderColorConfig)

				call ApplySyntaxOnCoordinates(a:item["borderCoordinateList"], item_border_highlight_name)

				if has_key(a:item, "timeLineCoordinateList")
					"Lets treat the timeLine as an extension of the border...
					"This might not be what u want though, so it should be changed later :)
					call ApplyTimeLineColor(a:item, item_border_highlight_name)
				endif
			endif
		endif
	endif
endfunction


function ApplyLineColor(thing, vimConfig, runningNum)

	if has_key(a:vimConfig, "style")
		let styleConfig = a:vimConfig["style"]

		if has_key(styleConfig, "color")
			let colorConfig = styleConfig["color"]
			if has_key(colorConfig, "line")
				let thing_border_highlight_name = "thing_" . a:runningNum . "_line_color"

				let lineConfig = colorConfig["line"]

				call CreateHighlight(thing_border_highlight_name, lineConfig)

				call ApplySyntaxOnCoordinates(a:thing["lineCoordinateList"], thing_border_highlight_name)
			endif
		endif
	endif
endfunction


function ApplyVariantColor(variant, runningNum)
	let runningNum = a:runningNum
	if has_key(a:variant, "vim")
		"echom Apply border to variant
		call ApplyBorderColor(a:variant, a:variant["vim"], runningNum)
		let runningNum = runningNum + 1
		
	endif

	for branch in a:variant["branchList"]
		for action in branch["actionList"]
			let runningNum = ApplyActionColor(action, runningNum)
		endfor
	endfor

	return runningNum

endfunction


function ApplyActionColor(action, runningNum)
	let runningNum = a:runningNum

	if a:action["type"] == "on"
	
		if has_key(a:action, "vim")
			call ApplyBorderColor(a:action, a:action["vim"], runningNum)
			let runningNum = runningNum + 1
		endif

	elseif a:action["type"] == "communication"

		if has_key(a:action, "vim")
			call ApplyLineColor(a:action, a:action["vim"], runningNum)
			let runningNum = runningNum + 1
		endif

	elseif a:action["type"] == "variant"

		if has_key(a:action, "vim")
			let runningNum = ApplyVariantColor(a:action, runningNum)
		endif
	
	
	endif

	return runningNum
	
endfunction


function ApplyItemColor(item, runningItemNum)

	let item = a:item

	let runningItemNum = a:runningItemNum

	if has_key(item, "vim")
		let itemVimConfig = item["vim"]	

		call ApplyBorderColor(item, itemVimConfig, runningItemNum)
		let runningItemNum += 1
	endif

	if a:item["type"] == "container"
		for subItem in a:item["itemList"]	
			let runningItemNum = ApplyItemColor(subItem, runningItemNum)
		endfor
	endif

	return runningItemNum

endfunction


function ApplyColor()
	let runningNum = 0
	for item in g:sequence["itemList"]
		let runningNum = ApplyItemColor(item, runningNum)
	endfor

	for action in g:sequence["actionList"]
		call ApplyActionColor(action, runningNum)
	endfor
endfunction


function ApplyStyle()
	"Yesh (sean connery yes) its pretty empty as of now since we only gots
	"the color...
	call ApplyColor()
endfunction


function InitializeCommands()
	"Initialize commands
	"well. idea is to get all commands in sequence[vim][commands]
	"and then create a mapping for it to be used. Can it be smart? yesn't 
	"
	if has_key(g:sequence, "vim")
		let vimConfig = g:sequence["vim"]

		if has_key(vimConfig, "commands")
			for cmd in keys(vimConfig["commands"])
				execute "nnoremap <buffer> <leader>" . cmd . " :call ExecuteCommandOnCoord(\"" . cmd . "\")<CR>"
			endfor
		endif
	endif

endfunction


function InitializeVimSequence(fileName)
	"Initialize the sequence by loading the json-file,
	"applying style and initializing commands.

	call LoadSequence(a:fileName)

	call ApplyStyle()

	call InitializeCommands()

	"To make gg go to same column at first row when jumping back and
	"forth. Its really nice.
	setlocal nostartofline

endfunction


