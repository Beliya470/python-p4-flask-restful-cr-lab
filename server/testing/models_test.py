from app import app
from models import db, Plant

class TestPlant:
    '''Plant model in models.py'''
    
    def test_can_instantiate(self):
        '''can be instantiated with a name.'''
        p = Plant(name="Douglas Fir", image="some_image_url_or_path", price=20.0)
        assert(p)
    
    def test_can_be_created(self):
        '''can create records that can be committed to the database.'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="some_image_url_or_path", price=20.0)
            db.session.add(p)
            db.session.commit()
            assert(p.id)

            db.session.delete(p)
            db.session.commit()

    def test_can_be_retrieved(self):
        '''can be used to retrieve records from the database.'''
        with app.app_context():
            # Adding a plant before querying all plants
            p = Plant(name="Douglas Fir", image="some_image_url_or_path", price=20.0)
            db.session.add(p)
            db.session.commit()
            
            plants = Plant.query.all()
            assert(plants)  # this will now be True if the plant is added successfully
            
            # Clean up by deleting the added plant
            db.session.delete(p)
            db.session.commit()

    def test_can_be_serialized(self):
        '''can create records with a serialize() method for serialization.'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="some_image_url_or_path", price=20.0)
            db.session.add(p)
            db.session.commit()
            p_dict = Plant.query.filter_by(name="Douglas Fir").first().serialize()
            assert((type(p_dict) == dict) and (p_dict["name"] == "Douglas Fir"))
            
            db.session.delete(p)
            db.session.commit()
