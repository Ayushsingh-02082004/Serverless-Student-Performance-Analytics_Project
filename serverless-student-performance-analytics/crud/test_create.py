from decimal import Decimal
from student_crud import StudentCRUD

crud = StudentCRUD()

student = {

    "student_id": "1000",

    "weekly_self_study_hours": Decimal("15.5"),

    "attendance_percentage": Decimal("92.5"),

    "class_participation": Decimal("8.0"),

    "total_score": Decimal("95.0"),

    "grade": "A",

    "performance_category": "Excellent"
}

crud.create_student(student)
