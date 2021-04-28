# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---                    Niveau D - Fonction de gestion d'un Tour                    ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

# Niveau D
import D_fct_Village         as fVlg

# Niveau C
fHab = fVlg.fHab

# Niveau B

# Niveua A
fGoo = fHab.fGoo
fDis = fHab.fDis
fMeP = fHab.fMeP
v    = fHab.v



rd      = fHab.rd
asyncio = fHab.asyncio







async def Tour():
    
    await fHab.redef_TousLesHabitants()
    
#### Nuit
    
    await nuit_TousLesVillages()
    
    
    
#### Début de la Journée
    
    await debJournee_TousLesVillages()
    
    
    
#### Vote (Elimination / Election Maire)
    
    await vote_TousLesVillages()
    
    
    
#### Rapports municipaux Vespéraux
    
    await fHab.redef_TousLesHabitants()
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
    
    
    
#### Plantage Final
    
    await fDis.channelHistorique.send(f"{fDis.roleMaitre.mention}\nLe soleil ne va plus tardé à se coucher !\nIl est {v.maintenant()}")
    
# L'objectif est de saturer la ram (512 Mo) du serveur, pour qu'il plante, et redémarre automatiquement le programme  

    erreur = []
    
    while True : 
        erreur.append(erreur)





# %% Sous-Fonctions de Tour

async def nuit_TousLesVillages():

#### Gestion de la nuit
    
    for vlg in fVlg.TousLesVillages :
        asyncio.Task(vlg.gestion_nuit())



#### Application de la nuit

    if v.nbTours != 0 :
        for vlg in fVlg.TousLesVillages :
            await vlg.application_nuit()





async def debJournee_TousLesVillages():
    
    v.nbTours += 1
    await fDis.channelHistorique.send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.dem)}\n\n⬢⬢⬢\n```")
    await fDis.channelHistorique.edit(topic = f"Tour n°{v.nbTours}")
    
#### Début de la Journée - Partie 1
    
    for vlg in fVlg.TousLesVillages :
        await vlg.debutJournee_Partie1()
    
    
    
#### Redeffinition de ToutesLesPersonnes (pour les Hirondelles)
    
    await fHab.redef_TousLesHabitants()
    
    
    
#### Début de la Journée - Partie 2
    
    for vlg in fVlg.TousLesVillages :
        await vlg.debutJournee_Partie2()
    
    
    
#### Sauvegarde de Infos Joueurs
    
    nbColonnes = 11
    nbLignes   = len(fHab.TousLesHabitants) + 1
    
    feuilleDuJour = fGoo.Sauvegarde.add_worksheet(f"Matinée {str(v.dem)[:10]}", nbLignes, nbColonnes)
    feuilleDuJour.insert_rows( fGoo.page1_InfoJoueurs.get() )
    
    
    
    
    
async def vote_TousLesVillages():
    
    for vlg in fVlg.TousLesVillages :
        if "Le village a deja elu un maire" :
            asyncio.Task( vlg.gestion_voteEliminatoire() )
            
        else :
            asyncio.Task( "Election d'un nouveau maire"  )
    