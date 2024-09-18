import discord
from discord.ext import commands
import aiohttp
import base64
from io import BytesIO
from PIL import Image

@bot.command(name='captcha')
async def generate_captcha(ctx):
    api_url = 'http://localhost:5000/api/generate_captcha'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    captcha_data = data['captcha_data']
                    
                    captcha_bytes = base64.b64decode(captcha_data.split(",")[1])
                    
                    with Image.open(BytesIO(captcha_bytes)) as img:
                        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
                        
                        buffer = BytesIO()
                        img.save(buffer, format="PNG")
                        buffer.seek(0)
                        
                    file = discord.File(buffer, filename="captcha.png")
                    
                    embed = discord.Embed(description="```fix\ncaptcha:```")
                    embed.set_image(url="attachment://captcha.png")

                    await ctx.send(file=file, embed=embed)
                else:
                    await ctx.send("```fix\nfailed to generate captcha```")
        except aiohttp.ClientError:
            await ctx.send("```fix\nthis api is offline```")
        except Exception as e:
            await ctx.send(f"```fix\n{e}```")
