# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---          Niveau A - Fonctions et Constantes liées au Serveur Discord           ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


import discord
from   discord.ext import commands

# %% Constantes des serveurs

def def_constantes_discord ():
    """
    Redef de toutes les variables liés au serveur
    """
    
    print("Redef des Constantes liées à Discord")
    
    def_serveur   ()
    def_userAdmins()
    def_categories()
    def_salons    ()
    def_roles     ()





# %%% Bot

intentions = discord.Intents.all()
bot        = commands.Bot(command_prefix = '!', description = "Maître du Jeu", intents = intentions)

tokenMJ    = "NzM3NzE3MTkxNTI0NDgzMTIy.XyBarA.A83hDJo-1XCRMatEUxAWIlcmaI0" # Maitre du Jeu




# %%% Serveur

serveurMegaLG    = None
serveurMegaLG_LG = None
serveurMegaLG_FN = None

lien_serveurMegaLG_LG = "https://discord.gg/ch8rTdQXcb"
lien_serveurMegaLG_FN = "https://discord.gg/r6b6g7fpY3"

def def_serveur ():
    """
    Cette Fonction ne renvoie rien
    
    Elle doit être appelé lors du on_ready() pour définir serveurMegaLG, une fois que le bot est connecté 
    """
    global serveurMegaLG, serveurMegaLG_LG, serveurMegaLG_FN
    
    serveurMegaLG    = bot.get_guild (769495045308940288)
    serveurMegaLG_LG = bot.get_guild (899230046286385152)
    serveurMegaLG_FN = bot.get_guild (905945526950838273)





# %%% Users des Admins

userCamp = None
userMdJ  = None
userAss  = None

def def_userAdmins ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir les users des admins, une fois que le bot est connecté 
    """
    global userCamp
    
    userCamp = bot.get_user (269051521272905728)
    
    global userMdJ, userAss
    
    userMdJ  = bot.get_user (737717191524483122)
    userAss  = bot.get_user (783276858623000577)





# %%% Categories

CategoryChannel_GestionGrp = None

def def_categories ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir les categoryChannels du serveur, une fois que le bot est connecté 
    """
    
    global CategoryChannel_GestionGrp
    
    CategoryChannel_GestionGrp = bot.get_channel        (818582430100750376)





# %%% Channels

channelGeneral        = None

channelRegles         = None
channelInscription    = None
channelInfos          = None
channelRoles          = None

channelBugs           = None
channelAmeliorations  = None

channelHistorique     = None
channelAttente        = None

channelGifBug_Petit   = None
channelGifBug_Gros    = None

channelFctmentGrp     = None
channelGalaxie        = None
channelEtoile         = None
channelPlanete        = None
channelLune           = None



def def_salons ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir tout les channels du serveur, une fois que le bot est connecté 
    """
    
    global channelGeneral
    
    channelGeneral        = bot.get_channel        (790691318786949201)
    
    
    
#### ― Explications ―
    
    global channelInfos, channelInscription, channelRoles, channelRegles
    
    channelRegles         = bot.get_channel        (810553761164558346)
    channelInscription    = bot.get_channel        (845186482263293962)
    channelInfos          = bot.get_channel        (770001767634305115)
    channelRoles          = bot.get_channel        (770002724074291212)
    
    
    
#### ― Modifs ―
    
    global channelBugs, channelAmeliorations
    
    channelBugs           = bot.get_channel        (841694226206294036) 
    channelAmeliorations  = bot.get_channel        (810554730383671297)
    
    
    
#### ✽ - Bot - ✽

    global channelHistorique, channelAttente

    channelHistorique     = bot.get_channel        (782626433255997480)
    channelAttente        = bot.get_channel        (789105310408900619)
    

#### ✽ - Gifs et Autres - ✽

    global channelGifBug_Petit, channelGifBug_Gros

    channelGifBug_Petit   = bot.get_channel        (818580306318721055)
    channelGifBug_Gros    = bot.get_channel        (889911450309632102)
    
    
    
#### Gestion des Groupes
    
    global channelFctmentGrp, channelGalaxie, channelEtoile, channelPlanete, channelLune
    
    channelFctmentGrp     = bot.get_channel        (820420551931068436)
    channelGalaxie        = bot.get_channel        (823477780142489661)
    channelEtoile         = bot.get_channel        (818580520765751296)
    channelPlanete        = bot.get_channel        (818580935380303903)
    channelLune           = bot.get_channel        (818581474856140841)
    
    





# %%% Roles du Serveur

roleEveryone   , roleModerateur , roleBot = (None, None, None)
roleEveryone_LG, roleEveryone_FN          = (None, None      )
roleMdJ        , roleAssistant            = (None, None      )
roleArtisans   , roleSpectateurs          = (None, None      )
roleJoueurs    , roleMorts                = (None, None      )
roleISEN_Nantes                           =  None


id_roleEveryone    = 769495045308940288
id_roleModerateur  = 782627464530755604
id_roleBot         = 783283411833978901

id_roleEveryone_LG = 899230046286385152
id_roleEveryone_FN = 905945526950838273

id_roleMdJ         = 769496917797109771
id_roleAssistant   = 783281237481619467

id_roleArtisans    = 769985455470018620
id_roleSpectateurs = 795550455224205312

id_roleJoueurs     = 782625030123159562
id_roleMorts       = 790158481634099250

id_roleISEN_Nantes = 848145158561202227


def def_roles ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir tout les rôles du serveur, une fois que le bot est connecté 
    """
    
    global roleEveryone, roleModerateur, roleBot
    
    roleEveryone          = serveurMegaLG.get_role (id_roleEveryone)
    roleModerateur        = serveurMegaLG.get_role (id_roleModerateur)  
    roleBot               = serveurMegaLG.get_role (id_roleBot)
    
    
    global roleEveryone_LG, roleEveryone_FN
    
    roleEveryone_LG       = serveurMegaLG_LG.get_role (id_roleEveryone_LG)
    roleEveryone_FN       = serveurMegaLG_FN.get_role (id_roleEveryone_FN)  
    
    
    
    global roleMdJ, roleAssistant
    
    roleMdJ               = serveurMegaLG.get_role (id_roleMdJ)
    roleAssistant         = serveurMegaLG.get_role (id_roleAssistant)
    
    
    global roleArtisans, roleSpectateurs, roleJoueurs, roleMorts
    
    roleArtisans          = serveurMegaLG.get_role (id_roleArtisans)
    roleSpectateurs       = serveurMegaLG.get_role (id_roleSpectateurs)
    
    roleJoueurs           = serveurMegaLG.get_role (id_roleJoueurs)
    roleMorts             = serveurMegaLG.get_role (id_roleMorts)
    
    
    global roleISEN_Nantes
    
    roleISEN_Nantes       = serveurMegaLG.get_role (id_roleISEN_Nantes)









# %%% Emojis du Serveur

Emo_Maire         = ":military_medal:"

Emo_Villageois    =           "<:Villageois:788784861682204682>"
Emo_Voyante       =            "<:V_Voyante:788784786164285482>"
Emo_Salvateur     =          "<:V_Salvateur:788778406337576981>"
Emo_Sorciere      =           "<:V_Sorciere:788784785941332000>"
Emo_PttFille      =       "<:V_Petite_Fille:788784786280808458>"
Emo_Hirondelle    =           "<:V_Hironlle:788833861253595176>"
Emo_FNSoeur       =           "<:V_FN_Soeur:788778409253011507>"
Emo_FNFrere       =           "<:V_FN_Frere:788778408997683281>"
Emo_Cupidon       =            "<:V_Cupidon:788784786155634719>"
Emo_Corbeau       =            "<:V_Corbeau:788778409203073054>"
Emo_Chasseur      =          "<:V_Chassseur:788784786332319774>"
Emo_Ancien        =             "<:V_Ancien:788778406476251146>"
Emo_Juge          =               "<:V_Juge:839754641192648704>"
Emo_Voyante_dAura =       "<:V_Voyant_dAura:911400602557358080>"

Emo_LoupGarou     =           "<:Loup_Garou:788778408477327401>"
Emo_LGNoir        =              "<:LG_Noir:788778408867266651>"
Emo_EnfSauv       =    "<:LG_Enfant_Sauvage:788778408943288330>"
Emo_LGBlanc       =             "<:LG_Blanc:788778409421307925>"
Emo_LGBleu        =              "<:LG_Bleu:788836124223078521>"
Emo_Traitre       =           "<:LG_Traitre:911402148011589702>"

Emo_RoleInconnu   =         "<:role_Inconnu:850890294312173568>"

Emo_trollface     =            "<:trollface:788793941973139486>"

Emo_Yellow        =      "<:among_us_yellow:788815750559170582>"
Emo_White         =       "<:among_us_white:789053593926893599>"
Emo_Red           =         "<:among_us_red:788809362864996354>"
Emo_Purple        =      "<:among_us_purple:788809612651921478>"
Emo_Pink          =        "<:among_us_pink:788811911961509948>"
Emo_Orange        =      "<:among_us_orange:788815750709641236>"
Emo_Lime          =        "<:among_us_lime:788811912045527040>"
Emo_Green         =       "<:among_us_green:788811911956398121>"
Emo_Cyan          =        "<:among_us_cyan:788811911562002483>"
Emo_Brown         =       "<:among_us_brown:788811911701069855>"
Emo_Blue          =        "<:among_us_blue:788811911890075668>"
Emo_Black         =       "<:among_us_black:788809567109775410>"

Emo_BabyYellow    = "<:among_us_baby_yellow:790291918763982879>"
Emo_BabyWhite     =  "<:among_us_baby_white:790291918525431828>"
Emo_BabyRed       =    "<:among_us_baby_red:790291918520844324>"
Emo_BabyPurple    = "<:among_us_baby_purple:790291918268661761>"
Emo_BabyPink      =   "<:among_us_baby_pink:790291918621638656>"
Emo_BabyOrange    = "<:among_us_baby_orange:790291918515863573>"
Emo_BabyLime      =   "<:among_us_baby_lime:790291918554136656>"
Emo_BabyGreen     =  "<:among_us_baby_green:790291918126972959>"
Emo_BabyCyan      =   "<:among_us_baby_cyan:790291918483095562>"
Emo_BabyBrown     =  "<:among_us_baby_brown:790291918110064650>"
Emo_BabyBlue      =   "<:among_us_baby_blue:790291918630027264>"
Emo_BabyBlack     =  "<:among_us_baby_black:790291917439107082>"

Emos_Babys        = [ Emo_BabyYellow, Emo_BabyWhite, Emo_BabyRed   ,
                      Emo_BabyPurple, Emo_BabyPink , Emo_BabyOrange,
                      Emo_BabyLime  , Emo_BabyGreen, Emo_BabyCyan  ,
                      Emo_BabyBrown , Emo_BabyBlue , Emo_BabyBlack  ]



# %% Fonctions

def verifServeur (message):
    try :
        if message.guild == serveurMegaLG :
            return True
        else :
            return False
    except :
        return False
    
    

def salon_avec(info, type_dinfo) :
    """
    Cette Fonction renvoie le salon correspondant à l'info donnée en argument.
    Si aucun salon ne correspond, elle renvoie None.
       
    Voici les types d'information pris en charge : 'topic'
    """
    
    
    if type_dinfo == "topic" :
        for salon in serveurMegaLG.channels :
            
            try : 
                if salon.topic == info :
                    return salon
                
            except :
                pass
    
    return None
    

    
# %%% Envoie / Modification / Suppression de Message

async def envoieMsg (user_channel, contenu_message) :
    """
    Ajoute le texteAAjouter au bout de message, en éditant ce dernier
    Si le nouveau message est trop long, un autre message est envoyé, contenant uniquement texteAAjouter
    
    Cette fonction renvoie le message qui vient soit d'être édité, soit d'être envoyé 
    """
    
    while len(contenu_message) >= 2000 :
        
        await user_channel.send( contenu_message[ : 2000] )
        contenu_message = contenu_message[2001 : ]
    
    
    await user_channel.send(contenu_message)





async def effacerMsg (ctx_channel, nbMessage = 1):
    """
    Efface les nbMessage derniers messages du channel ctx_channel
    """
       
    if   type(ctx_channel) in (discord.channel.TextChannel, discord.channel.DMChannel) :
        channelEnQ = ctx_channel
        
    elif type(ctx_channel) == commands.context.Context                                 :
        channelEnQ = ctx_channel.channel
        
    messagesAEff = await channelEnQ.history(limit = 10**9).flatten()
    
    i = 0
    
    for m in messagesAEff:
        if i < nbMessage :
            try    : await m.delete() ; i += 1 ;
            except : pass





async def ajoutMsg (message, texteAAjouter) :
    """
    Ajoute le texteAAjouter au bout de message, en éditant ce dernier
    Si le nouveau message est trop long, un autre message est envoyé, contenant uniquement texteAAjouter
    
    Cette fonction renvoie le message qui vient soit d'être édité, soit d'être envoyé 
    """
    
    if   len(message.content) + len(texteAAjouter) < 2000 :
        await message.edit(content = message.content + texteAAjouter)
    
    else :
        message = await message.channel.send(texteAAjouter)
        
    return message





def ajoutListe (liste, texteAAjouter) :
    """
    Ajoute le texteAAjouter au bout du dernier élément de liste, en y ajoutant ce dernier
    Si le dernier élément est trop long, un nouvel élément sera ajouté à liste, contenant uniquement texteAAjouter
       
    Cette fonction renvoie la liste modifié par la fonction
       
    La liste, une fois remplie par tout le message peut ensuite être envoyé par envoieListe()
    """

    
    if   len(liste[-1]) + len(texteAAjouter) < 2000 :
        liste[-1] += texteAAjouter
    
    else :
        liste.append(texteAAjouter)
        
    return liste



async def envoieListe(channel, liste) :
    """
    Envoie les élément de liste dans channel sous forme de messages individuels
    """    
    
    for msg in liste :
        await channel.send(msg)


# %%% Ban / Unban / Kick

async def ban_MLG_LG_FN(*members) :
    
    for m in members:
        await serveurMegaLG_LG.ban(m)
        await serveurMegaLG_FN.ban(m)


async def unban_MLG_LG_FN(*members) :
    
    for m in members:
        await serveurMegaLG_LG.unban(m)
        await serveurMegaLG_FN.unban(m)


async def ban_tousLesMembres_de(serveur_ban, serveur_devant_etre_ban) :
    """
    Cette fonction va ban tous les membres du serveur_devant_etre_ban.
    Les membres seront banis de serveur_ban
    """
    
    for membre in serveur_devant_etre_ban.members :
        try :
            await serveur_ban.ban(membre)
        except :
            pass
    
    
    
async def unban_tousLesMembres_de(serveur_unban, serveur_devant_etre_unban) :
    """
    Cette fonction va unban tous les membres du serveur_devant_etre_unban.
    Les membres seront unbanis de serveur_unban
    """
    
    for membre in serveur_devant_etre_unban.members :
        await serveur_unban.unban(membre)
    
    
async def ban_tousLesMembres_de_MLG_LG_FN() :
    
    await ban_tousLesMembres_de(serveurMegaLG_LG, serveurMegaLG)
    await ban_tousLesMembres_de(serveurMegaLG_FN, serveurMegaLG)
    
    
async def unban_tousLesMembres_de_MLG_LG_FN() :
    
    await unban_tousLesMembres_de(serveurMegaLG_LG, serveurMegaLG)
    await unban_tousLesMembres_de(serveurMegaLG_FN, serveurMegaLG)



# %%% Attente de réponses

# %%%% Attente de réaction

async def attente_Reaction(message_surLequelReagir, reacteur, emojisEtReturns, timeout = None, reponseParDefaut = None):
    """
    Ajoute des réaction sur le message_surLequelReagir et attend que le reacteur réagisse sur le message
    Reacteur peut être un Member ou un User
    
    emojisEtReturns est une liste de liste :
        Chaque éléments de emojisEtReturns est une liste contant :
            - un emoji (sous forme de str)
            - ce qui est envoyé par la fonction si le réacteur réagis avec l'emoji donnée précédement
    
    Renvoie le return correspondant à l'emoji dans emojisEtReturns
    Renvoie reponseParDefaut si le confirmateur ne répond pas à temps
    """
    
    listeEmoji  = []
    
    for element in emojisEtReturns :
        emj = element[0]
        
        listeEmoji.append(emj)
        await message_surLequelReagir.add_reaction(emj)
        

    def verifEmoji(reaction, user):
        return message_surLequelReagir.id == reaction.message.id  and  user.id == reacteur.id  and  str(reaction.emoji) in listeEmoji
    
    
    try :
        reaction, user = await bot.wait_for("reaction_add", check = verifEmoji, timeout = timeout)
        
    except :
        for emoji in listeEmoji :
            await message_surLequelReagir.remove_reaction(emoji, userMdJ)
            
        return reponseParDefaut
    
    
    
    for emoji in listeEmoji :
        await message_surLequelReagir.remove_reaction(emoji, userMdJ)
    
    return emojisEtReturns[listeEmoji.index(str(reaction.emoji))] [1]





async def attente_Confirmation(message_aConfirmer, confirmateur, timeout = None, reponseParDefaut = True):
    """
    Ajoute des réaction sur le message_aConfirmer et attend que le confirmateur confirme le message
    Confirmateur peut être un Member ou un User
    
    Renvoie True si le message est confirmé et False sinon
    Renvoie reponseParDefaut si le confirmateur ne répond pas à temps
    """
    
    Emo_validation  = "✅"
    Emo_infirmation = "❌"
    
    decision = await attente_Reaction( message_aConfirmer     , confirmateur                       , 
                                       [[Emo_validation, True], [Emo_infirmation, False]]          ,
                                       timeout = timeout      , reponseParDefaut = reponseParDefaut )
    
    return decision







# %%%% Attente de message

async def attente_Message(expediteur_msgAttendu, salon_msgAttendu = "DMChannel", timeout = None, accuseReception = False) :
    """
    Attend que expediteur_msgAttendu envoie un msg dans salon_msgAttendu
    
    expediteur_msgAttendu peut être un Member ou un User
    salon_msgAttendu est un objet discord.channel
    
    Renvoie le message si il a été reçu à temps
    Renvoie None sinon
    """

    Emo_accuseReception  = "✅"

    if salon_msgAttendu == "DMChannel" :
        def verifMsg (msg):
            return msg.author.id == expediteur_msgAttendu.id  and  type(msg.channel) == discord.channel.DMChannel
        
    else :
        def verifMsg (msg):
            return msg.author.id == expediteur_msgAttendu.id  and       msg.channel  == salon_msgAttendu
    
    
    try :
        msgRecu = await bot.wait_for('message', check = verifMsg, timeout = timeout )
        
        if accuseReception :
            await msgRecu.add_reaction(Emo_accuseReception)
            
        return msgRecu
    
    except :
        return None



# %% Commandes

# %%% Nettoyage

@bot.command(aliases = ["nettoyage", "Net", "net", "N", "n"])
async def Nettoyage (ctx, nbMessages = 10**9):
    """
    Efface tout les messages que le @Maître du Jeu vous a envoyé 
    Vous pouvez y ajouter un paramètre optionnel, le nombre de message

    !Nettoyage     ==> Efface tout les messages qu'il vous a envoyé
    !Nettoyage 3   ==> Efface les 3 derniers messages qu'il vous a envoyé 
    """
        
    if ctx.guild != None :
        
        await effacerMsg(ctx)
        
        if ctx.author.guild_permissions.manage_messages == True :
            await effacerMsg(ctx, nbMessages)
            
    else :
        await effacerMsg(ctx, nbMessages)