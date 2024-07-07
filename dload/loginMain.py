#!/usr/bin/python3

import os,io,sys
import cgi,cgitb
from http import cookies
 
import loginDb
import loginCook
from  mydbg import *

cgitb.enable()            #ブラウザにエラーを表示する


# --------------------
#    セッションID生成
# --------------------
# import datetime,random,hashlib
import uuid
def getSid():

  # toke= "AadDTq:%$A"
  # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
  # rnd = random.randint(0,900000)
  # key = (toke + now + str(rnd)).encode("utf-8")
  # sid = hashlib.sha256(key).hexdigest()
 
  
  return str(uuid.uuid4())

 
html="""
<head>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>
<body>
    <h2>ログイン</h2>

    <form method="post">
      <p>メール：　　　<input type="text"    name="uid"></p>
      <p>パスワード：　<input type="text"    name="pwd"></p>

      <br>
      <p>
      <input type="submit" value="ID作成" name="btn">
      <input type="submit" value="login"  name="btn">
      <input type="submit" value="logout"  name="btn">
      <input type="submit" value="topPage" name="btn">
      </p>
    </form>
</body>
"""


try:
    if ( os.environ['REQUEST_METHOD'] == "GET" ):

      form = cgi.FieldStorage()
      lout     = form.getfirst( 'logout' )
      if lout=="True":
        HttpHead  = "Content-Type: text/html; charset=utf-8"
        print( HttpHead )
        print()
        print("logout処理はしていません…")
      else:
        # ログインフォームの表示
        print("Content-Type: text/html; charset=utf-8\n")
        print(html)
    
    else:
      # フォームからEmail(ユーザーID)とそのパスワードを取得する
      form = cgi.FieldStorage()
      btn     = form.getfirst( 'btn' )
      uid     = form.getfirst( 'uid' )
      pwd     = form.getfirst( 'pwd' )

      # DB操作クラスのインスタンス生成
      db = loginDb.dbase()

      # HTTP応答ヘッダー フィールド
      HttpHead  = "Content-Type: text/html; charset=utf-8"
      # HTTP応答本文
      msg       = ""
      # クッキー文字列の変数
      cookStr = ""
      
      if btn == "login":

        st1 = db.chkReg( uid, pwd )
        if st1 == "NG":
          msg = "ID,PWDが違います！"

        elif st1 == "OK":

          uid2, sid2 = loginCook.getCook()
          st2 = db.chkLogin( uid2, sid2 )

          if st2 == "OK":
            msg = "すでにloginしています"

          elif st2 == "NG":
            # セッションIDを生成
            sid = getSid()
            # ログイン情報テーブルにセッションIDを登録
            st3 = db.login( uid, sid )
            if st3 == "OK":
              # ユーザID,セッションIDのクッキー文字列を取得
              cookStr = loginCook.cookString( uid, sid )
              msg = "loginしました！"
            else:
              msg = st3
          else:
            msg = st2
        else:
          msg = st1


      elif btn == "logout":

          uid, sid = loginCook.getCook()
          st = db.chkLogin( uid, sid )
          if st == "NG":
            msg = "すでにlogoutしています"
          else:
            # 情報テーブルのセッションIDをクリア
            db.login( uid, '' )
            # クッキークリアの為にクッキー文字列を取得
            cookStr =loginCook.delCookString()
            msg = "logoutしました！"

      elif btn == "topPage":
      
          uid, sid = loginCook.getCook()
          st = db.chkLogin( uid, sid )

          msg = "<h1>何でもサイト</h1>"
          msg += "<a href=/cgi/books/loginMain.py?form>Form</a> "
          msg += "<a href=/cgi/books/loginMain.py?logout=True>logout</a><br><br>"
          if st == "OK":
            msg += uid + "さんは<br>"
            msg += "loginしています、ありがとう！"
          elif st == "NG":
            msg += "loginしていません"
          else:
            msg = st

      elif btn == "ID作成":

          if uid == None or pwd == None:
            msg = "ID,PWDを入力して下さい"
          else:

            st = db.reg( uid, pwd )
            dbg("stat", st)
            
            if st == "OK":
                msg = "ID作成OK"
            elif st == "NG":
                msg = "登録されています<br>"

            else:
                msg = st
            
      else:
          msg = "ボタン定義のエラー"

      # HTTPプロトコル応答ヘッダー出力
      print( HttpHead )

      if cookStr != "":
        print( cookStr )

      # ヘッダーフィールドと本文を区切る
      print()         
      print( msg )
      
except:
    # ここの「except」でこのようにエラー処理をすると
    # Webサーバのエラーログとブラウザの両方にエラー出力
    print("Content-Type: text/html; charset=utf-8\n")
    
    import traceback
    # Webサーバのエラーログに反映される
    traceback.print_exc()

    s = traceback.format_exc()
    s = s.replace("  ","　")  # 改行なし空白
    # s = s.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;")  # tab
    # s = s.replace("\"","&quot;") # 引用符
    s = s.replace("&","&amp;")   # アンパサンド
    s = s.replace("<","&lt;")    # 小なり記号
    s = s.replace(">","&gt;")    # 大なり記号
    s = s.replace("\n","<br>")  # 改行コード
    # ブラウザにエラーが出力される
    print(s)
    
    sys.exit()

