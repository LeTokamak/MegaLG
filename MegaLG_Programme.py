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

Version Delta                             δ7                                04/06/2021

"""

version = "δ7"


# Phase
import MegaLG_P1    as fP1
import MegaLG_P23   as fP23


# Niveau D
fVlg = fP23.fVlg


# Niveau C
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





async def event_reactions():
    asyncio.create_task(        ajout_roleArtisans() , name = "Ajout du rôle d'Artisant" )
    asyncio.create_task( fP1.reaction_reInscription(), name = "Ré-Inscription"           )
    asyncio.create_task( fP1.reaction_Groupe()       , name = "Changement de Groupe"     )





# %%% Envoie d'un message

async def event_messages():
    asyncio.create_task( fP23.message_voteVillage()  , name = "Vote du village"          )
    asyncio.create_task( fP23.message_voteLoupGarou(), name = "Vote des Loups-Garous"    )





# %% Commandes

# %%% Commandes Générales

# %%%% Bug

async def declarationBug (descriptionBug):
    """
    N'a qu'un seul niveau de bug ==> Vilebrequin
    """
    
    messagesGif = []
    
    async for message in fDis.channelGifVilebrequin.history():
        messagesGif.append(message)
    
    messagesBug = []
    
    async for message in fDis.channelBugs.history():
        if "Bug n°" == message.content[:6] :
            messagesBug.append(message)

    
    try :
        numero = int( messagesBug[0].content.split() [1] [2:] ) + 1
        
    except :
        numero = 0
    
    strDescriptionBug = ' '.join(descriptionBug)
    
    await fDis.channelBugs.send(f"Bug n°{numero} :\n>>> " + strDescriptionBug )
    await fDis.channelBugs.send( rd.choice(messagesGif).content )
    await fDis.channelBugs.send( "_ _\n\n\n_ _")
    
    

@fDis.bot.command()
async def Bug (ctx, *descriptionBug):
    await declarationBug (descriptionBug)

@fDis.bot.command()
async def bug (ctx, *descriptionBug):
    await declarationBug (descriptionBug)





async def miseAJourBug (numeroBug, descriptionMaJ):
    
    msgBug = None
    listeMessage = []
    async for message in fDis.channelBugs.history(oldest_first = True):
        listeMessage.append(message)
        
        try : 
            if f"n°{numeroBug}" == message.content.split(" ") [1] :
                msgBug = message
                
        except :
            pass
    
    
    if msgBug != None :
        
        strDescriptionMaJ = ' '.join(descriptionMaJ)
        
        await msgBug.reply(content = f"Mise à Jour du Bug n°{numeroBug} :\n>>> " + strDescriptionMaJ)



@fDis.bot.command()
async def majBug (ctx, numeroBug, *descriptionMaJ):
    await miseAJourBug (numeroBug, descriptionMaJ)





async def suppressionBug (numeroBug):
    
    msgBug = None
    listeMessage = []
    async for message in fDis.channelBugs.history(oldest_first = True):
        listeMessage.append(message)
        
        try : 
            if f"n°{numeroBug}" == message.content.split(" ") [1] :
                msgBug = message
                
        except :
            pass
    
    
    if msgBug != None :
        
        indexMsgBug = listeMessage.index(msgBug)
        msgsASuppr  = listeMessage[ indexMsgBug : indexMsgBug + 3 ]
        
        for msg in listeMessage :
            
            try : 
                if msg.reference.message_id == msgBug.id :
                    msgsASuppr.apppend(msg)
                    
            except :
                pass
        
        for msg in msgsASuppr :
            await msg.delete()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def supprBug (ctx, numeroBug):
    await suppressionBug (numeroBug)





# %%%% Nettoyage

async def cmd_Nettoyage (ctx, nbMessages):
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
    await cmd_Nettoyage (ctx, nbMessages)
    
@fDis.bot.command()
async def nettoyage (ctx, nbMessages = 10**9) :
    await cmd_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def Net       (ctx, nbMessages = 10**9) :
    await cmd_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def net       (ctx, nbMessages = 10**9) :
    await cmd_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def N         (ctx, nbMessages = 10**9) :
    await cmd_Nettoyage (ctx, nbMessages)

@fDis.bot.command()
async def n         (ctx, nbMessages = 10**9) :
    await cmd_Nettoyage (ctx, nbMessages)

    
    


# %%%% Commandes des Habitants 

# %%%%% Vote

@fDis.bot.command()
async def Vote(ctx, matricule):
    await fVlg.cmd_vote(ctx.author, matricule)
    
    
@fDis.bot.command()
async def vote(ctx, matricule):
    await fVlg.cmd_vote(ctx.author, matricule)

    

    

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
async def Renommage(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)
    
@fDis.bot.command()
async def renommage(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)





# %%% Commandes des Admins

# %%%% Toujours Utilisables

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def EmbedsRoles (ctx):
    
    await fDis.effacerMsg(ctx.channel)
    await fDis.effacerMsg(fDis.channelRoles, 10**9)
    
    await fRol.envoie_Embeds_TousLesRoles()





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def SupprTousVlg (ctx):
    
    fVlg.redef_villagesExistants()
    
    for vlg in fVlg.TousLesVillages :
        
        await vlg.salonRapport  .delete()
        await vlg.salonCimetiere.delete()
        await vlg.salonBucher   .delete()
        await vlg.salonDebat    .delete()
        await vlg.vocalDebat    .delete()
        
        await vlg.salonVoteLG   .delete()
        await vlg.salonConseilLG.delete()
        await vlg.vocalConseilLG.delete()
        
        await vlg.salonFamilleNb.delete()
        await vlg.vocalFamilleNb.delete()
        
        await vlg.categorie     .delete()
        
        await vlg.roleDiscord   .delete()
        await vlg.roleDiscordMort.delete()





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def TachesEnCours (ctx):
    
    Taches = asyncio.all_tasks()
    
    print("\n\n################# Tâches en cours #################\n")

    for t in Taches :
        print(t.get_name(), t, t.done())

    print(  "\n###################################################\n")





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def emojis (ctx):
    
    print("\n\n################ Emojis du Serveur ################\n")

    for emoji in fDis.serveurMegaLG.emojis :
        print(emoji.name, emoji.id, emoji)

    print(  "\n###################################################\n")





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
    
    await fHab.redef_TousLesHabitants()
    
### Modification des pseudos de tout les joueurs
    Joueurs = fGoo.donneeGoogleSheet( fGoo.page1_InfoJoueurs )
    
    for j in Joueurs :
        
        membJou = fDis.serveurMegaLG.get_member( j[fGoo.clef_idDiscord] )
        await membJou.edit(nick = membJou.display_name[v.nbDigit_Matricule + 1 :])





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
    
    v.phaseEnCours = fDis.channelHistorique.topic [ : len(v.phase0)]
    
    await fDis.channelHistorique.send(f"```⬢ -  Je suis connecté ! ({version} | {v.phaseEnCours})  - ⬢```\n`{v.maintenant()}` - Début du 'on_ready'")
    
    
#### Redéfinition Groupes, Habitants et Villages
    
    await fGrp.redef_groupesExistants()
    
    
#### Lancement des events 
    
    asyncio.create_task( event_reactions() )
    asyncio.create_task( event_messages () )
    
    
#### Lancement des attendes d'épitaphe
    
    async for message in fDis.channelAttente.history():
        
        if fDis.Emo_Red == message.content.split()[0] :
            asyncio.create_task( fHab.cimetiere(message = message, rappelDeFonction = True), name = f"Re-Lancement de Cimetière de {message.content}.")
    
    await fDis.channelHistorique.send(f"`{v.maintenant()}` - Fin du 'on_ready'")
    
    
#### Phase 3 - Récupération du numéro de Tour et Lancement du Tour
    
    if v.phaseEnCours == v.phase3 :
        # Le topic de channelHistorique est de la forme "Phase 3 - Tour n°45"
        
        v.nbTours = int( fDis.channelHistorique.topic.split() [-1] [2:] )
        
        await fP23.attente_lancementTour()





# %% --- Phase 1 ---

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Debut_Phase1 (ctx):
    await fP1.lancementInscription()



# %%% Inscription

@fDis.bot.command()
async def Inscription (ctx) :
    await fP1.cmd_Inscription(ctx.author)
    
@fDis.bot.command()
async def inscription (ctx) :
    await fP1.cmd_Inscription(ctx.author)
    
@fDis.bot.command()
async def I (ctx) :
    await fP1.cmd_Inscription(ctx.author)
    
@fDis.bot.command()
async def i (ctx) :
    await fP1.cmd_Inscription(ctx.author)
    


# %%% Création d'un nouveau Groupe 

@fDis.bot.command()
async def Creation_SousGroupe(ctx):
    await fGrp.com_NouveauGroupe(ctx)
    
@fDis.bot.command()
async def creation_sousgroupe(ctx):
    await fGrp.com_NouveauGroupe(ctx)
    
@fDis.bot.command()
async def CreationSousGroupe(ctx):
    await fGrp.com_NouveauGroupe(ctx)
    
@fDis.bot.command()
async def creationSGrp(ctx):
    await fGrp.com_NouveauGroupe(ctx)
    
@fDis.bot.command()
async def creatSGrp(ctx):
    await fGrp.com_NouveauGroupe(ctx)
    
@fDis.bot.command()
async def csg(ctx):
    await fGrp.com_NouveauGroupe(ctx)






# %% --- Phase 2 ---

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DebutPartie (ctx):
    
    await fDis.channelHistorique.edit(topic = v.phase2)
        
    await fP23.finInscription()
    await fP23.numerotationHabitants()
    await fP23.repartionGroupes_Villages()
    

    for vlg in fVlg.TousLesVillages :
        await fP23.distributionRole(vlg)

    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
    
    v.nbTours = 0
    await fDis.channelHistorique.edit(topic = f"{v.phase3} - Tour n°{v.nbTours}")
    
    await fP23.attente_lancementTour()






# %% --- Phase 3 ---

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Lancement(ctx):
    
    await fDis.effacerMsg(ctx)
    await fP23.attente_lancementTour()






fDis.bot.run(fDis.tokenMJ)