#!/usr/bin/python3



import os
import datetime

fname = "/var/www/log/dbg.log"
#fname = "/var/www/html/cgi/books/dbg.log"
mod   ="a"

# *msg　複数の引数をタプルで受け取る事ができる
def dbg( *msg ):
    
    import inspect
    
    cur= inspect.currentframe()
    info= inspect.getouterframes(cur)[1]
    fileLine = "%s[%d]" %(os.path.basename(info.filename), info.lineno)
    # tm  = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')        
    tm  = datetime.datetime.now().strftime('%H:%M:%S')        

    smsg = str(msg)       
    if len(msg) == 1:
      smsg2= smsg[1:-2]       # タプルの頭と尻の「(,)」を削除(引数が１つの場合)
    else:
      smsg2= smsg[1:-1]       # タプルの頭と尻の「()」を削除

    with open( fname, mod) as f:
      print( tm, fileLine, smsg2, flush=True, file=f  )

    ev = os.environ.get( 'DOCUMENT_ROOT')
    if ev == None:
      print( tm, fileLine, smsg2, flush=True)


# **msg　複数の引数を辞書型で受け取る
def dbgKey( **msg ):
    
    import inspect
    
    cur= inspect.currentframe()
    info= inspect.getouterframes(cur)[1]
    fileLine = "%s[%d]" %(os.path.basename(info.filename), info.lineno)
    # tm  = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')        
    tm  = datetime.datetime.now().strftime('%H:%M:%S')        

    smsg = str(msg)       
    smsg2= smsg[1:-1]       # 辞書の頭と尻のを削除

    with open( fname, mod) as f:
      print( tm, fileLine, smsg2, flush=True, file=f  )

    ev = os.environ.get( 'DOCUMENT_ROOT')
    if ev == None:
      print( tm, fileLine, smsg2, flush=True)
        
def dbgFile( fnameChg = "/var/www/html/dbg.log" ):

  global fname
  fname =fnameChg


def dbgInit( fileDel=True ):

  if fileDel == True:
    mod ="w"
  else:
    mod ="a"
    
  with open( fname, mod ) as f:
      tm  = datetime.datetime.now().strftime('%H:%M:%S')        
      with open( fname, mod) as f:
        print( '\nDebug Start',tm,fname, flush=True, file=f  )

# モジュールが読み込まれると初期化する
# dbgInit()
# dbgInit( fileDel=False )
# dbgInit( fileDel=True )


if __name__ == "__main__":
  
  dbg("デバッグ関数のテストケース")
  dbg("関数は次の二つになります")
  
  msg ="""

関数は次の二つになります

dbg( 変数1, 変数2,～)

dbgInit()
  デバッグ毎にファイルをクリアする（プログラムの最初で1回だけ呼ぶ）
  """
  
  no = 12345
  dbg( "数字型", no )
  strg ="Hello!"
  dbg( "文字列型", strg)
  
  dbg( "List内容", [1,2,3,"string"])

  stat =0
  dic ={"k1":1, "k2":5}
  dbg( "変数はいくつでも大丈夫", dic, stat)

  dbgKey( dic=dic, stat=stat)
