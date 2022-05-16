from App import application as app
from App import db
from flask import jsonify, request, render_template
from werkzeug.utils import secure_filename
from App.models import Person, Place, Review
from datetime import datetime
from pathlib import Path
import statistics

# ---------------  WEBSITE  -------------- #

@app.route('/', methods=['GET'])
def home():
    # Return the from for creating new places
    if request.method == 'GET':
        places = Place.query.all()
        reviewed_places = [p for p in places if len(p.reviews) > 0]
        return render_template('home.html', places=reviewed_places, places_dicts=[p.dict for p in places])

@app.route('/image/upload', methods=['GET', 'POST'])
def image_upload():
    # Return the from for creating new places
    if request.method == 'GET':
        return render_template('image_upload.html')
    elif request.method == 'POST':
      f = request.files['file']
      fname = f.filename.split('.')
      fname[0] = request.form.get('filename')
      fname = '.'.join(fname)
      f.save(f"App/static/images/{request.form.get('image_type')}/" + secure_filename(fname))
      return 'file uploaded successfully'

# ---------------  PERSON  --------------- #

@app.route('/person', methods=['GET', 'POST'])
def all_people():
    # Return all people as a json list of dicts
    if request.method == 'GET':
        all_people = Person.query.all()
        return jsonify([p.dict for p in all_people]), 200
    # POST a new review
    elif request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'save':
            p = Person(
                first_name = request.form.get('first_name'),
                last_name = request.form.get('last_name'),
                nickname = request.form.get('nickname'),
                image = None if request.form.get('image') == '' else request.form.get('image')
            )
            db.session.add(p)
            db.session.commit()
        else:
            response_data = request.get_json()
            p = Person(
                first_name = response_data['first_name'],
                last_name = response_data['last_name'],
                nickname = response_data['nickname'],
            )
            db.session.add(p)
            db.session.commit()
        return {'success' : 'all good!'}, 200

@app.route('/person/<id>', methods=['GET'])
def get_person(id):
    # Return a specific person
    if request.method == 'GET':
        person = Person.query.filter_by(person_id=id).first()
        return jsonify(person.dict), 200

@app.route('/person/create', methods=['GET'])
def create_person():
    # Return the from for creating new places
    if request.method == 'GET':
        images_path = Path("./App/static/images/person").iterdir()
        images = [[i.as_posix(), i.stem ] for i in images_path]
        return render_template('new_person.html', images=images)

# ----------------  PLACE  ---------------- #

@app.route('/place', methods=['GET', 'POST'])
def all_places():
    # Return all places as a json list of dicts
    if request.method == 'GET':
        all_places = Place.query.all()
        return jsonify([p.dict for p in all_places]), 200
    # POST a new review
    elif request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'save':
            p = Place(
                name = request.form.get('name'),
                latitude = request.form.get('lat'),
                longitude = request.form.get('long'),
                image = None if request.form.get('image') == '' else request.form.get('image')
            )
            db.session.add(p)
            db.session.commit()
        else:
            response_data = request.get_json()
            p = Place(
                name = response_data['name'],
                latitude = response_data['latitude'],
                longitude = response_data['longitude']
            )
            db.session.add(p)
            db.session.commit()
        return {'success' : 'all good!'}, 200

@app.route('/place/<id>', methods=['GET'])
def get_place(id):
    # Return a specific place
    if request.method == 'GET':
        place = Place.query.filter_by(place_id=id).first()
        return jsonify(place.dict), 200

@app.route('/place/create', methods=['GET'])
def create_place():
    # Return the from for creating new places
    if request.method == 'GET':
        images_path = Path("./App/static/images/place").iterdir()
        images = [[i.as_posix(), i.stem ] for i in images_path]
        return render_template('new_place.html', images=images)


# ----------------  Review  ---------------- #

@app.route('/review', methods=['GET', 'POST'])
def all_reviews():
    # Return all reviews as a json list of dicts
    if request.method == 'GET':
        all_reviews = Review.query.all()
        return jsonify([r.dict for r in all_reviews]), 200
    # POST a new review
    elif request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'save':
            r = Review(
                person_id = request.form.get('person_id'),
                place_id = request.form.get('place_id'),
                rating = request.form.get('rating'),
                content = request.form.get('content'),
                date_created = datetime.now(),
                date_modified = datetime.now(),
                image = None if request.form.get('image') == '' else request.form.get('image')
            )
        else:
            response_data = request.get_json()
            r = Review(
                person_id = response_data['person_id'],
                place_id = response_data['place_id'],
                rating = response_data['rating'],
                content = response_data['content'],
                date_created = datetime.fromtimestamp(response_data['date_created']),
                date_modified = datetime.fromtimestamp(response_data['date_modified'])
            )
        db.session.add(r)
        # Calculate the new aggregate for the place
        p = Place.query.filter_by(place_id=r.place_id).first()
        p.aggregate = round(statistics.mean([float(r.rating) for r in p.reviews]), 2)
        db.session.add(p)
        db.session.commit()
        return {'success' : 'all good!'}, 200

@app.route('/review/<id>', methods=['GET'])
def get_review(id):
    # Return a specific review
    if request.method == 'GET':
        review = Review.query.filter_by(review_id=id).first()
        return jsonify(review.dict), 200

@app.route('/review/create', methods=['GET'])
def create_review():
    # Return the from for creating new places
    if request.method == 'GET':
        all_places = Place.query.all()
        all_people = Person.query.all()
        images_path = Path("./App/static/images/review").iterdir()
        images = [[i.as_posix(), i.stem ] for i in images_path]
        return render_template('new_review.html', all_places=all_places, all_people=all_people, images=images)

@app.route('/review/<id>/edit', methods=['GET', 'POST'])
def edit_review(id):
    if request.method == 'GET':
        all_places = Place.query.all()
        all_people = Person.query.all()
        review = Review.query.filter_by(review_id=id).first()
        images_path = Path("./App/static/images/review").iterdir()
        images = [[i.as_posix(), i.stem ] for i in images_path]
        return render_template('edit_review.html', id=id, all_places=all_places, all_people=all_people, review=review, images=images)
    elif request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'save':
            review = Review.query.filter_by(review_id=id).first()
            review.person_id = request.form.get('person_id')
            review.place_id = request.form.get('place_id')
            review.rating = request.form.get('rating')
            review.content = request.form.get('content')
            review.date_modified = datetime.now()
            review.image = None if request.form.get('image') == '' else request.form.get('image')
            db.session.add(review)
            db.session.commit()
            return {'success' : 'all good!'}, 200
