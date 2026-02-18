from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException

app = FastAPI(
    title="Peliculas API",
    description="API de peliculas",
    version="1.0.0"
)

class MovieCreate(BaseModel):
    title: str
    director: str
    year: int
    available: bool

class Movie(MovieCreate):
    id: int

movies_db: List[Movie] = [
    Movie(id=1, title="The Matrix", director="The Wachowskis", year=1999, available=True),
    Movie(id=2, title="Inception", director="Christopher Nolan", year=2010, available=True),
    Movie(id=3, title="Interstellar", director="Christopher Nolan", year=2014, available=False),
    Movie(id=4, title="The Lord of the Rings: The Fellowship of the Ring", director="Peter Jackson", year=2001, available=True),
    Movie(id=5, title="The Lord of the Rings: The Two Towers", director="Peter Jackson", year=2002, available=True),
    Movie(id=6, title="The Lord of the Rings: The Return of the King", director="Peter Jackson", year=2003, available=False),
    Movie(id=7, title="Pulp Fiction", director="Quentin Tarantino", year=1994, available=True),
    Movie(id=8, title="Kill Bill: Vol. 1", director="Quentin Tarantino", year=2003, available=True),
    Movie(id=9, title="Avatar", director="James Cameron", year=2009, available=False),
    Movie(id=10, title="Titanic", director="James Cameron", year=1997, available=True),
    Movie(id=11, title="The Dark Knight", director="Christopher Nolan", year=2008, available=True),
    Movie(id=12, title="Batman Begins", director="Christopher Nolan", year=2005, available=False),
    Movie(id=13, title="Jurassic Park", director="Steven Spielberg", year=1993, available=True),
    Movie(id=14, title="Schindler's List", director="Steven Spielberg", year=1993, available=False),
    Movie(id=15, title="Forrest Gump", director="Robert Zemeckis", year=1994, available=True),
    Movie(id=16, title="Gladiator", director="Ridley Scott", year=2000, available=True),
    Movie(id=17, title="Alien", director="Ridley Scott", year=1979, available=False),
    Movie(id=18, title="Back to the Future", director="Robert Zemeckis", year=1985, available=True),
    Movie(id=19, title="The Godfather", director="Francis Ford Coppola", year=1972, available=True),
    Movie(id=20, title="The Godfather: Part II", director="Francis Ford Coppola", year=1974, available=False),
]

next_id = 21


@app.get("/movie")
def root():
    return movies_db

@app.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    for m in movies_db:
        if m.id == movie_id:
            return m
    raise HTTPException(status_code=404, detail="Movie not found")

@app.post("/movie", status_code=201)
def create_movie(movie_data: MovieCreate):
    global next_id

    new_movie = Movie(
        id=next_id,
        title=movie_data.title,
        director=movie_data.director,
        year=movie_data.year,
        available=movie_data.available
    )

    movies_db.append(new_movie)
    next_id+=1

    return new_movie

@app.put("/movie/{movie_id}")
def update_movie(movie_id: int, movie_data: MovieCreate):
    for m in movies_db:
        if m.id == movie_id:
            m.title=movie_data.title
            m.director=movie_data.director
            m.year=movie_data.year
            m.available=movie_data.available
            return m
        
    raise HTTPException(status_code=404, detail="Movie not found")
    
@app.delete("/movie/{movie_id}", status_code=204)
def delete_movie(movie_id:int):
    for m in movies_db:
        if m.id == movie_id:
            movies_db.remove(m)
            return
    raise HTTPException(status_code=404, detail="Movie not found")

@app.get("/movie/available/{status}")
def get_movie(status: bool):
    lista=[]
    for m in movies_db:
        if m.available == status:
            lista.append(m)

    return lista
   
@app.get("/movie/director/{directorenc}")
def get_director(directorenc: str):
    lista=[]
    print(directorenc)
    for m in movies_db:
        if m.director == directorenc:
            lista.append(m)

    return lista 
    