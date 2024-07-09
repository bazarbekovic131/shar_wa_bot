import psycopg2

class WADatabase():
    def __init__(self, db_config):
        self.conn = self.create_connection(db_config)

    def create_connection(self, db_config):
        try:
            conn = psycopg2.connect(**db_config)
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
    def get_users(self, query):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT phone from users WHERE phone = %s
                """, (query)
            )
            user  = cur.fetchone() # fetch phone number
            cur.close()
            return user
        
    def save_survey_results(self, user_phone, results):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE users SET 
                    age_group = %s,
                    production_experience = %s,
                    experience_years = %s,
                    marital_status = %s,
                    children_status = %s,
                    completed_survey = TRUE
                    WHERE phone = %s
                """, (results['age_group'], results['production_experience'], results['experience_years'], results['marital_status'], results['children_status'], user_phone )
            )
            user  = cur.fetchone() # fetch phone number
            cur.close()
            return user
        
    def get_user_id_from_phone_number(self, phone_number):
        # Example implementation to get user_id from phone number
        with self.conn.cursor() as cur:       
            cur.execute("SELECT user_id FROM users WHERE phone_number = %s", (phone_number,))
            result = cur.fetchone()
            cur.close()
            return result[0] if result else None

    