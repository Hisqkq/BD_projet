import psycopg2
import psycopg2.extras
from db_connection import connect

create_table_queries = [
    """
    CREATE TABLE region (
        id_region INT PRIMARY KEY,
        nom_region VARCHAR(26)
    );
    """,
    """
    CREATE TABLE departement (
        id_departement VARCHAR(3) PRIMARY KEY,
        nom_departement VARCHAR(23),
        id_region INT REFERENCES region(id_region)
    );
    """,
    """
    CREATE TABLE commune (
        id_commune CHAR(5) PRIMARY KEY,
        nom_commune VARCHAR(45),
        superf FLOAT CONSTRAINT sup_pos CHECK ( superf > 0 ),
        id_departement varchar(3) REFERENCES departement(id_departement)
    );
    """,
    """
    CREATE TABLE chef_lieu_departement (
        id_departement VARCHAR(3) PRIMARY KEY,
        id_chef_lieu CHAR(5) REFERENCES commune(id_commune),
        FOREIGN KEY (id_departement) REFERENCES departement(id_departement)
    );
    """,
    """
    CREATE TABLE chef_lieu_region (
        id_region INT PRIMARY KEY,
        id_chef_lieu CHAR(5) REFERENCES commune(id_commune),
        FOREIGN KEY (id_region) REFERENCES region(id_region)
    );
    """,
    """
    CREATE TABLE statistique_mariage (
        id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        typmar VARCHAR(3),
        regdep INT,
        sexe CHAR(1) CONSTRAINT check_sexe CHECK ( sexe IN ('H', 'F') ),
        etamat INT,
        grage VARCHAR(5),
        lnepoux VARCHAR(6),
        natepoux VARCHAR(6),
        mmar INT,
        nbmaries INT,
        id_departement VARCHAR(3),
        id_region INT,
        annee INT,
        FOREIGN KEY (id_departement) REFERENCES departement(id_departement),
        FOREIGN KEY (id_region) REFERENCES region(id_region)
    );
    """,
    """
    CREATE TABLE statistiques_population (
        codgeo VARCHAR(5),
        annee INT,
        annee2 INT,
        type_statistique VARCHAR(50),
        valeur FLOAT CONSTRAINT val_pos CHECK ( valeur >= 0 ),
        FOREIGN KEY (codgeo) REFERENCES commune(id_commune),
        PRIMARY KEY (codgeo, annee, type_statistique)
    );
    """
]

conn = connect()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Nombre de population par region en 2020 

select_query = """
SELECT SUM(valeur) as population_region, region.nom_region 
FROM statistiques_population JOIN commune ON statistiques_population.codgeo = commune.id_commune
JOIN departement ON commune.id_departement = departement.id_departement
JOIN region ON departement.id_region = region.id_region
WHERE type_statistique = 'Population' AND annee = 2020
GROUP BY region.nom_region;
"""

cur.execute(select_query)

rows = cur.fetchall()

for row in rows:
    print('Population de la région', row['nom_region'], 'en 2020:', row['population_region'])
    
conn.commit()
