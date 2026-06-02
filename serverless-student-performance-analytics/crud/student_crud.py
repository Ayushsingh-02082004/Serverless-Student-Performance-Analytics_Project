import boto3
from decimal import Decimal


class StudentCRUD:

    def __init__(self):

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="ap-south-1"
        )

        self.table = self.dynamodb.Table(
            "student_performance"
        )

    # -----------------------------
    # CREATE
    # -----------------------------
    def create_student(self, student):

        response = self.table.put_item(
            Item=student
        )

        print("Student inserted successfully")

        return response

    # -----------------------------
    # READ
    # -----------------------------
    def read_student(self, student_id):

        response = self.table.get_item(
            Key={
                "student_id": str(student_id)
            }
        )

        item = response.get("Item")

        if item:
            print(item)
        else:
            print("Student not found")

        return item

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_student(
        self,
        student_id,
        weekly_self_study_hours,
        attendance_percentage,
        class_participation,
        total_score,
        grade
    ):

        response = self.table.update_item(

            Key={
                "student_id": str(student_id)
            },

            UpdateExpression="""
            SET
            weekly_self_study_hours = :h,
            attendance_percentage = :a,
            class_participation = :c,
            total_score = :s,
            grade = :g
            """,

            ExpressionAttributeValues={

                ":h": Decimal(
                    str(weekly_self_study_hours)
                ),

                ":a": Decimal(
                    str(attendance_percentage)
                ),

                ":c": Decimal(
                    str(class_participation)
                ),

                ":s": Decimal(
                    str(total_score)
                ),

                ":g": grade
            },

            ReturnValues="UPDATED_NEW"
        )

        print("Student updated")

        return response

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_student(
        self,
        student_id
    ):

        response = self.table.delete_item(
            Key={
                "student_id": str(student_id)
            }
        )

        print("Student deleted")

        return response
