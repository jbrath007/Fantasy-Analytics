import { useState } from "react";

function PlayerSearch() 
{
    const [playerId, setPlayerId] = useState("");
    const [stats, setStats] = useState(null);

const fetchStats = () => 
{
    fetch(`http://localhost:5000/player/${playerId}`)
        .then(res => res.json())
        //.then(data => setStats(data))
        .then(data => {
            console.log(data);
            setStats(data);

        })
        .catch(err => console.error(err));
};

return(
  <div style={{ padding: "30px"}}>
	  <h2>Player Search app</h2>
	
	  <input
	     placeholder="Enter Player Name:"
       onChange = {e => setPlayerId(e.target.value)}
    />

    <button onClick={fetchStats}>Search For Player</button>

      {stats && !stats.error && !stats.error &&(
        <div style={{ marginTop: "30px", padding:"20px"}}>
          <p>
            <strong>Name:</strong> {stats.name}{" "}
            <strong>Position:</strong> {stats.position}
          </p>
          <p><strong>Team:</strong> {stats.team} </p>

          <h2>Player Stats</h2>
          {Object.entries(stats.stats).map(([key, value])=> (
            <p key={key}>
              {key}: {value}
            </p>
          ))}

          <p><strong>Fantasy Points:</strong> {stats.fantasy_points}</p>
        </div>
      )}
  </div>
);

}
export default PlayerSearch;