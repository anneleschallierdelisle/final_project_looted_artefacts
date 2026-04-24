from flask import Flask, jsonify, request, render_template
import pymysql
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

def get_db_connection():

    load_dotenv()
    username = os.getenv('db_username')
    password = os.getenv('db_password')

    try:
        connection = pymysql.connect(
            host='localhost',
            user=username,
            password=password,
            database='new_yemen_looted_artefacts',              
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>API Documentation of the Yemeni Looted Artefacts database</title>
        <style>
            body {
                background-color: #f5efeb;
                font-family: Consolas, monospace;
            }
        </style>
    </head>
    <body>
        <h1 style="color:825000">API Documentation of the Yemeni Looted Artefacts database</h1>           
        <p>Please read information below to get data</code></p>
        <p>Base URL: <code>http://127.0.0.1:5000/</code></p>
        <p>Data sources:</p>
            <p><a href="https://goam.gov.ye/Looted" target="_blank" style="color:#825000;">
                List of looted antiquities of the general Authority for Antiquities and Museums of Yemen</a></p> 
                
            <p><a href="https://whc.unesco.org/en/list/" target="_blank" style="color:#825000;">
                UNESCO World Heritage Sites
            </a></p>
        </p>
    
        <h2 style="color:#777777">Endpoints</h2>
        <ul>
            <li><strong>GET /yemeni_looted_artefacts</strong> : list and detailed descriptions of yemeni looted artefacts (pagination: limit, offset)</li>
            <li><strong>GET /yemeni_looted_artefacts/&lt;artifact_id&gt;</strong> : get one artefact by ID</li>
            <li><strong>GET /artefacts_scoring</strong> : list of artefact scoring, compare descriptions and images' artifacts between both sources (national authority and art_dealer) (pagination)</li>
            <li><strong>GET /search_looted_artefacts</strong> : search yemeni looted artefacts with filters (country, normalized_domain)</li>
            <li><strong>GET /unesco_sites_in_danger/&lt;states_name_en&gt;</strong> : get information for one country with unesco sites, more especially in danger</li>
        </ul>
    
        <h2 style="color:#777777">Pagination</h2>
        <p>limit: number of records returned</p>  
        <p>offset: starting point in the dataset</p>
        <li>/yemeni_looted_artefacts?limit=10&offset=0</li>
        
        <h2 style="color:#825000">Filtrering - see examples below</h2>
        <ul>
          <li>/yemeni_looted_artefacts?limit=10&offset=0</li>
          <li>/yemeni_looted_artefacts/0-25_p036_bea25d9f</li>
          <li>/search_looted_artefacts?country=UK&normalized_domain=christies.com</li>
          <li>/unesco_sites_in_danger/Yemen</li>
        </ul>   
    </body>
    </html>
    """
    
# single endpoint looted artefact_id
@app.route("/yemeni_looted_artefacts/<artifact_id>", methods=["GET"])
def get_one_looted_artefact(artifact_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database."}), 500

    query = """
        SELECT artifact_id, type, detail, material, iconography, 
               period_precise, pdf_name, page_num
        FROM looted_artefacts
        WHERE artifact_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (artifact_id,))
        artefact = cursor.fetchone()

    connection.close()

    # if artifact_id does not exist
    if not artefact:
        return jsonify({"error": "Artifact not found"}), 404

    return jsonify({
        "success": True,
        "result": artefact
    })

# list endpoint looted_artefacts
@app.route("/yemeni_looted_artefacts", methods=["GET"])
def get_looted_artefacts():
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    # offset = (page - 1) * limit
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database."}), 500

    query = """
    SELECT 
    artifact_id, type, detail, material, iconography, period_precise, pdf_name, page_num FROM looted_artefacts 
    LIMIT %s OFFSET %s
    """

    params = [limit, offset]
    
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        looted_artefacts = cursor.fetchall()

    connection.close()
    return jsonify({
        "success": True,
        "limit": limit,
        "offset": offset,
        "count": len(looted_artefacts),
        "results": looted_artefacts
    })


# single endpoint unesco country
@app.route("/unesco_sites_in_danger/<states_name_en>", methods=["GET"])
def get_one_unesco_country(states_name_en):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database."}), 500

    query = """
        SELECT states_name_en, no_danger, yes_danger, percent_danger, `rank`
        FROM unesco_sites_in_danger
        WHERE states_name_en = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (states_name_en,))
        country = cursor.fetchone()

    connection.close()

    # if country not found
    if not country:
        return jsonify({"error": "Mispelling country, please refer to UNESCO website"}), 404

    return jsonify({
        "success": True,
        "result": country
    })

    

# list endpoint artefacts scoring
@app.route("/artefacts_scoring", methods=["GET"])
def get_artefacts_scoring():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database."}), 500

    query = "SELECT artifact_id, score_txt, score_img, pdf_upgrd_description, wb_txt_lg, link, pdf_name, page_num FROM artefacts_scoring LIMIT %s OFFSET %s"

    params = [limit, offset]
    
    with connection.cursor() as cursor:

        cursor.execute(query, params)
        artefacts_scoring = cursor.fetchall()

    connection.close()
    return jsonify({
        "success": True,
        "limit": limit,
        "offset": offset,
        "count": len(artefacts_scoring),
        "results": artefacts_scoring
    })


@app.route("/search_looted_artefacts", methods=["GET"])
def search_looted_artefacts():
    
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    
    main_website = request.args.get("normalized_domain")
    country = request.args.get("country")

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database."}), 500

    query = """
        SELECT artifact_id, link, normalized_domain, country
        FROM looted_identified_artefacts WHERE 1=1
    """
    params = [] #no fill because we append them then

    if main_website:
        query += " AND normalized_domain LIKE %s"
        params.append(f"%{main_website}%")

    if country:
        query += " AND country = %s"
        params.append(country)
    
    #pagination
    query += " LIMIT %s OFFSET %s" #don't forget to add a space before LIMIT
    params.append(limit)
    params.append(offset)


    with connection.cursor() as cursor:
        cursor.execute(query, params)
        looted_identified_artefacts = cursor.fetchall()

    connection.close()
    return jsonify({
        "success": True,
        "limit": limit,
        "offset": offset,
        "main_website": main_website,
        "country": country,
        "count": len(looted_identified_artefacts),
        "results": looted_identified_artefacts
    })
    
if __name__ == "__main__":
    app.run(debug=True)
