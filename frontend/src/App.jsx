import { Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import PlayerSearch from "./PlayerSearch";

function App()
{
  return (
    <div>
      {/*Navigation */}
      <nav id="destop-nav"> 
        <div>
          <ul class="nav-links">
            <div class="menu-links">
              <Link to="/">Home</Link> |{" "}
              <Link to="/search">Player Search</Link>
            </div>
          </ul>
        </div>
        
      </nav>

      {/* Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<PlayerSearch />} />
      </Routes>
    </div>
  );
}

export default App;