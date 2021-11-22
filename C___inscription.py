# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---            Niveau C - Fonctions d'Inscription et de Ré-Inscription             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


#Niveau B
import B___groupe      as fGrp

#Niveau A
fDis = fGrp.fDis
fGoo = fGrp.fGoo
fMeP = fGrp.fMeP
v    = fGrp.v

asyncio = fGrp.asyncio


Emo_Homme = "♂️"
Emo_Femme = "♀️"
    

# %% Inscription

async def fct_Inscription (membre_aInscrire):
    
    contenuMsg_Inscription = f"Inscription de {membre_aInscrire.mention} en cours..."
    msgAtt = await fDis.channelAttente.send( contenuMsg_Inscription )
    
    contenuMsg_Intro  =  "**Bonjour et Bienvenue sur le serveur du __Méga Loups-Garous__ !**\n"
    contenuMsg_Intro += f"Je suis le {fDis.userMdJ.mention} de la partie, et je suis très fier qu'une personne de plus soit intriguée par mon travail !\n"
    contenuMsg_Intro +=  "\n"
    contenuMsg_Intro +=  "Comme vous n'avez jamais jouer avant, vous allez devoir vous **Inscrire**, rassurez-vous c'est très rapide !\n"
    contenuMsg_Intro +=  "\n\n_ _"
    
    await membre_aInscrire.send(contenuMsg_Intro)
    
    
    
# =============================================================================
#### --- Récolte des données personnelles ---
# =============================================================================    

#### Sexe
    
    emojisEtReturns = [[Emo_Homme, "H"], [Emo_Femme, "F"]]

    contenuMsg_Sexe  =  "Dans un premier temps, il faut que vous choissiez votre **sexe** !\n"
    contenuMsg_Sexe +=  "> J'utilise cette info pour accorder mes phrases, pour qu'elles soient plus imersivent.\n"
    contenuMsg_Sexe +=  ">      *Alberte a été retrouvé·e mort·e chez lui/elle ce matin...* devient\n"
    contenuMsg_Sexe +=  ">      *Alberte a été retrouvée morte chez elle ce matin...*\n"
    contenuMsg_Sexe +=  "> \n"
    contenuMsg_Sexe +=  "> *Évidemment, rien ne vous empèche de mentir.*\n"
    contenuMsg_Sexe +=  "\n"
    contenuMsg_Sexe += f"Pour choisir le masculin, réagissez avec {Emo_Homme}, et pour le féminin ce sera {Emo_Femme}."
    
    msgSexe   = await membre_aInscrire.send( contenuMsg_Sexe                                    )
    choixSexe = await fDis.attente_Reaction( msgSexe        , membre_aInscrire, emojisEtReturns )
    
    choixConfirme = False
    
    while not choixConfirme :
    
        if   choixSexe == "H" : 
            contenuMsg_VerifSexe = "Donc ça sera **Monsieur**, c'est bien ça ?"
        else : 
            contenuMsg_VerifSexe = "Donc ça sera **Madame**, c'est bien ça ?"
            
        msgConfirmSexe = await membre_aInscrire.send    ( contenuMsg_VerifSexe                   )
        choixConfirme  = await fDis.attente_Confirmation( msgConfirmSexe      , membre_aInscrire )
        
        await msgConfirmSexe.delete()
        
        if not choixConfirme :
            if choixSexe == "H" : choixSexe = "F"
            else                : choixSexe = "H"
    
    
    
#### Pseudo
    
    if   choixSexe == "H" : deb_contenuMsg_Pseudo = "Très bien *Monsieur*"
    else                  : deb_contenuMsg_Pseudo = "Compris *Madame*"
    
    contenuMsg_Pseudo  = deb_contenuMsg_Pseudo + ", maintenant vous devez choisir votre **Pseudo** ?"

    await membre_aInscrire.send( contenuMsg_Pseudo )
    
    choixConfirme = False
    pseudo        = fMeP.MeF_Pseudo(membre_aInscrire.display_name)
    
    while not choixConfirme :
        
        contenuMsg_VerifPseudo  = f"Est-ce ce pseudo vous convient : **{pseudo}** ?\n"
        contenuMsg_VerifPseudo +=  "> *Votre pseudo a été mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
        
        msgConfirmPseudo = await membre_aInscrire.send( contenuMsg_VerifPseudo )
        choixConfirme    = await fDis.attente_Confirmation(msgConfirmPseudo, membre_aInscrire)
        
        if not choixConfirme :
            
            await msgConfirmPseudo.delete()
            await membre_aInscrire.send( "*Vous pouvez taper un nouveau pseudo !*" )
            
        msgReponsePseudo = await fDis.attente_Message( membre_aInscrire         )
        pseudo           = fMeP.MeF_Pseudo(            msgReponsePseudo.content )
    
    

    
    
    
# =============================================================================
#### --- Insertion de la nouvelle ligne à la 2eme ligne dans Infos Joueurs ---
# =============================================================================
    
    nvlLigne = { fGoo.clef_Sexe       : choixSexe                   , 
                 fGoo.clef_Pseudo     : pseudo                      ,
                 fGoo.clef_Groupe     : fGrp.GroupeParDefaut.numero , 
                 fGoo.clef_numVillage : 0                           ,
                 fGoo.clef_idDiscord  : membre_aInscrire.id          }
    
    fGoo.ajoutLigne(nvlLigne, fGoo.page1_InfoJoueurs)
    fGoo.ajoutLigne(nvlLigne, fGoo.page1_Archives   )
    
    
    
# =============================================================================
#### --- Suppression du role de Spectateur et/ou du role de Mort et Ajout du role de Joueur ---
# =============================================================================
    
    await membre_aInscrire.remove_roles(fDis.roleMorts, fDis.roleSpectateurs)                
    await membre_aInscrire.   add_roles(fDis.roleJoueurs                    )
    
    
    
# =============================================================================
#### --- Message de confirmation de l'inscription ---
# =============================================================================
    
    if   choixSexe == "H" : inscrit = "inscrit"
    else                  : inscrit = "inscrite"
    
    await membre_aInscrire      .send(f"**C'est bon {pseudo}, tu as bien été {inscrit} !**\nTu n'as plus qu'à attendre le début de la partie !" )
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyYellow}  |  Inscription de {membre_aInscrire.mention} : {pseudo}   |   ({choixSexe})")
    await msgAtt                .delete()    
    
    await fGrp.autorisation_SalonsGrp(membre_aInscrire, nvlLigne[fGoo.clef_Groupe])

    



# %% Ré-Inscription

AnciensJoueurs   = fGoo.donneeGoogleSheet(fGoo.page1_Archives)
listeidDisConnus = fGoo.colonne_avec(fGoo.page1_Archives, fGoo.clef_idDiscord)

async def ReInscription (membre_ReInscrit):
        
# =============================================================================
#### Récupération des données personnelles
# =============================================================================
    
    nvlLigne, num_ligne = fGoo.ligne_avec(membre_ReInscrit.id, fGoo.clef_idDiscord, AnciensJoueurs) 
    
    if nvlLigne[fGoo.clef_Pseudo] in ("None", None) :
        nvlLigne[fGoo.clef_Pseudo] = membre_ReInscrit.display_name
    
    fGoo.ajoutLigne(nvlLigne, fGoo.page1_InfoJoueurs)
    
    
# =============================================================================
#### Suppression du role de Spectateur et/ou du role de Mort et Ajout du role de Joueur
# =============================================================================
        
    await membre_ReInscrit.   add_roles(fDis.roleJoueurs                    )
    await membre_ReInscrit.remove_roles(fDis.roleSpectateurs, fDis.roleMorts) 
    
    await membre_ReInscrit      .send(f"**Salut {nvlLigne[fGoo.clef_Pseudo]}, tu as bien été reinscrit !**\nTu n'as plus qu'à attendre le début de la partie !")
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyOrange}  |  Ré-inscription de {membre_ReInscrit.mention} : {nvlLigne[fGoo.clef_Pseudo]}   |   {nvlLigne[fGoo.clef_Groupe]}")

    await fGrp.autorisation_SalonsGrp(membre_ReInscrit, nvlLigne[fGoo.clef_Groupe])





# %% Event Inscription

idMessage_Inscription = 864264877160792064

erreurIns_phase1     = "**ERREUR** - Les inscriptions **ne sont pas** ouvertes pour l'instant..."
erreurIns_dejaJoueur = "**ERREUR** - Vous êtes **déjà** inscrit !"

messagIns_reInscript = "**Vous avez déjà participer à une ancienne partie.**\nVous avez donc été ré-inscrit !"


async def evt_Inscription (membre_voulant_sIncrire):
    
    nom_taches = [ tache.get_name() for tache in asyncio.all_tasks() ]
    
    nomTache_ReInscription = f"ReInscription de {membre_voulant_sIncrire}"
    nomTache_Inscription   = f"Inscription de {membre_voulant_sIncrire}"
    
#### Cas 1 : Est on en phase d'Inscription ?
    
    if   v.phaseEnCours != v.phase1 :
        await membre_voulant_sIncrire.send( erreurIns_phase1     )
    
    
    
#### Cas 2 : Est il déjà inscrit ?
    
    elif fDis.roleJoueurs in membre_voulant_sIncrire.roles :
        await membre_voulant_sIncrire.send( erreurIns_dejaJoueur )
    
    
    
#### Cas 3 : La fonction est-elle déjà lancée ?
    
    elif nomTache_ReInscription in nom_taches  or  nomTache_Inscription in nom_taches :
        pass
    
    
    
#### Cas 4 : A-t-il déjà participé à une partie ?
    
    elif membre_voulant_sIncrire.id in listeidDisConnus :
        await membre_voulant_sIncrire.send( messagIns_reInscript )
        asyncio.create_task( ReInscription( membre_voulant_sIncrire ), name = nomTache_ReInscription )
    
    
    
#### Sinon à tous ces cas : Inscription
    
    else :
        asyncio.create_task( fct_Inscription( membre_voulant_sIncrire ), name = nomTache_Inscription )





# %%% Réaction Inscription

async def reaction_Inscription():
    
    def verifReInscription(payload):
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifPhase   = v.phaseEnCours     == v.phase1
        verifMessage = payload.message_id == idMessage_Inscription
        verifEmoji   = str(payload.emoji) == fDis.Emo_BabyYellow
        
        return verifUser  and  verifPhase and verifMessage and verifEmoji
    
#### Boucle infini
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifReInscription)
        await evt_Inscription(payload.member)
        
        
        
        
        
# %% Modification des infos personnelles

async def fct_modif_infosPerso(user_a_maj):
    
    contenuMsg_Inscription = f"MàJ des infos personnelles de {user_a_maj.mention} en cours..."
    msgAtt = await fDis.channelAttente.send( contenuMsg_Inscription )
    
        
    
# =============================================================================
#### Anciennes données persos
# =============================================================================
    
    ancienne_ligne_joueur, nb_ligne_InfoJoueurs = fGoo.ligne_avec(user_a_maj.id, fGoo.clef_idDiscord, fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs))
    
    if ancienne_ligne_joueur[fGoo.clef_Sexe] == "H" : ancien_sexe =  "un Homme"
    else                                            : ancien_sexe = "une Femme"
    
    contenuMsg_Intro  =  "Bonjour, vous voulez changer vos infos personnelles, voilà ce que je sais sur vous :\n"
    contenuMsg_Intro += f"> Vous êtes **{ancien_sexe}**, et je vous appele **{ancienne_ligne_joueur[fGoo.clef_Pseudo]}**.\n"
    contenuMsg_Intro +=  "\n\n_ _"
    
    await user_a_maj.send(contenuMsg_Intro)
    
    
    
# =============================================================================
#### --- MaJ des données personnelles ---
# =============================================================================    

#### Sexe
    
    if ancienne_ligne_joueur[fGoo.clef_Sexe] == "H" : eventuel_nouv_sexe,  texte_eventuel_nouv_sexe,  Emo_eventuel_nouv_sexe  =  "F", "une **Femme**" , Emo_Femme
    else                                            : eventuel_nouv_sexe,  texte_eventuel_nouv_sexe,  Emo_eventuel_nouv_sexe  =  "H", "un **Homme**"  , Emo_Homme

    emojisEtReturns = [[Emo_eventuel_nouv_sexe, eventuel_nouv_sexe], ["❌", None]]

    contenuMsg_Sexe  = f"Est-ce que vous souhaitez devenir {texte_eventuel_nouv_sexe} ?\n"
    contenuMsg_Sexe +=  "> Pour rappel, j'utilise cette info pour accorder mes phrases, pour qu'elles soient plus imersivent.\n"
    contenuMsg_Sexe +=  ">      *Alberte a été retrouvé·e mort·e chez lui/elle ce matin...* devient\n"
    contenuMsg_Sexe +=  ">      *Alberte a été retrouvée morte chez elle ce matin...*\n"
    contenuMsg_Sexe +=  "> \n"
    contenuMsg_Sexe +=  "> *Évidemment, rien ne vous empèche de mentir.* 😈\n"
    contenuMsg_Sexe +=  "\n"
    contenuMsg_Sexe += f"Choisissez {Emo_eventuel_nouv_sexe} pour devenir {texte_eventuel_nouv_sexe}, ou la ❌ pour ne pas changer de sexe."
    
    msgSexe         = await user_a_maj.send(       contenuMsg_Sexe                              )
    choix_nouv_Sexe = await fDis.attente_Reaction( msgSexe        , user_a_maj, emojisEtReturns )
    
    choixConfirme = False
    
    while not choixConfirme  and  choix_nouv_Sexe != None :
    
        if   choix_nouv_Sexe == "H" : contenuMsg_VerifSexe = "Donc ça sera **Monsieur**, c'est bien ça ?"
        else                        : contenuMsg_VerifSexe = "Donc ça sera **Madame**, c'est bien ça ?"
            
        msgConfirmSexe = await user_a_maj.send(           contenuMsg_VerifSexe             )
        choixConfirme  = await fDis.attente_Confirmation( msgConfirmSexe      , user_a_maj )
        
        await msgConfirmSexe.delete()
        
        if not choixConfirme :
            if choix_nouv_Sexe == "H" : choix_nouv_Sexe = "F"
            else                      : choix_nouv_Sexe = "H"
    
    if choix_nouv_Sexe == None : 
        choix_nouv_Sexe = ancienne_ligne_joueur[fGoo.clef_Sexe]
    
    
    
#### Pseudo
    
    if   choix_nouv_Sexe == "H" : deb_contenuMsg_Pseudo = "Très bien *Monsieur*"
    else                        : deb_contenuMsg_Pseudo = "Compris *Madame*"
    
    
    contenuMsg_Modif_Pseudo = deb_contenuMsg_Pseudo + f", est-ce que vous voulez modifier votre ancien **Pseudo** ({ancienne_ligne_joueur[fGoo.clef_Pseudo]}) ?\n"
    
    msgConfirm_Modif_Pseudo = await user_a_maj.send(           contenuMsg_Modif_Pseudo             )
    modif_pseudo_demandee   = await fDis.attente_Confirmation( msgConfirm_Modif_Pseudo, user_a_maj )
    
    if modif_pseudo_demandee :
        
        contenuMsg_Pseudo  =  "Le **prochain message** que vous enverrez sera votre __nouveau__ **pseudo** (après l'avoir confirmé, comme pour le sexe).\n"
        
        await user_a_maj.send( contenuMsg_Pseudo )
        
        choixConfirme = False
        
        while not choixConfirme :
        
            msgReponsePseudo = await fDis.attente_Message( user_a_maj               )
            nouv_pseudo      = fMeP.MeF_Pseudo(            msgReponsePseudo.content )
            
            
            contenuMsg_VerifPseudo  = f"Est-ce que ce pseudo vous convient **{nouv_pseudo}** ?\n"
            contenuMsg_VerifPseudo +=  "> *Votre pseudo a été mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
            
            msgConfirmPseudo = await user_a_maj.send(           contenuMsg_VerifPseudo             )
            choixConfirme    = await fDis.attente_Confirmation( msgConfirmPseudo      , user_a_maj )
            
            await msgConfirmPseudo.delete()
            
            if not choixConfirme :
                await user_a_maj.send( "*Vous pouvez taper un nouveau pseudo !*" )
    
    else :
        nouv_pseudo = ancienne_ligne_joueur[fGoo.clef_Pseudo]
        
    
    
    
    
# =============================================================================
#### --- Remplacement de la ligne de Info Joueurs ---
# =============================================================================
    
    nvlLigne_InfoJoueurs = { fGoo.clef_Matricule    : ancienne_ligne_joueur[fGoo.clef_Matricule]    ,
                            
                             fGoo.clef_Sexe         : choix_nouv_Sexe                               ,
                             fGoo.clef_Pseudo       : nouv_pseudo                                   ,
                             
                             fGoo.clef_Groupe       : ancienne_ligne_joueur[fGoo.clef_Groupe]       , 
                             fGoo.clef_numVillage   : ancienne_ligne_joueur[fGoo.clef_numVillage]   ,
                             
                             fGoo.clef_idDiscord    : user_a_maj.id                                 ,
                             
                             fGoo.clef_Role         : ancienne_ligne_joueur[fGoo.clef_Role]         ,
                             fGoo.clef_caractRoles  : ancienne_ligne_joueur[fGoo.clef_caractRoles]  ,
                             fGoo.clef_caractJoueur : ancienne_ligne_joueur[fGoo.clef_caractJoueur]  }
    
    fGoo.remplacerLigne(nvlLigne_InfoJoueurs, nb_ligne_InfoJoueurs, fGoo.page1_InfoJoueurs)
    
    
    
# =============================================================================
#### --- Remplacement de la ligne des Archives ---
# =============================================================================
    
    x, nb_ligne_Archives = fGoo.ligne_avec(user_a_maj.id, fGoo.clef_idDiscord, fGoo.donneeGoogleSheet(fGoo.page1_Archives))
    
    nvlLigne_Archives = { fGoo.clef_Sexe       : choix_nouv_Sexe             , 
                          fGoo.clef_Pseudo     : nouv_pseudo                 ,
                          
                          fGoo.clef_Groupe     : fGrp.GroupeParDefaut.numero , 
                          fGoo.clef_numVillage : 0                           ,
                          
                          fGoo.clef_idDiscord  : user_a_maj.id                }
    
    
    
    fGoo.remplacerLigne(nvlLigne_Archives, nb_ligne_Archives, fGoo.page1_Archives)
    
    
    
# =============================================================================
#### --- Message de confirmation de la modification ---
# =============================================================================   
    
    await user_a_maj.send(f"C'est bon {nouv_pseudo}, tes infos personnelles ont bien été changées !" )
    await msgAtt    .delete()    





# %%% === Commande ===

erreurMaJ_pasJoueur = "**ERREUR** - Vous **n'êtes pas** inscrit !"

@fDis.bot.command(aliases = ["Modif", "modif", "MaJ_Infos_Perso", "MaJ", "maj"])
async def Modif_Infos_Perso(ctx):
    
    membre_a_modif = fDis.serveurMegaLG.get_member(ctx.author.id)
    
    if   fDis.roleJoueurs not in membre_a_modif.roles :
        await membre_a_modif.send( erreurMaJ_pasJoueur )
    
    else :
        await fct_modif_infosPerso(membre_a_modif)