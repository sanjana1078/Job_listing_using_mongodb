from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['job_listing_database']
jobs_collection = db['jobs']

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_job_page')
def add_job_page():
    return render_template('add_job.html')

@app.route('/add_job', methods=['POST'])
def add_job():
    job_data = request.form.to_dict()
    jobs_collection.insert_one(job_data)
    return redirect(url_for('view_jobs'))

@app.route('/view_jobs')
def view_jobs():
    jobs = list(jobs_collection.find())
    return render_template('view_jobs.html', jobs=jobs)

@app.route('/delete_job/<job_id>', methods=['POST'])
def delete_job(job_id):
    jobs_collection.delete_one({'_id': ObjectId(job_id)})
    return jsonify({'message': 'Job deleted successfully'})

@app.route('/update_job_page/<job_id>')
def update_job_page(job_id):
    job = jobs_collection.find_one({'_id': ObjectId(job_id)})
    return render_template('update_job.html', job=job)

@app.route('/update_job/<job_id>', methods=['POST'])
def update_job(job_id):
    new_job_data = request.form.to_dict()
    jobs_collection.update_one({'_id': ObjectId(job_id)}, {'$set': new_job_data})
    return jsonify({'message': 'Job updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
