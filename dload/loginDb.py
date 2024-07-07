#!/usr/bin/python3

import mysql.connector
import datetime,random,hashlib

from mydbg import *
# from  mydbg import *
# dbg("loginDbモジュール1", __name__)


# st=156
# st2=[1,2,3,]
# dbg( st=st, key2=st2)
# dbg("test",1,2,st2,st)
# -------------------
#     DBアクセスのクラス
# -------------------
class dbase:

    # コンストラクタ
    def __init__(self):

        # 接続
        self.con = mysql.connector.connect(
            database  ='testdb',
            user      ='koba',
            password  ='test01'
        )

        self.con.autocommit = False

    # デストラクタ
    def __del__(self):
        # print("<br>インスタンス破棄OK(db close)<br>")
        self.con.close()
        
     
    # ログイン情報テーブルの作成
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
    def create(self):

        try:
            tableName = 'loginInf'
            
            sql = '''
                CREATE TABLE %s (

                  uid VARCHAR(50),
                  pwd   VARCHAR(10),
                  sid   VARCHAR(100)
                 
                )''' %( tableName )

            cursor = self.con.cursor ()
            cursor.execute( "drop table if exists %s" %tableName )
            
            cursor.execute(sql)
            self.con.commit()
            print( "テーブル作成OK")

        except mysql.connector.Error as e:
            self.con.rollback()
            print( "MySql error:", e.args)

        finally:
            cursor.close()


        
    '''''''''''''''''''''''''''''''''''''''''''''
    メッソ名
        ログイン情報テーブルにユーザIDとセッションIDを登録

      引数
        reg( self, uid, pwd ):
        uid   ユーザID
        pwd   パスワード

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
    def reg( self, uid, pwd ):

        try:
          msg =""
          cursor = self.con.cursor ( prepared=True)

          # 「select ～　for update」を使って排他ロックする
          # 誰かが先に使われた場合は、待ち状態になる、
          # 待ち状態が続く場合はタイムアウトのエラーになります
          sql = "select *  from loginInf where uid =?  for update"
          cursor.execute (sql, (uid,))

          row = cursor.fetchone()
          if row == None:

            sql = "insert into loginInf ( uid, pwd, sid ) values (?, ?, '' )"
            cursor.execute(sql, (uid,pwd))

            self.con.commit()
            msg = "OK"

          else:
            self.con.rollback()
            msg = "NG"
            
        except mysql.connector.Error as e:
            self.con.rollback()
            msg = "MySql error:" + str( e.args )


        finally:
            cursor.close()
            return msg




    # 登録済みかをチェックする、IDとパスワードがテーブルにあるか
    # return、Noneなら未登録か間違い
    
    def chkReg( self, uid, pwd ):

        dbgFile("/var/www/log/%s.log" %(__name__))
        dbgKey( funcName= "chkReg In" )
        dbgKey( uid=uid, pwd=pwd )
        
        try:
            msg = ""
            cursor = self.con.cursor( prepared=True )
            
            sql = "select *  from loginInf where uid =? and pwd=?"
            cursor.execute(sql, (uid,pwd))
        
            row =cursor.fetchone()
            if row == None:
              msg = "NG"
            else:
              msg = "OK"

        except mysql.connector.Error as e:
            msg = "MySql error:" + str(e.args)

        finally:
            cursor.close()
            return msg





    def chkRegNG( self, uid, pwd ):

        try:
            cursor = self.con.cursor (buffered=True)
            # cursor = self.con.cursor ()
            # pwd= "' or 'A'='A"
            sql = "select *  from loginInf where uid ='%s' and pwd='%s'" %(uid, pwd)
            cursor.execute(sql)
        
            row =cursor.fetchone()
            # cursor.reset()
            # row =cursor.fetchall()
            if row == None:
              cursor.close()
              return ""
            else:
              cursor.close()
              return "OK"

        except mysql.connector.Error as e:
            dbg( "chkReg: MySqlError" , e.args)
            return "MySql error:" + str(e.args)




    # ログイン
    # 該当するユーザID、セッションIDを登録
    
    def login( self, uid, sid ):

        try:
            # cursor = self.con.cursor ()
            # sql = "update loginInf set sid='%s' where uid ='%s'" %( sid, uid )
            # cursor.execute(sql)

            msg =""
            cursor = self.con.cursor( prepared=True )
            sql = "update loginInf set sid = ? where uid = ?"
            cursor.execute(sql, ( sid, uid ))
            self.con.commit()
            msg ="OK"
            
        except mysql.connector.Error as e:
            self.con.rollback()
            msg = "MySql error:" + str(e.args)

        finally:
            cursor.close()
            return msg


    # ログインしているかチェック
    
    def chkLogin( self, uid, sid ):

        try:
            msg =""
            cursor = self.con.cursor( prepared=True )
            
            sql = "select *  from loginInf where uid=? and sid=?"
            cursor.execute(sql, (uid, sid))

            row = cursor.fetchone()
            if row != None:
              msg = "OK"
            else:
              msg = "NG"

        except mysql.connector.Error as e:
            msg =  "MySql error:" + str(e.args)

        finally:
            cursor.close()
            return msg
        





# -------------------------------
#         main
#　(コマンドラインから)
# 単体でテストする場合
# -------------------------------
def main():

 import sys

 db =dbase()
 while(True):
    print( "0. コンストラクタ" )
    print( "1. テーブル作成" )
    print( "2. 登録(ID作成)" )
    print( "3. chkReg" )
    print( "4. login" )
    print( "5. chkLogin" )


    no = input("No")
    no = int(no)

    if no==0:
      sys.exit()

    uid = input("ユーザID")
    pwd = input("password")
    sid = input("セッションID")
    if no==1:
      db.create()

    elif no==2:
      st = db.reg(uid, pwd )

      if st == "OK":
        print("登録OK")
      elif st == "NG":
        print("登録済み")
      else:
        print("reg() error"+ st)
        

    elif no==3:
      st = db.chkReg( uid, pwd )
      print( "st", st )

      # uid= "koba"
      # pwd= "' or 'A'='A"
      # st = db.chkRegNG( uid, pwd )
      # print( "st", st )


    elif no==4:
      st = db.login( uid, sid )
      print( "st", st, type(st))

    elif no==5:
      st = db.chkLogin( uid, sid )
      print( "st", st, type(st))
        

if __name__ == "__main__":
    
    main()



