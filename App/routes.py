from App import application as app
from App import db
from flask import jsonify, request, render_template
from App.models import Person, Place, Review
from datetime import datetime

@app.route('/')
def home():
    R = jsonify("Hello World!")
    R.status_code = 200
    return R

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
        return render_template('new_person.html')

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
                longitude = request.form.get('long')
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
        return render_template('new_place.html')


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
                date_modified = datetime.now()
            )
            db.session.add(r)
            db.session.commit()
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
        return render_template('new_review.html', all_places=all_places, all_people=all_people)