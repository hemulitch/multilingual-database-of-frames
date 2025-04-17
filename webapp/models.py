from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


db = SQLAlchemy()

class BFN(db.Model):
    __tablename__ = "bfn"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)
    
    # connections
    bfn_to_frame_relations = db.relationship("BFN_Relationship", uselist=False, primaryjoin="BFN.id==BFN_Relationship.parent_id")
    bfn_to_lus = db.relationship("BFN_LexicalUnits", uselist=False, primaryjoin="BFN.id==BFN_LexicalUnits.frame_id")
    bfn_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="BFN.id==MultilingualFN.bfn_frame_id")

class BFN_Relationship(db.Model):
    __tablename__ = "bfn_frame_relations"

    parent_id = db.Column('parent_id', db.Integer, ForeignKey('bfn.id'))
    child_id = db.Column('child_id', db.Integer)
    relation_id = db.Column('relation_id', db.Integer, primary_key=True)

    relationship_to_types = db.relationship("RelationTypes", uselist=False, primaryjoin="BFN_Relationship.relation_id==RelationTypes.id")

class RelationTypes(db.Model):
    __tablename__ = "relation_types"

    id = db.Column('id', db.Integer, ForeignKey('bfn_frame_relations.relation_id'), primary_key=True)
    relation_type = db.Column('type', db.Text)
    superframe = db.Column('superframe', db.Text)
    subframe = db.Column('subframe', db.Text)
    definition = db.Column('definition', db.Text)

class BFN_LexicalUnits(db.Model):
    __tablename__ = "bfn_lu"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('bfn.id'))

class BrasilFN(db.Model):
    __tablename__ = "brasilfn"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    brasilfn_to_lus = db.relationship("BrasilFN_LexicalUnits", uselist=False, primaryjoin="BrasilFN.id==BrasilFN_LexicalUnits.frame_id")
    brasilfn_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="BrasilFN.id==MultilingualFN.brasilfn_frame_id")


class BrasilFN_LexicalUnits(db.Model):
    __tablename__ = "brasilfn_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('brasilfn.id'))

class DiCoEnviro(db.Model):
    __tablename__ = "dicoenviro"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    dicoenviro_to_lus = db.relationship("DiCoEnviro_LexicalUnits", uselist=False, primaryjoin="DiCoEnviro.id==DiCoEnviro_LexicalUnits.frame_id")
    dicoenviro_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="DiCoEnviro.id==MultilingualFN.dicoenviro_frame_id")

class DiCoEnviro_LexicalUnits(db.Model):
    __tablename__ = "dicoenviro_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('dicoenviro.id'))

class DiCoInfo(db.Model):
    __tablename__ = "dicoinfo"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    dicoinfo_to_lus = db.relationship("DiCoInfo_LexicalUnits", uselist=False, primaryjoin="DiCoInfo.id==DiCoInfo_LexicalUnits.frame_id")
    dicoinfo_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="DiCoInfo.id==MultilingualFN.dicoinfo_frame_id")

class DiCoInfo_LexicalUnits(db.Model):
    __tablename__ = "dicoinfo_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('dicoinfo.id'))

class GermanFN(db.Model):
    __tablename__ = "germanfn"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    germanfn_to_lus = db.relationship("GermanFN_LexicalUnits", uselist=False, primaryjoin="GermanFN.id==GermanFN_LexicalUnits.frame_id")
    germanfn_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="GermanFN.id==MultilingualFN.germanfn_frame_id")

class GermanFN_LexicalUnits(db.Model):
    __tablename__ = "germanfn_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('germanfn.id'))

class GFOL(db.Model):
    __tablename__ = "gfol"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    gfol_to_lus = db.relationship("GFOL_LexicalUnits", uselist=False, primaryjoin="GFOL.id==GFOL_LexicalUnits.frame_id")
    gfol_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="GFOL.id==MultilingualFN.gfol_frame_id")

class GFOL_LexicalUnits(db.Model):
    __tablename__ = "gfol_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('gfol.id'))

class SpanishFN(db.Model):
    __tablename__ = "spanishfn"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    spanishfn_to_lus = db.relationship("SpanishFN_LexicalUnits", uselist=False, primaryjoin="SpanishFN.id==SpanishFN_LexicalUnits.frame_id")
    spanishfn_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="SpanishFN.id==MultilingualFN.spanishfn_frame_id")

class SpanishFN_LexicalUnits(db.Model):
    __tablename__ = "spanishfn_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('spanishfn.id'))

class SweFN(db.Model):
    __tablename__ = "swefn"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('frame', db.Text)
    frame_elements = db.Column('frame_elements', db.Text)
    definition = db.Column('definition', db.Text)
    link = db.Column('link', db.Text)

    swefn_to_lus = db.relationship("SweFN_LexicalUnits", uselist=False, primaryjoin="SweFN.id==SweFN_LexicalUnits.frame_id")
    swefn_to_multilingualfn = db.relationship("MultilingualFN", uselist=False, primaryjoin="SweFN.id==MultilingualFN.swefn_frame_id")

class SweFN_LexicalUnits(db.Model):
    __tablename__ = "swefn_lu"

    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.Text)
    pos = db.Column('pos', db.Text)
    lang = db.Column('lang', db.Text)
    frame_id = db.Column('frame_id', db.Integer, ForeignKey('swefn.id'))

class MultilingualFN(db.Model):
    __tablename__ = "multilingualfn"

    id = db.Column('multilingual_id', db.Integer, primary_key=True)
    frame_name = db.Column('frame_name', db.Text)
    swefn_frame_id = db.Column('swefn_frame_id', db.Integer, ForeignKey('swefn.id'))
    swefn_ME = db.Column('swefn_match_evaluation', db.Text)
    brasilfn_frame_id = db.Column('brasilfn_frame_id', db.Integer, ForeignKey('brasilfn.id'))
    brasilfn_ME = db.Column('brasilfn_match_evaluation', db.Text)
    dicoenviro_frame_id = db.Column('dicoenviro_frame_id', db.Integer, ForeignKey('dicoenviro.id'))
    dicoenviro_ME = db.Column('dicoenviro_match_evaluation', db.Text)
    bfn_frame_id = db.Column('bfn_frame_id', db.Integer, ForeignKey('bfn.id'))
    bfn_ME = db.Column('bfn_match_evaluation', db.Text)
    gfol_frame_id = db.Column('gfol_frame_id', db.Integer, ForeignKey('gfol.id'))
    gfol_ME = db.Column('gfol_match_evaluation', db.Text)
    dicoinfo_frame_id = db.Column('dicoinfo_frame_id', db.Integer, ForeignKey('dicoinfo.id'))
    dicoinfo_ME = db.Column('dicoinfo_match_evaluation', db.Text)
    germanfn_frame_id = db.Column('germanfn_frame_id', db.Integer, ForeignKey('germanfn.id'))
    germanfn_ME = db.Column('germanfn_match_evaluation', db.Text)
    spanishfn_frame_id = db.Column('spanishfn_frame_id', db.Integer, ForeignKey('spanishfn.id'))
    spanishfn_ME = db.Column('spanishfn_match_evaluation', db.Text)

class MultilingualFN_LexicalUnits(db.Model):
    __tablename__ = "multilingualfn_lus"

    id = db.Column('lu_id', db.Integer, primary_key=True)
    lu = db.Column('lu', db.Text)
    language = db.Column('language', db.Text)

    swefn_lu_id = db.Column('swefn_lu_id', db.Integer)
    gfol_lu_id = db.Column('gfol_lu_id', db.Integer)
    dicoenviro_lu_id = db.Column('dicoenviro_lu_id', db.Integer)
    dicoinfo_lu_id = db.Column('dicoinfo_lu_id', db.Integer)
    germanfn_lu_id = db.Column('germanfn_lu_id', db.Integer)
    brasilfn_lu_id = db.Column('brasilfn_lu_id', db.Integer)
    spanishfn_lu_id = db.Column('spanishfn_lu_id', db.Integer)
    bfn_lu_id = db.Column('bfn_lu_id', db.Integer)


class Multi_Frame_Lus(db.Model):
    __tablename__ = "multi_frame_lus"

    id = db.Column('id', db.Integer, primary_key=True)
    frame = db.Column('FrameName', db.Text)
    english = db.Column('English', db.Text)
    french = db.Column('French', db.Text)
    german = db.Column('German', db.Text)
    spanish = db.Column('Spanish', db.Text)
    portuguese = db.Column('Portuguese', db.Text)
    arabic = db.Column('Arabic', db.Text)
    chinese = db.Column('Chinese', db.Text)
    swedish = db.Column('Swedish', db.Text)
