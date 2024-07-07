#!/usr/bin/python3

import os,io,sys
import datetime
import cgi,cgitb

from http import cookies
from  mydbg import *

cgitb.enable()            #ブラウザにエラーを表示する


# -------------------------------
#     クッキー操作のモジュール
# -------------------------------
'''''''''''''''''''''''''''''''''''''''''''''
関数名
  クッキー情報の取得
  getCook()

引数
  なし
返却値
  タプル ユーザID、セッションID
  
機能
  ユーザIDとセッションIDを返却する関数
  クッキー情報がない場合は、空文字列が返る

処理
  ・環境変数「HTTP_COOKIE」から全てのクッキー情報を取得
  ・http.cookiesモジュールのSimpleCookieのインスタンスの取得
  ・valueオブジェクトで以下のクッキーの値を取得
    ユーザID,セッションID
 
'''''''''''''''''''''''''''''''''''''''''''''
def getCook():

  uid, sid = "", ""

  allCook = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

  #セッションIDのクッキーがあるかチェック
  if "UID" in allCook:
    uid = allCook["UID"].value

  if "SID" in allCook:
    sid = allCook["SID"].value
    
  return uid, sid



'''''''''''''''''''''''''''''''''''''''''''''
関数名
  クッキー登録の文字列取得
  cookString()

引数
  uid   ユーザID
  sid   セッションID
  mAge  有効秒数
返却値
  クッキー登録の文字列
  
機能
  引き渡されたユーザID,セッションID、有効秒数を元に
  クッキー登録の為の文字列を作成する

処理
  ・http.cookiesモジュールのSimpleCookieのインスタンスの取得
  ・引数のユーザID、セッションIDを設定
  ・引数の有効期限（max-age）を設定
  ・クッキー登録の文字列を取得
 
'''''''''''''''''''''''''''''''''''''''''''''
def cookString( uid,sid, mAge=60):
    
  cookStr = cookies.SimpleCookie()

  cookStr["UID"] = uid
  cookStr["SID"] = sid
  cookStr["UID"]["max-age"] = mAge  # second
  cookStr["SID"]["max-age"] = mAge  # second

  # expires = datetime.datetime.now() + datetime.timedelta( minutes= 1 )
  # ["SID"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
  # cookStr["SID"]["HttpOnly"] = True
  # cookStr["SID"]["Secure"] = True
  return cookStr.output()



'''''''''''''''''''''''''''''''''''''''''''''
関数名
  クッキー削除の文字列取得
  delCookString()

引数
  なし
返却値
  クッキー削除の文字列
  
機能
  クッキー削除の文字列取得

処理
  ・有効期限（max-age）を０秒にする
  ・クッキー登録の文字列取得の関数を呼出す
 
'''''''''''''''''''''''''''''''''''''''''''''
def delCookString():

  return cookString( "", "", 0 )

 
 
 
'''
--------------------------------------------------------
テスト方法について
ネットブラウザでURLを指定してテストする

「except」でこのようにエラー処理をすると
Webサーバのエラーログとブラウザの両方にエラー出力ができる

例）

設定用クッキー文字列の取得
  http://....sakura.ne.jp/cgi/books/loginCook.py?test=set

取得
  http://....sakura.ne.jp/cgi/books/loginCook.py?test=get

削除  
  http://....sakura.ne.jp/cgi/books/loginCook.py?test=del
  
--------------------------------------------------------
'''      
def main():
  

  try:
      form = cgi.FieldStorage()
      testNo  = form.getfirst( 'test')

      HttpHead  = "Content-Type: text/html; charset=utf-8"
      cookStr     = ""
      
      if testNo == "set":
          cookStr = cookString( "email", "sessionid-12345", 60 )

          dbg( "HttpHead", HttpHead)
          dbg( "cookStr", cookStr)

          # HTTPプロトコル応答ヘッダー出力
          print( HttpHead )
          if cookStr != "":
            print( cookStr )
          # ヘッダーフィールドと本文を区切る
          print()         
          print("cookString 成功<br>")

      if testNo == "get":
          uid, sid = getCook()

          print( HttpHead )

          # ヘッダーフィールドと本文を区切る
          print()         
          print( "getCook 成功<br>")
          print( "uid=(", uid, ")<br>")
          print( "sid=(", sid, ")<br>")
          
          if uid == "":
            print("UID 無し<br>")
          if sid == "":
            print("SID 無し<br>")

      if testNo == "del":
          cookStr =delCookString()

          # HTTPプロトコル応答ヘッダー出力
          print( HttpHead )
          if cookStr != "":
            print( cookStr )
            
          # ヘッダーフィールドと本文を区切る
          print()         
          print("delCookString 成功<br>")
            

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


        
if __name__ == "__main__":
    main()


