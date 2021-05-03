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



# %% Compo de la Prochaine Partie 

#### Nombre de rôles

nb_Villag = 10
nb_Cupido = 0
nb_Ancien = 0

nb_Salvat = 0
nb_Sorcie = 5
nb_Voyant = 5

nb_Chasse = 0
nb_Corbea = 4
nb_Hirond = 4
      
nb_Famill = 3

nb_LG     = 4
nb_LGNoir = 3
nb_LGBleu = 2

nb_LGBlan = 0
nb_EnSauv = 0


#### Paramètres de ces rôles

Ancien_nbProtec  = 3
Sorcie_nbPotVie  = 2
Sorcie_nbPotMort = 1
LGNoir_nbInfect  = 1


#### Paramètre de la Partie

vote_aucunHabChoisi_meutreHasard = False
vote_maire_plus2Voix             = True

partiePdt_Weekend                = True


# %% Variables de la Partie

phase0       = "```Phase 0 - Entre Partie```"

phase1       = "```Phase 1 - Inscription```"
phase2       = "```Phase 2 - Début de Partie```"
phase3       = "```Phase 3 - Partie```"
phase4       = "```Phase 4 - Fin de Partie```"

phaseEnCours = None

nbTours = 0




# %%% Variables horaires

HParis = tz.gettz("Europe/Paris")

def maintenant(fuseauHoraire = HParis):
    """
    Retourne l'heure actuelle (sous forme de datetime) dans le fuseauHoraire (dateutil.zoneinfo.tzfile) donné
    """
    return datetime.now(tz = fuseauHoraire)


hInit     = maintenant()
        
ajd       = datetime( hInit.year, hInit.month, hInit.day       , tzinfo = HParis )
dem       = ajd + timedelta(days = 1)



#### Heure de début de nuit

nuit_hDeb_Theo = datetime( ajd.year, ajd.month, ajd.day, 18, 00, tzinfo = HParis )
nuit_hDeb      = nuit_hDeb_Theo

if hInit > nuit_hDeb_Theo :
    nuit_hDeb = hInit



#### Autre moment important de la nuit

conseilLG_hFin = datetime( ajd.year, ajd.month, ajd.day, 20, 00, tzinfo = HParis )
part3_hDeb     = conseilLG_hFin + timedelta(seconds = 30)
nuit_hFin      = datetime( dem.year, dem.month, dem.day,  9, 00, tzinfo = HParis )



#### Durée des différentes phases

nuit_duree  = nuit_hFin  - nuit_hDeb
avtP3_duree = part3_hDeb - nuit_hDeb
part3_duree = nuit_hFin  - part3_hDeb



#### Moment important de la journée

tour1Vote_hFin  = datetime(dem.year, dem.month, dem.day, 13, 00, tzinfo = HParis)
envDefVote_hFin = datetime(dem.year, dem.month, dem.day, 17, 00, tzinfo = HParis)
tour2Vote_hFin  = datetime(dem.year, dem.month, dem.day, 17, 30, tzinfo = HParis)


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