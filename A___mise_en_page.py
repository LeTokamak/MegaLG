# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---                      Niveau A - Fonctions de Mise en Page                      ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""



import random as rd



# %%% Mise en forme de nombres

def AjoutZerosAvant(x, nbChiffre, espace = False):
    """Ajoute des zeros devant un Réel x jusqu'à atteindre nbChiffre chiffres
       AjoutZerosAvant(17   , 5) = '00017' 
       AjoutZerosAvant(99.36, 5) = '00099.36' """

    nbZeros = nbChiffre - len(str(int(x)))
    
    if espace : zero = " "
    else      : zero = "0"
    
    return nbZeros*zero + str(x)





# %%% Mise en forme de texte 

def de_dApostrophe (mot, debutDePhrase = False):
    """
    Renvoie le mot avec un de devant,
    si ce mot commence commence par une voyelle ou un 'h' (sauf exception (les 'h' aspirés)), la fonction renvoie d'mot 
       
       de_dApostrophe("pin")           ==> "de pin"
       de_dApostrophe("alain")         ==> "d'alain" 
       de_dApostrophe("haricot", True) ==> "De haricot"
    """
       
    mots_avec_h_aspiré = ("haie"     , "hache" , "hachisch", "haine"  , "haïtien"  , "haleter"  , "hall"   , "halle"     , "halte"     , "hamac"   , 
                          "hamburger", "hameau", "hamster" , "hanche" , "hand-ball", "handicapé", "hangar" , "hanneton"  , "hara-kiri" , "harceler", 
                          "hard"     , "harem" , "hareng"  , "haricot", "harpe"    , "harpon"   , "hasard" , "haschisch" , "hâte"      , "haut"    , 
                          "hauteur"  , "havane", "hérisson", "héron"  , "héros"    , "heurter"  , "hibou"  , "hic"       , "hiérarchie", "hip-hop" , 
                          "hippy"    , "hit"   , "hobby"   , "hocher" , "hockey"   , "holding"  , "hold-up", "hollandais", "hollywood" , "homard"  ,
                          "honte"    , "hoquet", "hors"    , "hot dog", "hooligan" , "houx"     , "hublot" , "huche"     , "hurler"    , "hussarde",
                          "hutte")
    
    if debutDePhrase : dApost, de = "D'", "De "
    else             : dApost, de = "d'", "de "
    
    if mot[0].lower() in "aàâ" + "eéèêë" + "iïî" + "oôö" + "uûùü" + "h"  and  mot.lower() not in mots_avec_h_aspiré :
        return dApost + mot
    
    else :
        return de + mot



def MeF_Prenom (texte) :
    """
    Cette fonction Met en Forme la variable texte (str) pour les transformer en Prénom
        "   JeAn-cléMENt frANçoiS       "  ==>  "Jean-Clément François"
    """
    
    # 1er split pour les espaces "___cléMENt__" et gestion des Majuscules
    
    listePrenoms = texte.split()
    listePrenoms_MeF = []
    
    for p in listePrenoms :
        listePrenoms_MeF.append( p[0].upper() + p[1:].lower() )
        
    prenom_Maj = " ".join( listePrenoms_MeF )
    
    
    
    # 2nd split pour la gestion des Majuscules après les "-" (prénoms composées)
    
    listePrenoms = prenom_Maj.split("-")
    listePrenoms_MeF = []
    
    for p in listePrenoms :
        if p != "" : listePrenoms_MeF.append( p[0].upper() + p[1:] )
    
    return "-".join( listePrenoms_MeF )





def MeF_Pseudo (texte) :
    
    pseudo = " ".join( texte.split() )
    
    return pseudo[0].upper() + pseudo[1:]



# %%% Mise en forme de dates

def mois (nb):
    if   nb ==  1 : return "Janvier"
    elif nb ==  2 : return "Février"
    elif nb ==  3 : return "Mars"
    elif nb ==  4 : return "Avril"
    elif nb ==  5 : return "Mai"
    elif nb ==  6 : return "Juin"
    elif nb ==  7 : return "Juillet"
    elif nb ==  8 : return "Août"
    elif nb ==  9 : return "Septembre"
    elif nb == 10 : return "Octobre"
    elif nb == 11 : return "Novembre"
    elif nb == 12 : return "Décembre"
    
    
def JSemaine (nb):
    if   nb ==  0 : return "Lundi"
    elif nb ==  1 : return "Mardi"
    elif nb ==  2 : return "Mercredi"
    elif nb ==  3 : return "Jeudi"
    elif nb ==  4 : return "Vendredi"
    elif nb ==  5 : return "Samedi"
    elif nb ==  6 : return "Dimanche"


def strDate(date, Mardi_20_Avril_2021 = True, Mardi_20_Avril = False, Mar_20_Avr = False):
    """
    ATTENTION : "Juin"[:3] == "Juillet"[:3]
    """   
    if   Mardi_20_Avril_2021 :
        return f"{JSemaine(date.weekday())} {date.day} {mois(date.month)} {date.year}"
    
    elif Mardi_20_Avril      :
        return f"{JSemaine(date.weekday())} {date.day} {mois(date.month)}"
    
    elif Mar_20_Avr         :
        return f"{JSemaine(date.weekday())[:3]} {date.day} {mois(date.month)[:3]}"



# %%% Gestion de Couleurs


def RGB_intHexa(R,G,B):
    return R*16**4 + G*16**2 + B



def couleurRandom(typeEmbed):
    if typeEmbed == "a" :
        #Nuances de Rouge - Orange - Jaune
        R = rd.choice(range(180,256))
        G = rd.choice(range(0,R+1))
        B = rd.choice(range(0,min(R,G,100)))
        
    if typeEmbed == "t" :
        #Nuances de Gris
        R = G = B = rd.choice(range(60,220))
        
    if typeEmbed == "matin" :
        #Nuances de Rouge - Orange - Jaune
        R = rd.choice(range(180,256))
        G = rd.choice(range(0,R+1))
        B = rd.choice(range(0,min(R,G,100)))
        
    if typeEmbed == "soir" :
        #Nuances de Rouge - Orange - Jaune
        R = rd.choice(range(180,256))
        G = rd.choice(range(0,R+1))
        B = rd.choice(range(0,min(R,G,100)))  
        
    if typeEmbed == "amour" :
        # Nuances de rose
        R = rd.choice(range(150,256))
        G = rd.choice(range(0,50))
        B = rd.choice(range(200,256))

    return RGB_intHexa(R, G, B)