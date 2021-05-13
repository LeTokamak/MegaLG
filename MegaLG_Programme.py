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

Version Delta                             δ3                                12/05/2021

"""

version = "δ3"


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
            verifUser  = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
            verifPhase = v.phaseEnCours == v.phase3
            
            if verifUser and verifPhase :
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
            verifUser  = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
            verifPhase = v.phaseEnCours == v.phase3
            
            if verifUser and verifPhase :
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

# %%%% Bug

@fDis.bot.command()
async def Bug (ctx, *descriptionBug):
    """
    N'a qu'un seul niveau de bug ==> Vilebrequin
    """
    
    messagesGif = []
    
    async for message in fDis.channelGifVilebrequin.history():
        messagesGif.append(message)
    
    print("########### Fct Bug ############")
    
    messagesBug = []
    
    async for message in fDis.channelBugs.history():
        print("Contenu message", message.content)
        if "Bug n°" == message.content[:6] :
            messagesBug.append(message)
    
    print(messagesBug)

    
    try :
        numero = int( messagesBug[0].content.split() [1] [2:] ) + 1
        
    except :
        numero = 0
        
    print(numero)
    
    await fDis.channelBugs.send(f"Bug n°{numero} : \n>>> { ' '.join(descriptionBug) }")
    await fDis.channelBugs.send( rd.choice(messagesGif).content )
    await fDis.channelBugs.send( "_ _\n\n\n_ _")
    
    
    
    

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
    
    
    


# %%%% Commandes des Habitants 

# %%%%% Vote

@fDis.bot.command()
async def Vote(ctx, matricule):
    await fVlg.cmd_voteVlg(ctx.author, matricule)
    
    
@fDis.bot.command()
async def vote(ctx, matricule):
    await fVlg.cmd_voteVlg(ctx.author, matricule)



# %%%%% VoteLG

@fDis.bot.command()
async def VoteLG(ctx, matricule):
    await fVlg.cmd_voteLG(ctx.author, matricule)

@fDis.bot.command()
async def voteLG(ctx, matricule):
    await fVlg.cmd_voteLG(ctx.author, matricule)
    
@fDis.bot.command()
async def votelg(ctx, matricule):
    await fVlg.cmd_voteLG(ctx.author, matricule)
    
    

# %%%%% Exil (reservée aux Juges et au Maire)

@fDis.bot.command()
async def Exil(ctx):
    await fVlg.cmd_demandeExilVote(ctx.author)

@fDis.bot.command()
async def exil(ctx):
    await fVlg.cmd_demandeExilVote(ctx.author)
    

    


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
async def SupprTousVlg (ctx):
    
    for vlg in fVlg.TousLesVillages :
        
        await vlg.salonRapport  .delete()
        await vlg.salonBucher   .delete()
        await vlg.salonDebat    .delete()
        await vlg.vocalDebat    .delete()
        
        await vlg.salonVoteLG   .delete()
        await vlg.salonConseilLG.delete()
        await vlg.vocalConseilLG.delete()
        
        await vlg.salonFamilleNb.delete()
        await vlg.vocalFamilleNb.delete()
    
        await vlg.roleDiscord   .delete()





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def TachesEnCours (ctx):
    
    Taches = asyncio.all_tasks()
    
    print("\n\n################# Tâches en cours #################\n")
    
    for t in Taches :
        print(t.get_name(), t, t.done())

    print("\n###################################################\n")





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
    
    async for message in fDis.channelHistorique.history():
        
        if "```Phase " in message.content  and  not phaseTrouvee :
            v.phaseEnCours = message.content
            phaseTrouvee = True
    
    await fDis.channelHistorique.send(f"```⬢ -  Je suis connecté ! ({version} | {v.phaseEnCours[3:-3]})  - ⬢```\n{v.maintenant()}")
    
    
#### Redéfinition Groupes, Habitants et Villages
    
    await fGrp.redef_groupesExistants()
    
    
#### Lancement des events 
    
    asyncio.Task( event_reactions() )
    asyncio.Task( event_messages () )
    
    
#### Lancement des attendes d'épitaphe
    
    async for message in fDis.channelAttente.history():
        
        if fDis.Emo_Red == message.content.split()[0] :
            asyncio.Task( fHab.cimetiere(message = message, rappelDeFonction = True) )
    
    await fDis.channelHistorique.send(f"```⬢ -  Fin du 'on_ready'  - ⬢```\n{v.maintenant()}")
    
    
#### Phase 3 - Récupération du numéro de Tour
    
    if v.phaseEnCours == v.phase3 :
        # Le topic de channelHistorique est de la forme "Tour n°45"
        
        v.nbTours = int(fDis.channelHistorique.topic[7: ])
    
    
#### Phase 3 - Lancement du Tour
        
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
    
    v.phaseEnCours = v.phase2
    await fDis.channelHistorique.send(v.phaseEnCours)
    
    await finInscription()
    await numerotationHabitants()
    await repartionGroupes_Villages()
    

    #for vlg in fVlg.TousLesVillages :
        #await distributionRole(vlg)

    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
        
    v.phaseEnCours = v.phase3
    await fDis.channelHistorique.send(v.phaseEnCours)
    
    v.nbTours = 0
    await fDis.channelHistorique.edit(topic = f"Tour n°{v.nbTours}")
    
    await attente_lancementTour()







async def finInscription():
    
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
        
#   j = ['', H, Clément, CAMPANA, 27, 0, 269051521272905728, '', '', '']
                
        membJou = fDis.serveurMegaLG.get_member(int(j[6]))
                
        surnom  = membJou.display_name
        
        while len(surnom) > 26 :
            surnom = surnom[ :-1]
        
        await membJou.edit(nick = f"{fMeP.AjoutZerosAvant(j[0],3)} | {surnom}")
    
    


    fGoo.page1_InfoJoueurs.clear()
    fGoo.page1_InfoJoueurs.insert_rows(fGoo.strListe(listeJoueurs))
    
    fGoo.page1_Sauvegarde .clear()
    fGoo.page1_Sauvegarde .insert_rows(fGoo.strListe(listeJoueurs))







async def repartionGroupes_Villages() :
    
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
                if vlg != vlg2  and  habitants(vlg) == habitants(vlg2):
                    liste_vlg.remove(vlg)
    
    
    def estUnSousGroupe_dUnVlgValide(grp):
        for vlg in listeVillages_Valides :
            for surGrp in vlg :
                if surGrp in grp.sur_Groupes :
                    return True
        return False
    
    
    def estUnSurGroupe(surGrp):
        for grp in fGrp.TousLesGroupes :
            if surGrp in grp.sur_Groupes :
                return True
                
        return False
    
    
    
#### --- Variables ---
    
    listeGroupes   = list(fGrp.TousLesGroupes)
    
    margeHabitants = 0.00 #0.05
    
    TousLesJoueurs = fDis.roleJoueurs.members
    
    nbHabitants_parVillage_Souhaite = 5
    
    nbVillages_Reel                 = 0
    nbHabitants_parVillage_Reel     = nbHabitants_parVillage_Souhaite
    
    ecartMin                        = len(TousLesJoueurs) + 1
    
    for n in range( 1, len(TousLesJoueurs) + 1 ):
        ecart = abs(len(TousLesJoueurs)/n - nbHabitants_parVillage_Souhaite)
        
        if ecart < ecartMin :
            nbVillages_Reel             = n
            nbHabitants_parVillage_Reel = len(TousLesJoueurs) // n
            
            ecartMin                    = ecart
    
    
    nbHab_parVlg_Min = int( nbHabitants_parVillage_Reel * (1 - margeHabitants) - 1 )
    nbHab_parVlg_Max = int( nbHabitants_parVillage_Reel * (1 + margeHabitants) + 1 )
    
    listeVillages_Valides = []
    
    
    
    
    
#### --- Nombre de personne dans chaque groupe ---

    for grp in listeGroupes :
        grp.personnes = []
        for member in TousLesJoueurs :
            if grp.salon.permissions_for(member).read_messages == True :
                grp.personnes.append(member)
        
        grp.nbPersonne = len(grp.personnes)
    
    
    
    
#### --- Nettoyages de listeGroupes ---
    
#### Groupes vides || Suppression des groupes vides ou ne contanant qu'une personne (géré après en tant que personne manquante)
    
    listeGroupes = [grp for grp in listeGroupes if grp.nbPersonne >= 2]
    
    
    
#### Groupes bons || Villages déjà formés (groupes ayant un bon nombre de personne)    
    
    listeVillages_Valides.extend([ (grp,)  for  grp   in listeGroupes          if grp.nbPersonne in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)])
    listeVillages_Valides =      [ (grp,)  for (grp,) in listeVillages_Valides if not estUnSousGroupe_dUnVlgValide(grp)]
    
    
    listeGroupes = [ grp for grp in listeGroupes if (grp.nbPersonne not in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)  and  not estUnSousGroupe_dUnVlgValide(grp) )]
    
    
    
#### Groupes surchargés || Suppression des sur-groupes ayant un trop grand nombre de personnes
    
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
    
    
    
    
    
#### --- Listage de toutes les combinaison ---
    
    composition_canton_Trouve = False
    
    while not composition_canton_Trouve :
        
        liste_VlgPossibles = []
    
#### Il y a peu de groupe : Listage complet
        
        if len(listeGroupes) <= 30 :
            
            for n in range(1,8):
                liste_VlgPossibles.extend( list(itertools.combinations(listeGroupes, n)) )
                
#### Il y a plus de groupe : Pré-triage et Listage des villages intéressants
        
        
#### Il y a trop de groupe : Listage impossible
        
        else :
            await fDis.channelHistorique.send("**ERREUR** - Il y a trop de groupes (> 30)")
        
        
        
        
        
#### --- Tri des villages Possibles ---    
    
#### 1er Tri : Suppression des villages trop petit ou trop grop et des villages incohérents
        
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   nbHabitant(vlg) in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1) ]
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   not verifVlg_Incoherent(vlg)                                     ]
        
        
        
#### 2ème Tri : Gestions des groupes Supprimé lors du 1er Tri
        
#### Listage des groupes manquants

        def verif_personneGrpDansVillage(liste_Vlg, grp):
            for vlg in liste_Vlg:
                if grp.personnes[0] in habitants(vlg) :
                    return True
                
            return False
        
        grpManquant = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillage(liste_VlgPossibles, grp) ]
        
#### Ajouts des petits groupes manquants au villages qui peuvent les accueillir 
        
        for grp in grpManquant :
            for vlg in liste_VlgPossibles : 
                if nbHabitant(vlg) + grp.nbPersonne < nbHab_parVlg_Max :
                    vlg += ( grp ,)
        
        grpManquant = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillage(liste_VlgPossibles, grp) ]
    
#### Formation d'un village avec les groupes manquants restants
        
        if len(grpManquant) != 0 :
            liste_VlgPossibles.append(tuple(grpManquant))
        
        
        
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
        
        
        
        suppressionVlg_identiques(listeVillages_Valides)
        
        listeGroupes = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillage(listeVillages_Valides, grp) ]
        
        
        
#### ===== FIN DE LA BOUCLE ====

        if len(listeGroupes) == 0 :
            composition_canton_Trouve = True
            
        else :
            message = "On a tous tenté mais il reste des groupes qui respecte tous les critères, lesquels veux-tu choisir et garder (envoie les villages a garder sous cette forme : '12 54 94 2 0 47') :"
            
            for i in range(len(liste_VlgPossibles)) :
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
    
    
    

    
#### --- Suppression des villages qui contiennent toutes les pers d'un autre village ---
    
    for vlg in listeVillages_Valides :
        for vlg2 in listeVillages_Valides :
            
            habDansVlg2 = True
            
            for hab in habitants(vlg) :
                habDansVlg2 = habDansVlg2  and  hab in habitants(vlg2)
            
            if habDansVlg2 and vlg != vlg2 :
                listeVillages_Valides.remove(vlg)
    
    
    
#### --- Transformation des villages validés en liste d'habitants ---
    
    liste_VlgValides_Habs = []
    
    for vlg in listeVillages_Valides:
        liste_VlgValides_Habs.append( habitants(vlg) )
    
    
    
#### --- Gestion des personnes manquantes ---
    
    listeJoueursRestants = list(TousLesJoueurs)
    for vlg in listeVillages_Valides :
        for hab in habitants(vlg):
            try :
                listeJoueursRestants.remove(hab)
            except :
                print(f"ERREUR - Cette personne a déjà été supprimmé : {hab.display_name} ({vlg})")
    
    
    if len(listeJoueursRestants) in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1) :
        liste_VlgValides_Habs.append(tuple(listeJoueursRestants))
        listeJoueursRestants = []
    
    
    
#### Ajout des personnes restantes aux autres villages (manuellement)
    
    for joueur in listeJoueursRestants :
        
        grpJoueur = None
        for grp in fGrp.TousLesGroupes :
            if grp.salon.permissions_for(joueur).read_messages == True :
                grpJoueur = grp
        
        
        message = f"Il reste {joueur} (il est dans {grpJoueur}) (envoie le village sous cette forme : '12') :"
        
        for i in range(len(listeVillages_Valides)) :
            vlg = listeVillages_Valides[i]
            message += f"\n> n°{i}    [{len(liste_VlgValides_Habs[i])}]   - (  "
            for grp in vlg :
                message += f"{grp} ({grp.nbPersonne})   ,   "
            message += ")"
        
        await fDis.userCamp.send(message)
        reponse = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
        
        liste_VlgValides_Habs[int(reponse.content)].append(joueur)
    
    
    
#### Création d'un village avec toutes les personnes restantes, si possible
    
    message = "Voici la liste des villages définitive :"
    
    for i in range(len(liste_VlgValides_Habs)) :
        vlg = liste_VlgValides_Habs[i]
        message += f"\n> n°{i}    [{len(vlg)}]   - (   "
        for joueur in vlg :
            message += f"{joueur.display_name}   ,   "
        message += ")"
    
    await fDis.userCamp.send(message)
    
    
    
#### --- Création des villages ---
    
    donneeJoueur = fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs)
    
#### Association des habitants à leur village
    
    for i in range(len(liste_VlgValides_Habs)) :
        
        vlg = liste_VlgValides_Habs[i]
        
        for hab in vlg :
            ligne, numLigne = fGoo.ligne_avec( hab.id, fGoo.clef_idDiscord, donneeJoueur )
            fGoo.remplacerVal_ligne( i+1 , fGoo.clef_numVillage, numLigne, fGoo.page1_InfoJoueurs )
        
        await asyncio.sleep(1)
    
    await fHab.redef_TousLesHabitants()
    
#### Création des villages
    
    for i in range(len(liste_VlgValides_Habs)) :
    
        await fVlg.creationVillage( numNouvVillage = i+1 )
        
        await asyncio.sleep(0.5)







async def distributionRole(village):
    
#### Paquet des Rôles
    
    paquetRoles  =   []
    
    paquetRoles += 0*[fRol.role_Villageois]
    paquetRoles += 1*[fRol.role_VillaVilla]
    paquetRoles += 1*[fRol.role_Cupidon   ]
    paquetRoles += 0*[fRol.role_Ancien    ]
    
    paquetRoles += 2*[fRol.role_Salvateur ]
    paquetRoles += 2*[fRol.role_Sorciere  ]
    paquetRoles += 2*[fRol.role_Voyante   ]
    
    paquetRoles += 2*[fRol.role_Corbeau   ]
    paquetRoles += 2*[fRol.role_Hirondelle]
    paquetRoles += 2*[fRol.role_Juge      ]
    
    paquetRoles += 5*[fRol.role_FamilleNb ]
    
    
    
    paquetRoles += 4*[fRol.role_LG        ]
    paquetRoles += 1*[fRol.role_LGNoir    ]
    paquetRoles += 1*[fRol.role_LGBleu    ]
    
    paquetRoles += 3*[fRol.role_LGBlanc   ]
    paquetRoles += 2*[fRol.role_EnfantSauv]
    
    
    
#### Paquet des Rôles Restants
    
    paquetRoles_Restant = list(paquetRoles)
    
    rd.shuffle(paquetRoles_Restant)
    


#### --- Distribution des Rôles ---
    
    for hab in village.habitants :
        
        if len(paquetRoles_Restant) != 0 :
            habRole = paquetRoles_Restant.pop(0)
            
        else :
            habRole = rd.choice(paquetRoles)
        
        
        
#### Caractéristiques des Rôles

        if   habRole == fRol.role_Ancien   : caractRole =    v.Ancien_nbProtec
        elif habRole == fRol.role_Sorciere : caractRole = f"{v.Sorcie_nbPotVie} {v.Sorcie_nbPotMort}"
        elif habRole == fRol.role_Juge     : caractRole =    v.Juge_nbExil
        elif habRole == fRol.role_LGNoir   : caractRole =    v.LGNoir_nbInfect
        
        
        
#### Enregistrement
        
        ligne, numLigne = fGoo.ligne_avec( hab.matri, fGoo.clef_Matricule, fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs) )
        
        fGoo.remplacerVal_ligne( habRole[fRol.clefNom], fGoo.clef_Role       , numLigne, fGoo.page1_InfoJoueurs )
        fGoo.remplacerVal_ligne( caractRole           , fGoo.clef_caractRoles, numLigne, fGoo.page1_InfoJoueurs )
        
        await asyncio.sleep(0.1)
        
        
        
#### Envoie du Rôle
        
        await hab.member.send( f"Vous êtes **{habRole[fRol.clefNom]}** :" )
        await hab.member.send( embed = habRole[fRol.clefEmbed]            )
        
        



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