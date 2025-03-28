from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load datasets
education_df = pd.read_csv("education.csv")
jobs_df = pd.read_csv("Jobs_Dataset.csv")

# Simple job recommendation function
def recommend_jobs(qualification):
    """Recommend jobs based on user qualification."""
    recommended_jobs = jobs_df[jobs_df['Qualification'].str.contains(qualification, case=False, na=False)]
    return recommended_jobs[['Job Title', 'Company', 'Location', 'Salary', 'Job Type']].to_dict(orient="records")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get("qualification")
    
    if not user_input:
        return jsonify({"error": "No qualification provided"}), 400
    
    recommendations = recommend_jobs(user_input)
    
    if not recommendations:
        return jsonify({"message": "No matching jobs found"}), 404
    
    return jsonify({"jobs": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
