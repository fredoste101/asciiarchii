" So this file contains utility-functions for generated json-sequence,
" and accompaning ascii-graph.
"
" It has functions to load in the json-config,
" and color the different components
" and add commands to be used on different components
"
" All functions and (global/buffer) variables should be 
" prefixed with ASCIIARCHII_


function! ASCIIARCHII_ExecuteCommandOnCoord(commandName)
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

	if has_key(b:ASCIIARCHII_sequence, "vim")
		let sequenceVimConfig = b:ASCIIARCHII_sequence["vim"]
		
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


function! ASCIIARCHII_LoadSequence(fileName)
	"Load in the sequence. It will be stored in a global variable
	"Not very nice solution, but hey...    just hey.
	
	let b:ASCIIARCHII_sequence = json_decode(join(readfile(a:fileName), "\n"))

endfunction


function! ASCIIARCHII_CreateHighlight(name, colorConfig)
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


function! ASCIIARCHII_ApplySyntaxOnCoordinates(coordinateList, highlightName)
	"coordinateList is a list of coordinate lists: [[x0, y0], [x1, y0]]
	for range in a:coordinateList 
		
		let start = "\\%" . (range[0][1] + 1) . "l" . "\\%" . (range[0][0] + 1) . "c"
		let end   = "\\%" . (range[1][1] + 1) . "l" . "\\%" . (range[1][0] + 1) . "c"

		let syntaxCommand = "syntax region " . a:highlightName . " start=\"" . start . "\" end=\"" . end . "\""
		
		"echom syntaxCommand

		execute syntaxCommand 
	endfor
endfunction


function! ASCIIARCHII_ApplyTimeLineColor(item, highlightName)
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


function! ASCIIARCHII_ApplyBorderColor(item, itemVimConfig, runningItemNum)
	"Apply any border colors if any exists
	
	if has_key(a:itemVimConfig, "style")
		let styleConfig = a:itemVimConfig["style"]

		if has_key(styleConfig, "color")
			let colorConfig = styleConfig["color"]

			if has_key(colorConfig, "border")
				let borderColorConfig = colorConfig["border"]

				let item_border_highlight_name = "ASCIIARCHII_thing_" . a:runningItemNum . "_border_color"

				call ASCIIARCHII_CreateHighlight(item_border_highlight_name, borderColorConfig)

				call ASCIIARCHII_ApplySyntaxOnCoordinates(a:item["borderCoordinateList"], item_border_highlight_name)

				if has_key(a:item, "timeLineCoordinateList")
					"Lets treat the timeLine as an extension of the border...
					"This might not be what u want though, so it should be changed later :)
					call ASCIIARCHII_ApplyTimeLineColor(a:item, item_border_highlight_name)
				endif
			endif
		endif
	endif
endfunction


function! ASCIIARCHII_ApplyLineColor(thing, vimConfig, runningNum)

	if has_key(a:vimConfig, "style")
		let styleConfig = a:vimConfig["style"]

		if has_key(styleConfig, "color")
			let colorConfig = styleConfig["color"]
			if has_key(colorConfig, "line")
				let thing_border_highlight_name = "ASCIIARCHII_thing_" . a:runningNum . "_line_color"

				let lineConfig = colorConfig["line"]

				call ASCIIARCHII_CreateHighlight(thing_border_highlight_name, lineConfig)

				call ASCIIARCHII_ApplySyntaxOnCoordinates(a:thing["lineCoordinateList"], thing_border_highlight_name)
			endif
		endif
	endif
endfunction


function! ASCIIARCHII_ApplyVariantColor(variant, runningNum)
	let runningNum = a:runningNum
	if has_key(a:variant, "vim")
		"echom Apply border to variant
		call ASCIIARCHII_ApplyBorderColor(a:variant, a:variant["vim"], runningNum)
		let runningNum = runningNum + 1
		
	endif

	for branch in a:variant["branchList"]
		for action in branch["actionList"]
			let runningNum = ASCIIARCHII_ApplyActionColor(action, runningNum)
		endfor
	endfor

	return runningNum

endfunction


function! ASCIIARCHII_ApplyActionColor(action, runningNum)
	let runningNum = a:runningNum

	if a:action["type"] == "on"
	
		if has_key(a:action, "vim")
			call ASCIIARCHII_ApplyBorderColor(a:action, a:action["vim"], runningNum)
			let runningNum = runningNum + 1
		endif

	elseif a:action["type"] == "communication"

		if has_key(a:action, "vim")
			call ASCIIARCHII_ApplyLineColor(a:action, a:action["vim"], runningNum)
			let runningNum = runningNum + 1
		endif

	elseif a:action["type"] == "variant"

		if has_key(a:action, "vim")
			let runningNum = ASCIIARCHII_ApplyVariantColor(a:action, runningNum)
		endif
	
	
	endif

	return runningNum
	
endfunction


function! ASCIIARCHII_ApplyItemColor(item, runningItemNum)

	let item = a:item

	let runningItemNum = a:runningItemNum

	if has_key(item, "vim")
		let itemVimConfig = item["vim"]	

		call ASCIIARCHII_ApplyBorderColor(item, itemVimConfig, runningItemNum)
		let runningItemNum += 1
	endif

	if a:item["type"] == "container"
		for subItem in a:item["itemList"]	
			let runningItemNum = ASCIIARCHII_ApplyItemColor(subItem, runningItemNum)
		endfor
	endif

	return runningItemNum

endfunction


function! ASCIIARCHII_ApplyColor()
	let runningNum = 0
	for item in b:ASCIIARCHII_sequence["itemList"]
		let runningNum = ASCIIARCHII_ApplyItemColor(item, runningNum)
	endfor

	for action in b:ASCIIARCHII_sequence["actionList"]
		call ASCIIARCHII_ApplyActionColor(action, runningNum)
	endfor
endfunction


function! ASCIIARCHII_ApplyStyle()
	"Yesh (sean connery yes) its pretty empty as of now since we only gots
	"the color...
	call ASCIIARCHII_ApplyColor()
endfunction


function! ASCIIARCHII_InitializeCommands()
	"Initialize commands
	"well. idea is to get all commands in sequence[vim][commands]
	"and then create a mapping for it to be used. Can it be smart? yesn't 
	
	if has_key(b:ASCIIARCHII_sequence, "vim")
		let vimConfig = b:ASCIIARCHII_sequence["vim"]

		if has_key(vimConfig, "commands")
			for cmd in keys(vimConfig["commands"])
				execute "nnoremap <buffer> <leader>" . cmd . " :call ASCIIARCHII_ExecuteCommandOnCoord(\"" . cmd . "\")<CR>"
			endfor
		endif
	endif

endfunction


"
" Functions to allow header to be shown in top-window
"

function ASCIIARCHII_debugPrint(msg)
	"Turn this to true if you want to debug the mess that is the
	"header-window... glhf bradda, u gonna need it (the luck, not the fun)
	
	if v:false
		echom a:msg
	endif
endfunction
                                                           

function! ASCIIARCHII_openHeaderWin()                                    
                                                             
    call ASCIIARCHII_debugPrint("openHeaderWin")

    if b:ASCIIARCHII_headerWindowId != 0                                  
    	call ASCIIARCHII_debugPrint("HEADER EXISTS")
    	
        if b:ASCIIARCHII_headerWindowId == win_getid()                     
    	    call ASCIIARCHII_debugPrint("WE ALREADY IN THE HEADER. no open")

            return                                              
        endif                                                      
                                                                  
        "Maybe even check that I'm in the mainWindow?              
        if b:ASCIIARCHII_mainWindowId == win_getid()
	    let pos = getcurpos()                                       
	    call win_gotoid(b:ASCIIARCHII_headerWindowId)                            
	    let pos[1] = 1 "Keep at line 1 in header, everythin' else equal
					     
	    call setpos(".", pos)         
	    call win_gotoid(b:ASCIIARCHII_mainWindowId)
	endif
       
    else
    	call ASCIIARCHII_debugPrint("WE ARE OPENING THE HEADER")

        let b:ASCIIARCHII_mainWindowId = win_getid()
        let pos = getcurpos() 
        execute ":sp"                                              
        let b:ASCIIARCHII_headerWindowId = win_getid()                           

	call ASCIIARCHII_debugPrint("ids after opening: main:" .. b:ASCIIARCHII_mainWindowId ..  " header:" .. b:ASCIIARCHII_headerWindowId)
                                                                    
        let pos[1] = 1 "Keep at line 1 in header, everythin' else equal
                                                         
        call setpos(".", pos)                             
	
        execute "resize " .. (b:ASCIIARCHII_sequence['header']['size'][1] + b:ASCIIARCHII_sequence['marginToFirstAction'])                                
	let b:ASCIIARCHII_currentWindow = 1

        call win_gotoid(b:ASCIIARCHII_mainWindowId)                     
    end                                                      
endfunction                                                   
                                                               
                                                                
function! ASCIIARCHII_closeHeaderWin()                                        
    call ASCIIARCHII_debugPrint("closeHeaderWin")

    if b:ASCIIARCHII_headerWindowId != 0                                      
        call win_execute(b:ASCIIARCHII_headerWindowId, "close")                
    endif                                                           

    let b:ASCIIARCHII_headerWindowId = 0                                         
    let b:ASCIIARCHII_mainWindowId   = 0                                         
    let b:ASCIIARCHII_currentWindow  = 0                                          
endfunction                                                            
                                                                        
                                                                         
function! ASCIIARCHII_sequenceLeave()                                                  
    "We will close all windows when we move outside of one of them into new
    "buffer. This is probably not 100% perfect, but hey, it is what it is
    
    call ASCIIARCHII_debugPrint("sequenceLeave")
    call ASCIIARCHII_debugPrint("SEQUENCE LEAVE: " .. b:ASCIIARCHII_headerWindowId .. " " .. b:ASCIIARCHII_mainWindowId .. " " .. b:ASCIIARCHII_currentWindow) 

    if b:ASCIIARCHII_headerWindowId != 0 && b:ASCIIARCHII_mainWindowId != 0
        if b:ASCIIARCHII_headerWindowId == win_getid()
	    call ASCIIARCHII_debugPrint("kill main window")

            let b:ASCIIARCHII_currentWindow = 2
	    
            call win_execute(b:ASCIIARCHII_mainWindowId, "close")
            
            let b:ASCIIARCHII_mainWindowId = win_getid()
            let b:ASCIIARCHII_headerWindowId = 0

        else
	    call ASCIIARCHII_debugPrint("kill header window")

            let b:ASCIIARCHII_currentWindow = 1

            call win_execute(b:ASCIIARCHII_headerWindowId, "close")
            let b:ASCIIARCHII_headerWindowId = 0

        endif
    endif
endfunction


function! ASCIIARCHII_sequenceSwapWindow()
    call ASCIIARCHII_debugPrint("sequenceSwapWindow")

    if b:ASCIIARCHII_headerWindowId != 0 && b:ASCIIARCHII_mainWindowId != 0
        if b:ASCIIARCHII_headerWindowId == win_getid()
	    call ASCIIARCHII_debugPrint("we in header")

            let b:ASCIIARCHII_currentWindow = 2

        elseif b:ASCIIARCHII_mainWindowId == win_getid()
	    call ASCIIARCHII_debugPrint("we in main")

            let b:ASCIIARCHII_currentWindow = 1

	else
	    call ASCIIARCHII_debugPrint("NEW WINDOW not a sequence... what to do here...")

	    if win_id2win(b:ASCIIARCHII_headerWindowId) == 0
	        "header have disapeared. must rethink life
	        call ASCIIARCHII_debugPrint("RETHINKING LIFE")

	        let b:ASCIIARCHII_headerWindowId = 0
                let b:ASCIIARCHII_currentWindow = 0
	    endif

	    if b:ASCIIARCHII_currentWindow == 1
	        call ASCIIARCHII_debugPrint("in main, closing header")

		call win_execute(b:ASCIIARCHII_headerWindowId, "close")
	        let b:ASCIIARCHII_headerWindowId = 0

	    elseif b:ASCIIARCHII_currentWindow == 2

	        call ASCIIARCHII_debugPrint("in header, closing main, switching main id")
		call win_execute(b:ASCIIARCHII_mainWindowId, "close")
                let b:ASCIIARCHII_mainWindowId = b:ASCIIARCHII_headerWindowId
	        let b:ASCIIARCHII_headerWindowId = 0
	    endif

        endif
    else

	call ASCIIARCHII_debugPrint("DO NOTHING " .. win_getid())
    endif
endfunction


function! ASCIIARCHII_sequenceEnter()
    call ASCIIARCHII_debugPrint("SEQUENCE ENTER")
    if b:ASCIIARCHII_currentWindow == 0
	"If we were here before, we came from a header-less sequence
        return
    endif
 
    if b:ASCIIARCHII_currentWindow == 1
        "we were in the main-window. so open up header
	call ASCIIARCHII_debugPrint("START IN MAIN")
        call ASCIIARCHII_openHeaderWin()
 
    else
	call ASCIIARCHII_debugPrint("START IN HEADER")
	"We were in header, so open header, and go there
        call ASCIIARCHII_openHeaderWin()
 
        call win_gotoid(b:ASCIIARCHII_headerWindowId)
    endif
endfunction
 

function! ASCIIARCHII_InitializeVimSequence(fileName)
	"Initialize the sequence by loading the json-file,
	"applying style and initializing commands.
	
	"The sequence :) A bit of a global variable catastrophe, but could be fixed
	"l8ter (l8ter equals never as they say)
	let b:ASCIIARCHII_sequence = v:null

	call ASCIIARCHII_LoadSequence(a:fileName)

	call ASCIIARCHII_ApplyStyle()

	call ASCIIARCHII_InitializeCommands()


	"To make gg go to same column at first row when jumping back and
	"forth. Its really nice. But, even nicer is the open-header
	"functionality I'm about to lay down in this ucka' (it is layed down,
	"with varying amounts of success...)
	setlocal nostartofline

	"Ok, the header-window thing is a bit shaky... it sort of works, but
	"in some cases it might spaz out :(
	let b:ASCIIARCHII_mainWindowId      = 0                                      
	let b:ASCIIARCHII_headerWindowId    = 0                                       
									   
	"To know where to go when we go into the buffer yet again :) lets go
	let b:ASCIIARCHII_currentWindow = 0                                   

	augroup ASCIIARCHII_sequence_au
	    au!
	    autocmd BufLeave <buffer> call ASCIIARCHII_sequenceLeave()
	    autocmd BufEnter <buffer> call ASCIIARCHII_sequenceEnter()
	    autocmd WinEnter <buffer> call ASCIIARCHII_sequenceSwapWindow()
	augroup END

	"TODO: these commands might interfere with user-defined commands...
	"Must check if that is true and take action accordingly...
	nnoremap <buffer> <leader>oh :call ASCIIARCHII_openHeaderWin()<CR>
	nnoremap <buffer> <leader>ch :call ASCIIARCHII_closeHeaderWin()<CR>
endfunction


