# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---            Niveau A - Variables et constantes de Partie et de Temps            ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""



from   datetime import datetime, timedelta
from   dateutil import tz

import asyncio

separation  = "_ _\n_ _\n_ _"




nbDigit_Matricule = 3

# %% Compo de la Prochaine Partie 

#### Nombre des rôles (pour une partie à 30)

tailleVlg_Ideal = 12

prop_Villag        = 0
prop_VillaVilla    = 1
prop_Cupido        = 1
prop_Ancien        = 0

prop_Salvat        = 2
prop_Sorcie        = 2
prop_Voyant        = 2
prop_Voyante_dAura = 0

prop_Corbea        = 1
prop_Hirond        = 1
prop_Juge          = 0

prop_Chasse        = 0
      
prop_Famill        = 0

prop_LG            = 1
prop_LGNoir        = 1
prop_LGBleu        = 0
prop_Traitre       = 0

prop_LGBlan        = 0
prop_EnSauv        = 0


somme_roles   = prop_Villag + prop_VillaVilla + prop_Cupido + prop_Ancien
somme_roles  += prop_Salvat + prop_Sorcie     + prop_Voyant + prop_Voyante_dAura
somme_roles  += prop_Corbea + prop_Hirond     + prop_Juge
somme_roles  += prop_Chasse + prop_Famill
somme_roles  += prop_LG     + prop_LGNoir     + prop_LGBleu + prop_Traitre
somme_roles  += prop_LGBlan + prop_EnSauv 

#print(somme_roles)



#### Paramètres de ces rôles

Ancien_nbProtec  = 3
Sorcie_nbPotVie  = 2
Sorcie_nbPotMort = 1
LGNoir_nbInfect  = 1
Juge_nbExil      = 2



#### Paramètre de la Partie

vote_aucunHabChoisi_meurtreHasard = False
vote_maire_voixBonus             = 1

partiePdt_Weekend                = False

FN_peuventParler_pdt_Journee     = True
LG_peuventParler_pdt_Journee     = True



#### Mode clair / flou et obscur

choix_mode_clair  = "Mode Clair"
choix_mode_obscur = "Mode Obscur"

mode_choisi = choix_mode_clair

mort_infecte_cache   = False 
mort_amoureux_cache  = False

mort_noct_role_cache  = False
mort_soir_role_cache  = False

tombe_affiche_role    = True

rapportMunicipal_affichage_roles = True


def passage_en_mode_clair () :
    
    global mort_infecte_cache , mort_amoureux_cache
    global mort_noct_role_cache, mort_soir_role_cache
    
    global tombe_affiche_role

    global rapportMunicipal_affichage_roles
    
    global mode_choisi
    
    
    
    mode_choisi = choix_mode_clair
    
    mort_infecte_cache   = False 
    mort_amoureux_cache  = False
    
    mort_noct_role_cache  = False
    mort_soir_role_cache = False
    
    tombe_affiche_role    = True
    
    rapportMunicipal_affichage_roles = True





def passage_en_mode_obscur () :
    
    global mort_infecte_cache , mort_amoureux_cache
    global mort_noct_role_cache, mort_soir_role_cache
    
    global tombe_affiche_role

    global rapportMunicipal_affichage_roles
    
    global mode_choisi
    
    
    
    mode_choisi = choix_mode_obscur
    
    mort_infecte_cache   = True 
    mort_amoureux_cache  = True
    
    mort_noct_role_cache  = True
    mort_soir_role_cache = True
    
    tombe_affiche_role    = False
    
    rapportMunicipal_affichage_roles = False
    
    
passage_en_mode_obscur()
    

# %% Variables de la Partie

# %%% Variables horaires

HParis = tz.gettz("Europe/Paris")

def maintenant(fuseauHoraire = HParis):
    """
    Retourne l'heure actuelle (sous forme de datetime) dans le fuseauHoraire (dateutil.zoneinfo.tzfile) donné
    """
    return datetime.now(tz = fuseauHoraire)


hInit  = maintenant()
        
ajd    = datetime( hInit.year, hInit.month, hInit.day       , tzinfo = HParis )
dem    = ajd + timedelta(days = 1)



#### Heure de début de nuit

nuit_hDeb_Theo = datetime( ajd.year, ajd.month, ajd.day,  8, 00, tzinfo = HParis )
nuit_hDeb      = nuit_hDeb_Theo

if hInit > nuit_hDeb_Theo :
    
    if hInit - nuit_hDeb_Theo < timedelta(hours = 3):
        nuit_hDeb = hInit
        
    else :
        ajd       = dem
        dem       = ajd + timedelta(days = 1)
        
        nuit_hDeb = datetime( ajd.year, ajd.month, ajd.day,  8, 00, tzinfo = HParis )



#### Autres moments important de la nuit

conseilLG_hFin = datetime( ajd.year, ajd.month, ajd.day, 14, 00, tzinfo = HParis )
part3_hDeb     = conseilLG_hFin + timedelta(seconds = 10)
nuit_hFin      = datetime( ajd.year, ajd.month, ajd.day, 18, 00, tzinfo = HParis )



#### Durée des différentes phases

nuit_duree  =  nuit_hFin -  nuit_hDeb

conseilLG_duree = conseilLG_hFin - nuit_hDeb
avtP3_duree     =     part3_hDeb -  nuit_hDeb
part3_duree     =      nuit_hFin - part3_hDeb



#### Moments important de la journée

tour1Vote_hFin  = datetime( ajd.year, ajd.month, ajd.day, 21, 30, tzinfo = HParis )
envDefVote_hFin = datetime( ajd.year, ajd.month, ajd.day, 23, 30, tzinfo = HParis )
tour2Vote_hFin  = datetime( dem.year, dem.month, dem.day,  0, 00, tzinfo = HParis )


def dans_premierTour() :
    """
    Renvoie True si 13h n'est pas passé
    """
    
    return maintenant() < tour1Vote_hFin


def dans_dernierTour() :
    """
    Renvoie True si 17h30 n'est pas passé
    """
    
    return maintenant() < tour2Vote_hFin

async def attente_du_moment_x (moment_fin_attente):
    
    while maintenant() < moment_fin_attente :
        await asyncio.sleep(1)




# %% Fonction de Plantage

def plantage():
    """
    L'objectif est de saturer la ram (512 Mo) du serveur heroku, pour qu'il plante,
    et redémarre automatiquement le programme  
    """
    
    erreur = []
    
    while True : 
        erreur.append(erreur)