from flask import Flask, json, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, delete_application_from_db, get_all_applications
from sqlalchemy import text

app = Flask(__name__)


@app.route("/")
def hello_world():
  jobs=load_jobs_from_db()
  return render_template('home.html', jobs=jobs, company_name='Visteon')



@app.route("/api/jobs")
def list_jobs():
  jobs=load_jobs_from_db()
  return jsonify(jobs)


@app.route("/job/<id>", methods=['get'])
def show_job(id):
  job=load_job_from_db(id)
  if not job:
    return "Not Found", 404 
#   return jsonify(job)
  return render_template('jobpage.html',
                         job=job)


@app.route("/job/<id>/apply")
def show_job_json(id):
  data=request.args
  return jsonify(data)

@app.route("/job/<id>/apply", methods=["post"])
def apply_to_job(id):
  data=request.form 
  job=load_job_from_db(id)
  add_application_to_db(id,data)
  return render_template('application_submitted.html', application=data,job=job)

@app.route("/applications")
def show_all_applications():
    applications = get_all_applications()
    return render_template('all_applications.html', applications=applications)


@app.route("/job/<id>/", methods=["GET","POST","DELETE"])
def delete_application(id):
    application_id_to_delete = request.form.get('application_id')

    try:
        delete_application_from_db(application_id_to_delete)
        return jsonify({"message": f"Application {application_id_to_delete} deleted successfully"})
    except Exception as e:
        return jsonify({"error": f"Failed to delete application: {str(e)}"}), 500



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)





