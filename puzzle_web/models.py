from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PlayerRecord(db.Model):
    """玩家记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)  # 时间（秒）

    def __repr__(self):
        return f"<PlayerRecord {self.name}: {self.steps} steps, {self.time} seconds>"