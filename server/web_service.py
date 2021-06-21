from flask import Flask, jsonify
from flask_cors import CORS
from db_access import DBAccess
import scraper


app = Flask(__name__)
CORS(app)


@app.route('/fetch_programs', methods=['GET'])
def fetch_programs():
    fetched_programs = DBAccess.getInstance().fetch_programs()
    if fetched_programs:
        return jsonify(msg="Programs fetched successfully", data=fetched_programs)
    return jsonify(msg='Error while fetching programs', data=False)


@app.route('/update_programs', methods=['GET'])
def update_programs():
    response = scraper.update_database()
    if response:
        return fetch_programs()
    return jsonify(msg="No updates were made", data=None)


if __name__ == '__main__':
    scraper.populate_database()
    app.run()
