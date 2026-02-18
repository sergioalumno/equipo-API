from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

class PlayerCreate(BaseModel):
    name:str
    position:str
    number:int

class Player(PlayerCreate):
    id: int
    team_id: Optional[int] = None

class TeamCreate(BaseModel):
    name:str
    city:str
    stadium:str

class Team(TeamCreate):
    id: int

teams_db: List[Team] = [
    Team(id=1, name="Sevilla FC", city="Sevilla", stadium="Ramón Sánchez-Pizjuán"),
    Team(id=2, name="Real Betis", city="Sevilla", stadium="Benito Villamarín"),
    Team(id=3, name="FC Barcelona", city="Barcelona", stadium="Estadi Olímpic Lluís Companys"),
    Team(id=4, name="Real Madrid", city="Madrid", stadium="Santiago Bernabéu"),
    Team(id=5, name="Atlético de Madrid", city="Madrid", stadium="Cívitas Metropolitano"),
]

players_db: List[Player] = [
    # Sevilla FC
    Player(id=1, name="Marko Dmitrović", position="Portero", number=13, team_id=1),
    Player(id=2, name="Sergio Ramos", position="Defensa", number=4, team_id=1),
    Player(id=3, name="Jesús Navas", position="Defensa", number=16, team_id=1),
    Player(id=4, name="Ivan Rakitić", position="Centrocampista", number=10, team_id=1),
    Player(id=5, name="Youssef En-Nesyri", position="Delantero", number=15, team_id=1),

    # Real Betis
    Player(id=6, name="Rui Silva", position="Portero", number=1, team_id=2),
    Player(id=7, name="Germán Pezzella", position="Defensa", number=6, team_id=2),
    Player(id=8, name="Guido Rodríguez", position="Centrocampista", number=5, team_id=2),
    Player(id=9, name="Isco", position="Centrocampista", number=22, team_id=2),
    Player(id=10, name="Borja Iglesias", position="Delantero", number=9, team_id=2),

    # FC Barcelona
    Player(id=11, name="Marc-André ter Stegen", position="Portero", number=1, team_id=3),
    Player(id=12, name="Ronald Araújo", position="Defensa", number=4, team_id=3),
    Player(id=13, name="Jules Koundé", position="Defensa", number=23, team_id=3),
    Player(id=14, name="Pedri", position="Centrocampista", number=8, team_id=3),
    Player(id=15, name="Robert Lewandowski", position="Delantero", number=9, team_id=3),

    # Real Madrid
    Player(id=16, name="Thibaut Courtois", position="Portero", number=1, team_id=4),
    Player(id=17, name="Dani Carvajal", position="Defensa", number=2, team_id=4),
    Player(id=18, name="Antonio Rüdiger", position="Defensa", number=22, team_id=4),
    Player(id=19, name="Jude Bellingham", position="Centrocampista", number=5, team_id=4),
    Player(id=20, name="Vinícius Jr.", position="Delantero", number=7, team_id=4),

    # Atlético de Madrid
    Player(id=21, name="Jan Oblak", position="Portero", number=13, team_id=5),
    Player(id=22, name="José María Giménez", position="Defensa", number=2, team_id=5),
    Player(id=23, name="Koke", position="Centrocampista", number=6, team_id=5),
    Player(id=24, name="Antoine Griezmann", position="Delantero", number=7, team_id=5),
    Player(id=25, name="Álvaro Morata", position="Delantero", number=19, team_id=5),

    # Free agents (team_id = None)
    Player(id=26, name="David de Gea", position="Portero", number=1, team_id=None),
    Player(id=27, name="Eden Hazard", position="Delantero", number=10, team_id=None),
    Player(id=28, name="Sergio Busquets", position="Centrocampista", number=5, team_id=None),
    Player(id=29, name="Ángel Di María", position="Delantero", number=11, team_id=None),
    Player(id=30, name="Neymar Jr.", position="Delantero", number=10, team_id=None),
]

next_team_id = 6
next_player_id = 31

@app.get("/teams")
def get_teams():
    return teams_db

@app.get("/teams/{team_id}", status_code=200)
def get_team_id(team_id: int):

    for t in teams_db:
        if t.id==team_id:
            return t
    raise HTTPException(status_code=404, detail="Movie not found")
    
@app.post("/teams", status_code=201)
def post_teams(teamsData: TeamCreate):
    global next_team_id

    new_team = Team(
        id=next_team_id,
        name=teamsData.name,
        city=teamsData.city,
        stadium=teamsData.stadium
    )

    teams_db.append(new_team)
    next_team_id=next_team_id+1

    return new_team

@app.put("/teams/{team_id}", status_code=200)
def put_teams(team_id: int, teamsData: TeamCreate):
    for t in teams_db:
        if t.id == team_id:
            t.name=teamsData.name
            t.city=teamsData.city
            t.stadium=teamsData.stadium
            return
        raise HTTPException(status_code=404, detail="not found")

@app.delete("/teams/{team_id}", status_code=204)
def del_teams(team_id: int):
    for t in teams_db:
        if t.id==team_id:
            for p in players_db:
                if p.team_id == team_id:
                    p.team_id=None
            teams_db.remove(t)        
            return
    raise HTTPException(status_code=404, detail="not found")
        
# players
@app.get("/players")
def get_players():
    return players_db

@app.get("/players/{player_id}", status_code=200)
def get_player_id(player_id: int):

    for t in players_db:
        if t.id==player_id:
            return t
    raise HTTPException(status_code=404, detail="not found")

@app.post("/player", status_code=201)
def post_player(playersData: PlayerCreate):
    global next_player_id

    new_player = Player(
        id=next_player_id,
        name=playersData.name,
        position=playersData.position,
        number=playersData.number,
        team_id=None
    )

    players_db.append(new_player)
    next_player_id=next_player_id+1

    return new_player

@app.put("/player/{player_id}", status_code=200)
def put_players(player_id: int, playersData: Player):
    for p in players_db:
        if p.id == player_id:
            p.name=playersData.name
            p.position=playersData.position
            p.number=playersData.number
            p.team_id=playersData.team_id
            return p
    raise HTTPException(status_code=404, detail="not found")

@app.delete("/players/{player_id}", status_code=204)
def del_players(player_id: int):
    for p in players_db:
        if p.id == player_id:
            players_db.remove(p)
            return
        
    raise HTTPException(status_code=404, detail="not found")

@app.get("/players/free")
def players_free():
    listalibre=[]
    for p in players_db:
        if p.team_id is None:
            listalibre.append(p)

    if len(listalibre)==0:
        raise HTTPException(status_code=404, detail="not found")

    return listalibre

@app.get("/teams/{team_id}/players", status_code=200)
def listajugeq(team_id: int):
    lista=[]
    for p in players_db:
        if p.team_id==team_id:
            lista.append(p)
    
    if len(lista)==0:
        raise HTTPException(status_code=404, detail="not found")
    
    return lista

@app.post("/teams/{team_id}/players/{player_id}", status_code=200)
def asig_equip(team_id: int, player_id: int):
    for t in teams_db:
        if t.id == team_id:
            for p in players_db:
                if p.id == player_id:
                    p.team_id=t.id
                    return p
    
    raise HTTPException(status_code=404, detail="not found")

@app.delete("/teams/{team_id}/players/{player_id}", status_code=200)
def deljugeq(team_id: int, player_id: int):
    for t in teams_db: 
        if t.id == team_id:
            for p in players_db:
                if p.id == player_id:
                    p.team_id=None
                    return p
    
    raise HTTPException(status_code=404, detail="not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )