import { useState } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { categoryLabels, resourceTypes } from "../data/categories";

export const SearchBox = ({ store }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const searchQuery = searchTerm.trim().toLowerCase();
  const searchableItems = resourceTypes.flatMap((type) =>
    store[type].map((item) => ({
      ...item,
      type
    }))
  );
  const searchResults = searchQuery.length < 2
    ? []
    : searchableItems
        .filter((item) => item.name.toLowerCase().includes(searchQuery))
        .slice(0, 6);

  const closeSearch = () => {
    setSearchTerm("");
    setIsSearchOpen(false);
  };

  return (
    <div className="search-dropdown">
      <label className="visually-hidden" htmlFor="databank-search">
        Buscar en la databank
      </label>
      <input
        id="databank-search"
        className="form-control search-input"
        type="search"
        placeholder="Buscar..."
        value={searchTerm}
        autoComplete="off"
        onChange={(event) => {
          setSearchTerm(event.target.value);
          setIsSearchOpen(true);
        }}
        onFocus={() => setIsSearchOpen(true)}
      />
      {isSearchOpen && searchQuery.length >= 2 && (
        <div className="search-menu">
          {searchResults.length === 0 && (
            <div className="search-empty">Sin resultados</div>
          )}

          {searchResults.map((item) => (
            <Link
              className="search-result"
              key={`${item.type}-${item.uid}`}
              to={`/details/${item.type}/${item.uid}`}
              onClick={closeSearch}
            >
              <span className="fw-semibold">{item.name}</span>
              <span className="d-block small">{categoryLabels[item.type]}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

SearchBox.propTypes = {
  store: PropTypes.shape({
    people: PropTypes.array.isRequired,
    planets: PropTypes.array.isRequired,
    vehicles: PropTypes.array.isRequired
  }).isRequired
};
