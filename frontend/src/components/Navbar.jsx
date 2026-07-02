import { Link } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";
import { FavoritesDropdown } from "./FavoritesDropdown";
import { SearchBox } from "./SearchBox";

export const Navbar = () => {
  const { store, dispatch } = useGlobalReducer();

  return (
    <nav className="navbar navbar-expand navbar-galaxy" data-bs-theme="dark">
      <div className="container navbar-content">
        <Link to="/" className="navbar-brand fw-bold">
          Blog de Star Wars
        </Link>
        <SearchBox store={store} />
        <FavoritesDropdown favorites={store.favorites} dispatch={dispatch} />
      </div>
    </nav>
  );
};
