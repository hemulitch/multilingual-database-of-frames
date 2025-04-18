from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
from models import db, BFN, BFN_Relationship, RelationTypes, BFN_LexicalUnits, BrasilFN,  BrasilFN_LexicalUnits, DiCoEnviro, DiCoEnviro_LexicalUnits, DiCoInfo, DiCoInfo_LexicalUnits, GermanFN, GermanFN_LexicalUnits, GFOL, GFOL_LexicalUnits, SpanishFN, SpanishFN_LexicalUnits, SweFN, SweFN_LexicalUnits, MultilingualFN, MultilingualFN_LexicalUnits, Multi_Frame_Lus, Lus_to_frame
from sqlalchemy import or_
import pandas as pd
import networkx as nx

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'MultilingualFramenet.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# def create_graph(path):
#     df = pd.read_csv(path)
#     G = nx.Graph()
#     for _, row in df.iterrows():
#         node1, node2, connection_type = row['super'], row['sub'], row['type']
#         G.add_edge(node1, node2, type=connection_type)

#     return G

def find_related_frames(frame_id, depth):
    if depth == 0:
        return []
    
    relations = BFN_Relationship.query.filter(
        (BFN_Relationship.parent_id == frame_id) | (BFN_Relationship.child_id == frame_id)
    ).all()

    related_frames = []
    
    for relation in relations:
        related_frame_id = (
            relation.child_id if relation.parent_id == frame_id else relation.parent_id
        )
        related_frame = BFN.query.get(related_frame_id)
        relation_type = relation.relationship_to_types.relation_type if relation.relationship_to_types else "Unknown"

        if related_frame:
            related_frames.append({
                "frame_id": related_frame.id,
                "frame_name": related_frame.frame,
                "relation_id": relation.relation_id,
                "relation_type": relation_type,
            })
            # Recursive call for the next level
            related_frames += find_related_frames(related_frame.id, depth - 1)
    
    return related_frames

def relation_color_map(relation_type):
    """Map relation types to colors."""
    color_map = {
        "Using": "blue",
        "Inheritance": "red",
        "Subframe": "green",
        "Perspective_on": "black",
        "Causative_of": "yellow",
        "Inchoative_of":"brown",
        "Metaphor":"purple"
    }
    return color_map.get(relation_type, "gray")  

@app.route('/graph3_menu', methods=['GET', 'POST'])
def graph3_menu(): 
    frames = BFN.query.with_entities(BFN.id, BFN.frame).all() 
    if request.method == 'POST':
        frame_id = int(request.form['frame_id']) 
        frame = BFN.query.get(frame_id)
        if frame:
            related_frames = find_related_frames(frame.id, depth=3)
            nodes = {frame.id: {"id": frame.id, "name": frame.frame}}
            edges = set()
            for rf in related_frames:
                if rf["frame_id"] not in nodes:
                    nodes[rf["frame_id"]] = {"id": rf["frame_id"], "name": rf["frame_name"]}

                if frame_id != rf["frame_id"]:
                        edges.add((
                            frame_id,
                            rf["frame_id"],
                            rf["relation_type"],
                            relation_color_map(rf["relation_type"]),
                        ))
            edges_list = [
                {"source": edge[0], "target": edge[1], "relation": edge[2], "color": edge[3]}
                for edge in edges
            ]  
            for edge in edges_list:
                if edge["source"] not in nodes:
                    source_frame = BFN.query.get(edge["source"])
                    nodes[edge["source"]] = {"id": source_frame.id, "name": source_frame.frame}
                if edge["target"] not in nodes:
                    target_frame = BFN.query.get(edge["target"])
                    nodes[edge["target"]] = {"id": target_frame.id, "name": target_frame.frame}

            graph_data = {"nodes": list(nodes.values()), "edges": edges_list}
            print(edges)
            return render_template('graph3_results.html', frame_name=frame.frame, graph_data=graph_data)
    return render_template('/graph3_menu.html', frames=frames)
    
def join_lus(frame):
  ''' Getting a full list of lexical units from all languages'''
  fr = Multi_Frame_Lus.query.filter(Multi_Frame_Lus.frame==frame).all()[0]
  langs = [fr.english, fr.arabic, fr.chinese, fr.french, fr.german, fr.swedish, fr.portuguese]

  lus = []
  for lang in langs:
    if lang != None:
      for lu in lang.split(', '):
        lus.append(lu)
  return lus

def connected_by_lus(frame):
  '''Getting a dict of frames and their lexical units'''
  fr = Multi_Frame_Lus.query.filter(Multi_Frame_Lus.frame==frame).all()[0]
  langs = [fr.english, fr.arabic, fr.chinese, fr.french, fr.german, fr.swedish, fr.portuguese]

  lus = []
  for lang in langs:
    if lang != None:
      for lu in lang.split(', '):
        lus.append(lu)

  connected_frames = []
  for lu in lus:
    frames = Lus_to_frame.query.filter(Lus_to_frame.lus_name==lu).all()
    if len(frames) >0:
      for frame in frames[0].frames.split(', '):
        cfs = Multi_Frame_Lus.query.filter(Multi_Frame_Lus.frame == frame).all()
        for cf in cfs:
          connected_frames.append({
            "frame_id": cf.id,
            "frame_name": cf.frame,
            "frame_lus": join_lus(cf.frame)
          })

  return connected_frames

def matches(node1, node2):
    matched_lus = []
    for lu in nodes[node1][2]:
        if lu in nodes[node2][2]:
            matched_lus.append(lu)
    return(matched_lus)
    
@app.route('/graph2_menu', methods=['GET', 'POST'])    
def graph2_menu():
    frames = Multi_Frame_Lus.query.with_entities(Multi_Frame_Lus.id, Multi_Frame_Lus.frame).all()
    if request.method == 'POST':
        frame_id = int(request.form['frame_id'])
        frame = Multi_Frame_Lus.query.get(frame_id)
        if frame:
            connected_frames = connected_by_lus(frame.frame)
            nodes = {}
            edges = []
            for cf in connected_frames:
              if cf['frame_id'] not in nodes:
                    nodes[cf["frame_id"]] = (cf["frame_id"], cf["frame_name"], cf['frame_lus'])

            for node1 in nodes:
              for node2 in nodes:

                if node1 != node2 and len(matched_lus)>0:
                    edges.append((
                      nodes[node1][0],
                      nodes[node2][0],
                      matches(node1, node2)

                  ))

            edges_list = [
                {"node1": edge[0], "node2": edge[1], "connection": edge[2]}
                for edge in edges
            ]
            graph_data = {"nodes": list(nodes.values()), "edges": edges_list}
            print(edges)
            return render_template('graph2_results.html', frame_name=frame.frame, graph_data=graph_data)
    return render_template('/graph2_menu.html', frames=frames)

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data')
def data(): 
    return render_template('data.html')

@app.route('/graphs')
def graphs_main_page(): 
    return render_template('graphs.html')

@app.route('/graph_framenets')
def graphs_framenets():
    return render_template('graph_framenets.html')

@app.route('/lexical_units')
def lexical_units():
    search_query = request.args.get('search', '')
    language_filter = request.args.get('language', '')
    page = request.args.get('page', 1, type=int)

    # Query to filter by search term and language
    query = MultilingualFN_LexicalUnits.query

    if search_query:
        query = query.filter(MultilingualFN_LexicalUnits.lu.contains(search_query))

    if language_filter:
        query = query.filter(MultilingualFN_LexicalUnits.language == language_filter)

    # Apply pagination
    pagination = query.paginate(page=page, per_page=200, error_out=False)

    return render_template('lexical_units.html', lexical_units=pagination.items, pagination=pagination)

@app.route('/lexical_units/<int:lu_id>')
def lexical_unit_detail(lu_id):

    lu = MultilingualFN_LexicalUnits.query.get_or_404(lu_id)

    related_frames = {'BFN': [], 'BrasilFN': [], 'GermanFN': [], 'GFOL': [],
                      'SpanishFN': [], 'DiCoEnviro': [], 'DiCoInfo': [],
                      'SweFN': []}

    brasilfn_associated_ids_str = lu.brasilfn_lu_id
    if brasilfn_associated_ids_str:
        brasilfn_associated_ids = brasilfn_associated_ids_str.split()
        for id_str in brasilfn_associated_ids:
            brasilfn_lu_id = int(id_str.split('.')[0])
            related_frame = BrasilFN_LexicalUnits.query.get(brasilfn_lu_id)

            if related_frame:
                frame_info = BrasilFN.query.get(related_frame.frame_id)
                multilingual_entry = MultilingualFN.query.filter_by(brasilfn_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['BrasilFN'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    bfn_associated_ids_str = lu.bfn_lu_id
    if bfn_associated_ids_str:
        bfn_associated_ids = bfn_associated_ids_str.split()
        for id_str in bfn_associated_ids:
            bfn_lu_id = int(id_str.split('.')[0])
            related_frame = BFN_LexicalUnits.query.get(bfn_lu_id)

            if related_frame:
                frame_info = BFN.query.get(related_frame.frame_id)
                multilingual_entry = MultilingualFN.query.filter_by(bfn_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['BFN'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    germanfn_associated_ids_str = lu.germanfn_lu_id
    if germanfn_associated_ids_str:
        germanfn_associated_ids = germanfn_associated_ids_str.split()
        for id_str in germanfn_associated_ids:
            germanfn_lu_id = int(id_str.split('.')[0])
            related_frame = GermanFN_LexicalUnits.query.get(germanfn_lu_id)

            if related_frame:
                frame_info = GermanFN.query.get(related_frame.frame_id)

                multilingual_entry = MultilingualFN.query.filter_by(germanfn_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['GermanFN'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    
    gfol_associated_ids_str = lu.gfol_lu_id
    if gfol_associated_ids_str:
        gfol_associated_ids = gfol_associated_ids_str.split()
        for id_str in gfol_associated_ids:
            gfol_lu_id = int(id_str.split('.')[0])
            related_frame = GFOL_LexicalUnits.query.get(gfol_lu_id)

            if related_frame:
                frame_info = GFOL.query.get(related_frame.frame_id)
                multilingual_entry = MultilingualFN.query.filter_by(gfol_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['GFOL'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    spanishfn_associated_ids_str = lu.spanishfn_lu_id
    if spanishfn_associated_ids_str:
        spanishfn_associated_ids = spanishfn_associated_ids_str.split()
        for id_str in spanishfn_associated_ids:
            spanishfn_lu_id = int(id_str.split('.')[0])
            related_frame = SpanishFN_LexicalUnits.query.get(spanishfn_lu_id)

            if related_frame:
                frame_info = SpanishFN.query.get(related_frame.frame_id)
                multilingual_entry = MultilingualFN.query.filter_by(spanish_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['SpanishFN'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })
    
    dicoenviro_associated_ids_str = lu.dicoenviro_lu_id
    if dicoenviro_associated_ids_str:
        dicoenviro_associated_ids = dicoenviro_associated_ids_str.split()
        for id_str in dicoenviro_associated_ids:
            dicoenviro_lu_id = int(id_str.split('.')[0])
            related_frame = DiCoEnviro_LexicalUnits.query.get(dicoenviro_lu_id)

            if related_frame:
                frame_info = DiCoEnviro.query.get(related_frame.frame_id)

                multilingual_entry = MultilingualFN.query.filter_by(dicoenviro_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['DiCoEnviro'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    dicoinfo_associated_ids_str = lu.dicoinfo_lu_id
    if dicoinfo_associated_ids_str:
        dicoinfo_associated_ids = dicoinfo_associated_ids_str.split()
        for id_str in dicoinfo_associated_ids:
            dicoinfo_lu_id = int(id_str.split('.')[0])
            related_frame = DiCoInfo_LexicalUnits.query.get(dicoinfo_lu_id)

            if related_frame:
                frame_info = DiCoInfo.query.get(related_frame.frame_id)
                multilingual_entry = MultilingualFN.query.filter_by(dicoinfo_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['DiCoInfo'].append({
                        'frame_id' : multilingual_entry,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    swefn_associated_ids_str = lu.swefn_lu_id
    if swefn_associated_ids_str:
        swefn_associated_ids = swefn_associated_ids_str.split()
        for id_str in swefn_associated_ids:
            swefn_lu_id = int(id_str.split('.')[0])
            related_frame = SweFN_LexicalUnits.query.get(swefn_lu_id)

            if related_frame:
                frame_info = SweFN.query.get(related_frame.frame_id)
                multilingual_entry = MultilingualFN.query.filter_by(swefn_frame_id=related_frame.frame_id).first()
                multilingual_frame_id = multilingual_entry.id if multilingual_entry else None

                if frame_info:
                    related_frames['SweFN'].append({
                        'frame_id' : multilingual_frame_id,
                        'word': related_frame.word,
                        'pos': related_frame.pos,
                        'frame_name': frame_info.frame
                    })

    return render_template('lexical_unit_detail.html', lu=lu, 
                           related_frames=related_frames)

@app.route('/frames', methods=['GET', 'POST'])
def frames():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    if search_query:
        frames = MultilingualFN.query.filter(
            or_(
                MultilingualFN.frame_name.contains(search_query),
            )
        )
    else:
        frames = MultilingualFN.query
    
    # Apply pagination
    pagination = frames.paginate(page=page, per_page=200, error_out=False)

    return render_template('frames.html', frames=pagination.items, pagination=pagination)

@app.route('/frame/<int:frame_id>', methods=['GET'])
def frame_detail(frame_id):
    frame = MultilingualFN.query.get_or_404(frame_id)
    
    brasilfn = BrasilFN.query.get(frame.brasilfn_frame_id) if frame.brasilfn_frame_id else None
    dicoenviro = DiCoEnviro.query.get(frame.dicoenviro_frame_id) if frame.dicoenviro_frame_id else None
    swefn = SweFN.query.get(frame.swefn_frame_id) if frame.swefn_frame_id else None
    bfn = BFN.query.get(frame.bfn_frame_id) if frame.bfn_frame_id else None
    gfol = GFOL.query.get(frame.gfol_frame_id) if frame.gfol_frame_id else None
    dicoinfo = DiCoInfo.query.get(frame.dicoinfo_frame_id) if frame.dicoinfo_frame_id else None
    germanfn = GermanFN.query.get(frame.germanfn_frame_id) if frame.germanfn_frame_id else None
    spanishfn = SpanishFN.query.get(frame.spanishfn_frame_id) if frame.spanishfn_frame_id else None

    return render_template('frame_detail.html', frame=frame, 
                           swefn=swefn, brasilfn=brasilfn, 
                           dicoenviro=dicoenviro, bfn=bfn, 
                           gfol=gfol, dicoinfo=dicoinfo,
                           germanfn=germanfn, spanishfn=spanishfn)

if __name__ == '__main__':
    app.run(debug=True)
