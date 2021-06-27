# -*- coding: utf-8 -*-
"""
Test
"""

# Niveau C
import C_fct_Inscription as fIns


# Niveau B
fGrp = fIns.fGrp


# Niveau A
fGoo = fGrp.fGoo
fDis = fGrp.fDis
fMeP = fGrp.fMeP
v    = fGrp.v



rd      = fGrp.rd
asyncio = fGrp.asyncio


@fDis.bot.command()
@fDis.commands.has_permissions(ban_members = True)
async def Test (ctx):
    print("C'est un TEST")