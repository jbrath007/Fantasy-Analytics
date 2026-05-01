import { Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import PlayerSearch from "./PlayerSearch";

function App()
{
  return (
    <div>
      {/*Navigation */}
      <nav style={{ marginBottom: "20px" }}>
        <Link to="/">Home</Link> |{" "}
        <Link to="/search">Player Search</Link>
      </nav>

      {/* ROutes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<PlayerSearch />} />
      </Routes>
    </div>
  );
}

export default App;