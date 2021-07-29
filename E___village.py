# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---             Niveau E - Classe et Fonctions de Gestion des Villages             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


# Niveau D
import D___fcts_nocturnes       as fNct

# Niveau C
fHab    = fNct.fHab

# Niveau B
fRol    = fHab.fRol

# Niveau A
fGoo    = fHab.fGoo
fDis    = fHab.fDis
fMeP    = fHab.fMeP
v       = fHab.v


rd      = fHab.rd
asyncio = fHab.asyncio


scrutin_ElectionMaire = "Election d'un nouveau maire"
scrutin_En1Tour       = "Vote en 1 Tour"
scrutin_En2Tour_1erT  = "Vote en 2 Tours - 1er Tour"
scrutin_En2Tour_2emT  = "Vote en 2 Tours - 2ème Tour"





class Village :
    
    def __init__ (self, numVillage, nom):

        self.numero         = numVillage
        self.nom            = nom
        
        self.habitants      = []
        self.maire          = None
        
        
        
#### Constantes Discord
        
        self.roleDiscord    = None
        self.roleDiscordMort= None
        
        self.categorie      = None
        
        self.salonRapport   = None
        self.salonCimetiere = None
        self.salonBucher    = None
        self.salonDebat     = None
        self.vocalDebat     = None
        
        self.salonVoteLG    = None
        self.salonConseilLG = None
        self.vocalConseilLG = None
        
        self.salonFamilleNb = None
        self.vocalFamilleNb = None
        
        
        
#### Variables Nocturnes
        
        self.voteLG_EnCours                = False
        self.matriculeHab_choixConseilLG   = 0
        self.msgResultatLG                 = None
        
        self.matriculeLGN_quiOntInfecte    = []
        self.matriculeHab_tuesLGBlanc      = []
        
        self.matriculeHab_protegeSalvat    = []
        
        self.matriculeSorciere_sauveuse    = []
        self.matriculeSorciere_tueuses     = []
        self.matriculeHab_tuesSorciere     = []
        
        self.matricule_choixCorbeaux       = []
        self.matricule_choixHirondelles    = []
        
        self.matriculeHab_vraimentTues     = []
        
        
        
#### Variables Diurnes
        
        self.votesEnPlus          = []
        self.typeScrutin          = None
        
        self.resultatVote         = []
        
        self.exilOrdonne          = False
        self.exilOrdonne_parMaire = False
        self.juges_OrdonantExil   = []
    
    
    
    
    
    def depouillement(self, typeDeSuffrage = None):
        """
        La fonction depouillement va :
              - Les trier, les compter et ranger par ordre croissant les résultats
              - Construire un message pour envoyer les résultats
              
        Elle prend le paramettre typeDeSuffrage, qui peut valoir 
            scrutin_ElectionMaire,
            scrutin_En1Tour      ,
            scrutin_En2Tour_1erT ,
            scrutin_En2Tour_2emT ou
            'LG'
        """
        
        symbolesVote = "⬢"
        
#### Type de Suffrage
        
        if typeDeSuffrage == None :
            typeDeSuffrage = self.typeScrutin
        
        
        
#### Rassemblement de tout les votes
        
        if typeDeSuffrage == "LG" :
            votes = self.recolteBulletins(nbVoteParHab_egal_1 = True)
        else : 
            votes = self.recolteBulletins()
        
# --- votes = [1, 2, 2, 4, 5, 4, 4, 1, 2, 4, 2, 1, 1, 5, 4, 2, 4, 2, 4, 5, 4, 3, 1, 5, 2, 4, 4]
        
        votes.sort()
        
# --- votes = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]
        
        
#### Nettoyages des votes (exclusion des 0, des personnes n'étant pas dans le village et des personnes non accusées)
        
        votes     = [ v   for v in votes   if v != 0                                         ]
        votes     = [ v   for v in votes   if fHab.habitant_avec(v).numVlg == self.numero ]
        
        if typeDeSuffrage == scrutin_En2Tour_2emT :
            votes = [ v   for v in votes   if fHab.habitant_avec(v) in self.accuses       ]
    
        
        
        nbSuffrages = len(votes)
        
# =============================================================================
#### --- Cas 1 : Si personne n'a voté ---
# =============================================================================
    
        if nbSuffrages == 0 :
            msgResultat    = "```Personne n'a voté```"
            resultatsTries = []
        
        
        
# =============================================================================
#### --- Cas 2 : S'il y a des voix à comptabiliser ---
# =============================================================================
        
        else :
            
#### Comptage des votes, création de la variable resultats
            
            resultats = [ [votes[0], votes.count(votes[0])] ]
            
            for v in votes :
        
##  Si l'on n'a pas déjà compté le nombre de voix que cette personne a reçu, alors on le compte
        
                if resultats[-1][0] != v:
                    resultats.append( [v, votes.count(v)] )
        
# --- resultats = [ [1,5] , [2,7] , [3,1] , [4,10] , [5,4] ]
            
            
            
            
            
#### Rangement des resultats (1er, 2eme, 3eme...)
            
            resultatsTries = []
            
            while len(resultats) > 0 :
                maxReslt = resultats[0]
                
                for i in resultats[1:] :
                    if i[1] > maxReslt[1] :
                        maxReslt = i
                
                resultatsTries.append(maxReslt)
                resultats.remove(maxReslt)
                
# --- resultatsTries = [  [4,10] , [2,7] , [1,5] , [5,4] , [3,1]  ]
            
            
            
            
            
#### Ecriture du message décrivant les résultats
            
### Gestion du vote des LG
            
            debutMsgResultat = ""
            
            if typeDeSuffrage == "LG":
                
##  Verif si Egalité entre 1er et 2eme, alors personne n'est désigné 
                
                if len(resultatsTries) > 1  and  resultatsTries[0][1] == resultatsTries[1][1] :
                    self.matriculeHab_choixConseilLG =  0
                    debutMsgResultat                    =  "Personne n'est designée par le conseil ! (égalité)\n" 
                
                else :
                    self.matriculeHab_choixConseilLG =  resultatsTries[0][0]
                    persChoisie                         =  fHab.habitant_avec(self.matriculeHab_choixConseilLG)
                    debutMsgResultat                    = f"**{persChoisie.prenom} {persChoisie.nom}** ({persChoisie.groupe}) est la victime designée par le conseil !\n" 
            
            
### Message de présentation des résultats
    
            msgResultat = debutMsgResultat + "```py\n"
            
            valHexag = resultatsTries[0][1] // 30 + 1
            
            for p in resultatsTries :
                msgResultat += f"{fMeP.AjoutZerosAvant(p[0], 3)} {fMeP.AjoutZerosAvant(p[1], 3, espace = True)} / {nbSuffrages}   "
                msgResultat +=  (round(p[1]/valHexag) // 10)  *  (10*symbolesVote + " ")
                msgResultat +=  (round(p[1]/valHexag) %  10)  *      symbolesVote
                msgResultat +=  "\n"
            
            msgResultat += "```"
            
            
            
        return msgResultat, resultatsTries
    
    
    
# %% Salons et rôles discords
    
    async def creation_roleEtSalons (self):
        
# =============================================================================
#### Création du Role du Village
# =============================================================================
        
        self.roleDiscord     = await fDis.serveurMegaLG.create_role( name        = self.nom,
                                                                     permissions = fDis.roleJoueurs.permissions,
                                                                     colour      = fDis.roleJoueurs.colour,
                                                                     hoist       = True,
                                                                     mentionable = True,
                                                                     reason      = f"Role discord du Village {self.nom} - n°{self.numero}" )
        
        self.roleDiscordMort = await fDis.serveurMegaLG.create_role( name        = self.nom,
                                                                     permissions = fDis.roleMorts.permissions,
                                                                     colour      = fDis.roleMorts.colour,
                                                                     mentionable = True,
                                                                     reason      = f"Role discord du Village {self.nom} - n°{self.numero}" )
        
        for hab in fHab.TousLesHabitants :
            if hab.numVlg == self.numero :
                await hab.member.add_roles( self.roleDiscord )
        

# =============================================================================
#### Création de la Catégorie du Village
# =============================================================================

        self.categorie = await fDis.serveurMegaLG.create_category( name = f"⬢ - {self.nom} - ⬢" , position = fDis.CategoryChannel_GestionGrp.position + 1 )
        
        
# =============================================================================
#### Création des Salons du Village
# =============================================================================

        self.salonRapport   = await self.categorie.create_text_channel ( "📋┃rapport-municipal"   , topic = f"Rapport Municipal {fMeP.de_dApostrophe(self.nom)}"              )
        self.salonCimetiere = await self.categorie.create_text_channel ( "💀┃cimetière"           , topic = f"Cimetière {fMeP.de_dApostrophe(self.nom)}"                      )
        self.salonBucher    = await self.categorie.create_text_channel ( "🔥┃bûcher"              , topic = f"Salon de Vote {fMeP.de_dApostrophe(self.nom)}"                  )
        self.salonDebat     = await self.categorie.create_text_channel ( "🔪┃débats"              , topic = f"Salon de Débat {fMeP.de_dApostrophe(self.nom)}"                 )
        self.vocalDebat     = await self.categorie.create_voice_channel( "📢┃débats"                                                                                          )
        
        self.salonVoteLG    = await self.categorie.create_text_channel ( "🐺┃votes-du-conseil"    , topic = f"Salon de Vote des Loups-Garous {fMeP.de_dApostrophe(self.nom)}" )
        self.salonConseilLG = await self.categorie.create_text_channel ( "🐺┃meute"               , topic = f"Débats entre les Loups-Garous {fMeP.de_dApostrophe(self.nom)}"  )
        self.vocalConseilLG = await self.categorie.create_voice_channel( "🐺┃meute"                                                                                           )
        
        self.salonFamilleNb = await self.categorie.create_text_channel ( "🏡┃la-maison-familiale" , topic = f"Maison familiale {fMeP.de_dApostrophe(self.nom)}"               )
        self.vocalFamilleNb = await self.categorie.create_voice_channel( "🏡┃les débats familiaux"                                                                            )



### Gestion des permissions des salons du village

        await self.salonRapport  .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonCimetiere.set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonBucher   .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonDebat    .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.vocalDebat    .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonVoteLG   .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonConseilLG.set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.vocalConseilLG.set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonFamilleNb.set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.vocalFamilleNb.set_permissions( fDis.roleEveryone   , read_messages = False )
        
        
        await self.salonRapport  .set_permissions( self.roleDiscord    , read_messages = True , send_messages = False )
        await self.salonBucher   .set_permissions( self.roleDiscord    , read_messages = True , send_messages = False )
        await self.salonCimetiere.set_permissions( self.roleDiscord    , read_messages = True , send_messages = False )
        await self.salonDebat    .set_permissions( self.roleDiscord    , read_messages = True , send_messages = True  )
        await self.vocalDebat    .set_permissions( self.roleDiscord    , read_messages = True                         )
        
        
        await self.salonRapport  .set_permissions( self.roleDiscordMort, read_messages = True , send_messages = False )
        await self.salonBucher   .set_permissions( self.roleDiscordMort, read_messages = True , send_messages = False )
        await self.salonCimetiere.set_permissions( self.roleDiscordMort, read_messages = True , send_messages = False )
        await self.salonDebat    .set_permissions( self.roleDiscordMort, read_messages = True , send_messages = False )
        await self.vocalDebat    .set_permissions( self.roleDiscordMort, read_messages = False                        )
        
        
        
# =============================================================================
#### Enregistrement des modifications
# =============================================================================
        
        self.ecriture_GoogleSheet()
    
    
    
    
    
    def ecriture_GoogleSheet(self):
        
# =============================================================================
#### Création du dictionnaire correspondant à la ligne du Village
# =============================================================================
        
        ligneVillage = {fGoo.clefVlg_numVillage : self.numero,
                        fGoo.clefVlg_Nom        : self.nom    }

        if v.phaseEnCours in (v.phase2, v.phase3) :
            ligneVillage[fGoo.clefVlg_idRoleDiscord         ] = self.roleDiscord    .id
            ligneVillage[fGoo.clefVlg_idRoleDiscord_Mort    ] = self.roleDiscordMort.id
            
            ligneVillage[fGoo.clefVlg_idSalon_Rapport       ] = self.salonRapport  .id
            ligneVillage[fGoo.clefVlg_idSalon_Bucher        ] = self.salonBucher   .id
            ligneVillage[fGoo.clefVlg_idSalon_Cimetiere     ] = self.salonCimetiere.id
            ligneVillage[fGoo.clefVlg_idSalon_Debat         ] = self.salonDebat    .id
            ligneVillage[fGoo.clefVlg_idSalon_vocDebat      ] = self.vocalDebat    .id
            
            ligneVillage[fGoo.clefVlg_idSalon_VoteLG        ] = self.salonVoteLG   .id
            ligneVillage[fGoo.clefVlg_idSalon_DebatLG       ] = self.salonConseilLG.id
            ligneVillage[fGoo.clefVlg_idSalon_vocDebatLG    ] = self.vocalConseilLG.id
            
            ligneVillage[fGoo.clefVlg_idSalon_FamilleNomb   ] = self.salonFamilleNb.id
            ligneVillage[fGoo.clefVlg_idSalon_vocFamilleNomb] = self.vocalFamilleNb.id
        
        
# =============================================================================
#### Recherche du numéro de ligne et remplacement de celle-ci
# =============================================================================
        
        igne, numeroLigne = fGoo.ligne_avec(self.numero,
                                            fGoo.clefVlg_numVillage,
                                            fGoo.donneeGoogleSheet(fGoo.page_Villages))
        
        fGoo.remplacerLigne(ligneVillage, numeroLigne, fGoo.page_Villages)
    
    
    
    
    
    async def changementNom (self, nouveauNom):
        
        self.nom = nouveauNom
        
# =============================================================================
#### Modification du nom du Role du Village
# =============================================================================
        
        await self.roleDiscord    .edit( name   = self.nom, 
                                         reason = f"Changement de nom du Village n°{self.numero}, qui devient **{self.nom}**" )
        
        await self.roleDiscordMort.edit( name   = self.nom, 
                                         reason = f"Changement de nom du Village n°{self.numero}, qui devient **{self.nom}**" )
        
        
# =============================================================================
#### Modification du nom de la Catégorie du Village
# =============================================================================

        await self.categorie.edit ( name = f"⬢ - {self.nom} - ⬢" )
        
        
# =============================================================================
#### Modification des topics des Salons du Village
# =============================================================================
        
        async def editTopic(debutTopic, salon) :
            await salon.edit(topic = f"{debutTopic} {fMeP.de_dApostrophe(self.nom)}")
        
        
        
        await editTopic( "Rapport Municipal"                , self.salonRapport   )
        await editTopic( "Cimetière"                        , self.salonCimetiere )
        await editTopic( "Salon de Vote"                    , self.salonBucher    )
        await editTopic( "Salon de Débat"                   , self.salonDebat     )
        await editTopic( "Débats Vocaux"                    , self.vocalDebat     )
        
        await editTopic( "Salon de Vote des Loups-Garous"   , self.salonVoteLG    )
        await editTopic( "Débats entre les Loups-Garous"    , self.salonConseilLG )
        await editTopic( "Discussion entre les Loups-Garous", self.vocalConseilLG )
        
        await editTopic( "Maison familiale"                 , self.salonFamilleNb )
        await editTopic( "Réunion familiale"                , self.vocalFamilleNb )
        
        
        
# =============================================================================
#### Enregistrement de la modification
# =============================================================================
        
        fGoo.remplacerVal_ligne_avec( self.nom   , fGoo.clefVlg_Nom       ,
                                      self.numero, fGoo.clefVlg_numVillage,
                                      fGoo.page_Villages                    )
    
    
    
    
    
# %% Habitants
    
    def redef_habitants(self) :
        self.habitants = []
        
        for hab in fHab.TousLesHabitants :
            if hab.numVlg == self.numero :
                self.habitants.append(hab)
                
                if hab.estMaire :
                    self.maire = hab
                
    
    
    
    
    async def rapportMunicipal(self):
        
        m = v.maintenant()
        
        listeMsgJoueurs = [f"__**Rapport municipal**__\nRecencement de {fMeP.AjoutZerosAvant(m.hour,2)} : {fMeP.AjoutZerosAvant(m.minute,2)} :"]
        RolesRestants   = []
        
# =============================================================================
#### --- Recencement ---
# =============================================================================
        
        grpPrec_rang1, grpPrec_rang2, grpPrec_rang3, grpPrec_rang4 = (None, None, None, None)
        
        nbRolesInconnus = 0
        
        for hab in self.habitants :
    
#### Groupe de Rang 1
    
            if hab.groupe.rang >= 1   and   grpPrec_rang1 != hab.groupe.chemin[0] :
                
                listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, f"\n\n__**⬢⬢⬢⬢⬢   {hab.groupe.chemin[0]}   ⬢⬢⬢⬢⬢**__")
                grpPrec_rang2, grpPrec_rang3, grpPrec_rang4        = (None, None, None)
            
            
#### Groupe de Rang 2
            
            if hab.groupe.rang >= 2   and   grpPrec_rang2 != hab.groupe.chemin[1] :
                
                if grpPrec_rang2 == None : prefixe = "\n"
                else                     : prefixe = "\n"
                
                listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, prefixe + f"\n> **⬢⬢⬢ -   {hab.groupe.chemin[1]}   - ⬢⬢⬢**")
                grpPrec_rang3, grpPrec_rang4                       = (None, None)
            
            
#### Groupe de Rang 3
            
            if hab.groupe.rang >= 3   and   grpPrec_rang3 != hab.groupe.chemin[2] :
                
                if grpPrec_rang3 == None : prefixe = "\n> "
                else                     : prefixe = "\n> "
                
                listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, prefixe + f"\n> --- {hab.groupe.chemin[2]} ---")
                grpPrec_rang4                                      = (None)
            
            
#### Groupe de Rang 4
            
            if hab.groupe.rang == 4   and   grpPrec_rang4 != hab.groupe.chemin[3] :
                
                if grpPrec_rang4 == None : prefixe = ""
                else                     : prefixe = "\n> "
                
                listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, prefixe + f"\n> *{hab.groupe.chemin[3]}*")
            
            
            
            if   hab.groupe.rang == 0 : grpPrec_rang1, grpPrec_rang2, grpPrec_rang3, grpPrec_rang4 =                     [None, None, None, None]
            elif hab.groupe.rang == 1 : grpPrec_rang1, grpPrec_rang2, grpPrec_rang3, grpPrec_rang4 = hab.groupe.chemin + [None, None, None      ]
            elif hab.groupe.rang == 2 : grpPrec_rang1, grpPrec_rang2, grpPrec_rang3, grpPrec_rang4 = hab.groupe.chemin + [None, None            ]
            elif hab.groupe.rang == 3 : grpPrec_rang1, grpPrec_rang2, grpPrec_rang3, grpPrec_rang4 = hab.groupe.chemin + [None                  ]
            elif hab.groupe.rang == 4 : grpPrec_rang1, grpPrec_rang2, grpPrec_rang3, grpPrec_rang4 = hab.groupe.chemin
            
            if hab.role == fRol.role_VillaVilla : texteVilVil = fRol.role_VillaVilla[fRol.clefEmoji]
            else                                : texteVilVil = ":black_circle:"
            
            if hab.estMaire                     : texteMaire  = fDis.Emo_Maire
            else                                : texteMaire  = ":black_circle:"
            
            listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, f"\n>       ⬢  {texteVilVil} {texteMaire}  {hab.user.mention} - {hab.prenom} {hab.nom}")
            
#### Role
            if not hab.estUnExile :
                RolesRestants.append( fRol.emojiRole(hab.role, hab.estUnHomme) )
            else :
                nbRolesInconnus += 1
            
        listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs,f"\n\n\nIl reste encore **{len(RolesRestants)} joueurs** vivants.")
        
        await fDis.envoieListe(self.salonRapport, listeMsgJoueurs)
        
        
        
# =============================================================================
#### --- Rôles Restants ---
# =============================================================================
        
        msgNbRole = "_ _\n__**Rôles restants :**__"

#### Rôles Inconnus (des exilés)
        
        if   nbRolesInconnus != 0 :
            msgNbRole += f"\n`{nbRolesInconnus}` {fDis.Emo_RoleInconnu}\n\n"
        
#### = Listage des rôles =
        
        Emo_Roles = [[fRol.role_Villageois [fRol.clefEmoji], fRol.role_Cupidon    [fRol.clefEmoji], fRol.role_Ancien  [fRol.clefEmoji] ],
                     [fRol.role_Salvateur  [fRol.clefEmoji], fRol.role_Sorciere   [fRol.clefEmoji], fRol.role_Voyante [fRol.clefEmoji] ],
                     [fRol.role_Corbeau    [fRol.clefEmoji], fRol.role_Hirondelle [fRol.clefEmoji], fRol.role_Juge    [fRol.clefEmoji] ],
                 list(fRol.role_FamilleNb  [fRol.clefEmoji]                                                                            ),
                     [                                                                                                                 ],
                     [fRol.role_LG         [fRol.clefEmoji], fRol.role_LGNoir     [fRol.clefEmoji], fRol.role_LGBleu  [fRol.clefEmoji] ],
                     [fRol.role_LGBlanc    [fRol.clefEmoji], fRol.role_EnfantSauv [fRol.clefEmoji]                                     ] ]
        
        
        for ligneRole in Emo_Roles :
            
#### Retour à la ligne

            ligneVide = True
            
            for role in RolesRestants:
                ligneVide = ligneVide  and  not (role in ligneRole)
            
            if   not ligneVide :
                msgNbRole += "\n> "
                
            elif ligneRole == []:
                msgNbRole += "\n"
            
            for i in range(len(ligneRole)):
                
                if RolesRestants.count(ligneRole[i]) != 0 :
                    msgNbRole += f"`{RolesRestants.count(ligneRole[i])}` {ligneRole[i]}"
                    
                    somme_RolesRestants_finLigne = 0
                    
                    for emo_role in ligneRole[ i+1 : ] :
                        somme_RolesRestants_finLigne += RolesRestants.count(emo_role)
                        
                    if somme_RolesRestants_finLigne != 0 : 
                        msgNbRole += 10 * " "
        
        msgNbRole += "_ _"
        
        await self.salonRapport.send( msgNbRole )
    
    
    
    
    
# %% Exils et Dissolution
    
    async def dissolution(self) :
        

        if TousLesVillages == [self]:
            
            await self.salonBucher.send("Le village **aurait dû être dissous**, mais comme c'est le dernier restant, sa dissolution est **impossible** !")
        
        
        
        else :

#### Choix du village d'arrivé au hasard

            nouvVillage = self
            while nouvVillage == self :
                nouvVillage = rd.choice(TousLesVillages)
            
            
#### Exil de tous les habitants
            
            self.redef_habitants()
            
            for hab in self.habitants :
                if not hab.estMorte :
                    await exil_dans_nouvVillage(hab, nouvVillage, ancienVillage = self)
                    await asyncio.sleep(0.1)
            
            
#### Message dans le nouveau Village
            
            contenuMsg_AnnonceExil = f"**{self.nom}** a été détruit... {len(self.habitants)} habitants viennent d'arriver à {nouvVillage.nom} !"
            
            await nouvVillage.salonDebat.send(contenuMsg_AnnonceExil)
            
            
#### Suppresion du Référencement du Village
            
            fGoo.suppressionLigne_avec(self.numero, fGoo.clefVlg_numVillage, fGoo.page_Villages)
            
            TousLesVillages.remove(self)
            
            return nouvVillage
    
    
    
    async def gestion_mort_maire(self) :
        pass
    
    
    
    
    
# %% Nuit

    async def gestion_nuit(self) :
    
# =============================================================================
#### --- Gestion des Permissions ---
# =============================================================================

        await self.salonRapport.set_permissions( self.roleDiscord , read_messages = True  , send_messages = False )
        await self.salonBucher .set_permissions( self.roleDiscord , read_messages = True  , send_messages = False )
        await self.salonDebat  .set_permissions( self.roleDiscord , read_messages = True  , send_messages = False )
        await self.vocalDebat  .set_permissions( self.roleDiscord , read_messages = False                         ) 
        
        
        
# =============================================================================
#### --- Envoie des messages de début de nuit ---
# =============================================================================
        
# Historique
        
        self.msgHistoNuit = await fDis.channelHistorique .send(f"```Début de la Nuit {v.nbTours} - Village n°{self.numero} : {self.nom} - {fMeP.strDate(v.ajd)}```")
        
        
# Channel des Loups-Garous
        
        await self.salonVoteLG   .send(f"```Conseil des Loups-Garous n°{v.nbTours} - {fMeP.strDate(v.ajd)}```")
        await self.salonConseilLG.send(f"```Conseil des Loups-Garous n°{v.nbTours} - {fMeP.strDate(v.ajd)}```")
        
        self.msgResultatLG = await self.salonVoteLG.send("Personne n'a encore voté.")
        
        
        
# =============================================================================
#### --- Lancement des Fonctions Nocturnes ---
# =============================================================================
        
        for hab in self.habitants :
            asyncio.Task( hab.role[fRol.clefFctsNoct](hab, self) )
            
#### Accès au Conseil des Loups-Garous
            
            verifLG_Camp =  hab.role[fRol.clefCamp] == fRol.campLG
            verifLG_Infe =  hab.estInf
            verif_LGBlan =  hab.role == fRol.role_LGBlanc
            verif_EnfSau =  hab.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(hab.pereProtecteur) == None
            
            if verifLG_Camp  or  verifLG_Infe  or  verif_LGBlan  or  verif_EnfSau :
                asyncio.Task( Conseil_LG(hab, self) )
                
#### Nomination des gardes mayoraux
            
            if v.nbTours == 1  and  hab.estMaire :
                asyncio.Task( fNct.fctNoct_Maire(hab, self) )
            
            
            
# =============================================================================
#### --- Attente que la nuit se termine ---
# =============================================================================
    
        while v.maintenant() < v.nuit_hFin :
            await asyncio.sleep(1)





    async def application_nuit(self) :
        
        donneeInfosJoueurs = fGoo.donneeGoogleSheet( fGoo.page1_InfoJoueurs )
        msgResumNuit       = await fDis.channelHistorique.send(f"```Résumé de la Nuit {v.nbTours} - {self.nom} - {fMeP.strDate(v.ajd)}```")
        
# %%% Protection des Joueurs
    
# =============================================================================
#### --- Habitants protégés par les Salvateurs ---
# =============================================================================
    
        matriculeHab_proteges = list(self.matriculeHab_protegeSalvat)
        
        msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Les {fDis.Emo_Salvateur} ont protégé : {matriculeHab_proteges}.")

    
    
# =============================================================================
#### --- Habitants protégés par les Sorcières ---
# =============================================================================
    
### Si une sorcière a sauvé ET si aucun Loup Garou Noir n'a infecté
    
        if len(self.matriculeSorciere_sauveuse) != 0  and  len(self.matriculeLGN_quiOntInfecte) == 0 :
            
            matriculeHab_proteges.append(self.matriculeHab_choixConseilLG)
            
            
##  Choix au Hasard de la Sorcière qui sauve 
            
            matricule_SorciereChoisie = rd.choice(self.matriculeSorciere_sauveuse)
            
            
##  Modification de InfosJoueurs (moins une potion de Vie pour SorciereChoisie)
            
            ligne, num_ligne = fGoo.ligne_avec(matricule_SorciereChoisie, 
                                               fGoo.clef_Matricule      , 
                                               donneeInfosJoueurs        )
            
            nbPotionsVie, nbPotionsMort = ligne[fGoo.clef_caractRoles].split()       # 12 4 ==> 12 Potions de Vie et 4 Potions de Mort
            nvlCaractRoles_Sorciere     = f"{int(nbPotionsVie) - 1} {nbPotionsMort}"
            
            fGoo.remplacerVal_ligne( nvlCaractRoles_Sorciere, fGoo.clef_caractRoles,
                                     num_ligne                                     ,
                                     fGoo.page1_InfoJoueurs                         )
            
            
##  Message Historique de la Nuit
            
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> La {fDis.Emo_Sorciere} {matricule_SorciereChoisie} a sauvé : {self.matriculeHab_choixConseilLG} qui a été désigné par les LG.")
    
    
    
        msgResumNuit = await fDis.ajoutMsg(msgResumNuit,"\n> \n>  - ⬢⬢⬢ - ")
    
    
    
    
    
# %%% Conseil des Loups-Garous
           
# =============================================================================
#### --- Cas où un des Loups-Garous Noirs a infecté ---
# =============================================================================
        
        if   len(self.matriculeLGN_quiOntInfecte) != 0 :
    
#### Loup-Garou Noir        
    
##  Choix au Hasard du Loup-Garou Noir qui infecte
            
            matricule_LGNoir = rd.choice(self.matriculeLGN_quiOntInfecte)
    
    
##  Modification de InfosJoueurs (moins une infection pour le LGNoir)
    
            fGoo.ajoutVal_cellule_avec( -1                  , fGoo.clef_caractRoles ,
                                        matricule_LGNoir    , fGoo.clef_Matricule   ,
                                        fGoo.page1_InfoJoueurs                      ,
                                        typeObjetCellule = int                        )   
            
            
            
            
            
#### Personne Infecté
            
            habitantInfecte        = fHab.habitant_avec(self.matriculeHab_choixConseilLG)
            
            if habitantInfecte.estMaire :
                habitantInfecte = rd.choice(habitantInfecte.gardesMaire)
            
            habitantInfecte.estInf = True
            
##  Messages d'infections
            
            await habitantInfecte.user.send("Vous avez été infecté par un Loup-Garou Noir, vous rencontrerez vos nouveaux camarades ce soir !")
                
            if habitantInfecte.estUnHomme : e = ""
            else                          : e = "e"

            await self.salonConseilLG.send(f"{habitantInfecte.user.mention} vient d'être infecté{e} !")
                
                
##  Modification de InfosJoueurs
            
            fGoo.ajoutVal_cellule_avec( "Infecté "            , fGoo.clef_caractJoueur,
                                        habitantInfecte.matri , fGoo.clef_Matricule   ,
                                        fGoo.page1_InfoJoueurs                          )
            
            
##  Gestion des Permissions
            
            await self.salonConseilLG.set_permissions ( habitantInfecte.member , read_messages = True , send_messages = False )
                       
       
### Message Historique de la Nuit
            
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Le {fDis.Emo_LGNoir} {matricule_LGNoir} a infecté : {habitantInfecte.matri} qui a été désigné par les LG.")
            
            
            
            
            
# =============================================================================
#### --- Cas où les LGN n'inf pas et où la victime du conseil n'est pas protégée ---
# =============================================================================
        
        elif self.matriculeHab_choixConseilLG not in matriculeHab_proteges  and  self.matriculeHab_choixConseilLG != 0 :
            
            self.matriculeHab_vraimentTues.append(self.matriculeHab_choixConseilLG)
            
### Message Historique de la Nuit
    
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> {self.matriculeHab_choixConseilLG} a été dévoré par les {fDis.Emo_LoupGarou}.")
        
        
        
        
        
# =============================================================================
#### --- Dernier Cas : Personne n'est tué ---
# =============================================================================
        
        else :
            
### Message Historique de la Nuit
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Les {fDis.Emo_LoupGarou} n'ont dévoré personne.")
    
    
    
        msgResumNuit = await fDis.ajoutMsg(msgResumNuit,"\n> \n>  - ⬢⬢⬢ - ")
    
    
    
    
    
# %%% Meurtre des habitants choisis par les Sorcières
    
        for i in range(len(self.matriculeSorciere_tueuses)):
            
            matHab_Empoisonne = self.matriculeHab_tuesSorciere[i]
            
            if matHab_Empoisonne not in self.matriculeHab_vraimentTues :
            
# =============================================================================
#### --- Cas où une seule sorcière l'a choisi ---
# =============================================================================
            
                if self.matriculeHab_tuesSorciere.count(matHab_Empoisonne) == 1 :
                    
                    mat_SorciereChoisie = self.matriculeSorciere_tueuses[i]
                        
### Message Historique de la Nuit
                    msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> {fDis.Emo_Sorciere} {mat_SorciereChoisie} a empoisonné {matHab_Empoisonne} (une seule personne l'a choisie)")
                    
                    
                    
# =============================================================================
#### --- Cas où plusieurs sorcières l'ont choisi ---
# =============================================================================
                
                else :
                    
##  Choix au hasard de la sorcière tueuse parmis celle ayant choisie le même habitant
                    matSorc_ayantTueMemeHab = []
                    
                    for hab in range(len(self.matriculeHab_tuesSorciere)):
                        if self.matriculeHab_tuesSorciere[hab] == matHab_Empoisonne :
                            matSorc_ayantTueMemeHab.append(self.matriculeSorciere_tueuses[hab])
                    
                    mat_SorciereChoisie = rd.choice(matSorc_ayantTueMemeHab)
    
    
##  Message Historique de la Nuit
                    msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> {fDis.Emo_Sorciere} {mat_SorciereChoisie} a empoisonné {matHab_Empoisonne} (choisie au hasard parmis {matSorc_ayantTueMemeHab})")
        
    
    
    
    
### Mise à jour de Infos Joueurs (moins une potion de Mort pour SorciereChoisie)
                    
                ligne, num_ligne = fGoo.ligne_avec( mat_SorciereChoisie, 
                                                    fGoo.clef_Matricule, 
                                                    donneeInfosJoueurs  )
                
                nbPotionsVie, nbPotionsMort = ligne[fGoo.clef_caractRoles].split()       # 12 4 ==> 12 Potions de Vie et 4 Potions de Mort
                nvlCaractRoles_Sorciere     = f"{nbPotionsVie} {int(nbPotionsMort) - 1}"
                
                fGoo.remplacerVal_ligne( nvlCaractRoles_Sorciere, fGoo.clef_caractRoles, 
                                         num_ligne                                     , 
                                         fGoo.page1_InfoJoueurs                          )
    
            
    
### Ajout de matHab_Empoisonne à la liste des self.matriculeHab_vraimentTues
         
                if matHab_Empoisonne not in matriculeHab_proteges : 
                    self.matriculeHab_vraimentTues.append(matHab_Empoisonne)
                        
                    msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> {matHab_Empoisonne} n'est pas protégé... Il va mourir !")
                    
                msgResumNuit = await fDis.ajoutMsg(msgResumNuit,"\n> \n>  - ⬢⬢⬢ - ")
        
        
        
        
        
# %%% Meurtre des habitants choisis par les Loups-Garous Blancs

        for matHab in self.matriculeHab_tuesLGBlanc :
            
            if matHab not in self.matriculeHab_vraimentTues  and  matHab not in matriculeHab_proteges :
                self.matriculeHab_vraimentTues.append(matHab)
                
### Message Historique de la Nuit
                msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Un {fDis.Emo_LGBlanc} a dévoré {matHab}.")
                
                
                
        if len(self.matriculeHab_tuesLGBlanc) != 0 :
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit,"\n> \n>  - ⬢⬢⬢ - ")
    


    

# %%% Protection du Maire
    
        for matHab in self.matriculeHab_vraimentTues :
            
            habitant = fHab.habitant_avec(matHab)
            
            if habitant.estMaire  and  len(habitant.gardesMaire) != 0 :

                
#### Suppression des gardes morts de habitant.gardesMaire

                for matGarde in habitant.gardesMaire :
                    if fHab.habitant_avec(matGarde) == None :
                        habitant.gardesMaire.remove(matGarde)
                
                
                
                if len(habitant.gardesMaire) != 0 :
                
                    self.matriculeHab_vraimentTues.remove(matHab)
                    
                    matGardeTue = rd.choice(habitant.gardesMaire)
                    
                    self.matriculeHab_vraimentTues.append(matGardeTue)
                    
                    
#### Enregistrement dans Infos Joueur
                    
                    ligne, numligne  = fGoo.ligne_avec(matHab, fGoo.clef_Matricule, fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs))
                    
                    caractJoueur     = ligne[fGoo.clef_caractJoueur]
                    caractJoueur_Spl = caractJoueur.split()
                    caractJoueur_Spl.remove(f"M{matGardeTue}")
                    
                    nvl_caractJoueur = " ".join( caractJoueur_Spl ) + " "
                    
                    fGoo.remplacerVal_ligne(nvl_caractJoueur, fGoo.clef_caractJoueur, numligne, fGoo.page1_InfoJoueurs)
                    
                    
#### Message envoyé au Maire
                    
                    gardeTue = fHab.habitant_avec(matGardeTue)
                    
                    if gardeTue.estUnHomme : lui = "lui"
                    else                   : lui = "elle"
                    
                    await habitant.user.send(f"On a cherché à vous tuer cette nuit, mais heureuseument vous avez été protégé par **{gardeTue.prenom} {gardeTue.nom}** !\n En revanche, {lui} n'a pas survécu...")
        
                    
#### Message Historique de la Nuit
                    msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> {habitant.user.mention} est un {fDis.Emo_Maire}, il a été protégé par {gardeTue.user.mention} | {gardeTue.prenom} {gardeTue.nom}\n> \n>  - ⬢⬢⬢ - ")
        
        
        
        
        
# %%% Protection des Anciens
        
        for matHab in self.matriculeHab_vraimentTues :
            
            habitant = fHab.habitant_avec(matHab)
            
            if habitant.role == "Ancien"  and  habitant.nbProtectRest != 0 :
                
                self.matriculeHab_vraimentTues.remove(matHab)
                
##  Modification de InfosJoueurs
                
                fGoo.ajoutVal_cellule_avec( -1     , fGoo.clef_caractRoles ,
                                            matHab , fGoo.clef_Matricule   ,
                                            fGoo.page1_InfoJoueurs         ,
                                            typeObjetCellule = int           )
                
### Message envoyées à l'Ancien
                if habitant.estUnHomme : e = ""
                else                   : e = "e"
                
                if habitant.nbProtectRest != 1 :  await habitant.user.send(f"On a cherché à vous tuer cette nuit, mais vous vous êtes bien défendu !\nVous êtes encore en vie, mais vous n'êtes protégé{e} plus que {habitant.nbProtectRest - 1} fois.")
                else                           :  await habitant.user.send( "On a cherché à vous tuer cette nuit, mais vous vous êtes bien défendu !\nVous avez survécu, mais hélas c'étais la dernière fois !")
    
                
### Message Historique de la Nuit
                msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> {habitant.user.mention} est un {fDis.Emo_Ancien}, il n'a donc pas été tué, il lui reste {habitant.nbProtectRest - 1} protections.\n> \n>  - ⬢⬢⬢ - ")
    
    
    
    
    
    
    
# %% Journée
    
    async def debutJournee(self):
        
        
#### Début de Journée
        
        await self.salonRapport    .send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```\n_ _")
        await self.salonBucher     .send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```\n_ _")
        await self.salonDebat      .send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```")
        
        
        
        
        
# =============================================================================
#### === Annonce des morts de la nuit ===
# =============================================================================
        
        if len(self.matriculeHab_vraimentTues) == 0 :
            contenuMsg = "_Personne n'a été tué cette nuit_"
            
            if v.nbTours - 1 == 0 :
                contenuMsg += " **(Nuit n°0)**"
            
            await self.salonBucher.send(contenuMsg)
            
            
            
        else :
            
            village = self


#### Dissolution si le maire est tué
            
            if self.maire != None  and  self.maire.matri in self.matriculeHab_vraimentTues :
                village = await self.dissolution()
                
                
#### Meutre des personne à Tuer
            
            for matri in self.matriculeHab_vraimentTues :
                
                habTue = fHab.habitant_avec(matri)
                await habTue.Tuer(village = village)

           
                
        await self.salonBucher.send(v.separation)
        
        
#### Ré-autorisation d'écriture
        
        await self.salonRapport.set_permissions ( self.roleDiscord, read_messages = True, send_messages = False )
        await self.salonBucher .set_permissions ( self.roleDiscord, read_messages = True, send_messages = True  )
        await self.salonDebat  .set_permissions ( self.roleDiscord, read_messages = True, send_messages = True  )
        await self.vocalDebat  .set_permissions ( self.roleDiscord, read_messages = True                        )
    
        
    
    
    
    
    
# %%% Votes 
    
    def recolteBulletins(self, nbVoteParHab_egal_1 = False):
        """
        Recolte tous les votes des habitant du village
        """

        votes = list(self.votesEnPlus)
        
        for hab in self.habitants :
            
            if not nbVoteParHab_egal_1 :
                votes.extend( hab.nbVote * [hab.choixVote] )
            
            else :
                votes.extend(          1 * [hab.choixVote] )
        
        return votes
    
    
    
# %%%% Election du Maire
    
    async def gestion_electionMaire(self):
        
        await self.salonBucher.send("```⬢⬢⬢     Élection d'un nouveau maire     ⬢⬢⬢```\n_ _")
        self.msgHistorique_votes = await fDis.channelHistorique.send(f"{fDis.Emo_BabyBrown} - {self.nom} - Élection d'un nouveau maire")
        
        
#### Dépouillement initial
        
        self.typeScrutin = scrutin_ElectionMaire
        
        contenuMsg_resultat, self.resultatVote = self.depouillement()
        self.msgResultat = await self.salonBucher.send("Voici les résultats du vote :\n" + contenuMsg_resultat)
        
        
#### Boucle de vote
        
        while v.dans_dernierTour() :
            
            await asyncio.sleep(1)
            
            
        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_BabyBrown} - Fin de l'élection") 
        
        
        
        
        
#### === Application des votes ===
        
#### --- Cas 1 : Quelqu'un a été choisi par le village ---
        
        if   len(self.resultatVote) != 0 :
            
#### Selection du 1er et des habitants à égalité avec lui
            persDesignes = [ fHab.habitant_avec(self.resultatVote[0][0]) ]
            i = 1
            
            while i < len(self.resultatVote)  and  self.resultatVote[i-1][1] == self.resultatVote[i][1] :
                
                persDesignes.append( fHab.habitant_avec(self.resultatVote[i][0]) )
                i += 1
            
            
#### Choix du nouveau maire au hasard parmis les 1ers
            nouvMaire = rd.choice( persDesignes )
            
#### Annonce du résultat
            await self.salonBucher.send(f"Le village a élu **{nouvMaire.prenom} {nouvMaire.nom}** ({nouvMaire.member.mention} - {nouvMaire.groupe})")
        
        
        
        
#### --- Cas 2 : Personne n'a été choisi par le village ---
        
        else :
            
#### Choix du maire au hasard
            nouvMaire = rd.choice( self.habitants )
            
#### Annonce du résultat
            await self.salonBucher.send( f"Comme personne n'a voté, le hasard décidera de qui sera le nouveau maire du village !\nLa personne choisie est {nouvMaire.prenom} {nouvMaire.nom} ({nouvMaire.member.mention} - {nouvMaire.groupe})" )
        
        

#### --- Eregistrement ---

        nouvMaire.estMaire = True
        
        fGoo.ajoutVal_cellule_avec( "Maire "       , fGoo.clef_caractJoueur,
                                    nouvMaire.matri, fGoo.clef_Matricule   ,
                                    fGoo.page1_InfoJoueurs                   )
            
        self.maire = nouvMaire
        
        
        

            
            
    
    
    
    
# %%%% Vote Eliminatoire 


    async def gestion_voteEliminatoire(self):
        
# =============================================================================
#### === Corbeaux et Hirondelles ===
# =============================================================================
        
        await fDis.channelHistorique.send(f"**{self.nom}**\n> {fDis.Emo_Corbeau} : {self.matricule_choixCorbeaux}\n> {fDis.Emo_Hirondelle} : {self.matricule_choixHirondelles}\n_ _")
    
        msgCorbHiron = ""
    
        
        
#### Annonce des Corbeaux
        
        if len(self.matricule_choixCorbeaux) != 0 :
            
            msgCorbHiron += f"Choix des {fDis.Emo_Corbeau} :"
            
            for matriCorb in self.matricule_choixCorbeaux :
                if matriCorb not in self.matriculeHab_vraimentTues :
                    hab = fHab.habitant_avec(matriCorb)
                    
                    msgCorbHiron += f"\n> ⬢ {hab.user.mention}  |  {hab.prenom} {hab.nom}  ( {hab.groupe} )"
                    self.votesEnPlus.extend(2*[matriCorb])
            
            
##  Séparation
            
            if len(self.matricule_choixHirondelles) != 0 : 
                msgCorbHiron += "\n_ _\n"  
        
    
#### Annonce des Hirondelles
    
        if len(self.matricule_choixHirondelles) != 0 :
    
            msgCorbHiron += f"Choix des {fDis.Emo_Hirondelle} :"
            
            for matriHiron in self.matricule_choixHirondelles :
                if matriHiron not in self.matriculeHab_vraimentTues :
                    hab = fHab.habitant_avec(matriHiron)
                    
                    msgCorbHiron += f"\n> ⬢ {hab.user.mention}  |  {hab.prenom} {hab.nom}  ( {hab.groupe} )"
                    hab.nbVote += 2
    
### Envoie et Séparation
    
        if len(self.matricule_choixCorbeaux) + len(self.matricule_choixHirondelles) != 0 :
            await self.salonBucher.send(msgCorbHiron)
            await self.salonBucher.send(v.separation)
        
        
        
        
        
# =============================================================================
#### === Phase de Vote ===
# =============================================================================
        
#### Vote en 1 tour s'il y a moins de 10 habitants en vie
        
        if len(self.habitants) < 10 :
            await self.vote_en_1tour()        
        
        
#### Vote en 2 tours sinon
        
        else :
            await self.vote_en_2tours()
        
        
        
        
        
# =============================================================================
#### === Resultat du Vote ===
# =============================================================================
        
        persTue = None

#### --- Cas 1 : Quelqu'un a été choisi par le village ---
        
        if   len(self.resultatVote) != 0 :
            
#### Selection du 1er et des habitants à égalité avec lui
            persDesignes = [ fHab.habitant_avec(self.resultatVote[0][0]) ]
            i = 1
            
            while i < len(self.resultatVote)  and  self.resultatVote[i-1][1] == self.resultatVote[i][1] :
                
                persDesignes.append( fHab.habitant_avec(self.resultatVote[i][0]) )
                i += 1
            
            
#### Choix la personne tué au hasard parmis les 1ers
            persTue = rd.choice(persDesignes)
            
            phraseSentence = f"Le village a choisi de tuer {persTue.prenom} {persTue.nom} ({persTue.member.mention} - {persTue.groupe})."
        
        
        
        
        
#### --- Cas 2 : Personne n'a été choisi par le village ---
        
        else :
            
#### ||| Variante 1 ||| Choix de l'habitant tué au hasard
            
            if v.vote_aucunHabChoisi_meutreHasard :
                persTue        = rd.choice( self.habitants )
                
                phraseSentence = f"Comme personne n'a voté, un habitant choisi au hasard partira sur le bûcher !\nLa personne choisie est {persTue.prenom} {persTue.nom} ({persTue.member.mention} - {persTue.groupe})"
            
            
            
#### ||| Variante 2 ||| Personne n'est tué
            
            else :
                phraseSentence = "Comme personne n'a voté, personne ne sera tué."
        
        
        
        
        
#### --- Annonce de la sentence ---

        await self.salonBucher.send( phraseSentence )
        
        
        
        
        
# =============================================================================
#### === Application du Vote ===
# =============================================================================
        
        if persTue != None :
            
#### --- Gestion de l'exil ---
            
            persTue_aEteExile = False
            
            if self.exilOrdonne  and  not persTue.estMaire :
                
                if self.exilOrdonne_parMaire :
                    contenuMsgAnnonce_Exil = "**CEPENDANT**, __le maire__ a décidé de l'exiler dans un autre village !"
                
                else :
                    contenuMsgAnnonce_Exil = "**CEPENDANT**, un juge a décidé d'être clément et il l'a exilé dans un autre village !"
                
                await self.salonBucher.send(contenuMsgAnnonce_Exil)
                
                
                if not self.exilOrdonne_parMaire :
                    juge = rd.choice(self.juges_OrdonantExil)
                    
                    fGoo.ajoutVal_cellule_avec( -1                  , fGoo.clef_caractRoles ,
                                                juge.matri          , fGoo.clef_Matricule   ,
                                                fGoo.page1_InfoJoueurs                      ,
                                                typeObjetCellule = int                        )   
                    
                    await juge.member.send(f"Vous avez exilé {persTue.prenom} {persTue.nom}")
                
                
                persTue_aEteExile = await self.exilVote(persTue)
            
            
            
#### --- Meutre ---
            
            if not persTue_aEteExile :
                
                village = self
                
                if persTue.estMaire : 
                    village = await self.dissolution()
                    
                await persTue.Tuer(village = village, meurtreNocturne = False)
                






    async def vote_en_1tour(self):
        
        await self.salonBucher.send("```⬢⬢⬢     Vote du village     ⬢⬢⬢```\n _Il y a **moins** de 10 Habitants dans le village, il n'y aura donc qu'un seul tour_\n_ _")
        self.msgHistorique_votes = await fDis.channelHistorique.send(f"{fDis.Emo_BabyCyan} - {self.nom} - Début du vote, en 1 tour")
        
        
#### Dépouillement initial
        
        self.typeScrutin = scrutin_En1Tour
        
        contenuMsg_resultat, self.resultatVote = self.depouillement()
        self.msgResultat = await self.salonBucher.send("Voici les résultats du vote :\n" + contenuMsg_resultat)
        
        
#### Boucle de vote
        
        while v.dans_dernierTour() :
            
            await asyncio.sleep(1)
            
            
        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_Cyan} - Fin du vote") 
    
    
    
    
    
    async def vote_en_2tours(self):
        
        await self.salonBucher.send("```⬢⬢⬢     Vote du village     ⬢⬢⬢```\n _Il y a **plus** de 10 Habitants dans le village, le vote sera composé de 2 tours_\n_ _")
        
# =============================================================================
#### --- 1er Tour ---
# =============================================================================
        
        self.msgHistorique_votes = await fDis.channelHistorique.send(f"{fDis.Emo_BabyCyan} - {self.nom} - Début du 1er Tour")
        
        
#### Dépouillement initial
        
        self.typeScrutin = scrutin_En2Tour_1erT
        
        contenuMsg_resultat, self.resultatVote = self.depouillement()
        self.msgResultat = await self.salonBucher.send("Voici les résultats du 1er tour :\n" + contenuMsg_resultat)
        
        
#### Boucle de vote
        
        while v.dans_premierTour() :
            
            await asyncio.sleep(1)

    
        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_Cyan} - Fin du 1er Tour") 
        
        
        
        
        
# =============================================================================
#### --- Accusés ---
# =============================================================================
        
        self.accuses = []
        
#### Cas 1 : Si personne n'a voté
        
        if   len(self.resultatVote) == 0 :
            self.accuses = self.habitants
    
    
    
#### Cas 2 : Il y a 5 habitants ou moins désignés lors du 1er Tour
    
        elif len(self.resultatVote) <= 5 :
            for p in self.resultatVote :
                self.accuses.append( fHab.habitant_avec(p[0]) )
        
        
        
#### Cas 3 : Il y a plus de 5 habitants désignés lors du 1er Tour

        else :
            
# Prends les 5 habitants qui ont reçu le plus de voix lors du vote du village
            
            self.accuses = [ fHab.habitant_avec(self.resultatVote[0][0]), 
                        fHab.habitant_avec(self.resultatVote[1][0]), 
                        fHab.habitant_avec(self.resultatVote[2][0]), 
                        fHab.habitant_avec(self.resultatVote[3][0]), 
                        fHab.habitant_avec(self.resultatVote[4][0]) ]
            i = 5
            
#  Prend les habitants à égalité avec le 5eme
            
            while i <= len(self.resultatVote)-1  and  self.resultatVote[i][1] == self.resultatVote[i-1][1] :
                
                self.accuses.append( fHab.habitant_avec(self.resultatVote[i][0]) )
                i += 1
        
        
        
        
        
#### Annonces des Accusés et attente de leur défense
        
        if  len(self.resultatVote) != 0 :
    
            await self.salonBucher.send("Les accusés désignés lors du 1er tour sont :\n")
                
            for a in self.accuses :
                msgDefense = await self.salonBucher.send(f"      ⬢ {a.user.mention}  |  {a.prenom} {a.nom}  ( {a.groupe} )")
                asyncio.Task(a.Defense_1erTour(v.envDefVote_hFin, msgDefense))
                
                
        else :
                
            await self.salonBucher.send("Personne n'a voté lors du premier tour, il n'y a donc aucun accusés aujourd'hui !\n*Vous pouvez voter pour n'importe qui lors du 2nd Tour*")
                
        await self.salonBucher.send(v.separation)
        
        
        
        
        
# =============================================================================
#### --- 2nd Tour ---
# =============================================================================
        
        self.msgHistorique_votes = await fDis.channelHistorique.send(f"{fDis.Emo_BabyCyan} - {self.nom} - Début du 2nd Tour")
    
#### Dépouillement initial
        
        self.typeScrutin = scrutin_En2Tour_2emT
        
        contenuMsg_resultat, self.resultatVote = self.depouillement()
        self.msgResultat = await self.salonBucher.send("Voici les résultats du 2ème tour :\n" + contenuMsg_resultat)
    
#### Boucle de vote
    
        while v.dans_dernierTour() :
                
            await asyncio.sleep(1)
        
        
        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_Cyan} - Fin du vote") 





    async def exilVote(self, habitant):
        
        
        if TousLesVillages == [self]:
            
            if habitant.estUnHomme : e, Il = "" , "Il"
            else                   : e, Il = "e", "Il"
            
            await self.salonBucher.send(f"**MAIS**, comme ce village est le seul restant, {habitant.prenom} ne peut être exilé{e}...\n{Il} va donc être tué{e}, comme prévu...")
            
            return False
        
        
        
        else :

#### Choix du village d'arrivé au hasard            

            nouvVillage = self
            while nouvVillage == self :
                nouvVillage = rd.choice(TousLesVillages)
            
    #### Exil
            
            await exil(habitant, nouvVillage, ancienVillage = self)
            
    #### Message dans le nouveau Village
            
            if habitant.estUnHomme : contenuMsg_AnnonceExil = f"Un petit nouveau vient d'arriver en ville, il s'agit de {habitant.member.mention}  |  {habitant.prenom} {habitant.nom}."
            else                   : contenuMsg_AnnonceExil = f"Une petite nouvelle vient d'arriver en ville, il s'agit de {habitant.member.mention}  |  {habitant.prenom} {habitant.nom}."
            
            await nouvVillage.salonDebat.send(contenuMsg_AnnonceExil)
            
            return True





# %% Fonctions liés aux Villages

TousLesVillages = []

async def creationVillage (numNouvVillage = 0, nom = None, ajout_A_TousLesVillages = True):
    """
    Créée un nouveau village, ajoute ce village à TousLesVillages si ajout_A_TousLesVillages == True
    """   
    
# =============================================================================
#### Recherche d'un numéro disponible pour le nouveau groupe
# =============================================================================
    
    if numNouvVillage == 0 :
        numTrouve       = False
        
        numDejaUtilises = fGoo.colonne_avec(fGoo.page_Villages, fGoo.clefVlg_numVillage)
        
        while not numTrouve :
            numNouvVillage += 1
            if numNouvVillage not in numDejaUtilises :
                numTrouve = True
    
    
    
# =============================================================================
#### Nom par Défaut
# =============================================================================
    
    if nom == None :
        nom = f"Village {numNouvVillage}"
    
    
    
# =============================================================================
#### Création du nouveau Village
# =============================================================================
    
    nouvVillage = Village(numNouvVillage, nom)
    nouvVillage.redef_habitants()
    
    nvlLigne = {fGoo.clefVlg_numVillage : numNouvVillage}
    
    fGoo.ajoutLigne(nvlLigne, fGoo.page_Villages, numero_nvlLigne = "fin")
    
    if v.phaseEnCours in (v.phase2, v.phase3) :
        await nouvVillage.creation_roleEtSalons()
    
    else :
        nouvVillage.ecriture_GoogleSheet()
    
    await asyncio.sleep(0.5)
    
    
    
# =============================================================================
#### Ajout à TousLesVillages
# =============================================================================
    
    if ajout_A_TousLesVillages :
        TousLesVillages.append(nouvVillage)
    
    return nouvVillage





def redef_villagesExistants():
    """
    Fonction re-définissant les villages créés précédemment
    """
    
    print(f"Redef des Villages ({v.phaseEnCours})")
    
    global TousLesVillages
    
    donneeVillages  = fGoo.donneeGoogleSheet(fGoo.page_Villages)
    TousLesVillages = []
    
    
    
#### Redefinition des Groupe déjà dans le fichier Google Drive
    
    for ligneVlg in donneeVillages :
        
        nouvVillage = Village(ligneVlg[fGoo.clefVlg_numVillage], ligneVlg[fGoo.clefVlg_Nom])
        
        nouvVillage.redef_habitants()
        
        if type(ligneVlg[fGoo.clefVlg_idRoleDiscord]) == int :
            
            nouvVillage.roleDiscord     = fDis.serveurMegaLG.get_role(ligneVlg[fGoo.clefVlg_idRoleDiscord     ])
            nouvVillage.roleDiscordMort = fDis.serveurMegaLG.get_role(ligneVlg[fGoo.clefVlg_idRoleDiscord_Mort])
            
            nouvVillage.salonRapport    = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_Rapport          ])
            nouvVillage.salonCimetiere  = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_Cimetiere        ])
            nouvVillage.salonBucher     = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_Bucher           ])
            nouvVillage.salonDebat      = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_Debat            ])
            nouvVillage.vocalDebat      = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_vocDebat         ])
            
            nouvVillage.salonVoteLG     = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_VoteLG           ])
            nouvVillage.salonConseilLG  = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_DebatLG          ])
            nouvVillage.vocalConseilLG  = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_vocDebatLG       ])
            
            nouvVillage.salonFamilleNb  = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_FamilleNomb      ])
            nouvVillage.vocalFamilleNb  = fDis.bot.get_channel(ligneVlg[fGoo.clefVlg_idSalon_vocFamilleNomb   ])
            
            nouvVillage.categorie       = nouvVillage.salonRapport.category
        
        TousLesVillages.append(nouvVillage)





def village_avec (info, type_dinfo):
    """
    Cette Fonction renvoie le village correspondant à l'info donnée en argument.
    Si aucun village ne correspond, elle renvoie None.
    
    Voici les types d'information pris en charge : 
       'numero'
       'idSalon_Rapport'  'idSalon_Bucher'  'idSalon_Debat'  'idSalon_VocDebat'
       'idSalon_VoteLG'  'idSalon_ConseilLG'  'idSalon_VocConseilLG'
       'idSalon_FamilleNb'  'idSalon_VocFamilleNb'
    """
    
    if   type_dinfo == "numero" :
        
        for vlg in TousLesVillages :
            if vlg.numero == info :
                return vlg
            
    
    
    
    
    elif type_dinfo == "idSalon_Rapport" :
        
        for vlg in TousLesVillages :
            if vlg.salonRapport.id == info :
                return vlg
    
    
    elif type_dinfo == "idSalon_Bucher" :
        
        for vlg in TousLesVillages :
            if vlg.salonBucher.id == info :
                return vlg
    
    
    elif type_dinfo == "idSalon_Debat" :
        
        for vlg in TousLesVillages :
            if vlg.salonDebat.id == info :
                return vlg
    
    
    elif type_dinfo == "idSalon_VocDebat" :
        
        for vlg in TousLesVillages :
            if vlg.vocalDebat.id == info :
                return vlg
    
    
    
    
    
    elif type_dinfo == "idSalon_VoteLG" :
        
        for vlg in TousLesVillages :
            if vlg.salonVoteLG.id == info :
                return vlg
        
        
    elif type_dinfo == "idSalon_ConseilLG" :
        
        for vlg in TousLesVillages :
            if vlg.salonConseilLG.id == info :
                return vlg
    
    
    elif type_dinfo == "idSalon_VocConseilLG" :
        
        for vlg in TousLesVillages :
            if vlg.vocalConseilLG.id == info :
                return vlg
    
    
    
    
    
    elif type_dinfo == "idSalon_FamilleNb" :
        
        for vlg in TousLesVillages :
            if vlg.salonFamilleNb.id == info :
                return vlg
    
    
    elif type_dinfo == "idSalon_VocFamilleNb" :
        
        for vlg in TousLesVillages :
            if vlg.vocalFamilleNb.id == info :
                return vlg
    
    
    
    return None


    

async def exil_dans_nouvVillage(habitant, nouvVillage, ancienVillage = None):
    """
    Cette fonction enlève l'habitant de son ancien village et le place dans un nouveau
    """
    
#### Changement de Village dans Info Joueur
    
    fGoo.remplacerVal_ligne_avec( nouvVillage.numero, fGoo.clef_numVillage,
                                  habitant.matri    , fGoo.clef_Matricule , 
                                  fGoo.page1_InfoJoueurs                    )

    
#### Ajout de "Exilé " dans Info Joueur
    
    fGoo.ajoutVal_cellule_avec( "Exilé "       , fGoo.clef_caractJoueur ,
                                habitant.matri , fGoo.clef_Matricule    ,
                                fGoo.page1_InfoJoueurs                    )
    
    
#### Gestion des Rôles

    if ancienVillage == None :
        ancienVillage = village_avec(habitant.numVlg, "numero")
    
    await habitant.member.remove_roles( ancienVillage.roleDiscord )
    await habitant.member.   add_roles(   nouvVillage.roleDiscord )
    
    
#### Gestion des permitions
    
    await ancienVillage.salonVoteLG   .set_permissions( habitant.member , read_messages = False , send_messages = False )
    await ancienVillage.salonConseilLG.set_permissions( habitant.member , read_messages = False , send_messages = False )
    await ancienVillage.vocalConseilLG.set_permissions( habitant.member , read_messages = False                         )
    
    await ancienVillage.salonFamilleNb.set_permissions( habitant.member , read_messages = False , send_messages = False )
    await ancienVillage.vocalFamilleNb.set_permissions( habitant.member , read_messages = False                         )
    
    
#### Message d'exil 

    contenuMsg_Exil  = f"Vous avez été exilé de votre ancien village, vous habiterez maintenant à **{nouvVillage.nom}** !"
    contenuMsg_Exil +=  "\n\n*Rappel des règles* :"
    contenuMsg_Exil +=  "\n> - Au niveau de vos éventuels pouvoirs, **rien ne change** : Si vous êtes sorcière par exemple, votre nombre de potions ne change pas."
    contenuMsg_Exil +=  "\n> - Loin des Yeux, près du Cœur... Les flèches de Cupidon sont puissantes, donc si vous l'étiez, vous restez **amoureux**, malgré la distance !"
    contenuMsg_Exil +=  "\n> - Malheurement, la salive du Loup-Garou Noir est aussi très puissante, donc si vous l'étiez, vous restez **infecté**."
        
    await habitant.member.send(contenuMsg_Exil)





# %% Conseil des Loups-Garous

async def Conseil_LG (LoupGarou, village):
    
    contenuMsg_Attente = f"{fDis.Emo_LoupGarou} en tant que {fRol.emojiRole(LoupGarou.role, LoupGarou.estUnHomme)}   - {LoupGarou.user.mention}  |  {LoupGarou.prenom} {LoupGarou.nom}"
    
    msgAtt = await fDis.channelAttente.send( contenuMsg_Attente )
    
#### Début du Conseil
    
    village.voteLG_EnCours = True
    
    await village.salonVoteLG   .set_permissions( LoupGarou.member , read_messages = True  , send_messages = True  )
    await village.salonConseilLG.set_permissions( LoupGarou.member , read_messages = True  , send_messages = True  )
    await village.vocalConseilLG.set_permissions( LoupGarou.member , read_messages = True                          )
    
    
#### Attente de la Fin du Conseil
    
    while v.maintenant() < v.conseilLG_hFin :
        await asyncio.sleep(1)
    
    
#### Fin du conseil
    
    village.voteLG_EnCours = False
    
    await village.salonVoteLG   .set_permissions( LoupGarou.member , read_messages = False , send_messages = False )
    await village.salonConseilLG.set_permissions( LoupGarou.member , read_messages = True  , send_messages = v.LG_peuventParler_pdt_Journee )
    await village.vocalConseilLG.set_permissions( LoupGarou.member , read_messages = v.LG_peuventParler_pdt_Journee                         )
    
    
### Fin de l'attente
    await msgAtt.delete()





# %% === Event - Village ===

async def fct_vote(member, contenuMsg):
    """
    Fonction prenant gérant le vote 
    """
    
    habVlg  = fHab.habitant_avec( member.id            )
    village =       village_avec( habVlg.numVlg, "numero" )
    
    if village.typeScrutin != None  or  village.voteLG_EnCours:
        
#### Essaye de int le msg
        
        try :
            matriculeHab_Choisi = int(contenuMsg)
        except :
            matriculeHab_Choisi = None
        
        
        
#### Si le matricule correspond à quelqu'un en vie
        
        if fHab.habitant_avec( matriculeHab_Choisi ) != None :
            
            habVlg.choixVote = matriculeHab_Choisi
            
            if   village.typeScrutin != None : 
                
                village.msgHistorique_votes = await fDis.ajoutMsg(village.msgHistorique_votes, f"\n   - {habVlg.user.mention} vote {habVlg.nbVote} fois pour {habVlg.choixVote}\n") 
                
                contenuMsg_resultat, village.resultatVote = village.depouillement()
                await village.msgResultat   .edit(content = "Voici les résultats du vote :\n" + contenuMsg_resultat)
            
            
            elif village.voteLG_EnCours :
                
                contenuMsg_resultat, x                    = village.depouillement('LG')
                await village.msgResultatLG .edit(content = contenuMsg_resultat)





# %%% Vote du Village

async def message_voteVillage():
    
    def verifVoteVillage(message):
        verifSalon, verifUser = (False, False)
        
        verifPhase = v.phaseEnCours == v.phase3
        
        if fDis.verifServeur(message) :
            verifUser  = fDis.roleJoueurs in message.author.roles
            
            if verifUser and verifPhase :
                verifSalon = village_avec(message.channel.id, 'idSalon_Bucher') != None
        
        return verifUser  and  verifPhase and verifSalon


    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteVillage)
        await fDis.effacerMsg (message.channel)
        await fct_vote(message.author, message.content)
        
        



# %%% Vote du Conseil des Loups-Garous
        
async def message_voteLoupGarou():
    
    def verifVoteLG(message):
        verifSalon, verifUser = (False, False)
        
        verifPhase = v.phaseEnCours == v.phase3
        
        if fDis.verifServeur(message) :
            verifUser  = fDis.roleJoueurs in message.author.roles
            
            if verifUser and verifPhase :
                verifSalon = village_avec(message.channel.id, 'idSalon_VoteLG') != None
        
        return verifUser  and  verifPhase and verifSalon


    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteLG)
        await fDis.effacerMsg(message.channel)
        await fct_vote(message.author, message.content)





# %% === Commandes - Village (Joueurs) ===

# %%% Changement du nom du village (reservée au Maire)

async def cmd_changementNomVillage(memberVlg, tupleNom):
    
    habitant   = fHab.habitant_avec(memberVlg.id)
    nouveauNom = " ".join(tupleNom)
    
    if habitant != None  and  habitant.estMaire :
        if len(nouveauNom) <= 64 :
            await memberVlg.send("Le village va changer de nom !")
            
            village = village_avec(habitant.numVlg, "numero")
            await village.changementNom(nouveauNom)
        
        else :
            await memberVlg.send("**ERREUR** - Ce nom est trop long !")
    
    else :
        await memberVlg.send("**ERREUR** - Seul un maire peut changer le nom de son village !")


@fDis.bot.command()
async def Renommage(ctx, *tupleNom):
    await cmd_changementNomVillage(ctx.author, tupleNom)


@fDis.bot.command()
async def renommage(ctx, *tupleNom):
    await cmd_changementNomVillage(ctx.author, tupleNom)





# %%% Vote

async def cmd_vote(memberVlg, matricule):
    
    habVlg  = fHab.habitant_avec( memberVlg.id            )
    village =       village_avec( habVlg.numVlg, "numero" )
    
    verifLG_Camp = habVlg.role[fRol.clefCamp] == fRol.campLG
    verifLG_Infe = habVlg.estInf
    verif_LGBlan = habVlg.role == fRol.role_LGBlanc
    verif_EnfSau = habVlg.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(habVlg.pereProtecteur) == None
            
    if village.voteLG_EnCours  and  (verifLG_Camp  or  verifLG_Infe  or  verif_LGBlan  or  verif_EnfSau) :
        await fct_vote(memberVlg, matricule)
        
    else :
        await fct_vote(memberVlg, matricule)


@fDis.bot.command()
async def Vote(ctx, matricule):
    await cmd_vote(ctx.author, matricule)
    
    
@fDis.bot.command()
async def vote(ctx, matricule):
    await cmd_vote(ctx.author, matricule)

    

    

# %%% Exil (reservée aux Juges et au Maire)

async def cmd_demandeExilVote (member) :
    
    hab = fHab.habitant_avec(member.id)

#### Cas ou un maire est aussi juge

    if hab.estMaire  and  (hab.role == fRol.role_Juge  and  hab.nbExilRest >= 0):
        contenuMsg_Maire_ou_Juge  = "Vous êtes à la fois Maire (🎖️) et Juge (⚖️), sous quel rôle souhaitez-vous exiler la victime du village ?\n> *Choisissez le ⚫  pour annuler l'exil.*" 
        emojisEtReturns           = [["🎖️", ("Maire", False)], ["⚖️", ("Juge", False)], ["⚫", (None, True)]]
        
        message_Maire_ou_Juge     = await member.send(contenuMsg_Maire_ou_Juge)
        role_exilant, exil_annule = await fDis.attente_Reaction(message_Maire_ou_Juge, member, emojisEtReturns)
    
    
#### Autres cas, plus classiques
    
    elif hab.estMaire                                       : role_exilant, exil_annule = "Maire", False
    elif hab.role == fRol.role_Juge and hab.nbExilRest >= 0 : role_exilant, exil_annule = "Juge" , False
    else                                                    : role_exilant, exil_annule = None   , True
    
    
    if exil_annule :
        return


#### Message de confirmation

    contenuMsg_confirm_exilVote = "Êtes-vous certain de vouloir sauver la personne désignée par le village en l'**exilant** (dans un autre village choisi au hasard) ?" 

    if   role_exilant == "Maire" : contenuMsg_confirm_exilVote +=  "\n> Attention : Vous êtes maire, vous pouvez exiler autant de personne que vous voulez mais votre choix sera **public**."
    elif role_exilant == "Juge"  : contenuMsg_confirm_exilVote += f"\n> Il vous reste encore **{hab.nbExilRest} exils**.\n> Si le maire fait le même choix que vous, vous ne perderez pas d'exils !"
        
    message_aConfirmer = await member.send(contenuMsg_confirm_exilVote)
    exilConfirme       = await fDis.attente_Confirmation(message_aConfirmer, member)
    
    
#### ordreExil

    if exilConfirme :
        
        vlg = village_avec(hab.numVlg, 'numero')
        vlg.exilOrdonne = True
        
        if   hab.estMaire :
            vlg.exilOrdonne_parMaire = True
            await fDis.channelHistorique.send(f"Le **Maire de {vlg.nom}** a décidé d'exiler l'habitant désigné par le conseil.")
        
        else :
            vlg.juges_OrdonantExil.append(hab)
            await fDis.channelHistorique.send(f"Le **{hab.matri}** a décidé d'exiler l'habitant désigné par le conseil.")


@fDis.bot.command()
async def Exil(ctx):
    await cmd_demandeExilVote(ctx.author)


@fDis.bot.command()
async def exil(ctx):
    await cmd_demandeExilVote(ctx.author)





# %% === Commandes - Village (Admins) ===

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def SupprTousVlg (ctx):
    
    redef_villagesExistants()
    
    for vlg in TousLesVillages :
        
        await vlg.salonRapport   .delete()
        await vlg.salonCimetiere .delete()
        await vlg.salonBucher    .delete()
        await vlg.salonDebat     .delete()
        await vlg.vocalDebat     .delete()
        
        await vlg.salonVoteLG    .delete()
        await vlg.salonConseilLG .delete()
        await vlg.vocalConseilLG .delete()
        
        await vlg.salonFamilleNb .delete()
        await vlg.vocalFamilleNb .delete()
        
        await vlg.categorie      .delete()
        
        await vlg.roleDiscord    .delete()
        await vlg.roleDiscordMort.delete()





# %%% Maintenance
     
@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Meutre (ctx, matricule_hab_tue):

    if v.phaseEnCours == v.phase3 :

        hab_tue = fHab.habitant_avec(int(matricule_hab_tue))
        
        await hab_tue.Tuer()
        await fDis.channelHistorique.send(f"{hab_tue.user.mention}  |  {hab_tue.matri} {hab_tue.prenom} {hab_tue.nom} - ( {hab_tue.groupe} ) vient d'être tué")





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Sauvetage (ctx, matricule_hab_sauv):
    
    if v.phaseEnCours == v.phase3 :
        
        hab_sauv = fHab.habitant_avec(int(matricule_hab_sauv))
        village  = village_avec(hab_sauv.numVlg, "numero")
        
        village.matriculeHab_protegeSalvat.append(int(matricule_hab_sauv))
        await fDis.channelHistorique.send(f"{matricule_hab_sauv} vient d'être protégé !")





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Rapport_TousLesVillages (ctx):

    if v.phaseEnCours in (v.phase2, v.phase3, v.phase4) :
        
        await fHab.redef_TousLesHabitants()
        for vlg in TousLesVillages :
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