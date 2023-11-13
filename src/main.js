
var VERSION = '2.0.2';
var EDITOR_VERSION = app.getVersion();
var IS_WIN = false;

var TRIGGERS = {
  2: '?txs-start',
  64: '?save-file',
};


function initialize() {
  debug('Initializing WakaTime v' + VERSION + '...');
  var proc = system('ver');
  proc.waitForFinished();
  if (proc.exitCode === 0) IS_WIN = true;
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

  var cli = '$HOME/.wakatime/wakatime-cli';
  if (IS_WIN) cli = '%USERPROFILE%/.wakatime/wakatime-cli.exe';

  var args = [
    cli,
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
