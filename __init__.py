from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from collections import Counter
import sqlite3
                                                                                                                                       
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

@app.route('/commits/')
def commits():
    # URL de l'API GitHub pour obtenir les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Effectuer la requête GET
    response = requests.get(url)
    data = response.json()
    
    # Traitement des données
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    dates = [datetime.strptime(commit['commit']['author']['date'], datetime_format).replace(tzinfo=pytz.UTC) for commit in data]
    counter = Counter([date.strftime("%Y-%m-%d %H:%M") for date in dates])
    
    # Préparer les données pour le graphique
    minutes = list(counter.keys())
    commit_counts = list(counter.values())
    
    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(minutes, commit_counts, marker='o')
    plt.xlabel('Minute')
    plt.ylabel('Nombre de Commits')
    plt.title('Nombre de Commits par Minute')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Sauvegarder le graphique
    file_path = 'static/commits_per_minute.png'
    plt.savefig(file_path)
    plt.close()
    
    return send_file(file_path, mimetype='image/png')
  
if __name__ == "__main__":
  app.run(debug=True)
