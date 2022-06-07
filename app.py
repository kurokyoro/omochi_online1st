
# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'omochi'

@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/check',methods=["GET"])
def check():
    return render_template('check.html')


@app.route("/answer", methods=["POST"])
def answer_post():
    # アンケートのanswerに入力されたtextを取得
    answer = request.form.get("answer")
    # アンケートに正しく答えた場合、クッキーにuser_idを保存する
    if answer != "":
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into answer values(null, ?,null,null)",(answer,))
        conn.commit()   
        #answer送信によって生成されたuser_idをくっきーに保存
        c.execute("select id from answer where answer = ?",(answer,))
        user_id = c.fetchone()
        session["user_id"] = user_id[0]
        conn.close()
        return redirect("/make_room_id")
    else:
        return render_template('check.html')

@app.route("/make_room_id")
def make_room_id():
    user_id = session["user_id"]
    room_id = (user_id - 1 - ((user_id - 1)%4) + 4)/4
    room_id = int(room_id)
    session["room_id"] = room_id
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("update answer set room_id = ? where id = ?",(room_id, user_id,))
    conn.commit()
    conn.close()


    session["room_id"] = room_id
    return redirect("/chat")

@app.route("/comment", methods=["POST"])
def comment_post():
    user_id = session["user_id"]
    room_id = session["room_id"]
    # チャットの発言欄に入力されたtextを取得
    comment = request.form.get("comment")
    # 正しく発言した場合、クッキーにuser_idを保存しチャットルームに戻す
    if comment != "":
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into comment values(null, ?, ?, ?)",(comment, user_id, room_id))
        conn.commit()
        conn.close()
        return redirect("/chat")
    else:
        return render_template('chat.html')

@app.route('/chat')
def thyatto():
    user_id = session["user_id"]
    room_id = session["room_id"]
    # thyatto画面にanswerのデータを送信

    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select id, answer, room_id from answer where room_id = ?",(room_id,))
    answer_list = []
    for row in c.fetchall():
        answer_list.append({"id":row[0], "answer":row[1], "room_id":row[2]})
    conn.close()

    # thyatto画面にcommentのデータを送信
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select id, comment, user_id, room_id from comment where room_id = ?",(room_id,))
    comment_list = []
    for row in c.fetchall():
        comment_list.append({"id":row[0], "comment":row[1], "user_id":row[2], "room_id":row[3]})
    conn.close()

    return render_template("chat.html", answer_list = answer_list,  comment_list = comment_list)


# @app.route('/chat')
# def chat():
#     return render_template('chat.html')

@app.route('/end')
def end():
    return render_template('end.html')




@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound404(code):
    return "404だよ！！見つからないよ！！！"



if __name__ == "__main__":
    app.run(debug=True)