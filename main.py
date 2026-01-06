import discord
from discord.ext import commands
from config import token
from logic import Pokemon

# Bot için yetkileri/intents ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Mesaj yazarının adını alma
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)  # Yeni bir Pokémon oluşturma
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi gönderilmesi
        image_url = await pokemon.show_img()  # Pokémon resminin URL'sini alma
        if image_url:
            embed = discord.Embed()  # Gömülü mesajı oluşturma
            embed.set_image(url=image_url)  # Pokémon'un görüntüsünün ayarlanması
            await ctx.send(embed=embed)  # Görüntü içeren gömülü bir mesaj gönderme
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  # Bir Pokémon'un daha önce oluşturulup oluşturulmadığını gösteren bir mesaj

@bot.command()
async def guess(ctx, tahmin: str):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        dogru_isim = await pokemon.get_name()
        
        if tahmin.lower() == dogru_isim.lower():
            Pokemon.points[author] += 100
            await ctx.send(f"Tebrikler {author}! Doğru bildin. +100 Puan kazandın!")
            pokemon.pokemon_number = random.randint(1, 1000)
            pokemon.name = await pokemon.get_name()
            await ctx.send(f"Yeni Pokémonun hazır! Resmini görmek için `!go` yazabilirsin.")
        else:
            await ctx.send(f"Maalesef yanlış! Bu Pokémon'un adı {dogru_isim} idi. Tekrar dene!")
    else:
        await ctx.send("Önce `!go` yazarak bir Pokémon edinmelisin!")

@bot.command()
async def mypoints(ctx):
    author = ctx.author.name
    puan = Pokemon.points.get(author, 0)
    await ctx.send(f"{author}, şu anki toplam puanın: {puan}")

# Botun çalıştırılması
bot.run(token)

# Botun çalıştırılması
bot.run(token)
