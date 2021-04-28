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





# %% Inscription

async def Inscription(membre_aInscrire, nb):
    
    ligne, num_ligne = fGoo.ligne_avec(nb, fGoo.clefForm_nbSynchro, fGoo.donneeGoogleSheet(fGoo.page1_RepFormulaire))
    
# =============================================================================
#### --- Adaptation des données personnelles ---
# =============================================================================
    
#### Sexe
    
    if   ligne[fGoo.clefForm_Sexe] == "Un Monsieur" : sexe, inscrit = "H", "inscrit"
    elif ligne[fGoo.clefForm_Sexe] == "Une Madame"  : sexe, inscrit = "F", "inscrite"
    
    
    
#### Prénom
    
# Verif Espaces et Majuscules pour les prénoms
    
    # 1er split pour les espaces "___cléMENt__" et gestion des Majuscules
    
    prenom = ligne[fGoo.clefForm_Prenom].split()
    Prenom = []
    
    for p in prenom :
        Prenom.append( p[0].upper() + p[1:].lower() )
        
        prenom = " ".join( Prenom )
        
    # 2nd split pour la gestion des Majuscules après les "-" (prénoms composées)
        prenom = prenom.split("-")
        Prenom = []
        
    for p in prenom :
        Prenom.append( p[0].upper() + p[1:] )
    
    prenom = "-".join( Prenom )
    
    
#### Nom
    
# Verif Espaces et Majuscules pour les noms
    
    nom    = " ".join( ligne[fGoo.clefForm_Nom].split() ).upper()
    
    
    
# =============================================================================
#### --- Insertion de la nouvelle ligne à la 2eme ligne dans Infos Joueurs ---
# =============================================================================
    
    nvlLigne = { fGoo.clef_Sexe       : sexe                        , 
                 fGoo.clef_Prenom     : prenom                      ,
                 fGoo.clef_Nom        : nom                         , 
                 fGoo.clef_Groupe     : fGrp.GroupeParDefaut.chemin ,
                 fGoo.clef_idDiscord  : str(membre_aInscrire.id)      }
    
    fGoo.ajoutLigne(nvlLigne, fGoo.page1_InfoJoueurs)
    
    
    
# =============================================================================
#### --- Suppression du role de Spectateur et/ou du role de Mort et Ajout du role de Joueur ---
# =============================================================================
    
    await membre_aInscrire.remove_roles(fDis.roleMorts, fDis.roleSpectateurs)                
    await membre_aInscrire.   add_roles(fDis.roleJoueurs                    )
    
    
    
# =============================================================================
#### --- Modification du Nombre de Synchronisation ---
# =============================================================================
        
    fGoo.suppressionLigne_avec( nb, fGoo.clefForm_nbSynchro, fGoo.page1_RepFormulaire )
    
    
    
# =============================================================================
#### --- Message de confirmation de l'inscription ---
# =============================================================================
        
    await membre_aInscrire      .send(f"**Salut {prenom}, tu as bien été {inscrit} !**\nTu n'as plus qu'à attendre le début de la partie !" )
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyYellow}  |  Inscription de {membre_aInscrire.mention} : {prenom} {nom}   |   ({sexe})")
        
    await fGrp.autorisation_SalonsGrp(membre_aInscrire, fGrp.GroupeParDefaut.chemin)









messageErreurSyncro = ["**ERREUR**  -  Vous n'avez pas rentré un entier.",
                       "**ERREUR**  -  Vous n'avez pas rentré un nombre à 4 chiffres.",
                       "**ERREUR**  -  Votre nombre n'est pas dans la base de donnée, êtes-vous certain de bien avoir envoyé le formulaire ?",
                       "**ERREUR**  -  Quelqu'un d'autre a utilisé le même nombre de Synchronisation que vous...\nClément a reçu un message pour vous inscrire manuellement !"]


async def evt_Inscription(auteurMsg, contenuMsg):
    
    nb = None


# =============================================================================
#### --- 1ère Verif /  Essaye de int le contenu du msg, si ça ne marche pas le msg n'est pas un entier ---
# =============================================================================

    try    : nb = abs(int(contenuMsg))
    except : await auteurMsg.send(messageErreurSyncro[0])
    
    
    
# =============================================================================
#### --- 2ème Verif /  Le Message n'est pas sous la bonne forme (|nb| > 9999) ---
# =============================================================================
    
    if   nb != None  and  nb > 9999 :
        await auteurMsg.send(messageErreurSyncro[1])
    
    elif nb != None  :
        
# Récupération des personnes inscrites et de leurs nombre de Synchro
        listeNbSynchro = fGoo.colonne_avec(fGoo.page1_RepFormulaire, fGoo.clefForm_nbSynchro)
        
        
        
# =============================================================================
#### --- 3ème Verif /  Le nb de Synchro n'est pas dans la base de donnée ---
# =============================================================================
        
        if   nb not in listeNbSynchro :
            await auteurMsg.send(messageErreurSyncro[2])
        
#### Inscription
        
        elif listeNbSynchro.count(nb) == 1 :
            await Inscription(auteurMsg, nb)
        
        
        
# =============================================================================
#### --- 4ème Verif /  Plusieurs personnes ont le même nb, Inscription Manuelle ---
# =============================================================================
        
        else :
            await auteurMsg             .send(messageErreurSyncro[3])
            await fDis.channelHistorique.send(f"{fDis.roleMaitre.mention} !\n{auteurMsg.mention} a le même nb de Synchro qu'une autre personne !")



        

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
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyOrange}  |  ReInscription de {membre_ReInscrit.mention} : {nvlLigne[fGoo.clef_Prenom]} {nvlLigne[fGoo.clef_Nom]}   |   {nvlLigne[fGoo.clef_Groupe]}")

    await fGrp.autorisation_SalonsGrp(membre_ReInscrit, nvlLigne[fGoo.clef_Groupe])
    




idMessage_ReInscription = 821018077248225290

async def evt_ReInscription (membre):

    idUser = membre.id 
    
    if idUser in listeidDisConnus :        
        await ReInscription(membre)
            
    else :
        erreurReInscription = f"**ERREUR**  -  Vous n'avez pas participer à la partie précédente, vous ne pouvez donc pas vous ré-inscrire.\n> Pour vous inscrire, vous devez remplir le formulaire et taper le Nombre de Synchronisation que vous avez choisi dans le salon `{fDis.channelAccueil.name}`.\n> *Si vous avez un problème, n'hésitez pas à envoyer un message privé à Clément Campana*"
        await membre.send(erreurReInscription)
    