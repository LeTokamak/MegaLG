 # -*- coding: utf-8 -*-

"""
Créé par Clément Campana

######################################################################################
######################################################################################
#############                                                            #############
#############               Méga Loups-Garous sur Discord                #############
#############                                                            #############
######################################################################################
######################################################################################

Version Delta                             δ1                                28/04/2021

"""

version = "δ1"

from MegaLG_eventsCommandes import (
    
# Events
    on_member_join     , on_member_remove   ,
    event_reactions    , event_messages     ,
                                    
# Commandes
    Nettoyage          , nettoyage          , Net               , net         , N        , n,
    Creation_SousGroupe, creation_sousgroupe, CreationSousGroupe, creationSGrp, creatSGrp, csg,
                                    
    ResetRolesDiscord  , ResetMatricules,
    Meutre             , Sauvetage          , Rapport_TousLesVillages, Amoureux    , #AmoureuxAlea,
                                    
# Niveau E / C
    fTou, fIns )


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


print("COUCOU")

# %% on_ready

@fDis.bot.event
async def on_ready():
    
    fDis.def_cstsMegaLG()
    
    
#### Recherche de la phase en cours
    
    v.phaseEnCours = v.phase0
    
    phaseTrouvee = False
    
    async for message in fDis.channelHistorique.history(limit = 10**9):
        
        if "```Phase " in message.content  and  not phaseTrouvee :
            v.phaseEnCours = message.content
            phaseTrouvee = True
    
    await fDis.channelHistorique.send(f"```⬢ -  Je suis connecté ! ({version} | {v.phaseEnCours[3:-3]})  - ⬢```\n{v.maintenant()}")
    
    
#### Redéfinition Groupes et Villages
    
    await fGrp.redef_groupesExistants()
    await fVlg.redef_villagesExistants()
    
    
#### Lancement des events 
    
    asyncio.Task(event_reactions())
    asyncio.Task(event_messages() )
    
    
#### Lancement des attendes d'épitaphe
    
    async for message in fDis.channelAttente.history(limit = 10**9):
        
        if fDis.Emo_Red == message.content.split()[0] :
            asyncio.Task( fHab.cimetiere(message = message, rappelDeFonction = True) )
    
    
#### Phase 3 - Récupération du numéro de Tour
    
    if v.phaseEnCours == v.phase3 :
        # Le topic de channelHistorique est de la forme "Tour n°45"
        
        v.nbTours = int(fDis.channelHistorique.topic[7: ])
    
    
#### Phase 3 - Lancement du Tour
    
    if v.phaseEnCours == v.phase3 :
        await attente_lancementTour()





# %% Phase 1

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Inscription (ctx):
    await lancementInscriptions()



async def lancementInscriptions():

    v.phaseEnCours = v.phase1
    await fDis.channelHistorique.send(v.phaseEnCours)
    
#### Gestions des permissions
    
    await fDis.channelAccueil.set_permissions(fDis.roleSpectateur, read_messages = True, send_messages = True)
    
    
#### Message de Ré-Inscription
    
    msgReInscription = await fDis.channelAccueil.fetch_message(fIns.idMessage_ReInscription)
    await msgReInscription.clear_reactions()
    await msgReInscription.add_reaction(fDis.Emo_BabyOrange)
    
    
#### Nettoyage de Infos Joueurs






# %% Phase 2

"""

################################################################################
#####                                                                      #####
#####                           - Paquet Roles -                           #####
#####                                                                      #####
################################################################################


### Création de paquetRoles, le paquet qui sera mélanger puis qui sera distribué aux joueurs

paquetRoles  = list(fRol.paquetRoles_Initial)

rd.shuffle(paquetRoles)




################################################################################
#####                                                                      #####
#####                      - Distribution des Rôles -                      #####
#####                                                                      #####
################################################################################


@fDis.bot.command()
@commands.has_permissions(ban_members = True)
async def Distrib (ctx):    
    
### Efface le !Distrib
    await fDis.effacerMsg(ctx)
        
    
# ----------------------------------------------
# --- Numérotation et distribution des rôles ---
# ----------------------------------------------
    
    Joueurs   = pd.DataFrame(fGoo.page1_InfoJoueurs.get_all_records())
    
    Ville   = []
    Annee   = []
    Filiere = []
    Comu    = []
    
    for j in Joueurs["Groupe"] :
        
        if j[:4] == "ISEN":
            Ville  .append(j[  -1])
            Annee  .append(j[  -3])
            Filiere.append(j[5:-4])
            Comu   .append("ISEN")
        
        else :
            Ville  .append("None")
            Annee  .append("None")
            Filiere.append("None")
            
            if   j != "Autre" :
                Comu   .append(j)
            else :
                Comu   .append("ZZZZZZZZ")
            
    
    Joueurs["Ville"]   = Ville
    Joueurs["Année"]   = Annee
    Joueurs["Filière"] = Filiere
    Joueurs["Comu"]    = Comu
    
### Rangement des joueurs par Ville, Année, Filière, Nom et enfin par Prénom

    JouRanges = Joueurs.sort_values(by = ["Comu", "Ville", "Année", "Filière", "Nom", "Prénom"])

    
### Numérotation et distribution des rôles    

    JouRanges["Mat"]  = range(1, len(JouRanges) + 1)
    JouRanges["Role"] = paquetRoles
    
    JouReduit = JouRanges.drop(["Ville", "Année", "Filière", "Comu"], axis = 1)
    
    JouTerm   = fGoo.dfToList(JouReduit)

    
### Caractéristiques des Rôles

    for num in range(1, len(JouRanges) + 1) :
        role = JouTerm[num][7]
        
        if   role == fRol.info_Ancien["nom"] : JouTerm[num][8] =    c.Ancien_nbProtec
        elif role == fRol.info_Sorcie["nom"] : JouTerm[num][8] = f"{c.Sorcie_nbPotVie} {c.Sorcie_nbPotMort}"
        elif role == fRol.info_LGNoir["nom"] : JouTerm[num][8] =    c.LGNoir_nbInfect


### Réécriture de Infos Joueurs et Sauvegarde

    fGoo.page1_InfoJoueurs.clear()
    fGoo.page1_InfoJoueurs.insert_rows(fGoo.strListe(JouTerm))
    
    fGoo.page1_Sauvegarde .clear()
    fGoo.page1_Sauvegarde .insert_rows(fGoo.strListe(JouTerm))
    
    
    
# ----------------------------------------------------
# --- Envoie des rôles et modification des pseudos ---
# ----------------------------------------------------

    for j in JouTerm[1:] :
        
#   j = [23, H, Clément, Campana, ISEN CSI 2 N, 269051521272905728, , "Loup-Garou", '', , '']
                
        membJou = fDis.serveurMegaLG.get_member(int(j[5]))
        
        await membJou.send(f"Vous êtes **{j[7]}** :")
        await membJou.send(embed = fRol.Role_avec(j[7])["embeds"])
        
        surnom  = membJou.display_name
        
        while len(surnom) > 26 :
            surnom = surnom[:-1]
        
        await membJou.edit(nick = f"{fMeP.AjoutZerosAvant(j[0],3)} | {surnom}")
    
    
    
# ---------------------------
# --- Rapports municipaux ---
# ---------------------------
    
    villePrec = ""
    anneePrec = ""
    filiePrec = ""
    groupPrec = ""
    
    msgJoueurs = await channelRapport.send("Recencement de début de Partie :\n\n\n\n")
    
    for j in dfToList(JouRanges)[1:] :
        
#   j = [23, H, Clément, Campana, ISEN CSI 2 N, 269051521272905728, , "Loup-Garou", '', , '', 'N', '2', 'CSI', 'ISEN']
#        0   1     2        3           4                5         6       7        8  9  10  11   12    13      14

        if groupPrec != j[14]:
            prefixe = "\n\n\n"
            if j[14] == "ISEN" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe +  "__**⬢⬢⬢⬢⬢   ISEN   ⬢⬢⬢⬢⬢**__")
            else               : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + f"__**⬢⬢⬢⬢⬢   {j[4]}   ⬢⬢⬢⬢⬢**__")
            villePrec = ""
            anneePrec = ""
            filiePrec = ""
        
        if j[14] == "ISEN" :
            if villePrec != j[11] :
                prefixe = ""
                if villePrec != "" : prefixe = "\n"
                if j[11] == "B" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   BREST   - ⬢⬢⬢**")
                if j[11] == "C" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   CAEN   - ⬢⬢⬢**")
                if j[11] == "N" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   NANTES   - ⬢⬢⬢**")
                if j[11] == "R" : msgJoueurs = await ajoutMsg(msgJoueurs, prefixe + "\n> **⬢⬢⬢ -   RENNES   - ⬢⬢⬢**")
                anneePrec = ""
                filiePrec = ""
            
            if anneePrec != j[12] :
                if j[12] == "1" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 1ère Année ---")
                if j[12] == "2" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 2ème Année ---")
                if j[12] == "3" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 3ème Année ---")
                if j[12] == "4" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 4ème Année ---")
                if j[12] == "5" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- 5ème Année ---")
                if j[12] == "P" : msgJoueurs = await ajoutMsg(msgJoueurs, "\n> \n> --- Profs ---")
                filiePrec = ""
                
            if filiePrec != j[13]  and  j[13] != "M"  and  j[12] != "P" :
                msgJoueurs = await ajoutMsg(msgJoueurs, f"\n> {j[13]}")
            
        villePrec = j[11]
        anneePrec = j[12]
        filiePrec = j[13]
        groupPrec = j[14]
        
        membJou = serveurMegaLG.get_member(int(j[5]))
        
        msgJoueurs = await ajoutMsg(msgJoueurs, f"\n>       ⬢ {membJou.mention} - {j[2]} {j[3]}")


"""



# %% Phase 3

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Tour(ctx):
        
    await fDis.effacerMsg(ctx)
    await fTou.Tour()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Lancement(ctx):
    
    await fDis.effacerMsg(ctx)
    await attente_lancementTour()



async def attente_lancementTour() :
        
    m = v.maintenant()

#### ||| Variable ||| Si on est dans le WE on ne lance pas la fonction Tour

    if not v.partiePdt_Weekend  and  m.weekday() in (4,5) :
        await fDis.channelHistorique.send("Nous somme Vendredi ou Samedi, la fonction Lancement à été stoppée dans son élan !")
        return None
    
#### Attente qu'il soit 18h pour lancer la fontion Tour    

    tempsAtt = v.nuit_hDeb - m
                
    await fDis.channelHistorique.send(f"Attente de {tempsAtt} avant de lancer la nuit n°{v.nbTours}")
    
    if tempsAtt > v.timedelta(0) :
        await asyncio.sleep(tempsAtt.seconds)
    
    await fTou.Tour()



#fDis.bot.run(fDis.tokenMJ)