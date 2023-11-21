from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Research(db.Model, SerializerMixin):
    __tablename__ = "research_table"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    research_authors = db.relationship("ResearchAuthors", back_populates="research")

    serialize_rules=("-research_authors.research",)

    @validates("year")
    def validates_year(year):
        if not year or len(year) is not 4:
            raise ValueError("Year must be a valid 4 diget year")
        return year
        


class Author(db.Model, SerializerMixin):
    __tablename__ = "author_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    research_authors = db.relationship("ResearchAuthors", back_populates="author")
    
    serialize_rules=("-research_authors.author",)

    @validates("field_of_study")
    def validates_field_of_study(field_of_study):
        valid_list = ["AI", "ROBOTICS", "MACHINE LEARNING", "VISION", "CYBERSECURITY"]
        if field_of_study.upper() not in valid_list:
            raise ValueError('Filed of Study must be "AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"')
        return field_of_study


class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = "research_authors_table"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author_table.id"))
    author = db.relationship("Author", back_populates="research_authors")
    research_id = db.Column(db.Integer, db.ForeignKey("research_table.id"))
    research = db.relationship("Research", back_populates="research_authors")

    serialize_rules=("-author.research_authors", "-research.research_authors")