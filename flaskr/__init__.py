from flask import Flask,jsonify,request,abort
from models import setup_db, Plant
from flask_cors import CORS
import random

PLANTS_PER_PAGE = 10
def paginate_plants(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * PLANTS_PER_PAGE
    end = start + PLANTS_PER_PAGE
    plants = [plant.format() for plant in selection]
    current_plants = plants[start:end]
    return current_plants

def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/plants')
    def get_plants():
        plants = Plant.query.all()
        current_plants=paginate_plants(request,plants)
        if len(current_plants)==0:
            abort(404)
        else:
            formatted_plants = current_plants
            return jsonify({
                'success':True,
                'plants':formatted_plants,
                'totals_plants':len(Plant.query.all())
            })

    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id): 
        plant=Plant.query.filter_by(id=plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success':True,
                'plant':plant.format()
            })


    @app.route('/plants/<int:plant_id>', methods=['DELETE'])
    def delete_plant(plant_id):
        try: 
            plant=Plant.query.filter_by(id=plant_id).one_or_none()

            if plant is None:
                abort(404)
            else:
                plant.delete()
                totals_plants=Plant.query.all()
                return jsonify({
                    'success':True,
                    'deleted':plant_id,
                    'plants':paginate_plants(request,totals_plants),
                    'totals_plants':len(totals_plants)
                })
        except:
            abort(422)
        


    @app.route('/plants/<int:plant_id>', methods=['PATCH'])
    def update_plant(plant_id):
        #ici on récupère l'information passée dans le body
        body=request.get_json()
        try:
            plant=Plant.query.filter_by(id=plant_id).one_or_none()
            if plant is None:
                abort(404)
            else:
                if 'primary_color' in body:
                    plant.primary_color=body.get('primary_color')
                    plant.update()
                    return jsonify({
                        'success':True,
                        'id':plant.id
                    })
        except:
            abort(400)
       
    return app