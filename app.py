from flask import Flask, render_template, request

from settings import FLATS_PER_PAGE, Session
from tutorial.spiders.flats import Flat

app = Flask(__name__)


@app.route('/')
def index():
    page = int(request.args.get('page', 1))

    # Calculate offset and limit for pagination
    offset = (page - 1) * FLATS_PER_PAGE
    limit = FLATS_PER_PAGE
    session = Session()
    flats = session.query(Flat).offset(offset).limit(limit).all()
    total_flats = session.query(Flat).count()

    # Calculate total number of pages
    total_pages = (total_flats + FLATS_PER_PAGE - 1) // FLATS_PER_PAGE

    return render_template('index.html', flats=flats, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
