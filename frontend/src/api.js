const request = async (url, options = {}) => {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.message || "No se pudo completar la solicitud.");
  }

  return data;
};

const favoriteEndpointTypes = {
  people: "people",
  planets: "planet",
  vehicles: "vehicle"
};

export const getPeople = () => request("/people");

export const getPlanets = () => request("/planets");

export const getVehicles = () => request("/vehicles");

export const getEntity = (type, uid) => request(`/${type}/${uid}`);

export const getFavorites = () => request("/users/favorites");

export const addFavorite = (type, uid) => {
  return request(`/favorite/${favoriteEndpointTypes[type]}/${uid}`, { method: "POST" });
};

export const removeFavorite = (type, uid) => {
  return request(`/favorite/${favoriteEndpointTypes[type]}/${uid}`, { method: "DELETE" });
};
