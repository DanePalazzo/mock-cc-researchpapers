#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db , Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class ResearchFetch(Resource):
    def get(self):
        research = [research.to_dict(rules=("-research_authors",)) for research in Research.query.all()]
        return research, 200

class ResearchByID(Resource):
    def get(self, id):
        research = Research.query.filter_by(id=id).first()
        if not research:
            return {"error": "Research paper not found"}, 404
        return research.to_dict(), 200
    
    def delete(self, id):
        research = Research.query.filter_by(id=id).first()
        if not research:
            return {"error": "Research paper not found"}, 404
        db.session.delete(research)
        db.session.commit()
        return {}, 204

class Authors(Resource):
    def get(self):
        authors = [author.to_dict(rules=("-research_authors",)) for author in Author.query.all()]
        return authors, 200
    

class ResaerchAuthor(Resource):
    def post(self):
        try:
            new_research_author = ResearchAuthors(
                author_id = request.json["author_id"],
                research_id = request.json["research_id"],
            )
            db.session.add(new_research_author)
            db.session.commit()
            return new_research_author.to_dict(), 201
        except:
            return {"errors": ["validation errors"]}, 400



api.add_resource(ResearchFetch, "/research")
api.add_resource(ResearchByID, "/research/<int:id>")
api.add_resource(Authors, "/authors")
api.add_resource(ResaerchAuthor, "/research_author")

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/research')
def restaurants():

    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)
