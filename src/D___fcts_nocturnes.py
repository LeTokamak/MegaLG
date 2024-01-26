# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---              Niveau D - Fonctions Nocturnes des différents Rôles               ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""


# Niveau C
import C___habitant       as fHab

# Niveau B
fRol    = fHab.fRol

# Niveau A
fGoo    = fHab.fGoo
fDis    = fHab.fDis
fMeP    = fHab.fMeP
v       = fHab.v


rd      = fHab.rd
asyncio = fHab.asyncio





# %% Villageois

async def fctNoct_Chasseur (chasseur, village):
    pass





# %%% Villageois Basiques

async def fctNoct_Villageois (villageois, village):
    pass





async def fctNoct_Cupidon (cupidon, village):
    
    contenuMsgCupi_Question =  "Bonsoir Cupidon, vous allez pouvoir choisir les deux personnes que vous souhaitez réunir !\nPour cela envoyez ici leurs matricules, un par un."
    contenuMsgCupi_Detail   =  "\n```\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne repondez pas, le couple sera créé au hasard.\n```"
    
    contenuMsgCupi_Attente  = f"{fDis.Emo_Cupidon} en tant que {fRol.emojiRole(cupidon.role, cupidon.estUnHomme)}   - {cupidon.user.mention}  |  {cupidon.pseudo}"
    
    contenuMsgCupi_HistoDeb = f"\n{fRol.emojiRole(cupidon.role, cupidon.estUnHomme)}   - {cupidon.user.mention}  |  {cupidon.pseudo}"


    
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
                
            await cupidon.user.send(f"Vous n'avez pas répondu, votre couple vous a donc été attribué au hasard, c'est :\n> {fMeP.AjoutZerosAvant(amour1.matricule ,3)}  |  **{amour1.pseudo}** en {amour1.groupe} et \n> {fMeP.AjoutZerosAvant(amour2.matricule ,3)}  |  **{amour2.pseudo}** en {amour2.groupe}.")
        
        
#### Annonce du couple aux amoureux
        
        if amour1.estUnHomme : e1 = "" 
        else                 : e1 = "e"
        
        if amour2.estUnHomme : e2 = ""
        else                 : e2 = "e"
        
        await amour1.user.send(f"Vous venez de recevoir une flèche en plein cœur ! Mais pas d'inquiètude, c'est un mignon petit bébé qui vous a attaqué{e1}.\n> Mais depuis, vous êtes attiré{e1} par {fMeP.AjoutZerosAvant(amour2.matricule ,3)}  |  **{amour2.pseudo}** en {amour2.groupe}, quelle étrange coïncidence...")
        await amour2.user.send(f"Vous venez de recevoir une flèche en plein cœur ! Mais pas d'inquiètude, c'est un mignon petit bébé qui vous a attaqué{e2}.\n> Mais depuis, vous êtes attiré{e2} par {fMeP.AjoutZerosAvant(amour1.matricule ,3)}  |  **{amour1.pseudo}** en {amour1.groupe}, quelle étrange coïncidence...")
        
#### Modif de Infos Joueurs pour l'ajout des matricules du couple
        
        fGoo.ajoutVal_cellule_avec( f"{amour1.matricule} {amour2.matricule} ", fGoo.clef_caractRoles , 
                                    cupidon.matricule                    , fGoo.clef_Matricule   ,
                                    fGoo.page1_InfoJoueurs                                    )

        fGoo.ajoutVal_cellule_avec( f"A{amour2.matricule} ", fGoo.clef_caractJoueur ,
                                    amour1.matricule       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                       )
        
        fGoo.ajoutVal_cellule_avec( f"A{amour1.matricule} ", fGoo.clef_caractJoueur ,
                                    amour2.matricule       , fGoo.clef_Matricule    ,
                                    fGoo.page1_InfoJoueurs                       )
        
    
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCupi_HistoDeb + f"\n     A choisi {amour1.user.mention}  |  **{amour1.pseudo}**  et  {amour2.user.mention}  |  **{amour2.pseudo}**")
        
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





# %%% Villageois Nocturnes

async def fctNoct_Salvateur (salvateur, village):
    
    contenuMsgSalva_Question =  "Bonsoir Salvateur, qui allez vous protéger cette nuit ?"
    contenuMsgSalva_Detail   =  "\n```\nVous pouvez protéger un joueur de toutes les attaques nocturnes !\n - Vous pouvez protéger plusieurs fois de suite la même personne.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n```"
    
    contenuMsgSalva_Attente  = f"{fDis.Emo_Salvateur} en tant que {fRol.emojiRole(salvateur.role, salvateur.estUnHomme)}   - {salvateur.user.mention}  |  {salvateur.pseudo}"
    
    contenuMsgSalva_HistoDeb = f"\n{fRol.emojiRole(salvateur.role, salvateur.estUnHomme)}   - {salvateur.user.mention}  |  {salvateur.pseudo}"
    
    
    
### Message
    await salvateur.user.send(contenuMsgSalva_Question + contenuMsgSalva_Detail)
           
#### Attente du Matricule de la personne protégée
    msgAtt = await fDis.channelAttente.send(contenuMsgSalva_Attente)
    habProtege, aRepondu = await salvateur.attenteMatri_Habitant(v.nuit_hFin)
    
    
    if aRepondu :
        village.matriculeHab_protegeSalvat.append(habProtege.matricule)
        
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
        
    contenuMsgSorci_Attente  = f"{fDis.Emo_Sorciere} en tant que {fRol.emojiRole(sorciere.role, sorciere.estUnHomme)}   - {sorciere.user.mention}  |  {sorciere.pseudo}"
    contenuMsgSorci_HistoDeb = f"\n{fRol.emojiRole(sorciere.role, sorciere.estUnHomme)}   - {sorciere.user.mention}  |  {sorciere.pseudo}"
        
        
#### --- Cas où les LG ont choisi quelqu'un ---
        
    if   village.matriculeHab_choixConseilLG != 0 :
        persChoisie = fHab.habitant_avec(village.matriculeHab_choixConseilLG)
            
#### Construction du Message pour la Sorcière
        ( msgNb_potVie , msgNb_potMort , et ) = ("", "", "")
        
        contenuMsgSorci_Detail   = "\n```\n - Vous ne pouvez utiliser qu'une potion par nuit."
            
        if   sorciere.nbPotionsVie  >= 2 : msgNb_potVie  = f"**{sorciere.nbPotionsVie} potions** de Vie"
        elif sorciere.nbPotionsVie  == 1 : msgNb_potVie  =  "plus qu'**une potion** de Vie"
            
        if   sorciere.nbPotionsMort >= 2 : msgNb_potMort = f"**{sorciere.nbPotionsMort} potions** de Mort"
        elif sorciere.nbPotionsMort == 1 : msgNb_potMort =  "plus qu'**une potion** de Mort"
        
        if   sorciere.nbPotionsVie != 0 and sorciere.nbPotionsMort != 0 : et = " et "
        
        
        
        if sorciere.nbPotionsVie  != 0 :
            contenuMsgSorci_Detail += "\n - Pour sauver la victime du conseil, réagissez à ce message avec 🟢.\n - Si plusieurs sorcière la sauvent, seulement une choisie au hasard perdra sa potion."
            
        if sorciere.nbPotionsMort != 0 :
            contenuMsgSorci_Detail += "\n - Pour tuer quelqu'un d'autre, réagissez à ce message avec 🔴.\n - Si plusieurs sorcières tuent la même personne, seulement une choisie au hasard perdra sa potion."
            
        if sorciere.nbPotionsVie  != 0  and  sorciere.nbPotionsMort != 0 :
            contenuMsgSorci_Detail += "\n - Et pour utiliser une potion de vie **et** une potion de mort, réagissez à ce message avec  2️⃣"
            
        contenuMsgSorci_Question  = f"Bonsoir Sorcière, les loups-garous ont choisi comme victime : **{persChoisie.pseudo} {persChoisie.groupe}** ({fMeP.AjoutZerosAvant(persChoisie.matricule, 3)}), voulez-vous utiliser une de vos potions ?\nIl vous reste {msgNb_potVie}{et}{msgNb_potMort}."
        contenuMsgSorci_Detail   +=  "\n - Pour ne rien faire, réagissez à ce message avec ⚫ (ou ne faites rien).\n```"
    
    
    
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
    choixDeux = "La Sorcière a décidé sauver ET de tuer"

    emojisEtReturns = []
        
    if sorciere.nbPotionsVie  != 0 and village.matriculeHab_choixConseilLG != 0 : 
        emojisEtReturns.append(["🟢", choixSauv])
        
    if sorciere.nbPotionsMort != 0 : 
        emojisEtReturns.append(["🔴", choixTuer])
    
    if sorciere.nbPotionsVie  != 0 and village.matriculeHab_choixConseilLG != 0  and  sorciere.nbPotionsMort != 0 : 
        emojisEtReturns.append(["2️⃣", choixDeux])
        
    emojisEtReturns.append(["⚫", choixRien])
    
    
    
    
    
# =============================================================================
#### === Attente de la Réponse de la Sorcière ===
# =============================================================================       
    
    msgAtt = await fDis.channelAttente.send( contenuMsgSorci_Attente )
    
    tempsRestant = v.nuit_hFin - v.maintenant()
    
    choixSorciere = await fDis.attente_Reaction(msgQuestion, sorciere.user, emojisEtReturns, timeout = tempsRestant.seconds)
    
#### --- Cas 1 : La sorcière ne réponds pas où elle répond "rR" ---
    
    if choixSorciere in (choixRien, None) :
        
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + "\n   La sorcière n'a rien fait cette nuit.")
    
    
    
#### --- Cas 2 : La sorcière sauve la victime des LG ---
    
    if choixSorciere in (choixSauv, choixDeux) :
        
        village.matriculeSorciere_sauveuse.append( sorciere.matricule )
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + "\n   La sorcière a sauvé la victime des Loups-Garous !")
    
    
    
#### --- Cas 3 : La sorcière veut tuer quelqu'un d'autre ---
    
    if choixSorciere in (choixTuer, choixDeux) :
    
#### Message
        contenuMsgPoison_Question = "Sorcière, vous avez décidé d'utiliser une de vos potions de mort. Qui voulez-vous empoisonner ?"
        contenuMsgPoison_Detail   = "\n```\nPour choisir votre victime, envoyez ici son matricule.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n```"
        
        await sorciere.user.send(contenuMsgPoison_Question + contenuMsgPoison_Detail)
        
#### Attente de Réponse
        msgAtt2 = await fDis.channelAttente.send(contenuMsgSorci_Attente + "   ##### Choix de la personne à empoisonner #####")
        victimeSorciere, aRepondu = await sorciere.attenteMatri_Habitant(v.nuit_hFin)
        
        if aRepondu :
            village.matriculeSorciere_tueuses.append(        sorciere.matricule )
            village.matriculeHab_tuesSorciere.append( victimeSorciere.matricule )
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgSorci_HistoDeb + f"\n   La sorcière a tué {victimeSorciere.user.mention} {victimeSorciere.pseudo} !")
            
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
    
    contenuMsgVoyante_Attente  = f"{fDis.Emo_Voyante} en tant que {fRol.emojiRole(voyante.role, voyante.estUnHomme)}   - {voyante.user.mention}  |  {voyante.pseudo}"
    
    contenuMsgVoyante_HistoDeb = f"\n{fRol.emojiRole(voyante.role, voyante.estUnHomme)}   - {voyante.user.mention}  |  {voyante.pseudo}"
    
#### Message
    await voyante.user.send(contenuMsgVoyante_Question + contenuMsgVoyante_Detail)
    
#### Attente du Matricule d'habitant
    msgAtt = await fDis.channelAttente.send(contenuMsgVoyante_Attente)
    pers, aRepondu = await voyante.attenteMatri_Habitant(v.nuit_hFin)
    
    
    
    if aRepondu :
        
#   Cas où pers est un Loup Bleu
        if   pers.role == fRol.role_LGBleu :
            role_vu = rd.choice( [ role   for role in fRol.TousLesRoles   if role[fRol.clefCamp] == fRol.campVillage ] )
        
        elif pers.role == fRol.role_Traitre :
            role_vu = fRol.role_LG
                
        else :
            role_vu = pers.role
        
#### Réponse de la boule de cristal
        reponseBoule = f"{fMeP.AjoutZerosAvant(pers.matricule,3)}  |  **{pers.pseudo}** {pers.groupe} est **{role_vu[fRol.clefNom]}**"

        await voyante.user.send(f"Vous voyez dans votre boule que {reponseBoule}.")
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgVoyante_HistoDeb + f"\n     Elle a vu dans sa boule que {reponseBoule}.")
    
    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgVoyante_HistoDeb +  "\n     Elle n'a pas regardé sa boule.")
    
### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Voyante_dAura (voyante_dAura, village):
    
    contenuMsgVoyante_Question =  "Bonsoir Voyante d'Aura, c'est l'heure de démasquer vos ennemis ! Vous allez pouvoir voir le camp d'un habitant, qui choisissez-vous ?"
    contenuMsgVoyante_Detail   =  "\n```\nPour choisir un joueur, envoyez son matricule sous ce message.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n```"
    
    contenuMsgVoyante_Attente  = f"{fDis.Emo_Voyante_dAura} en tant que {fRol.emojiRole(voyante_dAura.role, voyante_dAura.estUnHomme)}   - {voyante_dAura.user.mention}  |  {voyante_dAura.pseudo}"
    
    contenuMsgVoyante_HistoDeb = f"\n{fRol.emojiRole(voyante_dAura.role, voyante_dAura.estUnHomme)}   - {voyante_dAura.user.mention}  |  {voyante_dAura.pseudo}"
    
#### Message
    await voyante_dAura.user.send(contenuMsgVoyante_Question + contenuMsgVoyante_Detail)
    
#### Attente du Matricule d'habitant
    msgAtt = await fDis.channelAttente.send(contenuMsgVoyante_Attente)
    pers, aRepondu = await voyante_dAura.attenteMatri_Habitant(v.nuit_hFin)
    
    
    
    if aRepondu :
        
#   Cas où pers est un Loup Bleu
        if   pers.role[fRol.clefCamp] == fRol.campVillage  or  pers.role == fRol.role_LGBleu  or  (pers.role == fRol.role_EnfantSauv  and  fHab.habitant_avec(pers.pereProtecteur) != None) :
            if pers.estUnHomme : camp_vu = "Gentil"
            else               : camp_vu = "Gentille"
                
        else :
            if pers.estUnHomme : camp_vu = "Méchant"
            else               : camp_vu = "Méchante"
        
#### Réponse de la boule de cristal
        reponseEsprit = f"{fMeP.AjoutZerosAvant(pers.matricule,3)}  |  **{pers.pseudo}** {pers.groupe} est **{camp_vu}**"

        await voyante_dAura.user.send(f"Selon vous, {reponseEsprit}.")
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgVoyante_HistoDeb + f"\n     Elle a vu que {reponseEsprit}.")
    
    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgVoyante_HistoDeb +  "\n     Elle n'a rien vu.")
    
### Fin de l'attente
    await msgAtt.delete()





# %%% Villageois Vote

async def fctNoct_Corbeau (corbeau, village):
    
    contenuMsgCorbeau_Question =  "Bonsoir Corbeau, qui allez-vous désigner cette nuit ?"
    contenuMsgCorbeau_Detail   =  "\n```\nVous allez pouvoir votez de manière anonyme pour la personne que vous voulez, elle recevra 2 voix, pour cela envoyez ici son matricule.\n - Si plusieurs Corbeaux font le même choix que vous, les voix se cumulerons.\n - Ces ne voix compterons que pour le premier tour.\n - Si le matricule ne correspond à personne, vous pourrez le retaper\n```"
    
    contenuMsgCorbeau_Attente  = f"{fDis.Emo_Corbeau} en tant que {fRol.emojiRole(corbeau.role, corbeau.estUnHomme)}   - {corbeau.user.mention}  |  {corbeau.pseudo}"
    
    contenuMsgCorbeau_HistoDeb = f"\n{fRol.emojiRole(corbeau.role, corbeau.estUnHomme)}   - {corbeau.user.mention}  |  {corbeau.pseudo}"
    
### Message
    await corbeau.user.send( contenuMsgCorbeau_Question + contenuMsgCorbeau_Detail )
            
### Attente d'une Réponse
    msgAtt = await fDis.channelAttente.send( contenuMsgCorbeau_Attente )
    pers, aRepondu = await corbeau.attenteMatri_Habitant(v.nuit_hFin)



    if aRepondu :
        village.matricule_choixCorbeaux.append(pers.matricule)
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCorbeau_HistoDeb + f"\n     Ce corbeau a choisi {pers.user.mention}.")


    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgCorbeau_HistoDeb +  "\n     Ce corbeau n'a choisi personne.")

### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Hirondelle (hirondelle, village):
    
    contenuMsgHirond_Question =  "Bonsoir Hirondelle, qui allez-vous désigner cette nuit ?"
    contenuMsgHirond_Detail   =  "\n```\nVous allez pouvoir choisir une personne de manière anonyme, sa voix comptera triple, pour cela envoyez ici son matricule.\n - Si plusieurs Hirondelles font le même choix que vous, les voix se cumulerons.\n - Si le matricule ne correspond à personne, vous pourrez le retaper\n```"
    
    contenuMsgHirond_Attente  = f"{fDis.Emo_Hirondelle} en tant que {fRol.emojiRole(hirondelle.role, hirondelle.estUnHomme)}   - {hirondelle.user.mention}  |  {hirondelle.pseudo}"
    
    contenuMsgHirond_HistoDeb = f"\n{fRol.emojiRole(hirondelle.role, hirondelle.estUnHomme)}   - {hirondelle.user.mention}  |  {hirondelle.pseudo}"
    
### Message
    await hirondelle.user.send(contenuMsgHirond_Question + contenuMsgHirond_Detail)
            
### Atente d'une Réponse
    msgAtt = await fDis.channelAttente.send(contenuMsgHirond_Attente)
    pers, aRepondu = await hirondelle.attenteMatri_Habitant(v.nuit_hFin)



    if aRepondu :
        village.matricule_choixHirondelles.append(pers.matricule)
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgHirond_HistoDeb + f"\n     Cette hirondelle a choisi {pers.user.mention}.")
            
    else :
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgHirond_HistoDeb +  "\n     Cette hirondelle n'a choisi personne.")

### Fin de l'attente
    await msgAtt.delete()





async def fctNoct_Juge (juge, village):
    pass





# %%% Famille Nombreuse

async def fctNoct_FamilleNombreuse (membreFN, village):
    
    try :
        
        contenuMsgFamiNom_Attente = f"{fDis.Emo_FNFrere} en tant que {fRol.emojiRole(membreFN.role, membreFN.estUnHomme)}   - {membreFN.user.mention}  |  {membreFN.pseudo}"
        
### Accès aux channels
        await village.salonFamilleNb  .set_permissions ( membreFN.member_FN , read_messages = True , send_messages = True )
        await village.vocalFamilleNb  .set_permissions ( membreFN.member_FN , read_messages = True                        )
        
### Attente
        msgAtt = await fDis.channelAttente.send(contenuMsgFamiNom_Attente)
        await asyncio.sleep(v.nuit_duree.seconds)
                
        await msgAtt.delete()
                
### Fin de la nuit
    
        await village.salonFamilleNb  .set_permissions ( membreFN.member_FN , read_messages = True , send_messages = v.FN_peuventParler_pdt_Journee )
        await village.vocalFamilleNb  .set_permissions ( membreFN.member_FN , read_messages = v.FN_peuventParler_pdt_Journee                        )



    except :
        contenuMsgFamiNom_Attente = f"**Pas sur le serveur** | {fDis.Emo_FNFrere} en tant que {fRol.emojiRole(membreFN.role, membreFN.estUnHomme)}   - {membreFN.user.mention}  |  {membreFN.pseudo}"
        msgAtt = await fDis.channelAttente.send(contenuMsgFamiNom_Attente)
        
        await asyncio.sleep(v.nuit_duree.seconds)
                
        await msgAtt.delete()





# %% Loups-Garous

async def fctNoct_LG (lg, village):
    """
    Les Loups-Garous simples n'ont pas de fonction nocturne dédié, ils assistent juste au conseil des LG.
    La fonction du conseil des Loups-Garous est définie en dessous
    """
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
    
    contenuMsgLGNoir_HistoDeb = f"{fRol.emojiRole(lgNoir.role, lgNoir.estUnHomme)}   - {lgNoir.user.mention}  |  {lgNoir.pseudo}"
    
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
            village.matriculeLGN_quiOntInfecte.append(lgNoir.matricule)
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGNoir_HistoDeb + "\n   Ce Loup Noir **infecte** cette nuit !")
        
        else :
            village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGNoir_HistoDeb + "\n   Ce Loup Noir n'infecte pas cette nuit.")
        
        
        await msgAtt.delete()





async def fctNoct_LGBleu (lgBleu, village):
    pass


async def fctNoct_Traitre (traitre, village):
    pass


# %%% Loups-Garous Solitaires

async def fctNoct_LGBlanc (lgBlanc, village):
    
    contenuMsgLGBlanc_Question =  "Bonsoir Loup-Garou Blanc, nous sommes mercredi soir, la nuit va donc être sanglante... Alors qui souhaitez-vous tuer ?"
    contenuMsgLGBlanc_Detail   =  "\n```\nVous pouvez choisir n'importe quel joueur !\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne choisisez personne, le hasard décidera à votre place !\n```"
    
    contenuMsgLGBlanc_HistoDeb = f"\n{fRol.emojiRole(lgBlanc.role, lgBlanc.estUnHomme)}   - {lgBlanc.user.mention}  |  {lgBlanc.pseudo}"
    
    contenuMsgLGBlanc_Attente  = f"{fDis.Emo_LGBlanc} en tant que {contenuMsgLGBlanc_HistoDeb}"
    
    
    if  v.ajd.weekday() == 2 :    

### Message
        await lgBlanc.user.send(contenuMsgLGBlanc_Question + contenuMsgLGBlanc_Detail)

### Attente d'une réponse
        msgAtt = await fDis.channelAttente.send(contenuMsgLGBlanc_Attente)
        habTue, aRepondu = await lgBlanc.attenteMatri_Habitant(v.nuit_hFin)

        if not aRepondu :
            habTue = rd.choice(fHab.TousLesHabitants)
            
        village.matriculeHab_tuesLGBlanc.append(habTue.matricule)

### Historique et Fin de l'attente
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgLGBlanc_HistoDeb + f"\n     Ce Loup Blanc a choisi {habTue.user.mention}.")
        await msgAtt.delete()





async def fctNoct_EnfantSauvage (enfSauvage, village):
    
    contenuMsgEnfSauv_Question =  "Bonsoir Enfant Sauvage, quel sera votre modèle ?"
    contenuMsgEnfSauv_Detail   =  "\n```\nPour le choisir, envoyez ici son matricule.\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne repondez pas, votre modele vous sera attribué au hasard.\n```"
    
    contenuMsgEnfSauv_HistoDeb = f"{fRol.emojiRole(enfSauvage.role, enfSauvage.estUnHomme)}   - {enfSauvage.user.mention}  |  {enfSauvage.pseudo}"
    
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
            
            await enfSauvage.user.send(f"Vous n'avez pas répondu, votre modèle vous a donc été attribué au hasard, c'est : {fMeP.AjoutZerosAvant(modele.matricule ,3)}  |  **{modele.pseudo}** en {modele.groupe}.")
        
        
### Ajout du matricule du modele dans Infos Joueurs
        
        fGoo.remplacerVal_ligne_avec(     modele.matricule , fGoo.clef_caractRoles , 
                                      enfSauvage.matricule , fGoo.clef_Matricule   ,
                                      fGoo.page1_InfoJoueurs                    )
        
        village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgEnfSauv_HistoDeb + f"\n     A choisi {modele.member.mention}  |  {modele.pseudo} comme modele\n")
        
        
### Fin de l'attente
        await msgAtt.delete()



        

# %% Conseil des Loups-Garous

async def participation_au_Conseil_LG (LoupGarou, village):
    
    try :
        contenuMsg_Attente = f"{fDis.Emo_LoupGarou} en tant que {fRol.emojiRole(LoupGarou.role, LoupGarou.estUnHomme)}   - {LoupGarou.user.mention}  |  {LoupGarou.pseudo}"
        
#### Début du Conseil
        
        await village.salonVoteLG   .set_permissions( LoupGarou.member , read_messages = True  , send_messages = True  )
        await village.salonConseilLG.set_permissions( LoupGarou.member , read_messages = True  , send_messages = True  )
        await village.vocalConseilLG.set_permissions( LoupGarou.member , read_messages = True                          )
        
        
#### Attente de la Fin du Conseil
        
        msgAtt = await fDis.channelAttente.send( contenuMsg_Attente )

        while v.maintenant() < v.conseilLG_hFin :
            await asyncio.sleep(1)
        
        
#### Fin du conseil
        
        await village.salonVoteLG   .set_permissions( LoupGarou.member , read_messages = False , send_messages = False )
        await village.salonConseilLG.set_permissions( LoupGarou.member , read_messages = True  , send_messages = v.LG_peuventParler_pdt_Journee )
        await village.vocalConseilLG.set_permissions( LoupGarou.member , read_messages = v.LG_peuventParler_pdt_Journee                         )
        
        
### Fin de l'attente
        await msgAtt.delete()
        
    
    except :
        
        contenuMsg_Attente = f"**Pas sur le serveur** | {fDis.Emo_LoupGarou} en tant que {fRol.emojiRole(LoupGarou.role, LoupGarou.estUnHomme)}   - {LoupGarou.user.mention}  |  {LoupGarou.pseudo}"
        msgAtt = await fDis.channelAttente.send( contenuMsg_Attente )

        await asyncio.sleep(v.conseilLG_duree.seconds)
        
        await msgAtt.delete()





# %% Maire

async def nomination_gardes_maire (maire, village):
    
    if maire.estUnHomme : monsieur, le_seul = "Monsieur", "le seul"
    else                : monsieur, le_seul = "Madame"  , "la seule"

#### Attente de Lancement
    
    strEmo_Lancmt               =  "🟢"

    contenuMsgLancmt_Question   = f"Bonsoir {monsieur} le Maire, vous allez pouvoir choisir vos gardes du corps."
    contenuMsgLancmt_Precision  = f"\n> Pour lancer la nomination, réagissez à ce message avec {strEmo_Lancmt} !"
    contenuMsgLancmt_Precision +=  "\n> Vous devez absolument réagir __**après**__ avoir terminé vos activités nocturnes, pour ne pas vous emmêler les pinceaux lors des désignations des matricules !"
    contenuMsgLancmt_Precision +=  "\n> Si vous ne réagissez pas à ce message, vos gardes vous seront atribués au hasard."
    
    contenuMsgMaire_AttenteDeb  = f"{fDis.Emo_Maire}   - {maire.user.mention}  |  {maire.pseudo}  |  {village.nom} - *Attente du début de la fonction nocturne*"
    
    msgAtt_Debut      = await fDis.channelAttente.send(contenuMsgMaire_AttenteDeb)
    messageLancement  = await maire.user.send(contenuMsgLancmt_Question + contenuMsgLancmt_Precision)
    
    lancementAutorise = await fDis.attente_Reaction(messageLancement, maire.user, [[strEmo_Lancmt, True]], timeout = v.nuit_duree.seconds, reponseParDefaut = False)
    
    await messageLancement.delete()
    await msgAtt_Debut.delete()
    
    
    
    
    
    contenuMsgMaire_Question = f"Re-bonsoir {monsieur} le Maire, quels seront vos deux gardes du corps ?\n Pour les choisir, envoyez ici leur matricules un par un !\n __Petite précisions__ : Ils ne vous protègerons **que des attaques nocturnes** et vous serez **{le_seul}** à connaître leur identité !"
    contenuMsgMaire_Detail   =  """\n```\n - Ces gardes du corps seront des "boucliers humains", ils vous protègerons, mais ils le payerons de leur vie...\n - Si le matricule ne correspond à personne, vous pourrez le retaper.\n - Si vous ne repondez pas, vos gardes vous seront attribués au hasard.\n```"""
    
    contenuMsgMaire_HistoDeb = f"\n{fDis.Emo_Maire}   - {maire.user.mention}  |  {maire.pseudo}"
    
    contenuMsgMaire_Attente  = f"{fDis.Emo_Maire} en tant que {fRol.emojiRole(maire.role, maire.estUnHomme)}   - {maire.user.mention}  |  {maire.pseudo}"
    

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
    
    maire.gardesMaire.append(garde1.matricule)
    maire.gardesMaire.append(garde2.matricule)
    
    fGoo.ajoutVal_cellule_avec( f"M{garde1.matricule} M{garde2.matricule} ", fGoo.clef_caractJoueur,
                                maire.matricule                            , fGoo.clef_Matricule   ,
                                fGoo.page1_InfoJoueurs                                       )    
    
    await maire.user.send(f"Vos gardes sont :\n>       {fMeP.AjoutZerosAvant(garde1.matricule ,3)}  |  **{garde1.pseudo}** en {garde1.groupe}\n>       {fMeP.AjoutZerosAvant(garde2.matricule ,3)}  |  **{garde2.pseudo}** en {garde2.groupe}.")
    
    village.msgHistoNuit = await fDis.ajoutMsg(village.msgHistoNuit, contenuMsgMaire_HistoDeb + f"\n     A choisi {garde1.member.mention} et {garde2.member.mention} comme gardes du corps.\n")





# %% === Ajouts des fonctions nocturnes aux dictionnaires des Rôles ===

fRol.role_Villageois   [fRol.clefFctsNoct] = fctNoct_Villageois
fRol.role_VillaVilla   [fRol.clefFctsNoct] = fctNoct_Villageois
fRol.role_Cupidon      [fRol.clefFctsNoct] = fctNoct_Cupidon
fRol.role_Ancien       [fRol.clefFctsNoct] = fctNoct_Ancien

fRol.role_Salvateur    [fRol.clefFctsNoct] = fctNoct_Salvateur
fRol.role_Sorciere     [fRol.clefFctsNoct] = fctNoct_Sorciere
fRol.role_Voyante      [fRol.clefFctsNoct] = fctNoct_Voyante
fRol.role_Voyante_dAura[fRol.clefFctsNoct] = fctNoct_Voyante_dAura

fRol.role_Corbeau      [fRol.clefFctsNoct] = fctNoct_Corbeau
fRol.role_Hirondelle   [fRol.clefFctsNoct] = fctNoct_Hirondelle
fRol.role_Juge         [fRol.clefFctsNoct] = fctNoct_Juge

fRol.role_Chasseur     [fRol.clefFctsNoct] = fctNoct_Chasseur

fRol.role_FamilleNb    [fRol.clefFctsNoct] = fctNoct_FamilleNombreuse

fRol.role_LG           [fRol.clefFctsNoct] = fctNoct_LG
fRol.role_LGNoir       [fRol.clefFctsNoct] = fctNoct_LGNoir
fRol.role_LGBleu       [fRol.clefFctsNoct] = fctNoct_LGBleu
fRol.role_Traitre      [fRol.clefFctsNoct] = fctNoct_Traitre

fRol.role_LGBlanc      [fRol.clefFctsNoct] = fctNoct_LGBlanc
fRol.role_EnfantSauv   [fRol.clefFctsNoct] = fctNoct_EnfantSauvage