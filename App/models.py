from App import db

class Person(db.Model):
    # Primary Key
    person_id = db.Column(db.Integer, primary_key=True)
    # General information
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    nickname = db.Column(db.String(50), unique=False, nullable=True)
    # Relationships
    reviews = db.relationship("Review", back_populates="person")

    @property
    def dict(self):
        return {
            'id' : self.person_id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'nickname' : self.nickname,
            'reviews' : [r.dict for r in self.reviews]
        }

    def __str__(self):
        return f'<Person {self.first_name} {self.last_name} {self.person_id}>'

class Place(db.Model):
    # Primary Key
    place_id = db.Column(db.Integer, primary_key=True)
    # General information
    name = db.Column(db.String(50), unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    longitude = db.Column(db.Float, unique=False, nullable=False)
    # Relationships
    reviews = db.relationship("Review", back_populates="place")

    @property
    def dict(self):
        return {
            'id' : self.place_id,
            'name' : self.name,
            'latitude' : self.latitude,
            'longitude' : self.longitude,
            'reviews' : [r.dict for r in self.reviews]
        }

    def __str__(self):
        return f'<Place {self.place_id}>'

class Review(db.Model):
    # Primary Key
    review_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, unique=False, nullable=False)
    date_modified = db.Column(db.DateTime, unique=False, nullable=False)

    # Relationships
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    person = db.relationship("Person", back_populates="reviews")
    place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    place = db.relationship("Place", back_populates="reviews")

    @property
    def dict(self):
        return {
            'id' : self.review_id,
            'rating' : self.rating,
            'content' : self.content,
            'person_id' : self.person_id,
            'place_id' : self.place_id,
            'date_created' : self.date_created.timestamp(),
            'date_modified' : self.date_modified.timestamp()
        }

    def __str__(self):
        return f'<Review {self.review_id}>'