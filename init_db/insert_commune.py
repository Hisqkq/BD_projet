import pandas as pd
from db import insert_dataframe_into_table

def filter_dom_codes(df, column_name):
    dom_codes = ['971', '972', '973', '974', '976']
    return df[~df[column_name].isin(dom_codes)]

# Région
df_region = pd.read_csv('data/CDR/v_region_2023.csv', sep=',')
df_region_to_insert = df_region[['REG', 'LIBELLE']].rename(columns={'REG': 'id_region', 'LIBELLE': 'nom_region'})
df_region_to_insert = df_region_to_insert[df_region_to_insert['id_region'] > 6]

# Département
df_departement = pd.read_csv('data/CDR/v_departement_2023.csv', sep=',')
df_departement_to_insert = df_departement[['DEP', 'LIBELLE', 'REG']].rename(columns={'DEP': 'id_departement', 'LIBELLE': 'nom_departement', 'REG': 'id_region'})
df_departement_to_insert = filter_dom_codes(df_departement_to_insert, 'id_departement')

# Commune
df_commune = pd.read_csv('data/CDR/v_commune_2023.csv', sep=',', dtype={'TYPECOM': str})
df_commune = df_commune[df_commune['TYPECOM'].isin(['COM', 'ARM'])]
pop_data = pd.read_csv('data/statistiques/population/base-cc-serie-historique-2020.csv', sep=';', dtype={'CODGEO': str})
superficie = pop_data[['CODGEO', 'SUPERF']]
df_commune = df_commune.merge(superficie, left_on='COM', right_on='CODGEO')
df_commune = df_commune[['COM', 'LIBELLE', 'SUPERF', 'DEP']]
df_commune = df_commune.rename(columns={'COM': 'id_commune', 'LIBELLE': 'nom_commune', 'SUPERF': 'superf', 'DEP': 'id_departement'})
df_commune = filter_dom_codes(df_commune, 'id_departement')

# Chef lieu département
df_chef_lieu_departement = df_departement[['DEP', 'CHEFLIEU']].rename(columns={'DEP': 'id_departement', 'CHEFLIEU': 'id_chef_lieu'})
df_chef_lieu_departement = filter_dom_codes(df_chef_lieu_departement, 'id_departement')

# Chef lieu région
df_chef_lieu_region = df_region[['REG', 'CHEFLIEU']].rename(columns={'REG': 'id_region', 'CHEFLIEU': 'id_chef_lieu'})
df_chef_lieu_region = df_chef_lieu_region[df_chef_lieu_region['id_region'] > 6]

def fill_tables_commune():
    insert_dataframe_into_table(df_region_to_insert, 'region', ['id_region', 'nom_region'])
    insert_dataframe_into_table(df_departement_to_insert, 'departement', ['id_departement', 'nom_departement', 'id_region'])
    insert_dataframe_into_table(df_commune, 'commune', ['id_commune', 'nom_commune', 'superf', 'id_departement'])
    insert_dataframe_into_table(df_chef_lieu_departement, 'chef_lieu_departement', ['id_departement', 'id_chef_lieu'])
    insert_dataframe_into_table(df_chef_lieu_region, 'chef_lieu_region', ['id_region', 'id_chef_lieu'])



