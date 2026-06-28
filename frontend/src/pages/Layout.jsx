import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import ScrollToTop from "../components/ScrollToTop";
import { Navbar } from "../components/Navbar";
import { Footer } from "../components/Footer";
import { getFavorites } from "../api";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Layout = () => {
    const { dispatch } = useGlobalReducer();

    useEffect(() => {
        const loadFavorites = async () => {
            try {
                const favorites = await getFavorites();
                dispatch({ type: "set_favorites", payload: favorites });
            } catch (error) {
                dispatch({ type: "set_error", payload: error.message });
            }
        };

        loadFavorites();
    }, [dispatch]);

    return (
        <ScrollToTop>
            <Navbar />
                <Outlet />
            <Footer />
        </ScrollToTop>
    );
};
