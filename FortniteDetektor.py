#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=blacklisted-name
# pylint: disable=missing-docstring

from datetime import datetime, timezone

import logging

#if __debug__:
#    logging.basicConfig(level=logging.DEBUG)
#else:
logging.basicConfig(level=logging.INFO)

import discord # pylint: disable=import-error, wrong-import-position
IS_REWRITE = bool(discord.version_info.major)

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)

    async def on_member_update(self, before, after):
        if IS_REWRITE:
            foo = before.activities != after.activities
        else:
            foo = before.game != after.game

        if __debug__ and foo and not after.bot:
            print('------------------------')
            print(f'Time: {datetime.now()}')
            print(f'Name: {after.name}')
            if IS_REWRITE:
                print(f'Activities: {after.activities}')
            else:
                print(f'Game: {after.game}')

        if IS_REWRITE:
            bar = False
            for activity in after.activities:
                try:
                    if activity.application_id == 432980957394370572:
                        bar = True
                        break
                except AttributeError:
                    pass
        else:
            bar = after.game is not None and after.game.name == 'Fortnite'

        if foo and bar:
            if IS_REWRITE:
                asozial = after.guild.id == 367648314184826880
            else:
                asozial = after.server.id == '367648314184826880'

            if asozial:
                embed = discord.Embed(
                    description=f'{after.mention} spielt Fortnite.',
                    timestamp=datetime.now(timezone.utc))
            else:
                embed = discord.Embed(
                    description=f'{after.mention} is playing Fortnite.',
                    timestamp=datetime.now(timezone.utc))

            if after.avatar_url:
                embed.set_footer(text=str(after), icon_url=after.avatar_url)
            else:
                embed.set_footer(text=str(after), icon_url=after.default_avatar_url)

            if IS_REWRITE:
                try:
                    await discord.utils.find(
                        lambda channel: 'fortnite' in channel.name.lower(),
                        after.guild.channels).send(embed=embed)
                except(AttributeError, discord.ClientException, discord.HTTPException):
                    pass
                try:
                    await after.ban(reason='Fortnite', delete_message_days=0)
                except(discord.ClientException, discord.HTTPException):
                    try:
                        await after.kick(reason='Fortnite')
                    except(discord.ClientException, discord.HTTPException):
                        try:
                            await after.add_roles(
                                discord.utils.find(
                                    lambda role: 'fortnite' in role.name.lower()
                                    and not role.managed,
                                    after.guild.roles))
                        except(discord.ClientException, discord.HTTPException):
                            pass
            else:
                try:
                    await client.send_message(
                        discord.utils.find(
                            lambda channel: 'fortnite' in channel.name.lower(),
                            after.server.channels),
                        embed=embed)
                except(discord.ClientException, discord.HTTPException):
                    pass
                try:
                    await client.ban(after, delete_message_days=0)
                except(discord.ClientException, discord.HTTPException):
                    try:
                        await client.kick(after)
                    except(discord.ClientException, discord.HTTPException):
                        try:
                            await client.add_roles(
                                after,
                                discord.utils.find(
                                    lambda role: 'fortnite' in role.name.lower()
                                    and not role.managed,
                                    after.server.roles))
                        except(discord.ClientException, discord.HTTPException):
                            pass

client = Client()
client.run('TOKEN')
