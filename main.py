import discord
from discord.ext import commands
import os

bot_token = os.environ.get('token')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Çevresel değişkenler veya yapılandırma dosyasından log bilgilerini alın
log_guild_id = 1145353323269079134  # Log sunucusunun ID'si
log_channel_id = 1147902537974960339  # Log kanalının ID'si
moderator_role_name = 'moderator'  # Moderatör rolünün adını burada değiştirin

@bot.event
async def on_ready():
    print(f'{bot.user} aktif!')

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="/44atv"))


@bot.event
async def on_member_update(before, after):
    try:
        removed_roles = set(before.roles) - set(after.roles)
        added_roles = set(after.roles) - set(before.roles)

        log_guild = bot.get_guild(log_guild_id)
        log_channel = log_guild.get_channel(log_channel_id)

        user_name_member = f"{after.name}#{after.discriminator}"  # Rolü alınan veya verilen üye
        server_name = before.guild.name

        # Get the audit logs
        audit_logs = []
        async for log in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
            audit_logs.append(log)

        # The person who made the change is the 'user' of the first (and in this case, only) entry in the audit log
        moderator = audit_logs[0].user
        moderator_name = f"{moderator.name}#{moderator.discriminator}"
        moderator_avatar = moderator.avatar.url if moderator.avatar else None

        # If the moderator is a bot, skip this iteration
        if moderator.bot:
            return

        # İşlemi gerçekleştiren kişi bot değilse
        if not after.bot:
            for role in removed_roles:
                if not any(member.bot for member in role.members):
                    role_name = role.name

                    embed = discord.Embed(
                        title="BİR ROL ALINDI",
                        color=0xFF0000  # Kırmızı renk
                    )
                    embed.set_thumbnail(url=before.guild.icon.url)
                    embed.add_field(
                        name="__**Moderatör**__",
                        value=moderator_name,
                        inline=False
                    )
                    embed.add_field(
                        name="__**Üye**__",
                        value=user_name_member,
                        inline=False
                    )
                    embed.add_field(
                        name="__**Alınan Rol**__",
                        value=role_name,
                        inline=False
                    )
                    embed.add_field(
                        name="__**Sunucu Adı**__",
                        value=server_name,
                        inline=False
                    )
                    embed.set_footer(icon_url=moderator_avatar)
                    embed.timestamp = discord.utils.utcnow()

                    await log_channel.send(embed=embed)

            for role in added_roles:
                if not any(member.bot for member in role.members):
                    role_name = role.name

                    embed = discord.Embed(
                        title="BİR ROL VERİLDİ",
                        color=0x00FF00  # Yeşil renk
                    )
                    embed.set_thumbnail(url=before.guild.icon.url)
                    embed.add_field(
                        name="__**Moderatör**__",
                        value=moderator_name,
                        inline=False
                    )
                    embed.add_field(
                        name="__**Üye**__",
                        value=user_name_member,
                        inline=False
                    )
                    embed.add_field(
                        name="__**Verilen Rol**__",
                        value=role_name,
                        inline=False
                    )
                    embed.add_field(
                        name="__**Sunucu Adı**__",
                        value=server_name,
                        inline=False
                    )
                    embed.set_footer(icon_url=moderator_avatar)
                    embed.timestamp = discord.utils.utcnow()

                    await log_channel.send(embed=embed)
    except Exception as e:
        print(f'Hata oluştu: {e}')

bot.run(bot_token)
