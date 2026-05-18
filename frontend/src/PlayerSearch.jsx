import { useState } from "react";

function PlayerSearch() 
{
    const [playerId, setPlayerId] = useState("");
    const [stats, setStats] = useState(null);
    const [isSectionVisible, setIsSectionVisible] = useState(false);

const fetchStats = () => 
{
    fetch(`http://localhost:5000/player/${playerId}`)
        .then(res => res.json())
        .then(data => {
            console.log(data);

            setStats(data);
            setIsSectionVisible(true);
        })
        //show stat section after the button is pressed
        .catch(err => console.error(err));
};

//reseting the page
const resetPage = () =>
{
  setPlayerId("");
  setStats(null);
  setIsSectionVisible(false);
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
          
          <div className="btn-container">
            <button class="btn btn-color1" alt="search button" onClick={fetchStats}>Search For Player</button>
            <button class="btn btn-color2" alt="reset button" onClick={resetPage}>Reset</button>
          </div>

          <div className="stat-container">
            {isSectionVisible && (
              <div className="stat__section">
                {stats && !stats.error ? (
                  <div id="stats">
                    <p className="name_position">
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
                ) : (
                  <p>Player not found!</p>
                  )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  </section>
  
);

}
export default PlayerSearch;