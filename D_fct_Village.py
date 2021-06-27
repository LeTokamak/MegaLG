# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---             Niveau D - Classe et Fonctions de Gestion des Villages             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


# Niveau C
import C_fct_Habitant       as fHab

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




def depouillement (village, typeDeSuffrage = None):
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
        typeDeSuffrage = village.typeScrutin
    
    
    
#### Rassemblement de tout les votes
    """
    if typeDeSuffrage == "LG" :
        votes = list( village.votesConseilLG )
    else : 
        votes = village.recolteBulletins()
    """
    
    if typeDeSuffrage == "LG" :
        votes = village.recolteBulletins(nbVoteParHab_egal_1 = True)
    else : 
        votes = village.recolteBulletins()
    
# --- votes = [1, 2, 2, 4, 5, 4, 4, 1, 2, 4, 2, 1, 1, 5, 4, 2, 4, 2, 4, 5, 4, 3, 1, 5, 2, 4, 4]
    
    votes.sort()
    
# --- votes = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]
    
    
#### Nettoyages des votes (exclusion des 0, des personnes n'étant pas dans le village et des personnes non accusées)
    
    votes     = [ v   for v in votes   if v != 0                                         ]
    votes     = [ v   for v in votes   if fHab.habitant_avec(v).numVlg == village.numero ]
    
    if typeDeSuffrage == scrutin_En2Tour_2emT :
        votes = [ v   for v in votes   if fHab.habitant_avec(v) in village.accuses       ]

    
    
    
    
    
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
                village.matriculeHab_choixConseilLG =  0
                debutMsgResultat                    =  "Personne n'est designée par le conseil ! (égalité)\n" 
            
            else :
                village.matriculeHab_choixConseilLG =  resultatsTries[0][0]
                persChoisie                         =  fHab.habitant_avec(village.matriculeHab_choixConseilLG)
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
        #self.votesConseilLG                = []
        #self.LG_ayant_votes                = []
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
        """
        async def cloneSalon(debutTopic, nom) :
            salonRetourne = self.categorie.create_text_channel( name = nom )
            await salonRetourne.edit( topic = f"{debutTopic} {fMeP.de_dApostrophe(self.nom)}", category = self.categorie )
            
            return salonRetourne
        
        
### Clonage d'un des salons de référence, pour créer les salons du village
        
        self.salonRapport   = await self.categorie.create_text_channel( "📋┃rapport-municipal", "Rapport Municipal"                , fDis.channelRapport     )
        self.salonCimetiere = await cloneSalon( "Cimetière"                        , fDis.channelCimetiere   )
        self.salonBucher    = await cloneSalon( "Salon de Vote"                    , fDis.channelBucher      )
        self.salonDebat     = await cloneSalon( "Salon de Débat"                   , fDis.channelDebat       )
        self.vocalDebat     = await cloneSalon( "Débats Vocaux"                    , fDis.vocalDebat         )
        
        self.salonVoteLG    = await cloneSalon( "Salon de Vote des Loups-Garous"   , fDis.channelVotesLG     )
        self.salonConseilLG = await cloneSalon( "Débats entre les Loups-Garous"    , fDis.channelLoupsGarous )
        self.vocalConseilLG = await cloneSalon( "Discussion entre les Loups-Garous", fDis.vocalLoupsGarous   )
        
        self.salonFamilleNb = await cloneSalon( "Maison familiale"                 , fDis.channelFamilleNom  )
        self.vocalFamilleNb = await cloneSalon( "Réunion familiale"                , fDis.vocalFamilleNom    )
        """
        
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

        await self.salonRapport  .set_permissions( self.roleDiscord , read_messages = True  , send_messages = False )
        await self.salonBucher   .set_permissions( self.roleDiscord , read_messages = True  , send_messages = False )
        await self.salonCimetiere.set_permissions( self.roleDiscord , read_messages = True  , send_messages = False )
        await self.salonDebat    .set_permissions( self.roleDiscord , read_messages = True  , send_messages = True  )
        await self.vocalDebat    .set_permissions( self.roleDiscord , read_messages = True                          )
        
        
        await self.salonRapport  .set_permissions( self.roleDiscordMort , read_messages = True  , send_messages = False )
        await self.salonBucher   .set_permissions( self.roleDiscordMort , read_messages = True  , send_messages = False )
        await self.salonCimetiere.set_permissions( self.roleDiscordMort , read_messages = True  , send_messages = False )
        await self.salonDebat    .set_permissions( self.roleDiscordMort , read_messages = True  , send_messages = False )
        await self.vocalDebat    .set_permissions( self.roleDiscordMort , read_messages = False                         )
        
# =============================================================================
#### Enregistrement des modifications
# =============================================================================
        
        self.ecriture_GoogleSheet()
    
    
    
    
    
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
                    await exil(hab, nouvVillage, ancienVillage = self)
                    await asyncio.sleep(0.1)
            
            
#### Message dans le nouveau Village
            
            contenuMsg_AnnonceExil = f"**{self.nom}** a été détruit... {len(self.habitants)} habitants viennent d'arriver à {nouvVillage.nom} !"
            
            await nouvVillage.salonDebat.send(contenuMsg_AnnonceExil)
            
            
#### Suppresion du Référencement du Village
            
            fGoo.suppressionLigne_avec(self.numero, fGoo.clefVlg_numVillage, fGoo.page_Villages)
            
            TousLesVillages.remove(self)
            
            return nouvVillage
    
    
    
    
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
                asyncio.Task( fctNoct_Maire(hab, self) )
            
            
            
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

            if self.maire.matri in self.matriculeHab_vraimentTues :
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
        
        contenuMsg_resultat, self.resultatVote = depouillement(self)
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
        
        contenuMsg_resultat, self.resultatVote = depouillement(self)
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
        
        contenuMsg_resultat, self.resultatVote = depouillement(self)
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
        
        contenuMsg_resultat, self.resultatVote = depouillement(self)
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


    

async def exil(habitant, nouvVillage, ancienVillage = None):
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















# %% Fonctions Nocturnes des différents rôles

async def fctNoct_Villageois (villageois, village):
    pass





async def fctNoct_Cupidon (cupidon, village):
    
    contenuMsgCupi_Question =  "Bonsoir Cupidon, vous allez pouvoir choisir les deux personnes que vous souhaitez réunir !\nPour cela envoyez ici leurs matricules, un par un."
    contenuMsgCupi_Detail   =  "\n```\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne repondez pas, le couple sera créé au hasard.\n```"
    
    contenuMsgCupi_Attente  = f"{fDis.Emo_Cupidon} en tant que {fRol.emojiRole(cupidon.role, cupidon.estUnHomme)}   - {cupidon.user.mention}  |  {cupidon.prenom} {cupidon.nom}"
    
    contenuMsgCupi_HistoDeb = f"\n{fRol.emojiRole(cupidon.role, cupidon.estUnHomme)}   - {cupidon.user.mention}  |  {cupidon.prenom} {cupidon.nom}"


    
# =============================================================================
#### --- Demande des amoureux ---
# =============================================================================

    if v.nbTours == 0 :

### Message

        await cupidon.user.send(contenuMsgCupi_Question + contenuMsgCupi_Detail)
                
#### Attente des Matricules des Amoureux
    
        msgAtt = await fDis.channelAttente.send(contenuMsgCupi_Attente)
                
        amour1 = amour2 = None
        aRepondu        = True
                
        while amour1 == amour2  and  aRepondu :
            await cupidon.user.send("Qui sera le premier amoureux ?")
            amour1, aRepondu = await cupidon.attenteMatri_Habitant(v.nuit_hFin, autorisation_AutoDesignation = True)
                    
            await cupidon.user.send("Et qui sera le second ?")
            amour2, aRepondu = await cupidon.attenteMatri_Habitant(v.nuit_hFin, autorisation_AutoDesignation = True)
                    
            if amour1 == amour2  and  aRepondu :
                await cupidon.user.send("Vous devez choisir deux amoureux différents.\nVous allez pouvoir en choisir de nouveaux !")
            
#### Cupidon n'a pas répondu, choix du couple au harsard
    
        if not aRepondu :
            
            amour1 = amour2 = rd.choice(village.habitants)
            
            while amour2 == amour1 :
                amour2 = rd.choice(village.habitants)
                
            await cupidon.user.send(f"Vous n'avez pas répondu, votre couple vous a donc été attribué au hasard, c'est :\n> {fMeP.AjoutZerosAvant(amour1.matri ,3)}  |  **{amour1.prenom} {amour1.nom}** en {amour1.groupe} et \n> {fMeP.AjoutZerosAvant(amour2.matri ,3)}  |  **{amour2.prenom} {amour2.nom}** en {amour2.groupe}.")
        
        
#### Annonce du couple aux amoureux
        
        if amour1.estUnHomme : e1 = "" 
        else                 : e1 = "e"
        
        if amour2.estUnHomme : e2 = ""
        else                 : e2 = "e"
        
        await amour1.user.send(f"Vous venez de recevoir une flèche en plein cœur ! Mais pas d'inquiètude, c'est un mignon petit bébé qui vous a attaqué{e1}.\n> Mais depuis, vous êtes attiré{e1} par {fMeP.AjoutZerosAvant(amour2.matri ,3)}  |  **{amour2.prenom} {amour2.nom}** en {amour2.groupe}, quelle étrange coïncidence...")
        await amour2.user.send(f"Vous venez de recevoir une flèche en plein cœur ! Mais pas d'inquiètude, c'est un mignon petit bébé qui vous a attaqué{e2}.\n> Mais depuis, vous êtes attiré{e2} par {fMeP.AjoutZerosAvant(amour1.matri ,3)}  |  **{amour1.prenom} {amour1.nom}** en {amour1.groupe}, quelle étrange coïncidence...")
        
#### Modif de Infos Joueurs pour l'ajout des matricules du couple
        
        fGoo.ajoutVal_cellule_avec( f"{amour1.matri} {amour2.matri} ", fGoo.clef_caractRoles , 
                                    cupidon.matri                    , fGoo.clef_Matricule   ,
                                    fGoo.page1_InfoJoueurs                                    )

        fGoo.ajoutVal_cellule_avec( f"A{amour2.matri} ", fGoo.clef_caractJoueur ,
                                    amour1.matri       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                       )
        
        fGoo.ajoutVal_cellule_avec( f"A{amour1.matri} ", fGoo.clef_caractJoueur ,
                                    amour2.matri       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                       )
        
    
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCupi_HistoDeb + f"\n     A choisi {amour1.user.mention}  |  **{amour1.prenom} {amour1.nom}**  et  {amour2.user.mention}  |  **{amour2.prenom} {amour2.nom}**")
        
### Fin de l'attente
        
        await msgAtt.delete()


        """
# =============================================================================
# Message Dominicale
# =============================================================================

    elif False :
                
        await cupidon.user.send("Bonsoir Cupidon, aujourd'hui c'est dimanche et comme chaque dimanche vous allez pouvoir communiquer avec votre couple préféré !\n```\nLe prochain message partira directement en destination de votre couple cheri !\n - Vous pouvez y mettre ce que vous voulez, mais vous ne pourrez pas le modifier !```")
                
### Attente de Message
                
        msgAtt = await fDis.channelAttente.send(contenuMsgCupi_Attente)
        messageReponse, aRepondu = await cupidon.attenteMessage(v.nuit_hFin)
                
### Cherche reponse.content, fonctionne si reponse est un discord.Message
                
        if aRepondu :
            contenu = messageReponse.content
                                            
##  Envoie contenu aux membre du couple
                        
            for a in cupidon.couple :
                await fHab.habitant_avec(int(a)).user.send(f"Vous avez reçu ceci :\n>>> {contenu}")
        
##  Historique
    
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCupi_HistoDeb + f"\n     {cupidon.couple} ont reçu ceci :\n> {contenu}\n")
    
    
### Cupidon n'a pas répondu
    
        else :
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCupi_HistoDeb + f"\n     {cupidon.couple} n'ont rien reçu.\n")
                
        await msgAtt.delete()
        """




async def fctNoct_Ancien (ancien, village):
    pass





async def fctNoct_Salvateur (salvateur, village):
    
    contenuMsgSalva_Question =  "Bonsoir Salvateur, qui allez vous protéger cette nuit ?"
    contenuMsgSalva_Detail   =  "\n```\nVous pouvez protéger un joueur de toutes les attaques nocturnes !\n - Vous pouvez protéger plusieurs fois de suite la même personne.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n```"
    
    contenuMsgSalva_Attente  = f"{fDis.Emo_Salvateur} en tant que {fRol.emojiRole(salvateur.role, salvateur.estUnHomme)}   - {salvateur.user.mention}  |  {salvateur.prenom} {salvateur.nom}"
    
    contenuMsgSalva_HistoDeb = f"\n{fRol.emojiRole(salvateur.role, salvateur.estUnHomme)}   - {salvateur.user.mention}  |  {salvateur.prenom} {salvateur.nom}"
    
    
    
### Message
    await salvateur.user.send(contenuMsgSalva_Question + contenuMsgSalva_Detail)
           
#### Attente du Matricule de la personne protégée
    msgAtt = await fDis.channelAttente.send(contenuMsgSalva_Attente)
    habProtege, aRepondu = await salvateur.attenteMatri_Habitant(v.nuit_hFin)
    
    
    if aRepondu :
        village.matriculeHab_protegeSalvat.append(habProtege.matri)
        
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSalva_HistoDeb + f"\n     Ce salvateur a choisi {habProtege.user.mention}.")
        
    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSalva_HistoDeb +  "\n     Ce salvateur n'a choisi personne.")

### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Sorciere (sorciere, village):
   

    if (sorciere.nbPotionsVie + sorciere.nbPotionsMort) == 0 :
        return

### Attente du début de la partie 3
    await sorciere.attente(v.avtP3_duree.seconds)
        
        
        
        
        
# =============================================================================
#### === Construction du Message ===
# =============================================================================
        
    contenuMsgSorci_Attente  = f"{fDis.Emo_Sorciere} en tant que {fRol.emojiRole(sorciere.role, sorciere.estUnHomme)}   - {sorciere.user.mention}  |  {sorciere.prenom} {sorciere.nom}"
    contenuMsgSorci_HistoDeb = f"\n{fRol.emojiRole(sorciere.role, sorciere.estUnHomme)}   - {sorciere.user.mention}  |  {sorciere.prenom} {sorciere.nom}"
        
        
#### --- Cas où les LG ont choisi quelqu'un ---
        
    if   village.matriculeHab_choixConseilLG != 0 :
        persChoisie = fHab.habitant_avec(village.matriculeHab_choixConseilLG)
            
#### Construction du Message pour la Sorcière
        ( msgNb_potVie , msgNb_potMort ,
          detail_potVie, detail_potMort, et ) = ("", "", "", "", "")
            
        if   sorciere.nbPotionsVie  >= 2 : msgNb_potVie  = f"**{sorciere.nbPotionsVie} potions** de Vie"
        elif sorciere.nbPotionsVie  == 1 : msgNb_potVie  =  "plus qu'**une potion** de Vie"
            
        if   sorciere.nbPotionsMort >= 2 : msgNb_potMort = f"**{sorciere.nbPotionsMort} potions** de Mort"
        elif sorciere.nbPotionsMort == 1 : msgNb_potMort =  "plus qu'**une potion** de Mort"
        
        if   sorciere.nbPotionsVie != 0 and sorciere.nbPotionsMort != 0 : et = " et "
        
        
        
        if sorciere.nbPotionsVie  != 0 :
            detail_potVie  = "\n - Pour sauver la victime du conseil, réagissez à ce message avec 🟢.\n - Si plusieurs sorcière la sauvent, seulement une choisie au hasard perdra sa potion."
            
        if sorciere.nbPotionsMort != 0 :
            detail_potMort = "\n - Pour tuer quelqu'un d'autre, réagissez à ce message avec 🔴.\n - Si plusieurs sorcières tuent la même personne, seulement une choisie au hasard perdra sa potion."
            
        contenuMsgSorci_Question = f"Bonsoir Sorcière, les loups-garous ont choisi comme victime : **{persChoisie.prenom} {persChoisie.nom} {persChoisie.groupe}** ({fMeP.AjoutZerosAvant(persChoisie.matri, 3)}), voulez-vous utiliser une de vos potions ?\nIl vous reste {msgNb_potVie}{et}{msgNb_potMort}."
        contenuMsgSorci_Detail   = f"\n```\n - Vous ne pouvez utiliser qu'une potion par nuit.{detail_potVie}{detail_potMort}\n - Pour ne rien faire, réagissez à ce message avec ⚫ (ou ne faites rien).\n```"
    
    
    
#### --- Cas où les LG n'ont choisi personne et quand la sorcière à encore des potions de mort ---
        
    elif sorciere.nbPotionsMort != 0 :
            
        contenuMsgSorci_Question = f"Bonsoir Sorcière, les loups-garous n'ont pas choisi de victime ce soir.\nNéanmoins, vous pouvez utiliser une de vos potions de mort (Il vous en reste **{sorciere.nbPotionsMort}**), voulez-vous en utiliser une ?"
        contenuMsgSorci_Detail   =  "\n```\n - Pour tuer quelqu'un d'autre, réagissez à ce message avec 🔴.\n - Si plusieurs sorcières tuent la même personne, seulement une choisie au hasard perdra sa potion.\n - Pour ne rien faire, réagissez à ce message avec ⚫ (ou ne faites rien).\n```"
            
#### Envoie du Message à la Sorcière
    msgQuestion = await sorciere.user.send(contenuMsgSorci_Question + contenuMsgSorci_Detail)
        
        
        
        
        
# =============================================================================
#### === Détermination des réponses Possibles ===
# =============================================================================
        
    choixRien = "La Sorcière a décidé de ne rien faire"
    choixSauv = "La Sorcière a décidé de sauver la victime du conseil"
    choixTuer = "La Sorcière a décidé de tuer quelqu'un d'autre"

    emojisEtReturns = []
        
    if sorciere.nbPotionsVie  != 0 and village.matriculeHab_choixConseilLG != 0 : 
        emojisEtReturns.append(["🟢", choixSauv])
        
    if sorciere.nbPotionsMort != 0 : 
        emojisEtReturns.append(["🔴", choixTuer])
        
    emojisEtReturns.append(["⚫", choixRien])
    
    
    
    
    
# =============================================================================
#### === Attente de la Réponse de la Sorcière ===
# =============================================================================       
    
    msgAtt = await fDis.channelAttente.send( contenuMsgSorci_Attente )
    
    tempsRestant = v.nuit_hFin - v.maintenant()
    
    choixSorciere = await fDis.attente_Reaction(msgQuestion, sorciere.user, emojisEtReturns, timeout = tempsRestant.seconds)
    
#### --- Cas 1 : La sorcière ne réponds pas où elle répond "rR" ---
    
    if   choixSorciere in (choixRien, None) :
        
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + "\n   La sorcière n'a rien fait cette nuit.")
    
    
    
#### --- Cas 2 : La sorcière sauve la victime des LG ---
    
    elif choixSorciere == choixSauv :
        
        village.matriculeSorciere_sauveuse.append( sorciere.matri )
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + "\n   La sorcière a sauvé la victime des Loups-Garous !")
    
    
#### --- Cas 3 : La sorcière veut tuer quelqu'un d'autre ---
    
    elif choixSorciere == choixTuer :
    
#### Message
        contenuMsgPoison_Question = "Sorcière, vous avez décidé d'utiliser une de vos potions de mort. Qui voulez-vous empoisonner ?"
        contenuMsgPoison_Detail   = "\n```\nPour choisir votre victime, envoyez ici son matricule.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n```"
        
        await sorciere.user.send(contenuMsgPoison_Question + contenuMsgPoison_Detail)
        
#### Attente de Réponse
        msgAtt2 = await fDis.channelAttente.send(contenuMsgSorci_Attente + "   ##### Choix de la personne à empoisonner #####")
        victimeSorciere, aRepondu = await sorciere.attenteMatri_Habitant(v.nuit_hFin)
        
        if aRepondu :
            village.matriculeSorciere_tueuses.append(        sorciere.matri )
            village.matriculeHab_tuesSorciere.append( victimeSorciere.matri )
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + f"\n   La sorcière a tué {victimeSorciere.user.mention} {victimeSorciere.prenom} {victimeSorciere.nom} !")
            
        else :
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + "\n   La sorcière n'a tué personne.")
        
        
### Fin de l'attente (Empoisonnement)
        await msgAtt2.delete()
    
    
###############################################################################
    
    
### Fin de l'attente                
    await msgAtt.delete()





async def fctNoct_Voyante (voyante, village):
    
    contenuMsgVoyante_Question =  "Bonsoir Voyante, c'est l'heure de faire chauffer votre boule de cristal ! Vous allez pouvoir voir le rôle d'un habitant, qui choisissez-vous ?"
    contenuMsgVoyante_Detail   =  "\n```\nPour choisir un joueur, envoyez son matricule sous ce message.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n```"
    
    contenuMsgVoyante_Attente  = f"{fDis.Emo_Voyante} en tant que {fRol.emojiRole(voyante.role, voyante.estUnHomme)}   - {voyante.user.mention}  |  {voyante.prenom} {voyante.nom}"
    
    contenuMsgVoyante_HistoDeb = f"\n{fRol.emojiRole(voyante.role,voyante.estUnHomme)}   - {voyante.user.mention}  |  {voyante.prenom} {voyante.nom}"
    
#### Message
    await voyante.user.send(contenuMsgVoyante_Question + contenuMsgVoyante_Detail)
    
#### Attente du Matricule d'habitant
    msgAtt = await fDis.channelAttente.send(contenuMsgVoyante_Attente)
    pers, aRepondu = await voyante.attenteMatri_Habitant(v.nuit_hFin)
    
    
    
    if aRepondu :
        
#   Cas où pers est un Loup Bleu
        if pers.role == fRol.role_LGBleu :
            Role = rd.choice( [ role[fRol.clefNom]   for role in fRol.TousLesRoles   if role[fRol.clefCamp] == fRol.campVillage ] )
        
        else :
            Role = pers.role[fRol.clefNom]
        
#### Réponse de la boule de cristal
        reponseBoule = f"{fMeP.AjoutZerosAvant(pers.matri,3)}  |  **{pers.prenom} {pers.nom}** {pers.groupe} est **{Role}**"

        await voyante.user.send(f"Vous voyez dans votre boule que {reponseBoule}.")
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgVoyante_HistoDeb + f"\n     Elle a vu dans sa boule que {reponseBoule}.")
    
    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgVoyante_HistoDeb +  "\n     Elle n'a pas regardé sa boule.")
    
### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Chasseur (chasseur, village):
    pass
    




async def fctNoct_Corbeau (corbeau, village):
    
    contenuMsgCorbeau_Question =  "Bonsoir Corbeau, qui allez-vous désigner cette nuit ?"
    contenuMsgCorbeau_Detail   =  "\n```\nVous allez pouvoir votez de manière anonyme pour la personne que vous voulez, elle recevra 2 voix, pour cela envoyez ici son matricule.\n - Si plusieurs Corbeaux font le même choix que vous, les voix se cumulerons.\n - Ces ne voix compterons que pour le premier tour.\n - Si le matricule ne correspond à personne, vous pourrez le retaper\n```"
    
    contenuMsgCorbeau_Attente  = f"{fDis.Emo_Corbeau} en tant que {fRol.emojiRole(corbeau.role, corbeau.estUnHomme)}   - {corbeau.user.mention}  |  {corbeau.prenom} {corbeau.nom}"
    
    contenuMsgCorbeau_HistoDeb = f"\n{fRol.emojiRole(corbeau.role, corbeau.estUnHomme)}   - {corbeau.user.mention}  |  {corbeau.prenom} {corbeau.nom}"
    
### Message
    await corbeau.user.send( contenuMsgCorbeau_Question + contenuMsgCorbeau_Detail )
            
### Attente d'une Réponse
    msgAtt = await fDis.channelAttente.send( contenuMsgCorbeau_Attente )
    pers, aRepondu = await corbeau.attenteMatri_Habitant(v.nuit_hFin)



    if aRepondu :
        village.matricule_choixCorbeaux.append(pers.matri)
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCorbeau_HistoDeb + f"\n     Ce corbeau a choisi {pers.user.mention}.")


    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCorbeau_HistoDeb +  "\n     Ce corbeau n'a choisi personne.")

### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Hirondelle (hirondelle, village):
    
    contenuMsgHirond_Question =  "Bonsoir Hirondelle, qui allez-vous désigner cette nuit ?"
    contenuMsgHirond_Detail   =  "\n```\nVous allez pouvoir choisir une personne de manière anonyme, sa voix comptera triple, pour cela envoyez ici son matricule.\n - Si plusieurs Hirondelles font le même choix que vous, les voix se cumulerons.\n - Si le matricule ne correspond à personne, vous pourrez le retaper\n```"
    
    contenuMsgHirond_Attente  = f"{fDis.Emo_Hirondelle} en tant que {fRol.emojiRole(hirondelle.role, hirondelle.estUnHomme)}   - {hirondelle.user.mention}  |  {hirondelle.prenom} {hirondelle.nom}"
    
    contenuMsgHirond_HistoDeb = f"\n{fRol.emojiRole(hirondelle.role, hirondelle.estUnHomme)}   - {hirondelle.user.mention}  |  {hirondelle.prenom} {hirondelle.nom}"
    
### Message
    await hirondelle.user.send(contenuMsgHirond_Question + contenuMsgHirond_Detail)
            
### Atente d'une Réponse
    msgAtt = await fDis.channelAttente.send(contenuMsgHirond_Attente)
    pers, aRepondu = await hirondelle.attenteMatri_Habitant(v.nuit_hFin)



    if aRepondu :
        village.matricule_choixHirondelles.append(pers.matri)
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgHirond_HistoDeb + f"\n     Cette hirondelle a choisi {pers.user.mention}.")
            
    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgHirond_HistoDeb +  "\n     Cette hirondelle n'a choisi personne.")

### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Juge (juge, village):
    pass





async def fctNoct_FamilleNombreuse (membreFN, village):
    
    contenuMsgFamiNom_Attente = f"{fDis.Emo_FNFrere} en tant que {fRol.emojiRole(membreFN.role, membreFN.estUnHomme)}   - {membreFN.user.mention}  |  {membreFN.prenom} {membreFN.nom}"
    
### Accès aux channels
    await village.salonFamilleNb  .set_permissions ( membreFN.member , read_messages = True , send_messages = True )
    await village.vocalFamilleNb  .set_permissions ( membreFN.member , read_messages = True )
    
### Attente
    msgAtt = await fDis.channelAttente.send(contenuMsgFamiNom_Attente)
    await asyncio.sleep(v.nuit_duree.seconds)
            
    await msgAtt.delete()
            
### Fin de la nuit

    await village.salonFamilleNb  .set_permissions ( membreFN.member , read_messages = True , send_messages = v.famNomb_peuventParler_Journee )
    await village.vocalFamilleNb  .set_permissions ( membreFN.member , read_messages = v.famNomb_peuventParler_Journee )





async def fctNoct_LG (lg, village):
    pass





async def fctNoct_LGNoir (lgNoir, village):
    
    await lgNoir.attente(v.avtP3_duree.seconds)
    
# =============================================================================
#### === Construction du Message ===
# =============================================================================

    if lgNoir.nbInfRestantes >= 2 : s = "s"
    else                          : s = ""
    
    contenuMsgLGNoir_Question = f"Bonsoir Loup-Garou Noir, est-ce que vous souhaitez infecter la victime du conseil pour qu'il devienne un des votres ?\nVous pouvez encore infecter {lgNoir.nbInfRestantes} joueur{s}."
    contenuMsgLGNoir_Detail   =  "\n```\n - Si plusieurs Loups-Garous Noirs infectent la même personne, le loup qui infectera réellement sera choisi au hasard.\n - Si vous ne repondez pas, vous n'infecterez pas.\n```"
    
    contenuMsgLGNoir_HistoDeb = f"{fRol.emojiRole(lgNoir.role, lgNoir.estUnHomme)}   - {lgNoir.user.mention}  |  {lgNoir.prenom} {lgNoir.nom}"
    
    contenuMsgLGNoir_Attente  = f"{fDis.Emo_LGNoir} en tant que {contenuMsgLGNoir_HistoDeb}"
    


# =============================================================================
#### === Coeur de la fonction ===
# =============================================================================

#### VERIF 1 - Nb Infection ?
#        Si il est <= 0, fin de la fonction

    if lgNoir.nbInfRestantes <= 0 :
        pass


#### VERIF 2 - Abstention du conseil ?
#        S'ils n'ont désigné personne, envoie d'un message

    elif village.matriculeHab_choixConseilLG == 0  :
        await lgNoir.user.send("Les Loups-Garous n'ont choisi personne. Donc vous ne pouvez infecter personne.")
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGNoir_HistoDeb + "\n   Ce Loup Noir n'infecte pas cette nuit. (Les Loups n'ont choisi personne)")


#### Si les VERIFS sont OK :

    else :
        
        msgAtt              = await fDis.channelAttente.send(contenuMsgLGNoir_Attente)
        
        
        msgConfirmation_LGN = await lgNoir.user.send(contenuMsgLGNoir_Question + contenuMsgLGNoir_Detail)
        aChoisi_dInfecter   = await fDis.attente_Confirmation(msgConfirmation_LGN, lgNoir.user, timeout = v.part3_duree.seconds)
        
        if aChoisi_dInfecter :
            village.matriculeLGN_quiOntInfecte.append(lgNoir.matri)
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGNoir_HistoDeb + "\n   Ce Loup Noir **infecte** cette nuit !")
        
        else :
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGNoir_HistoDeb + "\n   Ce Loup Noir n'infecte pas cette nuit.")
        
        
        await msgAtt.delete()





async def fctNoct_LGBleu (lgBleu, village):
    return





async def fctNoct_LGBlanc (lgBlanc, village):
    
    contenuMsgLGBlanc_Question =  "Bonsoir Loup-Garou Blanc, nous sommes mercredi soir, la nuit va donc être sanglante... Alors qui souhaitez-vous tuer ?"
    contenuMsgLGBlanc_Detail   =  "\n```\nVous pouvez choisir n'importe quel joueur !\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne choisisez personne, le hasard décidera à votre place !\n```"
    
    contenuMsgLGBlanc_HistoDeb = f"\n{fRol.emojiRole(lgBlanc.role, lgBlanc.estUnHomme)}   - {lgBlanc.user.mention}  |  {lgBlanc.prenom} {lgBlanc.nom}"
    
    contenuMsgLGBlanc_Attente  = f"{fDis.Emo_LGBlanc} en tant que {contenuMsgLGBlanc_HistoDeb}"
    
    
    if  v.ajd.weekday() == 2 :    

### Message
        await lgBlanc.user.send(contenuMsgLGBlanc_Question + contenuMsgLGBlanc_Detail)

### Attente d'une réponse
        msgAtt = await fDis.channelAttente.send(contenuMsgLGBlanc_Attente)
        habTue, aRepondu = await lgBlanc.attenteMatri_Habitant(v.nuit_hFin)

        if not aRepondu :
            habTue = rd.choice(fHab.TousLesHabitants)
            
        village.matriculeHab_tuesLGBlanc.append(habTue.matri)

### Historique et Fin de l'attente
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGBlanc_HistoDeb + f"\n     Ce Loup Blanc a choisi {habTue.user.mention}.")
        await msgAtt.delete()





async def fctNoct_EnfantSauvage (enfSauvage, village):
    
    contenuMsgEnfSauv_Question =  "Bonsoir Enfant Sauvage, quel sera votre modèle ?"
    contenuMsgEnfSauv_Detail   =  "\n```\nPour le choisir, envoyez ici son matricule.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne repondez pas, votre modele vous sera attribué au hasard.\n```"
    
    contenuMsgEnfSauv_HistoDeb = f"{fRol.emojiRole(enfSauvage.role, enfSauvage.estUnHomme)}   - {enfSauvage.user.mention}  |  {enfSauvage.prenom} {enfSauvage.nom}"
    
    contenuMsgEnfSauv_Attente  = f"{fDis.Emo_EnfSauv} en tant que {contenuMsgEnfSauv_HistoDeb}"
    
    
    if v.nbTours == 0 :
        
### Message
        await enfSauvage.user.send(contenuMsgEnfSauv_Question + contenuMsgEnfSauv_Detail)
        
        
### Attente de Réponse
        msgAtt = await fDis.channelAttente.send(contenuMsgEnfSauv_Attente)
        
        modele, aRepondu = await enfSauvage.attenteMatri_Habitant(v.nuit_hFin)
        
        
##  Choix de modele au harsard, de manière à ce qu'il soit différent de pers
        
        if not aRepondu :
            
            modele = enfSauvage
            while modele == enfSauvage :
                modele = rd.choice(fHab.TousLesHabitants)
            
            await enfSauvage.user.send(f"Vous n'avez pas répondu, votre modèle vous a donc été attribué au hasard, c'est : {fMeP.AjoutZerosAvant(modele.matri ,3)}  |  **{modele.prenom} {modele.nom}** en {modele.groupe}.")
        
        
### Ajout du matricule du modele dans Infos Joueurs
        
        fGoo.remplacerVal_ligne_avec(     modele.matri , fGoo.clef_caractRoles , 
                                      enfSauvage.matri , fGoo.clef_Matricule   ,
                                      fGoo.page1_InfoJoueurs                    )
        
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgEnfSauv_HistoDeb + f"\n     A choisi {modele.member.mention}  |  {modele.prenom} {modele.nom} comme modele\n")
        
        
### Fin de l'attente
        await msgAtt.delete()





async def fctNoct_Maire (maire, village):
    
    if maire.estUnHomme : monsieur, le_seul = "Monsieur", "le seul"
    else                : monsieur, le_seul = "Madame"  , "la seule"

#### Attente de Lancement
    
    strEmo_Lancmt               =  "🟢"

    contenuMsgLancmt_Question   = f"Bonsoir {monsieur} le Maire, vous allez pouvoir choisir vos gardes du corps."
    contenuMsgLancmt_Precision  = f"\n> Pour lancer la nomination, réagissez à ce message avec {strEmo_Lancmt} !"
    contenuMsgLancmt_Precision +=  "\n> Vous devez absolument réagir __**après**__ avoir terminé vos activités nocturnes, pour ne pas vous emmêler les pinceaux lors des désignations des matricules !"
    contenuMsgLancmt_Precision +=  "\n> Si vous ne réagissez pas à ce message, vos gardes vous seront atribués au hasard."
    
    contenuMsgMaire_AttenteDeb  = f"{fDis.Emo_Maire}   - {maire.user.mention}  |  {maire.prenom} {maire.nom}  |  {village.nom} - *Attente du début de la fonction nocturne*"
    
    msgAtt_Debut      = await fDis.channelAttente.send(contenuMsgMaire_AttenteDeb)
    messageLancement  = await maire.user.send(contenuMsgLancmt_Question + contenuMsgLancmt_Precision)
    
    lancementAutorise = await fDis.attente_Reaction(messageLancement, maire.user, [[strEmo_Lancmt, True]], timeout = v.nuit_duree.seconds, reponseParDefaut = False)
    
    await messageLancement.delete()
    await msgAtt_Debut.delete()
    
    
    
    
    
    contenuMsgMaire_Question = f"Re-bonsoir {monsieur} le Maire, quels seront vos deux gardes du corps ?\n Pour les choisir, envoyez ici leur matricules un par un !\n __Petite précisions__ : Ils ne vous protègerons **que des attaques nocturnes** et vous serez **{le_seul}** à connaître leur identité !"
    contenuMsgMaire_Detail   =  """\n```\n - Ces gardes du corps seront des "boucliers humains", ils vous protègerons, mais ils le payerons de leur vie...\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne repondez pas, vos gardes vous seront attribués au hasard.\n```"""
    
    contenuMsgMaire_HistoDeb = f"\n{fDis.Emo_Maire}   - {maire.user.mention}  |  {maire.prenom} {maire.nom}"
    
    contenuMsgMaire_Attente  = f"{fDis.Emo_Maire} en tant que {fRol.emojiRole(maire.role, maire.estUnHomme)}   - {maire.user.mention}  |  {maire.prenom} {maire.nom}"
    

#### === Cas 1 : Lancement Autorisé ===

    if lancementAutorise :
        
### Message
        await maire.user.send(contenuMsgMaire_Question + contenuMsgMaire_Detail)
        
        
### Attente de Réponse
        msgAtt = await fDis.channelAttente.send(contenuMsgMaire_Attente)
        
        garde1 = garde2 = None
        aRepondu        = True
                
        while garde1 == garde2  and  aRepondu :
            await maire.user.send("Qui sera votre premier garde ?")
            garde1, aRepondu = await maire.attenteMatri_Habitant(v.nuit_hFin)
                    
            await maire.user.send("Et qui sera le second ?")
            garde2, aRepondu = await maire.attenteMatri_Habitant(v.nuit_hFin)
                    
            if   garde1 == garde2  and  aRepondu :
                await maire.user.send("Vous devez choisir deux gardes différents.\nVous allez pouvoir en choisir de nouveaux !")
        
        await msgAtt.delete()
        
        
        
        
        
#### === Cas 2 : Le Maire n'a pas choisis de garde ===

    if not lancementAutorise  or  not aRepondu :
        
##  Choix des gardes au harsard, de manière à ce qu'il soit différent
        
        garde1 = maire
        
        while garde1.estMaire :
            garde1 = garde2 = rd.choice(village.habitants)
        
        while garde2.estMaire  or  garde1 == garde2 :
            garde2          = rd.choice(village.habitants)
        
        await maire.user.send("Vous n'avez pas répondu, vos gardes vous ont donc été attribués au hasard.")
    
    
    
#### --- Enregistrement ---
    
    maire.gardesMaire.append(garde1.matri)
    maire.gardesMaire.append(garde2.matri)
    
    fGoo.ajoutVal_cellule_avec( f"M{garde1.matri} M{garde2.matri} ", fGoo.clef_caractJoueur,
                                maire.matri                        , fGoo.clef_Matricule   ,
                                fGoo.page1_InfoJoueurs                                       )    
    
    await maire.user.send(f"Vos gardes sont :\n>       {fMeP.AjoutZerosAvant(garde1.matri ,3)}  |  **{garde1.prenom} {garde1.nom}** en {garde1.groupe}\n>       {fMeP.AjoutZerosAvant(garde2.matri ,3)}  |  **{garde2.prenom} {garde2.nom}** en {garde2.groupe}.")
    
    village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgMaire_HistoDeb + f"\n     A choisi {garde1.member.mention} et {garde2.member.mention} comme gardes du corps.\n")





# %%% Ajouts des fonctions nocturnes aux dictionnaires des Roles

fRol.role_Villageois[fRol.clefFctsNoct] = fctNoct_Villageois
fRol.role_VillaVilla[fRol.clefFctsNoct] = fctNoct_Villageois
fRol.role_Cupidon   [fRol.clefFctsNoct] = fctNoct_Cupidon
fRol.role_Ancien    [fRol.clefFctsNoct] = fctNoct_Ancien

fRol.role_Salvateur [fRol.clefFctsNoct] = fctNoct_Salvateur
fRol.role_Sorciere  [fRol.clefFctsNoct] = fctNoct_Sorciere
fRol.role_Voyante   [fRol.clefFctsNoct] = fctNoct_Voyante

fRol.role_Corbeau   [fRol.clefFctsNoct] = fctNoct_Corbeau
fRol.role_Hirondelle[fRol.clefFctsNoct] = fctNoct_Hirondelle
fRol.role_Juge      [fRol.clefFctsNoct] = fctNoct_Juge

fRol.role_Chasseur  [fRol.clefFctsNoct] = fctNoct_Chasseur

fRol.role_FamilleNb [fRol.clefFctsNoct] = fctNoct_FamilleNombreuse

fRol.role_LG        [fRol.clefFctsNoct] = fctNoct_LG
fRol.role_LGNoir    [fRol.clefFctsNoct] = fctNoct_LGNoir
fRol.role_LGBleu    [fRol.clefFctsNoct] = fctNoct_LGBleu

fRol.role_LGBlanc   [fRol.clefFctsNoct] = fctNoct_LGBlanc
fRol.role_EnfantSauv[fRol.clefFctsNoct] = fctNoct_EnfantSauvage





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
    await village.salonConseilLG.set_permissions( LoupGarou.member , read_messages = True  , send_messages = False )
    await village.vocalConseilLG.set_permissions( LoupGarou.member , read_messages = False                         )
    
    
### Fin de l'attente
    await msgAtt.delete()





async def evt_voteLG(memberLG, contenuMsg):
    
    habLG   = fHab.habitant_avec( memberLG.id            )
    village =       village_avec( habLG.numVlg, "numero" )
    
#### Essaye de int le msg
    try :    
        matricule = int(contenuMsg)
    except : 
        matricule = None
    
    
    
#### Si le matricule correspond à quelqu'un en vie
    if village.voteLG_EnCours  and  fHab.habitant_avec(matricule) != None :
        
        """
#   Si ce LG a déjà voté, remplacement du vote
        
        if habLG.matri in village.LG_ayant_votes :
            village.votesConseilLG[ village.LG_ayant_votes.index(habLG.matri) ] = matricule
        
#   Si ce LG n'a pas voté, ajout du vote
        
        else :
            village.LG_ayant_votes.append(habLG.matri)
            village.votesConseilLG.append(matricule)
        """
        
        habLG.choixVote = matricule
        
#   Mise à Jour des Résultats
        
        contenuMsg_resultat, x = depouillement(village, 'LG')
        
        await village.msgResultatLG.edit(content = contenuMsg_resultat)





# %% Event Vote du Village

async def evt_voteVlg (memberVlg, contenuMsg):
    
    habVlg  = fHab.habitant_avec( memberVlg.id            )
    village =       village_avec( habVlg.numVlg, "numero" )
    
    if village.typeScrutin != None :
        
#### Essaye de int le msg
        try :
            matriculeHab_Choisi = int(contenuMsg)
        except :
            matriculeHab_Choisi = None
        
        
#### Si le matricule correspond à quelqu'un en vie
        if fHab.habitant_avec( matriculeHab_Choisi ) != None :
            
            habVlg.choixVote = matriculeHab_Choisi
            
            village.msgHistorique_votes = await fDis.ajoutMsg(village.msgHistorique_votes, f"\n   - {habVlg.user.mention} vote {habVlg.nbVote} fois pour {habVlg.choixVote}\n") 
            
            contenuMsg_resultat, village.resultatVote = depouillement(village)
            await village.msgResultat.edit(content = "Voici les résultats du vote :\n" + contenuMsg_resultat)





# %% Commandes Village

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



async def cmd_vote(memberVlg, matricule):
    
    habVlg  = fHab.habitant_avec( memberVlg.id            )
    village =       village_avec( habVlg.numVlg, "numero" )
    
    verifLG_Camp = habVlg.role[fRol.clefCamp] == fRol.campLG
    verifLG_Infe = habVlg.estInf
    verif_LGBlan = habVlg.role == fRol.role_LGBlanc
    verif_EnfSau = habVlg.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(habVlg.pereProtecteur) == None
            
    if village.voteLG_EnCours  and  (verifLG_Camp  or  verifLG_Infe  or  verif_LGBlan  or  verif_EnfSau) :
        await evt_voteLG(memberVlg, matricule)
        
    else :
        await evt_voteVlg(memberVlg, matricule)
    
    

async def cmd_demandeExilVote (member) :
    
    hab = fHab.habitant_avec(member.id)

#### Cas ou un maire est aussi juge

    if hab.estMaire  and  (hab.role == fRol.role_Juge  and  hab.nbExilRest >= 0):
        contenuMsg_Maire_ou_Juge  = "Vous êtes à la fois Maire (🎖️) et Juge (⚖️), sous quel rôle souhaitez-vous exiler la victime du village ? \n> *Choisissez le ⚫  pour annuler l'exil.*" 
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
    
    