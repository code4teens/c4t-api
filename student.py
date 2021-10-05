from models import Student, StudentSchema


def get_all():
    students = Student.query.order_by(Student.id).all()
    student_schema = StudentSchema(many=True)
    data = student_schema.dump(students)

    return data
