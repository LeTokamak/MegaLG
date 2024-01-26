 # -*- coding: utf-8 -*-

"""
Créé par Clément Campana

######################################################################################
######################################################################################
#############                                                            #############
#############               Méga Loups-Garous sur Discord                #############
#############                                                            #############
######################################################################################
######################################################################################

Version F-rond                               𝓯1                             03/09/2022
"""

version = "𝓯1.0"


# import MegaLG_Test

import os
import sys

os.chdir(f"{os.getcwd()}\\src")
sys.path.append(os.getcwd())

# Phase
import phase_0    as fP0
import phase_1    as fP1
import phase_2    as fP2
fP3 = fP2.fP3


# Niveau F

# Niveau E
fVlg = fP2.fVlg


# Niveau D

# Niveau C
fHab = fVlg.fHab


# Niveau B
fGrp = fHab.fGrp


# Niveau A
fDis = fHab.fDis
v    = fHab.v


asyncio = v.asyncio







# %% === on_ready ===

@fDis.bot.event
async def on_ready():
    
    fDis.def_constantes_discord()
    
#### Recherche de la phase en cours
    
    v.phaseEnCours = fDis.channelHistorique.topic[ : len(v.phase0) ]
    
    msgIntro = await fDis.channelHistorique.send(f"```⬢ -  Je suis connecté ! ({version} | {v.phaseEnCours})  - ⬢```\n`{v.maintenant()}` - Début du 'on_ready'")
    
    
    
    
    
#### Ajout du role ISEN Nantes aux membres du club étant sur le serveur

    # await fP0.gestion_role_iseniens()
    
    
    
    
    
#### Redéfinition Groupes, Habitants et Villages
    
    await fGrp.redef_groupesExistants()
    
    fVlg.redef_villagesExistants()
    await fHab.redef_TousLesHabitants()
    
    
    
    
    
#### Lancement des events

##   Réaction à un message

    asyncio.create_task( fP0.          ajout_roleArtisans()  , name = "Ajout du rôle d'Artisant" )
    asyncio.create_task( fP1.fIns.     reaction_Inscription(), name = "Inscription"              )
    asyncio.create_task( fP1.fIns.fGrp.reaction_Groupe()     , name = "Changement de Groupe"     )

##   Envoie d'un message

    asyncio.create_task( fVlg.message_voteVillage()          , name = "Vote du village"          )
    asyncio.create_task( fVlg.message_voteLoupGarou()        , name = "Vote des Loups-Garous"    )
    
    
    
    
    
#### Lancement des attendes d'épitaphe
    
    async for message in fDis.channelAttente.history():
        
        if fDis.Emo_Red == message.content.split()[0] :
            asyncio.create_task( fHab.cimetiere(message = message, rappelDeFonction = True), name = f"Re-Lancement de Cimetière de {message.content}.")
    
    await msgIntro.edit( content = msgIntro.content + f"\n`{v.maintenant()}` - Fin du 'on_ready'")
    
    
    
    
    
#### Phase 3 - Récupération du numéro de Tour et Lancement du Tour
    
    if v.phaseEnCours == v.phase3 :
        # Le topic de channelHistorique est de la forme "Phase 3 - Tour n°45"
        
        v.nbTours = int( fDis.channelHistorique.topic.split() [-1] [2:] )
        
        await fP3.attente_lancementTour()





fDis.bot.run(fDis.tokenMJ)