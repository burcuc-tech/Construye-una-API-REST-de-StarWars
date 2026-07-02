import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { categorySymbols, getImageSources } from "../data/imageSources";

export const StarWarsImage = ({ type, uid, alt, className = "", fallbackClassName = "" }) => {
  const [sourceIndex, setSourceIndex] = useState(0);
  const sources = getImageSources(type, uid);
  const source = sources[sourceIndex];

  useEffect(() => {
    setSourceIndex(0);
  }, [type, uid]);

  if (!source) {
    return (
      <div className={`star-image-fallback ${fallbackClassName}`} role="img" aria-label={alt}>
        <span>{categorySymbols[type]}</span>
        <strong>{alt}</strong>
      </div>
    );
  }

  return (
    <img
      src={source}
      className={className}
      alt={alt}
      onError={() => setSourceIndex((currentIndex) => currentIndex + 1)}
    />
  );
};

StarWarsImage.propTypes = {
  type: PropTypes.oneOf(["people", "planets", "vehicles"]).isRequired,
  uid: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  className: PropTypes.string,
  fallbackClassName: PropTypes.string
};
