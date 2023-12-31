from sqlalchemy import create_engine,text

db_connection_string = "mysql+pymysql://zspttffybz0akr3djirz:pscale_pw_YEJv0m50nhQVF1ZQ3NMvtyXk11IRszszqWqn0T1ye9W@aws.connect.psdb.cloud/rashmicareers?charset=utf8mb4"

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


# def add_application_to_db(job_id, data):
#     with engine.connect() as conn:
#         query = text("""
#             INSERT INTO applications 
#             (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
#             VALUES 
#             (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
#         """)
#         conn.execute(
#             query,
#             job_id=job_id,
#             full_name=data['full_name'],
#             email=data['email'],
#             linkedin_url=data['linkedin_url'],
#             education=data['education'],
#             work_experience=data['work_experience'],
#             resume_url=data['resume_url']
#         )