import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT_1 = os.getenv("TOKEN_BOT_1")
TOKEN_BOT_2 = os.getenv("TOKEN_BOT_2")

# =========================================================
# INTENTS
# =========================================================
intents = discord.Intents.all()

# =========================================================
# BOTS
# =========================================================
bot1 = commands.Bot(
    command_prefix="!",
    intents=intents
)
bot2 = commands.Bot(
    command_prefix="?",
    intents=intents
)

# =========================================================
# ACTIVIDADES BOT 1
# =========================================================
actividades_bot1 = [
    discord.Activity(
        type=discord.ActivityType.listening,
        name="BUENOS AIRES RP | BA"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Made by:✨cristhiangamer✨"
    )
]
indice_bot1 = 0

@tasks.loop(seconds=30)
async def rotar_bot1():
    global indice_bot1
    actividad = actividades_bot1[indice_bot1]
    await bot1.change_presence(
        status=discord.Status.online,
        activity=actividad
    )
    indice_bot1 = (indice_bot1 + 1) % len(actividades_bot1)

@bot1.event
async def on_ready():
    global indice_bot1
    print(f"✅ Bot 1 conectado como {bot1.user}")
    if not rotar_bot1.is_running():
        indice_bot1 = 0
        rotar_bot1.start()
    
    # ✅ Sincronizar comandos en tu servidor
    ID_SERVIDOR = discord.Object(id=1512640372701003877)
    try:
        await bot1.tree.sync(guild=ID_SERVIDOR)
        print("✅ Comandos Bot 1 sincronizados")
    except Exception as e:
        print(f"⚠️ Error sincronizando Bot 1: {e}")

# =========================================================
# ACTIVIDADES BOT 2
# =========================================================
actividades_bot2 = [
    discord.Activity(
        type=discord.ActivityType.listening,
        name="STAFF | Buenos Aires RP"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Made by:✨cristhiangamer✨"
    )
]
indice_bot2 = 0

@tasks.loop(seconds=30)
async def rotar_bot2():
    global indice_bot2
    actividad = actividades_bot2[indice_bot2]
    await bot2.change_presence(
        status=discord.Status.online,
        activity=actividad
    )
    indice_bot2 = (indice_bot2 + 1) % len(actividades_bot2)

@bot2.event
async def on_ready():
    global indice_bot2
    print(f"✅ Bot 2 conectado como {bot2.user}")
    if not rotar_bot2.is_running():
        indice_bot2 = 0
        rotar_bot2.start()
    
    # ✅ Sincronizar comandos en tu servidor
    ID_SERVIDOR = discord.Object(id=1512640372701003877)
    try:
        await bot2.tree.sync(guild=ID_SERVIDOR)
        print("✅ Comandos Bot 2 sincronizados")
    except Exception as e:
        print(f"⚠️ Error sincronizando Bot 2: {e}")

# =========================================================
# CARGAR COGS
# =========================================================
async def cargar_cogs_bot1():
    carpeta = "./cogs_bot1"
    if not os.path.exists(carpeta):
        print("⚠️ No existe la carpeta cogs_bot1")
        return
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".py") and not archivo.startswith("_"):
            try:
                await bot1.load_extension(f"cogs_bot1.{archivo[:-3]}")
                print(f"✅ Bot 1 | Cog cargado: {archivo}")
            except Exception as e:
                print(f"❌ Error cargando {archivo}: {e}")

async def cargar_cogs_bot2():
    carpeta = "./cogs_bot2"
    if not os.path.exists(carpeta):
        print("⚠️ No existe la carpeta cogs_bot2")
        return
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".py") and not archivo.startswith("_"):
            try:
                await bot2.load_extension(f"cogs_bot2.{archivo[:-3]}")
                print(f"✅ Bot 2 | Cog cargado: {archivo}")
            except Exception as e:
                print(f"❌ Error cargando {archivo}: {e}")

# =========================================================
# MANTENER ACTIVO EN RENDER
# =========================================================
from flask import Flask
import threading
app = Flask(__name__)

@app.route('/')
def mantener_activo():
    return "✅ Bots activos"

def iniciar_servidor():
    app.run(host="0.0.0.0", port=8080)

servidor = threading.Thread(target=iniciar_servidor)
servidor.daemon = True
servidor.start()

# =========================================================
# INICIAR
# =========================================================
async def main():
    await cargar_cogs_bot1()
    await cargar_cogs_bot2()
    await asyncio.gather(
        bot1.start(TOKEN_BOT_1),
        bot2.start(TOKEN_BOT_2)
    )

if __name__ == "__main__":
    asyncio.run(main())
