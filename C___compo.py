# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---          Niveau C - Classe et Fonctions liées aux Compos des Parties           ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

# Niveau B
import B___groupe          as fGrp
import B___roles           as fRol

# Niveau A 
fSQL = fGrp.fSQL
fDis = fGrp.fDis
fMeP = fGrp.fMeP
v    = fGrp.v





class Compo :
    
    def __init__(self, nombre_joueur):
        
        self.nb_joueur = nombre_joueur
        
        self.nom = "Compo sans nom"
        
        self.roles_de_la_compo = []
        
        self.Ancien_nbProtec  = 3
        self.Sorcie_nbPotVie  = 2
        self.Sorcie_nbPotMort = 1
        self.LGNoir_nbInfect  = 1
        self.Juge_nbExil      = 2
        
        
        
    
    
# %% Affichage de la compo
    
    def affichage_propre (self, nbJoueurs) :
        """
        Renvoie un str propre représentant la compo
        """

#### Listage des rôles (d'abords liste de groupe de mots)
            
        mots_roles = []
            
        for r in self.roles_de_la_compo :
                
            nb_meme_role = self.roles_de_la_compo.count(r)
                
            if nb_meme_role == 1 : mot = r[fRol.clefNom]
            else                 : mot = f"{nb_meme_role} {r[fRol.clefNom_pluriel]}"
                
            if mot not in mots_roles :
                mots_roles.append(mot)
                    
                    
#### Rangement des groupes de mots dans l'ordre du nombre de joueurs
            
        mots_roles_ranges = []
            
        while len(mots_roles) != 0 :
                
            nb_max = 1
            gm_max = mots_roles[0]
                
            for gm in mots_roles :
                    
                try    : nb_role = int(gm.split()[0])
                except : nb_role = 1
                    
                if nb_role > nb_max :
                    nb_max = nb_role
                    gm_max = gm
                
            mots_roles_ranges.append(gm_max)
            mots_roles.remove(gm_max)
                
    
#### Réunion des groupes de mots pour former une vraie phrase
    
        phrase_finale = ""
            
        while len(mots_roles_ranges) != 0 :
                
            groupe_mot = mots_roles_ranges[0]
                
            if   len(mots_roles_ranges) == 1 :
                phrase_finale += groupe_mot
                mots_roles_ranges = []
                    
            elif len(mots_roles_ranges) == 2 :
                phrase_finale += f"{groupe_mot} et {mots_roles_ranges[1]}"
                mots_roles_ranges = []
                    
            else :
                phrase_finale += f"{groupe_mot}, "
                mots_roles_ranges.remove(groupe_mot)
            
        return f"__{self.nom} :__ {phrase_finale}."




        
    def affichage_court (self, nbJoueurs) :
        """
        Renvoie un str propre représentant la compo
        """
        
#### Listage des rôles (d'abords liste de groupe de mots)
            
        mots_roles = []
            
        for r in self.roles_de_la_compo :
                
            nb_meme_role = self.roles_de_la_compo.count(r)
                
            if nb_meme_role == 1 : mot = r[fRol.clefSurnoms] [-1]
            else                 : mot = f"{nb_meme_role}{r[fRol.clefSurnoms] [-1]}"
                    
            if mot not in mots_roles :
                mots_roles.append(mot)
            
            
#### Rangement des groupes de mots dans l'ordre du nombre de joueurs
            
        mots_roles_ranges = []
            
        while len(mots_roles) != 0 :
                
            nb_max = 1
            gm_max = mots_roles[0]
                
            for gm in mots_roles :
                    
                try    : nb_role = int(gm.split()[0])
                except : nb_role = 1
                    
                if nb_role > nb_max :
                    nb_max = nb_role
                    gm_max = gm
                
            mots_roles_ranges.append(gm_max)
            mots_roles.remove(gm_max)
                
    
#### Réunion des groupes de mots pour former une vraie phrase
    
        phrase_finale = ""
            
        while len(mots_roles_ranges) != 0 :
                
            groupe_mot = mots_roles_ranges[0]
                
            if   len(mots_roles_ranges) == 1 :
                phrase_finale += groupe_mot
                mots_roles_ranges = []
                    
            else :
                phrase_finale += f"{groupe_mot},"
                mots_roles_ranges.remove(groupe_mot)
            
        return f"**{self.nom}** : {phrase_finale}."





# %% Niveau de difficulté



def choix_de_la_compo (membre_choisissant_la_compo) :
    pass

async def choix_compo(self) :
        
#### Choix du Niveau de la compo
        
    niveaux_dispos, compos_possibles = niveaux_dispos_pour_ces_extensions( choix_extensions, self.nbJoueurs )

    contenu_msgExtension  =  "```⬢⬢⬢ Choix de la compo ⬢⬢⬢```\n"

    if len(choix_extensions) == 1 : contenu_msgExtension += "`Extension choisie :`"
    else                          : contenu_msgExtension += "`Extensions choisies :`"
    contenu_msgExtension += f" {fCom.str_extensions(choix_extensions)}.\n"
    contenu_msgExtension +=  "\n"
    
    contenu_msgExtension +=  "Quel sera **le niveau** de la compo ?"
    
    emojisEtReturns = []
    
    for niveau in niveaux_dispos :
        emoji = fCom.emoji_niveau_difficulte(niveau)
        
        emojisEtReturns.append([emoji, niveau])
        contenu_msgExtension += f"\n> {emoji} - {niveau}"
        
    emojisEtReturns.append([fDis.Emo_infini, "Perso"])
    contenu_msgExtension +=f"\n\n {fDis.Emo_infini} - Compo personnalisée   *(🛠)*"
        
        
    await self.msgExtension.edit(content = contenu_msgExtension)
    returns      = await fDis.attente_Reaction( self.msgExtension, self.membre_referent, emojisEtReturns ) 
    choix_niveau = returns [0]
    
    try    : await self.msgExtension.clear_reactions()
    except : pass
        
        
        
#### Choix de la compo
        
# =============================================================================
#### === Compos proposées ===
# =============================================================================
        
    if choix_niveau != "Perso" :
            
        contenu_msgExtension  =  "```⬢⬢⬢ Choix de la compo ⬢⬢⬢```\n"
        
        if len(choix_extensions) == 1 : contenu_msgExtension += "`Extension choisie :`"
        else                          : contenu_msgExtension += "`Extensions choisies :`"
        contenu_msgExtension += f" {fCom.str_extensions(choix_extensions)}.\n"
        contenu_msgExtension += f"`Niveau choisi :` {choix_niveau}.\n"
        contenu_msgExtension +=  "\n"
        
        contenu_msgExtension += "Avec **quelle compo** voulez-vous jouer ?"
        
        emojisEtReturns = []
        
        i = 0
            
        for compo in compos_possibles :
                
            if compo.difficulte == choix_niveau :
                    
                i    += 1
                emoji = fDis.emoji_correspondant( i )
                
                emojisEtReturns.append([emoji, compos_possibles.index(compo)])
                contenu_msgExtension += f"\n> {emoji} - {compo.affichage_propre( self.nbJoueurs )}"
            
        await self.msgExtension.edit(content = contenu_msgExtension)
        returns     = await fDis.attente_Reaction( self.msgExtension, self.membre_referent, emojisEtReturns )
        choix_compo = returns [0]
            
        self.compo_choisie = compos_possibles[choix_compo]
        
        
        
# =============================================================================
#### === Compos personnalisée ===
# =============================================================================
        
    else :
        
        contenu_msgExtension  =  "```⬢⬢⬢ Choix de la compo ⬢⬢⬢```\n"
        
        contenu_msgExtension += f"__**{fDis.Emo_infini} - Compo personnalisée :**__\n"
        contenu_msgExtension +=  "Pour choisir votre compo, vous allez devoir envoyer un message décrivant votre compo sous cette forme :\n"
        contenu_msgExtension +=  "> *2 LG, 1 vlr, soulard, 1 doppelganger, 2 f-m*\n"
        contenu_msgExtension +=  "> **⤷** 2 Loups-Garous, 2 Francs-Maçons, Voleur, Soûlard, Doppelgänger\n"
        contenu_msgExtension +=  "\n"
        contenu_msgExtension +=  "Voilà la liste de tous les surnoms disponibles :"
            
        for role in fRol.TousLesRoles :
            
            contenu_msgExtension += f"\n> **{role[fRol.clefNom]}** - "
            
            for surnom in role[fRol.clefSuroms] :
                contenu_msgExtension += f"{surnom}, "
                    
            contenu_msgExtension  = contenu_msgExtension[ : -2]
            
        await self.msgExtension.edit(content = contenu_msgExtension)
            
            
            
        def verif_msg (msg):
                
            verifServeur =   msg.guild == self.serveur
            verifSalon   = msg.channel == self.salon_texte_referent
            verifUser    =  msg.author == self.membre_referent
            
            return verifServeur and verifSalon and verifUser
        
        compo_trouve       = False
        ancien_compo_roles = []
            
        ajout_de_role      = True
            
        while not compo_trouve :
                
            msg                = await fDis.bot.wait_for( 'message', check = verif_msg )
            self.compo_choisie = fCom.conversion_str_compo( msg.content, ajout_de_role, ancien_compo_roles )
            
            compo_roles  = self.compo_choisie.liste_roles[0]
            compo_trouve = len(compo_roles) == self.nbJoueurs + 3
            
            liste_msg_erreur = []
            
            if not compo_trouve :
                
                ancien_compo_roles = compo_roles
                nb_role_manquant   = self.nbJoueurs + 3 - len(ancien_compo_roles)
                
                if abs(nb_role_manquant) == 1 : str_nb_role =  "un role"
                else                          : str_nb_role = f"**{abs(nb_role_manquant)}** roles"
                
                if nb_role_manquant > 0 :
                    contenu_msgCompo  = f"ERREUR - Il manque {str_nb_role} dans la compo.\n"
                    contenu_msgCompo +=  "> Vous pouvez envoyer un nouveau message donnant **uniquement les rôles manquants**.\n"
                    
                    ajout_de_role = True
                
                else :
                    contenu_msgCompo  = f"ERREUR - Il y a {str_nb_role} de trop dans la compo.\n"
                    contenu_msgCompo +=  "> Vous pouvez envoyer un nouveau message donnant **uniquement les rôles à enlever**.\n"
                    
                    ajout_de_role = False
                
                msg_erreur = await self.salon_texte_referent.send(contenu_msgCompo)
                liste_msg_erreur.append( msg_erreur )
        
        for msg_erreur in liste_msg_erreur :
            await msg_erreur.delete()

# %% Fonctions - compo

compos_enregistrees = [ ]

def creation_nouvelle_compo (nom, extensions, niveau_difficulte, proposee_dans_jeux_de_base, roles_de_base, *roles_a_ajouter):
    """
    Ajoute une nouvelle compo à compos_enregistrees.
    """
        
    compos_enregistrees.append( Compo(nom, extensions, niveau_difficulte, proposee_dans_jeux_de_base, roles_de_base, roles_a_ajouter) )





def niveaux_dispos_pour_ces_extensions (extensions, nbJoueurs) :
    """
    Renvoie  : 
        - La liste des compos disponibles avec ces extensions et ce nombre de Joueur
        - Ainsi que la liste des niveaux de ces compos
    """
    
#### Combinaisons des extentions possibles
    
    if   extensions == seul_LG_Nuit          : combinaisons_extensions_possibles = (seul_LG_Nuit      , )
    elif extensions == seul_LG_Crepuscule    : combinaisons_extensions_possibles = (seul_LG_Crepuscule, )
    elif extensions == seul_Vampire          : combinaisons_extensions_possibles = (seul_Vampire      , )
    
    elif extensions == LG_Nuit_Crepuscule    : combinaisons_extensions_possibles = (seul_LG_Nuit      , seul_LG_Crepuscule, LG_Nuit_Crepuscule    )
    elif extensions == LG_Nuit_Vampire       : combinaisons_extensions_possibles = (seul_LG_Nuit      , seul_Vampire      , LG_Nuit_Vampire       )
    elif extensions == LG_Crepuscule_Vampire : combinaisons_extensions_possibles = (seul_LG_Crepuscule, seul_Vampire      , LG_Crepuscule_Vampire )
    
    elif extensions == toutes_les_extensions : combinaisons_extensions_possibles = (seul_LG_Nuit      , seul_LG_Crepuscule, seul_Vampire      , LG_Nuit_Crepuscule, LG_Nuit_Vampire, LG_Crepuscule_Vampire, toutes_les_extensions )
    
    
    
#### Sélection des compos avec ces extensions 
    
    compos_possibles = []
    
    for compo in compos_enregistrees :
        
        if compo.extensions in combinaisons_extensions_possibles  and  nbJoueurs in range(compo.nbJou_min, compo.nbJou_max + 1) :
            compos_possibles.append(compo)
    
    
    
#### Liste des niveaux des compos sélectionnées
    
    niveaux_dispos = []
    
    for compo in compos_possibles :
        
        if compo.difficulte not in niveaux_dispos :
            niveaux_dispos.append( compo.difficulte )
    
    
    return niveaux_dispos, compos_possibles





def conversion_str_compo (str_entree, ajout_de_role, ancien_liste_role) :
    """
    Renvoie  : 
        - La liste des compos disponibles avec ces extensions et ce nombre de Joueur
        - Ainsi que la liste des niveaux de ces compos
    """
    
    liste_groupe_mot = str_entree.split(",")
    liste_role       = ancien_liste_role
    
    for str_groupe_mot in liste_groupe_mot :
        liste_mot = str_groupe_mot.split()
        
        if len(liste_mot) == 1 : nb_role, mot_role = 1                , liste_mot[0]
        else                   : nb_role, mot_role = int(liste_mot[0]), liste_mot[1]
        
        role = fRol.role_avec(mot_role, "surnom")
            
        if ajout_de_role :
            liste_role.extend( nb_role * [role] )
            
        else :
            for i in range(nb_role) :
                try    : liste_role.remove( role )
                except : pass
    
    while None in liste_role :
        liste_role.remove(None)
    
    return Compo("__Compo personnalisée__", None, None, False, liste_role, [])





# %% Définition de toutes les compos

# %%% 1     - Loup-Garou pour une Nuit

#### Initiation

creation_nouvelle_compo("La Première Nuit", seul_LG_Nuit, initiation, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Voyante, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Villageois],
                        [fRol.role_Villageois],
                        [fRol.role_Villageois, fRol.role_Villageois])



#### Facile

creation_nouvelle_compo("Pleine Lune", seul_LG_Nuit, facile, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Insomniaque, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Villageois],
                        [fRol.role_Villageois],
                        [fRol.role_Villageois, fRol.role_Voyante], 
                        [fRol.role_Villageois, fRol.role_Villageois, fRol.role_Voyante])


creation_nouvelle_compo("Nuit Solitaire", seul_LG_Nuit, facile, True, 
                        [fRol.role_LG, fRol.role_Voyante, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Villageois, fRol.role_Villageois],
                        [fRol.role_Villageois])



#### Moyen

creation_nouvelle_compo("Confusion", seul_LG_Nuit, moyen, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Soulard, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Insomniaque                                            ],
                        [fRol.role_Villageois                                                                                                         ],
                        [fRol.role_Villageois,                                            fRol.role_Voyante                                                ],
                        [fRol.role_Villageois, fRol.role_Villageois,                           fRol.role_Voyante                                                ],
                        [fRol.role_Villageois, fRol.role_Villageois, fRol.role_Villageois,          fRol.role_Voyante                                                ],
                        [fRol.role_Villageois, fRol.role_Villageois, fRol.role_Villageois,          fRol.role_Voyante, fRol.role_Sbire                                    ],
                        [fRol.role_Villageois, fRol.role_Villageois,                           fRol.role_Voyante, fRol.role_Sbire, fRol.role_Franc_macon, fRol.role_Franc_macon] )


creation_nouvelle_compo("Bénéfice", seul_LG_Nuit, moyen, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Chasseur, fRol.role_Voyante, fRol.role_Voleur, fRol.role_Soulard, fRol.role_Insomniaque],
                        [fRol.role_Noiseuse],
                        [fRol.role_Noiseuse, fRol.role_Villageois],
                        [fRol.role_Noiseuse, fRol.role_Villageois, fRol.role_Villageois])


creation_nouvelle_compo("Mystérieux compagnons", seul_LG_Nuit, moyen, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Sbire, fRol.role_Chasseur, fRol.role_Voyante, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Franc_macon, fRol.role_Franc_macon],
                        [fRol.role_Villageois])


creation_nouvelle_compo("Incertitudes", seul_LG_Nuit, moyen, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Tanneur, fRol.role_Voyante, fRol.role_Voleur, fRol.role_Soulard, fRol.role_Insomniaque],
                        [fRol.role_Noiseuse ],
                        [fRol.role_Noiseuse, fRol.role_Villageois],
                        [fRol.role_Noiseuse, fRol.role_Franc_macon, fRol.role_Franc_macon],
                        [fRol.role_Noiseuse, fRol.role_Franc_macon, fRol.role_Franc_macon, fRol.role_Chasseur],
                        [fRol.role_Noiseuse, fRol.role_Franc_macon, fRol.role_Franc_macon, fRol.role_Chasseur, fRol.role_Sbire],
                        [fRol.role_Noiseuse, fRol.role_Franc_macon, fRol.role_Franc_macon, fRol.role_Chasseur, fRol.role_Sbire, fRol.role_Villageois] )



#### Difficile

creation_nouvelle_compo("Alliance dans la pénombre", seul_LG_Nuit, difficile, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Franc_macon, fRol.role_Franc_macon, fRol.role_Sbire, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Insomniaque],
                        [fRol.role_Soulard],
                        [fRol.role_Soulard, fRol.role_Voyante],
                        [fRol.role_Soulard, fRol.role_Voyante, fRol.role_Villageois],
                        [fRol.role_Soulard, fRol.role_Voyante, fRol.role_Villageois, fRol.role_Villageois],
                        [fRol.role_Soulard, fRol.role_Voyante, fRol.role_Villageois, fRol.role_Villageois, fRol.role_Tanneur] )
    
""" Doppelganger pas encore programmée
creation_nouvelle_compo("Revenants", seul_LG_Nuit, difficile, True, 
                        [fRol.role_LG, fRol.role_LG, fRol.role_Doppelganger, fRol.role_Sbire, fRol.role_Chasseur, fRol.role_Voyante, fRol.role_Voleur, fRol.role_Noiseuse, fRol.role_Villageois, fRol.role_Franc_macon, fRol.role_Franc_macon],
                        [fRol.role_Insomniaque],
                        [fRol.role_Insomniaque, fRol.role_Soulard] )
"""

#### Anarchie (à programmer)


# %%%   2   - Loup-Garou pour un Crépuscule

# %%%     3 - Vampire pour une Nuit 

# %%% 1,2   - Loup-Garou pour une Nuit et pour un Crépuscule

# %%% 1  ,3 - Loup-Garou et Vampire pour une Nuit 

# %%%   2,3 - Loup-Garou pour un Crépuscule et Vampire pour une Nuit

# %%% 1,2,3 - Toutes les extensions

