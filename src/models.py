from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(40), nullable=False)
    height: Mapped[str] = mapped_column(String(40), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(40), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(40), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(40), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="people")

    def serialize(self):
        properties = {
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year
        }

        return {
            "id": self.id,
            "uid": str(self.id),
            "name": self.name,
            **properties,
            "properties": properties,
            "description": "Perfil del personaje con datos guardados en la API local."
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[str] = mapped_column(String(80), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        properties = {
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "diameter": self.diameter
        }

        return {
            "id": self.id,
            "uid": str(self.id),
            "name": self.name,
            **properties,
            "properties": properties,
            "description": "Planeta de Star Wars con datos guardados en la API local."
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(180), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(80), nullable=False)
    crew: Mapped[str] = mapped_column(String(40), nullable=False)
    passengers: Mapped[str] = mapped_column(String(40), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="vehicle")

    def serialize(self):
        properties = {
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "vehicle_class": self.vehicle_class,
            "crew": self.crew,
            "passengers": self.passengers
        }

        return {
            "id": self.id,
            "uid": str(self.id),
            "name": self.name,
            **properties,
            "properties": properties,
            "description": "Vehiculo de Star Wars con datos guardados en la API local."
        }


class Favorite(db.Model):
    __table_args__ = (
        CheckConstraint(
            "(CASE WHEN people_id IS NOT NULL THEN 1 ELSE 0 END) + "
            "(CASE WHEN planet_id IS NOT NULL THEN 1 ELSE 0 END) + "
            "(CASE WHEN vehicle_id IS NOT NULL THEN 1 ELSE 0 END) = 1",
            name="favorite_one_entity_check"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int | None] = mapped_column(ForeignKey("people.id"), nullable=True)
    planet_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicle.id"), nullable=True)

    user: Mapped[User] = relationship(back_populates="favorites")
    people: Mapped[People | None] = relationship(back_populates="favorites")
    planet: Mapped[Planet | None] = relationship(back_populates="favorites")
    vehicle: Mapped[Vehicle | None] = relationship(back_populates="favorites")

    def serialize(self):
        if self.people:
            entity = self.people
            entity_type = "people"
        elif self.planet:
            entity = self.planet
            entity_type = "planets"
        else:
            entity = self.vehicle
            entity_type = "vehicles"

        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
            "type": entity_type,
            "uid": str(entity.id) if entity else None,
            "name": entity.name if entity else None,
            "item": entity.serialize() if entity else None
        }
