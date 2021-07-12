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
fGrp = fIns.fGrp


# Niveau A
fGoo = fGrp.fGoo
fDis = fGrp.fDis
fMeP = fGrp.fMeP
v    = fGrp.v



rd      = fGrp.rd
asyncio = fGrp.asyncio


async def lancementInscription():
    
    v.phaseEnCours = v.phase1
    await fDis.channelHistorique.edit(topic = v.phase1)   
    
    
#### Message de Ré-Inscription
    
    msgReInscription = await fDis.channelAccueil.fetch_message(fIns.idMessage_ReInscription)
    await msgReInscription.clear_reactions()
    await msgReInscription.add_reaction(fDis.Emo_BabyOrange)
    
    
#### Nettoyage de Infos Joueurs

    pass
    
    

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Debut_Phase1 (ctx):
    await lancementInscription()

