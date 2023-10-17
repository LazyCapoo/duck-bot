from disnake.ext import commands
import disnake
import cv2
from deepface import DeepFace
import os
import matplotlib.pyplot as plt
import requests

class EmotionCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='find out how someone is feeling!!')
    async def emotioncheck(
            inter: disnake.ApplicationCommandInteraction,
            image: disnake.Attachment = commands.Param(default=None),
            link: str = commands.Param(default=None)
    ):
        await inter.response.defer()
        # Image uploads download the image to /images, links download to main folder
        if image is not None:
            name = image.filename
            path = os.path.join("images", name)
            await image.save(fp=path)
            img = cv2.imread(f'images\\{name}')
            plt.imshow(img[:, :, :: -1])
            try:
                result = DeepFace.analyze(img, actions=['emotion'])
            except ValueError:
                os.remove(f'images\\{name}')
                await inter.followup.send("There isnt a face in the picture, please fix that")

            file = disnake.File(path, filename=name)
            embed = disnake.Embed(title=f"This person is most likely {result[0]['dominant_emotion']}")
            embed.set_image(url="attachment://image.png")
            await inter.followup.send(file=file, embed=embed)
            os.remove(f'images\\{name}')
        if link is not None:
            data = requests.get(link).content
            f = open('img.jpg', 'wb')
            f.write(data)
            f.close()
            img = cv2.imread(f'img.jpg')
            plt.imshow(img[:, :, :: -1])
            try:
                result = DeepFace.analyze(img, actions=['emotion'])
            except ValueError:
                await inter.followup.send("There isnt a face in the picture, please fix that")

            file = disnake.File(fp='img.jpg', filename="img.jpg")
            embed = disnake.Embed(title=f"This person is most likely {result[0]['dominant_emotion']}")
            embed.set_image(url="attachment://img.png")
            await inter.followup.send(file=file, embed=embed)
            os.remove(f'img.jpg')

def setup(bot: commands.Bot):
    bot.add_cog(EmotionCommand(bot))