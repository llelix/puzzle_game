from flask import Flask, render_template, jsonify, request
from database import init_db, add_record, get_records
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sliding_puzzle.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化数据库
init_db(app)

@app.route("/")
def index():
    """首页"""
    return render_template("index.html")

@app.route("/records", methods=["GET"])
def get_leaderboard():
    """获取排行榜"""
    records = get_records()
    leaderboard = [{"name": record.name, "steps": record.steps, "time": record.time} for record in records]
    return jsonify(leaderboard)

@app.route("/records", methods=["POST"])
def save_record():
    """保存玩家记录"""
    data = request.json
    name = data.get("name")
    steps = data.get("steps")
    time = data.get("time")
    if name and steps and time:
        add_record(name, steps, time)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)