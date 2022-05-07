from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))

    def to_json(self):
        return {
            "goal":{
                "id": self.goal_id,
                "title": self.title
            }
        }