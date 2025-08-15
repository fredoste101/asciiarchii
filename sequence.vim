"Well then... How the f am I gonna do this then...


let currentFileName = @%


let currentFileNameNoExtension = split(currentFileName, '\.')[0]

let jsonFileName = currentFileNameNoExtension . ".json"



let g:sequence = json_decode(join(readfile(jsonFileName), "\n"))


"echo sequence




function SequenceJump()

	let pos = getcurpos()

	"We use 0-counted shit in the sequence
	let x = pos[2] - 1
	let y = pos[1] - 1


	"echo g:sequence["cmdList"]

	for cmd in g:sequence["cmdList"]
		
		if y >= cmd["startCoord"][1] && y <= cmd["endCoord"][1]
			if x >= cmd["startCoord"][0] && x <= cmd["endCoord"][0]
				execute(cmd["cmd"])
				return
			endif
		endif

	endfor

	echo "x: " . string(x) . " " . "y: " . string(y)

endfunction



:nnoremap <buffer> <leader>gd :call SequenceJump()<CR>
