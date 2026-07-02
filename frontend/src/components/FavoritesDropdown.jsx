import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { removeFavorite } from "../api";
import { categoryLabels } from "../data/categories";

export const FavoritesDropdown = ({ favorites, dispatch }) => {
  const [isFavoritesOpen, setIsFavoritesOpen] = useState(false);
  const favoritesDropdownRef = useRef(null);

  useEffect(() => {
    const closeFavoritesOnOutsideClick = (event) => {
      if (!favoritesDropdownRef.current?.contains(event.target)) {
        setIsFavoritesOpen(false);
      }
    };

    document.addEventListener("mousedown", closeFavoritesOnOutsideClick);

    return () => {
      document.removeEventListener("mousedown", closeFavoritesOnOutsideClick);
    };
  }, []);

  const handleRemoveFavorite = async (favorite) => {
    dispatch({ type: "set_error", payload: null });

    try {
      await removeFavorite(favorite.type, favorite.uid);
      dispatch({
        type: "remove_favorite",
        payload: { uid: favorite.uid, type: favorite.type }
      });
    } catch (error) {
      dispatch({ type: "set_error", payload: error.message });
    }
  };

  return (
    <div className="favorites-dropdown ms-auto" ref={favoritesDropdownRef}>
      <div className="favorites-actions">
        <Link to="/favorites" className="btn btn-outline-warning fw-semibold favorites-page-link" onClick={() => setIsFavoritesOpen(false)}>
          Ver favoritos
        </Link>
        <button
          className="btn btn-warning fw-semibold favorites-toggle"
          type="button"
          aria-expanded={isFavoritesOpen}
          aria-haspopup="true"
          onClick={() => setIsFavoritesOpen((current) => !current)}
        >
          Favoritos <span className="badge text-bg-dark ms-1">{favorites.length}</span>
        </button>
      </div>
      <div className={`favorites-menu ${isFavoritesOpen ? "is-open" : ""}`}>
        {favorites.length === 0 && (
          <div className="favorite-empty text-secondary py-3">No hay favoritos todavía</div>
        )}

        {favorites.map((favorite) => (
          <div key={`${favorite.type}-${favorite.uid}`} className="favorite-item">
            <Link className="favorite-link" to={`/details/${favorite.type}/${favorite.uid}`} onClick={() => setIsFavoritesOpen(false)}>
              <span className="fw-semibold">{favorite.name}</span>
              <span className="d-block small text-secondary">{categoryLabels[favorite.type]}</span>
            </Link>
            <button
              className="favorite-remove-button"
              type="button"
              aria-label={`Eliminar ${favorite.name} de favoritos`}
              onClick={() => handleRemoveFavorite(favorite)}
            >
              <i className="fa-solid fa-trash" aria-hidden="true"></i>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

FavoritesDropdown.propTypes = {
  dispatch: PropTypes.func.isRequired,
  favorites: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    type: PropTypes.oneOf(["people", "planets", "vehicles"]).isRequired,
    uid: PropTypes.string.isRequired
  })).isRequired
};
