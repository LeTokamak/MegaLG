# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---         Niveau B - Fonctions et Constantes liées aux Rôles des Joueurs         ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

# Niveau A
import A_fct_Discord          as fDis
import A_fct_MiseEnPage       as fMeP
import A_variables            as v


Embed = fDis.discord.Embed





# %% Création des dictionnaires des différents rôles

role_Villageois, role_Cupidon   , role_Ancien     = {}, {}, {}
role_Salvateur , role_Sorciere  , role_Voyante    = {}, {}, {}
role_Chasseur  , role_Corbeau   , role_Hirondelle = {}, {}, {}
role_FamilleNb                                    = {}
role_LG        , role_LGNoir    , role_LGBleu     = {}, {}, {}
role_LGBlanc   , role_EnfantSauv                  = {}, {}


TousLesRoles = [ role_Villageois, role_Cupidon   , role_Ancien    ,
                 role_Salvateur , role_Sorciere  , role_Voyante   ,
                 role_Chasseur  , role_Corbeau   , role_Hirondelle,
                 role_FamilleNb ,
                 role_LG        , role_LGNoir    , role_LGBleu    ,
                 role_LGBlanc   , role_EnfantSauv                  ]



# %%% Noms des rôles

clefNom = "nom"

role_Villageois[clefNom] = "Villageois"
role_Cupidon   [clefNom] = "Cupidon"
role_Ancien    [clefNom] = "Ancien"

role_Salvateur [clefNom] = "Salvateur"
role_Sorciere  [clefNom] = "Sorcière"
role_Voyante   [clefNom] = "Voyante"

role_Chasseur  [clefNom] = "Chasseur"
role_Corbeau   [clefNom] = "Corbeau"
role_Hirondelle[clefNom] = "Hirondelle"
      
role_FamilleNb [clefNom] = "Membre de la Famille Nombreuse"

role_LG        [clefNom] = "Loup-Garou"
role_LGNoir    [clefNom] = "Loup-Garou Noir"
role_LGBleu    [clefNom] = "Loup-Garou Bleu"

role_LGBlanc   [clefNom] = "Loup-Garou Blanc"
role_EnfantSauv[clefNom] = "Enfant Sauvage"



# %%% Nombre de chaque rôle

clefNb = "nombre"

role_Villageois[clefNb] = v.nb_Villag
role_Cupidon   [clefNb] = v.nb_Cupido
role_Ancien    [clefNb] = v.nb_Ancien

role_Salvateur [clefNb] = v.nb_Salvat
role_Sorciere  [clefNb] = v.nb_Sorcie
role_Voyante   [clefNb] = v.nb_Voyant

role_Chasseur  [clefNb] = v.nb_Chasse
role_Corbeau   [clefNb] = v.nb_Corbea
role_Hirondelle[clefNb] = v.nb_Hirond
      
role_FamilleNb [clefNb] = v.nb_Famill

role_LG        [clefNb] = v.nb_LG
role_LGNoir    [clefNb] = v.nb_LGNoir
role_LGBleu    [clefNb] = v.nb_LGBleu

role_LGBlanc   [clefNb] = v.nb_LGBlan
role_EnfantSauv[clefNb] = v.nb_EnSauv



# %%% Couleurs des embeds de chaque rôle

clefCouleur = "couleur"

role_Villageois[clefCouleur] = 0xFFC400
role_Cupidon   [clefCouleur] = 0xFF00AB
role_Ancien    [clefCouleur] = 0xB0B0B0

role_Salvateur [clefCouleur] = 0x00C134
role_Sorciere  [clefCouleur] = 0xAB00FF
role_Voyante   [clefCouleur] = 0x00FFE6

role_Chasseur  [clefCouleur] = 0xA27044
role_Corbeau   [clefCouleur] = 0xC79900
role_Hirondelle[clefCouleur] = 0x00B3C7
      
role_FamilleNb [clefCouleur] = 0x44FF00

role_LG        [clefCouleur] = 0xFF0000
role_LGNoir    [clefCouleur] = 0x9F0000
role_LGBleu    [clefCouleur] = 0xF9F9F9

role_LGBlanc   [clefCouleur] = 0x0C80F5
role_EnfantSauv[clefCouleur] = 0xE6777B



# %%% Emojis correspondant à chaque rôle

clefEmoji = "emoji"

role_Villageois[clefEmoji] = fDis.Emo_Villageois
role_Cupidon   [clefEmoji] = fDis.Emo_Cupidon
role_Ancien    [clefEmoji] = fDis.Emo_Ancien

role_Salvateur [clefEmoji] = fDis.Emo_Salvateur
role_Sorciere  [clefEmoji] = fDis.Emo_Sorciere
role_Voyante   [clefEmoji] = fDis.Emo_Voyante

role_Chasseur  [clefEmoji] = fDis.Emo_Chasseur
role_Corbeau   [clefEmoji] = fDis.Emo_Corbeau
role_Hirondelle[clefEmoji] = fDis.Emo_Hirondelle
      
role_FamilleNb [clefEmoji] =(fDis.Emo_FNFrere, fDis.Emo_FNSoeur)

role_LG        [clefEmoji] = fDis.Emo_LoupGarou
role_LGNoir    [clefEmoji] = fDis.Emo_LGNoir
role_LGBleu    [clefEmoji] = fDis.Emo_LGBleu

role_LGBlanc   [clefEmoji] = fDis.Emo_LGBlanc
role_EnfantSauv[clefEmoji] = fDis.Emo_EnfSauv


    
# %%% URL des Images de chaque rôle

clefImage = "urlImage"

role_Villageois[clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte1.png"
role_Cupidon   [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte7.png"
role_Ancien    [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte8.png"

role_Salvateur [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte4.png"
role_Sorciere  [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte5.png"
role_Voyante   [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte3.png"

role_Chasseur  [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte6.png"
role_Corbeau   [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte17.png"
role_Hirondelle[clefImage] = "https://media.discordapp.net/attachments/677824808221933585/715106297825067088/image0.png?width=677&height=677"
      
role_FamilleNb [clefImage] =("https://www.loups-garous-en-ligne.com/jeu/assets/images/carte26.png", "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte22.png")

role_LG        [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png"
role_LGNoir    [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte21.png"
role_LGBleu    [clefImage] = "https://cdn.discordapp.com/attachments/778152934948470834/788836782279884800/le-loup-garou-bleu.png"

role_LGBlanc   [clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte9.png"
role_EnfantSauv[clefImage] = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte16.png"
    

    
# %%% Descriptions des embeds de chaque rôle


# =============================================================================
# Gestions des "s" dus aux paramètres des Rôles
# =============================================================================

#   Ancien

if   v.Ancien_nbProtec >= 2                      : s_Ancien = "s"
else                                             : s_Ancien = ""


#   Sorcière

if   v.Sorcie_nbPotVie + v.Sorcie_nbPotMort >= 2 : s_So_Potion = "s"
else                                             : s_So_Potion  = ""

if   v.Sorcie_nbPotVie  == 0                     : So_potsVie =  ""
elif v.Sorcie_nbPotVie  == 1                     : So_potsVie =  "\n - **1** potion de vie, qui peut sauver une victime des loups."
elif v.Sorcie_nbPotVie  >= 2                     : So_potsVie = f"\n - **{v.Sorcie_nbPotVie}** potions de vie, qui peuvent sauver la victime des loups."

if   v.Sorcie_nbPotMort == 0                     : So_potsMort =  ""
elif v.Sorcie_nbPotMort == 1                     : So_potsMort =  "\n - **1** potion de mort, pour se débarrasser d'un gêneur."
elif v.Sorcie_nbPotMort >= 2                     : So_potsMort = f"\n - **{v.Sorcie_nbPotMort}** potions de mort, pour se débarrasser des gêneurs."



# =============================================================================
# Ecriture des descriptions
# =============================================================================

clefDescription = "description"

role_Villageois[clefDescription] =  "Il ne dispose d'aucun pouvoir particulier : uniquement sa perspicacité et sa force de persuasion !"
role_Cupidon   [clefDescription] =  "Au début de la partie, il forme un couple de deux joueurs. Leur objectif sera de survivre ensemble, si l'un d'eux meurt, l'autre sera emporté par le chagrin..."
role_Ancien    [clefDescription] = f"Grâce à l'expérience acquise lors de la première apparition de Loups-Garous dans la région (il y a bien longtemps...), il peut résister à **{v.Ancien_nbProtec}** attaque{s_Ancien} lors de la nuit."

role_Salvateur [clefDescription] =  "Cet homme courageux et téméraire peut lors de la nuit, protéger quelqu'un de toutes les attaques nocturnes !"
role_Sorciere  [clefDescription] = f"Cette experte des sciences occultes a aussi quelques compétences en cuisine... Elle a confectionné **{v.Sorcie_nbPotVie + v.Sorcie_nbPotMort}** potion{s_So_Potion} :{So_potsVie}{So_potsMort}"
role_Voyante   [clefDescription] =  "Après avoir abandonné l'astrologie, suite à une conjonction Vénus-Saturne rendant cette discipline caduque, elle acquit sa première boule de cristal.\nAvec elles, elle peut chaque nuit, découvrir la véritable identité d'un des habitants."

role_Chasseur  [clefDescription] =  "A sa mort, il peut éliminer un joueur en utilisant la dernière balle de son fusil..."
role_Corbeau   [clefDescription] =  "Chaque nuit, il désigne un joueur qui aura d'office 2 voix contre lui lors du vote du lendemain."
role_Hirondelle[clefDescription] =  "Chaque nuit, elle choisit un joueur, sa voix comptera 3 fois plus lors du vote du village."

role_FamilleNb [clefDescription] =  "Les membres de la famille nombreuse se connaissent tous et passent toutes leurs soirées ensemble, ils sont unis et rien ne les divisera ! (sauf peut-être les loups...)"

role_LG        [clefDescription] =  "La pilosité exceptionnelle de cette bête lui permet de prendre part au débat nocturne, avec ses compères Loups-Garous, pour décider d'une victime à dévorer..."
role_LGNoir    [clefDescription] = f"Il peut transformer la victime des loups en loup-garou, et il le peut **{v.LGNoir_nbInfect}** fois !\nUne infection qui peut se révéler cruciale, car l'infecté garde ses pouvoirs d'innocent !"
role_LGBleu    [clefDescription] =  "C'est un loup-garou tout à fait classique, mais grâce à son pelage bleuté il peut se faire passer pour plus innocent qu'il ne l'est, aux yeux d'une voyante."

role_LGBlanc   [clefDescription] =  "Son objectif est de finir la partie seul.\nLes autres loups croient qu'il est des leurs, mais il n'en est rien...\nChaque mercredi, il peut dévorer n'importe quel habitant, qui soit poilu ou non !"
role_EnfantSauv[clefDescription] =  "Ce petit bonhomme abandonné a choisi, lors de son arrivée dans le village, un modèle qui le guide et qui lui permet de ne pas trop perdre les pédales...\nSi ce dernier meurt, il retomberait dans la bestialité avec laquelle il a grandi, et il deviendrait Loup-Garou."



# %%% Détails techniques de chaque rôle (précisés sur les embeds)

clefDetails = "details"

role_Villageois[clefDetails] =  None
role_Cupidon   [clefDetails] =  "*Il est appelé lors de la première nuit, pour choisir son couple.*"
role_Ancien    [clefDetails] =  "*S'il est attaqué pendant la nuit et si personne ne le protège, alors il perdra une résistance nocturne et il sera informé de cette attaque le lendemain matin.*"

role_Salvateur [clefDetails] =  "*Les salvateurs sont appelés individuellement pendant la nuit.\nUn salvateur peut protéger plusieurs nuits de suite la même personne, il ne peut pas se protéger lui-même.*"
role_Sorciere  [clefDetails] =  "*Les sorcières sont appelées individuellement **après** le conseil des Loups-Garous.\nSi plusieurs sorcières font le même choix, seulement une de ces sorcières (choisie aléatoirement) perdra sa potion.*"
role_Voyante   [clefDetails] =  "*Les voyantes sont appelées individuellement pendant la nuit.*"

role_Chasseur  [clefDetails] =  "*Si lors de sa mort, il ne désigne personne, sa balle se logera dans une personne choisie au hasard...*"
role_Corbeau   [clefDetails] =  "*Les corbeaux sont appelés individuellement pendant la nuit.\nSi x corbeaux choisissent la même personne, cette personne aura 2x voix contre lui d'office !\nLes choix des corbeaux sont rendus publics le lendemain matin.*"
role_Hirondelle[clefDetails] =  "*Les hirondelles sont appelées individuellement pendant la nuit.\nSi x hirondelles choisissent la même personne, cette personne aura un pouvoir énorme, c'est-à-dire 2x+1 voix !\nLes choix des hirondelles sont rendus publics le lendemain matin.*"

role_FamilleNb [clefDetails] =  "*Pendant toute la nuit, deux salons (un textuel et un vocal) leur sont ouverts.\nIls peuvent y faire ce qu'ils veulent, il n'y a aucune modération !*"

role_LG        [clefDetails] =  "*Le système de vote du conseil des loups-garous est le même que celui du village, les résultats du vote sont envoyés après chaque vote.\nEn cas d'égalité ou si personne n'a voté, personne ne sera dévoré.*"
role_LGNoir    [clefDetails] =  "*Seul l'infecté sera averti du choix du Loup-Garou Noir, le village ne le saura pas (contrairement à Wolfy).*"
role_LGBleu    [clefDetails] =  "*Si la Voyante tente de le démasquer, elle verra un rôle choisi au hasard parmi les rôles étant du côté du village.*"

role_LGBlanc   [clefDetails] =  "*Le joueur choisi (qui peut être un villageois ou un loup-garou), ne peut pas être sauvé par les Sorcières...\nSeuls les Salvateurs peuvent le protéger.*"
role_EnfantSauv[clefDetails] =  "*Il est appelé lors de la première nuit, pour choisir son modèle.*"



# %%% Camp du rôle

campVillage = "Village"
campLG      = "Loups-Garous"
campSolo    = "Solitaire"
campVilLG   = "Village puis Loups-Garous"

clefCamp = "camp"

role_Villageois[clefCamp] = campVillage
role_Cupidon   [clefCamp] = campVillage
role_Ancien    [clefCamp] = campVillage

role_Salvateur [clefCamp] = campVillage
role_Sorciere  [clefCamp] = campVillage
role_Voyante   [clefCamp] = campVillage

role_Chasseur  [clefCamp] = campVillage
role_Corbeau   [clefCamp] = campVillage
role_Hirondelle[clefCamp] = campVillage
      
role_FamilleNb [clefCamp] = campVillage

role_LG        [clefCamp] = campLG
role_LGNoir    [clefCamp] = campLG
role_LGBleu    [clefCamp] = campLG

role_LGBlanc   [clefCamp] = campSolo
role_EnfantSauv[clefCamp] = campVilLG



# %%% Embeds des différents rôles

clefEmbed  = "embed"

motCamp    = "Camp"


# =============================================================================
# Création de l'embeds de la Famille Nombreuse
# =============================================================================

Ebd_Famill =         Embed( title = "**Famille Nombreuse**"         , description = role_FamilleNb[clefDescription]   , color = role_FamilleNb[clefCouleur] )
Ebd_Famill . set_thumbnail(   url = role_FamilleNb[clefImage][0]                                                                                            )
Ebd_Famill .     add_field(  name = motCamp                         ,       value = role_FamilleNb[clefCamp]          , inline = True                       )
Ebd_Famill .     add_field(  name = "Taille de la Famille Nombreuse",       value = role_FamilleNb[clefNb]            , inline = True                       )
Ebd_Famill .     add_field(  name = "__Détails Techniques du Rôle__",       value = role_FamilleNb[clefDetails]       , inline = False                      )    


role_FamilleNb [clefEmbed] = Ebd_Famill


# =============================================================================
# Création des embeds des Autres Roles 
# =============================================================================

AutresRoles = [role_Villageois, role_Cupidon    , role_Ancien    ,
               role_Salvateur , role_Sorciere   , role_Voyante   ,
               role_Chasseur  , role_Corbeau    , role_Hirondelle,
               role_LG        , role_LGNoir     , role_LGBleu    ,
               role_LGBlanc   , role_EnfantSauv                   ]

for role in AutresRoles :
    
    Ebd_Role =         Embed( title = f"**{role[clefNom]}**"                        , description = role[clefDescription],  color = role[clefCouleur] )
    Ebd_Role . set_thumbnail(   url = role[clefImage]                                                                                                 )
    Ebd_Role .     add_field(  name = motCamp                                       ,       value = role[clefCamp]       , inline = True              )
    Ebd_Role .     add_field(  name = f"Nombre {fMeP.de_dApostrophe(role[clefNom])}",       value = role[clefNb]         , inline = True              )
    
    if role[clefDetails] != None :
        Ebd_Role . add_field(  name = "__Détails Techniques du Rôle__"              ,       value = role[clefDetails]    , inline = False             )
        
    role[clefEmbed] = Ebd_Role



# %%% Fonctions Nocturnes des rôles

clefFctsNoct = "fonction nocturne"

# Elles sont definit dans D_fct_Village







# %% Fonctions liées aux rôles

# =============================================================================
# Paquet de tous les Roles
# =============================================================================

paquetRoles_Initial = []

for role in TousLesRoles :
    paquetRoles_Initial += role[clefNb] * [ role[clefNom] ]





def role_avec (info, type_dinfo):
    """Renvoie le dictionnaire du role correspondant à info
    
       Voici les types d'information pris en charge : 'nom'"""
    
### Recherche d'un nom de Role

    if type_dinfo == "nom" :
        
        for role in TousLesRoles :
            if role[clefNom] == info :
                return role
            
    return None





def emojiRole (info, estUnHomme):
    """Renvoie l'emoji correspondant à info (en prenant en compte le sexe)
    
       Info peut être un dictionnaire (cad le role recherché) ou un str (cad le nom du role recherché)"""
    
    if   type(info) == dict :
        emoji = info[clefEmoji]
    
    elif type(info) == str  :
        emoji = role_avec(info, "nom")[clefEmoji]
    
    
    if type(emoji) != tuple :
        return emoji
    
    elif estUnHomme :
        return emoji[0]
    
    else :
        return emoji[1]
    
    
    
def imageRole (info, estUnHomme):
    """Renvoie l'url correspondant à info (en prenant en compte le sexe)
    
       Info peut être un dictionnaire (cad le role recherché) ou un str (cad le nom du role recherché)"""
    
    if   type(info) == dict :
        urlImage = info[clefImage]
    
    elif type(info) == str  :
        urlImage = role_avec(info, "nom")[clefImage]
            
    
    if type(urlImage) != tuple :
        return urlImage
    
    elif estUnHomme :
        return urlImage[0]
    
    else :
        return urlImage[1]




   
async def envoie_EmbedsRoles ():
    """Fonction renvoyant tous les embeds de TousLesRoles"""

    separation = "_ _\n_ _\n_ _"

    await fDis.channelRoles.send("```Camp du Village```")
    
    if role_Villageois[clefNb] != 0 : await fDis.channelRoles.send( embed = role_Villageois[clefEmbed] )
    if role_Cupidon   [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Cupidon   [clefEmbed] )
    if role_Ancien    [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Ancien    [clefEmbed] )
    
    if role_Villageois[clefNb] + role_Cupidon   [clefNb] + role_Ancien    [clefNb] != 0 : await fDis.channelRoles.send( separation )
    
    
    if role_Salvateur [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Salvateur [clefEmbed] )
    if role_Sorciere  [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Sorciere  [clefEmbed] )
    if role_Voyante   [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Voyante   [clefEmbed] )
    
    if role_Salvateur [clefNb] + role_Sorciere  [clefNb] + role_Voyante   [clefNb] != 0 : await fDis.channelRoles.send( separation )
    
    
    if role_Chasseur  [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Chasseur  [clefEmbed] )
    if role_Corbeau   [clefNb] != 0 : await fDis.channelRoles.send( embed = role_Corbeau   [clefEmbed] )
    if role_Hirondelle[clefNb] != 0 : await fDis.channelRoles.send( embed = role_Hirondelle[clefEmbed] )
    
    if role_Chasseur  [clefNb] + role_Corbeau   [clefNb] + role_Hirondelle[clefNb] != 0 : await fDis.channelRoles.send( separation )
    
    
    if role_FamilleNb [clefNb] != 0 :
        await fDis.channelRoles.send( embed = role_FamilleNb[clefEmbed] )
        await fDis.channelRoles.send( separation )
    
    
    
    await fDis.channelRoles.send("```Camp des Loups-Garous```")
    
    if role_LG        [clefNb] != 0 : await fDis.channelRoles.send( embed = role_LG        [clefEmbed] )
    if role_LGNoir    [clefNb] != 0 : await fDis.channelRoles.send( embed = role_LGNoir    [clefEmbed] )
    if role_LGBleu    [clefNb] != 0 : await fDis.channelRoles.send( embed = role_LGBleu    [clefEmbed] )
    
    if role_LG        [clefNb] + role_LGNoir    [clefNb] + role_LGBleu    [clefNb] != 0 : await fDis.channelRoles.send( separation )
    
    
    if role_LGBlanc   [clefNb] != 0 : await fDis.channelRoles.send( embed = role_LGBlanc   [clefEmbed] )
    if role_EnfantSauv[clefNb] != 0 : await fDis.channelRoles.send( embed = role_EnfantSauv[clefEmbed] )