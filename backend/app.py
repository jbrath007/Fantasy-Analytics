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
                "Passing Yards": player["Passing Yards"],
                "Passing Touchdowns": player["Passing Touchdowns"],
                "Completions": player["Completions"],
                "Interceptions": player["Interceptions"],
                "Rush Attempts": player["Rush Attempts"],
                "Rushing Yards": player["Rushing Yards"],
                "Rushing Touchdowns": player["Rushing Touchdowns"],
                "Fumbles": player["Fumbles"]
            },
            "fantasy_points": player["Fantasy Points"]  
        })
    
    elif not rb.empty:
        player = rb.iloc[0] 
        return jsonify({
            "name": player["full_name"],
            "position": player["position"],
            "team": player["team"],
            "stats":{
                "Rush Attempts": player["Rush Attempts"],
                "Rushing Yards": player["Rushing Yards"],
                "Rushing Touchdowns": player["Rushing Touchdowns"],
                "Targets": player["Targets"],
                "Receptions": player["Receptions"],
                "Receiving Yards": player["Receiving Yards"],
                "Yards After Catch": player["Yards After Catch"],
                "Receiving Touchdowns": player["Receiving Touchdowns"]
            },
            "fantasy_points": player["Fantasy Points"]  
        })
    
    elif not wr.empty or not te.empty:
        player = (wr if not wr.empty else te).iloc[0] 
        return jsonify({
            "name": player["full_name"],
            "position": player["position"],
            "team": player["team"],
            "stats":{
                "Rush Attempts": player["Rush Attempts"],
                "Rushing Yards": player["Rushing Yards"],
                "Rushing Touchdowns": player["Rushing Touchdowns"],
                "Fumble": player["Fumbles"],
                "Targets": player["Targets"],
                "Receptions": player["Receptions"],
                "Receiving Yards": player["Receiving Yards"],
                "Yards After Catch": player["Yards After Catch"],
                "Receiving Touchdowns": player["Receiving Touchdowns"]
            },
            "fantasy_points": player["Fantasy Points"]  
        })

    return jsonify({"Error": "Player Not Found!"})

if __name__ == "__main__":
    app.run(debug=True)