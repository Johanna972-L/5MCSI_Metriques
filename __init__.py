from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from collections import Counter
import sqlite3, requests
                                                                                                                                       
app = Flask(__name__)                                                                                                                  

@app.route('/')
def hello_word():
  return render_template('hello.html')
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
  return render_template("histogramme.html")

@app.route('/commits_data/')
def commits_data():
    try:
        # URL de l'API GitHub pour obtenir les commits
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        commits_data = response.json()

        # Extraire les dates des commits et convertir en minutes
        commit_times = [commit['commit']['author']['date'] for commit in commits_data]
        minutes = [datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M') for date in commit_times]

        # Compter les occurrences de chaque minute
        minute_counts = Counter(minutes)
        
        # Convertir les données en format utilisable pour Google Charts
        data = [{'minute': minute, 'count': count} for minute, count in minute_counts.items()]
        return jsonify(data)
    
    except requests.RequestException as e:
        return jsonify({'error': 'Erreur de connexion à l\'API GitHub', 'details': str(e)}), 502
    except Exception as e:
        return jsonify({'error': 'Erreur lors du traitement des données', 'details': str(e)}), 500

def commits-page():
  return render_template("commits.html")
  
if __name__ == "__main__":
  app.run(debug=True)
