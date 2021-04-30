# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---                               Events et Commandes                              ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                28/04/2021
"""


# Niveau E
import E_fct_Tour               as fTou

# Niveau D
fVlg = fTou.fVlg

# Niveau C
import C_fct_Inscription        as fIns
fHab = fVlg.fHab

# Niveau B
fGrp = fHab.fGrp

# Niveau A
fGoo = fHab.fGoo
fDis = fHab.fDis

v    = fHab.v

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
    
    print("Lancement role Artisans")
    
    def verifArtisans(payload):
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifMessage = payload.message_id == idMessage_Artisans
        
        return verifUser  and  verifMessage
    
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifArtisans)
        await payload.member.add_roles(fDis.roleArtisans)



async def reaction_reInscription():
    
    print("Lancement reInscription")
    
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
    
    print("Lancement Groupe")
    
    def verifGroupe(payload):
        salon        = fDis.serveurMegaLG.get_channel(payload.channel_id)
        
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifPhase   = v.phaseEnCours     == v.phase1
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

async def message_Inscription():
    
    def verifInscription(message):
        verifPhase = verifSalon = False
        verifUser  = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
        
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
        verifPhase = verifSalon = False
        verifUser  = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
        
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
        verifPhase = verifSalon = False
        verifUser  = message.author.id not in (fDis.userMdJ.id, fDis.userAss.id)  and  fDis.roleMaitre not in message.author.roles
        
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