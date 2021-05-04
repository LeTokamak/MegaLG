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

# %% Constantes du serveurs

def def_cstsMegaLG ():
    """
    Redef de toutes les variables liés au serveur MégaLG
    """
    
    print("Redef des Constantes")
    
    def_userAdmins()
    def_serveurMegaLG()
    def_categoryChannelsMegaLG()
    def_channelsMegaLG()
    def_rolesMegaLG()





# %%% Bot et Serveur

#### Création de l'objet Bot

intentions = discord.Intents.all()
bot        = commands.Bot(command_prefix='!', description="Maître du Jeu", intents = intentions)

tokenMJ = "NzM3NzE3MTkxNTI0NDgzMTIy.XyBarA.A83hDJo-1XCRMatEUxAWIlcmaI0" # Maitre du Jeu


#### Serveur

serveurMegaLG = None

def def_serveurMegaLG ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir serveurMegaLG, une fois que le bot est connecté 
    """
    global serveurMegaLG
    
    serveurMegaLG = bot.get_guild (769495045308940288)





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





# %%% Category Channels

"""
 <CategoryChannel id=769495045308940289 name='Infos'                   position=0 nsfw=False>,
 <CategoryChannel id=818582430100750376 name='Gestion des Groupes'     position=1 nsfw=False>,
 <CategoryChannel id=769996371246710804 name='Place du Village'        position=2 nsfw=False>,
 <CategoryChannel id=770011182978957352 name='Forêt Nocturne'          position=3 nsfw=False>,
 <CategoryChannel id=790156426739056650 name="L'Au delà"               position=4 nsfw=False>,
 <CategoryChannel id=782626299146403861 name='Historique'              position=5 nsfw=False>,
 <CategoryChannel id=817842578581880863 name='Salon du Personnel'      position=6 nsfw=False>,
 <CategoryChannel id=817843165855219734 name='Ajouts'                  position=7 nsfw=False>,
 <CategoryChannel id=817797543324680254 name='Améliorations'           position=8 nsfw=False>,
 <CategoryChannel id=776186937219350569 name='Bureau des Programmeurs' position=9 nsfw=False>,
 <CategoryChannel id=786274888465252352 name='Bureau du Maître'        position=10 nsfw=False>,

 """

CategoryChannel_GestionGrp = None


def def_categoryChannelsMegaLG ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir les categoryChannels du serveur, une fois que le bot est connecté 
    """
    
    global CategoryChannel_GestionGrp
    
    CategoryChannel_GestionGrp = bot.get_channel        (818582430100750376)





# %%% Channels


# Autres Chanels (le 10/03/2021)

"""
 <TextChannel id=817798385821155339 name='⬢_6│anges-et-démons' position=32 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798571604705382 name='⬢_9│' position=35 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798264384389121 name='⬢_5│mode-obscure' position=31 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=778275316971864094 name='🚬┃salon-privé-avec-dè-gro-cigar-é-tou' position=43 nsfw=False news=False category_id=786274888465252352>,
 <TextChannel id=817798234247397386 name='⬢_4│génocide-de-tout-l-univers' position=30 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=796450089303932948 name='☕┃le-salon-du-personnel' position=22 nsfw=False news=False category_id=817842578581880863>,
 <TextChannel id=817803097199738910 name='👾┃proposition-de-roles' position=23 nsfw=False news=False category_id=817843165855219734>,
 <TextChannel id=817798768766091304 name='⬢_e│' position=40 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798546635096075 name='⬢_8│' position=34 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=778152934948470834 name='💎┃archive-du-programmeur' position=21 nsfw=False news=False category_id=782626299146403861>,
 <TextChannel id=783611815313408040 name='🥃┃boulot' position=44 nsfw=False news=False category_id=786274888465252352>,
 <TextChannel id=817816477464789052 name='💬┃phrases-de-mort' position=25 nsfw=False news=False category_id=817843165855219734>,
 <TextChannel id=817798672682975233 name='⬢_b│' position=37 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=788005245799497728 name='🐍┃programmes' position=26 nsfw=False news=False category_id=817843165855219734>,
 <TextChannel id=817804723490914305 name='🤖┃nouvelles-commandes' position=24 nsfw=False news=False category_id=817843165855219734>,
 <VoiceChannel id=790157873078337556 name='🥀┃discutions fantomatiques' position=3 bitrate=64000 user_limit=0 category_id=790156426739056650>,
 <VoiceChannel id=786275485029105704 name="∯┃Vocal privé (réservé à l'élite du serveur)" position=5 bitrate=64000 user_limit=0 category_id=786274888465252352>,
 <TextChannel id=817798696267284520 name='⬢_c│' position=38 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798134956032000 name='⬢_2│meurtre-des-afk' position=28 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798432054837308 name='⬢_7│modification-horaire' position=33 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798213779718224 name='⬢_3│compo-de-la-prochaine-partie' position=29 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817797845007466546 name='⬢_1│système-de-groupe' position=27 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=790157757557768222 name='🍂┃discutions-fantomatiques' position=18 nsfw=False news=False category_id=790156426739056650>,
 <TextChannel id=817798793416015893 name='⬢_f│' position=41 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=776187355497103360 name='🎨┃écrivains-dignes-de-rembrandt' position=42 nsfw=False news=False category_id=776186937219350569>,
 <TextChannel id=817798744044732416 name='⬢_d│' position=39 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=817798639208366141 name='⬢_a│le-canton' position=36 nsfw=False news=False category_id=817797543324680254>,
 <TextChannel id=787400715562909737 name='🕸┃le-vieux-salon-du-personnel-abandonné' position=45 nsfw=False news=False category_id=786274888465252352>,
 <VoiceChannel id=778290209489027112 name='☕┃le salon du personnel' position=4 bitrate=64000 user_limit=0 category_id=817842578581880863>
 """



channelAccueil       = None
channelGeneral       = None

channelRegles        = None
channelInfos         = None
channelRoles         = None
channelAmeliorations = None

channelFctmentGrp    = None
channelGalaxie       = None
channelEtoile        = None
channelPlanete       = None
channelLune          = None

channelRapport       = None
channelCimetiere     = None
channelBucher        = None
channelDebat         = None
vocalDebat           = None

channelVotesLG       = None
channelLoupsGarous   = None
vocalLoupsGarous     = None
channelFamilleNom    = None
vocalFamilleNom      = None

channelHistorique    = None
channelAttente       = None


def def_channelsMegaLG ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir tout les channels du serveur, une fois que le bot est connecté 
    """
    
    global channelAccueil, channelGeneral
    
    channelAccueil        = bot.get_channel        (769495045308940291)
    channelGeneral        = bot.get_channel        (790691318786949201)
    
    
    
#### Infos
    
    global channelInfos, channelRoles, channelRegles, channelAmeliorations
    
    channelRegles         = bot.get_channel        (810553761164558346)
    channelInfos          = bot.get_channel        (770001767634305115)
    channelRoles          = bot.get_channel        (770002724074291212)
    channelAmeliorations  = bot.get_channel        (810554730383671297)



#### Gestion des Groupes
    
    global channelFctmentGrp, channelGalaxie, channelEtoile, channelPlanete, channelLune
    
    channelFctmentGrp     = bot.get_channel        (820420551931068436)
    channelGalaxie        = bot.get_channel        (823477780142489661)
    channelEtoile         = bot.get_channel        (818580520765751296)
    channelPlanete        = bot.get_channel        (818580935380303903)
    channelLune           = bot.get_channel        (818581474856140841)



#### Place du Village

    global channelRapport, channelCimetiere, channelBucher,  channelDebat, vocalDebat
    
    channelRapport        = bot.get_channel        (780161660362293249)
    channelCimetiere      = bot.get_channel        (771492797886103552)
    channelBucher         = bot.get_channel        (769998111120293897)
    channelDebat          = bot.get_channel        (770000300349980722)
    vocalDebat            = bot.get_channel        (769495045308940292)



#### Forêt Nocturne

    global channelVotesLG, channelLoupsGarous, vocalLoupsGarous, channelFamilleNom, vocalFamilleNom


    channelVotesLG        = bot.get_channel        (784072098612117555)
    channelLoupsGarous    = bot.get_channel        (770013706523770880)
    vocalLoupsGarous      = bot.get_channel        (770014246129893386)
    channelFamilleNom     = bot.get_channel        (774762395318747168)
    vocalFamilleNom       = bot.get_channel        (774763711856508928)



#### Historique

    global channelHistorique, channelAttente

    channelHistorique     = bot.get_channel        (782626433255997480)
    channelAttente        = bot.get_channel        (789105310408900619)






# %%% Roles du Serveur

roleEveryone    = None
roleMaitre      = None
roleBot         = None

roleMdJ         = None
roleAssistant   = None

roleArtisans    = None
roleSpectateurs = None

roleJoueurs     = None
roleMorts       = None



def def_rolesMegaLG ():
    """
    Cette Fonction ne renvoie rien
       
    Elle doit être appelé lors du on_ready() pour définir tout les rôles du serveur, une fois que le bot est connecté 
    """
    
    global roleEveryone, roleMaitre, roleBot
    
    roleEveryone          = serveurMegaLG.get_role (769495045308940288)
    roleMaitre            = serveurMegaLG.get_role (782627464530755604)  
    roleBot               = serveurMegaLG.get_role (783283411833978901)
    
    
    global roleMdJ, roleAssistant
    
    roleMdJ               = serveurMegaLG.get_role (769496917797109771)
    roleAssistant         = serveurMegaLG.get_role (783281237481619467)
    
    
    global roleArtisans, roleSpectateurs, roleJoueurs, roleMorts
    
    roleArtisans          = serveurMegaLG.get_role (769985455470018620)
    roleSpectateurs       = serveurMegaLG.get_role (795550455224205312)
    
    roleJoueurs           = serveurMegaLG.get_role (782625030123159562)
    roleMorts             = serveurMegaLG.get_role (790158481634099250)











# %%% Emojis du Serveur

Emo_Maire       = ":military_medal:"

Emo_Villageois  = "<:Villageois:788784861682204682>"
Emo_Voyante     = "<:V_Voyante:788784786164285482>"
Emo_Salvateur   = "<:V_Salvateur:788778406337576981>"
Emo_Sorciere    = "<:V_Sorciere:788784785941332000>"
Emo_PttFille    = "<:V_Petite_Fille:788784786280808458>"
Emo_Hirondelle  = "<:V_Hirondelle:788833861253595176>"
Emo_FNSoeur     = "<:V_FN_Soeur:788778409253011507>"
Emo_FNFrere     = "<:V_FN_Frere:788778408997683281>"
Emo_Cupidon     = "<:V_Cupidon:788784786155634719>"
Emo_Corbeau     = "<:V_Corbeau:788778409203073054>"
Emo_Chasseur    = "<:V_Chassseur:788784786332319774>"
Emo_Ancien      = "<:V_Ancien:788778406476251146>"

Emo_LoupGarou   = "<:Loup_Garou:788778408477327401>"
Emo_LGNoir      = "<:LG_Noir:788778408867266651>"
Emo_EnfSauv     = "<:LG_Enfant_Sauvage:788778408943288330>"
Emo_LGBlanc     = "<:LG_Blanc:788778409421307925>"
Emo_LGBleu      = "<:LG_Bleu:788836124223078521>"

Emo_trollface   = "<:trollface:788793941973139486>"

Emo_Yellow      = "<:among_us_yellow:788815750559170582>"
Emo_White       = "<:among_us_white:789053593926893599>"
Emo_Red         = "<:among_us_red:788809362864996354>"
Emo_Purple      = "<:among_us_purple:788809612651921478>"
Emo_Pink        = "<:among_us_pink:788811911961509948>"
Emo_Orange      = "<:among_us_orange:788815750709641236>"
Emo_Lime        = "<:among_us_lime:788811912045527040>"
Emo_Green       = "<:among_us_green:788811911956398121>"
Emo_Cyan        = "<:among_us_cyan:788811911562002483>"
Emo_Brown       = "<:among_us_brown:788811911701069855>"
Emo_Blue        = "<:among_us_blue:788811911890075668>"
Emo_Black       = "<:among_us_black:788809567109775410>"

Emo_BabyYellow  = "<:among_us_baby_yellow:790291918763982879>"
Emo_BabyWhite   = "<:among_us_baby_white:790291918525431828>"
Emo_BabyRed     = "<:among_us_baby_red:790291918520844324>"
Emo_BabyPurple  = "<:among_us_baby_purple:790291918268661761>"
Emo_BabyPink    = "<:among_us_baby_pink:790291918621638656>"
Emo_BabyOrange  = "<:among_us_baby_orange:790291918515863573>"
Emo_BabyLime    = "<:among_us_baby_lime:790291918554136656>"
Emo_BabyGreen   = "<:among_us_baby_green:790291918126972959>"
Emo_BabyCyan    = "<:among_us_baby_cyan:790291918483095562>"
Emo_BabyBrown   = "<:among_us_baby_brown:790291918110064650>"
Emo_BabyBlue    = "<:among_us_baby_blue:790291918630027264>"
Emo_BabyBlack   = "<:among_us_baby_black:790291917439107082>"

Emos_Babys      = [Emo_BabyYellow, Emo_BabyWhite, Emo_BabyRed   ,
                   Emo_BabyPurple, Emo_BabyPink , Emo_BabyOrange,
                   Emo_BabyLime  , Emo_BabyGreen, Emo_BabyCyan  ,
                   Emo_BabyBrown , Emo_BabyBlue , Emo_BabyBlack ]



# %% Fonctions

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
    reactionMdJ = []
    
    for element in emojisEtReturns :
        emj = element[0]
        
        listeEmoji.append(emj)
        await message_surLequelReagir.add_reaction(emj)
        

    def verifEmoji(reaction, user):
        return message_surLequelReagir.id == reaction.message.id  and  user.id == reacteur.id  and  str(reaction.emoji) in listeEmoji
    
    
    try :
        reaction, user = await bot.wait_for("reaction_add", check = verifEmoji, timeout = timeout)
        
    except :
        for r in reactionMdJ :
            await r.clear()
            
        return reponseParDefaut
    
    
    
    for r in reactionMdJ :
        await r.clear()
    
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
    
    return await attente_Reaction( message_aConfirmer     , confirmateur                     , 
                                   [[Emo_validation, True], [Emo_infirmation, False]]        ,
                                   timeout = timeout      , reponseParDefaut=reponseParDefaut )







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
