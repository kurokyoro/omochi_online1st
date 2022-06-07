# splite3をimportする
# datetimeもimportするOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

import sqlite3, datetime

dt_now = datetime.datetime.now()
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flaskでは標準でFlask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'sunabaco'


# top画面表示
@app.route('/', methods=["GET"])
def top():
    return render_template('o_top.html')

# 入室ボタンが押されたらchoyusei画面を表示
@app.route('/entering', methods=["GET"])
def entering():
     # thyatto画面にtemaのデータを送信
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select tema from tema where id = 1")
    tema = c.fetchone()
    tema = tema[0]

    conn.close()

    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select question from tema where id = 1")
    question = c.fetchone()
    question = question[0]

    conn.close()
    return render_template('o_chyousei.html',tema = tema, question =question)




# アンケート回答ボタンが押されると回答内容とユーザー固有のIDをDB内のanswerテーブルに格納
@app.route("/answer", methods=["POST"])
def answer_post():
    # アンケートのanswerに入力されたtextを取得
    answer = request.form.get("answer")
    # アンケートに正しく答えた場合、クッキーにuser_idを保存する
    if answer != "":
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into answer values(null, ?,null, null)",(answer,))
        conn.commit()   
        #answer送信によって生成されたuser_idをくっきーに保存
        c.execute("select id from answer where answer = ?",(answer,))
        user_id = c.fetchone()
        session["user_id"] = user_id[0]
        conn.close()
        return redirect("/make_roomId_colorId")
    else:
        return render_template('o_chyousei.html')


@app.route("/make_roomId_colorId")
def make_room_id():
    user_id = session["user_id"]
    room_id = (user_id - 1 - ((user_id - 1)%4) + 4)/4
    color_id = user_id%4
    room_id = int(room_id)
    color_id = int(color_id)
    session["room_id"] = room_id
    session["color_id"] = color_id
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("update answer set room_id = ? , color_id = ? where id = ?",(room_id, color_id, user_id))
    conn.commit()
    conn.close()


    session["room_id"] = room_id
    session["color_id"] =color_id
    return redirect("/thyatto")





# 発言ボタンが押されると発言内容がIDをDB内のcommentテーブルに格納
@app.route("/comment", methods=["POST"])
def comment_post():
    user_id = session["user_id"]
    room_id = session["room_id"]
    color_id = session["color_id"]
    # チャットの発言欄に入力されたtextを取得
    comment = request.form.get("comment")
    # 正しく発言した場合、クッキーにuser_idを保存しチャットルームに戻す
    if comment != "":
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into comment values(null, ?, ?, ?, ?)",(comment, user_id, room_id, color_id))
        conn.commit()
        conn.close()
        return redirect("/thyatto")
    else:
        return redirect("/thyatto")




# thyatto画面表示
@app.route('/thyatto')
def thyatto():
    user_id = session["user_id"]
    room_id = session["room_id"]
    color_id = session["color_id"]

 # thyatto画面にtemaのデータを送信
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select tema from tema where id = 1")
    tema = c.fetchone()
    tema = tema[0]

    conn.close()

    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select question from tema where id = 1")
    question = c.fetchone()
    question = question[0]

    conn.close()
    # thyatto画面にanswerのデータを送信

    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select id, answer, room_id, color_id from answer where room_id = ?",(room_id,))
    answer_list = []
    for row in c.fetchall():
        answer_list.append({"id":row[0], "answer":row[1], "room_id":row[2], "color_id":row[3]})
    conn.close()

    # thyatto画面にcommentのデータを送信
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select id, comment, user_id, room_id, color_id from comment where room_id = ?",(room_id,))
    comment_list = []
    for row in c.fetchall():
        comment_list.append({"id":row[0], "comment":row[1], "user_id":row[2], "room_id":row[3], "color_id":row[4]})
    conn.close()

    return render_template("o_thyatto.html",tema = tema, question =question, answer_list = answer_list,  comment_list = comment_list)





# end画面表示
@app.route('/end')
def end():
    return render_template('o_end.html')






@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound404(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=True)