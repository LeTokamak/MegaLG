# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---             Niveau F - Classe et Fonctions de Gestion des Villages             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


# Niveau E
import E___fcts_nocturnes       as fNct

# Niveau D
fHab    = fNct.fHab

# Niveau C

# Niveau B
fRol    = fHab.fRol

# Niveau A
fSQL    = fHab.fSQL
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
        
        self.roleDiscord     = None
        self.roleDiscordMort = None
        
        self.categorie       = None
        self.categorie_LG    = None
        self.categorie_FN    = None
        
        self.salonRapport    = None
        self.salonCimetiere  = None
        self.salonBucher     = None
        self.salonDebat      = None
        self.vocalDebat      = None
        
        self.salonVoteLG     = None
        self.salonConseilLG  = None
        self.vocalConseilLG  = None
        
        self.salonFamilleNb  = None
        self.vocalFamilleNb  = None
        
        
        
#### Variables Nocturnes
        
        self.voteLG_EnCours              = False
        self.matriculeHab_choixConseilLG = 0
        self.msgResultatLG               = None
        
        self.matriculeLGN_quiOntInfecte  = []
        self.matriculeHab_tuesLGBlanc    = []
        
        self.matriculeHab_protegeSalvat  = []
        
        self.matriculeSorciere_sauveuse  = []
        self.matriculeSorciere_tueuses   = []
        self.matriculeHab_tuesSorciere   = []
        
        self.matricule_choixCorbeaux     = []
        self.matricule_choixHirondelles  = []
        
        self.habitants_qui_seront_tuer   = []
        
        
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
        votes     = [ v   for v in votes   if fHab.habitant_avec(v, num_village = self.numero).numVlg == self.numero ]
        
        if typeDeSuffrage == scrutin_En2Tour_2emT :
            votes = [ v   for v in votes   if fHab.habitant_avec(v, num_village = self.numero) in self.accuses       ]
    
        
        
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
                    persChoisie                         =  fHab.habitant_avec(self.matriculeHab_choixConseilLG, num_village = self.numero)
                    debutMsgResultat                    = f"**{persChoisie.pseudo}** ({persChoisie.groupe}) est la victime designée par le conseil !\n" 
            
            
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
#### Création des Catégories du Village
# =============================================================================

        self.categorie    = await fDis.serveurMegaLG   .create_category( name = f"⬢ - {self.nom} - ⬢" , position = fDis.CategoryChannel_GestionGrp.position + 1 )
        self.categorie_LG = await fDis.serveurMegaLG_LG.create_category( name = f"⬢ - {self.nom} - ⬢" , position = fDis.CategoryChannel_GestionGrp.position + 1 )
        self.categorie_FN = await fDis.serveurMegaLG_FN.create_category( name = f"⬢ - {self.nom} - ⬢" , position = fDis.CategoryChannel_GestionGrp.position + 1 )
        
# =============================================================================
#### Création des Salons du Village
# =============================================================================

        self.salonRapport   = await self.categorie   .create_text_channel ( "📋┃rapport-municipal"   , topic = f"Rapport Municipal {fMeP.de_dApostrophe(self.nom)}"              )
        self.salonCimetiere = await self.categorie   .create_text_channel ( "💀┃cimetière"           , topic = f"Cimetière {fMeP.de_dApostrophe(self.nom)}"                      )
        self.salonBucher    = await self.categorie   .create_text_channel ( "🔥┃bûcher"              , topic = f"Salon de Vote {fMeP.de_dApostrophe(self.nom)}"                  )
        self.salonDebat     = await self.categorie   .create_text_channel ( "🔪┃débats"              , topic = f"Salon de Débat {fMeP.de_dApostrophe(self.nom)}"                 )
        self.vocalDebat     = await self.categorie   .create_voice_channel( "📢┃débats"                                                                                          )
        
        self.salonVoteLG    = await self.categorie_LG.create_text_channel ( "🐺┃votes-du-conseil"    , topic = f"Salon de Vote des Loups-Garous {fMeP.de_dApostrophe(self.nom)}" )
        self.salonConseilLG = await self.categorie_LG.create_text_channel ( "🐺┃meute"               , topic = f"Débats entre les Loups-Garous {fMeP.de_dApostrophe(self.nom)}"  )
        self.vocalConseilLG = await self.categorie_LG.create_voice_channel( "🐺┃meute"                                                                                           )
        
        self.salonFamilleNb = await self.categorie_FN.create_text_channel ( "🏡┃la-maison-familiale" , topic = f"Maison familiale {fMeP.de_dApostrophe(self.nom)}"               )
        self.vocalFamilleNb = await self.categorie_FN.create_voice_channel( "🏡┃les débats familiaux"                                                                            )



### Gestion des permissions des salons du village

        await self.salonRapport  .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonCimetiere.set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonBucher   .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.salonDebat    .set_permissions( fDis.roleEveryone   , read_messages = False )
        await self.vocalDebat    .set_permissions( fDis.roleEveryone   , read_messages = False )
        
        await self.salonVoteLG   .set_permissions( fDis.roleEveryone_LG, read_messages = False )
        await self.salonConseilLG.set_permissions( fDis.roleEveryone_LG, read_messages = False )
        await self.vocalConseilLG.set_permissions( fDis.roleEveryone_LG, read_messages = False )
        
        await self.salonFamilleNb.set_permissions( fDis.roleEveryone_FN, read_messages = False )
        await self.vocalFamilleNb.set_permissions( fDis.roleEveryone_FN, read_messages = False )
        
        
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
        
        self.ecriture_BdD_SQL()
    
    
    
    
    
    def ecriture_BdD_SQL(self):
        
# =============================================================================
#### Création du dictionnaire correspondant à la ligne du Village
# =============================================================================
        
        ligneVillage = {fSQL.clef_numVillage : self.numero,
                        fSQL.clef_nomVillage : self.nom    }

        try :
            ligneVillage[fSQL.clef_idRole_vlg    ] = self.roleDiscord    .id
            ligneVillage[fSQL.clef_idRoleMort_vlg] = self.roleDiscordMort.id
            
            ligneVillage[fSQL.clef_idSalon_vlg_Rapport  ] = self.salonRapport  .id
            ligneVillage[fSQL.clef_idSalon_vlg_Role     ] = self.salonRole     .id
            ligneVillage[fSQL.clef_idSalon_vlg_Bucher   ] = self.salonBucher   .id
            ligneVillage[fSQL.clef_idSalon_vlg_Cimetiere] = self.salonCimetiere.id
            ligneVillage[fSQL.clef_idSalon_vlg_Debat    ] = self.salonDebat    .id
            ligneVillage[fSQL.clef_idSalon_vlg_vocDebat ] = self.vocalDebat    .id
            
            ligneVillage[fSQL.clef_idSalon_vlg_voteLG    ] = self.salonVoteLG   .id
            ligneVillage[fSQL.clef_idSalon_vlg_debatLG   ] = self.salonConseilLG.id
            ligneVillage[fSQL.clef_idSalon_vlg_vocDebatLG] = self.vocalConseilLG.id
            
            ligneVillage[fSQL.clef_idSalon_vlg_FamilleNomb   ] = self.salonFamilleNb.id
            ligneVillage[fSQL.clef_idSalon_vlg_vocFamilleNomb] = self.vocalFamilleNb.id
            
        except :
            pass
        
        
# =============================================================================
#### Recherche du numéro de ligne et remplacement de celle-ci
# =============================================================================
        
        fSQL.remplacer_ligne_avec(fSQL.nom_table_villages, 
                                  fSQL.clef_numVillage   , self.numero,
                                  ligneVillage)
    
    
    
    
    
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

        await self.categorie   .edit ( name = f"⬢ - {self.nom} - ⬢" )
        await self.categorie_LG.edit ( name = f"⬢ - {self.nom} - ⬢" )
        await self.categorie_FN.edit ( name = f"⬢ - {self.nom} - ⬢" )
        
        
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
        
        fSQL.remplacer_val_lignes_avec(fSQL.nom_table_villages,
                                       fSQL.clef_nomVillage, self.numero,
                                       fSQL.clef_nomVillage, self.nom)   
    
    
    
    
# %% Distibution Rôles
    
    def distribution_roles(self, compo) :
    
    #### Paquet des Rôles Restants
        
        paquetRoles_Restant = compo.roles_de_la_compo.copy()
        
        rd.shuffle(paquetRoles_Restant)
        
    
    
    #### --- Distribution des Rôles ---
    
        for hab in self.habitants :
            
            habRole = paquetRoles_Restant.pop(0)
            
            
            
    #### Caractéristiques des Rôles
            
            caractRole = ""
    
            if   habRole == fRol.role_Ancien   : caractRole =    compo.Ancien_nbProtec
            elif habRole == fRol.role_Sorciere : caractRole = f"{compo.Sorcie_nbPotVie} {compo.Sorcie_nbPotMort}"
            elif habRole == fRol.role_Juge     : caractRole =    compo.Juge_nbExil
            elif habRole == fRol.role_LGNoir   : caractRole =    compo.LGNoir_nbInfect
            
            
            
    #### Enregistrement
            
            fSQL.remplacer_val_lignes_avec(fSQL.nom_table_joueurs,
                                           fSQL.clef_idDiscord   , hab.idDis,
                                           fSQL.clef_idRole      , habRole[fRol.clefIdRole])
            
            fSQL.remplacer_val_lignes_avec(fSQL.nom_table_joueurs,
                                           fSQL.clef_idDiscord   , hab.idDis,
                                           fSQL.clef_caractRole  , caractRole)
            
            
    #### Envoie du Rôle
            
            await hab.member.send( f"Vous êtes **{habRole[fRol.clefNom]}** :" )
            await hab.member.send( embed = habRole[fRol.clefEmbed]            )
                
    
    
    
    
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
        
        grpPrec = None
        
        nbRolesInconnus = 0
        
        for hab in self.habitants :
    
#### Groupe
    
            if grpPrec != hab.groupe :
                
                listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, f"\n\n__**⬢⬢⬢   {hab.groupe.nom}   ⬢⬢⬢**__\n")
            
            grpPrec = hab.groupe
            
            
#### Emojis Villageois-Villageois et Maire
            
            if hab.role == fRol.role_VillaVilla : texteVilVil = fRol.role_VillaVilla[fRol.clefEmoji]
            else                                : texteVilVil = ":black_circle:"
            
            if hab.estMaire                     : texteMaire  = fDis.Emo_Maire
            else                                : texteMaire  = ":black_circle:"
            
            
#### Ligne écrite
            
            listeMsgJoueurs = fDis.ajoutListe(listeMsgJoueurs, f"\n>       ⬢  {texteVilVil} {texteMaire}  {hab.user.mention} - {hab.pseudo}")
            
            
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
        
        if v.rapportMunicipal_affichage_roles  or  v.nbTours == 0:
            
            if   v.nbTours != 0 :
                msgNbRole = "_ _\n__**Rôles restants :**__"
                
            else :
                msgNbRole = "```\n⬢⬢⬢\n\nCompo initiale :\n\n⬢⬢⬢\n```\n_ _"
    
#### Rôles Inconnus (des exilés)
            
            if   nbRolesInconnus != 0 :
                msgNbRole += f"\n`{nbRolesInconnus}` {fDis.Emo_RoleInconnu}\n\n"
            
#### = Listage des rôles =
            
            Emo_Roles = [[fRol.role_Villageois [fRol.clefEmoji], fRol.role_Cupidon    [fRol.clefEmoji], fRol.role_Ancien  [fRol.clefEmoji]                                            ],
                         [fRol.role_Salvateur  [fRol.clefEmoji], fRol.role_Sorciere   [fRol.clefEmoji], fRol.role_Voyante [fRol.clefEmoji] , fRol.role_Voyante_dAura [fRol.clefEmoji] ],
                         [fRol.role_Corbeau    [fRol.clefEmoji], fRol.role_Hirondelle [fRol.clefEmoji], fRol.role_Juge    [fRol.clefEmoji]                                            ],
                     list(fRol.role_FamilleNb  [fRol.clefEmoji]                                                                                                                       ),
                         [                                                                                                                                                            ],
                         [fRol.role_LG         [fRol.clefEmoji], fRol.role_LGNoir     [fRol.clefEmoji], fRol.role_LGBleu  [fRol.clefEmoji] , fRol.role_Traitre [fRol.clefEmoji]       ],
                         [fRol.role_LGBlanc    [fRol.clefEmoji], fRol.role_EnfantSauv [fRol.clefEmoji]                                                                                ] ]
            
            
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
            
#### Envoie des rôles
            
            await self.salonRapport.send( msgNbRole )
           
    
    
    
    
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
        
        self.msgResultatLG = await self.salonVoteLG.send("```Personne n'a voté```")
        
        
        
# =============================================================================
#### --- Lancement des Fonctions Nocturnes ---
# =============================================================================
        
        for hab in self.habitants :
            asyncio.Task( hab.role[fRol.clefFctsNoct](hab, self), name = f"Fonction Nocturne de {hab.pseudo} ({hab.matricule}) - {hab.role[fRol.clefNom]}" )
            
#### Accès au Conseil des Loups-Garous
            
            verifLG_Camp =  hab.role[fRol.clefCamp] == fRol.campLG  and  hab.role != fRol.role_Traitre
            verifLG_Infe =  hab.estInf
            verif_LGBlan =  hab.role == fRol.role_LGBlanc
            verif_EnfSau =  hab.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(hab.pereProtecteur, num_village = self.numero) == None
            
            if verifLG_Camp  or  verifLG_Infe  or  verif_LGBlan  or  verif_EnfSau :
                asyncio.Task( fNct.participation_au_Conseil_LG(hab, self), name = f"Participation au Conseil des LG de {hab.pseudo} ({hab.matricule}) - {hab.role[fRol.clefNom]}")
            
#### Nomination des gardes mayoraux
            
            if hab.estMaire  and  len(hab.gardesMaire) == 0 :
                asyncio.Task( fNct.nomination_gardes_maire(hab, self), name = f"Nomination gardes mayoraux de {hab.pseudo} ({hab.matricule}) - {hab.role[fRol.clefNom]}" )



# =============================================================================
#### --- Attente de la fin du vote des Loups-Garous ---
# =============================================================================

        self.voteLG_EnCours = True
        
        await asyncio.sleep(v.conseilLG_duree.seconds)
            
        self.voteLG_EnCours = False
        
        
        
# =============================================================================
#### --- Attente que la nuit se termine ---
# =============================================================================
    
        while v.maintenant() < v.nuit_hFin :
            await asyncio.sleep(1)





    async def application_nuit(self) :
        
        msgResumNuit       = await fDis.channelHistorique.send(f"```Résumé de la Nuit {v.nbTours} - {self.nom} - {fMeP.strDate(v.ajd)}```")
        
        self.habitants_qui_seront_tuer   = []
        
# %%% Protection des Joueurs
    
# =============================================================================
#### --- Habitants protégés par les Salvateurs ---
# =============================================================================
    
        matriculeHab_proteges = list(self.matriculeHab_protegeSalvat)
        
        msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Les {fDis.Emo_Salvateur} ont protégé : {self.matriculeHab_protegeSalvat}.")

    
    
# =============================================================================
#### --- Habitants protégés par les Sorcières ---
# =============================================================================
    
### Si une sorcière a sauvé ET si aucun Loup Garou Noir n'a infecté
    
        if len(self.matriculeSorciere_sauveuse) != 0  and  len(self.matriculeLGN_quiOntInfecte) == 0 :
            
            matriculeHab_proteges.append(self.matriculeHab_choixConseilLG)
            
            
##  Choix au Hasard de la Sorcière qui sauve 
            
            matricule_SorciereChoisie = rd.choice(self.matriculeSorciere_sauveuse)
            idDiscord_SorciereChoisie = [hab.idDis   
                                         for hab in self.habitants
                                         if hab.matricule == matricule_SorciereChoisie][0]
            
            
##  Modification de InfosJoueurs (moins une potion de Vie pour SorciereChoisie)
            
            ligne = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                                     fSQL.idDiscord, idDiscord_SorciereChoisie)[0]
            
            nbPotionsVie, nbPotionsMort = ligne[fSQL.clef_caractRole].split()       # 12 4 ==> 12 Potions de Vie et 4 Potions de Mort
            nvlCaractRoles_Sorciere     = f"{int(nbPotionsVie) - 1} {nbPotionsMort}"
            
            fSQL.remplacer_val_lignes_avec(fSQL.nom_table_joueurs,
                                           fSQL.idDiscord        , idDiscord_SorciereChoisie,
                                           fSQL.clef_caractRole  , nvlCaractRoles_Sorciere)
            
            
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
            idDiscord_LGNoir = [hab.idDis   
                                for hab in self.habitants
                                if hab.matricule == matricule_LGNoir][0]

    
##  Modification de la table Joueurs (moins une infection pour le LGNoir)
            
            fSQL.ajouter_val_cellule_avec(fSQL.nom_table_joueurs, 
                                          fSQL.clef_idDiscord, idDiscord_LGNoir,
                                          fSQL.clef_caractRole, -1) 
            
            
            
#### Personne Infecté
            
            habitantInfecte = fHab.habitant_avec(info        = self.matriculeHab_choixConseilLG,
                                                 num_village = self.numero                      )
            
            if habitantInfecte.estMaire :
                mat_habitantInfecte = rd.choice(habitantInfecte.gardesMaire)
                habitantInfecte     = fHab.habitant_avec(mat_habitantInfecte, num_village = self.numero)
            
            habitantInfecte.estInf = True
            
##  Messages d'infections
            
            if habitantInfecte.estUnHomme : e = ""
            else                          : e = "e"

            await self.salonConseilLG.send(f"{habitantInfecte.user.mention} vient d'être infecté{e} !")
                
                
##  Modification de InfosJoueurs
            fSQL.ajouter_val_cellule_avec(fSQL.nom_table_joueurs, 
                                          fSQL.clef_idDiscord   , habitantInfecte.idDis,
                                          fSQL.clef_caractJoue  , "Infecté ")
                        
            
##  Accès au serveur des Loups-Garous
            
            msg_invitation_inf = "Vous avez été infecté par un Loup-Garou Noir, vous rencontrerez vos nouveaux camarades ce soir !\n> **Vous pouvez rejoindre le serveur des Loups-Garous avec ce lien :**"

            await fDis.invitation_MegaLG_LG( habitantInfecte.user, msg_invitation_inf)
            
       
### Message Historique de la Nuit
            
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Le {fDis.Emo_LGNoir} {matricule_LGNoir} a infecté : {habitantInfecte.matricule} qui a été désigné par les LG.")
            
            
            
            
            
# =============================================================================
#### --- Cas où les LGN n'inf pas et où la victime du conseil n'est pas protégée ---
# =============================================================================
        
        elif self.matriculeHab_choixConseilLG not in matriculeHab_proteges  and  self.matriculeHab_choixConseilLG != 0 :
            
            self.habitants_qui_seront_tuer.append(fHab.habitant_avec(self.matriculeHab_choixConseilLG, num_village = self.numero))
            
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
            
            matHab_Empoisonne   = self.matriculeHab_tuesSorciere[i]
            habitant_empoisonne = fHab.habitant_avec(matHab_Empoisonne, num_village = self.numero)
            
            if habitant_empoisonne not in self.habitants_qui_seront_tuer :
            
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
                
                idDiscord_SorciereChoisie = [hab.idDis   
                                             for hab in self.habitants
                                             if hab.matricule == mat_SorciereChoisie][0]

                ligne = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                                         fSQL.idDiscord, idDiscord_SorciereChoisie)[0]
                
                nbPotionsVie, nbPotionsMort = ligne[fSQL.clef_caractRole].split()       # 12 4 ==> 12 Potions de Vie et 4 Potions de Mort
                nvlCaractRoles_Sorciere     = f"{nbPotionsVie} {int(nbPotionsMort) - 1}"
                
                fSQL.remplacer_val_lignes_avec(fSQL.nom_table_joueurs,
                                               fSQL.idDiscord        , idDiscord_SorciereChoisie,
                                               fSQL.clef_caractRole  , nvlCaractRoles_Sorciere)
                
                
                
### Ajout de habitant_empoisonne à la liste des self.habitants_qui_seront_tuer
         
                if matHab_Empoisonne not in matriculeHab_proteges : 
                    self.habitants_qui_seront_tuer.append(habitant_empoisonne)
                        
                    msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> {matHab_Empoisonne} n'est pas protégé... Il va mourir !")
                    
                msgResumNuit = await fDis.ajoutMsg(msgResumNuit,"\n> \n>  - ⬢⬢⬢ - ")
        
        
        
        
        
# %%% Meurtre des habitants choisis par les Loups-Garous Blancs

        for matHab in self.matriculeHab_tuesLGBlanc :
            
            habitant_devore = fHab.habitant_avec(matHab, num_village = self.numero)
            
            if habitant_devore not in self.habitants_qui_seront_tuer  and  matHab not in matriculeHab_proteges :
                self.habitants_qui_seront_tuer.append(habitant_devore)
                
### Message Historique de la Nuit
                msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> Un {fDis.Emo_LGBlanc} a dévoré {matHab}.")
                
                
                
        if len(self.matriculeHab_tuesLGBlanc) != 0 :
            msgResumNuit = await fDis.ajoutMsg(msgResumNuit,"\n> \n>  - ⬢⬢⬢ - ")
    


    

# %%% Protection du Maire
    
        for habitant in self.habitants_qui_seront_tuer :
            
            if habitant.estMaire  and  len(habitant.gardesMaire) != 0 :
                
                mat_gardes_pouvant_proteger_le_maire = list(habitant.gardesMaire)



                for matGarde in mat_gardes_pouvant_proteger_le_maire :
                    
                    garde = fHab.habitant_avec(matGarde, num_village = self.numero)

#### Suppression des gardes morts de habitant.gardesMaire
#### Suppression des gardes déjà dans self.habitants_qui_seront_tuer

                    if garde == None  or  garde in self.habitants_qui_seront_tuer:
                        mat_gardes_pouvant_proteger_le_maire.remove(matGarde)
                

                
                if len(mat_gardes_pouvant_proteger_le_maire) != 0 :
                
                    self.habitants_qui_seront_tuer.remove(habitant)
                    
                    matGardeTue = rd.choice(mat_gardes_pouvant_proteger_le_maire)
                    gardeTue    = fHab.habitant_avec(matGardeTue, num_village = self.numero)
                    
                    self.habitants_qui_seront_tuer.append(gardeTue)
                    
                    
#### Enregistrement dans Infos Joueur
                    
                    ligne = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                                             fSQL.idDiscord, habitant.idDis)[0]
                    
                    caractJoueur     = ligne[fSQL.clef_caractJoue]
                    caractJoueur_Spl = caractJoueur.split()
                    caractJoueur_Spl.remove(f"M{gardeTue.matricule}")
                    
                    nvl_caractJoueur = " ".join( caractJoueur_Spl ) + " "
                    
                    fSQL.remplacer_val_lignes_avec(fSQL.nom_table_joueurs,
                                                   fSQL.idDiscord, habitant.idDis,
                                                   fSQL.caractJoue, nvl_caractJoueur)
                    
#### Message envoyé au Maire
                    
                    if gardeTue.estUnHomme : lui = "lui"
                    else                   : lui = "elle"
                    
                    await habitant.user.send(f"On a cherché à vous tuer cette nuit, mais heureuseument vous avez été protégé par **{gardeTue.pseudo}** !\n En revanche, {lui} n'a pas survécu...")
        
                    
#### Message Historique de la Nuit
                    msgResumNuit = await fDis.ajoutMsg(msgResumNuit, f"\n> \n> {habitant.user.mention} est un {fDis.Emo_Maire}, il a été protégé par {gardeTue.user.mention} | {gardeTue.pseudo}\n> \n>  - ⬢⬢⬢ - ")
        
        
        
        
        
# %%% Protection des Anciens
        
        for habitant in self.habitants_qui_seront_tuer :
            
            if habitant.role == "Ancien"  and  habitant.nbProtectRest > 0 :
                
                self.habitants_qui_seront_tuer.remove(habitant)
                
##  Modification de InfosJoueurs

                fSQL.ajouter_val_cellule_avec(fSQL.nom_table_joueurs,
                                              fSQL.clef_idDiscord, habitant.idDis,
                                              fSQL.clef_caractRole, -1)

                
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
        
        await self.salonRapport.send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```\n_ _")
        await self.salonBucher .send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```\n_ _")
        await self.salonDebat  .send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```")
        
        
#### Annonce des morts de la nuit
#     |   Je ne gère ici que le cas où personne n'a été tué, 
#     | les habitants seront vraiment tuées dans la fonction gestion_dissolutions_meurtres_exils 
#     | qui est appelée juste après avoir lancée les méthodes debutJournee de tous les villages 

        if len(self.habitants_qui_seront_tuer) == 0 :
            contenuMsg = f"*Aucun habitant de {self.nom} n'a été tué cette nuit*"
            
            if v.nbTours - 1 == 0 :
                contenuMsg += "\n> **(Nuit n°0)**"
                contenuMsg += "\n> *__Pour rappel :__ la Nuit n°0 est une nuit qui se passe comme les autres, mais elle n'a **aucune conséquence**.*"
            
            await self.salonBucher.send(contenuMsg)
        
        
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
        
#### Messages d'introduction
        
        await self.salonBucher.send(v.separation + "\n```⬢⬢⬢     Élection d'un nouveau maire     ⬢⬢⬢```\n_ _")
        self.msgHistorique_votes = await fDis.channelHistorique.send(f"{fDis.Emo_BabyBrown} - {self.nom} - Élection d'un nouveau maire")
        
        
        
# =============================================================================
#### --- Lancement du Scrutin ---
# =============================================================================
        
        self.typeScrutin = scrutin_ElectionMaire
        
        
#### Dépouillement initial
#     |   Ce premier dépouillement sert à définir les attributs du village
        
        contenuMsg_resultat, self.resultatVote = self.depouillement()
        self.msgResultat = await self.salonBucher.send("Voici les résultats du vote :\n" + contenuMsg_resultat)
        
        
#### Attente de la fin du vote
#     |   Cette boucle attend que le vote se termine,
#     | les votes des habitants ne sont pas gérés ici, mais dans la fonction : message_voteVillage
#     |
#     |   Cette fonction modifie les attributs de scrutin du village (qui viennent d'être définit)
        
        while v.dans_dernierTour() :
            await asyncio.sleep(1)
        
        
#### Fin du vote

        self.typeScrutin = None
        
        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_BabyBrown} - Fin de l'élection") 
        
        
        
# =============================================================================
#### === Application des votes ===
# =============================================================================
        
#### --- Cas 1 : Quelqu'un a été choisi par le village ---
#     |   Le maire réellement élu est choisi au hasard parmis les personnes ayant reçu le plus vote
        
        if   len(self.resultatVote) != 0 :
            
#    -->  Sélection du 1er et des habitants à égalité avec lui

            persDesignes = [ fHab.habitant_avec(self.resultatVote[0][0], num_village = self.numero) ]
            i            = 1
            
            while i < len(self.resultatVote)  and  self.resultatVote[i-1][1] == self.resultatVote[i][1] :
                
                persDesignes.append( fHab.habitant_avec(self.resultatVote[i][0], num_village = self.numero) )
                i += 1
            
            
#    -->  Choix du nouveau maire au hasard parmis les 1ers
#    -->  Et annonce du résultat

            nouvMaire = rd.choice( persDesignes )
            
            contenuMsg_resultat_Maire  = f"Le village a élu comme maire : **{nouvMaire.pseudo}** ({nouvMaire.member.mention} - {nouvMaire.groupe})"
            
        
        
        
        
#### --- Cas 2 : Personne n'a été choisi par le village ---
#     |   Comme personne n'a voté, le maire est choisi au hasard parmis les habitants
        
        else :
            
#    -->  Choix du nouveau maire au hasard parmis les 1ers
#    -->  Et annonce du résultat

            nouvMaire = rd.choice( self.habitants )
            
            if nouvMaire.estUnHomme : le_nouveau = "Le nouveau"
            else                    : le_nouveau = "La nouvelle"
            
            contenuMsg_resultat_Maire  =  "Comme personne n'a voté, c'est donc le hasard qui va décider !\n"
            contenuMsg_resultat_Maire += f"> {le_nouveau} maire est **{nouvMaire.pseudo}** ({nouvMaire.member.mention} - {nouvMaire.groupe})"
        
        
        await self.salonBucher.send( contenuMsg_resultat_Maire )
        
        

#### --- Eregistrement ---

        nouvMaire.estMaire = True
        
        fSQL.ajouter_val_cellule_avec(fSQL.nom_table_joueurs,
                                      fSQL.clef_idDiscord, nouvMaire.idDis,
                                      fSQL.clef_caractJoue, "Maire ")
            
        self.maire = nouvMaire
    
    
    
    
    
# %%%% Vote Eliminatoire 


    async def gestion_voteEliminatoire(self):
        
        await self.salonBucher.send(v.separation)
        
# =============================================================================
#### --- Corbeaux et Hirondelles ---
# =============================================================================
        
        contenuMsg_Histo_Corb_Hiron  = f"**{self.nom}**\n"
        contenuMsg_Histo_Corb_Hiron += f"> {fDis.Emo_Corbeau} : {self.matricule_choixCorbeaux}\n"
        contenuMsg_Histo_Corb_Hiron +=  "> \n"
        contenuMsg_Histo_Corb_Hiron += f"> {fDis.Emo_Hirondelle} : {self.matricule_choixHirondelles}\n"
        contenuMsg_Histo_Corb_Hiron +=  "_ _"
        
        await fDis.channelHistorique.send(contenuMsg_Histo_Corb_Hiron)
        
        
        contenuMsg_Corb_Hiron = ""
    
        
        
# --> Annonce des Corbeaux
        
        if len(self.matricule_choixCorbeaux) != 0 :
            
            contenuMsg_Corb_Hiron += f"Choix des {fDis.Emo_Corbeau} :"
            
            for matriCorb in self.matricule_choixCorbeaux :
                hab = fHab.habitant_avec(matriCorb, num_village = self.numero)
                
                if hab != None :
                    contenuMsg_Corb_Hiron += f"\n> ⬢ {hab.user.mention}  |  {hab.pseudo}  ( {hab.groupe} )"
                    self.votesEnPlus.extend(2*[matriCorb])
            
            
            # Séparation entre corbeaux et hirondelles
            
            if len(self.matricule_choixHirondelles) != 0 : 
                contenuMsg_Corb_Hiron += "\n_ _\n"  
        
        
    
# --> Annonce des Hirondelles
    
        if len(self.matricule_choixHirondelles) != 0 :
    
            contenuMsg_Corb_Hiron += f"Choix des {fDis.Emo_Hirondelle} :"
            
            for matriHiron in self.matricule_choixHirondelles :
                hab = fHab.habitant_avec(matriHiron, num_village = self.numero)
                
                if hab != None :
                    contenuMsg_Corb_Hiron += f"\n> ⬢ {hab.user.mention}  |  {hab.pseudo}  ( {hab.groupe} )"
                    hab.nbVote += 2
        
        
# --> Envoie du Message
        
        if contenuMsg_Corb_Hiron != "" :
            await self.salonBucher.send(contenuMsg_Corb_Hiron)
            await self.salonBucher.send(v.separation)
        
        
        
        
        
# =============================================================================
#### --- Phase de Vote ---
# =============================================================================
        
#### Vote en 1 tour s'il y reste moins de 10 habitants en vie
        
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
#     |   L'habitant qui sera tué est choisi au hasard parmis les personnes ayant reçu le plus vote
        
        if   len(self.resultatVote) != 0 :
            
#    -->  Selection du 1er et des habitants à égalité avec lui

            persDesignes = [ fHab.habitant_avec(self.resultatVote[0][0], num_village = self.numero) ]
            i            = 1
            
            while i < len(self.resultatVote)  and  self.resultatVote[i-1][1] == self.resultatVote[i][1] :
                
                persDesignes.append( fHab.habitant_avec(self.resultatVote[i][0], num_village = self.numero) )
                i += 1
            
            
#    -->  Choix la personne tué au hasard parmis les 1ers

            persTue = rd.choice(persDesignes)
            
            contenuMsg_Sentence = f"Le village a choisi de tuer {persTue.pseudo} ({persTue.member.mention} - {persTue.groupe})."
        
        
        
        
        
#### --- Cas 2 : Personne n'a été choisi par le village ---

        else :
            
#### ||| Variante 1 ||| Choix de l'habitant tué au hasard
            
            if v.vote_aucunHabChoisi_meurtreHasard :
                persTue        = rd.choice( self.habitants )
                
                contenuMsg_Sentence  =  "Comme personne n'a voté, un habitant choisi au hasard partira sur le bûcher !\n"
                contenuMsg_Sentence += f"> La personne choisie est {persTue.pseudo} ({persTue.member.mention} - {persTue.groupe})"
            
            
#### ||| Variante 2 ||| Personne n'est tué
            
            else :
                contenuMsg_Sentence = "Comme personne n'a voté, personne ne sera tué."
        
        
        
        
        
#### --- Annonce de la sentence ---

        await self.salonBucher.send( contenuMsg_Sentence )
        
        
        
        
        
# =============================================================================
#### === Gestion des exils ===
# =============================================================================
        
        self.habitants_qui_seront_tuer   = []

        if persTue != None :
            
#### --- Meurtre ---
            
            self.habitants_qui_seront_tuer   = [persTue]
                
                




    async def vote_en_1tour(self):
        
        await self.salonBucher.send("```⬢⬢⬢     Vote du village     ⬢⬢⬢```\n> *Il y a **moins** de 10 Habitants dans le village, il n'y aura donc qu'un seul tour*\n_ _")
        self.msgHistorique_votes = await fDis.channelHistorique.send(f"{fDis.Emo_BabyCyan} - {self.nom} - Début du vote, en 1 tour")
        
        
#### Dépouillement initial
        
        self.typeScrutin = scrutin_En1Tour
        
        contenuMsg_resultat, self.resultatVote = self.depouillement()
        self.msgResultat = await self.salonBucher.send("Voici les résultats du vote :\n" + contenuMsg_resultat)
        
        
#### Boucle de vote
        
        while v.dans_dernierTour() :
            
            await asyncio.sleep(1)
            
            
#### Fin du vote 

        self.typeScrutin = None

        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_Cyan} - Fin du vote") 
    
    
    
    
    
    async def vote_en_2tours(self):
        
        await self.salonBucher.send("```⬢⬢⬢     Vote du village     ⬢⬢⬢```\n> *Il y a **plus** de 10 Habitants dans le village, le vote sera composé de 2 tours*\n_ _")
        
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


#### Fin du vote

        self.typeScrutin = None
    
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
                self.accuses.append( fHab.habitant_avec(p[0], num_village = self.numero) )
        
        
        
#### Cas 3 : Il y a plus de 5 habitants désignés lors du 1er Tour

        else :
            
# Prends les 5 habitants qui ont reçu le plus de voix lors du vote du village
            
            self.accuses = [ fHab.habitant_avec(self.resultatVote[0][0], num_village = self.numero), 
                             fHab.habitant_avec(self.resultatVote[1][0], num_village = self.numero), 
                             fHab.habitant_avec(self.resultatVote[2][0], num_village = self.numero), 
                             fHab.habitant_avec(self.resultatVote[3][0], num_village = self.numero), 
                             fHab.habitant_avec(self.resultatVote[4][0], num_village = self.numero) ]
            i = 5
            
#  Prend les habitants à égalité avec le 5eme
            
            while i <= len(self.resultatVote)-1  and  self.resultatVote[i][1] == self.resultatVote[i-1][1] :
                
                self.accuses.append( fHab.habitant_avec(self.resultatVote[i][0], num_village = self.numero) )
                i += 1
        
        
        
        
        
#### Annonces des Accusés et attente de leur défense
        
        if  len(self.resultatVote) != 0 :
    
            await self.salonBucher.send("Les accusés désignés lors du 1er tour sont :\n")
                
            for a in self.accuses :
                msgDefense = await self.salonBucher.send(f"      ⬢ {a.user.mention}  |  {a.pseudo}  ( {a.groupe} )")
                asyncio.Task(a.Defense_1erTour(v.envDefVote_hFin, msgDefense))
                
                
        else :
                
            await self.salonBucher.send("Personne n'a voté lors du premier tour, il n'y a donc aucun accusés aujourd'hui !\n> *Vous pouvez voter pour n'importe qui lors du second Tour*")
                
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
        
        
#### Fin du vote

        self.typeScrutin = None
        
        self.msgHistorique_votes = await fDis.ajoutMsg(self.msgHistorique_votes, f"\n{fDis.Emo_Cyan} - Fin du vote") 



# %% Fin de la partie

    async def verif_finDePartie (self) :
        
# =============================================================================
#### Condition de fin de partie
# =============================================================================

        """
        La partie se termine si :
            ==> Il y a plus de LG que de Vlg :
                - Sauf si les sorcières ont encore des potions de vie ou de mort 
                - Sauf si des gardes sont encore en vie
                
        """
        
        victoire_des_vlg = False
        victoire_des_lgs = False
        victoire_solo    = False
        
        contenuMsg_rapportEtatPartie = f"=== État de la partie du Village n°{self.numero} : {self.nom} ===\n"
        
        villageoisImpuissants  = [ hab   for hab in self.habitants   if len(hab.role[fRol.clefPouvoir]) == 0 and hab.role[fRol.clefCamp] == fRol.campVillage ]
        loupsGarousImpuissants = [ hab   for hab in self.habitants   if len(hab.role[fRol.clefPouvoir]) == 0 and hab.role[fRol.clefCamp] == fRol.campLG      ]
        
        villageois  = [ hab   for hab in self.habitants   if hab.role[fRol.clefCamp] == fRol.campVillage ]
        loupsGarous = [ hab   for hab in self.habitants   if hab.role[fRol.clefCamp] == fRol.campLG ]
        
        
        
#### === Vérif 0 : Règles bassiques du jeu === 
        
        if len(villageois) == 0 :
            contenuMsg_rapportEtatPartie += "> `Vérif 0` - Il n'y a plus aucun de {fDis.Emo_Villageois}. **VICTOIRE DES LOUPS-GAROUS**"
            victoire_des_lgs = True
            
        if len(loupsGarous) == 0 :
            contenuMsg_rapportEtatPartie += "> `Vérif 0` - Il n'y a plus aucun de {fDis.Emo_LoupGarou}. **VICTOIRE DES VILLAGEOIS**"
            victoire_des_vlg = True
            
      # if seul un couple est en vie
      
      # if seul un role solo est en vie
        
        
        
#### === Vérif 1 : Prédictions Élémentaires ===
        
        if not victoire_des_vlg  and  not victoire_des_lgs :
            if len(villageois) > len(loupsGarous) :
                contenuMsg_rapportEtatPartie += "> `Vérif 1` - Il y a plus de {fDis.Emo_Villageois} que de {fDis.Emo_LoupGarou}. **VAINQUEURS INDÉTERMINABLES**"
            else :
                contenuMsg_rapportEtatPartie += "> `Vérif 1` - Il y a moins de {fDis.Emo_Villageois} que de {fDis.Emo_LoupGarou}. **VAINQUEURS ÉVENTUELLEMENT DÉTERMINABLES**"
                
                
#### === Vérif 2 : Prédictions Avancées ===

                # if len(loupsGarous) + nb_infection_total + nb_enfantSauvage
        




# %% Fonctions liés aux Villages

# %%% Manipulation de villages

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
        
        numDejaUtilises = fSQL.colonne_avec(fSQL.nom_table_villages, fSQL.clef_numVillage)
        
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
    
    nvlLigne = {fSQL.clef_numVillage : numNouvVillage}
    
    fSQL.ajouter_ligne(fSQL.nom_table_villages, nvlLigne)
    
    await nouvVillage.creation_roleEtSalons()
    
    
    
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
    
    donneeVillages  = fSQL.donnees_de_la_table(fSQL.nom_table_villages)
    TousLesVillages = []
    
    
    
#### Redefinition des Groupe déjà dans le fichier Google Drive
    
    for ligneVlg in donneeVillages :
        
        nouvVillage = Village(ligneVlg[fSQL.clef_numVillage], 
                              ligneVlg[fSQL.clef_nomVillage])
        
        nouvVillage.redef_habitants()
        
        if type(ligneVlg[fSQL.clef_idRole_vlg]) == int :
            
            nouvVillage.roleDiscord     = fDis.serveurMegaLG.get_role(ligneVlg[fSQL.clef_idRole_vlg     ])
            nouvVillage.roleDiscordMort = fDis.serveurMegaLG.get_role(ligneVlg[fSQL.clef_idRoleMort_vlg ])
            
            nouvVillage.salonRapport    = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_Rapport   ])
            nouvVillage.salonRole       = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_Role      ])
            nouvVillage.salonCimetiere  = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_Bucher    ])
            nouvVillage.salonBucher     = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_Cimetiere ])
            nouvVillage.salonDebat      = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_Debat     ])
            nouvVillage.vocalDebat      = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_vocDebat  ])
            
            nouvVillage.salonVoteLG     = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_voteLG    ])
            nouvVillage.salonConseilLG  = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_debatLG   ])
            nouvVillage.vocalConseilLG  = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_vocDebatLG])
            
            nouvVillage.salonFamilleNb  = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_FamilleNomb   ])
            nouvVillage.vocalFamilleNb  = fDis.bot.get_channel(ligneVlg[fSQL.clef_idSalon_vlg_vocFamilleNomb])
            
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




# %%% Dissolutions, meurtres et exils

async def gestion_meurtres (meurtre_nocturne):
    """
    Cette fonction gère TOUTES les exécutions.
    C'est elle qui s'occupe aussi de tuer les amoureux.
    
    Pour cela elle : 
        - Regarde chaque village individuellement et elle regroupe les personnes à tuer
        - Ensuite les personnes à tuer sont réellement exécuter (y compris les amants)
    """
    
    tous_les_habitants_a_tuer     = []
    
# =============================================================================
#### --- Définition de tous_les_habitants_a_tuer ---
# =============================================================================
    
    for village in TousLesVillages :
        tous_les_habitants_a_tuer  .extend(village.habitants_qui_seront_tuer  )
        
#### Ajouts des éventuels amants (représentés par des listes de la forme [amoureux_de_hab_tué, hab_tué])
        
    for habitant in tous_les_habitants_a_tuer :
        
        if type(habitant) == list : habitant = habitant[0]
        
        if habitant.estAmoureux :
            
            for mat_amant in habitant.amants :
                
                amant = fHab.habitant_avec(mat_amant, num_village = habitant.numVlg)
                if amant not in tous_les_habitants_a_tuer :
                    
                    tous_les_habitants_a_tuer.append( [amant, habitant] )

# Ici tous_les_habitants_a_tuer est une liste contenant :
#  | Des habitants, qui seront directement tués
#  | Des listes contenant deux objets habitant, dont le premier est l'amant qui se suicide suite à la mort du second
          
           
    
# =============================================================================
#### --- Meurtre de tous les habitants à tuer ---
# =============================================================================

    for element in tous_les_habitants_a_tuer :
        
        if type(element) == list : habitant_a_tuer, amant_tue_en_premier = element
        else                     : habitant_a_tuer, amant_tue_en_premier = element, None
        
        village = village_avec(habitant_a_tuer.numVlg, "numero")
        
        await habitant_a_tuer.Tuer( village         = village                     , 
                                    meurtreNocturne = meurtre_nocturne            , 
                                    suicideAmoureux = amant_tue_en_premier != None, 
                                    premAmoureuxTue = amant_tue_en_premier          )
        
        
#### Cas de la mort d'un modèle d'un enfant sauvage
        
        for hab in fHab.TousLesHabitants : 
            if hab != habitant_a_tuer  and  hab.role == fRol.role_EnfantSauv  and  hab.pereProtecteur == habitant_a_tuer.matricule :
                
                await fDis.invitation_MegaLG_LG(hab.user, "Votre modèle est mort, vous devenez donc un loup-garou...\n*Vous pouvez rejoindre vos nouveaux compère sur ce serveur :*")
        
        
       
        
        


# %%% Gestion des permissions

async def gestion_permission_serveurMegaLG_LG (membre_Discord) :
    """
    Gestion des permissions de membre_Discord dans le serveurMegaLG_LG
    """
    
    hab = fHab.habitant_avec(membre_Discord.id)
    vlg =       village_avec(hab.numVlg, "numero")
    
    verifLG_Camp = False
    verifLG_Infe = False
    verif_LGBlan = False
    verif_EnfSau = False
    
    membre_serveurMLG = fDis.serveurMegaLG.get_member(membre_Discord.id)
    
    if hab != None :
        verifLG_Camp =  hab.role[fRol.clefCamp] == fRol.campLG  and  hab.role != fRol.role_Traitre
        verifLG_Infe =  hab.estInf
        verif_LGBlan =  hab.role == fRol.role_LGBlanc
        verif_EnfSau =  hab.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(hab.pereProtecteur, num_village = vlg.numero) == None

        
        
    
    if verifLG_Camp or verifLG_Infe or verif_LGBlan or verif_EnfSau :
        
        await fDis.channelHistorique.send(f"{membre_serveurMLG.mention} vient d'arriver dans le serveur des {fDis.Emo_LoupGarou}. *(en tant que {fDis.Emo_LoupGarou})*")
        
        if v.nuit_hDeb < v.maintenant() < v.conseilLG_hFin :
            asyncio.Task( fNct.participation_au_Conseil_LG(hab, vlg), name = f"Participation au Conseil des LG de {hab.pseudo} ({hab.matricule}) - {hab.role[fRol.clefNom]}")
                
        else : 
            await vlg.salonVoteLG   .set_permissions( membre_Discord , read_messages = False , send_messages = False )
            await vlg.salonConseilLG.set_permissions( membre_Discord , read_messages = True  , send_messages = v.LG_peuventParler_pdt_Journee )
            await vlg.vocalConseilLG.set_permissions( membre_Discord , read_messages = v.LG_peuventParler_pdt_Journee                         )
        
        
        
    elif membre_serveurMLG == None  or  fDis.roleModerateur not in membre_serveurMLG.roles :
        
        await fDis.serveurMegaLG_FN.kick(membre_Discord)
        
        
        
    elif fDis.roleModerateur in membre_serveurMLG.roles :
        
        await fDis.channelHistorique.send(f"{membre_serveurMLG.mention} vient d'arriver dans le serveur des {fDis.Emo_LoupGarou}. *(en tant que modérateur)*")
    
    



async def gestion_permission_serveurMegaLG_FN (membre_Discord) :
    """
    Gestion des permissions de membre_Discord
    """
    
    hab = fHab.habitant_avec(membre_Discord.id)
    vlg =       village_avec(hab.numVlg, "numero")
    
    membre_serveurMLG = fDis.serveurMegaLG.get_member(membre_Discord.id)
    
    if hab != None  and  hab.role == fRol.role_FamilleNb :
        
        await fDis.channelHistorique.send(f"{membre_serveurMLG.mention} vient d'arriver dans le serveur des {fDis.Emo_FNSoeur}. *(en tant que {fDis.Emo_FNSoeur})*")
        
        if v.nuit_hDeb < v.maintenant() < v.nuit_hFin :
            asyncio.Task( fNct.fctNoct_FamilleNombreuse(hab, vlg), name = f"Fonction Nocturne de {hab.pseudo} ({hab.matricule}) - {hab.role[fRol.clefNom]}" )
    
        else :
            await vlg.salonFamilleNb  .set_permissions ( membre_Discord , read_messages = True , send_messages = v.FN_peuventParler_pdt_Journee )
            await vlg.vocalFamilleNb  .set_permissions ( membre_Discord , read_messages = v.FN_peuventParler_pdt_Journee                        )
            
    
    elif membre_serveurMLG == None  or  fDis.roleModerateur not in membre_serveurMLG.roles :
        
        await fDis.serveurMegaLG_FN.kick(membre_Discord)


    elif fDis.roleModerateur in membre_serveurMLG.roles :
        
        await fDis.channelHistorique.send(f"{membre_serveurMLG.mention} vient d'arriver dans le serveur des {fDis.Emo_FNSoeur}. *(en tant que modérateur)*")





# %% === Event - Vote ===

async def fct_vote(member, contenuMsg):
    """
    Fonction prenant en argument le :
        - Membre ayant envoyé un message 
        - Le contenu du message envoyé
        
    Cette fonction gère le vote lors de tous les scrutins ! (Election / Elimination / Loups-Garous)
    
    Le membre qui a lancé cette fonction à bien le droit de voter (cette condition a été vérifié avant)
    """
    
    habVlg  = fHab.habitant_avec( member.id               )
    village =       village_avec( habVlg.numVlg, "numero" )
    
    if village.typeScrutin != None  or  village.voteLG_EnCours:
        
#### Gestion de la fonction de random
        
        if contenuMsg in ["Random", "random", "Rd", "rd", "R", "r"]:
            
            matriculeHab_Choisi = habVlg.matricule
            
            while matriculeHab_Choisi == habVlg.matricule :
                
                habChoisi           = rd.choice( village.habitants )
                matriculeHab_Choisi = habChoisi.matricule
        
        
        
#### Essaye de int le msg

        else :
            try    : matriculeHab_Choisi = int(contenuMsg)
            except : matriculeHab_Choisi = None
        
        
        
#### Si le matricule correspond à quelqu'un en vie
        
        if fHab.habitant_avec( matriculeHab_Choisi, num_village = village.numero) != None :
            
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
        
        habVlg     = fHab.habitant_avec( message.author.id )
        
        verifUser  = habVlg != None
        verifSalon = False
        verifVote  = False
        
        if verifUser :
            
            village    = village_avec( habVlg.numVlg, "numero" )
            verifSalon = message.channel == village.salonBucher
            verifVote  = village.typeScrutin != None
        
        return verifUser and verifSalon and verifVote 



    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteVillage)
        await fDis.effacerMsg (message.channel)
        await fct_vote(message.author, message.content)
        
        



# %%% Vote du Conseil des Loups-Garous
        
async def message_voteLoupGarou():
    
    def verifVoteLG(message):
        
        habVlg     = fHab.habitant_avec( message.author.id )
        
        verifUser  = habVlg != None
        verifSalon = False
        verifVote  = False
        
        if verifUser :
            
            village    = village_avec( habVlg.numVlg, "numero" )
            verifSalon = message.channel == village.salonVoteLG
            verifVote  = village.voteLG_EnCours
        
        return verifUser and verifSalon and verifVote



    while True :
        message = await fDis.bot.wait_for('message', check = verifVoteLG)
        await fDis.effacerMsg(message.channel)
        await fct_vote(message.author, message.content)





# %% === Commandes - Village (Joueurs) ===

@fDis.bot.command(aliases = ["renommage_village", "Renommage_Vlg", "renommage_vlg", "Renommage", "renommage"])
async def Renommage_Village(ctx, *tupleNom):
    
    habitant   = fHab.habitant_avec(ctx.author.id)
    nouveauNom = " ".join(tupleNom)
    
    if habitant != None  and  habitant.estMaire :
        if len(nouveauNom) <= 64 :
            await ctx.author.send("Le village va changer de nom !")
            
            village = village_avec(habitant.numVlg, "numero")
            await village.changementNom(nouveauNom)
        
        else :
            await ctx.author.send("**ERREUR** - Ce nom est trop long !")
    
    else :
        await ctx.author.send("**ERREUR** - Seul un maire peut changer le nom de son village !")





@fDis.bot.command(aliases = ["vote", "V", "v"])
async def Vote(ctx, matricule):
    
    habVlg  = fHab.habitant_avec( ctx.author.id           )
    village =       village_avec( habVlg.numVlg, "numero" )
    
    verifLG_Camp = habVlg.role[fRol.clefCamp] == fRol.campLG
    verifLG_Infe = habVlg.estInf
    verif_LGBlan = habVlg.role == fRol.role_LGBlanc
    verif_EnfSau = habVlg.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(habVlg.pereProtecteur, num_village = village.numero) == None
            
    if village.voteLG_EnCours  and  (verifLG_Camp  or  verifLG_Infe  or  verif_LGBlan  or  verif_EnfSau) :
        await fct_vote(ctx.author, matricule)
        
    else :
        await fct_vote(ctx.author, matricule)




    
@fDis.bot.command(aliases = ["exil_vote", "Exil", "exil"])
async def Exil_Vote (ctx) :
    
    hab = fHab.habitant_avec(ctx.author.id)

#### Cas ou un maire est aussi juge

    if hab.estMaire  and  (hab.role == fRol.role_Juge  and  hab.nbExilRest >= 0):
        contenuMsg_Maire_ou_Juge  = "Vous êtes à la fois Maire (🎖️) et Juge (⚖️), sous quel rôle souhaitez-vous exiler la victime du village ?\n> *Choisissez le ⚫  pour annuler l'exil.*" 
        emojisEtReturns           = [["🎖️", ("Maire", False)], ["⚖️", ("Juge", False)], ["⚫", (None, True)]]
        
        message_Maire_ou_Juge     = await ctx.author.send(contenuMsg_Maire_ou_Juge)
        role_exilant, exil_annule = await fDis.attente_Reaction(message_Maire_ou_Juge, ctx.author, emojisEtReturns)
    
    
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
        
    message_aConfirmer = await ctx.author.send(contenuMsg_confirm_exilVote)
    exilConfirme       = await fDis.attente_Confirmation(message_aConfirmer, ctx.author)
    
    
#### ordreExil

    if exilConfirme :
        
        vlg = village_avec(hab.numVlg, 'numero')
        vlg.exilOrdonne = True
        
        if   hab.estMaire :
            vlg.exilOrdonne_parMaire = True
            await fDis.channelHistorique.send(f"Le **Maire de {vlg.nom}** a décidé d'exiler l'habitant désigné par le conseil.")
        
        else :
            vlg.juges_OrdonantExil.append(hab)
            await fDis.channelHistorique.send(f"Le **{hab.matricule}** a décidé d'exiler l'habitant désigné par le conseil.")





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
        await vlg.categorie_LG   .delete()
        await vlg.categorie_FN   .delete()
        
        await vlg.roleDiscord    .delete()
        await vlg.roleDiscordMort.delete()





# %%% Maintenance
     

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def RedefAll (ctx) :
    redef_villagesExistants()
    fHab.redef_TousLesHabitants()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Meurtre (ctx, num_village, matricule_hab_tue):

    if v.phaseEnCours == v.phase3 :
        
        redef_villagesExistants()
        fHab.redef_TousLesHabitants()
        
        hab_tue = fHab.habitant_avec(int(matricule_hab_tue), num_village=int(num_village))
        
        await hab_tue.Tuer(village_avec(hab_tue.numVlg, "numero"))
        await fDis.channelHistorique.send(f"{hab_tue.user.mention}  |  {hab_tue.matricule} {hab_tue.pseudo} - ( {hab_tue.groupe} ) vient d'être tué (meurtre ordonné par {ctx.author})")



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Sauvetage (ctx, num_village, matricule_hab_sauv):
    
    if v.phaseEnCours == v.phase3 :
        
        hab_sauv = fHab.habitant_avec(int(matricule_hab_sauv), num_village=int(num_village))
        village  = village_avec(hab_sauv.numVlg, "numero")
        
        village.matriculeHab_protegeSalvat.append(int(matricule_hab_sauv))
        await fDis.channelHistorique.send(f"{matricule_hab_sauv} vient d'être protégé (protection ordonnée par {ctx.author}) !")



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Rapport_TousLesVillages (ctx):

    if v.phaseEnCours in (v.phase2, v.phase3, v.phase4) :
        
        fHab.redef_TousLesHabitants()
        for vlg in TousLesVillages :
            await vlg.rapportMunicipal()



@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Amoureux (ctx, matricule1, matricule2, num_village):
    
    mat_amour1 = int(matricule1)
    mat_amour2 = int(matricule2)
    
    pers1 = fHab.habitant_avec(mat_amour1, num_village = int(num_village))
    pers2 = fHab.habitant_avec(mat_amour2, num_village = int(num_village))
    
    fSQL.ajouter_val_cellule_avec(fSQL.nom_table_joueurs, 
                                  fSQL.clef_idDiscord , pers1.idDis, 
                                  fSQL.clef_caractJoue, f"A{pers2.matricule} ")
    
    fSQL.ajouter_val_cellule_avec(fSQL.nom_table_joueurs, 
                                  fSQL.clef_idDiscord , pers2.idDis, 
                                  fSQL.clef_caractJoue, f"A{pers1.matricule} ")
        
    await pers1.user.send(f"Vous êtes amoureux de {pers2.matricule}  |  {pers2.pseudo} {pers2.groupe}")
    await pers2.user.send(f"Vous êtes amoureux de {pers1.matricule}  |  {pers1.pseudo} {pers1.groupe}")
    
    fHab.redef_TousLesHabitants()
    
    
    
    
"""
@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def AmoureuxAlea (ctx):
    
    fHab.redef_TousLesHabitants()
    
    Celibs = []
    
    for pers in fPer.ToutesLesPersonnes :
        if not pers.estAmoureux :
            Celibs.append(pers)
    
    while len(Celibs) >= 2 : 
    
        pers1 = fMeP.rd.choice(Celibs)
        pers2 = fMeP.rd.choice(Celibs)
        
        Celibs.remove(pers1)
        Celibs.remove(pers2)
        
        fGoo.ajoutVal_cellule_avec( f"A{pers2.matricule} ", fGoo.clef_caractJoueur ,
                                    pers1.matricule       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                      )
    
        fGoo.ajoutVal_cellule_avec( f"A{pers1.matricule} ", fGoo.clef_caractJoueur ,
                                    pers2.matricule       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                      )
    
        await pers1.user.send(f"Vous êtes amoureux de {pers2.matricule}  |  {pers2.pseudo} {pers2.groupe}")
        await pers2.user.send(f"Vous êtes amoureux de {pers1.matricule}  |  {pers1.pseudo} {pers1.groupe}")
"""