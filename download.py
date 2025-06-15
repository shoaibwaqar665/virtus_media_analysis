from flask import Flask, send_file
from dbOperations import save_data_to_files
app = Flask(__name__)

@app.route('/download/json')
def download_json():
    return send_file('channels_data.json', as_attachment=True)

@app.route('/download/csv')
def download_csv():
    return send_file('channels_data.csv', as_attachment=True)

if __name__ == "__main__":
    save_data_to_files()
    app.run(debug=True)