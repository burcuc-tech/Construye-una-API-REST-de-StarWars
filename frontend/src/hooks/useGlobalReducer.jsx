import { useEffect, useReducer, createContext, useContext } from "react";
import PropTypes from "prop-types";
import storeReducer, { initialStore, RESOURCES_CACHE_VERSION } from "../store";

const StoreContext = createContext();

export function StoreProvider({ children }) {
    const [store, dispatch] = useReducer(storeReducer, initialStore());

    useEffect(() => {
        const resources = {
            version: RESOURCES_CACHE_VERSION,
            people: store.people,
            planets: store.planets,
            vehicles: store.vehicles
        };

        localStorage.setItem("starWarsResources", JSON.stringify(resources));
    }, [store.people, store.planets, store.vehicles]);

    return <StoreContext.Provider value={{ store, dispatch }}>
        {children}
    </StoreContext.Provider>;
}

StoreProvider.propTypes = {
    children: PropTypes.node
};

export default function useGlobalReducer() {
    const { dispatch, store } = useContext(StoreContext);
    return { dispatch, store };
}
