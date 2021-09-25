# -*- coding: utf-8 -*-

"""
======================================================================================
===                                                                                ===
===                                     Phase 0                                    ===
===                                                                                ===
======================================================================================
                                          v1                                29/05/2021
"""


# Niveau C
import C___habitant       as fHab

# Niveau B

# Niveua A
fGoo = fHab.fGoo
fDis = fHab.fDis
v    = fHab.v



rd      = fHab.rd
asyncio = fHab.asyncio



# %% Events
     
@fDis.bot.event
async def on_member_join (member):
    """
    Assigne le rôle de Spectateur aux nouveaux membres.
    """
    
    await member.add_roles(fDis.roleSpectateurs)
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyGreen}  |  {member.mention} vient d'arriver sur le serveur !")





@fDis.bot.event
async def on_member_remove(member):
    """
    Tue les joueurs venants de quitter le serveur.
    """
    
    await fDis.channelHistorique.send(f"{fDis.Emo_BabyBlack}  |  {member} vient de quitter le serveur !")
    
    if v.phaseEnCours == v.phase3  and  fDis.roleJoueurs in member.roles :
        
        fHab.redef_TousLesHabitants()
        
        persPartie = fHab.habitant_avec(member.id)
        await fDis.channelHistorique.send(f"Il était un joueur : {persPartie.user.mention}  |  {persPartie.matricule} {persPartie.prenom} {persPartie.nom} - ( {persPartie.groupe} ) !")
        
        await persPartie.Tuer(departServeur = True)
        await persPartie.user.send("Vous avez quitté le serveur, vous avez donc été tué...")





@fDis.bot.event
async def on_typing(salon, user, quand):
    """
    Ajoute un message tapé dans page_CompteMsg à la colonne et à la ligne correspondante.
    """
    
#### Recherche de la bonne colonne

    if   type(salon) == fDis.discord.channel.TextChannel  and  salon.name not in fGoo.clefs_Messages :
        fGoo.ajout_nouvColonne(salon.name, fGoo.page_CompteMsg)
        fGoo.clefs_Messages.append(salon.name)
        
        clef_salon = salon.name
    
    elif type(salon) == fDis.discord.channel.DMChannel : clef_salon = fGoo.clefMsg_DMChannel 
    else                                               : clef_salon = salon.name
    
    
    
#### Recherche de la bonne ligne
    
    ligne, numero_ligne = fGoo.ligne_avec(user.id, fGoo.clefMsg_idDiscord, fGoo.donneeGoogleSheet(fGoo.page_CompteMsg))
    
    if numero_ligne != None :
        fGoo.ajoutVal_cellule( 1, 
                               clef_salon,          numero_ligne,
                               fGoo.page_CompteMsg, typeObjetCellule = int)
        
    else :
        nvlLigne = { fGoo.clefMsg_idDiscord    : user.id ,
                     fGoo.clefMsg_display_name : user.display_name ,
                     clef_salon                : 1 
                   }
        
        fGoo.ajoutLigne(nvlLigne, fGoo.page_CompteMsg)





idMessage_Artisans = 856186925462454282

async def ajout_roleArtisans():
    
    def verifArtisans(payload):
        verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
        
        verifMessage = payload.message_id == idMessage_Artisans
        
        return verifUser  and  verifMessage
    
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifArtisans)
        
        await payload.member.add_roles(fDis.roleArtisans)






# %% Commande de Bug

# %%% Déclaration d'un nouveau Bug

async def declarationBug (descriptionBug, niveau_bug):
    """
    Gère des bugs pouvant avoir deux niveaux :
        Le niveau 1 - le moins grave
        Le niveau 2 - le plus grave
        
    En fonction du niveau du bug, le gif ne sera pas le même et le message variera
    """

#### Sélection du gif

    messagesGif = []
    
    if niveau_bug == 1 : channel_Gif = fDis.channelGifBug_Petit
    if niveau_bug == 2 : channel_Gif = fDis.channelGifBug_Gros
    
    async for message in channel_Gif.history():
        messagesGif.append(message)
    
    url_gif_choisi = rd.choice(messagesGif).content
    
    

#### Recherche du numéro du nouveau bug
    
    messagesBug = []
    
# Sélection des messages dans channel bug annonçant un bug 
    
    async for message in fDis.channelBugs.history():
        if "Bug n°" == message.content[:6] :
            messagesBug.append(message)

    
# Chois du numéro du nouveau bug, soit le numéro suivant, soit 0

    try :
        numero = int( messagesBug[0].content.split() [1] [2:] ) + 1
        
    except :
        numero = 0
    


#### Envoie du message de bug
    
    if niveau_bug == 1 : description_niveau = "*(Bug mineur)*"
    if niveau_bug == 2 : description_niveau = "**(Bug majeur)**"

    strDescriptionBug = ' '.join(descriptionBug)
    
    await fDis.channelBugs.send(f"Bug n°{numero} : {description_niveau}\n>>> " + strDescriptionBug )
    await fDis.channelBugs.send( url_gif_choisi )
    await fDis.channelBugs.send( "_ _\n\n\n_ _")
    
    
    
    

@fDis.bot.command(aliases = ["Bug", "bug", "B", "b"])
async def Bug_niveau_1 (ctx, *descriptionBug):
    await declarationBug (descriptionBug, niveau_bug = 1)
    

@fDis.bot.command(aliases = ["Bug2", "bug2", "B2", "b2"])
async def Bug_niveau_2 (ctx, *descriptionBug):
    await declarationBug (descriptionBug, niveau_bug = 2)





# %%% Mise à Jour d'un Bug

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






# %%% Suppression d'un Bug

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





# %% Commandes des Admins

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





# %% Commandes de contrôle

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def tachesEnCours (ctx):
    
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