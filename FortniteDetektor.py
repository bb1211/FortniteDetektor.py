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

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)

    async def on_member_update(self, before, after):
        foo = before.activities != after.activities

        bar = False
        for activity in after.activities:
            try:
                if activity.application_id == 432980957394370572:
                    bar = True
                    break
            except AttributeError:
                pass

        if foo and bar:
            asozial = after.guild.id == 367648314184826880

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

client = Client()
client.run('TOKEN')
