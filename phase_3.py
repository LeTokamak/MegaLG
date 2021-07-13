# -*- coding: utf-8 -*-

"""
======================================================================================
===                                                                                ===
===                                     Phase 3                                    ===
===                                                                                ===
======================================================================================
                                          v1                                29/05/2021
"""

# Niveau F
import F___tour     as fTou


# Niveau E

# Niveau D

# Niveau C

# Niveau B

# Niveau A
fDis = fTou.fDis
v    = fTou.v


asyncio = fTou.asyncio





async def attente_lancementTour() :
        
    m = v.maintenant()
    
#### ||| Variable ||| Si on est dans le WE on ne lance pas la fonction Tour
    
    if not v.partiePdt_Weekend  and  m.weekday() in (4,5) :
        await fDis.channelHistorique.send("Nous somme Vendredi ou Samedi, la fonction Lancement à été stoppée dans son élan !")
        return None
    
    
    
#### Attente du début de la nuit pour lancer la fontion Tour 
    
    tempsAtt            = v.nuit_hDeb  -  m
    intervalMaintenance = v.nuit_hDeb  -  (v.tour2Vote_hFin - v.timedelta(days = 1))   # 30 mins
    
    
    
#  -  Plantage si le temps d'Attente est suppérieur à 30 minutes  -
    
    if tempsAtt >= intervalMaintenance :
        
        tempsAtt_Plantage = tempsAtt - (intervalMaintenance - v.timedelta(minutes = 5))
        
        await fDis.channelHistorique.send(f"Attente de {tempsAtt_Plantage} avant le plantage")
        await asyncio.sleep(tempsAtt_Plantage.seconds)
        
        v.plantage()
    
    
    
#  -  Sinon attente avant de lancer la fonction Tour  -
    
    else :
        await fDis.channelHistorique.send(f"Attente de {tempsAtt} avant de lancer la nuit n°{v.nbTours}")
        
        if tempsAtt > v.timedelta(0) :
            await asyncio.sleep(tempsAtt.seconds)
        
        await fTou.Tour()





@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Lancement(ctx):
    
    await fDis.effacerMsg(ctx)
    await attente_lancementTour()