import discord
import requests
import asyncio
import os

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
SERVERS_API   = "https://www.grandarena.game/api/servers/status"

SERVIDORES = {
    "saopaulo-01":  {"nombre": "🇧🇷 Brasil",   "canal_id": 1496371797761855609},
    "virginia-01":  {"nombre": "🇺🇸 Virginia",  "canal_id": 1496372065383616582},
    "paris-01":     {"nombre": "🇫🇷 Francia",   "canal_id": 1496372118852468766},
    "singapore-01": {"nombre": "🇸🇬 Singapur",  "canal_id": 1496372175656194189},
}

HEADERS_WEB = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.grandarena.game/lobby"
}

intents = discord.Intents.default()
client  = discord.Client(intents=intents)

async def actualizar_canales():
    await client.wait_until_ready()
    print("🟢 Bot conectado, actualizando canales...")

    while not client.is_closed():
        try:
            r    = requests.get(SERVERS_API, headers=HEADERS_WEB, timeout=5)
            data = r.json()

            for server_id, info in SERVIDORES.items():
                if server_id not in data:
                    continue

                players = data[server_id]["players"]
                emoji   = "🟢" if players > 0 else "🔴"
                nombre  = info["nombre"]
                nuevo_nombre = f"{emoji} {nombre}: {players} jugador{'es' if players != 1 else ''}"

                canal = client.get_channel(info["canal_id"])
                if canal and canal.name != nuevo_nombre:
                    await canal.edit(name=nuevo_nombre)
                    print(f"Actualizado: {nuevo_nombre}")

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(10)  # Discord permite editar nombres cada ~5-10 segundos

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    client.loop.create_task(actualizar_canales())

client.run(DISCORD_TOKEN)
