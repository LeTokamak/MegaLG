# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------------
---                                                                                ---
---                    Niveau F - Fonction de gestion d'un Tour                    ---
---                                                                                ---
--------------------------------------------------------------------------------------
                                          v1                                29/03/2021
"""

# Niveau E
import E___village        as fVlg

# Niveau D

# Niveau C
fHab = fVlg.fHab

# Niveau B

# Niveua A
fSQL = fHab.fSQL
fDis = fHab.fDis
fMeP = fHab.fMeP
v    = fHab.v



rd      = fHab.rd
asyncio = fHab.asyncio







async def Tour():
    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    
    
#### Rapports municipaux Crépusculaires
    
    for vlg in fVlg.TousLesVillages :
        await vlg.rapportMunicipal()
    
    
    
# %% Nuit
    
#### Gestion de la nuit
    
    coroutinesNocturnes = []
    
    for vlg in fVlg.TousLesVillages :
        coroutinesNocturnes.append( vlg.gestion_nuit() )
    
    await asyncio.gather(*coroutinesNocturnes)
    
    
    
#### Application de la nuit
    
    if v.nbTours != 0 :
        for vlg in fVlg.TousLesVillages :
            await vlg.application_nuit()
    
    
    
    
    
# %% Journée
    
    v.nbTours += 1
    await fDis.channelHistorique.edit(topic = f"{v.phase3} - Tour n°{v.nbTours}")
    await fDis.channelHistorique.send(f"```\n⬢⬢⬢\n\nJournée {v.nbTours} - {fMeP.strDate(v.ajd)}\n\n⬢⬢⬢\n```")
    
#### Début de la Journée
    
    for village in fVlg.TousLesVillages :
        await village.debutJournee()
    
    await fVlg.gestion_dissolutions_meurtres_exils(meurtre_nocturne = True)
    
    
    
#### Re-définition de ToutesLesPersonnes (pour les Hirondelles)
    
    anciensVillages = list(fVlg.TousLesVillages)
    
    await fHab.redef_TousLesHabitants()
    fVlg.redef_villagesExistants()
    
    
    
#### Rajout des choix des Corbeaux / Hirondelles
    
    for i in range(len(anciensVillages)) :
        fVlg.TousLesVillages[i].matricule_choixCorbeaux    = anciensVillages[i].matricule_choixCorbeaux
        fVlg.TousLesVillages[i].matricule_choixHirondelles = anciensVillages[i].matricule_choixHirondelles
    
    
    
#### Rapports municipaux Matinaux
    
    for village in fVlg.TousLesVillages :
        await village.rapportMunicipal()
    
    
    
    
    
# %%% Vote (Elimination / Election Maire)
    
    coroutinesVotes = []
    
    for vlg in fVlg.TousLesVillages :
        if vlg.maire == None : coroutinesVotes.append( vlg.gestion_electionMaire   () )
        else                 : coroutinesVotes.append( vlg.gestion_voteEliminatoire() )
        
    await asyncio.gather(*coroutinesVotes)
    
    await fVlg.gestion_dissolutions_meurtres_exils(meurtre_nocturne = False)
    
    
    
    
    
# %%% Fin de Journée    
    
#### Plantage Final
    
    await asyncio.sleep( 5*60 )
    
    await fDis.channelHistorique.send(f"Le soleil ne va plus tardé à se coucher !\n> Il est {v.maintenant()}.")
    
    v.plantage()