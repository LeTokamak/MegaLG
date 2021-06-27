# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---            Niveau A - Fonctions et Constantes liées à Google Drive             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""



import gspread
from   oauth2client.service_account import ServiceAccountCredentials



#### Accès au Google Drive, création des variables de pages


scope  = ["https://spreadsheets.google.com/feeds"       , 
          "https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive.file"  , 
          "https://www.googleapis.com/auth/drive"        ]

creds  = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


# %% Création des Fichier

#### Infos Joueurs

InfoJoueurs         = client.open("Infos Joueurs")
page1_InfoJoueurs   = InfoJoueurs.sheet1


#### Sauvegarde

Sauvegarde          = client.open("Sauvegarde")
page1_Sauvegarde    = Sauvegarde.sheet1


#### Archive

Archives            = client.open("Archives")
page1_Archives      = Archives.sheet1


#### Groupes et Villages

Groupes_Villages    = client.open("Groupes et Villages")
page_Groupes        = Groupes_Villages.sheet1
page_Villages       = Groupes_Villages.get_worksheet(1)


#### Comptage des Messages

Compte_Msg          = client.open("Comptage des Messages")
page_CompteMsg      = Compte_Msg.sheet1





# %%% Création des clefs des Fichiers

#### Clefs de Joueurs (InfoJoueurs, Sauvegarde et Archives ont les mêmes clefs)

clefs_Joueurs = page1_InfoJoueurs.get()[0]

( clef_Matricule    ,
 
  clef_Sexe         ,
  clef_Prenom       ,
  clef_Nom          ,
  
  clef_Groupe       ,
  clef_numVillage   ,
  clef_idDiscord    ,
  
  clef_Role         ,
  clef_caractRoles  ,
  clef_caractJoueur  )= clefs_Joueurs



#### Clefs de Groupes

clefs_Groupes = page_Groupes.get()[0]

( clefGrp_numGroupe  ,
  clefGrp_CheminBrut ,
 
  clefGrp_idSalon    ,

  clefGrp_MsgSortie  ,
  clefGrp_MsgEntree  ,
  clefGrp_EmoEntree   ) = clefs_Groupes



#### Clefs de Villages

clefs_Villages = page_Villages.get()[0]

( clefVlg_numVillage             ,
  clefVlg_Nom                    ,
  
  clefVlg_idRoleDiscord          ,
  clefVlg_idRoleDiscord_Mort     ,
  
  clefVlg_idSalon_Rapport        ,
  clefVlg_idSalon_Cimetiere      ,
  clefVlg_idSalon_Bucher         ,
  clefVlg_idSalon_Debat          ,
  clefVlg_idSalon_vocDebat       ,
  
  clefVlg_idSalon_VoteLG         ,
  clefVlg_idSalon_DebatLG        ,
  clefVlg_idSalon_vocDebatLG     ,
  
  clefVlg_idSalon_FamilleNomb    ,
  clefVlg_idSalon_vocFamilleNomb  ) = clefs_Villages



#### Clefs de Villages

clefs_Messages = page_CompteMsg.get()[0]

( clefMsg_idDiscord              ,
  clefMsg_display_name           ,
  
  clefMsg_prenom                 ,
  clefMsg_nom                    ,
  clefMsg_sexe                   ,
  
  clefMsg_est_a_ISEN             ,
  clefMsg_ville                  ,
  clefMsg_promo                  ,
  
  clefMsg_infos_verifie          ,
  
  clefMsg_separateur             ,
  clefMsg_DMChannel               ) = clefs_Messages[:11]



# %% Fonctions

def page_fichier(fichierGoogleSheet, num_page = 0) :
    """
    Renvoie la page numéro num_page de fichierGoogleSheet 
    """
    
    if num_page == 0 :
        if   fichierGoogleSheet == InfoJoueurs   : return page1_InfoJoueurs
        elif fichierGoogleSheet == Sauvegarde    : return page1_Sauvegarde
        elif fichierGoogleSheet == Archives      : return page1_Archives
    
    return fichierGoogleSheet.get_worksheet(num_page)



def clefs_de_page (page_fichier) :
    """
    Renvoie la liste des clefs de la page
    """

    if   page_fichier == (page1_InfoJoueurs, page1_Sauvegarde, page1_Archives) : return clefs_Joueurs
    elif page_fichier == page_Groupes                                          : return clefs_Groupes
    elif page_fichier == page_Villages                                         : return clefs_Villages
    elif page_fichier == page_CompteMsg                                        : return clefs_Messages
    else                                                                       : return page_fichier.get()[0]
    




# %%% Fonctions d'accès à des pages, à des données ou des colonnes

def donneeGoogleSheet(page_fichier):
    """
    Renvoie les données les plus récentes de la page_fichier sous forme de liste de dictionaires
    """    
    
    return page_fichier.get_all_records()

      
        
def colonne_avec(page_fichier, clefColonne):
    """
    Renvoie la liste de toute la colonne de fichierGoogleSheet ayant la clef correspondante
    """

    colonne = []

    for d in donneeGoogleSheet(page_fichier):
        colonne.append(d[clefColonne])
        
    return colonne





# %%% Modification de page de fichier Google Sheet

# %%%% En-tête

def ajout_nouvColonne(nom_nouvColonne, page_fichier):
    """
    Ajoute une nouvelle colonne à page_fichier 
    """
    clefs          = clefs_de_page(page_fichier)
    
    numero_ligne   = 1
    numero_colonne = len(clefs) + 2
    
    page_fichier.update_cell(numero_ligne, numero_colonne, nom_nouvColonne)
    
    
    
    
    

# %%%% Lignes

def ajoutLigne(nvlLigne, page_fichier, numero_nvlLigne = 2) :
    """
    Ajoute une nouvelle ligne à page_fichier
    
    nvlLigne doit être un dictionnaire, les clefs doivent être celles du fichier
    
    Si des colonnes ne sont pas spécifiés, elles sont comblé par rien ("") 
    Si numero_nvlLigne == "fin", alors la ligne est ajouté à la fin de page_fichier
    """
    
    clefs          = clefs_de_page(page_fichier)
    liste_nvlLigne = []
    
    for c in clefs :
        try    : liste_nvlLigne.append( str(nvlLigne[c]) )
        except : liste_nvlLigne.append(        ""        )
    
    if numero_nvlLigne == "fin":
        numero_nvlLigne = len(donneeGoogleSheet(page_fichier)) + 2
    
    page_fichier.insert_row( liste_nvlLigne, numero_nvlLigne )



def remplacerLigne(nvlLigne, numero_ligne, page_fichier):
    """
    Remplace les valeurs de la ligne n°numero_ligne par celles de nouvelleLigne
    """
    page_fichier.delete_rows(numero_ligne)
    
    ajoutLigne(nvlLigne, page_fichier, numero_ligne)



def suppressionLigne_avec(info, clefColonne, page_fichier) :
    """
    Supprime la ligne de page_fichier ayant la clefColonne correspondant à l'info donnée en argument
    """
    
    ligne, numero_ligne = ligne_avec( info, clefColonne, donneeGoogleSheet(page_fichier) )
    
    page_fichier.delete_rows(numero_ligne)
    



    
# %%%% Cellules (Valeurs)    

def remplacerVal_ligne(nouvelleVal, clefColonne_aRemplacer, numero_ligne, page_fichier, x = None):
    
    clefs  = clefs_de_page(page_fichier)
    
    numero_colonne      = clefs.index(clefColonne_aRemplacer) + 1
    
    page_fichier.update_cell(numero_ligne, numero_colonne, str(nouvelleVal))
    
    

def remplacerVal_ligne_avec(nouvelleVal, clefColonne_aRemplacer, info, clefColonne_aRechercher, page_fichier):
    
    donnee = donneeGoogleSheet(page_fichier)
    clefs  = clefs_de_page(page_fichier)
    
    ligne, numero_ligne = ligne_avec(info, clefColonne_aRechercher, donnee)
    numero_colonne      = clefs.index(clefColonne_aRemplacer) + 1
    
    page_fichier.update_cell(numero_ligne, numero_colonne, str(nouvelleVal))
    


def ajoutVal_cellule(valeur_aAjouter, clefColonne_cellule, numero_ligne, page_fichier, typeObjetCellule = str):
    """
    typeObjetCellule peut valoir : int ou str
    """
    clefs  = clefs_de_page(page_fichier)
    
    numero_colonne      = clefs.index(clefColonne_cellule) + 1
    try :
        ancienneValeur  = typeObjetCellule( page_fichier.cell(numero_ligne, numero_colonne).value )
    except ValueError :
        ancienneValeur  = 0
    
    page_fichier.update_cell(numero_ligne, numero_colonne, str(ancienneValeur + valeur_aAjouter))



def ajoutVal_cellule_avec(valeur_aAjouter, clefColonne_cellule, info, clefColonne_aRechercher, page_fichier, typeObjetCellule = str):
    """
    typeObjetCellule peut valoir : int ou str
    """
    donnee = donneeGoogleSheet(page_fichier)
    clefs  = clefs_de_page(page_fichier)
    
    ligne, numero_ligne = ligne_avec(info, clefColonne_aRechercher, donnee)
    numero_colonne      = clefs.index(clefColonne_cellule) + 1
    
    ancienneValeur      = typeObjetCellule( page_fichier.cell(numero_ligne, numero_colonne).value )
    
    page_fichier.update_cell(numero_ligne, numero_colonne, str(ancienneValeur + valeur_aAjouter))





# %%% Mise en forme de Donnée ou de Liste

def dfToList(DataFrame) :
    """Transforme un DataFrame en Liste, le premier élément de la liste renvoyée est l'en-tete du DataFrame"""
    
    entete = list(DataFrame)
    donnee = DataFrame.values
    
    ListeFinale = [entete]
    for d in donnee :
        ListeFinale.append(list(d))
    
    return ListeFinale



def listeDonnee(donnee):
    """
    Renvoie la liste des données sous forme de liste de liste
    
    Les données en argument doivent être une liste de dictionaire
    """
    
    listeFinale = [ list(donnee[0]) ] # En-tête
    
    for d in donnee :
        listeFinale.append(list(d.values()))
        
    return listeFinale



def strListe(listeInitiale):
    """
    Applique la fonction str() à tout les éléments de listeInitiale
    
    listeInitiale doit être une liste de liste
    """    
    
    listeFinale = []
    listeInter  = []
    
    for i in listeInitiale :
        for a in i:
            listeInter.append(str(a))
        listeFinale.append(listeInter)
        listeInter = []
    
    return listeFinale





# %%% Recherche de ligne / cellule

def ligne_avec(info, clefColonne, donnee) :
    """
    Cette Fonction renvoie : 
        - le dictionnaire de la ligne du fichierGoogleSheet correspondant à l'info donnée en argument 
        - le numéro de la ligne dans fichierGoogleSheet
        
    Si aucune ligne ne correspond, elle renvoie None, None.
    """
        
    for i in range(len(donnee)) :
       
        if donnee[i][clefColonne] == info :
            return donnee[i], i+2

    return None, None


