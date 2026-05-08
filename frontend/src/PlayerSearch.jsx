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
  <section id="stat-page">
    <div>
      <div class="info__container">
        
        <h2 class="header">Player Search app</h2>
        
        <div class="query_container">
          <div class="message-container">
            <input class="message" placeholder="Enter Player Name:"
            onChange = {e => setPlayerId(e.target.value)}/>
          </div>
          
          <div class="btn-container">
            <button class="btn" alt="search button" onClick={fetchStats}>Search For Player</button>
          </div>
          <div class="stat-container">
            <div class="stat__section">
               {stats && !stats.error && !stats.error &&(
                <div>
                  <p class="name_position">
                    <strong>Name:</strong> {stats.name}
                  </p>
                  <p>
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
          </div>
        </div>
      </div>
    </div>
  </section>
  
);

}
export default PlayerSearch;