from flask import Flask, render_template_string

app = Flask(__name__)

LEVELS = {
    1: list('qwertyuiop'),
    2: list('asdfghjkl;'),
    3: list('qwertyuiopasdfghjkl;'),
    4: list('zxcvbnm,./'),
    5: list('qwertyuiopasdfghjkl;zxcvbnm,./'),
    6: list('1234567890'),
    7: list('qwertyuiopasdfghjkl;zxcvbnm,./1234567890'),
}

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Typing Speed Game</title>
<style>
body{font-family:Arial;text-align:center;background:#f0f0f0;margin:0;padding:20px;}
#word{font-size:2em;margin:20px;color:#333;}
input{font-size:1.2em;padding:12px;width:60%;}
button{padding:10px 20px;font-size:1em;}
#result{margin-top:20px;font-size:1.2em;}

body {
    font-family: Arial, sans-serif;
    background: #111;
    color: #eee;
    text-align: center;
    margin: 0;
    transition: background 0.3s, color 0.3s;
}

body.light-mode {
    background: #fff;
    color: #111;
}

input[type=text], button {
    transition: background 0.3s, color 0.3s;
}

body.light-mode input[type=text], body.light-mode button {
    background: #eee;
    color: #111;
}

input[type=text], button {
    background: #222;
    color: #eee;
    border: none;
    border-radius: 3px;
}


.level-button, select {
    transition: background 0.3s, color 0.3s;
    background-color: #222;
    color: #eee;
    border: none;
    border-radius: 100px;
}

body.light-mode .level-button, 
body.light-mode select {
    background-color: #eee;
    color: #111;
}



#target-area span {
    color: #fff; /* Light color for visibility in dark mode */
    background-color: transparent; /* Optional: transparent background for clarity */
    border-radius: 4px; /* Optional: rounded edges for better appearance */
}
body.light-mode #target-area span {
    color: #111; /* Darker color for light mode */
}

</style>
</head>
<body>
<h1>Typing Speed Game</h1>

<button id="darkModeToggle" onclick="toggleDarkMode()">☾☼ Dark Mode</button>

<p>Select Level: <select id="levelSelect"></select> 
<button onclick="startGame()">Start</button></p>
<div id="game" style="display:none;">
  <div id="word"></div>
  <input type="text" id="inputBox" oninput="checkInput()">
  <div id="result"></div>
</div>
<script>
const levels = {{ levels | safe }};
let currentWord = '', startTime, correct = 0, total = 0, levelKeys = [];

window.onload = () => {
  let sel = document.getElementById('levelSelect');
  Object.keys(levels).forEach(l => {
    let opt = document.createElement('option');
    opt.value = l; opt.text = 'Level ' + l;
    sel.appendChild(opt);
  });
}

function toggleDarkMode() {
    document.body.classList.toggle('light-mode');
}



function startGame(){
  const lvl = document.getElementById('levelSelect').value;
  levelKeys = levels[lvl];
  document.getElementById('game').style.display='block';
  document.getElementById('result').textContent='';
  correct = total = 0;
  newWord();
  startTime = new Date().getTime();
}

function newWord(){
  let len = Math.floor(Math.random()*5)+3;
  currentWord = Array.from({length: len}, ()=> levelKeys[Math.floor(Math.random()*levelKeys.length)]).join('');
  document.getElementById('word').textContent = currentWord;
  document.getElementById('inputBox').value='';
}

function checkInput(){
  let userInput = document.getElementById('inputBox').value;
  if(userInput === currentWord){
    correct++; total++;
    newWord();
  } else if(userInput.length >= currentWord.length){
    total++;
    newWord();
  }
  let elapsed = (new Date().getTime() - startTime)/1000;
  let wpm = ((correct/elapsed)*60).toFixed(1);
  document.getElementById('result').textContent = `Correct: ${correct} | Speed: ${wpm} WPM`;
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML, levels=LEVELS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
