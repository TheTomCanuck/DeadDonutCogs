from .redeventsub import redeventsub


async def setup(bot):
    cog = redeventsub(bot)
    await bot.add_cog(cog)