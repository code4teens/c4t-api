from config import db, ma


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    display_name = db.Column(db.String(64), nullable=False, unique=True)


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        sqla_session = db.session
