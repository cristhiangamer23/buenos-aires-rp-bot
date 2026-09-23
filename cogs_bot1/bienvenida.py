import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from typing import Literal

CANAL_BIENVENIDA_ID = 1512640379156041734

class Bienvenida(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archivo = "autoroles.json"
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def cargar_datos(self):
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar_datos(self, datos):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    # ===================== EMBED con Components V2 =====================
    def crear_embed_bienvenida(self, member: discord.Member):
        """Embed profesional optimizado para Components V2"""
        servidor_icon = member.guild.icon.url if member.guild.icon else None
        
        embed = discord.Embed(
            description=(
                f"## 🎉 Bienvenido, {member.mention}\n\n"
                f"Te damos la más cordial bienvenida a **Buenos Aires Roleplay**, "
                f"una comunidad dedicada a ofrecer una experiencia de rol seria, "
                f"organizada y de excelencia.\n\n"
                f"🏙️ Aquí podrás crear historias inolvidables, vivir experiencias únicas "
                f"y formar parte de una comunidad que valora el respeto y la calidad.\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"### 📋 Para comenzar:\n"
                f"✅ Lee detenidamente las normas del servidor\n"
                f"✅ Revisa los canales de información\n"
                f"✅ Mantén siempre el respeto hacia todos los miembros\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"💙 ¡Que disfrutes tu estadía!"
            ),
            color=0x2B6CB0  # Azul elegante y profesional
        )
        
        embed.set_author(
            name="Buenos Aires Roleplay",
            icon_url=servidor_icon
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        
        embed.set_footer(
            text="Buenos Aires Roleplay • Comunidad Oficial",
            icon_url=servidor_icon
        )
        
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member):
        datos = self.cargar_datos()
        guild_id = str(member.guild.id)
        if guild_id in datos:
            config = datos[guild_id]
            if not member.bot:
                for rol_id in config.get("usuarios", []):
                    rol = member.guild.get_role(int(rol_id))
                    if rol:
                        await member.add_roles(rol)
            if member.bot:
                for rol_id in config.get("bots", []):
                    rol = member.guild.get_role(int(rol_id))
                    if rol:
                        await member.add_roles(rol)
            for rol_id in config.get("ambos", []):
                rol = member.guild.get_role(int(rol_id))
                if rol:
                    await member.add_roles(rol)
        canal = member.guild.get_channel(CANAL_BIENVENIDA_ID)
        if canal:
            embed = self.crear_embed_bienvenida(member)
            await canal.send(
                content=f"🎊 ¡Un nuevo integrante se une a nosotros — {member.mention}!",
                embed=embed,
                flags=discord.MessageFlags.is_components_v2()
            )

    @app_commands.command(
        name="panel_bienvenida",
        description="Muestra una vista previa del mensaje de bienvenida"
    )
    async def panel_bienvenida(self, interaction: discord.Interaction):
        embed = self.crear_embed_bienvenida(interaction.user)
        await interaction.response.send_message(
            embed=embed,
            flags=discord.MessageFlags.is_components_v2()
        )

    @app_commands.choices(tipo=[
        app_commands.Choice(name="Usuarios", value="usuarios"),
        app_commands.Choice(name="Bots", value="bots"),
        app_commands.Choice(name="Ambos", value="ambos"),
    ])
    @app_commands.describe(
        roles="Menciona los roles con @ que se asignarán automáticamente",
        tipo="Tipo de usuario que recibirá los roles"
    )
    @app_commands.command(
        name="autoroles",
        description="Configura los roles automáticos"
    )
    async def autoroles(
        self,
        interaction: discord.Interaction,
        roles: str,
        tipo: Literal["usuarios", "bots", "ambos"]
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Sin permisos", ephemeral=True)
            return
        await interaction.response.defer()
        lista_roles = []
        for r in roles.split():
            r = r.replace("<@&", "").replace(">", "")
            if r.isdigit():
                rol = interaction.guild.get_role(int(r))
                if rol:
                    lista_roles.append(str(rol.id))
        if not lista_roles:
            await interaction.followup.send("❌ No se detectaron roles válidos")
            return
        datos = self.cargar_datos()
        guild_id = str(interaction.guild.id)
        if guild_id not in datos:
            datos[guild_id] = {
                "usuarios": [],
                "bots": [],
                "ambos": []
            }
        for r in lista_roles:
            if r not in datos[guild_id][tipo]:
                datos[guild_id][tipo].append(r)
        self.guardar_datos(datos)
        embed_conf = discord.Embed(
            title="✅ Rol de autorol agregado",
            description=(
                f"**Tipo:** {tipo}\n\n"
                f"**Roles agregados:** {', '.join([f'<@&{r}>' for r in lista_roles])}"
            ),
            color=discord.Color.green()
        )
        await interaction.followup.send(
            embed=embed_conf,
            flags=discord.MessageFlags.is_components_v2()
        )

async def setup(bot):
    await bot.add_cog(Bienvenida(bot))
