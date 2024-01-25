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
import A___sql                as fSQL
import A___discord            as fDis
import A___mise_en_page       as fMeP


rd = fMeP.rd

groupe_en_attente_de_deb_de_partie = 0





class Groupe :
        
    def __init__ (self, num_groupe, nom_groupe, chef, date_dern_act, groupeEstPublic = True, mdp_groupe = None):
        
        self.numero     = num_groupe
        self.nom        = nom_groupe
        
        self.estPublic  = groupeEstPublic
        self.motDePasse = mdp_groupe
        
        self.salon      = None
        self.chef       = chef
        
        self.date_derniere_activite    = date_dern_act
        
        self.type_de_partie_a_lancee   = groupe_en_attente_de_deb_de_partie
        self.date_deb_prochaine_partie = None
        self.numero_compo_choisie      = None
        
        
    
    
    
    async def creation_salonEtMessages (self):       
        
# =============================================================================
#### Création du Salon du Groupe
# =============================================================================

### Clonage d'un des salons de référence, pour créer le salon

        if self.estPublic : intro_salon = f"🔓┃{self.numero}┃"
        else              : intro_salon = f"🔒┃{self.numero}┃"

        self.salon = await fDis.channelPlanete.clone( name = intro_salon + self.nom )
        await self.salon.edit(position = fDis.channelPlanete.position + 1, topic = f"Groupe créé par {self.chef.display_name}, c'est lui qui peut lancer la partie !")
        
        
                
# =============================================================================
#### Création du Message de Sortir sur lequel réagir pour quitter le groupe
# =============================================================================
        
        contenu_MsgGroupe  = f"**Bienvenue dans le groupe _{self.nom}_**\n"
        contenu_MsgGroupe += f"Pour lancer la partie le **chef** du groupe ({self.chef.mention}) doit réagir à ce message, vous pouvez lancer 2 types de partie :\n"
        contenu_MsgGroupe += f"> {fDis.Emo_BabyOrange} - Une Partie **personnelle**, avec uniquement les personnes dans ce groupe, elle se lancera à 20h, après que le chef ai réagis.\n"
        contenu_MsgGroupe += f"> {fDis.Emo_BabyCyan} - Une Partie **commune**, avec les autres groupes du serveur, elle se lancera dimanche prochain à 20h, après que le chef ai réagis.\n"
        contenu_MsgGroupe +=  "> Les autres membres du groupe peuvent aussi réagir, pour que le chef sâche qu'elle est l'envie majoritaire du groupe.\n"
        contenu_MsgGroupe +=  "\n"
        
        if not self.estPublic : contenu_MsgGroupe += f"Comme votre groupe est privé, pour que de nouveaux membres y rentre, ils devront entrer ce mot de passe : ||{self.motDePasse}||\n"
        
        contenu_MsgGroupe +=  f"Pour rentrer dans **ce** groupe, n'importe qui doit taper la commande suivante (en l'envoyant directement au {fDis.userMdJ.mention}) :\n"
        
        if self.estPublic     : contenu_MsgGroupe += f"> `!rejoindreGroupe {self.numero}`\n"
        else                  : contenu_MsgGroupe += f"> `!rejoindreGroupe {self.numero} `||`{self.motDePasse}`||\n"
        
        contenu_MsgGroupe += "\n"
        
        self.msgGroupe = await self.salon.send(contenu_MsgGroupe)
        await self.msgGroupe.add_reaction(fDis.Emo_BabyOrange)
        await self.msgGroupe.add_reaction(fDis.Emo_BabyCyan)
        
        
        
# =============================================================================
#### Mise à jour de la liste des groupes publics
# =============================================================================
        
        await majMsg_listeGroupes()
        
        
        
# =============================================================================
#### Enregistrement des modifications
# =============================================================================
        
        self.ecriture_GoogleSheet()
            
    
    
    
    
    def ecriture_BdD_SQL(self):
        
#### Création du dictionnaire correspondant à la ligne du Groupe
        
        ligneGroupe = {fSQL.clef_numGroupe   : self.numero        ,
                       fSQL.clef_nomGroupe   : self.nom           ,
                       
                       fSQL.clef_idSalon_Grp : self.salon    .id  ,
                       fSQL.clef_idChef_Grp  : self.chef     .id  ,
                       fSQL.clef_grp_public  : int(self.estPublic),
                       fSQL.clef_code_groupe : self.code          ,
                       
                       fSQL.clef_date_activi_grp : self.date_derniere_activite,
                       
                       fSQL.clef_partie_lance : self.type_de_partie_a_lancee ,
                       fSQL.clef_deb_partie   : self.date_deb_prochaine_partie,
                       fSQL.clef_numCompo     : self.numero_compo_choisie}
        
        
        
#### Remplacement (ou ecriture si inexistant) de la ligne du groupe
        
        fSQL.remplacer_ligne_avec(fSQL.nom_table_groupes,
                                  fSQL.clef_numGroupe, self.numero,
                                  ligneGroupe)

    
    
    def __str__ (self) :
        return f"[{self.numero} / {self.nom}]"





# %%% Gestions des permissions
    
    async def autorisation_Salon(self, membre):
        await self.salon.set_permissions(membre, read_messages = True , send_messages = True )  



    async def expulsion_Salon(self, membre):
        await self.salon.set_permissions(membre, read_messages = False, send_messages = False)  
        
        
        
    async def changementGroupe_entree(self, membre) :
        
        lignes = fSQL.lignes_avec (fSQL.nom_table_joueurs, fSQL.clef_idDiscord, membre.id)
        
        if len(lignes) == 0 :
            
            lignes = [ {fSQL.clef_pseudo    : membre.display_name,
                        fSQL.clef_idDiscord : membre.id           } ]
        
        lignes[0][fSQL.clef_groupe] = self.numero
        
        fSQL.remplacer_ligne_avec(fSQL.nom_table_joueurs,
                                  fSQL.clef_idDiscord, membre.id,
                                  lignes[0])
        
        await expulsion_TousLesGroupes(membre)
        await self.autorisation_Salon(membre)
    
    
    
    async def changementGroupe_sortie(self, membre_partant_du_groupe) :
        
        liste_membres = [ membre   for membre in self.salon.members   if  fDis.roleBot not in membre.roles  and  fDis.roleModerateur not in membre.roles ]

        if self.chef.id == membre_partant_du_groupe.id :
            
            if len(liste_membres) == 0 :
                await self.suppression_Groupe()
                
            else :
                await self.changementChef_alea()
        
        
        
        
        
# %% Changement du chef
    
    async def changementChef_alea(self):
#### Sélection du nouveau chef        

        liste_membres = self.salon.members
        liste_membres = [ membre   for membre in liste_membres   if  fDis.roleBot not in membre.roles  and  fDis.roleModerateur not in membre.roles ]

        nouvChef = fMeP.rd.choice( liste_membres )
        
#### Redef du chef
        
        self.chef = nouvChef
                
        fSQL.remplacer_val_lignes_avec(fSQL.nom_table_groupes,
                                       fSQL.clef_numGroupe, self.numero,
                                       fSQL.clef_idChef_Grp, nouvChef.id )
        
#### Publication du choix
        
        contenuMsg_infoChangementChef  =  "**L'ancien chef du Groupe vient de partir...**\n"
        contenuMsg_infoChangementChef += f"> *Le hasard a choisi {nouvChef.mention} comme nouveau chef du groupe !*"
        
        await self.salon.send(contenuMsg_infoChangementChef)
        
        await self.salon.edit( topic = f"Groupe dirigé par {self.chef.display_name}, c'est lui qui peut lancer la partie !" )
        
        
        
    
    
    async def suppression_Groupe(self):
        
        global TousLesGroupes
        
#### Suppresion du salon du Groupe
        
        await self.salon.delete()
        
        
        
#### Suppresion des références au groupe dans la table des joueurs
        
        lignes = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                                  fSQL.clef_numGroupe, self.numero)
        
        for ligne in lignes :
            
            ligne[fSQL.clef_numGroupe] = None
            
            fSQL.remplacer_ligne_avec(fSQL.nom_table_joueurs,
                                      fSQL.clef_idDiscord, ligne[fSQL.clef_idDiscord],
                                      ligne)
        
        
        
#### Suppresion des références au groupe dans la table des joueurs
        
        fSQL.suppression_lignes_avec(fSQL.nom_table_groupes,
                                     fSQL.clef_numGroupe, self.numero)
        
        
        
#### Suppresion du Groupe de la liste de TousLesGroupes
        
        TousLesGroupes.remove(self)
        
        
        
#### MaJ de la Liste des Groupes
        
        await majMsg_listeGroupes()
        
        
        




# %% Fonctions liés aux Groupes

TousLesGroupes = []

async def creationGroupe (chef, nom_groupe, groupeEstPublic = True, mdp_groupe = None, ajout_A_TousLesGroupes = True) :
    """
    Créée un nouveau groupe, ajoute ce groupe à TousLesGroupes si ajout_A_TousLesGroupes == True
    """
    
# =============================================================================
#### Recherche d'un numéro disponible pour le nouveau groupe
# =============================================================================
    
    numTrouve       = False
    numNouvGroupe   = 0
    
    numDejaUtilises = fSQL.colonne_avec(fSQL.nom_table_groupes, fSQL.clef_numGroupe)
    
    while not numTrouve :
        numNouvGroupe += 1
        if numNouvGroupe not in numDejaUtilises :
            numTrouve = True
    
    
    
# =============================================================================
#### Création du nouveau Groupe
# =============================================================================
    
    nouvGroupe = Groupe(numNouvGroupe, nom_groupe, chef, groupeEstPublic, mdp_groupe)
    await nouvGroupe.creation_salonEtMessages()
    
    
    
# =============================================================================
#### Ajout à TousLesGroupes
# =============================================================================
    
    if ajout_A_TousLesGroupes :
        TousLesGroupes.append(nouvGroupe)
    
    return nouvGroupe





def groupe_avec (info, type_dinfo):
    """
    Cette Fonction renvoie le groupe correspondant à l'info donnée en argument.
    Si aucun groupe ne correspond, elle renvoie None.
    Sauf si creation_si_existe_pas où dans ce cas elle le créera si elle le peut.
    
    Voici les types d'information pris en charge : 
        'numero'  'nom'  'idMsg_Groupe'
    """
    
    if   type_dinfo == "numero" :
        
        for g in TousLesGroupes :
            if g.numero == info :
                return g
    
    elif type_dinfo == "nom" :
        
        for g in TousLesGroupes :
            if g.nom == info :
                return g
        
    elif type_dinfo == "idMsg_Groupe" :
        
        for g in TousLesGroupes :
            if g.msgGroupe.id == info :
                return g
    
    return None





async def redef_groupesExistants():
    """
    Fonction re-définissant les groupes créés précédemment
    """
    
    print( "Redef des Groupes" )
    
    global TousLesGroupes
    
    donneeGroupes  = fSQL.donnees_de_la_table(fSQL.nom_table_groupes)
    TousLesGroupes = []
    
    
    
# =============================================================================
#### Redefinition des Groupe déjà dans le fichier Google Drive
# =============================================================================
    
    for ligneGrp in donneeGroupes :
        
        nouvGroupe = Groupe(num_groupe      = ligneGrp[fSQL.clef_numGroupe], 
                            nom_groupe      = ligneGrp[fSQL.clef_nomGroupe],
                            chef            = fDis.serveurMegaLG.get_member(ligneGrp[fSQL.clef_idChef_Grp]),
                            
                            date_dern_act   = ligneGrp[fSQL.clef_date_activi_grp],
                            
                            groupeEstPublic = bool( ligneGrp[fSQL.clef_grp_public] ),
                            mdp_groupe      = ligneGrp[fSQL.clef_code_groupe]                                )
        
        nouvGroupe.salon      = fDis.bot.get_channel(ligneGrp[fSQL.clef_idSalon_Grp])
        #nouvGroupe.msgGroupe = await nouvGroupe.salon.fetch_message(ligneGrp[fGoo.clefGrp_msgGroupe])
            
        TousLesGroupes.append(nouvGroupe)
    




# %%% Liste des Groupes

msg_listeGroupes   = None
idMsg_listeGroupes = None



def contenuMsg_listeGroupes() :

    contenuMsg = "__**Liste des Groupes publics :**__\n"
    
    taille_nombre = len( str(TousLesGroupes[-1].numero) ) 
    
    for groupe in TousLesGroupes :
        if groupe.estPublic :
            contenuMsg += f"> `{fMeP.AjoutZerosAvant(groupe.numero, taille_nombre, espace = True)}` // {groupe.nom}\n"
    
    contenuMsg += "\n"
    contenuMsg += "Pour rejoindre un groupe, vous pouvez utiliser la commande : `!rejoindreGroupe` *numero_du_groupe* *mot_de_passe_du_groupe (seulement si le groupe est privé)*"
    contenuMsg += "Pour en créer un nouveau, vous pouver utiliser la commande : `!creation_nouvGroupe`"
    
    return contenuMsg
    

    
async def envoieMsg_listeGroupes():
    
    global msg_listeGroupes, idMsg_listeGroupes
    
    msg_listeGroupes   = await fDis.channelFctmentGrp.send(contenuMsg_listeGroupes())
    idMsg_listeGroupes = msg_listeGroupes.id

    return

    
    
async def majMsg_listeGroupes():
    
    global msg_listeGroupes, idMsg_listeGroupes
    
    if   msg_listeGroupes == None  and  idMsg_listeGroupes != None :
        msg_listeGroupes = await fDis.channelFctmentGrp.fetch_message(idMsg_listeGroupes)
    
    elif idMsg_listeGroupes == None :
        envoieMsg_listeGroupes()
        return
    
    await msg_listeGroupes.edit(content = contenuMsg_listeGroupes())
    
    return
    


# %%% Autorisation du Salon du Groupe

async def expulsion_TousLesGroupes(membre):
    
    for grp in TousLesGroupes :
        await grp.expulsion_Salon(membre)
    
    



# %% Commandes liés aux groupes

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
    

# %%% Commande de Création de Groupe


Erreurs_NouvGrp = ["**ERREUR** - Vous ne pouvez pas utiliser cette commande car vous n'êtes plus un Spectateur...\n> Vous ne pouvez pas créer de groupe ou en changer lorsque vous êtes en pleine partie !",
                   "**ERREUR** - Un groupe porte déjà ce nom !"]



@fDis.bot.command(aliases = ["Creation_Nouvgroupe", "Creation_nouvGroupe", "creation_NouvGroupe",
                             "Creation_nouvgroupe", "creation_nouvGroupe", "creation_Nouvgroupe", "creation_nouvgroupe"
                             
                             "CreationNouvGroupe" ,  "creationNouvGroupe",  "CreationnouvGroupe", "CreationNouvgroupe",
                             "Creationnouvgroupe" ,  "creationNouvgroupe",  "creationnouvGroupe", "creationnouvgroupe",
                             
                             "CNG", "cng"])
async def Creation_NouvGroupe(ctx):
    """
    Cette commande gère la création d'un groupe ou d'un sous-groupe.
    Elle n'est utilisable que pendant la phase d'inscription.
    
    """
    
    auteur = fDis.serveurMegaLG.get_member( ctx.message.author.id )
    
    ligne  = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                              fSQL.clef_idDiscord, auteur.id)[0]
    
    
# =============================================================================
#### --- 1ère Verif - L'auteur de la commande est-il un Spectateur ? ---
# =============================================================================
    
    if fDis.roleSpectateurs not in auteur.roles :
        await auteur.send(Erreurs_NouvGrp[0])
        return 
    
    



# =============================================================================
#### Attente du nom du groupe
# =============================================================================

    contenuMsg_nomGroupe  = "Bonjour ! Quel sera le nom de votre **nouveau groupe** ?\n"
    contenuMsg_nomGroupe += "> Le **prochain message** que vous enverrez sera le nom de votre nouveau groupe (après l'avoir confirmé).\n"
    
    await auteur.send( contenuMsg_nomGroupe )
    
    choixConfirme = False
    
    while not choixConfirme :
    
        msgReponseNomGrp = await fDis.attente_Message( auteur )
        nom_groupe       = msgReponseNomGrp.content
        
        contenuMsg_VerifNom  = f"Êtes-vous certain de choisir ce nom : **{nom_groupe}** ?\n"
        
        msgConfirmNom    = await auteur.send              ( contenuMsg_VerifNom         )
        choixConfirme    = await fDis.attente_Confirmation( msgConfirmNom      , auteur )
        
        await msgConfirmNom.delete()
        
#### --- 2ème Verif - Le groupe existe-t-il déjà ? ---
            
        grp_ACreer = groupe_avec( nom_groupe, "nom" )
            
        if type(grp_ACreer) == Groupe :
            await auteur.send(Erreurs_NouvGrp[1])
            choixConfirme = False
        
        if not choixConfirme:
            await auteur.send( "*Vous pouvez taper un nouveau nom de groupe !*" )
    
    
    
    
    
# =============================================================================
#### Choix du type de groupe (privé/public)
# =============================================================================
    
    contenuMsg_typeGroupe  = "Quel est le type du groupe que voulez-vous créer ?\n"
    contenuMsg_typeGroupe += "> 🔓 - Un groupe public, qui sera affiché et accessible par tout le monde.\n"
    contenuMsg_typeGroupe += "> 🔒 - Un groupe privé, qui ne sera accessible qu'en connaissant le **mot de passe** que vous aurez choisi.\n"
    contenuMsg_typeGroupe += "> \n"
    contenuMsg_typeGroupe += "> Si vous ne voulez plus créer de groupe, réagissez avec 🛑."
    
    emojisEtReturns = [["🔓", True], ["🔒", False], ["🛑", "Stop"]]
        
    msgTypeGrp          = await auteur.send          ( contenuMsg_typeGroupe                          )
    choixGoupeEstPublic = await fDis.attente_Reaction( msgTypeGrp           , auteur, emojisEtReturns )
    
    mdp_groupe = None
    
    if choixGoupeEstPublic == "Stop" :
        return
        
#### Définition du Mot de Passe si le groupe est privé
    
    if not choixGoupeEstPublic :

        contenuMsg_mdpGroupe  = "🔒 - Vous allez créer un groupe privé, quel sera son **mot de passe** ?\n"
        contenuMsg_mdpGroupe += "> Le **prochain message** que vous enverrez sera votre mot de passe, une fois que vous l'aurez confirmé.\n"
        
        await auteur.send( contenuMsg_mdpGroupe )
        
        choixConfirme = False
        
        while not choixConfirme :
        
            msgReponseNomGrp = await fDis.attente_Message( auteur )
            mdp_groupe       = msgReponseNomGrp.content
            
            contenuMsg_VerifNom  = f"Êtes-vous certain de choisir ce mot de passe : **{mdp_groupe}** ?\n"
            
            msgConfirmNom    = await auteur.send              ( contenuMsg_VerifNom         )
            choixConfirme    = await fDis.attente_Confirmation( msgConfirmNom      , auteur )
            
            await msgConfirmNom.delete()
            
            if not choixConfirme :
                await auteur.send( "*Vous pouvez taper un nouveau mot de passe !*" )
    




# =============================================================================
#### === Création du Nouveau Groupe ===
# =============================================================================
    
    nouvGroupe = await creationGroupe( auteur, nom_groupe, choixGoupeEstPublic, mdp_groupe )



# =============================================================================
#### Gestion des autorisations personnelles
# =============================================================================
    
    anciGroupe = groupe_avec(ligne[fSQL.clef_numGroupe], "numero")
    
    if anciGroupe != None :
        await anciGroupe.changementGroupe_sortie(auteur)
    
    await nouvGroupe.changementGroupe_entree(auteur)





# %%% Commande de Changement de Groupe

Erreurs_ChangGrp = ["**ERREUR** - Le groupe que vous avez choisi n'existe pas !",
                    "**ERREUR** - Vous ne pouvez changer de groupe que lorsque vous n'êtes pas en partie !"]


@fDis.bot.command(aliases = [                   "changement_Groupe", "changement_groupe", "ChangementGroupe", "changementGroupe", 
                             "Rejoindre_Groupe", "rejoindre_Groupe",  "rejoindre_groupe",  "RejoindreGroupe",  "rejoindreGroupe",
                             
                             "Rejoindre", "rejoindre", "Groupe", "groupe", "GRP", "Grp", "grp"])
async def Changement_Groupe(ctx, numero_str, code = None):
    """
    Cette commande gère le changement de groupe, il permet à n'importe quel joueur d'aller dans un groupe public ou privé.
    """
    
    auteur = fDis.serveurMegaLG.get_member( ctx.message.author.id )
    
    ligne  = fSQL.lignes_avec(fSQL.nom_table_joueurs,
                              fSQL.clef_idDiscord, auteur.id)[0]
    
    numero = int(numero_str)
    
# =============================================================================
#### Recherche du groupe
# =============================================================================
    
    groupe_destination = groupe_avec(numero, "numero")
    
#### --- Vérif --- Le groupe existe-t-il ?
    
    if groupe_destination == None :
        await auteur.send(Erreurs_ChangGrp[0])
        return
    

#### --- Vérif --- L'auteur de la commande est-il un Spectateur ?
    
    if fDis.roleSpectateurs not in auteur.roles :
        await auteur.send(Erreurs_NouvGrp[1])
        return 

    
# =============================================================================
#### Cas 1 : Le groupe est Privé
# =============================================================================
    
    if not groupe_destination.estPublic :
        
        if code == None :
            
#           --- Sous-cas 1 : Le code initial n'a pas été donné ---
            
            contenuMsg_code  = "Vous n'avez pas entrer le mot de passe pour rentrer dans ce groupe !\n"
            contenuMsg_code += "> *Je comparerais votre prochain message, avec le mot de passe du groupe.*\n"
            contenuMsg_code += "> *Si les deux correspondent, vous pourrez entrer dans le groupe !*"
            
            await auteur.send(contenuMsg_code)
            
            msgCode = await fDis.attente_Message( auteur )
            code    = msgCode.content


            
        while code != groupe_destination.code :
            
#           --- Sous-cas 2 : Le code est faux ---

            contenuMsg_code  = "Le mot de passe que vous avez entrer ne correspond pas à celui du groupe !\n"
            contenuMsg_code += "> *Vous pouvez le retaper, je comparerais le prochain message que vous enverrez ici avec le mot de passe du groupe.*\n"
            contenuMsg_code += "> *Si les deux correspondent, vous pourrez entrer dans le groupe !*"
            
            await auteur.send(contenuMsg_code)
            
            msgCode = await fDis.attente_Message( auteur )
            code    = msgCode.content



# =============================================================================
#### Cas 2 : Le groupe est Public
# =============================================================================

#       --- Sous-cas 3 : Le code est bon, entré dans le groupe ---        

    if groupe_destination.estPublic  or  code == groupe_destination.code :   
        
#       Gestion des autorisations personnelles
            
        anciGroupe = groupe_avec(ligne[fSQL.clef_numGroupe], "numero")
        
        if anciGroupe != None :
            await anciGroupe.changementGroupe_sortie(auteur)
        
        await groupe_destination.changementGroupe_entree(auteur)
    




# %%% Commande Admin

@fDis.bot.command(aliases = ["supprTousLesGroupes"])
@fDis.commands.has_permissions(ban_members = True)
async def suppression_salons_msgs_idDiscord_TousLesGroupes (ctx):
    """
    Cette commande supprime :
        - Les salons de Groupes (ainsi que les messages s'y trouvant)
        - Les id des salons, des msgs d'entrées et de sortie des groupes contenu dans fGoo.page_Groupes
    """
    
# Suppression des salons des groupes

    for grp in TousLesGroupes :
        try :
            await grp.suppression_Groupe()
        except :
            pass
