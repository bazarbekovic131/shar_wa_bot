from db import WADatabase


def test1():
    db.create_tables()

    # Example phone number
    phone = '+1234567890'

    # Create a new user
    db.create_user(phone)
    print(f"User created with phone: {phone}")

    # Check if user has completed the survey
    if not db.has_completed_survey(phone):
        # Mock survey results
        results = {
            'age_group': '20-30',
            'production_experience': 'да',
            'experience_years': 5,
            'marital_status': 'в браке',
            'children_status': 'да'
        }

        # Save survey results
        db.save_survey_results(phone, results)
        print(f"Survey results saved for phone: {phone}")
    else:
        print(f"User with phone: {phone} has already completed the survey.")


if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'shark_whatsapp',
        'user': 'shark',
        'password': 'shark',
        'port': '5432'
    }

    # Initialize the database
    db = WADatabase(db_config)

    vacancies = db.get_vacancies
    print(vacancies)
 