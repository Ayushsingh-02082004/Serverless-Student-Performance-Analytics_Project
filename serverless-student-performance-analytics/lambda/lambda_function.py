import json
import boto3
from decimal import Decimal


# AWS Clients
s3 = boto3.client("s3")

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    "student_performance"
)


# ----------------------------------
# Performance Category
# ----------------------------------

def calculate_performance_category(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Average"

    else:
        return "Poor"


# ----------------------------------
# Student Risk Detection
# ----------------------------------

def calculate_risk(
    attendance,
    score
):

    if (
        attendance < 60
        or score < 50
    ):
        return True

    return False


# ----------------------------------
# Lambda Handler
# ----------------------------------

def lambda_handler(event, context):

    try:

        # -------------------------
        # Get Bucket & File Name
        # -------------------------

        bucket_name = (
            event["Records"][0]
            ["s3"]["bucket"]["name"]
        )

        file_key = (
            event["Records"][0]
            ["s3"]["object"]["key"]
        )

        print(
            f"Bucket Name: {bucket_name}"
        )

        print(
            f"File Name: {file_key}"
        )

        # -------------------------
        # Read File From S3
        # -------------------------

        response = s3.get_object(
            Bucket=bucket_name,
            Key=file_key
        )

        file_content = (
            response["Body"]
            .read()
            .decode("utf-8")
        )

        # -------------------------
        # Invalid JSON Handling
        # -------------------------

        try:

            students = json.loads(
                file_content,
                parse_float=Decimal
            )

        except json.JSONDecodeError:

            print(
                "Invalid JSON File"
            )

            return {

                "statusCode": 400,

                "message":
                "Invalid JSON File"
            }

        # -------------------------
        # Required Fields
        # -------------------------

        required_fields = [

            "student_id",

            "weekly_self_study_hours",

            "attendance_percentage",

            "class_participation",

            "total_score",

            "grade"
        ]

        # -------------------------
        # Batch Processing
        # -------------------------

        if len(students) > 500:

            print(
                "Using Batch Processing"
            )

            with table.batch_writer() as batch:

                for student in students:

                    # -----------------
                    # Missing Fields
                    # -----------------

                    missing_fields = [

                        field

                        for field
                        in required_fields

                        if field
                        not in student
                    ]

                    if missing_fields:

                        print(

                            f"Student skipped. "
                            f"Missing fields: "
                            f"{missing_fields}"
                        )

                        continue

                    # -----------------
                    # Duplicate Check
                    # -----------------

                    existing_student = (
                        table.get_item(

                            Key={
                                "student_id":
                                str(
                                    student[
                                        "student_id"
                                    ]
                                )
                            }
                        )
                    )

                    if (
                        "Item"
                        in existing_student
                    ):

                        print(

                            f"Duplicate Student: "
                            f"{student['student_id']}"
                        )

                        continue

                    # -----------------
                    # Business Logic
                    # -----------------

                    student[
                        "performance_category"
                    ] = (
                        calculate_performance_category(
                            float(
                                student[
                                    "total_score"
                                ]
                            )
                        )
                    )

                    student[
                        "at_risk"
                    ] = (
                        calculate_risk(
                            float(
                                student[
                                    "attendance_percentage"
                                ]
                            ),
                            float(
                                student[
                                    "total_score"
                                ]
                            )
                        )
                    )

                    student[
                        "student_id"
                    ] = str(
                        student[
                            "student_id"
                        ]
                    )

                    batch.put_item(
                        Item=student
                    )

                    print(
                        f"Inserted "
                        f"{student['student_id']}"
                    )

        else:

            print(
                "Using Normal Insert"
            )

            for student in students:

                # -----------------
                # Missing Fields
                # -----------------

                missing_fields = [

                    field

                    for field
                    in required_fields

                    if field
                    not in student
                ]

                if missing_fields:

                    print(

                        f"Student skipped. "
                        f"Missing fields: "
                        f"{missing_fields}"
                    )

                    continue

                # -----------------
                # Duplicate Check
                # -----------------

                existing_student = (
                    table.get_item(

                        Key={
                            "student_id":
                            str(
                                student[
                                    "student_id"
                                ]
                            )
                        }
                    )
                )

                if (
                    "Item"
                    in existing_student
                ):

                    print(

                        f"Duplicate Student: "
                        f"{student['student_id']}"
                    )

                    continue

                # -----------------
                # Business Logic
                # -----------------

                student[
                    "performance_category"
                ] = (
                    calculate_performance_category(
                        float(
                            student[
                                "total_score"
                            ]
                        )
                    )
                )

                student[
                    "at_risk"
                ] = (
                    calculate_risk(
                        float(
                            student[
                                "attendance_percentage"
                            ]
                        ),
                        float(
                            student[
                                "total_score"
                            ]
                        )
                    )
                )

                student[
                    "student_id"
                ] = str(
                    student[
                        "student_id"
                    ]
                )

                table.put_item(
                    Item=student
                )

                print(
                    f"Inserted "
                    f"{student['student_id']}"
                )

        return {

            "statusCode": 200,

            "message":
            "File processed successfully"
        }

    except Exception as e:

        import traceback

        print(
            "ERROR OCCURRED"
        )

        print(
            traceback.format_exc()
        )

        raise e
