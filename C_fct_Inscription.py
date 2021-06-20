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
import B_fct_Groupe      as fGrp

#Niveau A
fDis = fGrp.fDis
fGoo = fGrp.fGoo





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

async def Inscription (membre_aInscrire):
    
    contenuMsg_Inscription = f"Inscription de {membre_aInscrire.mention} en cours..."
    msgAtt = await fDis.channelAttente.send( contenuMsg_Inscription )
    
    contenuMsg_Intro  =  "**Bonjour et Bienvenue sur le serveur du __Méga Loups-Garous__ !**\n"
    contenuMsg_Intro += f"Je suis le {fDis.userMdJ.mention} de la partie, et je suis très fier qu'une personne de plus soit intriguée par mon travail !\n"
    contenuMsg_Intro +=  "\n"
    contenuMsg_Intro +=  "Il est temps de passer à votre **Inscription**\n"
    contenuMsg_Intro +=  "\n\n_ _"
    
    await membre_aInscrire.send(contenuMsg_Intro)
    
    
    
# =============================================================================
#### --- Récolte des données personnelles ---
# =============================================================================    

#### Sexe
    
    Emo_Homme = "♂️"
    Emo_Femme = "♀️"
    
    emojisEtReturns = [[Emo_Homme, "H"], [Emo_Femme, "F"]]

    contenuMsg_Sexe  =  "Alors dans un premier temps, il faut que vous choissiez votre **sexe** !\n"
    contenuMsg_Sexe +=  "> J'utilise cette info pour accorder mes phrases, pour qu'elles soient plus imersivent.\n"
    contenuMsg_Sexe +=  ">      *Alberte a été retrouvé·e mort·e chez lui/elle ce matin...* devient "
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
    
    if   choixSexe == "H" : deb_contenuMsg_Prenom, monsieur, inscrit = "Très bien *Monsieur*" , "Monsieur", "inscrit"
    elif choixSexe == "F" : deb_contenuMsg_Prenom, monsieur, inscrit = "Compris *Madame*"     , "Madame"  , "inscrite"
    
    contenuMsg_Prenom  = deb_contenuMsg_Prenom + ", maintenant quel est votre **Prénom** ?\n"
    contenuMsg_Prenom +=  "> Le **prochain message** que vous enverrez sera votre prénom (après que vous l'avoir confirmé, comme pour le sexe).\n"
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
    contenuMsg_Nom +=  "> Le prochain message que vous enverrez sera votre **nom** (après que vous l'avoir confirmé, comme toujours).\n"
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