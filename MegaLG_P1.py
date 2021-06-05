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
import C_fct_Inscription as fIns


# Niveau B
fGrp = fIns.fGrp


# Niveau A
fGoo = fGrp.fGoo
fDis = fGrp.fDis
fMeP = fGrp.fMeP
v    = fGrp.v



rd      = fGrp.rd
asyncio = fGrp.asyncio





# %% Commandes

erreurIns_dejaJoueur = "**ERREUR** - Vous êtes **déjà** inscrit !"
erreurIns_phase1     = "**ERREUR** - Les inscriptions **ne sont pas** ouvertes pour l'instant..."
messagIns_reInscript = "**Vous avez déjà participer à une ancienne partie.**\nVous avez donc été ré-inscrit !"

async def cmd_Inscription(membre_voulantSIncrire):
    
    if   fDis.roleJoueurs in membre_voulantSIncrire.roles :
        await membre_voulantSIncrire.send( erreurIns_dejaJoueur )
    
    
    elif v.phaseEnCours != v.phase1 :
        await membre_voulantSIncrire.send( erreurIns_phase1     )
    
    
    elif membre_voulantSIncrire.id in fIns.listeidDisConnus :
        await membre_voulantSIncrire.send( messagIns_reInscript )
        
        await fIns.ReInscription(membre_voulantSIncrire)
    
    
    else :
        await fIns.Inscription(membre_voulantSIncrire)





# %% Events

# %%% Réactions

async def reaction_reInscription():
    
    def verifReInscription(payload):
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifPhase   = v.phaseEnCours     == v.phase1
        verifMessage = payload.message_id == fIns.idMessage_ReInscription
        verifEmoji   = str(payload.emoji) == fDis.Emo_BabyOrange
        
        return verifUser  and  verifPhase and verifMessage and verifEmoji
    
#### Boucle infini
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifReInscription)
        await fIns.evt_ReInscription(payload.member)





async def reaction_Groupe():
    
    def verifGroupe(payload):
        salon        = fDis.serveurMegaLG.get_channel(payload.channel_id)

#### Si la réaction n'a pas été faite dans un salon du serveur
        if salon == None :
            return False

#### Sinon la réaction a été faite dans un salon du serveur
        else :
            verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
            
            verifPhase   = v.phaseEnCours == v.phase1
            verifCategCh = salon.category == fDis.CategoryChannel_GestionGrp
        
            return verifUser  and  verifPhase and verifCategCh
    
#### Boucle infini
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifGroupe)
        await fGrp.evt_ChangementGroupe(payload.member, payload.message_id, str(payload.emoji))





# %% Fonctions 

async def lancementInscription():
    
    v.phaseEnCours = v.phase1
    await fDis.channelHistorique.edit(topic = v.phase1)   
    
    
#### Message de Ré-Inscription
    
    msgReInscription = await fDis.channelAccueil.fetch_message(fIns.idMessage_ReInscription)
    await msgReInscription.clear_reactions()
    await msgReInscription.add_reaction(fDis.Emo_BabyOrange)
    
    
#### Nettoyage de Infos Joueurs

    a = "A programmer"