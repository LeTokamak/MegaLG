# -*- coding: utf-8 -*-

"""
======================================================================================
===                                                                                ===
===                                     Phase 1                                    ===
===                                                                                ===
======================================================================================
                                          v1                                29/05/2021
"""


# Niveau C
import C___inscription as fIns


# Niveau B

# Niveau A
fGoo = fIns.fGoo
fDis = fIns.fDis
v    = fIns.v



async def lancementInscription():
    
    v.phaseEnCours = v.phase1
    await fDis.channelHistorique.edit(topic = v.phase1)   
    
    
#### Message de Inscription
    
    msgInscription = await fDis.channelInscription.fetch_message(fIns.idMessage_Inscription)
    await msgInscription.clear_reactions()
    await msgInscription.add_reaction(fDis.Emo_BabyYellow)
    
    
#### Nettoyage de Infos Joueurs
    
    nb_Joueurs_anc_partie = len( fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs) )
    
    if nb_Joueurs_anc_partie != 0 :
        fGoo.page1_InfoJoueurs.delete_rows(2, nb_Joueurs_anc_partie + 1)
        
    v.plantage()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Debut_Phase1 (ctx):
    await lancementInscription()