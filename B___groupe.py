# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---             Niveau B - Classes et Fonctions de Gestion des Groupes             ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

# Niveau A
import A___variables          as v
import A___google             as fGoo
import A___discord            as fDis
import A___mise_en_page       as fMeP


rd = fMeP.rd

import asyncio



Emo_departGroupe = "❌"

separateur = "↘"

class GroupeParDefaut :

    numero      = 0    

    cheminBrut  =  ""
    chemin      = [""]
    rang        = 0
    nom         = "*Aucun Groupe*"
    
    sur_Groupes = []
    salon       = None
    
    
    def __str__(self):
        return self.nom



class Groupe :
        
    def __init__ (self, numGroupe, cheminBrut):
        
        self.numero      = numGroupe
        
        self.cheminBrut  = cheminBrut
        self.chemin      = cheminBrut.split(separateur)
        self.rang        = len(self.chemin)
        self.nom         = self.chemin[-1]
        
        self.sur_Groupes = []
        
        self.salon       = None
        
        self.MsgSortie   = None
        self.MsgEntree   = None
        self.Emo_Entree  = None
    
    
    
    
    
    async def init_surGroupes(self, creation_si_existe_pas = True):
        
        for i in range(1, self.rang) :
            g_cheminBrut = separateur.join( self.chemin[:i] )
            
            groupe = await groupe_avec( g_cheminBrut, "chemin", creation_si_existe_pas )
            
            self.sur_Groupes.append( groupe )
            
            
#### Définition du salon du groupe supérieur 
    
        if   self.rang == 1 :
            self.salon_GroupeSup = fDis.channelFctmentGrp
                
        elif self.rang in [2,3,4]:
            self.salon_GroupeSup = self.sur_Groupes[-1].salon        
    
    
    
    
    
    async def creation_salonEtMessages (self):       
        
# =============================================================================
#### Création du Salon du Groupe
# =============================================================================

### Clonage d'un des salons de référence, pour créer le salon

        if self.rang == 1 : 
            self.salon = await fDis.channelGalaxie.clone( name = fDis.channelGalaxie.name[:2] + self.nom )
            await self.salon.edit(position = fDis.channelGalaxie.position + 1, topic = str(self))
                
        if self.rang == 2 : 
            self.salon = await fDis.channelEtoile .clone( name = fDis.channelEtoile .name[:2] + self.nom )
            await self.salon.edit(position = fDis.channelEtoile .position + 1, topic = str(self))
                
        if self.rang == 3 : 
            self.salon = await fDis.channelPlanete.clone( name = fDis.channelPlanete.name[:2] + self.nom )
            await self.salon.edit(position = fDis.channelPlanete.position + 1, topic = str(self))
                
        if self.rang == 4 : 
            self.salon = await fDis.channelLune   .clone( name = fDis.channelLune   .name[:2] + self.nom )
            await self.salon.edit(position = fDis.channelLune   .position + 1, topic = str(self))

        
        
# =============================================================================
#### Création du Message de Sortir sur lequel réagir pour quitter le groupe
# =============================================================================
        
        contenu_MsgSortie = f"**Bonjour et bienvenue dans le groupe _{self}_**\n> Si vous souhaiter le quiter, réagisez à ce message avec {Emo_departGroupe}..."
        
        self.MsgSortie = await self.salon.send(contenu_MsgSortie)
        await self.MsgSortie.add_reaction(Emo_departGroupe)
        
        
        
# =============================================================================
#### Création du Message d'Entrée sur lequel réagir pour rejoindre le groupe
# =============================================================================
        
        self.Emo_Entree = rd.choice(fDis.Emos_Babys)
            
        contenu_MsgEntree = f"Pour rentrer dans le groupe {self} :\n> Réagissez à ce message avec {self.Emo_Entree} !"
        
        self.MsgEntree  = await self.salon_GroupeSup.send(contenu_MsgEntree)
        await self.MsgEntree.add_reaction(self.Emo_Entree)
        
        
        
# =============================================================================
#### Enregistrement des modifications
# =============================================================================
        
        self.ecriture_GoogleSheet()
            
    
    
    
    
    def ecriture_GoogleSheet(self):
        
#### Création du dictionnaire correspondant à la ligne du Groupe
        
        ligneGroupe = {fGoo.clefGrp_numGroupe  : self.numero,
                       fGoo.clefGrp_CheminBrut : self.cheminBrut}

        if v.phaseEnCours == v.phase1 :
            
            ligneGroupe[fGoo.clefGrp_idSalon  ] = self.salon     .id
            ligneGroupe[fGoo.clefGrp_MsgSortie] = self.MsgSortie .id
            ligneGroupe[fGoo.clefGrp_MsgEntree] = self.MsgEntree .id
            ligneGroupe[fGoo.clefGrp_EmoEntree] = self.Emo_Entree
        
        
        
        
        
#### Recherche du numéro de ligne
        
        ligne, numeroLigne = fGoo.ligne_avec(self.numero,
                                             fGoo.clefGrp_numGroupe,
                                             fGoo.donneeGoogleSheet(fGoo.page_Groupes))
        
#### --- Cas 1 : Le groupe viens d'être créé ---

#### Ajout d'une nouvelle ligne à fGoo.page_Groupe

        if ligne == None :
            fGoo.ajoutLigne(ligneGroupe, fGoo.page_Groupes, numero_nvlLigne = "fin")



#### --- Cas 2 : Le groupe à déjà été noté dans le Google Sheet ---
                    
        else :
            fGoo.remplacerLigne(ligneGroupe, numeroLigne, fGoo.page_Groupes)
    
    
    
    

    def __str__(self):
        return " > ".join( self.chemin )





# %%% Gestions des permissions
    
    async def autorisation_Salon(self, membre):
        await self.salon.set_permissions(membre, read_messages = True , send_messages = True )  





    async def expulsion_Salon(self, membre):
        await self.salon.set_permissions(membre, read_messages = False, send_messages = False)  



    
    
    async def autorisation_SalonsDuChemin(self, membre):
        
        for g in self.sur_Groupes :
            await g.autorisation_Salon(membre)
        
        await self.autorisation_Salon(membre)
        




# %% Fonctions liés aux Groupes

TousLesGroupes = []

async def creationGroupe (cheminBrut, ajout_A_TousLesGroupes = True):
    """
    Créée un nouveau groupe, ajoute ce groupe à TousLesGroupes si ajout_A_TousLesGroupes == True
    """

# =============================================================================
#### Recherche d'un numéro disponible pour le nouveau groupe
# =============================================================================

    numTrouve       = False
    numNouvGroupe   = 0

    numDejaUtilises = fGoo.colonne_avec(fGoo.page_Groupes, fGoo.clefGrp_numGroupe)

    while not numTrouve :
        numNouvGroupe += 1
        if numNouvGroupe not in numDejaUtilises:
            numTrouve = True
    
    
    
# =============================================================================
#### Création du nouveau Groupe
# =============================================================================
    
    nouvGroupe = Groupe(numNouvGroupe, cheminBrut)
    await nouvGroupe.init_surGroupes()
    
    if v.phaseEnCours == v.phase1 :
        await nouvGroupe.creation_salonEtMessages()
        
    else :
        nouvGroupe.ecriture_GoogleSheet()
    
    
    
# =============================================================================
#### Ajout à TousLesGroupes
# =============================================================================
    
    if ajout_A_TousLesGroupes :
        TousLesGroupes.append(nouvGroupe)
    
    return nouvGroupe





async def groupe_avec (info, type_dinfo, creation_si_existe_pas = False):
    """
    Cette Fonction renvoie le groupe correspondant à l'info donnée en argument.
    Si aucun groupe ne correspond, elle renvoie None.
    Sauf si creation_si_existe_pas où dans ce cas elle le créera si elle le peut.
    
    Voici les types d'information pris en charge : 
        'numero'  'chemin'  'idMsg_Depart'  'idMsg_Entree'
    """
    
    if   type_dinfo == "numero" :
        
        for g in TousLesGroupes :
            if g.numero == info :
                return g
    
    
    
    elif type_dinfo == "chemin" :
        
        for g in TousLesGroupes :
            if g.cheminBrut == info :
                return g
            
        if creation_si_existe_pas :
            nouvGroupe = await creationGroupe(info)
            return nouvGroupe
        
        if GroupeParDefaut.cheminBrut == info :
            return GroupeParDefaut()
    
        
        
    elif type_dinfo == "idMsg_Depart" :
        
        for g in TousLesGroupes :
            if g.MsgSortie.id == info :
                return g
    
    
    
    elif type_dinfo == "idMsg_Entree" :
        
        for g in TousLesGroupes :
            if g.MsgEntree.id == info :
                return g
            
    
    return GroupeParDefaut()





async def redef_groupesExistants():
    """
    Fonction re-définissant les groupes créés précédemment
    """
    
    print(f"Redef des Groupes ({v.phaseEnCours})")
    
    global TousLesGroupes
    
    donneeGroupes  = fGoo.donneeGoogleSheet(fGoo.page_Groupes)
    TousLesGroupes = []
    
    
    
# =============================================================================
#### Redefinition des Groupe déjà dans le fichier Google Drive
# =============================================================================
    
    for ligneGrp in donneeGroupes :
        
        nouvGroupe = Groupe(ligneGrp[fGoo.clefGrp_numGroupe], ligneGrp[fGoo.clefGrp_CheminBrut])
        
        if type(ligneGrp[fGoo.clefGrp_idSalon]) == int :
            
            nouvGroupe.salon      = fDis.bot.get_channel(ligneGrp[fGoo.clefGrp_idSalon])
            nouvGroupe.MsgSortie  = await nouvGroupe.salon.fetch_message(ligneGrp[fGoo.clefGrp_MsgSortie])   
            nouvGroupe.Emo_Entree = ligneGrp[fGoo.clefGrp_EmoEntree]
            
        TousLesGroupes.append(nouvGroupe)
            
    
    
# =============================================================================
#### Initialisation des surGroupes de chacun des groupes préalablement redéfinit
# =============================================================================
    
#    (Création éventuelle de groupe n'étant pas inscrit dans le Google Sheet)        
    
    for grp in TousLesGroupes :
        await grp.init_surGroupes()



# =============================================================================
#### Vérification lors de la phase 1, que tous les salons ont été créés
# =============================================================================

#    (Cette vérif est placé après l'init des surGroupes car 
#        la méthode creation_salonEtMessages a besoin des surGroupes)   

    if v.phaseEnCours == v.phase1 :
        
        for grp in TousLesGroupes :
            await grp.init_surGroupes()
            
            if grp.salon != None :
                ligneGrp, numLigneGrp = fGoo.ligne_avec( grp.numero, fGoo.clefGrp_numGroupe, donneeGroupes)
                grp.MsgEntree = await grp.salon_GroupeSup.fetch_message(ligneGrp[fGoo.clefGrp_MsgEntree])
            
            else :
                await asyncio.sleep(1)
                await grp.creation_salonEtMessages()





async def autorisation_SalonsGrp(membre, numeroGroupe):
    """
    Donne l'accès aux salons des sur-groupes et du groupe du membre
    """

    if v.phaseEnCours == v.phase1 :

# =============================================================================
#### Définition des tous les salons de groupe
# =============================================================================

        TousLesSalonsGroupes = []
        
        for grp in TousLesGroupes :
            TousLesSalonsGroupes.append(grp.salon)
    
    
    
# =============================================================================
#### Définition des salons de groupe / sur-groupes
# =============================================================================

        salons_autorises = []   
        
        if numeroGroupe != GroupeParDefaut.numero :
            
            groupe = await groupe_avec( numeroGroupe, "numero" )
            
            salons_autorises.append(groupe.salon)
            
            for surGrp in groupe.sur_Groupes :
                salons_autorises.append(surGrp.salon)



# =============================================================================
#### Autorisation des salons auxquels le membre à accès
# =============================================================================

            await groupe.autorisation_SalonsDuChemin(membre)
    


# =============================================================================
#### Envoie d'un message dans le cas où le joueur n'a accès a aucun salon
# =============================================================================
    
        else :
            await membre.send("_**Tu n'es inscrit dans aucun groupe...**_\n> Le fonctionnement et l'utilité des groupes sont expliqués dans `#  ┃ ⅱ ┃ groupes`, va y faire un tour !")
    
           
    
# =============================================================================
#### Expulsion des salons auxquels le membre n'a pas accès
# =============================================================================
           
        for salonGrp in TousLesSalonsGroupes :
            if salonGrp not in salons_autorises :
               await salonGrp.set_permissions(membre, read_messages = False)
    
    


@fDis.bot.command(aliases = ["supprTousLesGroupes"])
@fDis.commands.has_permissions(ban_members = True)
async def suppression_salons_msgs_idDiscord_TousLesGroupes (ctx):
    """
    Cette commande supprime :
        - Les salons de Groupes 
        - Les messages d'entrée des groupes de rang n°1
        - Les id des salons, des msgs d'entrées et de sortie des groupes contenu dans fGoo.page_Groupes
    """
    
# Suppression des salons des groupes

    for grp in TousLesGroupes :
        try :
            await grp.salon.delete()
        except :
            pass


# Suppression des messages d'entrées des groupes de rang 1

        if grp.rang == 1 :
            try :
                await grp.MsgEntree.delete()
            except :
                pass


# Suppression des idDiscord dans fGoo.page_Groupes
    
    fGoo.modif_groupe_cellules(2, 3, fGoo.page_Groupes.row_count, 6, fGoo.page_Groupes)






# %% Events et commandes liés aux groupes

# %%% Slashs Commands
"""
@fDis.slash.slash(
    name = "Groupe_Changement",
    description = "ENCORE EN CHANTIER - Vous permet d'entrer dans un autre groupe.",
    guild_ids = [fDis.serveurMegaLG_idDis],
    options = [
        fDis.create_option(
            name        = "nom_groupe",
            description = "Quel est le nom du groupe que vous voulez rejoindre ?",
            option_type = 6,
            required    = True,
            choices = [
                fDis.create_choice(
                    value = "Grp 1", 
                    name  = "Groupe 1 - Le LG c'est Bien"
                ),
                fDis.create_choice(
                    value = "Grp 2",
                    name  = "Groupe 2 - Les Vlg c'est mieux !"
                ),
                fDis.create_choice(
                    value = "Grp 3",
                    name  = "Groupe 3 - Moi celui que je prefère, c'est toi")
            ]
        )
    ]
)
async def slash_changement_groupe(ctx, nom_groupe):
    await ctx.send(nom_groupe)
"""    
    

# %%% Commande de Création de Groupe / Sous-Groupe


Erreurs_NouvGrp = ["**ERREUR** - Vous ne pouvez pas utiliser cette commande car vous n'êtes pas un Joueur...\n> Si vous voulez vous inscrire (ou vous ré-inscrire), ça se passe dans ` ┃ⅰ┃ inscription`",
                   "**ERREUR** - Le groupe que vous essayer de créer existe déjà !",
                   "**ERREUR** - Vous ne pouvez pas créer un sous-groupe à votre groupe, vous êtes déjà dans le plus petit type de groupe possible.\n> Vous ne pouvez pas créer le groupe : #NOUVGRP#"]



@fDis.bot.command(aliases = ["creation_nouvgroupe", "CreationNouvGroupe", "CNG", "cng"])
async def Creation_NouvGroupe(ctx):
    """
    Cette commande gère la création d'un groupe ou d'un sous-groupe.
    Elle n'est utilisable que pendant la phase d'inscription.
    
    """
    
    auteur           = fDis.serveurMegaLG.get_member( ctx.message.author.id                          )
    ligne, num_ligne = fGoo.ligne_avec              ( auteur.id            , fGoo.clef_idDiscord,
                                                      fGoo.donneeGoogleSheet(fGoo.page1_InfoJoueurs) )
    
# =============================================================================
#### --- 1ère Verif - L'auteur de la commande est-il un Joueur ? ---
# =============================================================================
    
    if ligne == None :
        await auteur.send(Erreurs_NouvGrp[0])
        return 
            


# =============================================================================
#### Attente du nom du groupe
# =============================================================================

    AncienGrp = await groupe_avec( ligne[fGoo.clef_Groupe], "numero" )

    contenuMsg_nomGroupe  = f"Vous êtes actuellement dans {AncienGrp}, quel sera le nom de votre **nouveau groupe** ?\n"
    contenuMsg_nomGroupe +=  "> Le **prochain message** que vous enverrez sera le nom de votre nouveau groupe (après l'avoir confirmé).\n"
    contenuMsg_nomGroupe +=  "> Vous avez le droit à tous les caractères spéciaux."
    
    await auteur.send( contenuMsg_nomGroupe )
    
    choixConfirme = False
    
    while not choixConfirme :
    
        msgReponseNomGrp = await fDis.attente_Message( auteur )
        nom_groupe       = msgReponseNomGrp.content
        
        contenuMsg_VerifNom  = f"Est-ce bien le nom de votre futur groupe : **{nom_groupe}** ?\n"
        
        msgConfirmNom    = await auteur.send              ( contenuMsg_VerifNom         )
        choixConfirme    = await fDis.attente_Confirmation( msgConfirmNom      , auteur )
        
        await msgConfirmNom.delete()
        
        if not choixConfirme :
            await auteur.send( "*Vous pouvez taper un nouveau nom de groupe !*" )
    


# =============================================================================
#### Choix du type de groupe
# =============================================================================
    
    if   AncienGrp.rang == 0 :
        choixGrpPrincipal = True
    
    
    
    
    
    elif AncienGrp.rang in [1,2,3] :
        if   AncienGrp.rang == 1 : type_nouvSousGrp = "✨"
        elif AncienGrp.rang == 2 : type_nouvSousGrp = "🪐"
        elif AncienGrp.rang == 3 : type_nouvSousGrp = "🌙"
        
        contenuMsg_typeGroupe  =  "Quel est le type du groupe que vous voulez créer ?\n"
        contenuMsg_typeGroupe += f">  1️⃣ - Je veux créer un groupe principal, de type `🌌`, qui aurait comme salon `# 🌌┃{nom_groupe}`.\n"
        contenuMsg_typeGroupe += f">  2️⃣ - Je veux créer un sous-groupe de {AncienGrp}, de type `{type_nouvSousGrp}`, qui aurait comme salon `# {type_nouvSousGrp}┃{nom_groupe}`.\n"
        contenuMsg_typeGroupe +=  "> Si aucune de ces propositions ne vous conviennent, réagissez avec 🛑."
        
        emojisEtReturns = [["1️⃣", True], ["2️⃣", False], ["🛑", "Stop"]]
        
        msgTypeGrp        = await auteur.send          ( contenuMsg_typeGroupe                          )
        choixGrpPrincipal = await fDis.attente_Reaction( msgTypeGrp           , auteur, emojisEtReturns )
        
        if choixGrpPrincipal == "Stop" :
            return
        
        
        
        choixConfirme = False
        
        while not choixConfirme :
            
            emojisEtReturns = [ ["✅", True], ["❌", False], ["🛑", "Stop"] ]
            
            if choixGrpPrincipal : contenuMsg_VerifType = f"Vous souhaitez bien créer `# 🌌┃{nom_groupe}` ?"
            else                 : contenuMsg_VerifType = f"Vous souhaitez bien créer `# {type_nouvSousGrp}┃{nom_groupe}` ?"
                
            msgConfirmType = await auteur.send          ( contenuMsg_VerifType                          )
            choixConfirme  = await fDis.attente_Reaction( msgConfirmType      , auteur, emojisEtReturns )
            
            if choixConfirme == "Stop" :
                return
            
            await msgConfirmType.delete()
            
            if not choixConfirme : 
                choixGrpPrincipal = not choixGrpPrincipal
    
    
    
    
    
    else :
        contenuMsg_typeGroupe  =  "Quel est le type du groupe que vous voulez créer ?\n"
        contenuMsg_typeGroupe += f">  1️⃣ - Je veux créer un groupe principal, de type `🌌`, qui aurait comme salon `# 🌌┃{nom_groupe}`.\n"
        contenuMsg_typeGroupe += f">  2️⃣ - Je veux créer un sous-groupe de {AncienGrp.sur_Groupes[-1]}, de type `🌙`, qui aurait comme salon `# 🌙┃{nom_groupe}`.\n"
        contenuMsg_typeGroupe +=  "> Si aucune de ces propositions ne vous conviennent, réagissez avec 🛑."
        
        emojisEtReturns = [["1️⃣", True], ["2️⃣", False], ["🛑", "Stop"]]
        
        msgTypeGrp        = await auteur.send          ( contenuMsg_typeGroupe                          )
        choixGrpPrincipal = await fDis.attente_Reaction( msgTypeGrp           , auteur, emojisEtReturns )
        
        if choixGrpPrincipal == "Stop" :
            return
        
        
        
        choixConfirme = False
        
        while not choixConfirme :
            
            emojisEtReturns = [ ["✅", True], ["❌", False], ["🛑", "Stop"] ]
            
            if choixGrpPrincipal : contenuMsg_VerifType = f"Vous souhaitez bien créer `# 🌌┃{nom_groupe}` ?"
            else                 : contenuMsg_VerifType = f"Vous souhaitez bien créer `# 🌙┃{nom_groupe}` ?"
            
            msgConfirmType = await auteur.send          ( contenuMsg_VerifType                          )
            choixConfirme  = await fDis.attente_Reaction( msgConfirmType      , auteur, emojisEtReturns )
            
            if choixConfirme == "Stop" :
                return
            
            await msgConfirmType.delete()
            
            if not choixConfirme : 
                choixGrpPrincipal = not choixGrpPrincipal
            
            
        if not choixGrpPrincipal :
            AncienGrp = AncienGrp.sur_Groupes[-1]
    
    
    
    
    
# =============================================================================
#### --- 2ème Verif - Le groupe existe-t-il déjà ? ---
# =============================================================================
    
    if choixGrpPrincipal : grp_ACreer = await groupe_avec(                                      nom_groupe  , "chemin" )
    else                 : grp_ACreer = await groupe_avec( f"{AncienGrp.cheminBrut}{separateur}{nom_groupe}", "chemin" )
    
    if type(grp_ACreer) == Groupe :
        await auteur.send(Erreurs_NouvGrp[1])
        return 
    
    

# =============================================================================
#### === Création du Groupe / Sous-Groupe ===
# =============================================================================
    
    if choixGrpPrincipal : nouvGroupe = await creationGroupe(                                      nom_groupe   )
    else                 : nouvGroupe = await creationGroupe( f"{AncienGrp.cheminBrut}{separateur}{nom_groupe}" )



# =============================================================================
#### Gestion des autorisations personnelles
# =============================================================================
    
    fGoo.remplacerVal_ligne( nouvGroupe.numero, fGoo.clef_Groupe, 
                             num_ligne                          , 
                             fGoo.page1_InfoJoueurs              )
    
    await autorisation_SalonsGrp(auteur, nouvGroupe.numero)
    
    await auteur.send( "**C'est bon !** Le groupe a été créé !" )





# %%% Event de Changement de Groupe

async def evt_ChangementGroupe(membre, message_id, strEmoji):
    
#### Départ d'un ancien groupe
    
    futur_AncienGrp = await groupe_avec( message_id, "idMsg_Depart" )
    
    if type(futur_AncienGrp) != GroupeParDefaut  and  strEmoji == Emo_departGroupe :
        
        if   futur_AncienGrp.rang == 1 :
            numeroGrp = GroupeParDefaut.numero
        
        elif futur_AncienGrp.rang in [2,3,4] :
            numeroGrp = futur_AncienGrp.sur_Groupes[-1].numero
        
        fGoo.remplacerVal_ligne_avec( numeroGrp, fGoo.clef_Groupe   ,
                                      membre.id, fGoo.clef_idDiscord,
                                      fGoo.page1_InfoJoueurs         )
        
        await autorisation_SalonsGrp(membre, numeroGrp)
    
    
    
#### Entrée dans un nouveau groupe
    
    futur_NouveauGrp = await groupe_avec( message_id, "idMsg_Entree" )
    
    if type(futur_NouveauGrp) != GroupeParDefaut  and  strEmoji == futur_NouveauGrp.Emo_Entree :
        
        numeroGrp = futur_NouveauGrp.numero
        
        fGoo.remplacerVal_ligne_avec(numeroGrp, fGoo.clef_Groupe   ,
                                     membre.id, fGoo.clef_idDiscord,
                                     fGoo.page1_InfoJoueurs          )
        
        await autorisation_SalonsGrp(membre, numeroGrp)





async def reaction_Groupe():
    
    def verifGroupe(payload):
        salon        = fDis.serveurMegaLG.get_channel(payload.channel_id)

#### Si la réaction n'a pas été faite dans un salon du serveur
        if salon == None :
            return False

#### Sinon la réaction a été faite dans un salon du serveur
        else :
            verifUser    = payload.user_id not in (fDis.userMdJ.id, fDis.userAss.id, fDis.userCamp.id)
            
            verifPhase   = v.phaseEnCours == v.phase1
            verifCategCh = salon.category == fDis.CategoryChannel_GestionGrp
        
            return verifUser  and  verifPhase and verifCategCh
    
#### Boucle infini
    while True :
        payload = await fDis.bot.wait_for('raw_reaction_add', check = verifGroupe)
        await evt_ChangementGroupe(payload.member, payload.message_id, str(payload.emoji))