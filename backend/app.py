"""Making the data an app """
from flask import Flask, jsonify
from flask_cors import CORS
#from data import data_frame_stats
from data import qb_stats
from data import rb_stats
from data import wr_stats
from data import te_stats

app = Flask(__name__)
CORS(app)

@app.route("/player/<name>")
def get_player(name):
    #player = data_frame_stats[data_frame_stats["full_name"].str.upper() == player_name.upper()]
    qb = qb_stats[qb_stats["full_name"].str.lower() == name.lower()]
    rb = rb_stats[rb_stats["full_name"].str.lower() == name.lower()]
    wr = wr_stats[wr_stats["full_name"].str.lower() == name.lower()]
    te = te_stats[te_stats["full_name"].str.lower() == name.lower()]

    if not qb.empty:
        player = qb.iloc[0] 
        return jsonify({
            "name": player["full_name"],
            "position": player["position"],
            "team": player["team"],
            "stats":{
                "pass_yards": player["pass_yards"],
                "pass_td": player["pass_td"],
                "completions": player["completions"],
                "ints": player["ints"],
                "Rush Attempts": player["rush_attempt"],
                "rush_yards": player["rush_yards"],
                "rush_yards": player["rush_yards"],
                "rush_td": player["rush_td"],
                "Fumble": player["fumble"]
            },
            "fantasy_points": player["fantasy_points"]  
        })
    
    elif not rb.empty:
        player = rb.iloc[0] 
        return jsonify({
            "name": player["full_name"],
            "position": player["position"],
            "team": player["team"],
            "stats":{
                "Rush Attempts": player["rush_attempt"],
                "rush_yards": player["rush_yards"],
                "rush_td": player["rush_td"],
                "Targets": player["targets"],
                "rec": player["rec"],
                "rec_yards": player["rec_yards"],
                "rec_td": player["rec_td"]
            },
            "fantasy_points": player["fantasy_points"]  
        })
    
    elif not wr.empty or not te.empty:
        player = (wr if not wr.empty else te).iloc[0] 
        return jsonify({
            "name": player["full_name"],
            "position": player["position"],
            "team": player["team"],
            "stats":{
                "Rush Attempts": player["rush_attempt"],
                "rush_yards": player["rush_yards"],
                "rush_td": player["rush_td"],
                "Fumble": player["fumble"],
                "Targets": player["targets"],
                "rec": player["rec"],
                "rec_yards": player["rec_yards"],
                "rec_td": player["rec_td"]
            },
            "fantasy_points": player["fantasy_points"]  
        })

    return jsonify({"Error": "Player Not Found!"})

if __name__ == "__main__":
    app.run(debug=True)