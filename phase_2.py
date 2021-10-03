# -*- coding: utf-8 -*-

"""
======================================================================================
===                                                                                ===
===                                     Phase 2                                    ===
===                                                                                ===
======================================================================================
                                          v1                                29/05/2021
"""


import phase_3    as fP3

# Niveau F
fTou = fP3.fTou


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





async def finInscription():
    
#### Nettoyage des salons de groupes
    
    await fGrp.fct_suppression_salons_msgs_idDiscord_TousLesGroupes()





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
    
    await fHab.redef_TousLesHabitants()
    
    nbHabitants_parVillage_Souhaite = v.tailleVlg_Ideal
    
    #nbVillages_Reel                 = 0
    nbHabitants_parVillage_Reel     = nbHabitants_parVillage_Souhaite
    
    ecartMin                        = len(fHab.TousLesHabitants) + 1
    
    for n in range( 1, len(fHab.TousLesHabitants) + 1 ):
        ecart = abs(len(fHab.TousLesHabitants)/n - nbHabitants_parVillage_Souhaite)
        
        if ecart < ecartMin :
            #nbVillages_Reel             = n
            nbHabitants_parVillage_Reel = len(fHab.TousLesHabitants) // n
            
            ecartMin                    = ecart
    
    
    nbHab_parVlg_Min = int( nbHabitants_parVillage_Reel * (1 - margeHabitants) - 1 )
    nbHab_parVlg_Max = int( nbHabitants_parVillage_Reel * (1 + margeHabitants) + 1 )
    
    listeVillages_Valides = []
    
    
    
    
    
#### --- Nombre de personne dans chaque groupe ---

    for grp in listeGroupes :
        grp.personnes = []
        for hab in fHab.TousLesHabitants :
            if hab.groupe == grp :
                grp.personnes.append(hab)
        
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
                listeVillages_Valides.append(liste_VlgPossibles[int(j)])
            
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
    
    listeJoueursRestants = list(fHab.TousLesHabitants)
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
    
    for hab in listeJoueursRestants :
        
        grpJoueur = None
        for grp in fGrp.TousLesGroupes :
            if hab.groupe == grp :
                grpJoueur = grp
        
        
        message = f"Il reste {hab.member.mention} (il est dans {grpJoueur}) (envoie le village sous cette forme : '12') :"
        
        for i in range(len(listeVillages_Valides)) :
            vlg = listeVillages_Valides[i]
            message += f"\n> n°{i}    [{len(liste_VlgValides_Habs[i])}]   - (  "
            for grp in vlg :
                message += f"{grp} ({grp.nbPersonne})   ,   "
            message += ")"
        
        await fDis.userCamp.send(message)
        reponse = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
        
        liste_VlgValides_Habs[int(reponse.content)].append(hab)
    
    
    
#### Création d'un village avec toutes les personnes restantes, si possible
    
    message = "Voici la liste des villages définitive :"
    
    for i in range(len(liste_VlgValides_Habs)) :
        vlg = liste_VlgValides_Habs[i]
        message += f"\n> n°{i}    [{ len(vlg) }]   - (   "
        for joueur in vlg :
            message += f"{joueur.member.display_name}   ,   "
        message += ")"
    
    await fDis.userCamp.send(message)
    
    
    
#### --- Création des villages ---
    
    donneeJoueur = fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs)
    
#### Association des habitants à leur village
    
    for i in range(len(liste_VlgValides_Habs)) :
        
        vlg = liste_VlgValides_Habs[i]
        
        for hab in vlg :
            ligne, numLigne = fGoo.ligne_avec( hab.member.id, fGoo.clef_idDiscord, donneeJoueur )
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
        
        ligne, numLigne = fGoo.ligne_avec( hab.matricule, fGoo.clef_Matricule, donnee )
        
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
    
    await fP3.attente_lancementTour()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_1 (ctx):
    
    await fDis.channelHistorique.edit(topic = v.phase2)
    
    #await finInscription()
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
    
    await fP3.attente_lancementTour()
