from flask import Flask, jsonify, request

app = Flask(__name__)

def read_data_file():
    data = []
    try:
        with open('start_from.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) >= 2:
                        item = {
                            'name': parts[0],
                            'district': parts[1],
                            'type': parts[2] if len(parts) > 2 else 'Place'
                        }
                        data.append(item)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
    return data

@app.route('/api/locations', methods=['GET'])
def get_all_locations():
    data = read_data_file()
    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data
    })

@app.route('/api/locations/<search_term>', methods=['GET'])
def search_locations(search_term):
    data = read_data_file()
    search_term = search_term.lower()
    results = [
        loc for loc in data 
        if (search_term in loc['name'].lower() or 
            search_term in loc['district'].lower() or 
            search_term in loc['type'].lower())
    ]
    return jsonify({
        'status': 'success',
        'search_term': search_term,
        'count': len(results),
        'data': results
    })

@app.route('/api/districts/<district_name>', methods=['GET'])
def get_by_district(district_name):
    data = read_data_file()
    district_name = district_name.lower()
    results = [
        loc for loc in data 
        if district_name in loc['district'].lower()
    ]
    return jsonify({
        'status': 'success',
        'district': district_name,
        'count': len(results),
        'data': results
    })

@app.route('/api/types/<location_type>', methods=['GET'])
def get_by_type(location_type):
    data = read_data_file()
    location_type = location_type.lower()
    results = [
        loc for loc in data 
        if location_type in loc['type'].lower()
    ]
    return jsonify({
        'status': 'success',
        'type': location_type,
        'count': len(results),
        'data': results
    })

@app.route('/')
def home():
    return """
    <h1>Location API</h1>
    <p>Try these endpoints:</p>
    <ul>
        <li><a href="/api/locations">All locations</a></li>
        <li><a href="/api/locations/leh">Search 'leh'</a></li>
        <li><a href="/api/districts/leh">District 'leh'</a></li>
        <li><a href="/api/types/city">Type 'city'</a></li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)