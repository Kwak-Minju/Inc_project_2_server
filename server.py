
from flask import Flask, request
import pymysql
import json, datetime

app = Flask(__name__)

# 데이터 베이스 연결
def getCon():
  return pymysql.connect(host="localhost", 
                     user="root", password="1234", 
                     db="test3",
                     charset="utf8",
                     cursorclass=pymysql.cursors.DictCursor)
  
def json_default(value):
  if isinstance(value, datetime.date):
    return value.strftime('%Y-%m-%d')
  raise TypeError('not JSON serializable') 

# BoardPostList.js 게시물 리스트
@app.route('/boardlist', methods=['GET', 'POST'])
def boardlist() :
    con = getCon()
    cursor = con.cursor()
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') AS date FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC;")
    data = cursor.fetchall()
    return_data = json.dumps(data, default=json_default)
    
    # 반환할 때 json형식으로 반환
    return json.dumps(data, default=json_default)
  
# BoardContent.js 게시물 상세정보
@app.route('/boardDetail', methods=[ 'POST'])
def getBoardId():
  # boardId =int(request.get_data())
  boardId = request.get_json()
  id = boardId['id']

  con = getCon()
  cursor = con.cursor()
  sql = 'SELECT * FROM Board WHERE boardId = %s;'
  cursor.execute(sql, (id, ))
  data = cursor.fetchall()
  cursor.close()
    
  # 반환할 때 json형식으로 반환
  return json.dumps(data, default=json_default)

# BoardViewContent.js 게시물 수정
@app.route('/boardEdit', methods=['POST'])
def boardEdit() :
  boardData = request.get_json()
  print(boardData)
  con = getCon()
  cursor = con.cursor()

  cursor.execute("UPDATE Board SET title = '{}' WHERE boardId = {};".format(boardData['title'], boardData['boardId']))
  cursor.execute("UPDATE Board SET content = '{}' WHERE boardId = {};".format(boardData['content'], boardData['boardId']))
  cursor.connection.commit()


  return '성공적으로 수정되었습니다:)'

 # BoardViewContent.js 게시물 삭제
@app.route('/boardDelete', methods=['POST'])
def boardDelete() :
  boardData = request.get_json()
  print(boardData)
  con = getCon()
  cursor = con.cursor()

  cursor.execute("UPDATE Board SET status = 'inactive' WHERE boardId = {};".format(boardData['boardId']))
  cursor.connection.commit()


  return '성공적으로 삭제되었습니다'

if __name__ == "__main__" :
    app.run(debug=True)