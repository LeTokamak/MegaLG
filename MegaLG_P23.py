# -*- coding: utf-8 -*-

"""
======================================================================================
===                                                                                ===
===                                    Phase 2/3                                   ===
===                                                                                ===
======================================================================================
                                          v1                                29/05/2021
"""

# Niveau E
import E_fct_Tour        as fTou


# Niveau D
fVlg = fTou.fVlg


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

from   pandas            import DataFrame
import itertools





# %% Events

# %%% Messages

async def message_voteVillage():
    
    def verifVoteVillage(message):
        verifSalon, verifUser = (False, False)
        
        verifPhase = v.phaseEnCours == v.phase3
        
        if fDis.verifServeur(message) :
            verifUser  = fDis.roleJoueurs in message.author.roles
            
            if verifUser and verifPhase :
                verifSalon = fVlg.village_avec(message.channel.id, 'idSalon_Bucher') != None
        
        return verifUser  and  verifPhase and verifSalon


    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteVillage)
        await fDis.effacerMsg (message.channel)
        await fVlg.evt_voteVlg(message.author, message.content)


        
async def message_voteLoupGarou():
    
    def verifVoteLG(message):
        verifSalon, verifUser = (False, False)
        
        verifPhase = v.phaseEnCours == v.phase3
        
        if fDis.verifServeur(message) :
            verifUser  = fDis.roleJoueurs in message.author.roles
            
            if verifUser and verifPhase :
                verifSalon = fVlg.village_avec(message.channel.id, 'idSalon_VoteLG') != None
        
        return verifUser  and  verifPhase and verifSalon


    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteLG)
        await fDis.effacerMsg(message.channel)
        await fVlg.evt_voteLG(message.author, message.content)
        
        
        
# %% --- Phase 2 ---

async def finInscription():
    pass
    
#### Nettoyage des salons de groupes
    
    "A programmer"





async def numerotationHabitants():
    
    Joueurs = fGoo.donneeGoogleSheet( fGoo.page1_InfoJoueurs )

#### Tri des Joueurs par nom de groupe, par nom de joueur et par prénom

    for j in Joueurs :
        
        habitant = fHab.Habitant( 0                         ,
                                  j[fGoo.clef_Prenom      ] ,
                                  j[fGoo.clef_Nom         ] ,
                                  j[fGoo.clef_Groupe      ] ,
                                  0                         ,
                                  j[fGoo.clef_Sexe        ] ,
                                  j[fGoo.clef_idDiscord   ] ,
                                  ""                        ,
                                  ""                        ,
                                  ""                          )
        
        await habitant.init_groupe()
        
        if habitant.groupe != fGrp.GroupeParDefaut :
            j["strGroupe"] = str(habitant.groupe)
        
        else :
            j["strGroupe"] = "ZZZZZZZZZZZZZZZZZZ"
    
    
    
    dfJoueurs                      = DataFrame(Joueurs)
    dfJoueurs                      = dfJoueurs.sort_values(by = ["strGroupe", fGoo.clef_Nom, fGoo.clef_Prenom])
    dfJoueurs                      = dfJoueurs.drop(["strGroupe"], axis = 1)
    dfJoueurs[fGoo.clef_Matricule] = range(1, len(Joueurs) + 1)

    listeJoueurs                   = fGoo.dfToList(dfJoueurs)    
    
    
    
    for j in listeJoueurs[1:] :
        
#   j = ['', H, Clément, CAMPANA, 27, 0, 269051521272905728, '', '', '']
                
        membJou = fDis.serveurMegaLG.get_member(int(j[6]))
                
        surnom  = membJou.display_name
        
        while len(surnom) + (v.nbDigit_Matricule + 1) > 32 :
            surnom = surnom[ :-1]
        
        await membJou.edit(nick = f"{fMeP.AjoutZerosAvant(j[0], v.nbDigit_Matricule)}┃{surnom}")
    
    
    
    fGoo.page1_InfoJoueurs.clear()
    fGoo.page1_InfoJoueurs.insert_rows(fGoo.strListe(listeJoueurs))
    
    fGoo.page1_Sauvegarde .clear()
    fGoo.page1_Sauvegarde .insert_rows(fGoo.strListe(listeJoueurs))





async def repartionGroupes_Villages() :
    
    def habitants(vlg):
        habsVlg = []
        for grp in vlg :
            habsVlg.extend(grp.personnes)
            
        return habsVlg
    
    
    def nbHabitant(vlg):
        sommeHab = 0
        for grp in vlg :
            sommeHab += grp.nbPersonne
            
        return sommeHab
        
        
    def verifVlg_Incoherent(vlg):
        villageIncoherent = False
            
        for grp1 in vlg :
            for grp2 in vlg :
                if grp1 in grp2.sur_Groupes :
                    villageIncoherent = True
            
        return villageIncoherent
        
    
    def suppressionVlg_identiques(liste_vlg):
        for vlg in liste_vlg :
            for vlg2 in liste_vlg :
                if vlg != vlg2  and  habitants(vlg) == habitants(vlg2):
                    liste_vlg.remove(vlg)
    
    
    def estUnSousGroupe_dUnVlgValide(grp):
        for vlg in listeVillages_Valides :
            for surGrp in vlg :
                if surGrp in grp.sur_Groupes :
                    return True
        return False
    
    
    def estUnSurGroupe(surGrp):
        for grp in fGrp.TousLesGroupes :
            if surGrp in grp.sur_Groupes :
                return True
                
        return False
    
    
    
#### --- Variables ---
    
    listeGroupes   = list(fGrp.TousLesGroupes)
    
    margeHabitants = 0.05
    
    TousLesJoueurs = fDis.roleJoueurs.members
    
    nbHabitants_parVillage_Souhaite = v.tailleVlg_Ideal
    
    #nbVillages_Reel                 = 0
    nbHabitants_parVillage_Reel     = nbHabitants_parVillage_Souhaite
    
    ecartMin                        = len(TousLesJoueurs) + 1
    
    for n in range( 1, len(TousLesJoueurs) + 1 ):
        ecart = abs(len(TousLesJoueurs)/n - nbHabitants_parVillage_Souhaite)
        
        if ecart < ecartMin :
            #nbVillages_Reel             = n
            nbHabitants_parVillage_Reel = len(TousLesJoueurs) // n
            
            ecartMin                    = ecart
    
    
    nbHab_parVlg_Min = int( nbHabitants_parVillage_Reel * (1 - margeHabitants) - 1 )
    nbHab_parVlg_Max = int( nbHabitants_parVillage_Reel * (1 + margeHabitants) + 1 )
    
    listeVillages_Valides = []
    
    
    
    
    
#### --- Nombre de personne dans chaque groupe ---

    for grp in listeGroupes :
        grp.personnes = []
        for member in TousLesJoueurs :
            if grp.salon.permissions_for(member).read_messages == True :
                grp.personnes.append(member)
        
        grp.nbPersonne = len(grp.personnes)
    
    
    
    
#### --- Nettoyages de listeGroupes ---
    
#### Groupes vides || Suppression des groupes vides ou ne contanant qu'une personne (géré après en tant que personne manquante)
    
    listeGroupes = [grp for grp in listeGroupes if grp.nbPersonne >= 2]
    
    
    
#### Groupes bons || Villages déjà formés (groupes ayant un bon nombre de personne)    
    
    listeVillages_Valides.extend([ (grp,)  for  grp   in listeGroupes          if grp.nbPersonne in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)])
    listeVillages_Valides =      [ (grp,)  for (grp,) in listeVillages_Valides if not estUnSousGroupe_dUnVlgValide(grp)]
    
    
    listeGroupes = [ grp for grp in listeGroupes if (grp.nbPersonne not in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)  and  not estUnSousGroupe_dUnVlgValide(grp) )]
    
    
    
#### Groupes surchargés || Suppression des sur-groupes ayant un trop grand nombre de personnes
    
# Créations de village composé d'un seul sous-groupe ayant trop de membre
    listeVillages_Valides.extend([ (grp,)  for grp in listeGroupes   if (grp.nbPersonne >  nbHab_parVlg_Max  and  not estUnSurGroupe(grp))])
    
    
# Suppression des groupes ayant trop de membre (sur-groupes ==> A supprimer (les personnes supprimées sont gérés dans personnes manquantes) , sous-groupe ==> devenu des villages )
    listeGroupes =               [  grp    for grp in listeGroupes   if  grp.nbPersonne <= nbHab_parVlg_Max ]
    
    
    
    
    
#### --- Classement des Groupes par nombre de personne ---
    """
    PAS ENCORE UTILISE
    
    listeGroupes_Tries = []
    
    for i in range(1, nbHab_parVlg_Min + 1):
        listeGroupes_Tries.append([])
    
    for grp in listeGroupes :
        listeGroupes_Tries[grp.nbPersonne].append(grp)
    
    listeGroupes_Restants = list(listeGroupes_Tries)
    """
    
    
    
    
    
#### --- Listage de toutes les combinaison ---
    
    composition_canton_Trouve = False
    
    while not composition_canton_Trouve :
        
        liste_VlgPossibles = []
    
#### Il y a peu de groupe : Listage complet
        
        if len(listeGroupes) <= 30 :
            
            for n in range(1,8):
                liste_VlgPossibles.extend( list(itertools.combinations(listeGroupes, n)) )
                
#### Il y a plus de groupe : Pré-triage et Listage des villages intéressants
        
        
#### Il y a trop de groupe : Listage impossible
        
        else :
            await fDis.channelHistorique.send("**ERREUR** - Il y a trop de groupes (> 30)")
        
        
        
        
        
#### --- Tri des villages Possibles ---    
    
#### 1er Tri : Suppression des villages trop petit ou trop grop et des villages incohérents
        
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   nbHabitant(vlg) in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1) ]
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   not verifVlg_Incoherent(vlg)                                     ]
        
        
        
#### 2ème Tri : Gestions des groupes Supprimé lors du 1er Tri
        
#### Listage des groupes manquants

        def verif_personneGrpDansVillage(liste_Vlg, grp):
            for vlg in liste_Vlg:
                if grp.personnes[0] in habitants(vlg) :
                    return True
                
            return False
        
        grpManquant = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillage(liste_VlgPossibles, grp) ]
        
#### Ajouts des petits groupes manquants au villages qui peuvent les accueillir 
        
        for grp in grpManquant :
            for vlg in liste_VlgPossibles : 
                if nbHabitant(vlg) + grp.nbPersonne < nbHab_parVlg_Max :
                    vlg += ( grp ,)
        
        grpManquant = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillage(liste_VlgPossibles, grp) ]
    
#### Formation d'un village avec les groupes manquants restants
        
        if len(grpManquant) != 0 :
            liste_VlgPossibles.append(tuple(grpManquant))
        
        
        
#### 3ème Tri : Suppresion des villages ayant les même habitants
        
        suppressionVlg_identiques(liste_VlgPossibles)
        suppressionVlg_identiques(listeVillages_Valides)
        
    
        
# Ici liste_VlgPossibles ne contient que :
#   - des villages de bonne taille          (sauf un eventuel village créer avec les groupes manquants restants)
#   - des villages cohérents INDEPENDAMMENT (cad pas de sous-groupe associer avec un de ses sur-groupe)
#   - des villages différents               (aucun village n'ont les même habitants)
    
    
    
    
    
#### --- Determination des villages validés ---
    
#### Mise de côté des village contenant un groupe présent qu'une fois
    
        for grp in listeGroupes :
            
            comptePresenceGrp = 0
            for vlg in liste_VlgPossibles :
                if grp in vlg :
                    comptePresenceGrp += 1
            
            if comptePresenceGrp == 1 :
                for vlg in liste_VlgPossibles :
                    if grp in vlg :
                        listeVillages_Valides.append(vlg)
                        liste_VlgPossibles.remove(vlg)
                        for grp in vlg :
                            try    : listeGroupes.remove(grp)
                            except : pass
        
        
        suppressionVlg_identiques(listeVillages_Valides)
        
        listeGroupes = [ grp   for grp in listeGroupes   if not verif_personneGrpDansVillage(listeVillages_Valides, grp) ]
        
        
        
#### ===== FIN DE LA BOUCLE ====

        if len(listeGroupes) == 0 :
            composition_canton_Trouve = True
            
        else :
            message = "On a tous tenté mais il reste des groupes qui respecte tous les critères, lesquels veux-tu choisir et garder (envoie les villages a garder sous cette forme : '12 54 94 2 0 47') :"
            
            for i in range(len(liste_VlgPossibles)) :
                vlg = liste_VlgPossibles[i]
                message += f"\n> n°{i}    [{nbHabitant(vlg)}]   - (  "
                for grp in vlg :
                    message += f"{grp} ({grp.nbPersonne})   ,   "
                message += ")"
            
            await fDis.envoieMsg(fDis.userCamp, message)
            reponse = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
            
            for j in reponse.content.split():
                listeVillages_Valides.append(liste_VlgPossibles[j])
            
            del(liste_VlgPossibles)
    
    
    

    
#### --- Suppression des villages qui contiennent toutes les pers d'un autre village ---
    
    for vlg in listeVillages_Valides :
        for vlg2 in listeVillages_Valides :
            
            habDansVlg2 = True
            
            for hab in habitants(vlg) :
                habDansVlg2 = habDansVlg2  and  hab in habitants(vlg2)
            
            if habDansVlg2 and vlg != vlg2 :
                listeVillages_Valides.remove(vlg)
    
    
    
#### --- Transformation des villages validés en liste d'habitants ---
    
    liste_VlgValides_Habs = []
    
    for vlg in listeVillages_Valides:
        liste_VlgValides_Habs.append( habitants(vlg) )
    
    
    
#### --- Gestion des personnes manquantes ---
    
    listeJoueursRestants = list(TousLesJoueurs)
    for vlg in listeVillages_Valides :
        for hab in habitants(vlg):
            try :
                listeJoueursRestants.remove(hab)
            except :
                print(f"ERREUR - Cette personne a déjà été supprimmé : {hab.display_name} ({vlg})")
    
    
    if len(listeJoueursRestants) in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1) :
        liste_VlgValides_Habs.append(tuple(listeJoueursRestants))
        listeJoueursRestants = []
    
    
    
#### Ajout des personnes restantes aux autres villages (manuellement)
    
    for joueur in listeJoueursRestants :
        
        grpJoueur = None
        for grp in fGrp.TousLesGroupes :
            if grp.salon.permissions_for(joueur).read_messages == True :
                grpJoueur = grp
        
        
        message = f"Il reste {joueur} (il est dans {grpJoueur}) (envoie le village sous cette forme : '12') :"
        
        for i in range(len(listeVillages_Valides)) :
            vlg = listeVillages_Valides[i]
            message += f"\n> n°{i}    [{len(liste_VlgValides_Habs[i])}]   - (  "
            for grp in vlg :
                message += f"{grp} ({grp.nbPersonne})   ,   "
            message += ")"
        
        await fDis.userCamp.send(message)
        reponse = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
        
        liste_VlgValides_Habs[int(reponse.content)].append(joueur)
    
    
    
#### Création d'un village avec toutes les personnes restantes, si possible
    
    message = "Voici la liste des villages définitive :"
    
    for i in range(len(liste_VlgValides_Habs)) :
        vlg = liste_VlgValides_Habs[i]
        message += f"\n> n°{i}    [{len(vlg)}]   - (   "
        for joueur in vlg :
            message += f"{joueur.display_name}   ,   "
        message += ")"
    
    await fDis.userCamp.send(message)
    
    
    
#### --- Création des villages ---
    
    donneeJoueur = fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs)
    
#### Association des habitants à leur village
    
    for i in range(len(liste_VlgValides_Habs)) :
        
        vlg = liste_VlgValides_Habs[i]
        
        for hab in vlg :
            ligne, numLigne = fGoo.ligne_avec( hab.id, fGoo.clef_idDiscord, donneeJoueur )
            fGoo.remplacerVal_ligne( i+1 , fGoo.clef_numVillage, numLigne, fGoo.page1_InfoJoueurs )
        
        await asyncio.sleep(1)
    
    await fHab.redef_TousLesHabitants()
    
#### Création des villages
    
    for i in range(len(liste_VlgValides_Habs)) :
    
        await fVlg.creationVillage( numNouvVillage = i+1 )
        
        await asyncio.sleep(0.5)





async def distributionRole(village):
    
#### Paquet des Rôles
    
    paquetRoles  = []
    
    paquetRoles += v.prop_Villag     *[fRol.role_Villageois]
    paquetRoles += v.prop_VillaVilla *[fRol.role_VillaVilla]
    paquetRoles += v.prop_Cupido     *[fRol.role_Cupidon   ]
    paquetRoles += v.prop_Ancien     *[fRol.role_Ancien    ]
    
    paquetRoles += v.prop_Salvat     *[fRol.role_Salvateur ]
    paquetRoles += v.prop_Sorcie     *[fRol.role_Sorciere  ]
    paquetRoles += v.prop_Voyant     *[fRol.role_Voyante   ]
    
    paquetRoles += v.prop_Corbea     *[fRol.role_Corbeau   ]
    paquetRoles += v.prop_Hirond     *[fRol.role_Hirondelle]
    paquetRoles += v.prop_Juge       *[fRol.role_Juge      ]
    
    paquetRoles += v.prop_Famill     *[fRol.role_FamilleNb ]
    
    
    
    paquetRoles += v.prop_LG         *[fRol.role_LG        ]
    paquetRoles += v.prop_LGNoir     *[fRol.role_LGNoir    ]
    paquetRoles += v.prop_LGBleu     *[fRol.role_LGBleu    ]
    
    paquetRoles += v.prop_LGBlan     *[fRol.role_LGBlanc   ]
    paquetRoles += v.prop_EnSauv     *[fRol.role_EnfantSauv]
    
    
    
#### Paquet des Rôles Restants
    
    paquetRoles_Restant = list(paquetRoles)
    
    rd.shuffle(paquetRoles_Restant)
    


#### --- Distribution des Rôles ---
    
    donnee = fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs)

    for hab in village.habitants :
        
        if len(paquetRoles_Restant) != 0 :
            habRole = paquetRoles_Restant.pop(0)
            
        else :
            habRole = rd.choice(paquetRoles)
        
        
        
#### Caractéristiques des Rôles
        
        caractRole = ""

        if   habRole == fRol.role_Ancien   : caractRole =    v.Ancien_nbProtec
        elif habRole == fRol.role_Sorciere : caractRole = f"{v.Sorcie_nbPotVie} {v.Sorcie_nbPotMort}"
        elif habRole == fRol.role_Juge     : caractRole =    v.Juge_nbExil
        elif habRole == fRol.role_LGNoir   : caractRole =    v.LGNoir_nbInfect
        
        
        
#### Enregistrement
        
        ligne, numLigne = fGoo.ligne_avec( hab.matri, fGoo.clef_Matricule, donnee )
        
        fGoo.remplacerVal_ligne( habRole[fRol.clefNom], fGoo.clef_Role       , numLigne, fGoo.page1_InfoJoueurs)
        fGoo.remplacerVal_ligne( caractRole           , fGoo.clef_caractRoles, numLigne, fGoo.page1_InfoJoueurs)
        
        await asyncio.sleep(0.1)
        
        
        
#### Envoie du Rôle
        
        await hab.member.send( f"Vous êtes **{habRole[fRol.clefNom]}** :" )
        await hab.member.send( embed = habRole[fRol.clefEmbed]            )





# %%% Commandes




@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DebutPartie (ctx):
    
#### DP_1
    
    await fDis.channelHistorique.edit(topic = v.phase2)
    
    await finInscription()
    await numerotationHabitants()
    
    
    
#### DP_2
    
    await repartionGroupes_Villages()
    
    
    
#### DP_3
    
    for vlg in fVlg.TousLesVillages :
        await distributionRole(vlg)
    
    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
    
    v.nbTours = 0
    await fDis.channelHistorique.edit(topic = f"{v.phase3} - Tour n°{v.nbTours}")
    
    await attente_lancementTour()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_1 (ctx):
    
    await fDis.channelHistorique.edit(topic = v.phase2)
    
    await finInscription()
    await numerotationHabitants()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_2 (ctx):
    
    await repartionGroupes_Villages()
    


@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_3 (ctx):

    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()    

    for vlg in fVlg.TousLesVillages :
        await distributionRole(vlg)

    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
    
    v.nbTours = 0
    await fDis.channelHistorique.edit(topic = f"{v.phase3} - Tour n°{v.nbTours}")
    
    await attente_lancementTour()




# %% --- Phase 3 ---


async def attente_lancementTour() :
        
    m = v.maintenant()

#### ||| Variable ||| Si on est dans le WE on ne lance pas la fonction Tour

    if not v.partiePdt_Weekend  and  m.weekday() in (4,5) :
        await fDis.channelHistorique.send("Nous somme Vendredi ou Samedi, la fonction Lancement à été stoppée dans son élan !")
        return None
    
    
    
#### Attente du début de la nuit pour lancer la fontion Tour 

    tempsAtt            = v.nuit_hDeb  -  m
    intervalMaintenance = v.nuit_hDeb  -  (v.tour2Vote_hFin - v.timedelta(days = 1))   # 30 mins
    
    
    
    # Plantage si le temps d'Attente est suppérieur à 30 minutes
    
    if tempsAtt >= intervalMaintenance :
        
        tempsAtt_Plantage = tempsAtt - (intervalMaintenance - v.timedelta(minutes = 5))
        
        await fDis.channelHistorique.send(f"Attente de {tempsAtt_Plantage} avant le plantage")
        await asyncio.sleep(tempsAtt_Plantage.seconds)
        
        fTou.plantage()
    
    
    
    # Sinon attente avant de lancer la fonction Tour
    
    else :
        await fDis.channelHistorique.send(f"Attente de {tempsAtt} avant de lancer la nuit n°{v.nbTours}")
        
        if tempsAtt > v.timedelta(0) :
            await asyncio.sleep(tempsAtt.seconds)
        
        await fTou.Tour()
        
        
        
        

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Lancement(ctx):
    
    await fDis.effacerMsg(ctx)
    await attente_lancementTour()



# %%% Vote

@fDis.bot.command()
async def Vote(ctx, matricule):
    await fVlg.cmd_vote(ctx.author, matricule)
    
    
@fDis.bot.command()
async def vote(ctx, matricule):
    await fVlg.cmd_vote(ctx.author, matricule)

    

    

# %%% Exil (reservée aux Juges et au Maire)

@fDis.bot.command()
async def Exil(ctx):
    await fVlg.cmd_demandeExilVote(ctx.author)

@fDis.bot.command()
async def exil(ctx):
    await fVlg.cmd_demandeExilVote(ctx.author)





# %%% Changement du nom du village (reservée au Maire)

@fDis.bot.command()
async def Renommage(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)
    
@fDis.bot.command()
async def renommage(ctx, *tupleNom):
    await fVlg.cmd_changementNomVillage(ctx.author, tupleNom)




# %%% Maintenance
     
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
    
    if v.phaseEnCours == v.phase3 :
        
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