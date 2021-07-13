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
v    = fGrp.v



Emo_Homme = "♂️"
Emo_Femme = "♀️"

def MeF_Prenom (texte) :
    """
    Cette fonction Met en Forme la variable texte (str) pour les transformer en Prénom
        "   JeAn-cléMENt frANçoiS       "  ==>  "Jean-Clément François"
    """
    
    # 1er split pour les espaces "___cléMENt__" et gestion des Majuscules
    
    listePrenoms = texte.split()
    listePrenoms_MeF = []
    
    for p in listePrenoms :
        listePrenoms_MeF.append( p[0].upper() + p[1:].lower() )
        
    prenom_Maj = " ".join( listePrenoms_MeF )
    
    
    
    # 2nd split pour la gestion des Majuscules après les "-" (prénoms composées)
    
    listePrenoms = prenom_Maj.split("-")
    listePrenoms_MeF = []
    
    for p in listePrenoms :
        listePrenoms_MeF.append( p[0].upper() + p[1:] )
    
    return "-".join( listePrenoms_MeF )
    


    

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
    
    
    
#### Prénom
    
    if   choixSexe == "H" : deb_contenuMsg_Prenom = "Très bien *Monsieur*"
    else                  : deb_contenuMsg_Prenom = "Compris *Madame*"
    
    contenuMsg_Prenom  = deb_contenuMsg_Prenom + ", maintenant quel est votre **Prénom** ?\n"
    contenuMsg_Prenom +=  "> Le **prochain message** que vous enverrez sera votre **prénom** (après l'avoir confirmé, comme pour le sexe).\n"
    contenuMsg_Prenom +=  "> Vous avez le droit aux espaces et aux tirets."
    
    await membre_aInscrire.send( contenuMsg_Prenom )
    
    choixConfirme = False
    
    while not choixConfirme :
    
        msgReponsePrenom = await fDis.attente_Message( membre_aInscrire )
        prenom           = MeF_Prenom(msgReponsePrenom.content)
        
        contenuMsg_VerifPrenom  = f"Est-ce bien votre prénom **{prenom}** ?\n"
        contenuMsg_VerifPrenom +=  "> *Votre prénom a été mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
        
        msgConfirmPrenom = await membre_aInscrire.send( contenuMsg_VerifPrenom )
        choixConfirme    = await fDis.attente_Confirmation(msgConfirmPrenom, membre_aInscrire)
        
        await msgConfirmPrenom.delete()
        
        if not choixConfirme :
            await membre_aInscrire.send( "*Vous pouvez taper un nouveau prénom !*" )
    
    
    
#### Nom
    
    contenuMsg_Nom  = f"Et c'est {prenom} comment ?\n"
    contenuMsg_Nom +=  "> Le **prochain message** que vous enverrez sera votre **nom** (après l'avoir confirmé).\n"
    contenuMsg_Nom +=  "> Vous avez le droit aux espaces et aux tirets."
    
    await membre_aInscrire.send( contenuMsg_Nom )
    
    choixConfirme = False
    
    while not choixConfirme :
    
        msgReponseNom = await fDis.attente_Message( membre_aInscrire )
        nom           = " ".join( msgReponseNom.content.split() ).upper()
        
        contenuMsg_VerifNom  = f"Est-ce bien votre nom **{nom}** ?\n"
        contenuMsg_VerifNom +=  "> *Votre nom est mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
        
        msgConfirmNom = await membre_aInscrire.send( contenuMsg_VerifNom )
        choixConfirme = await fDis.attente_Confirmation(msgConfirmNom, membre_aInscrire)
        
        await msgConfirmNom.delete()
        
        if not choixConfirme :
            await membre_aInscrire.send( "*Vous pouvez taper un nouveau nom !*" )
    
    
    
# =============================================================================
#### --- Insertion de la nouvelle ligne à la 2eme ligne dans Infos Joueurs ---
# =============================================================================
    
    nvlLigne = { fGoo.clef_Sexe       : choixSexe                   , 
                 fGoo.clef_Prenom     : prenom                      ,
                 fGoo.clef_Nom        : nom                         , 
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
    
    await membre_aInscrire      .send(f"**C'est bon {prenom}, tu as bien été {inscrit} !**\nTu n'as plus qu'à attendre le début de la partie !" )
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyYellow}  |  Inscription de {membre_aInscrire.mention} : {prenom} {nom}   |   ({choixSexe})")
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
    
    fGoo.ajoutLigne(nvlLigne, fGoo.page1_InfoJoueurs)
    
    
# =============================================================================
#### Suppression du role de Spectateur et/ou du role de Mort et Ajout du role de Joueur
# =============================================================================
        
    await membre_ReInscrit.   add_roles(fDis.roleJoueurs                    )
    await membre_ReInscrit.remove_roles(fDis.roleSpectateurs, fDis.roleMorts) 
    
    await membre_ReInscrit      .send(f"**Salut {nvlLigne[fGoo.clef_Prenom]}, tu as bien été reinscrit !**\nTu n'as plus qu'à attendre le début de la partie !")
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyOrange}  |  Ré-inscription de {membre_ReInscrit.mention} : {nvlLigne[fGoo.clef_Prenom]} {nvlLigne[fGoo.clef_Nom]}   |   {nvlLigne[fGoo.clef_Groupe]}")

    await fGrp.autorisation_SalonsGrp(membre_ReInscrit, nvlLigne[fGoo.clef_Groupe])



"""

idMessage_ReInscription = 850873077617000488

erreurReI_joueurInconu  = "**ERREUR** - Vous n'avez pas participer à la partie précédente, vous ne pouvez donc pas vous ré-inscrire."
erreurReI_joueurInconu += "\n> Pour vous inscrire, taper la commande **!Inscription** (**!i**)."
erreurReI_joueurInconu += "\n> *Si vous avez un problème, n'hésitez pas à envoyer un message privé à Clément Campana.*"

erreurReI_dejaJoueur    = "**ERREUR** - Vous êtes **déjà** inscrit !"

async def evt_ReInscription (membre):

    if   membre.id not in listeidDisConnus :
        await membre.send( erreurReI_joueurInconu )
    
    elif fDis.roleJoueurs in membre.roles :
        await membre.send( erreurReI_dejaJoueur )
        
    else :
        await ReInscription(membre)
        




# %% Commande Inscription

erreurIns_dejaJoueur = "**ERREUR** - Vous êtes **déjà** inscrit !"
erreurIns_phase1     = "**ERREUR** - Les inscriptions **ne sont pas** ouvertes pour l'instant..."
messagIns_reInscript = "**Vous avez déjà participer à une ancienne partie.**\nVous avez donc été ré-inscrit !"

async def cmd_Inscription(user_voulantSIncrire):
    
    membre_voulantSIncrire = fDis.serveurMegaLG.get_member(user_voulantSIncrire.id)
    
    if   fDis.roleJoueurs in membre_voulantSIncrire.roles :
        await membre_voulantSIncrire.send( erreurIns_dejaJoueur )
    
    
    elif v.phaseEnCours != v.phase1 :
        await membre_voulantSIncrire.send( erreurIns_phase1     )
    
    
    elif membre_voulantSIncrire.id in listeidDisConnus :
        await membre_voulantSIncrire.send( messagIns_reInscript )
        
        await ReInscription(membre_voulantSIncrire)
    
    
    else :
        await fct_Inscription(membre_voulantSIncrire)



@fDis.bot.command()
async def Inscription (ctx) :
    await cmd_Inscription(ctx.author)
    
@fDis.bot.command()
async def inscription (ctx) :
    await cmd_Inscription(ctx.author)
    
@fDis.bot.command()
async def I (ctx) :
    await cmd_Inscription(ctx.author)
    
@fDis.bot.command()
async def i (ctx) :
    await cmd_Inscription(ctx.author)
    
"""

# %% Event Inscription

idMessage_Inscription = 864264877160792064

erreurIns_phase1     = "**ERREUR** - Les inscriptions **ne sont pas** ouvertes pour l'instant..."
erreurIns_dejaJoueur = "**ERREUR** - Vous êtes **déjà** inscrit !"

messagIns_reInscript = "**Vous avez déjà participer à une ancienne partie.**\nVous avez donc été ré-inscrit !"


async def evt_Inscription (membre_voulant_sIncrire):
    
#### Cas 1 : Est on en phase d'Inscription ?
    
    if   v.phaseEnCours != v.phase1 :
        await membre_voulant_sIncrire.send( erreurIns_phase1     )
    
    
    
#### Cas 2 : Est il déjà inscrit ?
    
    elif fDis.roleJoueurs in membre_voulant_sIncrire.roles :
        await membre_voulant_sIncrire.send( erreurIns_dejaJoueur )
    
    
    
#### Cas 3 : A-t-il déjà participé à une partie ?
    
    elif membre_voulant_sIncrire.id in listeidDisConnus :
        await membre_voulant_sIncrire.send( messagIns_reInscript )
        await ReInscription( membre_voulant_sIncrire )
    
    
    
#### Sinon à tous ces cas : Inscription
    
    else :
        await fct_Inscription( membre_voulant_sIncrire )





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
    
    contenuMsg_Inscription = f"MaJ des infos personnelles de {user_a_maj.mention} en cours..."
    msgAtt = await fDis.channelAttente.send( contenuMsg_Inscription )
    
        
    
# =============================================================================
#### Anciennes données persos
# =============================================================================
    
    ancienne_ligne_joueur, nb_ligne_InfoJoueurs = fGoo.ligne_avec(user_a_maj.id, fGoo.clef_idDiscord, fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs))
    
    if ancienne_ligne_joueur[fGoo.clef_Sexe] == "H" : ancien_sexe =  "un Homme"
    else                                            : ancien_sexe = "une Femme"
    
    contenuMsg_Intro  =  "Bonjour, vous voulez changer vos infos personnelles, voilà ce que je sais sur vous :\n"
    contenuMsg_Intro += f"> Vous êtes **{ancien_sexe}**, et vous vous appelez **{ancienne_ligne_joueur[fGoo.clef_Prenom]} {ancienne_ligne_joueur[fGoo.clef_Nom]}**.\n"
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
    contenuMsg_Sexe +=  "> *Évidemment, rien ne vous empèche de mentir.*\n"
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
    
    
    
#### Prénom
    
    if   choix_nouv_Sexe == "H" : deb_contenuMsg_Prenom = "Très bien *Monsieur*"
    else                        : deb_contenuMsg_Prenom = "Compris *Madame*"
    
    
    contenuMsg_Modif_Prenom = deb_contenuMsg_Prenom + f", est-ce que vous voulez modifier votre ancien **Prénom** ({ancienne_ligne_joueur[fGoo.clef_Prenom]}) ?\n"
    
    msgConfirm_Modif_Prenom = await user_a_maj.send(           contenuMsg_Modif_Prenom             )
    modif_prenom_demandee   = await fDis.attente_Confirmation( msgConfirm_Modif_Prenom, user_a_maj )
    
    if modif_prenom_demandee :
        
        contenuMsg_Prenom  =  "Le **prochain message** que vous enverrez sera votre __nouveau__ **prénom** (après l'avoir confirmé, comme pour le sexe).\n"
        contenuMsg_Prenom +=  "> Vous avez le droit aux espaces et aux tirets."
        
        await user_a_maj.send( contenuMsg_Prenom )
        
        choixConfirme = False
        
        while not choixConfirme :
        
            msgReponsePrenom = await fDis.attente_Message( user_a_maj               )
            nouv_prenom      = MeF_Prenom(                 msgReponsePrenom.content )
            
            
            contenuMsg_VerifPrenom  = f"Est-ce bien votre prénom **{nouv_prenom}** ?\n"
            contenuMsg_VerifPrenom +=  "> *Votre prénom a été mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
            
            msgConfirmPrenom = await user_a_maj.send(           contenuMsg_VerifPrenom             )
            choixConfirme    = await fDis.attente_Confirmation( msgConfirmPrenom      , user_a_maj )
            
            await msgConfirmPrenom.delete()
            
            if not choixConfirme :
                await user_a_maj.send( "*Vous pouvez taper un nouveau prénom !*" )
    
    else :
        nouv_prenom = ancienne_ligne_joueur[fGoo.clef_Prenom]
    
    
    
#### Nom
        
    contenuMsg_Modif_Nom = f"Et enfin, est-ce que vous voulez modifier votre ancien **Nom** ({ancienne_ligne_joueur[fGoo.clef_Nom]}) ?"
    
    msgConfirm_Modif_Nom = await user_a_maj.send(           contenuMsg_Modif_Nom             )
    modif_nom_demandee   = await fDis.attente_Confirmation( msgConfirm_Modif_Nom, user_a_maj )
    
    if modif_nom_demandee :
        
        contenuMsg_Nom  =  " Le **prochain message** que vous enverrez sera votre __nouveau__ **nom** (après l'avoir confirmé).\n"
        contenuMsg_Nom +=  "> Vous avez le droit aux espaces et aux tirets."
        
        await user_a_maj.send( contenuMsg_Nom )
        
        choixConfirme = False
        
        while not choixConfirme :
        
            msgReponseNom = await fDis.attente_Message( user_a_maj )
            nouv_nom      = " ".join( msgReponseNom.content.split() ).upper()
            
            contenuMsg_VerifNom  = f"Est-ce bien votre nom **{nouv_nom}** ?\n"
            contenuMsg_VerifNom +=  "> *Votre nom est mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
            
            msgConfirmNom = await user_a_maj.send(           contenuMsg_VerifNom             )
            choixConfirme = await fDis.attente_Confirmation( msgConfirmNom      , user_a_maj )
            
            await msgConfirmNom.delete()
            
            if not choixConfirme :
                await user_a_maj.send( "*Vous pouvez taper un nouveau nom !*" )
            
    else :
        nouv_nom = ancienne_ligne_joueur[fGoo.clef_Nom]
    
    
    
# =============================================================================
#### --- Remplacement de la ligne de Info Joueurs ---
# =============================================================================
    
    nvlLigne_InfoJoueurs = { fGoo.clef_Matricule    : ancienne_ligne_joueur[fGoo.clef_Matricule]    ,
                            
                             fGoo.clef_Sexe         : choix_nouv_Sexe                               ,
                             fGoo.clef_Prenom       : nouv_prenom                                   ,
                             fGoo.clef_Nom          : nouv_nom                                      ,
                             
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
                          fGoo.clef_Prenom     : nouv_prenom                 ,
                          fGoo.clef_Nom        : nouv_nom                    ,
                          
                          fGoo.clef_Groupe     : fGrp.GroupeParDefaut.numero , 
                          fGoo.clef_numVillage : 0                           ,
                          
                          fGoo.clef_idDiscord  : user_a_maj.id                }
    
    
    
    fGoo.remplacerLigne(nvlLigne_Archives, nb_ligne_Archives, fGoo.page1_Archives)
    
    
    
# =============================================================================
#### --- Message de confirmation de la modification ---
# =============================================================================   
    
    await user_a_maj.send(f"C'est bon {nouv_prenom}, tes infos personnelles ont bien été changées !" )
    await msgAtt    .delete()    





# %%% === Commande ===

erreurMaJ_pasJoueur = "**ERREUR** - Vous **n'êtes pas** inscrit !"

async def cmd_modif_infosPerso(user_voulantSIncrire):
    
    membre_voulantSIncrire = fDis.serveurMegaLG.get_member(user_voulantSIncrire.id)
    
    if   fDis.roleJoueurs not in membre_voulantSIncrire.roles :
        await membre_voulantSIncrire.send( erreurMaJ_pasJoueur )
    
    else :
        await fct_modif_infosPerso(membre_voulantSIncrire)



@fDis.bot.command()
async def Modif_Infos_Perso (ctx) :
    await cmd_modif_infosPerso(ctx.author)
    
@fDis.bot.command()
async def Modif (ctx) :
    await cmd_modif_infosPerso(ctx.author)
    
@fDis.bot.command()
async def modif (ctx) :
    await cmd_modif_infosPerso(ctx.author)
    

@fDis.bot.command()
async def MaJ_Infos_Perso (ctx) :
    await cmd_modif_infosPerso(ctx.author)
    
@fDis.bot.command()
async def MaJ (ctx) :
    await cmd_modif_infosPerso(ctx.author)
    
@fDis.bot.command()
async def maj (ctx) :
    await cmd_modif_infosPerso(ctx.author)
