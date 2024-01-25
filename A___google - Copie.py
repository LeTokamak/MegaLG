# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---            Niveau A - Fonctions et Constantes liées à Google Drive             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

# %%% Modification de page de fichier Google Sheet
   
# %%%% Cellules (Valeurs)

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
    
