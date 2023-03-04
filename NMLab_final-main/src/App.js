import React, {useState} from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import MapContainer from "./components/MapContainer";
import FaceContainer from "./components/FaceContainer";
import LoginContainer from "./components/LoginContainer";
import Navigator from "./Navigator.js";

const App = () => {
  const [login, setLogin] = useState(false);
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/app/" element={<Navigator login={login} setLogin={setLogin} />} >
            <Route path="map" element={<MapContainer />} />
            <Route path="face" element={<FaceContainer />} />
            {/* <Route path="voice" element={<VoiceContainer />} /> */}
            <Route
              path="*"
              element={
                <div>
                  <h2>404 Page not found</h2>
                </div>
              }
            />
          </Route>
          <Route path="/login" element={<LoginContainer login={login} setLogin={setLogin}/>} />
          <Route
            path="*"
            element={
              <Navigate to="/app" replace={true}/>
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
