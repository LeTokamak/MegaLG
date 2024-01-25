# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---             Niveau G - Commandes et événements lançant des parties             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


# Niveau F
import F___village     as fVlg

# Niveau E

# Niveau D
fHab    = fVlg.fHab

# Niveau C
fCom    = fHab.fCom

# Niveau B
fRol    = fHab.fRol
fGrp    = fHab.fGrp

# Niveau A
fSQL    = fHab.fSQL
fDis    = fHab.fDis
fMeP    = fHab.fMeP
v       = fHab.v


rd      = fHab.rd
asyncio = fHab.asyncio



asyncio = fGrp.asyncio


Emo_Homme = "♂️"
Emo_Femme = "♀️"
    

# %% Inscription et Ré-inscription

async def fct_Inscription (membre_aInscrire, timeout = None):
    
    contenuMsg_Inscription = f"Inscription de {membre_aInscrire.mention} en cours..."
    msgAtt = await fDis.channelAttente.send( contenuMsg_Inscription )
    
    contenuMsg_Intro  =  "**Bonjour et Bienvenue sur le serveur du __Méga Loups-Garous__ !**\n"
    contenuMsg_Intro += f"Je suis le {fDis.userMdJ.mention} de vos futures parties, et je suis très fier qu'une personne de plus soit intriguée par mon travail !\n"
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
    contenuMsg_Sexe +=  "> *Évidemment, rien ne vous empèche de mentir.* 😈😈😈\n"
    contenuMsg_Sexe +=  "\n"
    contenuMsg_Sexe += f"Comme vous l'avez certainement compris : pour choisir le masculin, réagissez avec {Emo_Homme}, et pour le féminin ce sera {Emo_Femme}."
    
    msgSexe   = await membre_aInscrire.send( contenuMsg_Sexe                                                                              )
    choixSexe = await fDis.attente_Reaction( msgSexe        , membre_aInscrire, emojisEtReturns, timeout = timeout, reponseParDefaut = "H")
    
    choixConfirme = False
    
    while not choixConfirme :
    
        if   choixSexe == "H" : 
            contenuMsg_VerifSexe = "Donc ça sera **Monsieur**, c'est bien ça ?"
        else : 
            contenuMsg_VerifSexe = "Donc ça sera **Madame**, c'est bien ça ?"
            
        msgConfirmSexe = await membre_aInscrire.send    ( contenuMsg_VerifSexe                   )
        choixConfirme  = await fDis.attente_Confirmation( msgConfirmSexe      , membre_aInscrire, timeout = timeout, reponseParDefaut = True)
        
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
        
        contenuMsg_VerifPseudo  = f"Est-ce que ce pseudo vous convient : **{pseudo}** ?\n"
        contenuMsg_VerifPseudo +=  "> *Votre pseudo a été mis en forme, pour qu'il est la même tête que ceux des autres joueurs.*"
        
        msgConfirmPseudo = await membre_aInscrire.send( contenuMsg_VerifPseudo )
        choixConfirme    = await fDis.attente_Confirmation(msgConfirmPseudo, membre_aInscrire, timeout = timeout, reponseParDefaut = True)
        
        if not choixConfirme :
            
            await msgConfirmPseudo.delete()
            await membre_aInscrire.send( "*Vous pouvez taper un nouveau pseudo !*" )
            
            msgReponsePseudo = await fDis.attente_Message( membre_aInscrire         )
            pseudo           = fMeP.MeF_Pseudo(            msgReponsePseudo.content )
    
    
    
    
    
#    =========================================================================
#### --- Insertion de la nouvelle ligne à la 2ème ligne dans Infos Joueurs ---
#    =========================================================================
    
    nvlLigne = {fSQL.clef_sexe       : choixSexe           , 
                fSQL.clef_pseudo     : pseudo              ,
                fSQL.clef_numGroupe  : None                , 
                fSQL.clef_numVillage : 0                   ,
                fSQL.clef_idDiscord  : membre_aInscrire.id  }
    
    fSQL.ajouter_ligne(fSQL.nom_table_joueurs, nvlLigne)
    
    
    
# =============================================================================
#### --- Suppression du role de Spectateur et/ou du role de Mort et Ajout du role de Joueur ---
# =============================================================================
    
    await membre_aInscrire.remove_roles(fDis.roleSpectateurs, fDis.roleMorts)
    await membre_aInscrire.add_roles   (fDis.roleJoueurs                    )
    
    
    
# =============================================================================
#### --- Message de confirmation de l'inscription ---
# =============================================================================
    
    if   choixSexe == "H" : inscrit = "inscrit"
    else                  : inscrit = "inscrite"
    
    await membre_aInscrire      .send(f"**C'est bon {pseudo}, tu as bien été {inscrit} !**\nTu n'as plus qu'à attendre le début de la partie !" )
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyYellow}  |  Inscription de {membre_aInscrire.mention} : {pseudo}   |   ({choixSexe})")
    await msgAtt                .delete()
    




async def fct_ReInscription (membre_ReInscrit):
        
# =============================================================================
#### Récupération des données personnelles
# =============================================================================
    
    nvlLigne = fSQL.lignes_avec(fSQL.nom_table_joueurs, 
                                fSQL.clef_idDiscord, membre_ReInscrit.id) 
    
    if nvlLigne[fSQL.clef_pseudo] in ("NULL", None) :
        nvlLigne[fSQL.clef_pseudo] = membre_ReInscrit.display_name
    
        fSQL.remplacer_ligne_avec(fSQL.nom_table_joueurs, 
                                  fSQL.clef_idDiscord, membre_ReInscrit.id,
                                  nvlLigne)
    
    
    
# =============================================================================
#### Suppression du role de Spectateur et/ou du role de Mort et Ajout du role de Joueur
# =============================================================================
    
    await membre_ReInscrit.remove_roles(fDis.roleSpectateurs, fDis.roleMorts)
    await membre_ReInscrit.add_roles   (fDis.roleJoueurs                    )
    
    if   nvlLigne[fSQL.clef_sexe] == "H" : reinscrit = "réinscrit"
    else                                 : reinscrit = "réinscrite"
    
    await membre_ReInscrit      .send(f"**Salut {nvlLigne[fSQL.clef_pseudo]}, tu as bien été {reinscrit} !**\nTu n'as plus qu'à attendre le début de la partie !")
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyOrange}  |  Ré-inscription de {membre_ReInscrit.mention} : {nvlLigne[fSQL.clef_pseudo]}   |   {nvlLigne[fSQL.clef_numGroupe]}")
    
    """
    groupe = fGrp.groupe_avec(nvlLigne[fSQL.clef_numGroupe], 'numero')
    
    if groupe != None :
        await groupe.autorisation_Salon(membre_ReInscrit)
    """




# %% Lancement des parties (Perso & Commune)

erreurIns_phase1     = "**ERREUR** - Les inscriptions **ne sont pas** ouvertes pour l'instant..."
erreurIns_dejaJoueur = "**ERREUR** - Vous êtes **déjà** inscrit !"

messagIns_reInscript = "**Vous avez déjà participer à une ancienne partie.**\nVous avez donc été ré-inscrit !"





async def evt_rejoindrePartieCommune (groupe):
    
    liste_membres_groupe = [ membre 
                                for membre in groupe.salon.members  
                                if  fDis.roleBot not in membre.roles  and  fDis.roleModerateur not in membre.roles ]
    
    for membre in liste_membres_groupe :
    
#### == 1 ==  Ajouter à tout les membres du groupe le role roleProchainePartComm

        await membre.add_roles(fDis.roleProchainePartComm)

#### == 2 ==  Vérifier le sexe et les pseudo des membres du groupe son connu

#### = 2.1 =  Si oui, ré-inscription (rien de spécial à faire)

        if membre.id in fSQL.colonne_avec(fSQL.nom_table_joueurs, fSQL.clef_idDiscord) :
            asyncio.create_task( fct_ReInscription(membre) )

#### = 2.2 =  Si non, inscription 
    
        else :
             asyncio.create_task( fct_Inscription(membre) )





async def evt_lancementPartiePerso (groupe):
    
#### == 0 == Introduction
#### = 0.1 = Gestion du temps
    
    moment_actuel = v.maintenant()
    
    #   S'il n'est pas encore 19h, la distribution aura lieu à 20h le jour meme, sinon se sera à 20h le lendemain 
    
    moment_distribution_role = v.datetime(moment_actuel.year, moment_actuel.month, moment_actuel.day, 20, 00)
    
    if moment_actuel.hour > 19 : moment_distribution_role += v.timedelta(days = 1)
    
#### = 0.2 = Listage des membres du groupe
    
    liste_membres_groupe = [ membre 
                                for membre in groupe.salon.members
                                if  fDis.roleBot not in membre.roles  and  fDis.roleModerateur not in membre.roles ]
    
    for membre in liste_membres_groupe :
    
        
    
#### == 1 ==   Ajouter à tout les membres du groupe le role roleJoueurs
#### == 2 ==   Vérifier que le sexe et les pseudo des membres du groupe sont connus
#### = 2.1 =   Si oui, ré-inscription (rien de spécial à faire)

        if membre.id in fSQL.colonne_avec(fSQL.nom_table_joueurs, fSQL.clef_idDiscord) :
            asyncio.create_task( fct_ReInscription(membre) )

#### = 2.2 =   Si non, inscription 
    
        else :
             asyncio.create_task( fct_Inscription(membre) ) # VERIFIER - Cas où l'inscription n'est pas faite avant la distribution


             
#### == 3 ==   Choix de la compo

    compo_choisie = await fCom.choix_de_la_compo()



#### == 4 ==   Attent qu'il soit 20h
    
    await v.attente_du_moment_x(moment_distribution_role)



#### == 5 ==   Création du Village
#### = 5.1 =   Recherche d'un numéro disponible pour le nouveau village
    
    numTrouve       = False
    numNouvVillage  = 0
    
    numDejaUtilises = fSQL.colonne_avec(fSQL.nom_table_villages, fSQL.clef_numVillage)
    
    while not numTrouve :
        numNouvVillage += 1
        if numNouvVillage not in numDejaUtilises :
            numTrouve = True



#### = 5.2 =   Mise à jour des numéros de village des futurs habitants

    for membre in liste_membres_groupe :
        fSQL.remplacer_val_lignes_avec(fSQL.nom_table_joueurs, 
                                       fSQL.clef_idDiscord   , membre.id,
                                       fSQL.clef_numVillage  , numNouvVillage)
        
        
    
#### = 5.3 =   Mise à jour des numéros de village des futurs habitants

    fHab.ajout_habitants_des_membre(liste_membres_groupe)
    
    await fVlg.creationVillage( numNouvVillage = numNouvVillage )
    
    
    
#### == 6 ==   Ajout de la partie à la pile des partie

    pass



# %%% Lancement Partie Commune

async def lancement_partieCommune():
    pass




# %%% Réaction lancement de partie
        
async def reactions_lancementPartie():
    
    def verifReInscription(payload):
        verifUser  = False
        verifEmoji = False
        
        groupe = fGrp.groupe_avec(payload.message_id, "idMsg_Groupe")
        
        verifMessage   = groupe != None
        if verifMessage :
            verifUser  = groupe.chef.id == payload.user_id
            verifEmoji = str(payload.emoji) in (fDis.Emo_BabyOrange, fDis.Emo_BabyCyan)
        
        return verifMessage and verifUser and verifEmoji
    
#### === Boucle infini ===
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifReInscription)
        
        groupe = fGrp.groupe_avec( payload.message_id , "idMsg_Groupe" )
        
#### Lancement de la partie commune
        if   str(payload.emoji) == fDis.Emo_BabyOrange :
            await evt_rejoindrePartieCommune(groupe)
            
#### Lancement de la partie perso
        elif str(payload.emoji) == fDis.Emo_BabyCyan :
            await evt_lancementPartiePerso  (groupe)
        
        
        
        
        
# %% Modification des infos personnelles

async def fct_modif_infosPerso(user_a_maj):
    
    contenuMsg_Inscription = f"MàJ des infos personnelles de {user_a_maj.mention} en cours..."
    msgAtt = await fDis.channelAttente.send( contenuMsg_Inscription )
    
        
    
# =============================================================================
#### Anciennes données persos
# =============================================================================

    ancienne_ligne_joueur = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                                             fSQL.clef_idDiscord, user_a_maj.id)
    
    if ancienne_ligne_joueur[fSQL.clef_sexe] == "H" : ancien_sexe =  "un Homme"
    else                                            : ancien_sexe = "une Femme"
    
    contenuMsg_Intro  =  "Bonjour, vous voulez changer vos infos personnelles, voilà ce que je sais sur vous :\n"
    contenuMsg_Intro += f"> Vous êtes **{ancien_sexe}**, et je vous appele **{ancienne_ligne_joueur[fSQL.clef_pseudo]}**.\n"
    contenuMsg_Intro +=  "\n\n_ _"
    
    await user_a_maj.send(contenuMsg_Intro)
    
    
    
# =============================================================================
#### --- MaJ des données personnelles ---
# =============================================================================    

#### Sexe
    
    if ancienne_ligne_joueur[fSQL.clef_sexe] == "H" : eventuel_nouv_sexe,  texte_eventuel_nouv_sexe,  Emo_eventuel_nouv_sexe  =  "F", "une **Femme**" , Emo_Femme
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
        choix_nouv_Sexe = ancienne_ligne_joueur[fSQL.clef_sexe]
    
    
    
#### Pseudo
    
    if   choix_nouv_Sexe == "H" : deb_contenuMsg_Pseudo = "Très bien *Monsieur*"
    else                        : deb_contenuMsg_Pseudo = "Compris *Madame*"
    
    
    contenuMsg_Modif_Pseudo = deb_contenuMsg_Pseudo + f", est-ce que vous voulez modifier votre ancien **Pseudo** ({ancienne_ligne_joueur[fSQL.clef_pseudo]}) ?\n"
    
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
        nouv_pseudo = ancienne_ligne_joueur[fSQL.clef_pseudo]
        
    
    
    
    
# =============================================================================
#### --- Remplacement de la ligne de Info Joueurs ---
# =============================================================================
    
    nvlLigne_InfoJoueurs = { fSQL.clef_matricule  : ancienne_ligne_joueur[fSQL.clef_matricule]    ,
                            
                             fSQL.clef_sexe       : choix_nouv_Sexe                               ,
                             fSQL.clef_pseudo     : nouv_pseudo                                   ,
                             
                             fSQL.clef_numGroupe  : ancienne_ligne_joueur[fSQL.clef_numGroupe]       , 
                             fSQL.clef_numVillage : ancienne_ligne_joueur[fSQL.clef_numVillage]   ,
                             
                             fSQL.clef_idDiscord  : user_a_maj.id                                 ,
                             
                             fSQL.clef_idRole     : ancienne_ligne_joueur[fSQL.clef_idRole]         ,
                             fSQL.clef_caractRole : ancienne_ligne_joueur[fSQL.clef_caractRole]  ,
                             fSQL.clef_caractJoue : ancienne_ligne_joueur[fSQL.clef_caractJoue]  }
    
    fSQL.remplacer_ligne_avec(fSQL.nom_table_joueurs,
                              fSQL.clef_idDiscord   , user_a_maj.id,
                              nvlLigne_InfoJoueurs                   )
    
    
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
        
        
        
        

# %% === ANCIENNE PHASE 1 ===

"""

idMessage_Inscription = 864264877160792064

@fDis.bot.command(aliases = ["Debut_Phase1"])
@fDis.commands.has_permissions(ban_members = True)
async def lancement_Inscription(ctx):
    
    v.phaseEnCours = v.phase1
    await fDis.channelHistorique.edit(topic = v.phase1)   
    
    
#### Message de Inscription
    
    msgInscription = await fDis.channelInscription.fetch_message(idMessage_Inscription)
    await msgInscription.clear_reactions()
    await msgInscription.add_reaction(fDis.Emo_BabyYellow)
    
    
#### Nettoyage de Infos Joueurs
    
    nb_Joueurs_anc_partie = len( fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs) )
    
    if nb_Joueurs_anc_partie != 0 :
        fGoo.page1_InfoJoueurs.delete_rows(2, nb_Joueurs_anc_partie + 1)
        
    v.plantage()

"""