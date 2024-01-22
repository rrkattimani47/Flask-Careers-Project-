from sqlalchemy import create_engine,text

db_connection_string = "mysql+pymysql://root:123@localhost/rashmicareers?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():  
  with engine.connect() as conn:
      result = conn.execute(text("select * from jobs"))
      jobs = []
      for row in result.all():
        jobs.append(dict(row._asdict()))
      return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        query = text("SELECT * FROM jobs WHERE id = :val")
        result = conn.execute(query.params(val=id))
        job = result.fetchone()
        if job:
            if isinstance(job, dict):
                return job
            else:
                return dict(job._asdict())
        else:
            return None


def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        try:
            query = text("""
                INSERT INTO applications 
                (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
                VALUES 
                (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
            """)
            conn.execute(
                query,
                {
                    "job_id": job_id,
                    "full_name": data['full_name'],
                    "email": data['email'],
                    "linkedin_url": data['linkedin_url'],
                    "education": data['education'],
                    "work_experience": data['work_experience'],
                    "resume_url": data['resume_url']
                }
            )
            conn.commit() 
        except Exception as e:
            print(f"Error: {e}")


def get_all_applications():
    with engine.connect() as conn:
        query = text("SELECT applications.*, jobs.title AS job_title FROM applications JOIN jobs ON applications.job_id = jobs.id")
        result = conn.execute(query)
        applications = [dict(row._asdict()) for row in result.fetchall()]
        return applications
    
def delete_application_from_db(application_id):
    with engine.connect() as conn:
        try:
            query = text("DELETE FROM applications WHERE id = :val")
            conn.execute(query.params(val=application_id))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")


