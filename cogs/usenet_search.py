"""Imports"""
import discord
import re
from discord.ext import commands
from cogs._nzbhydra import NzbHydra
from cogs._config import *

import cogs._helpers as hp
from loggerfile import logger


def cog_check():
    def predicate(ctx):
        if len(AUTHORIZED_CHANNELS_LIST) == 0:
            return True
        if ctx.message.channel.id in AUTHORIZED_CHANNELS_LIST:
            return True
        else:
            return False
    return commands.check(predicate)


class UsenetSearch(commands.Cog):
    """UsenetSearch commands"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.nzbhydra = NzbHydra()

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.channel.typing()
        return

    @commands.command()
    @cog_check()
    async def search(self, ctx: commands.Context, cmd: str = '', *, user_input: str = ''):
        commands = ['nzbfind', 'nzbsearch', 'movie', 'movies', "series", "tv"]
        if not cmd:
            return await ctx.send(f'No search term provided. Correct Usage: `{ctx.prefix}search command your query` where command can be: `{" , ".join(commands)}`')
        if not cmd.lower() in commands:
            user_input = cmd + ' ' + user_input
            cmd = 'nzbfind'
        cmd = cmd.lower()
        if not user_input:
            return await ctx.send(f'No search term provided. Correct Usage: `{ctx.prefix}search command your query` where command can be: `{" , ".join(commands)}`')
        msg = await ctx.send(f'Searching for `{user_input}`\nPlease wait', delete_after=300)
        output = None
        if cmd in ["nzbfind", "nzbsearch"]:
            logger.info(
                f'{ctx.author.name} ({ctx.author.id}) did a nzbfind for {user_input}')
            output = await self.nzbhydra.query_search(user_input)

        elif cmd in ["movie", "movies"]:
            if re.search("^tt[0-9]*$", user_input):
                logger.info(
                    f'{ctx.author.name} ({ctx.author.id}) did a imdb movie search for {user_input}')
                output = await self.nzbhydra.imdb_movie_search(user_input)

            elif imdbid := re.search(r".+(tt\d+)", user_input):
                try:
                    logger.info(
                        f'{ctx.author.name} ({ctx.author.id}) did a imdb movie search for {user_input}')
                    output = await self.nzbhydra.imdb_movie_search(imdbid.group(1))
                except:
                    logger.info(
                        f'{ctx.author.name} ({ctx.author.id}) did a movie search for {user_input}')
                    output = await self.nzbhydra.movie_search(user_input)

            else:
                output = await self.nzbhydra.movie_search(user_input)

        elif cmd in ["series", "tv"]:
            if re.search("^tt[0-9]*$", user_input):
                logger.info(
                    f'{ctx.author.name} ({ctx.author.id}) did a imdb series search for {user_input}')
                tvmazeid = await hp.getTVMazeId(imdbId=user_input)
                if tvmazeid:
                    logger.info(
                        f'Found tvmazeid for {user_input} which is: {tvmazeid}.')
                    output = await self.nzbhydra.tvmaze_series_search(tvmazeid)
                else:
                    logger.info(
                        f'Couldn\'t find tvmazeid for {user_input}.')
                    output = await self.nzbhydra.imdb_series_search(user_input)

            elif imdbid := re.search(r".+(tt\d+)", user_input):
                imdbidStr = imdbid.group(1)
                try:
                    logger.info(
                        f'{ctx.author.name} ({ctx.author.id}) did a imdb series search for {user_input}')
                    tvmazeid = await hp.getTVMazeId(imdbidStr)
                    if tvmazeid:
                        logger.info(
                            f'Found tvmazeid for {imdbidStr} which is: {tvmazeid}.')
                        output = await self.nzbhydra.tvmaze_series_search(tvmazeid)
                    else:
                        logger.info(
                            f'Couldn\'t find tvmazeid for {imdbidStr}.')
                        output = await self.nzbhydra.imdb_series_search(imdbidStr)
                except:
                    logger.info(
                        f'{ctx.author.name} ({ctx.author.id}) did a series search for {user_input}')
                    output = await self.nzbhydra.series_search(user_input)

            else:
                logger.info(
                    f'{ctx.author.name} ({ctx.author.id}) did a series search for {user_input}')
                output = await self.nzbhydra.series_search(user_input)

        if not output:
            output = 'Nothing found :('

            await msg.edit(content=output, delete_after=300)
        else:
            telegraph_url = await hp.telegraph_paste(content=output[0])
            await msg.edit(content=f'Found {output[1]} Results\n{telegraph_url}', delete_after=300)


async def setup(bot):
    await bot.add_cog(UsenetSearch(bot))
    print("UsenetSearch cog is loaded")
