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

Version Delta                             δ2                                28/04/2021

"""

version = "δ2"


# Niveau E
import E_fct_Tour        as fTou


# Niveau D
fVlg = fTou.fVlg


# Niveau C
import C_fct_Inscription as fIns
fHab = fVlg.fHab


# Niveau B
fGrp = fHab.fGrp
fRol = fHab.fRol


# Niveau A
fGoo = fHab.fGoo
fDis = fHab.fDis
fMeP = fHab.fMeP
v    = fHab.v



rd      = fHab.rd
asyncio = fHab.asyncio

import pandas            as pd
import itertools




# %% Events

# %%% Nouveau Membre
     
@fDis.bot.event
async def on_member_join (member):
    await member.add_roles(fDis.roleSpectateurs)
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyGreen}  |  {member.mention} vient d'arriver sur le serveur !")





# %%% Départ d'un Membre

@fDis.bot.event
async def on_member_remove(member):
    """Si qqun se barre, le tuer si il joue ==> Modifier la fonction tuer
                         ne rien faire sinon
    """
    
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyBlack}  |  {member} vient de quitter le serveur !")
    
    if v.phaseEnCours == v.phase3  and  fDis.roleJoueurs in member.roles :
        
        fHab.redef_TousLesHabitants()
        
        persPartie = fHab.habitant_avec(member.id)
        await fDis.channelHistorique.send(f"Il était un joueur : {persPartie.user.mention}  |  {persPartie.matri} {persPartie.prenom} {persPartie.nom} - ( {persPartie.groupe} ) !")
        
        await persPartie.Tuer(departServeur = True)
        await persPartie.user.send("""Vous avez quitté le serveur, vous avez donc été tué...\nVous pouvez utiliser la commande "!Nettoyage" pour effacer tout les messages que je vous ai envoyés.""")





# %%% Réaction à un message

idMessage_Artisans      = 817809404359081994



async def ajout_roleArtisans():
    
    def verifArtisans(payload):
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifMessage = payload.message_id == idMessage_Artisans
        
        return verifUser  and  verifMessage
    
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifArtisans)
        await payload.member.add_roles(fDis.roleArtisans)



async def reaction_reInscription():
    
    def verifReInscription(payload):
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifPhase   = v.phaseEnCours     == v.phase1
        verifMessage = payload.message_id == fIns.idMessage_ReInscription
        verifEmoji   = str(payload.emoji) == fDis.Emo_BabyOrange
        
        return verifUser  and  verifPhase and verifMessage and verifEmoji
    
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifReInscription)
        await fIns.evt_ReInscription(payload.member)



async def reaction_Groupe():
    
    def verifGroupe(payload):
        salon        = fDis.serveurMegaLG.get_channel(payload.channel_id)
        
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifPhase   = v.phaseEnCours == v.phase1
        verifCategCh = salon.category == fDis.CategoryChannel_GestionGrp
        
        return verifUser  and  verifPhase and verifCategCh
    
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifGroupe)
        await fGrp.evt_ChangementGroupe(payload.member, payload.message_id, str(payload.emoji))



async def event_reactions():
    asyncio.Task( ajout_roleArtisans()     )
    asyncio.Task( reaction_reInscription() )
    asyncio.Task( reaction_Groupe()        )





# %%% Envoie d'un message

def verifServeur (message):
    try :
        if message.guild == fDis.serveurMegaLG :
            return True
        else :
            return False
    except :
        return False



async def message_Inscription():
    
    def verifInscription(message):
        verifPhase = verifSalon = verifUser = False
        
        if verifServeur(message) :
            verifUser = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
            
            if verifUser :
                verifPhase = v.phaseEnCours  == v.phase1
                verifSalon = message.channel == fDis.channelAccueil
        
        return verifUser  and  verifPhase and verifSalon
    
    
    while True :
        message = await fDis.bot.wait_for('message', check = verifInscription)
        await fDis.effacerMsg(fDis.channelAccueil)
        await fIns.evt_Inscription(message.author, message.content)



async def message_voteVillage():
    
    def verifVoteVillage(message):
        verifPhase = verifSalon = verifUser = False
        
        if verifServeur(message) :
            verifUser = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
            
            if verifUser :
                verifPhase = v.phaseEnCours == v.phase3
                verifSalon = fVlg.village_avec(message.channel, 'idSalon_Bucher') != None
        
        return verifUser  and  verifPhase and verifSalon


    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteVillage)
        await fDis.effacerMsg (message.channel)
        await fVlg.evt_voteVlg(message.author, message.content)


        
async def message_voteLoupGarou():
    
    def verifVoteLG(message):
        verifPhase = verifSalon = verifUser = False
        
        if verifServeur(message) :
            verifUser = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
        
            if verifUser :
                verifPhase = v.phaseEnCours == v.phase3
                verifSalon = fVlg.village_avec(message.channel, 'idSalon_VoteLG') != None
        
        return verifUser  and  verifPhase and verifSalon


    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteLG)
        await fDis.effacerMsg(message.channel)
        await fVlg.evt_voteLG(message.author, message.content)

    
    
async def event_messages():
    asyncio.Task( message_Inscription()   )
    asyncio.Task( message_voteVillage()   )
    asyncio.Task( message_voteLoupGarou() )
    
    
    
    
    
# %% Commandes

# %%% Commandes Générales

# %%%% Nettoyage

async def com_Nettoyage (ctx, nbMessages):
    """
    Efface tout les messages que le @Maître du Jeu vous a envoyé 
    Vous pouvez y ajouter un paramètre optionnel, le nombre de message

    !Nettoyage     ==> Efface tout les messages qu'il vous a envoyé
    !Nettoyage 3   ==> Efface les 3 derniers messages qu'il vous a envoyé 
    """
        
    if ctx.guild == fDis.serveurMegaLG :
        
        await fDis.effacerMsg(ctx)
        
        if fDis.roleMaitre in ctx.author.roles :
            await fDis.effacerMsg(ctx, nbMessages)
            
    else :
        await fDis.effacerMsg(ctx, nbMessages)
        await fDis.channelHistorique.send(f"{fDis.Emo_BabyLime}  |  {ctx.author.mention} a fait un peu de ménage dans son salon privée !   ({nbMessages} messages supprimés)")



@fDis.bot.command()
async def Nettoyage (ctx, nbMessages = 10**9) :
    await com_Nettoyage (ctx, nbMessages)
    
@fDis.bot.command()
async def nettoyage (ctx, nbMessages = 10**9) :
    await com_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def Net       (ctx, nbMessages = 10**9) :
    await com_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def net       (ctx, nbMessages = 10**9) :
    await com_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def N         (ctx, nbMessages = 10**9) :
    await com_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def n         (ctx, nbMessages = 10**9) :
    await com_Nettoyage (ctx, nbMessages)





# %%%% Création d'un nouveau Groupe 

@fDis.bot.command()
async def Creation_SousGroupe(ctx, *tupleNom):
    await fGrp.com_NouveauGroupe(ctx, tupleNom)
    
@fDis.bot.command()
async def creation_sousgroupe(ctx, *tupleNom):
    await fGrp.com_NouveauGroupe(ctx, tupleNom)
    
@fDis.bot.command()
async def CreationSousGroupe(ctx, *tupleNom):
    await fGrp.com_NouveauGroupe(ctx, tupleNom)
    
@fDis.bot.command()
async def creationSGrp(ctx, *tupleNom):
    await fGrp.com_NouveauGroupe(ctx, tupleNom)
    
@fDis.bot.command()
async def creatSGrp(ctx, *tupleNom):
    await fGrp.com_NouveauGroupe(ctx, tupleNom)
    
@fDis.bot.command()
async def csg(ctx, *tupleNom):
    await fGrp.com_NouveauGroupe(ctx, tupleNom)
    
    
    
    

# %%%% Commandes de Maires 

# %%%%% Changement du nom du village 

@fDis.bot.command()
async def Nouveau_Nom_Village(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)

@fDis.bot.command()
async def nouveau_nom_village(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)

@fDis.bot.command()
async def NouvNomVlg(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)

@fDis.bot.command()
async def RenommageVlg(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)

@fDis.bot.command()
async def renommageVlg(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)

@fDis.bot.command()
async def Renommage(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)
    
@fDis.bot.command()
async def renommage(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)
    
    
    
    

# %%% Commandes des Admins

# %%%% Toujours Utilisables

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def ResetRolesDiscord (ctx):
    """
    Enlève les roles fDis.roleJoueurs et fDis.roleMorts des joueurs de la partie précédente
    Ajoute le role fDis.roleSpectateurs à tous les joueurs de la partie précédente
    """
       
### Efface !ResetRoles
    await fDis.effacerMsg(ctx)
    Participants = fGoo.donneeGoogleSheet( fGoo.page1_Sauvegarde )


### Modification des roles des participants à la partie précédentes
    for p in Participants :
                
        membPar = fDis.serveurMegaLG.get_member( p[fGoo.clef_idDiscord] )
        
        await membPar.remove_roles(fDis.roleJoueurs, fDis.roleMorts)
        await membPar.   add_roles(fDis.roleSpectateurs)
        
        
        
        

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def ResetMatricules (ctx):
    """
    Enlève la partie des pseudos des Joueurs correspondant à leur Matricule
    """

### Efface !ResetMatricules
    await fDis.effacerMsg(ctx)
    
### Modification des pseudos de tout les joueurs
    Joueurs = fGoo.donneeGoogleSheet( fGoo.page1_InfoJoueurs )
    
    for j in Joueurs :
        
        membJou = fDis.serveurMegaLG.get_member( j[fGoo.clef_idDiscord] )
        await membJou.edit(nick = membJou.display_name[6:])





# %%%% Partie
     
@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Meutre (ctx, matricule):

    if v.phaseEnCours in (v.phase2, v.phase3) :

        await fHab.redef_TousLesHabitants()
        
        persTuee = fHab.habitant_avec(int(matricule))
        
        await persTuee.Tuer()
        await fDis.channelHistorique.send(f"{persTuee.user.mention}  |  {persTuee.matri} {persTuee.prenom} {persTuee.nom} - ( {persTuee.groupe} ) vient d'être tué")





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Sauvetage (ctx, matriculePersSauve):
    
    if v.phaseEnCours in (v.phase2, v.phase3):
        
        v.choixSalvateurs.append(int(matriculePersSauve))
        await fDis.channelHistorique.send(f"{matriculePersSauve} vient d'être protégé !")





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Rapport_TousLesVillages (ctx):

    if v.phaseEnCours in (v.phase2, v.phase3, v.phase4) :
        
        await fHab.redef_TousLesHabitants()
        for vlg in fVlg.TousLesVillages :
            await vlg.rapportMunicipal()





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Amoureux (ctx, matricule1, matricule2):
    
    mat_amour1 = int(matricule1)
    mat_amour2 = int(matricule2)
    
    fGoo.ajoutVal_cellule_avec( f"A{matricule2} ", fGoo.clef_caractJoueur ,
                                mat_amour1       , fGoo.clef_Matricule    ,
                                fGoo.page1_InfoJoueurs                     )
    
    fGoo.ajoutVal_cellule_avec( f"A{matricule1} ", fGoo.clef_caractJoueur ,
                                mat_amour2       , fGoo.clef_Matricule    ,
                                fGoo.page1_InfoJoueurs                     )
            
    pers1 = fHab.habitant_avec(mat_amour1)
    pers2 = fHab.habitant_avec(mat_amour2)
    
    await pers1.user.send(f"Vous êtes amoureux de {pers2.matri}  |  {pers2.prenom} {pers2.nom} {pers2.groupe}")
    await pers2.user.send(f"Vous êtes amoureux de {pers1.matri}  |  {pers1.prenom} {pers1.nom} {pers1.groupe}")
    
    await fHab.redef_TousLesHabitants()
    
    
    
    
"""
@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def AmoureuxAlea (ctx):
    
    await fHab.redef_TousLesHabitants()
    
    Celibs = []
    
    for pers in fPer.ToutesLesPersonnes :
        if not pers.estAmoureux :
            Celibs.append(pers)
    
    while len(Celibs) >= 2 : 
    
        pers1 = fMeP.rd.choice(Celibs)
        pers2 = fMeP.rd.choice(Celibs)
        
        Celibs.remove(pers1)
        Celibs.remove(pers2)
        
        fGoo.ajoutVal_cellule_avec( f"A{pers2.matri} ", fGoo.clef_caractJoueur ,
                                    pers1.matri       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                      )
    
        fGoo.ajoutVal_cellule_avec( f"A{pers1.matri} ", fGoo.clef_caractJoueur ,
                                    pers2.matri       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                      )
    
        await pers1.user.send(f"Vous êtes amoureux de {pers2.matri}  |  {pers2.prenom} {pers2.nom} {pers2.groupe}")
        await pers2.user.send(f"Vous êtes amoureux de {pers1.matri}  |  {pers1.prenom} {pers1.nom} {pers1.groupe}")
"""





# %% === on_ready ===

@fDis.bot.event
async def on_ready():
    
    fDis.def_cstsMegaLG()
    
    
#### Recherche de la phase en cours
    
    v.phaseEnCours = v.phase0
    
    phaseTrouvee = False
    
    async for message in fDis.channelHistorique.history(limit = 10**9):
        
        if "```Phase " in message.content  and  not phaseTrouvee :
            v.phaseEnCours = message.content
            phaseTrouvee = True
    
    await fDis.channelHistorique.send(f"```⬢ -  Je suis connecté ! ({version} | {v.phaseEnCours[3:-3]})  - ⬢```\n{v.maintenant()}")
    
    
#### Redéfinition Groupes et Villages
    
    await fGrp.redef_groupesExistants()
    await fVlg.redef_villagesExistants()
    
    
#### Lancement des events 
    
    asyncio.Task(event_reactions())
    asyncio.Task(event_messages() )
    
    
#### Lancement des attendes d'épitaphe
    
    async for message in fDis.channelAttente.history(limit = 10**9):
        
        if fDis.Emo_Red == message.content.split()[0] :
            asyncio.Task( fHab.cimetiere(message = message, rappelDeFonction = True) )
    
    await fDis.channelHistorique.send(f"```⬢ -  Fin du 'on_ready'  - ⬢```\n{v.maintenant()}")
    
    await repartionGroupes_Villages()
    
#### Phase 3 - Récupération du numéro de Tour
    
    if v.phaseEnCours == v.phase3 :
        # Le topic de channelHistorique est de la forme "Tour n°45"
        
        v.nbTours = int(fDis.channelHistorique.topic[7: ])
    
    
#### Phase 3 - Lancement du Tour
    
    if v.phaseEnCours == v.phase3 :
        await attente_lancementTour()




# %% --- Phase 1 ---

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Inscription (ctx):
    
    await lancementInscription()



async def lancementInscription():

    v.phaseEnCours = v.phase1
    await fDis.channelHistorique.send(v.phaseEnCours)
    
#### Gestions des permissions
    
    await fDis.channelAccueil.set_permissions(fDis.roleSpectateurs, read_messages = True, send_messages = True)
    
    
#### Message de Ré-Inscription
    
    msgReInscription = await fDis.channelAccueil.fetch_message(fIns.idMessage_ReInscription)
    await msgReInscription.clear_reactions()
    await msgReInscription.add_reaction(fDis.Emo_BabyOrange)
    
    
#### Nettoyage de Infos Joueurs

    "A programmer"




# %% --- Phase 2 ---

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DebutPartie (ctx):
    
    #await finInscription()
    
    #await numerotationHabitants()
    
    await repartionGroupes_Villages()
    
    #await distributionRole()
    


async def finInscription():
    
    v.phaseEnCours = v.phase2
    await fDis.channelHistorique.send(v.phaseEnCours)
    
#### Gestions des permissions
    
    await fDis.channelAccueil.set_permissions(fDis.roleSpectateurs, read_messages = False, send_messages = False)
    
    
#### Nettoyage des salons de groupes
    
    "A programmer"



async def numerotationHabitants():
    
    Joueurs = fGoo.donneeGoogleSheet( fGoo.page1_InfoJoueurs )

#### Tri des Joueurs par nom de groupe, par nom de joueur et par prénom

    for j in Joueurs :
        
        habitant = fHab.Habitant( 0                         ,
                                  j[fGoo.clef_Prenom      ] ,
                                  j[fGoo.clef_Nom         ] ,
                                  j[fGoo.clef_Groupe      ] ,
                                  0                         ,
                                  j[fGoo.clef_Sexe        ] ,
                                  j[fGoo.clef_idDiscord   ] ,
                                  ""                        ,
                                  ""                        ,
                                  ""                          )
        
        await habitant.init_groupe()
        
        j["strGroupe"] = str(habitant.groupe)
    
    

    dfJoueurs                      = pd.DataFrame(Joueurs)
    dfJoueurs                      = dfJoueurs.sort_values(by = ["strGroupe", fGoo.clef_Nom, fGoo.clef_Prenom])
    dfJoueurs                      = dfJoueurs.drop(["strGroupe"], axis = 1)
    dfJoueurs[fGoo.clef_Matricule] = range(1, len(Joueurs) + 1)

    listeJoueurs                   = fGoo.dfToList(dfJoueurs)    
    
    
    
    for j in listeJoueurs[1:] :
        
#   j = [23, H, Clément, Campana, 27, 269051521272905728, '', '', '']
                
        membJou = fDis.serveurMegaLG.get_member(int(j[5]))
                
        surnom  = membJou.display_name
        
        while len(surnom) > 26 :
            surnom = surnom[ :-1]
        
        await membJou.edit(nick = f"{fMeP.AjoutZerosAvant(j[0],3)} | {surnom}")
    
    


    fGoo.page1_InfoJoueurs.clear()
    fGoo.page1_InfoJoueurs.insert_rows(fGoo.strListe(listeJoueurs))
    
    fGoo.page1_Sauvegarde .clear()
    fGoo.page1_Sauvegarde .insert_rows(fGoo.strListe(listeJoueurs))







async def repartionGroupes_Villages() :
    
    listeGroupes = list(fGrp.TousLesGroupes)

    margeHabitants = 0.00 #0.05
    
    
    def habitants(vlg):
        habsVlg = []
        for grp in vlg :
            habsVlg.extend(grp.personnes)
            
        return habsVlg
    
    
    def nbHabitant(vlg):
        sommeHab = 0
        for grp in vlg :
            sommeHab += grp.nbPersonne
            
        return sommeHab
        
        
    def verifVlg_Incoherent(vlg):
        villageIncoherent = False
            
        for grp1 in vlg :
            for grp2 in vlg :
                if grp1 in grp2.sur_Groupes :
                    villageIncoherent = True
            
        return villageIncoherent
        
    
    def suppressionVlg_identiques(liste_vlg):
        for vlg in liste_vlg :
            for vlg2 in liste_vlg :
                if habitants(vlg) == habitants(vlg):
                    print(f"Suppression de {vlg}, normalement impossible avec uniquement des sous-groupes \n{vlg} == {vlg2}")
                    liste_vlg.remove(vlg)
    
#### --- Variables ---

    nbHabitants_parVillage_Souhaite = 5
    
    nbVillages_Reel                 = 0
    nbHabitants_parVillage_Reel     = nbHabitants_parVillage_Souhaite
    
    ecartMin                        = len(fHab.TousLesHabitants) + 1
    
    for n in range( 1, len(fHab.TousLesHabitants) + 1 ):
        ecart = abs(len(fHab.TousLesHabitants)/n - nbHabitants_parVillage_Souhaite)
        
        if ecart < ecartMin :
            nbVillages_Reel             = n
            nbHabitants_parVillage_Reel = len(fHab.TousLesHabitants) // n
            
            ecartMin                    = ecart
    
    
    nbHab_parVlg_Min = int(nbHabitants_parVillage_Reel * (1 - margeHabitants) - 1)
    nbHab_parVlg_Max = int(nbHabitants_parVillage_Reel * (1 + margeHabitants) + 1)
    
    
    
    
    
#### --- Nombre de personne dans chaque groupe ---
    
    TousLesMembres = fDis.serveurMegaLG.members

    for grp in listeGroupes :
        grp.personnes = []
        for member in TousLesMembres :
            if grp.salon.permissions_for(member).read_messages == True  and  not (fDis.roleBot in member.roles)  and  not (fDis.roleMaitre in member.roles) :
                grp.personnes.append(member)
        
        grp.nbPersonne = len(grp.personnes)
    
    
#### --- Nettoyages de listeGroupes ---

    listeVillages_Valides = []

#### Groupes vides || Suppression des groupes vides ou ne contanant qu'une personne (géré après en tant que personne manquante)
        
    listeGroupes = [grp for grp in listeGroupes if grp.nbPersonne >= 2]
        
    
    

#### Groupes bons || Villages déjà formés (groupes ayant un bon nombre de personne)
    
    def estUnSousGroupe_dUnVlgValide(grp):
        for vlg in listeVillages_Valides :
            for surGrp in vlg :
                if surGrp in grp.sur_Groupes :
                    return True
        return False
    
    
    listeVillages_Valides.extend([ (grp,)  for  grp   in listeGroupes          if grp.nbPersonne in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)])
    
    print("\n\nTous Les Villages Validés : nbHab_parVlg_Min", nbHab_parVlg_Min, ",    nbHab_parVlg_Max", nbHab_parVlg_Max)

    for vlg in listeVillages_Valides :
        
        print(vlg)
        
        for grp in vlg :
            print("      ", grp)
    
    
    
    listeVillages_Valides =      [ (grp,)  for (grp,) in listeVillages_Valides if not estUnSousGroupe_dUnVlgValide(grp)]
    
    print("\nTous Les Villages Validés (Après nettoyage) :" )

    for vlg in listeVillages_Valides :
        
        print(vlg)
        
        for grp in vlg :
            print("      ", grp)
    

    
    listeGroupes = [ grp for grp in listeGroupes if (grp.nbPersonne not in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)  and  not estUnSousGroupe_dUnVlgValide(grp) )]
    

    print("\n\nTous Les Groupes non vide restants :")

    for grp in listeGroupes :
        
        print(grp.nbPersonne, grp)
        


    
#### Groupes surchargés || Suppression des sur-groupes ayant un trop grand nombre de personnes
    
    def estUnSurGroupe(surGrp):
        for grp in listeGroupes :
            if surGrp in grp.sur_Groupes :
                return True
                
        return False


# Créations de village composé d'un seul sous-groupe ayant trop de membre
    listeVillages_Valides.extend([ (grp,)  for grp in listeGroupes   if (grp.nbPersonne >  nbHab_parVlg_Max  and  not estUnSurGroupe(grp))])


# Suppression des groupes ayant trop de membre (sur-groupes ==> A supprimer (les personnes supprimées sont gérés dans personnes manquantes) , sous-groupe ==> devenu des villages )
    listeGroupes =               [  grp    for grp in listeGroupes   if  grp.nbPersonne <= nbHab_parVlg_Max ]
    
 



    
    
#### --- Classement des Groupes par nombre de personne ---
    """
    PAS ENCORE UTILISE
    
    listeGroupes_Tries = []
    
    for i in range(1, nbHab_parVlg_Min + 1):
        listeGroupes_Tries.append([])
    
    for grp in listeGroupes :
        listeGroupes_Tries[grp.nbPersonne].append(grp)
    
    listeGroupes_Restants = list(listeGroupes_Tries)
    """
    
    
    composition_canton_Trouve = False
    
    while not composition_canton_Trouve :
        
        print("Tous Les Groupes :")
    
        for grp in listeGroupes:
            print(grp.nbPersonne, str(grp))
        
#### --- Listage de toutes les combinaison ---
        
        liste_VlgPossibles = []
    
#### Il y a peu de groupe : Listage complet
    
        if len(listeGroupes) <= 30 :
            
            for n in range(1,8):
                liste_VlgPossibles.extend( list(itertools.combinations(listeGroupes, n)) )
    
#### Il y a plus de groupe : Pré-triage et Listage des villages intéressants
    
    
#### Il y a trop de groupe : Listage impossible
        
        else :
            await fDis.channel("**ERREUR** - Il y a trop de groupes (> 30)")
        
        
        print("nbVillage Possible :", len(liste_VlgPossibles))
        
        
#### --- Tri des villages Possibles ---    
    
#### 1er Tri : Suppression des villages trop petit ou trop grop et des villages incohérents
        
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   nbHabitant(vlg) in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1) ]
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   not verifVlg_Incoherent(vlg)                                     ]

        print("nbVillage Possible restant :", len(liste_VlgPossibles))
    
#### 2ème Tri : Gestions des groupes Supprimé lors du 1er Tri
        
#### Listage des groupes manquants
        """
        grpManquant = list(listeGroupes)
        
        for vlg in liste_VlgPossibles :
            for grp in vlg :
                if grp in grpManquant :
                    grpManquant.remove(grp)
        """
        
        def verif_personneGrpDansVillagePossible(grp):
            for vlg in liste_VlgPossibles:
                if grp.personnes[0] in habitants(vlg) :
                    return True
                
            return False
        
        grpManquant = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillagePossible(grp) ]
        
        print("Groupes Manquants :")
    
        for grp in listeGroupes:
            print(grp.nbPersonne, str(grp))
        
#### Ajouts des petits groupes manquants au villages qui peuvent les accueillir 
        
        for grp in grpManquant :
            for vlg in liste_VlgPossibles : 
                if nbHabitant(vlg) + grp.nbPersonne < nbHab_parVlg_Max :
                    vlg += ( grp ,)
        
        grpManquant = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillagePossible(grp) ]
    
#### Formation d'un village avec les groupes manquants restants
        
        if len(grpManquant) != 0 :
            liste_VlgPossibles.append(tuple(grpManquant))
        
        print("\nTous Les Villages Possibles :" )

        for vlg in liste_VlgPossibles :
            
            print(vlg)
            
            for grp in vlg :
                print("      ", grp)
        
        print("\nTous Les Villages Validés :" )

        for vlg in listeVillages_Valides :
            
            print(vlg)
            
            for grp in vlg :
                print("      ", grp)
        
#### 3ème Tri : Suppresion des villages ayant les même habitants
        
        suppressionVlg_identiques(liste_VlgPossibles)
        suppressionVlg_identiques(listeVillages_Valides)
        
    
        
# Ici liste_VlgPossibles ne contient que :
#   - des villages de bonne taille          (sauf un eventuel village créer avec les groupes manquants restants)
#   - des villages cohérents INDEPENDAMMENT (cad pas de sous-groupe associer avec un de ses sur-groupe)
#   - des villages différents               (aucun village n'ont les même habitants)
    
    
    
    
    
#### --- Determination des villages validés ---
    
#### Mise de côté des village contenant un groupe présent qu'une fois
    
        for grp in listeGroupes :
            
            comptePresenceGrp = 0
            for vlg in liste_VlgPossibles :
                if grp in vlg :
                    comptePresenceGrp += 1
            
            if comptePresenceGrp == 1 :
                for vlg in liste_VlgPossibles :
                    if grp in vlg :
                        listeVillages_Valides.append(vlg)
                        liste_VlgPossibles.remove(vlg)
                        for grp in vlg :
                            listeGroupes.remove(grp)
                        
            if comptePresenceGrp == 0 :
                print(f"ERREUR - Un groupe a été oublié, il s'agit de {grp}")
                
                
        suppressionVlg_identiques(listeVillages_Valides)



#### ===== FIN DE LA BOUCLE ====

        if len(listeGroupes) == 0 :
            composition_canton_Trouve = True
            
        else :
            message = "On a tous tenté mais il reste des groupes qui respecte tous les critères, lesquels veux-tu choisir et garder (envoie les villages a garder sous cette forme : '12 54 94 2 0 47') :"
            
            for i in range(liste_VlgPossibles) :
                vlg = liste_VlgPossibles[i]
                message += f"\n> n°{i}    [{nbHabitant(vlg)}]   - (  "
                for grp in vlg :
                    message += f"{grp} ({grp.nbPersonne})   ,   "
                message += ")"
                
            await fDis.userCamp.send(message)
            reponse = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
            
            for j in reponse.content.split():
                listeVillages_Valides.append(liste_VlgPossibles[j])
                
            del(liste_VlgPossibles)
    
    
    
    
    message = "Voici la liste des villages définitive :"
            
    for i in range(listeVillages_Valides) :
        vlg = listeVillages_Valides[i]
        message += f"\n> n°{i}    [{nbHabitant(vlg)}]   - (  "
        for grp in vlg :
            message += f"{grp} ({grp.nbPersonne})   ,   "
    message += ")"



    """
    #### Suppression de villages qui contiennent des groupes de village déjà validé
    
    for vlg in listeVillages_Valides :
        for grp in vlg :
            for vlg2 in liste_VlgPossibles:
                if grp in vlg :
                    liste_VlgPossibles

    for grp in listeGroupes :
        
        vlgs_persGrpPresent = []
        
        for vlg in liste_VlgPossibles + listeVillages_Valides :
            if grp.personne in habitants(vlg) :
                vlgs_persGrpPresent.append(vlg)

    """
    """
    for grp in listeGroupes :
        
        vlgs_persGrpPresent = []
        
        for vlg in liste_VlgPossibles + listeVillages_Valides :
            if grp.personne in habitants(vlg) :
                vlgs_persGrpPresent.append(vlg)
        
        if len(vlgs_persGrpPresent) > 1 :
            for vlg in vlgs_persGrpPresent :
                
                """                







    
    

"""

################################################################################
#####                                                                      #####
#####                           - Paquet Roles -                           #####
#####                                                                      #####
################################################################################


### Création de paquetRoles, le paquet qui sera mélanger puis qui sera distribué aux joueurs

paquetRoles  = list(fRol.paquetRoles_Initial)

rd.shuffle(paquetRoles)




################################################################################
#####                                                                      #####
#####                      - Distribution des Rôles -                      #####
#####                                                                      #####
################################################################################


@fDis.bot.command()
@commands.has_permissions(ban_members = True)
async def Distrib (ctx):    
    
### Efface le !Distrib
    await fDis.effacerMsg(ctx)
        
    
# ----------------------------------------------
# --- Numérotation et distribution des rôles ---
# ----------------------------------------------
    
    Joueurs   = pd.DataFrame(fGoo.page1_InfoJoueurs.get_all_records())
    
    Ville   = []
    Annee   = []
    Filiere = []
    Comu    = []
    
    for j in Joueurs["Groupe"] :
        
        if j[:4] == "ISEN":
            Ville  .append(j[  -1])
            Annee  .append(j[  -3])
            Filiere.append(j[5:-4])
            Comu   .append("ISEN")
        
        else :
            Ville  .append("None")
            Annee  .append("None")
            Filiere.append("None")
            
            if   j != "Autre" :
                Comu   .append(j)
            else :
                Comu   .append("ZZZZZZZZ")
            
    
    Joueurs["Ville"]   = Ville
    Joueurs["Année"]   = Annee
    Joueurs["Filière"] = Filiere
    Joueurs["Comu"]    = Comu
    
### Rangement des joueurs par Ville, Année, Filière, Nom et enfin par Prénom

    JouRanges = Joueurs.sort_values(by = ["Comu", "Ville", "Année", "Filière", "Nom", "Prénom"])

    
### Numérotation et distribution des rôles    

    JouRanges["Mat"]  = range(1, len(JouRanges) + 1)
    JouRanges["Role"] = paquetRoles
    
    JouReduit = JouRanges.drop(["Ville", "Année", "Filière", "Comu"], axis = 1)
    
    JouTerm   = fGoo.dfToList(JouReduit)

    
### Caractéristiques des Rôles

    for num in range(1, len(JouRanges) + 1) :
        role = JouTerm[num][7]
        
        if   role == fRol.info_Ancien["nom"] : JouTerm[num][8] =    c.Ancien_nbProtec
        elif role == fRol.info_Sorcie["nom"] : JouTerm[num][8] = f"{c.Sorcie_nbPotVie} {c.Sorcie_nbPotMort}"
        elif role == fRol.info_LGNoir["nom"] : JouTerm[num][8] =    c.LGNoir_nbInfect


### Réécriture de Infos Joueurs et Sauvegarde

    fGoo.page1_InfoJoueurs.clear()
    fGoo.page1_InfoJoueurs.insert_rows(fGoo.strListe(JouTerm))
    
    fGoo.page1_Sauvegarde .clear()
    fGoo.page1_Sauvegarde .insert_rows(fGoo.strListe(JouTerm))
    
    
    
# ----------------------------------------------------
# --- Envoie des rôles et modification des pseudos ---
# ----------------------------------------------------

    for j in JouTerm[1:] :
        
#   j = [23, H, Clément, Campana, ISEN CSI 2 N, 269051521272905728, , "Loup-Garou", '', , '']
                
        membJou = fDis.serveurMegaLG.get_member(int(j[5]))
        
        await membJou.send(f"Vous êtes **{j[7]}** :")
        await membJou.send(embed = fRol.Role_avec(j[7])["embeds"])
        
        surnom  = membJou.display_name
        
        while len(surnom) > 26 :
            surnom = surnom[:-1]
        
        await membJou.edit(nick = f"{fMeP.AjoutZerosAvant(j[0],3)} | {surnom}")
    
    
    
# ---------------------------
# --- Rapports municipaux ---
# ---------------------------
    
    villePrec = ""
    anneePrec = ""
    filiePrec = ""
    groupPrec = ""
    
    msgJoueurs = await channelRapport.send("Recencement de début de Partie :\n\n\n\n")
    
    for j in dfToList(JouRanges)[1:] :
        
#   j = [23, H, Clément, Campana, ISEN CSI 2 N, 269051521272905728, , "Loup-Garou", '', , '', 'N', '2', 'CSI', 'ISEN']
#        0   1     2        3           4                5         6       7        8  9  10  11   12    13      14

        if groupPrec != j[14]:
            prefixe = "\n\n\n"
            if j[14] == "ISEN" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe +  "__**⬢⬢⬢⬢⬢   ISEN   ⬢⬢⬢⬢⬢**__")
            else               : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + f"__**⬢⬢⬢⬢⬢   {j[4]}   ⬢⬢⬢⬢⬢**__")
            villePrec = ""
            anneePrec = ""
            filiePrec = ""
        
        if j[14] == "ISEN" :
            if villePrec != j[11] :
                prefixe = ""
                if villePrec != "" : prefixe = "\n"
                if j[11] == "B" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   BREST   - ⬢⬢⬢**")
                if j[11] == "C" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   CAEN   - ⬢⬢⬢**")
                if j[11] == "N" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   NANTES   - ⬢⬢⬢**")
                if j[11] == "R" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   RENNES   - ⬢⬢⬢**")
                anneePrec = ""
                filiePrec = ""
            
            if anneePrec != j[12] :
                if j[12] == "1" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 1ère Année ---")
                if j[12] == "2" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 2ème Année ---")
                if j[12] == "3" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 3ème Année ---")
                if j[12] == "4" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 4ème Année ---")
                if j[12] == "5" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 5ème Année ---")
                if j[12] == "P" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- Profs ---")
                filiePrec = ""
                
            if filiePrec != j[13]  and  j[13] != "M"  and  j[12] != "P" :
                msgJoueurs = await ajoutMsg(msgJoueurs, f"\n> {j[13]}")
            
        villePrec = j[11]
        anneePrec = j[12]
        filiePrec = j[13]
        groupPrec = j[14]
        
        membJou = serveurMegaLG.get_member(int(j[5]))
        
        msgJoueurs = await ajoutMsg(msgJoueurs, f"\n>       ⬢ {membJou.mention} - {j[2]} {j[3]}")


"""



# %% --- Phase 3 ---

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Tour(ctx):
        
    await fDis.effacerMsg(ctx)
    await fTou.Tour()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Lancement(ctx):
    
    await fDis.effacerMsg(ctx)
    await attente_lancementTour()



async def attente_lancementTour() :
        
    m = v.maintenant()

#### ||| Variable ||| Si on est dans le WE on ne lance pas la fonction Tour

    if not v.partiePdt_Weekend  and  m.weekday() in (4,5) :
        await fDis.channelHistorique.send("Nous somme Vendredi ou Samedi, la fonction Lancement à été stoppée dans son élan !")
        return None
    
#### Attente qu'il soit 18h pour lancer la fontion Tour    

    tempsAtt = v.nuit_hDeb - m
                
    await fDis.channelHistorique.send(f"Attente de {tempsAtt} avant de lancer la nuit n°{v.nbTours}")
    
    if tempsAtt > v.timedelta(0) :
        await asyncio.sleep(tempsAtt.seconds)
    
    await fTou.Tour()



fDis.bot.run(fDis.tokenMJ)