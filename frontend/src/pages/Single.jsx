import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { StarWarsImage } from "../components/StarWarsImage";
import useGlobalReducer from "../hooks/useGlobalReducer";
import { databankDescriptions } from "../data/databankDescriptions";
import { categoryLabels } from "../data/categories";
import { addFavorite, getEntity, removeFavorite } from "../api";

const infoTitles = {
  people: "Detalles",
  planets: "Detalles",
  vehicles: "Detalles"
};

const hiddenFields = new Set(["created", "edited", "url"]);

const fieldLabels = {
  birth_year: "Nacimiento",
  climate: "Clima",
  crew: "Tripulación",
  diameter: "Diámetro",
  eye_color: "Color de ojos",
  gender: "Género",
  hair_color: "Color de pelo",
  height: "Altura",
  manufacturer: "Fabricante",
  model: "Modelo",
  name: "Nombre",
  passengers: "Pasajeros",
  population: "Población",
  terrain: "Terreno",
  vehicle_class: "Clase"
};

const formatLabel = (key) => {
  return fieldLabels[key] || key.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
};

const renderValue = (value) => {
  if (Array.isArray(value)) {
    return value.length ? value.join(", ") : "Sin registros";
  }

  return value || "Desconocido";
};

export const Single = () => {
  const { type, uid } = useParams();
  const { store, dispatch } = useGlobalReducer();
  const [entity, setEntity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEntity = async () => {
      setLoading(true);
      setError(null);

      try {
        if (!Object.keys(categoryLabels).includes(type)) {
          throw new Error("Tipo de recurso no válido.");
        }

        const data = await getEntity(type, uid);
        setEntity(data);
      } catch (currentError) {
        setError(currentError.message);
      } finally {
        setLoading(false);
      }
    };

    fetchEntity();
  }, [type, uid]);

  const properties = entity?.properties || {};
  const name = properties.name || entity?.name || "Detalle";
  const description = databankDescriptions[`${type}-${uid}`] || entity?.description;
  const isFavorite = store.favorites.some(
    (favorite) => String(favorite.uid) === String(uid) && favorite.type === type
  );

  const handleFavorite = async () => {
    dispatch({ type: "set_error", payload: null });

    try {
      if (isFavorite) {
        await removeFavorite(type, uid);
        dispatch({ type: "remove_favorite", payload: { uid, type } });
      } else {
        const favorite = await addFavorite(type, uid);
        dispatch({ type: "add_favorite", payload: favorite });
      }
    } catch (currentError) {
      dispatch({ type: "set_error", payload: currentError.message });
    }
  };

  return (
    <main className="detail-page">
      <div className="container py-4">
        <div className="detail-actions">
          <Link to="/" className="btn btn-outline-light">
            Volver al inicio
          </Link>
        </div>

        {loading && (
          <div className="alert alert-info" role="status">
            Cargando detalle...
          </div>
        )}

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        {entity && (
          <div className="detail-shell">
            <div className="detail-media-column">
              <StarWarsImage
                type={type}
                uid={uid}
                className="img-fluid detail-image"
                alt={name}
                fallbackClassName="detail-image"
              />
            </div>
            <div className="detail-info-column">
              <div className="detail-header">
                <div>
                  <span className="badge text-bg-warning text-dark mb-3">{categoryLabels[type]}</span>
                  <h1>{name}</h1>
                </div>
                <button
                  className="btn btn-lg btn-warning detail-favorite-button"
                  type="button"
                  onClick={handleFavorite}
                >
                  {isFavorite ? "Quitar de favoritos" : "Agregar a favoritos"}
                </button>
                <p className="detail-description">{description}</p>
              </div>

              <div className="databank-details">
                <h2>{infoTitles[type]}</h2>
                <div className="databank-detail-list">
                  {Object.entries(properties)
                    .filter(([key]) => !hiddenFields.has(key))
                    .map(([key, value]) => (
                      <div className="databank-detail-item" key={key}>
                        <div className="databank-detail-label">{formatLabel(key)}</div>
                        <div className="databank-detail-value">{renderValue(value)}</div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};
