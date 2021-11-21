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

separation  = "_ _\n_ _\n_ _"




nbDigit_Matricule = 3

# %% Compo de la Prochaine Partie 

#### Nombre des rôles (pour une partie à 30)

tailleVlg_Ideal = 12

prop_Villag        = 1
prop_VillaVilla    = 1
prop_Cupido        = 1
prop_Ancien        = 1

prop_Salvat        = 2
prop_Sorcie        = 2
prop_Voyant        = 2
prop_Voyante_dAura = 1

prop_Corbea        = 1
prop_Hirond        = 1
prop_Juge          = 1

prop_Chasse        = 1
      
prop_Famill        = 1

prop_LG            = 2
prop_LGNoir        = 1
prop_LGBleu        = 1
prop_Traitre       = 1

prop_LGBlan        = 1
prop_EnSauv        = 1



#### Paramètres de ces rôles

Ancien_nbProtec  = 3
Sorcie_nbPotVie  = 2
Sorcie_nbPotMort = 1
LGNoir_nbInfect  = 1
Juge_nbExil      = 2



#### Paramètre de la Partie

vote_aucunHabChoisi_meurtreHasard = False
vote_maire_voixBonus             = 1

partiePdt_Weekend                = True

FN_peuventParler_pdt_Journee     = True
LG_peuventParler_pdt_Journee     = True



#### Mode clair / flou et obscur

choix_mode_clair  = "Mode Clair"
choix_mode_obscur = "Mode Obscur"

mode_choisi = choix_mode_clair

mort_infecte_cachee   = False 
mort_amoureux_cachee  = False

mort_noct_role_cache  = False
mort_soir_role_cachee = False

tombe_affiche_role    = True

rapportMunicipal_affichage_roles = True


def passage_en_mode_clair () :
    
    global mort_infecte_cachee , mort_amoureux_cachee
    global mort_noct_role_cache, mort_soir_role_cachee
    
    global tombe_affiche_role

    global rapportMunicipal_affichage_roles
    
    global mode_choisi
    
    
    
    mode_choisi = choix_mode_clair
    
    mort_infecte_cachee   = False 
    mort_amoureux_cachee  = False
    
    mort_noct_role_cache  = False
    mort_soir_role_cachee = False
    
    tombe_affiche_role    = True
    
    rapportMunicipal_affichage_roles = True





def passage_en_mode_obscur () :
    
    global mort_infecte_cachee , mort_amoureux_cachee
    global mort_noct_role_cache, mort_soir_role_cachee
    
    global tombe_affiche_role

    global rapportMunicipal_affichage_roles
    
    global mode_choisi
    
    
    
    mode_choisi = choix_mode_obscur
    
    mort_infecte_cachee   = True 
    mort_amoureux_cachee  = True
    
    mort_noct_role_cache  = True
    mort_soir_role_cachee = True
    
    tombe_affiche_role    = False
    
    rapportMunicipal_affichage_roles = False
    
    
passage_en_mode_obscur()
    

# %% Variables de la Partie

phase0       = "Phase 0" # Entre Partie

phase1       = "Phase 1" # Inscription
phase2       = "Phase 2" # Début de Partie
phase3       = "Phase 3" # Partie
phase4       = "Phase 4" # Fin de Partie

phaseEnCours = None

nbTours = 0




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





# %% Fonction de Plantage

def plantage():
    """
    L'objectif est de saturer la ram (512 Mo) du serveur heroku, pour qu'il plante, et redémarre automatiquement le programme  
    """
    
    erreur = []
    
    while True : 
        erreur.append(erreur)