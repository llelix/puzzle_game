from models import db, PlayerRecord

def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    with app.app_context():
        db.create_all()

def add_record(name, steps, time):
    """添加玩家记录"""
    record = PlayerRecord(name=name, steps=steps, time=time)
    db.session.add(record)
    db.session.commit()

def get_records():
    """获取排行榜"""
    return PlayerRecord.query.order_by(PlayerRecord.steps.asc(), PlayerRecord.time.asc()).limit(10).all()