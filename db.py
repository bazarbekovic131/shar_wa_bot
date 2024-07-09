import psycopg2

class WADatabase():
    #### create tables users and surveys for now ###

    def __init__(self, db_config):
        self.conn = self.create_connection(db_config)

    def create_connection(self, db_config):
        try:
            conn = psycopg2.connect(**db_config)
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
        
    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(32) UNIQUE,
                        has_completed_survey BOOLEAN
                        )""")
            
            cur.execute("""CREATE TABLE IF NOT EXISTS surveys (
                        id SERIAL PRIMARY KEY,
                        age_group VARCHAR(32),
                        production_experience VARCHAR(8),
                        experience_years INTEGER,
                        marital_status VARCHAR(8),
                        children_status VARCHAR(8),
                        completed_survey BOOLEAN,
                        phone VARCHAR(16) UNIQUE
                        )""")
    def get_users(self, query):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT phone from users WHERE phone = %s
                """, (query)
            )
            user  = cur.fetchone() # fetch phone number
            cur.close()
            return user # should return count of users instead of some user variable?
        
    def save_survey_results(self, user_phone, results):
        with self.conn.cursor() as cur: # in the table surveys
            cur.execute(
                """
                    UPDATE surveys SET 
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

    