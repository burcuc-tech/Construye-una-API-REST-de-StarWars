import { Link } from "react-router-dom";
import { EntityCard } from "../components/EntityCard";
import useGlobalReducer from "../hooks/useGlobalReducer";

const favoriteSections = [
  { key: "people", title: "Personajes" },
  { key: "planets", title: "Planetas" },
  { key: "vehicles", title: "Vehiculos" }
];

export const Favorites = () => {
  const { store } = useGlobalReducer();

  return (
    <main>
      <section className="hero-section favorites-hero">
        <div className="container">
          <p className="eyebrow mb-3">Reading list</p>
          <h1 className="hero-title">Favoritos</h1>
        </div>
      </section>

      <div className="container content-shell">
        {store.error && (
          <div className="alert alert-danger" role="alert">
            {store.error}
          </div>
        )}

        {store.favorites.length === 0 ? (
          <section className="resource-section">
            <div className="section-heading">
              <div>
                <p className="section-kicker">Databank</p>
                <h2>Tu seleccion</h2>
              </div>
              <span>0 favoritos</span>
            </div>
            <div className="favorites-empty-state">
              <h3>No hay favoritos todavia</h3>
              <p>Agrega personajes, planetas o vehiculos desde la databank.</p>
              <Link to="/" className="btn btn-dark">
                Explorar databank
              </Link>
            </div>
          </section>
        ) : (
          favoriteSections.map((section) => {
            const favorites = store.favorites.filter((favorite) => favorite.type === section.key);

            if (favorites.length === 0) return null;

            return (
              <section className="resource-section" key={section.key}>
                <div className="section-heading">
                  <div>
                    <p className="section-kicker">Favoritos</p>
                    <h2>{section.title}</h2>
                  </div>
                  <span>{favorites.length} favoritos</span>
                </div>

                <div className="row g-4">
                  {favorites.map((favorite) => (
                    <div className="col-12 col-sm-6 col-lg-4 col-xl-3" key={`${favorite.type}-${favorite.uid}`}>
                      <EntityCard item={favorite.item || favorite} type={favorite.type} />
                    </div>
                  ))}
                </div>
              </section>
            );
          })
        )}
      </div>
    </main>
  );
};
