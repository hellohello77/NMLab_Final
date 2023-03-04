import axios from "axios";

const errorHandling = (error) => {
  // if (error.response.status === 403) window.location.replace("/");
  console.log(error);
};

export const FaceAPI = {
  getCurrentFace: () =>
    axios.get(`/api/getCurrentFace`).catch((error) => errorHandling(error)),
  updateOwner: (formData) =>
    axios.post('/api/updateOwner', formData).catch((error) => errorHandling(error)),
  getAllWeird: () =>
    axios.get(`/api/getWeird`).catch((error) => errorHandling(error)),
};

export const PositionAPI = {
  getLocation: () =>
    axios.get(`/api/getLocation`).catch((error) => errorHandling(error)),
  resetDistance: () => 
    axios.post('/api/resetDistance').catch((error) => errorHandling(error)),
}