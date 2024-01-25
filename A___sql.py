# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---                Niveau A - Fonctions et Constantes liées à MySQL                ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                20/02/2023
"""

# https://python.doctor/page-database-data-base-donnees-query-sql-mysql-postgre-sqlite

import mysql.connector 
from datetime import datetime


# %% Connection au serveur SQL et création des tables

nom_database = "db_MegaLG"

a = datetime.now()

print(a)

conn = mysql.connector.connect(host="localhost", 
                               user="MdJ_MegaLG", password="JsuisLG#0810",
                               database=nom_database)
cursor = conn.cursor(buffered = True)

b = datetime.now()

print(b)

# %%% Définition des nom des tables et des clefs

#### Nom des tables

nom_table_joueurs  = "table_joueurs"
nom_table_groupes  = "table_groupes"
nom_table_villages = "table_villages"
nom_table_compos   = "table_compos"


#### Colonnes communes

clef_numGroupe  = "num_groupe"
clef_numVillage = "num_village"
clef_numCompo   = "num_compo"


#### Colonnes de la table Joueurs 

clef_idDiscord  = "id_discord"
clef_pseudo     = "pseudo"
clef_sexe       = "sexe"        #  H = 1  ///  F = 0

clef_matricule  = "matricule"

clef_idRole     = "id_role"
clef_caractRole = "caracteristiques_role"
clef_caractJoue = "caracteristiques_joueur"
clef_estVivant  = "est_vivant"
clef_ancienVlg  = "anciens_villages"

clef_points     = "points"



#### Colonnes de la tables Groupes

clef_nomGroupe   = "nom_groupe"

clef_idSalon_Grp = "id_salon_groupe"
clef_idChef_Grp  = "id_chef_groupe"
clef_grp_public  = "groupe_est_public"
clef_code_groupe = "code_groupe"

clef_date_activi_grp = "date_depuis_derniere_activite_dans_groupe"

clef_partie_lance = "type_de_partie"
clef_deb_partie  = "date_lancement_prochaine_partie"



#### Colonnes de la tables Villages

clef_nomVillage = "nom_village"

clef_idRole_vlg     = "id_role_discord_du_village"
clef_idRoleMort_vlg = "id_role_mort_discord_du_village"

clef_idSalon_vlg_Rapport   = "id_salon_vlg_rapport"
clef_idSalon_vlg_Role      = "id_salon_vlg_role" 
clef_idSalon_vlg_Bucher    = "id_salon_vlg_bucher"
clef_idSalon_vlg_Cimetiere = "id_salon_vlg_cimetiere"
clef_idSalon_vlg_Debat     = "id_salon_vlg_debat"
clef_idSalon_vlg_vocDebat  = "id_salonVoc_vlg_debat"

clef_idSalon_vlg_voteLG     = "id_salon_vlg_lg_vote"
clef_idSalon_vlg_debatLG    = "id_salon_vlg_lg_debat"
clef_idSalon_vlg_vocDebatLG = "id_salonVoc_vlg_lg_debat"

clef_idSalon_vlg_FamilleNomb    = "id_salon_vlg_fn_debat"
clef_idSalon_vlg_vocFamilleNomb = "id_salonVoc_vlg_fn_debat"


#### Colonnes de la table Compos 

clef_nom_compo  = "nom_compo"

clef_nb_joueur  = "nombre_de_joueur"
clef_type_compo = "type_compo"

clef_roles_compo  = "roles_dans_la_compo"
clef_caract_compo = "caracteristique_de_la_compo"



# %%% Création éventuelle des bases de donnée

#### ✅ - Testée
def creation_des_tables () :
    """
    Créée les tables stockant les données des Groupes, des Villages et des Joueurs.
    
    Type      Nb_Oct      Min      Moy     Max       Amplitude
    TINYINT 	1 	-128    	    0 	127 	    255
    SMALLINT 	2 	-32768 	        0 	32767 	    65535
    MEDIUMINT 	3 	-8388608 	    0 	8388607 	16777215
    INT 	    4 	-2147483648 	0 	2147483647 	4294967295
    BIGINT 	    8 	-2**63       	0 	2**63-1 	2**64-1
    """
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {nom_table_compos} (
            {clef_numCompo} INT NOT NULL PRIMARY KEY,
            {clef_nom_compo} VARCHAR(64) DEFAULT NULL,
            
            {clef_nb_joueur} TINYINT DEFAULT NULL,
            {clef_type_compo} TINYINT DEFAULT NULL,
            
            {clef_roles_compo} VARCHAR(250) DEFAULT NULL,
            {clef_caract_compo} VARCHAR(250) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci ;""")
    
    
    
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {nom_table_groupes} (
            {clef_numGroupe} SMALLINT NOT NULL PRIMARY KEY,
            {clef_nomGroupe} VARCHAR(64) DEFAULT NULL,
            
            {clef_idSalon_Grp} BIGINT DEFAULT NULL,
            {clef_idChef_Grp} BIGINT DEFAULT NULL,
            {clef_grp_public} TINYINT(1) DEFAULT NULL,
            {clef_code_groupe} VARCHAR(64) DEFAULT NULL,

            {clef_date_activi_grp} DATETIME DEFAULT NULL,

            {clef_partie_lance} TINYINT DEFAULT NULL,
            {clef_deb_partie} DATETIME DEFAULT NULL,
            
            {clef_numCompo} INT DEFAULT NULL,
            
        FOREIGN KEY ({clef_numCompo}) REFERENCES {nom_table_compos} ({clef_numCompo}) 
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci ;""")
    
    
    
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {nom_table_villages} (
            {clef_numVillage} SMALLINT NOT NULL PRIMARY KEY,
            {clef_nomVillage} VARCHAR(64) DEFAULT NULL,
            
            {clef_idRole_vlg} BIGINT DEFAULT NULL,
            {clef_idRoleMort_vlg} BIGINT DEFAULT NULL,
            
            {clef_idSalon_vlg_Rapport} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_Role} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_Bucher} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_Cimetiere} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_Debat} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_vocDebat} BIGINT DEFAULT NULL,
            
            {clef_idSalon_vlg_voteLG} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_debatLG} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_vocDebatLG} BIGINT DEFAULT NULL,
            
            {clef_idSalon_vlg_FamilleNomb} BIGINT DEFAULT NULL,
            {clef_idSalon_vlg_vocFamilleNomb} BIGINT DEFAULT NULL,

            {clef_numCompo} INT DEFAULT NULL,
            
        FOREIGN KEY ({clef_numCompo}) REFERENCES {nom_table_compos} ({clef_numCompo}) 
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci ;""")
    
    
    
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {nom_table_joueurs} (
            {clef_idDiscord} BIGINT NOT NULL PRIMARY KEY,
            {clef_pseudo} VARCHAR(64) DEFAULT NULL,
            {clef_sexe} TINYINT(1) DEFAULT NULL,
            
            {clef_matricule} SMALLINT DEFAULT NULL,
            {clef_idRole} SMALLINT DEFAULT NULL,
            {clef_caractRole} VARCHAR(64) DEFAULT NULL,
            {clef_caractJoue} VARCHAR(64) DEFAULT NULL,
            
            {clef_numGroupe} SMALLINT DEFAULT NULL,
            {clef_numVillage} SMALLINT DEFAULT NULL,
            
            {clef_estVivant} TINYINT(1) DEFAULT NULL,
            {clef_ancienVlg} VARCHAR(100) DEFAULT NULL,

            {clef_points} INT DEFAULT NULL,
            
        FOREIGN KEY ({clef_numGroupe}) REFERENCES {nom_table_groupes} ({clef_numGroupe}),
        FOREIGN KEY ({clef_numVillage}) REFERENCES {nom_table_villages} ({clef_numVillage}) 
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci ;""")
    
    conn.commit()



# %% Fonctions

# %%% Clefs de la table et colecte de la totalité de la table

#### ✅ - Testée
def clefs_de_la_table (nom_table):
    """
    Renvoie les clefs de la table ayant le nom donnée en entrée.
    """
    
    liste_noms_colonnes = []
    
    cursor.execute(f"SHOW columns FROM {nom_table};")
        
    for (nom_colonne, type_colonne, null_colonne, key_colonne, val_par_def, autres_infos) in cursor:
        liste_noms_colonnes.append(nom_colonne)

    return liste_noms_colonnes



#### ✅ - Testée
def donnees_de_la_table (nom_table):
    """
    Renvoie la liste des données se trouvant dans la table donnée en argument.
    Cette liste est une liste de dictionaire individuel (chacun d'entre eux correspond à une ligne de la table).
    """
    
    clefs_ligne = clefs_de_la_table(nom_table)
    
    cursor.execute(f"SELECT * FROM {nom_table};")
    
    liste_donne = []
    
    for val_ligne in cursor :
        
        dico_ligne = {}
        
        for i in range(len(clefs_ligne)) :
            
            try    : dico_ligne[clefs_ligne[i]] = val_ligne[i]
            except : dico_ligne[clefs_ligne[i]] = None
        
        liste_donne.append(dico_ligne)
        
    return liste_donne



# %%% Recherche de données

#### ✅ - Testée
def colonne_avec(nom_table, clefColonne):
    """
    Renvoie la liste de toute la colonne de fichierGoogleSheet ayant la clef correspondante.
    """

    cursor.execute(f"SELECT {clefColonne} FROM {nom_table};")
    
    colonne = []
    
    for (val,) in cursor:
        colonne.append( val )
        
    return colonne



#### ✅ - Testée
def lignes_avec (nom_table, clefColonne_aRechercher, info):
    """
    Renvoie la liste des données se trouvant dans la table donnée en argument, ayant le critère recherché.
    Cette liste est une liste de dictionaire individuel (chacun d'entre eux correspond à une ligne de la table).
    """
    
    clefs_ligne = clefs_de_la_table(nom_table)
    
    cursor.execute(f"SELECT * FROM {nom_table} WHERE {clefColonne_aRechercher} = {info};")
    
    liste_donne = []
    
    for val_ligne in cursor:
        liste_donne.append( {clefs_ligne[i] : val_ligne[i]   for i in range(len(clefs_ligne))} )
    
    return liste_donne



# %%% Modification de bases de données

# %%%% Ajout de données

#### ✅ - Testée
def ajouter_ligne (nom_table, dico_donnee):
    """
    Ajoute une ligne à la table portant le nom donnée en argument.
    """
        
    for clef in dico_donnee :
        if str(type(dico_donnee[clef])) == "<class 'datetime.datetime'>" : dico_donnee[clef] = str(dico_donnee[clef])
    
    
    
    commande = f"INSERT INTO {nom_table} ("
    
    for clef in dico_donnee.keys() :
        commande += f"{clef}, "
        
    commande = commande[:-2] + ") VALUES ("
    
    for valeur in dico_donnee.values() :
        if      valeur  == None  : commande +=  "NULL, "
        elif type(valeur) == str : commande += f"'{valeur}', "
        else                     : commande += f"{valeur}, "
        
    commande = commande[:-2] + ");"
    
    
    
    cursor.execute(commande)
    conn.commit()
    
    

#### ✅ - Testée
def ajouter_val_cellule_avec (nom_table, clefColonne_aRechercher, val_info, clefColonne_aAjouter, val_a_ajouter):
    """
    Ajoute la valeur val_a_ajouter à la premiere ligne renvoyée par lignes_avec.
    """
    
    ligne = lignes_avec( nom_table, 
                         clefColonne_aRechercher, val_info )[0]
    
    val_initiale = ligne[clefColonne_aAjouter]
    
    if val_initiale == None :
        if type(val_a_ajouter) == int : val_initiale = 0
        if type(val_a_ajouter) == str : val_initiale = ""
    
    remplacer_val_lignes_avec( nom_table, 
                               clefColonne_aRechercher, val_info,
                               clefColonne_aAjouter   , val_initiale + val_a_ajouter )
    
    
    
    
    
# %%%% Modification de la valeur d'une ligne

#### ✅ - Testée
def remplacer_val_lignes_avec (nom_table, clefColonne_aRechercher, val_info, clefColonne_aRemplacer, nouv_val):
    
    if str(type(val_info)) == "<class 'datetime.datetime'>" : val_info = str(val_info)
    if str(type(nouv_val)) == "<class 'datetime.datetime'>" : nouv_val = str(nouv_val)
    
    if     type(val_info)  == str                           : val_info = "'" + val_info + "'"
    if     type(nouv_val)  == str                           : nouv_val = "'" + nouv_val + "'"
    
    if          val_info   == None                          : val_info = "NULL"
    if          nouv_val   == None                          : nouv_val = "NULL"
    
    cursor.execute(f"UPDATE {nom_table} SET {clefColonne_aRemplacer} = {nouv_val} WHERE {clefColonne_aRechercher} = {val_info};")
    conn.commit()



#### ✅ - Testée
def remplacer_ligne_avec(nom_table, clefColonne_aRechercher, val_info, dico_donnee):
    """
    Supprime LES ligneS correspondant à l'info recherché. Si aucune ligne ne correspond, aucune n'est supprimée.
    Ajoute une ligne avec les nouvelles données.
    """
    suppression_lignes_avec(nom_table, clefColonne_aRechercher, val_info)
    
    ajouter_ligne(nom_table, dico_donnee)



# %%%% Suppression de donnée

#### ✅ - Testée
def suppression_lignes_avec(nom_table, clefColonne_aRechercher, val_info) :
    """
    Supprime les lignes de {nom_table} ayant la clefColonne_aRechercher correspondant à l'info donnée en argument.
    """
    
    if str(type(val_info)) == "<class 'datetime.datetime'>" : val_info = str(val_info)
    if     type(val_info)  == str                           : val_info = "'" + val_info + "'"    
    
    cursor.execute(f"DELETE FROM {nom_table} WHERE {clefColonne_aRechercher} = {val_info}")
    conn.commit()
    


#### ✅ - Testée
def supprimer_toutes_les_tables () :
    f"""
    Supprime toutes les tables contenues dans la base de donnée {nom_database}.
    """
    
    verif = input(f"{nom_database} : Vous êtes sur le point de supprimer toutes les tables contenu dans la base de donnée {nom_database}, \nêtes vous certain de vouloir faire cela ? ")
    
    if verif.lower() == "oui" :
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        conn.commit()
        
        cursor.execute(( "SELECT table_name "
                         "FROM information_schema.tables "
                        f"WHERE TABLE_SCHEMA = '{nom_database}';"))
        
        copie_cursor = list(cursor)
        
        for (table_name,) in copie_cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()





# %% Partie de Test

if __name__ == "__main__" : 

    print("1 - Suppression de toutes les tables. (supprimer_toutes_les_tables)")    

    supprimer_toutes_les_tables()
    
    print("\n --- \n2 - Création de toutes les tables. (creation_des_tables)")
    
    creation_des_tables()
    
    print("\n --- \n3 - Remplissage des tables. (ajouter_ligne)")

    dico_donnee_test_groupes  = {clef_numGroupe : 17, clef_nomGroupe : "Groupe n°17 😊⭐😈🧮", clef_date_activi_grp : str(a)}
    ajouter_ligne(nom_table_groupes, dico_donnee_test_groupes)
    
    
    dico_donnee_test_villages = {clef_numVillage : 17, clef_nomVillage : "Village n°17"}
    ajouter_ligne(nom_table_villages, dico_donnee_test_villages)
    
    
    dico_donnee_test_joueurs =  {clef_idDiscord : 60, clef_pseudo : "Pablio", clef_sexe : 1,
                                 clef_matricule : 34, clef_idRole : 2, clef_caractRole : "ADD", clef_caractJoue : "flhkdhh",
                                 clef_numGroupe : 17, clef_numVillage : 17}
    ajouter_ligne(nom_table_joueurs, dico_donnee_test_joueurs)
    
    dico_donnee_test_joueurs =  {clef_idDiscord : 7840, clef_pseudo : "Jean", clef_sexe : 0,
                                 clef_matricule : 32, clef_idRole : 2, clef_caractRole : None, clef_caractJoue : "flhkdfljdgkjh",
                                 clef_numGroupe : 17, clef_numVillage : None}
    ajouter_ligne(nom_table_joueurs, dico_donnee_test_joueurs)
    
    print("\n --- \n4 - Affichage des tables. (clefs_de_la_table) (donnees_de_la_table)")
    
    print(f"Clefs de la table joueur   : {clefs_de_la_table(nom_table_joueurs)}\n" )
    print(f"Données de la table joueur : {donnees_de_la_table(nom_table_joueurs)}\n")
    
    print("\n --- \n5 - Recherche dans une table. (colonne_avec) (lignes_avec)")
    
    print(f"Colonne idDiscord de la table joueur : {colonne_avec(nom_table_joueurs, clef_idDiscord)}\n")
    print(f"Joueurs ayant 32 comme Matricule     : {lignes_avec(nom_table_joueurs, clef_matricule, 32)}\n")
    
    print("\n --- \n6 - Ajout d'une valeur à une ligne. (ajouter_val_cellule_avec)")
    
    print(f"Ajout de '49.3' à l'idRole d'un joueur : {ajouter_val_cellule_avec(nom_table_joueurs, clef_idDiscord, 60, clef_idRole, 49.3)}\n")
    print(f"Données de la table joueur : {donnees_de_la_table(nom_table_joueurs)}\n")
    
    print("\n --- \n7 - Remplacement d'une valeur. (remplacer_val_lignes_avec)")
    
    print(f"Remplacement du pseudo d'un joueur : {remplacer_val_lignes_avec(nom_table_joueurs, clef_idDiscord, 7840, clef_pseudo, None)}\n")
    print(f"Données de la table joueur : {donnees_de_la_table(nom_table_joueurs)}\n")
    
    dico_donnee_test_joueurs =  {clef_idDiscord : 65740, clef_pseudo : "ghfgsdglq", clef_sexe : 0,
                                 clef_matricule : None, clef_caractRole : "bgkkhADD", clef_caractJoue : "flhkdhh",
                                 clef_numGroupe : 17}
    remplacer_ligne_avec(nom_table_joueurs, clef_idDiscord, 123, dico_donnee_test_joueurs)

    cursor.close()
    conn.close()