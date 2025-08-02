from flask import Flask,send_file,request,redirect,make_response,url_for,render_template
from pytubefix import YouTube
from uuid import uuid4
import os
import json
import subprocess
import time
from math import inf
import random
from pytubefix import YouTube
import smtplib
from email.mime.text import MIMEText
from waitress import serve
users = {}
from sys import platform

app=Flask(__name__)

class response():
   
  ERRORCODE = {
    0: 'login error',
    'login error': 0,
    1: 'URL not available',
    'URL not available': 1,
    2: 'already registered',
    'already registered': 2,
    3: 'verify error',
    'verify error': 3,
    200:'scuess',
    'scuess':200,
    'i dont know why but it broken ':80803,
    80803:'i dont know why but it broken ',
    56:'registeryet',
    'registeryet':56,
    97:'you forgot input url!',
    'you forgot input url!':97,
    98:'system limit!!!! cant be register',
    'system limit!!!! cant be register':98

}
  LOGINERROR=0
  URLNOTAVALIBLE=1
  REGISTERALREADY=2
  VERITYERROR=3
  SCUCESS=200
  WHYERRPR=80803
  REGISTERALYET=56
  ACQUIREURL=97
  SYSTEMLIMIT=98
def send_mail(target_mail,message,your_mail = 'pupss85319@gmail.com',your_password = 'upgm jfia zykj xonb',):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(your_mail,your_password)
    from_addr = your_mail
    to_addr = target_mail
    msg = MIMEText(message, 'plain', 'utf-8')  
    msg['Subject'] = 'YouTube downloader Gary great app'
    msg['From'] = from_addr
    msg['To'] = to_addr

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(your_mail, your_password)
    status = smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.quit()
def saveUser(users):
    with open("users.json","w") as file:
        json.dump(users,file)
def loadUser():

    global users 
    with open("users.json","r") as file:
        users=json.load(file)
def islogin(id):

    return   id and id in users.keys()
def uuid4():
    txt=''
    for n in range(6):
        txt+=chr(random.randint(97,122))
    return txt
def getid():
    loadUser()
    id=request.args.get('uuid')
    if not id:
        id=request.cookies.get('id')
    return id
def fake_d(url: str, output_path: str = ".", file_name: str = "."):
    
    if url=='1':
        2/0
    with open(file_name,'wb') as f:
        f.write(bytes(0))
    return '22'
def handle_robot(normalresbonse,code:int):
    global users
    saveUser(users)
    if code:
      if request.args.get('isrobot'):
        return str(code)
      

    if normalresbonse:
        if  request.args.get('isrobot'):
            return response.SCUCESS
    return normalresbonse
def download_video_youtube(url: str, output_path: str = ".", file_name: str = ".") -> str:
    """
    Parámetros:
    - url: str -> Enlace completo al Short (por ejemplo, https://www.youtube.com/shorts/1Fxq3DIUPuk)
    - output_path: str -> Carpeta de destino (por defecto, directorio actual)

    Retorna:
    - str: url of file downloaded.
    """
    
    yt = YouTube(url, use_po_token=True, po_token_verifier=po_token_verifier)

    video = yt.streams.get_highest_resolution()
    video.download(filename=file_name)
    
    return yt.title
if 'win' in  platform:
    print('win env , use fake download')
    download_video_youtube=fake_d
def po_token_verifier():
    token_object = generate_youtube_token()
    return token_object["visitorData"], token_object["poToken"]
def generate_youtube_token() -> dict:
    result = cmd("npx youtube-po-token-generator")
    data = json.loads(result.stdout)
    return data
def cmd(command, check=True, shell=True, capture_output=True, text=True):


    """
    Runs a command in a shell, and throws an exception if the return code is non-zero.
    :param command: any shell command.
    :return:
    """
    try:
        return subprocess.run(command, check=check, shell=shell, capture_output=capture_output, text=text)
    except subprocess.CalledProcessError as error:
        return ('0','0')   
if os.path.isfile('users.json'):
    loadUser()
@app.route("/")
def homepage():
    html=''
    if not islogin(getid()):
        return handle_robot(redirect('/login'),code=response.VERITYERROR)
    html+=f'<h1><b>{users[getid()]["name"]}</b>您好!</h1><br>'
    html+='<h1><a href="/download">點我下載</a></h1><br><h1><a href="/play">點我觀看</a></h1><br><h1><a href="/game">點我玩遊戲</a></h1><br><h1><a href="/logout">登出</a></h1>'
    return handle_robot(html,response.SCUCESS)
curent_title={}
@app.route('/download')
def download():
    if not islogin(getid()):
        return handle_robot(redirect('/login'),code=response.VERITYERROR)
    try:
        os.remove("a.mp4")
    except:
        pass

    url=request.args.get('url')
    if url is None:
        return handle_robot('''
                <h1>輸入影片網址</h1>
<form actoin="/download" method="get">
<input name="url" width="5000" aria-grabbed="true" type="text" size="80%" title="影片網址">
<input name="summit" type="submit" >
<a href="/">回首頁</a>
</form>''',code=response.SCUCESS)
    try:
      print('下載開始')
      title=download_video_youtube(url,file_name=f'{getid()}.mp4')
      #title=fake_d(url,file_name=f'{getid()}.mp4')
      curent_title[getid()]=title
          #download
      return handle_robot(f'伺服器成功取得影片!您的下載網址:<a href="/getvideo/{getid()}.mp4">{url_for("getvideo", name=f"{getid()}.mp4")}<br><a href="/download">回下載</a>',code=f'200:/getvideo/{getid()}.mp4')
    except:
        return handle_robot('影片無效',code=response.URLNOTAVALIBLE)
@app.route('/play')
def play():
    if not islogin(getid()):
        return redirect('/login')
    try:
        os.remove("a.mp4")
    except:
        pass

    url=request.args.get('url')
    if url is None:
        return'''
                <h1>輸入影片網址</h1>
<form actoin="/download" method="get">
<input name="url" width="5000" aria-grabbed="true" type="text" size="80%" title="影片網址">
<input name="summit" type="submit" >
<a href="/">回首頁</a>
</form>'''
    title=download_video_youtube(url)
        #download
    return send_file("a.mp4")
@app.route("/register")
def register():
    global users
    try:
        loadUser()
    except:
        pass
    if len(users.keys())<=50:
        name=request.args.get('name')
        email=request.args.get('mail')
        isrobot=request.args.get('isrobot')
        if not name :
            return handle_robot('''<form actoin="/register" method="get">
    <h1>輸入您的名稱</h1>
    <input name="name" width="5000" aria-grabbed="true" type="text" size="80%" title="id">
    <h1>輸入您的email</h1>
    <input name="mail" width="5000" aria-grabbed="true" type="mail" size="80%" title="id">
    <input name="summit" type="submit" >
    </form><br>''',code=response.SCUCESS)
        try:
            a=str(uuid4())
        except:
            a='1'
        iiiiiii=0
        for n in users.values():

            if email==n['email']:
                iiiiiii+=1               
                continue 
        
        if iiiiiii>0 :
          return handle_robot('<h1>already register <a href="/login">登入</a></h1>' ,code=response.REGISTERALREADY )
        users[a]={'name':name,'email':email,'id':a}
        saveUser(users)
        if not isrobot:
            send_mail(email,"your id is:  {}".format(a))
            return handle_robot(f'hello{name}!!  your id have be send <a href="/">首頁</a>',code=a)
        else:
            return a
    else:
        return handle_robot("人數已到達限制",code=response.SYSTEMLIMIT)
@app.route("/login")
def login():
    id = request.args.get('uuid')
    
    if not islogin(id):
        
        return handle_robot( '''
    <h1>輸入id</h1>
    <form actoin="/login" method="get">
    <input name="uuid" width="5000" aria-grabbed="true" type="text" size="80%" title="id">
    <input name="summit" type="submit" >
    </form><br>
    <h1><a href="/register">點此註冊</a></h1>
    <h1><a href="/game">點此玩遊戲</a></h1>
    <h1><a href="/findcode">忘記id?</a></h1>

    ''',code=response.VERITYERROR)
    if request.cookies.get('id') in users:
        return '您已登入!!<a href="/">首頁</a>在這<br><a href="/logout">登出</a>'
    re=make_response(redirect("/"))
    re.set_cookie('id',id,expires=time.time()+60*60*24*30*12*100)
    return re
@app.route('/logout')
def lg():
    id=request.cookies.get('id')
    if not id:
        return redirect('/login')
    re=make_response(f'{users[id]["name"]} 再見囉!<br><a href="/">回首頁</a>')
    re.set_cookie('id','',expires=0)
    return re
@app.route('/getvideo/<name>')
def getvideo(name):
    if not islogin(getid()):
        return handle_robot(redirect('/login'),code=response.VERITYERROR)
    return send_file(name,as_attachment=True,download_name=f'{curent_title[getid()]}.mp4')
@app.route('/findcode',methods=['GET','POST'])
def findcode():
    email=request.values.get('email')
    if not email:
        return '''<h1>輸入email</h1>
    <form actoin="/findcode" method="post">
    <input name="email" width="5000" aria-grabbed="true" type="text" size="80%" title="id">
    <input name="summit" type="submit" >
    </form><br>
    <h1><a href="/register">type to register </a></h1>
    '''
    i=0
    
    for n in users.values():

        if email!=n['email']:
            i+=1
            continue
    if i==len(users.values()):
        
        return handle_robot('<h1>you have not  register yet <a href="/register">type to register</a></h1>' ,code=response.REGISTERALYET)
    
    for n in users:
        if email==users[n]['email']:
            code=n
            
    print(f'your code is : {code} dont forgot it ')
    send_mail(email,'your code is : {} dont forgot it '.format(code))
    return "already send"
@app.route("/game")
def game():

    return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.3/p5.js"></script>
    <meta charset="utf-8" />

  </head>
  <body>
    <main>
    </main>
    <script>const COLS = 10;
const ROWS = 25;
const BLOCK_SIZE = 30;
const WIDTH = COLS * BLOCK_SIZE;
const HEIGHT = ROWS * BLOCK_SIZE;
let board;
let currentPiece;
let pieces = [
  { shape: [[1, 1, 1, 1]], color: '#8CDFD6' }, // I
  { shape: [[1, 1], [1, 1]], color: '#FFD23F' }, // O
  { shape: [[1, 1, 0], [0, 1, 1]], color: '#9BC1BC' }, // Z
  { shape: [[0, 1, 1], [1, 1, 0]], color: '#B8B8FF' }, // S
  { shape: [[1, 1, 1], [0, 1, 0]], color: '#EFBDEB' }, // T
  { shape: [[1, 1, 1], [1, 0, 0]], color: '#467599' }, // L
  { shape: [[1, 1, 1], [0, 0, 1]], color: '#BCEDF6' }  // J
];
let dropCounter = 0;
let dropInterval = 500; // 減少方塊下降的間隔時間
let levelUpThreshold = 10; 
let clearedRows = 0;
let score = 0;


function setup() {
  createCanvas(WIDTH,HEIGHT);
  frameRate(60); // 提高每秒幀數
  board = createEmptyBoard();
  currentPiece = createPiece();

}

function draw() {
  background(0);
  drawBoard();
  drawPiece(currentPiece);
  drawScore();

  dropCounter += deltaTime;
  if (dropCounter > dropInterval) {
    if (!movePiece(currentPiece, 0, 1)) {
      placePiece(currentPiece);
      currentPiece = createPiece();
      if (!isValidPosition(currentPiece, currentPiece.x, currentPiece.y)) {
        noLoop(); 
        textSize(32);
        fill(255, 0, 0);
        text('Game Over', WIDTH / 4, HEIGHT / 2);
      }
    }
    dropCounter = 0;
  }

  clearFullRows();
  fill(255,100,100,100)
  rectMode(CENTER)
  square(width/2,height/2,100);
  rectMode(CORNER);
  fill(0);
  text("rotate",width/2-20,height/2,);
}

function createEmptyBoard() {
  let board = [];
  for (let r = 0; r < ROWS; r++) {
    board[r] = [];
    for (let c = 0; c < COLS; c++) {
      board[r][c] = 0;
    }
  }
  return board;
}

function createPiece() {
  let piece = random(pieces);
  return {
    shape: piece.shape,
    color: piece.color,
    x: Math.floor(COLS / 2) - Math.floor(piece.shape[0].length / 2),
    y: 0
  };
}
function mousePressed() {
  if (isMouseOnPiece(currentPiece)) {
    rotatePiece(currentPiece);
  } else {
    if (mouseX>width/2-50 && mouseX<width/2+50){
      if (mouseY>height/2-50&&mouseY<height/2+50){
        
        rotatePiece(currentPiece);
      }
    }
    if (mouseX < WIDTH / 2) {
      movePiece(currentPiece, -1, 0);
    } else if (mouseX > WIDTH / 2) {
      movePiece(currentPiece, 1, 0);
//=====================================================
    }
//===================================================
  }
}

function isMouseOnPiece(piece) {
  for (let r = 0; r < piece.shape.length; r++) {
    for (let c = 0; c < piece.shape[r].length; c++) {
      if (piece.shape[r][c]) {
        let blockX = (piece.x + c) * BLOCK_SIZE;
        let blockY = (piece.y + r) * BLOCK_SIZE;
        if (mouseX >= blockX && mouseX < blockX + BLOCK_SIZE && mouseY >= blockY && mouseY < blockY + BLOCK_SIZE) {
          return true;
        }
      }
    }
  }
  return false;
}

function drawBoard() {
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      fill(230);
      stroke(200, 200, 200, 100); 
      rect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
      
      if (board[r][c]) {
        fill(board[r][c]);
        rect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
      }
    }
  }
}

function drawPiece(piece) {
  fill(piece.color);
  for (let r = 0; r < piece.shape.length; r++) {
    for (let c = 0; c < piece.shape[r].length; c++) {
      if (piece.shape[r][c]) {
        rect((piece.x + c) * BLOCK_SIZE, (piece.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
      }
    }
  }
}

function drawScore() {
  textSize(16);
  fill(0);
  text('Score: ' + score, 10, 20);
}

function isValidPosition(piece, x, y) {
  for (let r = 0; r < piece.shape.length; r++) {
    for (let c = 0; c < piece.shape[r].length; c++) {
      if (piece.shape[r][c]) {
        let newX = x + c;
        let newY = y + r;
        if (newX < 0 || newX >= COLS || newY < 0 || newY >= ROWS || board[newY][newX]) {
          return false;
        }
      }
    }
  }
  return true;
}

function movePiece(piece, dx, dy) {
  if (isValidPosition(piece, piece.x + dx, piece.y + dy)) {
    piece.x += dx;
    piece.y += dy;
    return true;
  }
  return false;
}

function placePiece(piece) {
  for (let r = 0; r < piece.shape.length; r++) {
    for (let c = 0; c < piece.shape[r].length; c++) {
      if (piece.shape[r][c]) {
        board[piece.y + r][piece.x + c] = piece.color;
      }
    }
  }
}

function clearFullRows() {
  let rowsCleared = 0;  
  for (let r = ROWS - 1; r >= 0; r--) {
    let isFull = true;
    for (let c = 0; c < COLS; c++) {
      if (!board[r][c]) {
        isFull = false;
        break;
      }
    }
    if (isFull) {
      board.splice(r, 1);
      board.unshift(new Array(COLS).fill(0));
      r++;
      clearedRows++;
      rowsCleared++;

      if (clearedRows % levelUpThreshold === 0) {
        dropInterval = max(dropInterval * 0.9, 100);
      }
    }
  }

  if (rowsCleared > 0) {
    score += 10 * (Math.pow(2, rowsCleared - 1));
  }
}

function keyPressed() {
  if (keyCode === LEFT_ARROW) {
    movePiece(currentPiece, -1, 0);
  } else if (keyCode === RIGHT_ARROW) {
    movePiece(currentPiece, 1, 0);
  } else if (keyCode === DOWN_ARROW) {
    movePiece(currentPiece, 0, 1);
  } else if (keyCode === UP_ARROW) {
    rotatePiece(currentPiece);
  }
}

function rotatePiece(piece) {
  let newShape = [];
  for (let c = 0; c < piece.shape[0].length; c++) {
    newShape[c] = [];
    for (let r = piece.shape.length - 1; r >= 0; r--) {
      newShape[c][piece.shape.length - 1 - r] = piece.shape[r][c];
    }
  }
  let originalShape = piece.shape;
  piece.shape = newShape;
  if (!isValidPosition(piece, piece.x, piece.y)) {
    piece.shape = originalShape; 
  }
}
</script>
<audio id="background-music" loop>
  <source src="music.mp3" type="audio/mpeg">
</audio>
  </body>
<button onclick="document.getElementById('background-music').play()">播放音樂</button>
</html>
'''
@app.route("/music.mp3")
def music():
    return send_file("music.mp3")

@app.route('/codedict')
def cd():
    return json.dumps(response.ERRORCODE)

if __name__ == "__main__":
    
    app.run("0.0.0.0", 2388, debug=True)
        #serve(app, host='0.0.0.0', port=2388) 
    

    

