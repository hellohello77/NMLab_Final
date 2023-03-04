// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

import {PositionAPI} from "../api.js"

mapboxgl.accessToken =
  "pk.eyJ1IjoibWVjb2xpMTIxOSIsImEiOiJjbDN5a2czbXkwMG1zM2tzNGxnbDB1Y3J0In0.HUc61PMJdrk1aF2i2E9x4Q";

class Map {
  constructor(ref) {
    this.navigating = false;
    this.container = ref;
    this.map = new mapboxgl.Map({
      container: this.container,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [121.54373533333333, 25.0190466666666684],
      zoom: 16
    });
    this.marker = new mapboxgl.Marker()
      .setLngLat([121.54373533333333, 25.0190466666666684])
      .addTo(this.map);
  }

  updateMarkerLocation(setTime, setDistance) {
    PositionAPI.getLocation().then((response) => {
      if (response) {
        const { coordinates, distance } = response.data;
        this.marker.setLngLat(coordinates);
        const current = new Date().toString()
        setTime(current);
        setDistance(distance);
      }
    }).catch(()=>{});
  }
}

export default Map;
