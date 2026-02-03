

THIS_CMD=${BASH_SOURCE[0]}
THIS_DIR=$(dirname $THIS_CMD)

./aa --file $THIS_DIR/test/files/vim/demo0.yaml --sequenceOut demoOut.aa --jsonOut demoOut.json

if [[ $? == 0 ]]; then
	vim -c "source sequence.vim" -c "call ASCIIARCHII_InitializeVimSequence('demoOut.json')" demoOut.aa
fi
