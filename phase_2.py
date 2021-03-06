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

#### Tri des Joueurs par nom de groupe, par pseudo de joueur

    for j in Joueurs :
        
        print(f"TEST - {j[fGoo.clef_Pseudo]} / {int(j[fGoo.clef_Groupe])} / {j[fGoo.clef_Sexe]} / {j[fGoo.clef_idDiscord]}")
        
        habitant = fHab.Habitant( 0                          ,
                                  j[fGoo.clef_Pseudo      ]  ,
                                  int(j[fGoo.clef_Groupe  ]) ,
                                  0                          ,
                                  j[fGoo.clef_Sexe        ]  ,
                                  j[fGoo.clef_idDiscord   ]  ,
                                  ""                         ,
                                  ""                         ,
                                  ""                           )
        
        await habitant.init_groupe()
        
        if habitant.groupe != fGrp.GroupeParDefaut :
            j["strGroupe"] = str(habitant.groupe)
        
        else :
            j["strGroupe"] = "ZZZZZZZZZZZZZZZZZZ"
    
    
    
    dfJoueurs                      = DataFrame(Joueurs)
    dfJoueurs                      = dfJoueurs.sort_values(by = ["strGroupe", fGoo.clef_Pseudo])
    dfJoueurs                      = dfJoueurs.drop(["strGroupe"], axis = 1)
    dfJoueurs[fGoo.clef_Matricule] = range(1, len(Joueurs) + 1)

    listeJoueurs                   = fGoo.dfToList(dfJoueurs)    
    
    
    
    for j in listeJoueurs[1:] :
        
#   j = ['', H, Tokamak, 27, 0, 269051521272905728, '', '', '']
                
        membJou = fDis.serveurMegaLG.get_member(int(j[5]))
                
        surnom  = j[2]
        
        while len(surnom) + (v.nbDigit_Matricule + 1) > 32 :
            surnom = surnom[ :-1]
        
        await membJou.edit(nick = f"{fMeP.AjoutZerosAvant(j[0], v.nbDigit_Matricule)}???{surnom}")
    
    
    
    fGoo.page1_InfoJoueurs.clear()
    fGoo.page1_InfoJoueurs.insert_rows(fGoo.strListe(listeJoueurs))
    
    fGoo.page1_Sauvegarde .clear()
    fGoo.page1_Sauvegarde .insert_rows(fGoo.strListe(listeJoueurs))





# %% R??partition des Groupes en Villages 

async def repartitionGroupes_Villages() :
    
# %%% Sous-fonctions
    
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
    
    
    def contient (L1, L2) :
        """
        Verifie si les ??l??ment de L2 sont contenus dans L1
        """
        L1_contient_L2 = True
        
        for element in L2 :
            L1_contient_L2 = L1_contient_L2  and  element not in L1
                
        return L1_contient_L2
    
    
    def suppressionVlg_identiques(liste_vlg):
        for vlg in liste_vlg :
            for vlg2 in liste_vlg :
                
                if vlg != vlg2  and  contient(habitants(vlg), habitants(vlg2)):
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
    
    def verif_personneGrpDansVillage(liste_Vlg, grp):
        for vlg in liste_Vlg :
            for hab in habitants(vlg) :
                if hab in grp.personnes :
                    return True
                
        return False
    
    
# %%% D??but de la fonction
    
    await fDis.channelHistorique.send("``` --- D??but de la r??partition des joueurs en villages --- ```")

    await fHab.redef_TousLesHabitants()
    
    
# =============================================================================
#### --- Taille des villages ---
# =============================================================================
    
    listeGroupes     = list(fGrp.TousLesGroupes)
    margeHabitants   = 0.00
    
    nbHab_parVlg_Min = int( v.tailleVlg_Ideal * (1 - margeHabitants) - 1 )
    nbHab_parVlg_Max = int( v.tailleVlg_Ideal * (1 + margeHabitants) + 1 )
    
    listeVillages_Valides = []
    
    await fDis.channelHistorique.send(f"> nbHab_parVlg_Min = {nbHab_parVlg_Min}\n> nbHab_parVlg_Max = {nbHab_parVlg_Max}")
    
    
    
    
    
# =============================================================================
#### --- Listage des membres de chaque groupe ---
# =============================================================================
#
#     Un attribut est ajout?? a chaque groupe, c'est une liste qui
#  contient les objets Habitants des membres du groupes.
#

    for grp in listeGroupes :
        
        grp.personnes = []
        
        for hab in fHab.TousLesHabitants :
            if hab.groupe == grp         : grp.personnes.append(hab)
        
        grp.nbPersonne = len(grp.personnes)
    
    
    
    
    
# =============================================================================
#### --- Nettoyages de listeGroupes ---
# =============================================================================
#
#    Suppression des groupes ne pouvant pas former de village, ou formant d??j?? un village. 
#
  
## -- Groupes vides -- 
#
# Suppression des groupes vides.
# Suppression des groupes ne contanant qu'une personne (g??r??e apr??s en tant que personne manquante).
#
    
    listeGroupes = [grp for grp in listeGroupes if grp.nbPersonne >= 2]
    
    
    
## -- Groupes bons --
#
# Cr??ation    des villages d??j?? form??s (groupes ayant un bon nombre de personne).
# Suppression des villages form??s ?? partir d'un sous-groupe d'un groupe formant un village.
# Suppression des groupes pouvant former des villages.
# Suppression des sous-groupes des villages form??es.
# 
    
    listeVillages_Valides.extend([ (grp,)  for  grp   in listeGroupes          if grp.nbPersonne in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)])
    listeVillages_Valides =      [ (grp,)  for (grp,) in listeVillages_Valides if not estUnSousGroupe_dUnVlgValide(grp)]
    
    
    listeGroupes = [ grp for grp in listeGroupes if (grp.nbPersonne not in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1)  and  not estUnSousGroupe_dUnVlgValide(grp) )]
    
    
    
## -- Groupes surcharg??s --
#
# Cr??ations de village compos?? d'un seul sous-groupe ayant trop de membre.
# Suppression des groupes ayant trop de membre :
#     sur-groupes  trop charg??s ==> A supprimer          (les personnes supprim??es sont g??r??s dans les personnes manquantes) 
#     sous-groupes trop charg??s ==> Devenus des villages
#    

    listeVillages_Valides.extend([ (grp,)  for grp in listeGroupes   if (grp.nbPersonne >  nbHab_parVlg_Max  and  not estUnSurGroupe(grp))])
    
    listeGroupes_nonValides =    [  grp    for grp in listeGroupes   if  grp.nbPersonne >= nbHab_parVlg_Max ]
    
    
    
    
    
## -- Envoie de listeGroupes_nonValides et de listeVillages_Valides --
    
    msgLogs  = "_ _\n\n\n ` Apr??s nettoyages des groupes `\n"
    
    msgLogs += "listeVillages_Valides ="
    
    for vlg in listeVillages_Valides :
        msgLogs += f"\n> {vlg} **( {nbHabitant(vlg)} )**"
        
    msgLogs += "\n\n"
    msgLogs += "listeGroupes_nonValides ="
    
    for grp in listeGroupes_nonValides :
        msgLogs += f"\n> {grp} **( {grp.nbPersonne} )**"
    
    await fDis.envoieMsg( fDis.channelHistorique, msgLogs )
    
    
    
    
    
    
# %%% Boucle de R??partition des groupes non valid??s en villages
    
    while len(listeGroupes_nonValides) != 0 :
        
        listeGroupes_aCombiner = list(listeGroupes_nonValides)
        
# =============================================================================
#### --- Listage de toutes les combinaison ---
# =============================================================================        
#
#     Listage des tous les combinaison de groupes (ou villages) possibles,
#  ce calcul de cobinaison est tr??s complexe, donc pour limiter le temps de 
#  calcul, des limites sont impos??es par le programme. 
#     Elles concernent :
#        - Le nombre de groupe utilis?? pour faire les combinaisons.
#        - Le nombre de groupe pouvant former un village.
#
        
        limite_nbGrp_max_combinaison = 30
        limite_nbGrp_par_combinaison = 8
        
# S'il y a trop de groupe : Le listage est imcomplet, seule une partie des groupes est combin?? 
        
        if len(listeGroupes_nonValides) > limite_nbGrp_max_combinaison :
            
            await fDis.channelHistorique.send(f"Il y a trop de groupes (> {limite_nbGrp_max_combinaison}) - Le listage n'est que partiel")
            listeGroupes_aCombiner = rd.sample(listeGroupes_aCombiner, limite_nbGrp_max_combinaison)
        
        liste_VlgPossibles = []
        
        for n in range(1, limite_nbGrp_par_combinaison):
            liste_VlgPossibles.extend( list(itertools.combinations(listeGroupes_aCombiner, n)) )
        
        
        
        
        
# =============================================================================
#### --- Tri des villages Possibles ---    
# =============================================================================
        
#### - 1er Tri :
# 
# Suppression des villages trop grop.
# Suppression des villages incoh??rents.
#
            
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   nbHabitant(vlg) <= nbHab_parVlg_Max ]
        liste_VlgPossibles = [ vlg   for vlg in liste_VlgPossibles if   not verifVlg_Incoherent(vlg)        ]
            
            
#### - 2??me Tri :
#
# Gestions des groupes n'??tant dans aucun village possible.
#
    
# --- Listage des groupes manquants ---
            
        grpManquant = [ grp   for grp in listeGroupes_nonValides   if not verif_personneGrpDansVillage(liste_VlgPossibles, grp) ]
        
        
        
# --- Ajouts des petits groupes manquants au villages qui peuvent les accueillir ---
            
        for vlg in liste_VlgPossibles :
            rd.shuffle(grpManquant)
            
            for grp in grpManquant :
                
                if nbHabitant(vlg) + grp.nbPersonne <= nbHab_parVlg_Max :
                    vlg += ( grp ,)
        
        grpManquant = [ grp   for grp in listeGroupes_nonValides   if not verif_personneGrpDansVillage(liste_VlgPossibles, grp) ]
        
        
        
# --- Formation de villages avec les groupes manquants restants ---
        
        if len(grpManquant) != 0 :
            
            nb_hab_nv_Vlg = 0
            nv_Vlg        = ( )
            
            for grp in grpManquant :
                
                nb_hab_nv_Vlg +=   grp.nbPersonne
                nv_Vlg        += ( grp ,)
                
                if nb_hab_nv_Vlg >= nbHab_parVlg_Min  or  True :
                    
                    liste_VlgPossibles.append(nv_Vlg)
                    
                    nb_hab_nv_Vlg = 0
                    nv_Vlg        = ( )
            
            
            if nv_Vlg != () :
                liste_VlgPossibles.append(nv_Vlg)
        
        
        
#### - 3??me Tri :
#
# Suppresion des villages possibles ayant les m??me habitants
#
        
        suppressionVlg_identiques( liste_VlgPossibles )
        
        
        
# A ce stade, liste_VlgPossibles ne contient que :
#   - des villages de bonne taille          (sauf un eventuel village cr??er avec les groupes manquants restants)
#   - des villages coh??rents INDEPENDAMMENT (cad pas de sous-groupe associer avec un de ses sur-groupe)
#   - des villages diff??rents               (aucun village n'ont les m??me habitants)
        
        msgLogs  = "_ _\n\n\n ` Boucle  -  Suite au tri des villages Possibles `\n"
        
        msgLogs += "listeVillages_Valides ="
        
        for vlg in listeVillages_Valides :
            msgLogs += f"\n> {vlg} **( {nbHabitant(vlg)} )**"
            
        msgLogs += "\n\n"
        msgLogs += "liste_VlgPossibles ="
        
        for vlg in liste_VlgPossibles :
            msgLogs += f"\n> {vlg} **( {nbHabitant(vlg)} )**"
        
        await fDis.envoieMsg( fDis.channelHistorique, msgLogs )
        
        await asyncio.sleep(2)
        
        
        
        
        
# =============================================================================
#### --- Validation de villages ---
# =============================================================================
#
# Validation des villages contenant un groupe pr??sent qu'une fois.
#
        
        for grp in listeGroupes_nonValides :
            
            comptePresenceGrp = 0
            for vlg in liste_VlgPossibles :
                if grp in vlg : comptePresenceGrp += 1
            
            if comptePresenceGrp == 1 :
                for vlg in liste_VlgPossibles :
                    if grp in vlg :
                        listeVillages_Valides.append(vlg)
                        liste_VlgPossibles   .remove(vlg)
                        
                        await fDis.channelHistorique.send(f"Boucle - Validation de {vlg}, car c'est le seul village o?? {grp} est pr??sent.")
        
        
        
        
        
# S??lection d'un autre village (au hasard) 
        
        vlg_choisi = rd.choice(liste_VlgPossibles)
        
        await fDis.channelHistorique.send(f"Boucle - S??lection de {vlg_choisi} au hasard parmis la liste des villages possibles.")
        
        listeVillages_Valides.append(vlg_choisi)
        
        del(liste_VlgPossibles)
        
        
        
        suppressionVlg_identiques( listeVillages_Valides )
        
        listeGroupes_nonValides = [ grp   for grp in listeGroupes_nonValides   if not verif_personneGrpDansVillage(listeVillages_Valides, grp) ]
        
        
        
        
        
# Cas o?? le rassemblement de tous les groupes non valid??s forme un village trop petit 
        
        if nbHabitant( tuple(listeGroupes_nonValides) ) < nbHab_parVlg_Min :
            
            listeVillages_Valides.append(tuple(listeGroupes_nonValides))
            listeGroupes_nonValides = []
            
            await fDis.channelHistorique.send(f"Boucle - Ajout d'un village constitu?? des groupes non valid??s\n> {listeVillages_Valides[-1]}")
    
    
    
    
    
# %%% Gestion des personnes sans groupes
    
# Transformation des villages valid??s en liste d'habitants
    
    liste_VlgValides_Habs = []
    
    for vlg in listeVillages_Valides:
        liste_VlgValides_Habs.append( habitants(vlg) )
    
    
    
# Listage des joueurs restants
    
    listeJoueursRestants = list(fHab.TousLesHabitants)
    
    for hab_vlg in liste_VlgValides_Habs :
        
        for hab in hab_vlg :
            
            try    : listeJoueursRestants.remove(hab)
            except : await fDis.channelHistorique.send(f"ERREUR - Cette personne a d??j?? ??t?? supprimm?? : {hab.member.display_name} ({hab_vlg})")
    
    
# Cas ou aucun village n'a ??t?? cr??er 

    
    
    
#### Cr??ation d'un village contenant tous les joueurs restants (si possible)
    
    if len(listeJoueursRestants) in range(nbHab_parVlg_Min, nbHab_parVlg_Max + 1) :
        
        liste_VlgValides_Habs.append(tuple(listeJoueursRestants))
        listeJoueursRestants = []
        
        await fDis.channelHistorique.send(f"Ajout d'un village constitu?? des joueurs restants\n> {liste_VlgValides_Habs[-1]}")
    
    
    
#### Si c'est impossible, ajout des joueurs restants aux villages les moins peupl??s
    
    else :

        for hab in listeJoueursRestants :
            
# Recherche du village le moins peupl??
            
            hab_vlg_moins_peuple = liste_VlgValides_Habs[0]
            
            for hab_vlg in liste_VlgValides_Habs :
                
                if len(hab_vlg) < len(hab_vlg_moins_peuple) :
                    hab_vlg_moins_peuple = hab_vlg
            
            
            index_vlg_moins_peuple = liste_VlgValides_Habs.index( hab_vlg_moins_peuple )
            
            
            
# Ajout de la personne au village le moins peupl??

            liste_VlgValides_Habs[index_vlg_moins_peuple].append(hab)
    
    
    
    
    
# %%% Cr??ation des villages
    
# Envoie de la liste des villages d??finitifs

    msgLogs  = "_ _\n\n\n ` Voici la liste des villages d??finitive : `\n"
    
    for i in range(len(liste_VlgValides_Habs)) :
        
        vlg = liste_VlgValides_Habs[i]
        
        msgLogs += f"\n> n??{i}    [{ len(vlg) }]   - (   "
        
        for joueur in vlg :
            msgLogs += f"{joueur.member.display_name}   ,   "
            
        msgLogs += ")"
    
    await fDis.envoieMsg( fDis.channelHistorique, msgLogs )
    
    await asyncio.sleep(1)
    
    
    
#### Association des habitants ?? leur village
    
    donneeJoueur = fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs)
    
    
    for i in range(len(liste_VlgValides_Habs)) :
        
        vlg = liste_VlgValides_Habs[i]
        
        for hab in vlg :
            ligne, numLigne = fGoo.ligne_avec( hab.member.id, fGoo.clef_idDiscord, donneeJoueur )
            
            fGoo.remplacerVal_ligne( i+1                   , fGoo.clef_numVillage, 
                                     numLigne              , 
                                     fGoo.page1_InfoJoueurs                       )
        
            await asyncio.sleep(0.1)
    
    
    
async def creationVillages (nbVlg) :
    
#### Cr??ation des villages

    await fHab.redef_TousLesHabitants()
    
    for i in range(nbVlg) :
    
        await fVlg.creationVillage( numNouvVillage = i+1 )
        await asyncio.sleep(0.5)





# %% Distribution des r??les

async def distributionRole(village):
    
#### Paquet des R??les
    
    paquetRoles  = []
    
    paquetRoles.extend( v.prop_Villag        *[fRol.role_Villageois   ] )
    paquetRoles.extend( v.prop_VillaVilla    *[fRol.role_VillaVilla   ] )
    paquetRoles.extend( v.prop_Cupido        *[fRol.role_Cupidon      ] )
    paquetRoles.extend( v.prop_Ancien        *[fRol.role_Ancien       ] )
    
    paquetRoles.extend( v.prop_Salvat        *[fRol.role_Salvateur    ] )
    paquetRoles.extend( v.prop_Sorcie        *[fRol.role_Sorciere     ] )
    paquetRoles.extend( v.prop_Voyant        *[fRol.role_Voyante      ] )
    paquetRoles.extend( v.prop_Voyante_dAura *[fRol.role_Voyante_dAura] )
    
    paquetRoles.extend( v.prop_Corbea        *[fRol.role_Corbeau      ] )
    paquetRoles.extend( v.prop_Hirond        *[fRol.role_Hirondelle   ] )
    paquetRoles.extend( v.prop_Juge          *[fRol.role_Juge         ] )
    
    paquetRoles.extend( v.prop_Famill        *[fRol.role_FamilleNb    ] )
    
    
    
    paquetRoles.extend( v.prop_LG            *[fRol.role_LG           ] )
    paquetRoles.extend( v.prop_LGNoir        *[fRol.role_LGNoir       ] )
    paquetRoles.extend( v.prop_LGBleu        *[fRol.role_LGBleu       ] )
    paquetRoles.extend( v.prop_Traitre       *[fRol.role_Traitre      ] )
    
    paquetRoles.extend( v.prop_LGBlan        *[fRol.role_LGBlanc      ] )
    paquetRoles.extend( v.prop_EnSauv        *[fRol.role_EnfantSauv   ] )
    
    
    
#### Paquet des R??les Restants
    
    paquetRoles_Restant = list(paquetRoles)
    
    rd.shuffle(paquetRoles_Restant)
    


#### --- Distribution des R??les ---
    
    donnee = fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs)

    for hab in village.habitants :
        
        if len(paquetRoles_Restant) != 0 :
            habRole = paquetRoles_Restant.pop(0)
            
        else :
            habRole = rd.choice(paquetRoles)
        
        
        
#### Caract??ristiques des R??les
        
        caractRole = ""

        if   habRole == fRol.role_Ancien   : caractRole =    v.Ancien_nbProtec
        elif habRole == fRol.role_Sorciere : caractRole = f"{v.Sorcie_nbPotVie} {v.Sorcie_nbPotMort}"
        elif habRole == fRol.role_Juge     : caractRole =    v.Juge_nbExil
        elif habRole == fRol.role_LGNoir   : caractRole =    v.LGNoir_nbInfect
        
        
        
#### Enregistrement
        
        ligne, numLigne = fGoo.ligne_avec( hab.matricule, fGoo.clef_Matricule, donnee )
        
        fGoo.remplacerVal_ligne( habRole[fRol.clefNom], fGoo.clef_Role       , numLigne, fGoo.page1_InfoJoueurs)
        fGoo.remplacerVal_ligne( caractRole           , fGoo.clef_caractRoles, numLigne, fGoo.page1_InfoJoueurs)
        
        await asyncio.sleep(0.2)
        
        
        
#### Envoie du R??le
        
        await hab.member.send( f"Vous ??tes **{habRole[fRol.clefNom]}** :" )
        await hab.member.send( embed = habRole[fRol.clefEmbed]            )





# %% Commandes

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DebutPartie (ctx):
    
#### DP_1
    
    await DP_1 (ctx)
    
    
    
#### DP_2
    
    await DP_2 (ctx)
    
    
    
#### DP_3
    
    await DP_3 (ctx)



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_1 (ctx):
    """
    Mise ?? Jour du topic du channelHistorique.
    
    Num??ration des joueurs en fonctions de (dans l'ordre) :
        - Leur groupe
        - Leur pseudo
    """
    
    await fDis.channelHistorique.edit(topic = v.phase2)
    
    #await finInscription()
    
    await numerotationHabitants()





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_2 (ctx):
    """
    R??partitions des Joueurs dans diff??rents Villages 
    
    Ces villages sont cr????s pour r??partir le mieux possible les groupes sans les s??parer.
    Cette fonction est tr??s complexe et ?? de grand risque de bug??, 
        c'est d'ailleurs pour ??a que la grande commande DebutPartie a ??t?? s??par??e en trois.
    """
    
    await repartitionGroupes_Villages()
    
    
    
    
    
@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def creationVlgs (ctx, nbVlg):
    
    await creationVillages(int(nbVlg))





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_3 (ctx):
    """
    Fin de la fonction de 
    
    Mise ?? Jour du topic du channelHistorique, pour compter les tour au fil de la partie.
    """
    
#### Distribution des r??les
    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()    
    
    for vlg in fVlg.TousLesVillages :
        await distributionRole(vlg)
        await asyncio.sleep(1)
    
    
    
#### Envoie des premiers rapports municipaux
    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
    
    
    
#### Mise ?? Jour du topic du channelHistorique, pour compter les tours au fil de la partie.
    
    v.nbTours = 0
    await fDis.channelHistorique.edit(topic = f"{v.phase3} - Tour n??{v.nbTours}")
    
    

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def DP_4 (ctx):

#### Gestions des permitions d'acc??s aux salons des Loups-Garous et celui de la Famille Nombreuse
    
    message_invitation_LG = "Vous ??tes Loups-Garous, vous pouvez donc rejoindre leur serveur avec ce lien :\n"
    message_invitation_FN = "Vous ??tes un membre de la Famille Nombreuse, vous pouvez donc rejoindre le serveur familiale avec ce lien :\n"

    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()  

    for hab in fHab.TousLesHabitants :
        verifLG_Camp =  hab.role[fRol.clefCamp] == fRol.campLG
        verif_LGBlan =  hab.role == fRol.role_LGBlanc
        
        if   verifLG_Camp or verif_LGBlan :
            await fDis.invitation_MegaLG_LG(hab.user, message_invitation_LG)
            
        elif hab.role == fRol.role_FamilleNb :
            await fDis.invitation_MegaLG_FN(hab.user, message_invitation_FN)
        
        """
        if verifLG_Camp or verif_LGBlan :
            await fDis.serveurMegaLG_LG.unban(hab.user)
        
        elif hab.role == fRol.role_FamilleNb :
            await fDis.serveurMegaLG_FN.unban(hab.user)
        """
    
    
#### Attente avant le lancement de la premi??re nuit
    
    await fP3.attente_lancementTour()