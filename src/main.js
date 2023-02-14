
var VERSION = '2.0.0';
var EDITOR_VERSION = app.getVersion();

var TRIGGERS = {
  2: '?txs-start',
  64: '?save-file',
};


function initialize() {
  debug('Initializing WakaTime v' + VERSION + '...');
}

function onSave() {
  var currentFile = app.getCurrentFileName();
  if (currentFile) {
    currentFile = app.getAbsoluteFilePath(currentFile);
    sendHeartbeat(currentFile, true);
  }
}

function sendHeartbeat(file, isWrite) {
  debug('Sending heartbeat for file:' + file);

  file = utils.urlToPath(file);

  var args = [
    '$HOME/.wakatime/wakatime-cli',
    '--entity',
    '"' + file + '"',
    '--plugin',
    '"texstudio/' + EDITOR_VERSION + ' texstudio-wakatime/' + VERSION + '"',
  ];
  if (isWrite)
    args.push('--write');
  if (typeof cursor !== 'undefined') {
    args.push('--lineno');
    args.push(cursor.lineNumber() + 1);
    var cursorpos = cursorPosition();
    if (cursorpos != null) {
      args.push('--cursorpos');
      args.push(cursorpos);
    }
  }

  // run wakatime-cli in separate process
  system(args.join(' '));
}

function cursorPosition() {
  if (typeof editor === 'undefined') {
    return null;
  }

  var lines = editor.document().textLines();
  var cursorpos = 0;
  var lineno = cursor.lineNumber();
  var currentLine = 0;
  while (currentLine <= lineno) {
    if (currentLine == lineno) {
      cursorpos += cursor.columnNumber();
    } else {
      cursorpos += lines[currentLine].length + 1;
    }
    currentLine += 1;
  }
  return cursorpos;
}

var trigger = TRIGGERS[triggerId];
switch (trigger) {
  case '?txs-start':
    initialize();
    break;
  case '?save-file':
    onSave();
    break;
}
