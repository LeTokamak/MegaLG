# -*- coding: utf-8 -*-
"""
Test
"""

# Niveau C
import C___compo as fCom


# Niveau B
fGrp = fCom.fGrp


# Niveau A
fGoo = fGrp.fGoo
fDis = fGrp.fDis
fMeP = fGrp.fMeP
v    = fGrp.v



rd      = fGrp.rd
asyncio = v.asyncio


@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Test_2 (ctx):
    print("C'est un TEST")
    
    

@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Maj_Archive (ctx):
    
    fDis.def_constantes_discord()
    
    for ligne in fGoo.donneeGoogleSheet(fGoo.page_fichier(fGoo.Archives)):
        
        try :
            if ligne[fGoo.clef_Pseudo] == "None" :
                membre = fDis.serveurMegaLG.get_member(ligne[fGoo.clef_idDiscord])
                nouv_pseudo = membre.display_name
                
                fGoo.remplacerVal_ligne_avec(nouv_pseudo, fGoo.clef_Pseudo, ligne[fGoo.clef_idDiscord], fGoo.clef_idDiscord, fGoo.page1_Archives)
            
        except :
            pass

    """    
    #for m in serveurMegaLG.members :
    #    print(m.mention, m.id, m, m.discriminator, m.avatar_url)
            
    #await vocalLoupsGarous .set_permissions ( serveurMegaLG.get_member(idTes1), read_messages = True, speak = True)

    print(type(b))
    
    print(b)
    
    Testtt           = discord.Embed(title = "**Clément Campana** en CSI 2 N",                   description = "Il est mort car il était trop nul..."  , color = 0x4E6B89)
    Testtt.set_thumbnail(           url = "https://www.loups-garous-en-ligne.com/jeu/assets/images/carte25.png")
    Testtt.set_footer(text = "Infecté et amoureux de **Thomas Le Gall** en CSI 2 N\n Ta msfqksjdvgizjskbwnvw")
    Testtt.add_field(              name = "Spécificité", value = "Infecté et amoureux de **Thomas Le Gall**", inline = True)
    
    msg = await channelHistorique.send("petit test")
    await msg.edit(embed = Testtt)
    """

fDis.bot.run(fDis.tokenMJ)