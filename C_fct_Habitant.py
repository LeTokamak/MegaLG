# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---               Niveau C - Classe et Fonctions liées aux Habitants               ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

#Niveau B
import B_fct_Groupe           as fGrp
import B_fct_Roles            as fRol

#Niveau A
fGoo = fGrp.fGoo
fDis = fGrp.fDis
fMeP = fGrp.fMeP
v    = fGrp.v


import asyncio
rd   = fMeP.rd





#### Phrases de Mort

inv = "invariable"


mortPhrases_Matin = [
    ("#PRENOM# ne s'est pas réveillé ce matin..."  ,
     "#PRENOM# ne s'est pas réveillée ce matin..." ) ,
    
    ("On a retrouvé plusieurs fois #PRENOM# dans la forêt", 
     inv                                                  ) ,
    
    ("""#PRENOM# a été retrouvé mort chez lui ce matin...\nD'après les voisins ses derniers mots avant de mourir étaient "Gaaaaarg ! Graaa... mnnmnmnmn......." """  ,
     """#PRENOM# a été retrouvé morte chez elle ce matin...\nD'après les voisins ses derniers mots avant de mourir étaient "Gaaaaarg ! Graaa... mnnmnmnmn......." """) ,
    
    ("Oh bah nooon, #PRENOM# a été décapité...\nQui est l'enflure qui a osé faire cela ?\nRetrouvez-le au plus vite avant qu'il ne sévisse de nouveau...", 
     inv                                                                                                                                                 ) ,
    
    ("Il est mort, **cheh** !"   ,
     "Elle est morte, **cheh** !") ,
    
    ("Rip, #PRENOM# a été assassiné, d'après les infos du Petit Isenien, il serait mort dans le capitole du village, en tentant de protéger le pupitre sacré..."    , 
     "Rip, #PRENOM# a été assassiné, d'après les infos du Petit Isenien, elle serait morte dans le capitole du village, en tentant de protéger le pupitre sacré..." ) ,
    
    ("Après avoir entendu un bruit inquiétant dans sa grange cette nuit, #PRENOM# est allé voir ce qu'il s'y passait...\nLe lendemain, ce **tocard** fut retrouvé en plusieurs morceaux, éparpillés dans la cour..."      , 
     "Après avoir entendu un bruit inquiétant dans sa grange cette nuit, #PRENOM# est allée voir ce qu'il s'y passait...\nLe lendemain, cette **idiote** fut retrouvée en plusieurs morceaux, éparpillés dans la cour..." ) ,
    
    ("#PRENOM# adorait son cheval, maintenant c'est lui qui l'adore !" , 
     inv                                                               ) ,
    
    ("""*"Il a vécu comme un sage... Et il est mort comme un con"*\n__Tycho Brahé__"""        ,
     """*"Elle a vécu comme un sage... Et elle est morte comme un conne"*\n__Tycho Brahé__""" )
    ]


mortPhrases_Soir  = [
    ("#PRENOM# finira sa journée sur le bûcher..." , 
     inv                                           ) ,
    
    ("#PRENOM# s'est tu bien avant de s'éteindre"  ,
     "#PRENOM# s'est tue bien avant de s'éteindre" ) ,
    
    ("""#PRENOM# a dit sur le bûcher "Je veux descendre !"...\nLe bourreau a répondu "Des **cendres** ? Ok" """ ,
     inv                                                                                                        ) ,
    
    ("Hoo, zut, #PRENOM# est mort, quel domage !\n(¬‿¬) "  ,
     "Hoo, zut, #PRENOM# est morte, quel domage !\n(¬‿¬) " ) ,
    
    ("Alors que le bûcher n'était pas allumé, #PRENOM# se prit **une enclume** en pleine tête !\nUne mesure écologique selon certain, un défouloir pour d'autres... Enfin dans tous les cas, il va falloir la nettoyer maintenant, l'enclume !" , 
     inv                                                                                                                                                                                                                                        )
    ]





mortPhrases_Homme_AmourDe_Hom = [
    "#PRENOM# est parti se perdre dans la forêt après la mort de son merveilleux #aPRENOM#...", 
    "*#aPRENOM# #aPRENOM# #aPRENOM#, je n'aime pas te savoir seul*\nC'est ce que disait la lettre qu'on a trouvée chez #PRENOM# en revanche lui, on ne l'a jamais retrouvé...",
    "Durant leur séance de coït, #aMENTION# est mort...\nNous avons également retrouvé #PRENOM# en pls à coté de son amant.\nLes rumeurs disent qu'il s'est suicidé à l'aide d'une bouteille de poison..."
    ]


mortPhrases_Homme_AmourDe_Fem = [
    "#PRENOM# est parti se perdre dans la forêt après la mort de sa merveilleuse #aPRENOM#...", 
    "*#aPRENOM# #aPRENOM# #aPRENOM#, je n'aime pas te savoir seule*\nC'est ce que disait la lettre qu'on a trouvée chez #PRENOM#, en revanche lui, on ne l'a jamais retrouvé...",
    "Durant leur séance de coït, #aMENTION# est morte...\nNous avons également retrouvé #PRENOM# en pls à coté de son amant.\nLes rumeurs disent qu'il s'est suicidé à l'aide d'une bouteille de poison..."
    ]


mortPhrases_Femme_AmourDe_Hom = [
    "#PRENOM# est partie se perdre dans la forêt après la mort de son merveilleux #aPRENOM#...", 
    "*#aPRENOM# #aPRENOM# #aPRENOM#, je n'aime pas te savoir seul*\nC'est ce que disait la lettre qu'on a trouvée chez #PRENOM#, en revanche elle, on ne l'a jamais retrouvée...",
    "Durant leur séance de coït, #aMENTION# est mort...\nNous avons également retrouvé #PRENOM# en pls à coté de son amant.\nLes rumeurs disent qu'elle s'est suicidée à l'aide d'une bouteille de poison..."
    ]


mortPhrases_Femme_AmourDe_Fem = [
    "#PRENOM# est partie se perdre dans la forêt après la mort de sa merveilleuse #aPRENOM#...", 
    "*#aPRENOM# #aPRENOM# #aPRENOM#, je n'aime pas te savoir seule*\nC'est ce que disait la lettre qu'on a trouvée chez #PRENOM#, en revanche elle, on ne l'a jamais retrouvée...",
    "Durant leur séance de coït, #aMENTION# est morte...\nNous avons également retrouvé #PRENOM# en pls à coté de son amant.\nLes rumeurs disent qu'elle s'est suicidée à l'aide d'une bouteille de poison..."
    ]






class Habitant :
    
    def __init__ (self, matricule, prenom, nom, numeroGroupe, numeroVillage, sexe, idDiscord, nomRole, caractRole, caractPers) :

#### Constantes Personnelles
        
        self.matri   = matricule
        
        self.prenom  = prenom
        self.nom     = nom
        
        self.numGrp  = numeroGroupe
        self.groupe  = None
        
        self.numVlg  = numeroVillage 
        
        self.user    = fDis.bot          .get_user  (idDiscord)
        self.member  = fDis.serveurMegaLG.get_member(idDiscord)
        self.idDis   = idDiscord
        
        self.role    = fRol.role_avec(nomRole, "nom")
        
        if sexe == "H" : self.estUnHomme = True
        if sexe == "F" : self.estUnHomme = False
        
        self.choixVote = 0
        self.nbVote    = 1
        
        self.estMorte  = False
        
        
#### Variables de Role
        
        caractRole = str(caractRole)
        
        if   self.role == fRol.role_Cupidon :
            self.couple         = caractRole.split()

        elif self.role == fRol.role_EnfantSauv :
            try    : self.pereProtecteur = int(caractRole)
            except : self.pereProtecteur = self.matri
        
        elif self.role == fRol.role_LGNoir :
            self.nbInfRestantes = int(caractRole)
            
        elif self.role == fRol.role_Sorciere :
            potions = caractRole.split()
            self.nbPotionsVie   = int(potions[0])
            self.nbPotionsMort  = int(potions[1])
        
        elif self.role == fRol.role_Ancien :
            self.nbProtectRest  = int(caractRole)
            
        elif self.role == fRol.role_Juge :
            self.nbExilRest     = int(caractRole)
        
        
#### Variables Personnelles
        
        caractPersonelles = str(caractPers).split()
        
        self.estInf       = False
        
        self.estAmoureux  = False
        self.amants       = []
        
        self.estMaire     = False
        self.gardesMaire  = []
        
        for c in caractPersonelles :
            if   "Infecté" == c :
                self.estInf      = True
            
            elif "A" in c and not self.estAmoureux :
                self.estAmoureux = True
                self.amants      = [ int(c[1:]) ]
                
            elif "A" in c and     self.estAmoureux :
                self.amants.append ( int(c[1:]) )
                
            elif "Maire" == c :
                self.estMaire = True
                
            elif "M" in c :
                self.gardesMaire.append( int(c[1:]) )
            
        
#### ||| Variante ||| Donne 2 voix de plus au maire lors des votes
        
        if self.estMaire  and  v.vote_maire_plus2Voix :
            self.nbVote += 2
        
        
#### Fonctions de Vérifications
        
        def verif_Msg_DMChannel(msg):
            return msg.author == self.user  and  type(msg.channel) == fDis.discord.channel.DMChannel
        
        self.verif_Msg_DMChannel = verif_Msg_DMChannel





    async def init_groupe(self):
        
        self.groupe = await fGrp.groupe_avec(self.numGrp, "numero")
        
        if v.phaseEnCours == v.phase1 :
            await fGrp.autorisation_SalonsGrp(self.member, self.numGrp)





# %%% Meurtre
    
    async def Tuer (self, meurtreNocturne = True, suicideAmoureux = False, premAmoureuxTue = None, departServeur = False):

        self.estMorte = True
        await fDis.channelHistorique.send(f"Tentative de meurtre de {self.matri} {self.prenom} {self.nom} {self.groupe}  |  {self.user.mention} {self.user}")



# -----------------------------------------------
# ---  Retire le joueur de Infos Joueurs      ---
# -----------------------------------------------

        fGoo.suppressionLigne_avec( self.matri                         , 
                                    fGoo.clef_Matricule                ,
                                    fGoo.page_fichier(fGoo.InfoJoueurs) )
        


# -----------------------------------------------
# ---  Création de l'embed d'annonce de mort  ---
# -----------------------------------------------

        if self.estUnHomme : Il, e, amoureux = "Il"  , "" , "amoureux"
        else               : Il, e, amoureux = "Elle", "e", "amoureuse"

### Titre de l'embed

        titreEmbed = f"**{self.prenom} {self.nom}** en {self.groupe}"


### Détails de l'embed
        
        Details = ""
        
        if   self.estInf  and  self.estAmoureux :
            Details = f"{Il} était infecté{e} et {amoureux} de "
            
        elif self.estInf :
            Details = f"{Il} était infecté{e}"
            
        elif self.estAmoureux :
            Details = f"{Il} était {amoureux} de "
            
        
        if self.estAmoureux :
            for matri in self.amants :
                amoureux = habitant_avec(matri, autorisationMort = True)
                Details += f"{amoureux.prenom} {amoureux.nom} en {amoureux.groupe}"
                
                if len(self.amants) >= 2  and  matri != self.amants[-1] :
                    Details += " et de "
                
                    
            if departServeur :
                if len(self.amants) == 1 : Details += "\nSon amant ne sera pas tué"
                else                     : Details += "\nSes amants ne seront pas tués"
        
            
### Image du Role de l'embed

        urlImageRole = fRol.imageRole(self.role, self.estUnHomme)
        
        
### Couleur de l'embed
    
        if   departServeur :
            couleurEmbed = 0x000000
        
        elif suicideAmoureux :
            couleurEmbed = fMeP.couleurRandom("amour")
            
        elif meurtreNocturne :
            couleurEmbed = fMeP.couleurRandom("matin")
            
        else :
            couleurEmbed = fMeP.couleurRandom("soir")


### Description de l'embed

        if   departServeur :
            descripEmbed = f"*{Il} a été tué{e} car {Il.lower()} a quitté le serveur.*"
        
        
        else :
            
            if suicideAmoureux :
                if     self.estUnHomme and     premAmoureuxTue.estUnHomme : finsDePhrases = mortPhrases_Homme_AmourDe_Hom
                if     self.estUnHomme and not premAmoureuxTue.estUnHomme : finsDePhrases = mortPhrases_Homme_AmourDe_Fem
                if not self.estUnHomme and     premAmoureuxTue.estUnHomme : finsDePhrases = mortPhrases_Femme_AmourDe_Hom
                if not self.estUnHomme and not premAmoureuxTue.estUnHomme : finsDePhrases = mortPhrases_Femme_AmourDe_Fem
                                    
                descripEmbed = rd.choice(finsDePhrases)

                descripEmbed = descripEmbed.replace( "#aPRENOM#" , premAmoureuxTue.prenom                                          )
                descripEmbed = descripEmbed.replace( "#aNOM#"    , premAmoureuxTue.nom                                             )
                descripEmbed = descripEmbed.replace( "#aGROUPE#" , str(premAmoureuxTue.groupe)                                     )
                descripEmbed = descripEmbed.replace( "#aROLE#"   , premAmoureuxTue.role[fRol.clefNom]                              )
                descripEmbed = descripEmbed.replace( "#aEMOJI#"  , fRol.emojiRole(premAmoureuxTue.role,premAmoureuxTue.estUnHomme) )
                descripEmbed = descripEmbed.replace( "#aMENTION#", str(premAmoureuxTue.user.mention)                               )
            
            
            else :
                
                if   meurtreNocturne : Phrases      = rd.choice(mortPhrases_Matin)
                else                 : Phrases      = rd.choice(mortPhrases_Soir )
                    
                if   self.estUnHomme : descripEmbed = Phrases[0]
                else                 : descripEmbed = Phrases[1]
                    
                if descripEmbed == inv : descripEmbed = Phrases[0]
            
            
            descripEmbed = descripEmbed.replace    (  "#PRENOM#" , self.prenom                                                     )
            descripEmbed = descripEmbed.replace    (  "#NOM#"    , self.nom                                                        )
            descripEmbed = descripEmbed.replace    (  "#GROUPE#" , str(self.groupe)                                                )
            descripEmbed = descripEmbed.replace    (  "#ROLE#"   , self.role[fRol.clefNom]                                         )
            descripEmbed = descripEmbed.replace    (  "#EMOJI#"  , fRol.emojiRole(self.role,self.estUnHomme)                       )
            descripEmbed = descripEmbed.replace    (  "#MENTION#", str(self.user.mention)                                          )
        
        
        
### Réalisation de l'embed    
        
        AnnonceMort = fDis.discord.Embed(title = titreEmbed, description = descripEmbed, color = couleurEmbed)
        AnnonceMort.set_thumbnail(url = urlImageRole)
        
        if Details != "" :
            AnnonceMort.set_footer(text = Details)
        
#   Envoie de AnnonceMort
        
        await fDis.channelBucher.send(embed = AnnonceMort)
        
        
        
# ---------------------------------------------------------
# ---  Gestions des roles, des amoureux et de la tombe  ---
# ---------------------------------------------------------
        
        if not departServeur :
            
##  Changement des Roles
            
            await self.member.remove_roles( fDis.roleJoueurs )
            await self.member.   add_roles( fDis.roleMorts   )
            
            await self.member.edit(nick = self.member.nick[6:])
            
##  Meurtre des éventuels Amoureux
            
            if self.estAmoureux :
                
                for matri in self.amants :
                    if not habitant_avec(matri, autorisationMort = True).estMorte :
                        await habitant_avec(matri).Tuer(suicideAmoureux = True, premAmoureuxTue = self)
            
##  Lancement de la fonction Cimetiere
            
            asyncio.create_task( cimetiere(habitant = self), name = f"Lancement cimetière de {self.prenom} {self.nom}." )

    


    
# %%% Vote
    
    def vote (self, vote):
        """
        Essaye de int contenuBulletin
        
        Si l'opération fonctionne, la fonction vérifie que le matricule correspond à quelqu'un
            Si c'est le cas la voix est comptée et la fonction retourne True

        Sinon la fonction retourne False
        """
        

        self.choixVote = vote
        return True

                


    



    async def Defense_1erTour (self, heureFinAttente, msgDefense):
        
#### Message

        await self.user.send("Vous avez été choisi par le village lors du premier tour, mais vous pouvez encore vous défendre !```\nLe prochain message que vous enverez ici sera votre défense, vous ne pourrez pas la modifier une fois quelle sera envoyée !\n - Il n'y a aucune restriction pour votre message, donc soyez créatif ! Enfin surtout convaincant !!!\n```")


#### Attente de Réponse

        msgAtt = await fDis.channelAttente.send(f"{fDis.Emo_BabyOrange} en tant que {fRol.emojiRole(self.role,self.estUnHomme)}   - {self.user.mention}  |  {self.prenom} {self.nom}")
        defenseRecu, aRepondu = await self.attenteMessage(heureFinAttente, self.verif_Msg_DMChannel)


#### Si une réponse à été reçu

        if aRepondu :
            Defense = fDis.discord.Embed(title = f"Défense de {self.prenom}", description = defenseRecu.content, color = fMeP.couleurRandom("a"))
        
            await msgDefense.edit(embed = Defense)


#### Fin de l'attente

        await msgAtt.delete()





# %%% Attente 

    async def attente(self, tempsAtt) :
        """tempsAtt est en secondes"""

### Début de l'attente
        msgAtt = await fDis.channelAttente.send(f"{fDis.Emo_BabyRed} en tant que {fRol.emojiRole(self.role, self.estUnHomme)}   - {self.user.mention}  |  {self.prenom} {self.nom}")
        await asyncio.sleep(tempsAtt)
        
### Fin de l'attente
        await msgAtt.delete()

    



    async def attenteMessage(self, heureFinAttente, verif = None):
        """Par défaut verif est égal à self.verif_Msg_DMChannel
        
           Attend une réponse (sous forme de Message) jusqu'à heureFinAttente
            - Si un message est reçu, la méthode renvoie :
                Le message en question, True  (a répondu)
            
            - Sinon, la méthode renvoie : 
                None (aucun msg)      , False (n'a pas répondu)
        """
        
        if verif == None : 
            verif = self.verif_Msg_DMChannel
        
        tempsAttente = ( heureFinAttente - v.maintenant() ).seconds
        
        
        try : 
            message = await fDis.bot.wait_for('message', check = verif, timeout = tempsAttente)
            return message, True
            
        except :
            pass
        
        return None, False





    async def attenteMatri_Habitant(self, heureFinAttente, verif = None, autorisation_AutoDesignation = False, autorisation_AutreVillage = False, verification_MaticuleChoisi = True):
        """
        Par défaut verif est égal à self.verif_Msg_DMChannel
        
        Methode vérifiant que le message entré est bien un entier correspondant à un habitant
        Renvoie un objet Habitant et un booléen indiquant si self a répondu
        """
        
        messagesEnvoyes = []
        
        estCertain      = False
        matricule       = ""
        
        while  not estCertain  or  habitant_avec(matricule) == None  or  (matricule == self.matri  and  not autorisation_AutoDesignation)  or  (habitant_avec(matricule).numVlg != self.numVlg  and  not autorisation_AutreVillage):
        
#### Attente d'un entier
            
            while type(matricule) != int :
                
                messageReponse, aRepondu = await self.attenteMessage(heureFinAttente, verif)
                
##  Si aucune réponse n'a été reçu avant heureFinAttente
                
                if not aRepondu :
                    for m in messagesEnvoyes :
                        await m.delete()
                    
                    return None, aRepondu
                
##  Essaye de int le matricule
                
                try :
                    matricule = int(messageReponse.content)
                
                except :
                    messagesEnvoyes.append( await self.user.send("**Votre message n'était pas un entier.**\nVous pouvez envoyer un nouveau matricule !") )
                    matricule = ""
                
                
                
            persChoisie = habitant_avec(matricule)
            
            
            
            
#### Vérifie si le matricule correspond à quelqu'un qui existe
            
            if   persChoisie == None :
                messagesEnvoyes.append( await self.user.send("**Ce matricule ne correspond à personne.**\nVous pouvez envoyer un nouveau matricule !") )
                matricule = ""
            
            
            
#### Vérifie si le matricule correspond à celui de self
            
            elif persChoisie == self  and  not autorisation_AutoDesignation :
                messagesEnvoyes.append( await self.user.send("**Vous ne pouvez pas vous choisir vous-même.**\nVous pouvez envoyer un nouveau matricule !") )
                matricule = ""
            
            
            
#### Vérifie si le matricule correspond à celui de quelqu'un d'un autre village
            
            elif habitant_avec(matricule).numVlg != self.numVlg  and  not autorisation_AutreVillage :
                messagesEnvoyes.append( await self.user.send("**Vous devez choisir un habitant de votre village.**\nVous pouvez envoyer un nouveau matricule !") )
                matricule = ""
            
            
            
#### Etes-vous certain de ce choix ?
            
            elif verification_MaticuleChoisi :
                
                nbMinutesAttente_Max = 5
                
                msgVerif = await self.user.send(f"Vous avez choisi **{persChoisie.prenom} {persChoisie.nom}** en {persChoisie.groupe}, est-ce que vous êtes certains de ce choix ?```\nSi oui, régissez avec ✅.\nSinon choisissez ❌, vous pourrez ensuite retaper le matricule.\n - Vous avez moins de {nbMinutesAttente_Max} mins pour réagir, sinon votre choix sera validé.```")
                messagesEnvoyes.append( msgVerif )
                
                
##  Calcul du temps d'attente
                
                m = v.maintenant()
                tempsAttenteVerif_Maximal = v.timedelta(minutes = nbMinutesAttente_Max)
                
                if  tempsAttenteVerif_Maximal  + m >= heureFinAttente :
                    tempsAttenteVerif_Effectif      = heureFinAttente - m
                
                else :
                    tempsAttenteVerif_Effectif      = tempsAttenteVerif_Maximal
                
                
##  Attente d'une réaction
                
                estCertain = await fDis.attente_Confirmation(msgVerif, self.user, timeout = tempsAttenteVerif_Effectif.seconds)
            
            else :
                estCertain = True
        
        
        
#### Conclusion
        
        for msg in messagesEnvoyes :
            await msg.delete()
        
        if   persChoisie.estUnHomme : e = ""
        else                        : e = "e"
        
        await self.user.send(f"**{persChoisie.prenom} {persChoisie.nom}** a bien été choisi{e} !")        
        
        return habitant_avec(matricule), aRepondu





# %% Fonctions Habitant

TousLesHabitants = []

async def redef_TousLesHabitants():

    global TousLesHabitants
    TousLesHabitants = []    

    Joueurs = fGoo.donneeGoogleSheet( fGoo.page1_InfoJoueurs )

    for j in Joueurs :
        
        nouvelHab = Habitant( j[fGoo.clef_Matricule   ] ,
                              j[fGoo.clef_Prenom      ] ,
                              j[fGoo.clef_Nom         ] ,
                              j[fGoo.clef_Groupe      ] ,
                              j[fGoo.clef_numVillage  ] ,
                              j[fGoo.clef_Sexe        ] ,
                              j[fGoo.clef_idDiscord   ] ,
                              j[fGoo.clef_Role        ] ,
                              j[fGoo.clef_caractRoles ] ,
                              j[fGoo.clef_caractJoueur]  )
        
        await nouvelHab.init_groupe()
        
        TousLesHabitants.append( nouvelHab )





def habitant_avec(info, autorisationMort = False) :
    """Revoie un objet Habitant, qui correspond à l'information donnée en argument
    
       Cette info peut être : - Un identifiant Discord
                              - Un matricule
                              - Un User (discord.user.User)
                              
       Si   , ce type d'information n'est pas géré par habitant_avec
            , personne ne corespond à cette information
            , l'habitant correspondant est mort
         
       Alors, habitant_avec renvoie None
    """
    
    persCorrespondante = ""



#### info est un identifiant Discord

    if   type(info) == int  and  info > 10**16 :
        
        for p in TousLesHabitants :
            if p.idDis == info      : persCorrespondante = p
    
    
#### info est un matricule
    
    elif type(info) == int  and  info < 10**6  :
        
        for p in TousLesHabitants :
            if p.matri == info      : persCorrespondante = p
    
    
#### info est un User
    
    elif type(info) == fDis.discord.user.User       :
        
        for p in TousLesHabitants :
            if p.idDis == info.id   : persCorrespondante = p





#### Verification finale
    
    if   type(persCorrespondante) == Habitant  and  (autorisationMort  or  not persCorrespondante.estMorte) :
        return persCorrespondante
    
    else :
        return None







# %% Fonction Cimetière

async def cimetiere (habitant = None, message = None, rappelDeFonction = False):
    """
    La fonction cimetiere gère la dernière demeure d'un Habitant, sa Tombe...
    
        Si la fonction est appelée pour la première fois, elle envoie un message au concerné
    pour l'informer de son destin, on y envera un message d'attente de réponse et un message
    qui l'informe de l'écriture
       
        Si la fonction est rappelée (lors d'un cycling par exemple), elle va récuperer les 
    infos se trouvant dans msgAtt envoyé lors du 1er appel de la fonction.
        Elle va ensuite relancer l'attente de l'épitaphe
    """



# %%%  Partie 1 - Initialisation des Variables

#### Cas où la fonction est appelée pour la première fois pour cet habitant 

    if not rappelDeFonction :
        HDeces = v.maintenant()
        msgAtt = await fDis.channelAttente.send(f"{fDis.Emo_Red} en tant que {fRol.emojiRole(habitant.role, habitant.estUnHomme)}   - {habitant.user.mention}  |  {habitant.prenom} {habitant.nom}     <| {HDeces.year} {HDeces.month} {HDeces.day} {HDeces.hour} {HDeces.minute} {int(habitant.estUnHomme)} {habitant.prenom.replace(' ','_')} {habitant.nom.replace(' ','_')} {habitant.groupe.replace(' ','_')} {habitant.role.replace(' ','_')} {habitant.idDis} {int(False)} |>")

## Définition des variables utilisées ensuite

        EstUnHomme = habitant.estUnHomme
        Prenom     = habitant.prenom
        Nom        = habitant.nom
        Groupe     = habitant.groupe
        Role       = habitant.role
        User       = habitant.user
        EpiRecue   = False
    
##  Annonce (si c'est la première fois que j'attend une réponse)

        if HDeces.hour < 17 : Bonjour = "Bonjour"
        else                : Bonjour = "Bonsoir"
        
        Annonce = f"{Bonjour} {Prenom}, il va falloir inscrire quelque chose sur votre tombe, quel sera votre épitaphe ?\n```\nPetits détails : - Le prochain message que vous enverrez ici partira directement sur votre tombe.\n                 - Votre épitaphe sera lu avant d'être publiée et pourra être censurée, et vous ne pourrez pas en choisir de nouvelle.\n                 - Vous pouvez indiquer les soupçons que vous avez sur les autres joueurs.```"#\n                 - Travaillez votre épitaphe, la plus mémorable sera récompensée !
    
        await habitant.user.send(Annonce)





####  Cas où la fonction cimetière est rappelée
    
    else :
        msgAtt  = message
        contenu = message.content.split()
        infos   = contenu[ contenu.index("<|")+1 : -1 ]

## Définition des variables utilisées ensuite

        HDeces     = v.datetime(int(infos[0]), int(infos[1]), int(infos[2]), int(infos[3]), int(infos[4]), tzinfo = v.HParis)
        EstUnHomme = bool(int(infos[5]))
        Prenom     = infos[6].replace('_',' ')
        Nom        = infos[7].replace('_',' ')
        Groupe     = infos[8].replace('_',' ')
        Role       = infos[9].replace('_',' ')
        User       = fDis.bot.get_user(int(infos[10]))
        EpiRecue   = bool(int(infos[11]))







# %%% Partie 2 - Attente de l'épitaphe

#### Cas où l'épitaphe n'a pas été reçue
    
    if not EpiRecue :
    
##########################
### Attente de réponse ###
##########################
               
        msgEpitaphe = await fDis.attente_Message(User, accuseReception = True)

        await msgAtt.edit(content = msgAtt.content[:-4] + "1" + msgAtt.content[-3:])



##################################
### Vérification de l'épitaphe ###
##################################

        msgAutorisation   = await fDis.userCamp.send(f"Voici l'épitaphe choisie par {Prenom} {Nom} {Groupe} {User.mention}, qui était {Role}, est-ce qu'elle convient ?\n>>> {msgEpitaphe.content}")
  
        epitapheAutorisee = await fDis.attente_Confirmation(msgAutorisation, fDis.userCamp)


### L'épitaphe convient

        if epitapheAutorisee :
            epitaphe = msgEpitaphe.content
  
    
  ### L'épitaphe ne convient pas, correction de l'épitaphe et enventuelle censure

        else :
            await fDis.bot.userCamp.send(f"La première épitaphe envoyée ne convenait pas...\nLe prochain message envoyée sera l'épitaphe de {Prenom} {Nom}, si ce message est dans ('C','c'), alors l'épitaphe sera entièrement censurée")
            
            msgEpitaphe_corrigee = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
            

            if msgEpitaphe_corrigee.content in "cCç" :
                epitaphe = "*Cette épitaphe a été entièrement censurée...*"

            else :
                epitaphe = msgEpitaphe_corrigee.content





#### Cas où l'épitaphe a été déjà été recue
      
### L'épitaphe n'a pas été sauvegardé, Clément doit donc la renvoyée

    else :
        
###############################################
### Attente de la réaction de fDis.userCamp ###
###############################################

        msgAttCamp = await fDis.userCamp.send(f"Attente de l'épitaphe de {Prenom} {Nom} {Groupe} étant {Role}. Réagi avec ✅ pour envoyer son épitaphe. (toujours 'c' pour censurer)")
        await msgAttCamp.add_reaction("✅")
        
        def checkEmoji(reaction, user):
            return msgAttCamp.id == reaction.message.id  and  str(reaction.emoji) == "✅"  and  user == fDis.userCamp
    
        reaction, user = await fDis.bot.wait_for("reaction_add", check = checkEmoji)

        await msgAttCamp.delete()
        
        

#############################
### Attente de l'épitaphe ###
#############################
        
        nouvMsgAtt  = await fDis.userCamp.send(f"Envoie l'épitaphe de {Prenom} {Nom}.")
        
        msgEpitaphe = await fDis.attente_Message(fDis.userCamp, accuseReception = True)
        
        await nouvMsgAtt.delete()
        
        
##  Correction de l'épitaphe et enventuelle censure
        
        if msgEpitaphe.content in "cCç" :
            epitaphe = "*Cette épitaphe a été entièrement censurée...*"
            
        else :
            epitaphe = msgEpitaphe.content





# %%% Partie 3 - Envoie de la Tombe
    
    if EstUnHomme : Decede, Il = "décédé" , "Il"
    else          : Decede, Il = "décédée", "Elle"
    
    urlImageRole = fRol.imageRole(Role, EstUnHomme)
    
    Tombe = fDis.discord.Embed(title = f"**{Prenom} {Nom} **", description = epitaphe, color = fMeP.couleurRandom('t'))
    Tombe.set_footer(text = f"{Il} était en {Groupe} et {Il.lower()} est {Decede} le {HDeces.day} {fMeP.mois(HDeces.month)} {HDeces.year} à {fMeP.AjoutZerosAvant(HDeces.hour,2)} : {fMeP.AjoutZerosAvant(HDeces.minute,2)}")
    Tombe.set_thumbnail(url = urlImageRole)
    
    await fDis.channelCimetiere.send(embed = Tombe)
    
    await msgAtt.delete()

