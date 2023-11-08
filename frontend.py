from flask import Flask, request, render_template, jsonify
from peewee import PostgresqlDatabase
from main import combine
import os

def create_app():
    app = Flask(__name__)

    db1 = PostgresqlDatabase(
        os.getenv('DB_NAME'), 
        user=os.getenv('DB_USERNAME'), 
        password=os.getenv('DB_PASSWORD'), 
        host=os.getenv('DB_HOST'), 
        port=os.getenv('DB_PORT')
    )

    db1.connect()

    @app.route('/', methods=['GET', 'POST'])
    def job_search():
        result = None
        if request.method == 'POST':
            keywords = request.form.get('keywords', '')
            location = request.form.get('location', '')
            websites = request.form.getlist('websites')
            results_want = int(request.form.get('results_want', 0))
            resume = request.form.get('resume', '')

            if results_want > 50:
                return jsonify({'error': 'results_want cannot be more than 50'}), 400

            try:
                result = combine(keywords, location, websites, results_want, resume)
            except Exception as e:
                print(f"Error occurred during SCRAPING: {e}")


        return render_template('index.html', result=result)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=10000)
