from flask import Flask, request

app = Flask(__name__)

# POSTとGETを許可
@app.route("/", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        print("✅ POSTリクエストを受信しました")
        # ここでLINEからのデータを受け取る（必要なら解析）
        return "OK", 200  # LINEに必ず200を返す
    else:
        return "Webhook is working!", 200

if __name__ == "__main__":
    # Renderやローカルで動かせるように設定
    app.run(host="0.0.0.0", port=10000)
