from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def health():
    return "OK", 200

@app.route("/webhook/cyberbiz/order", methods=["POST"])
def cyberbiz_order():
    data = request.get_json(silent=True)
    print(data)  
    return "ok", 200
