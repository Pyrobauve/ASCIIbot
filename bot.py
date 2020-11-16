import argparse
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
import discord
from discord.ext import commands
import os
import config

bot = commands.Bot(command_prefix='a/')
bot.remove_command('help')

TOKEN = config.TOKEN
dir = "data"
path = config.PATH

@bot.event
async def on_ready():
    print('-------------')
    print(bot.user.name)
    print('-------------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='ASCII Art | a/help'))

@bot.command()
async def help(ctx): #help command to check the command
    await ctx.message.delete(delay=None)
    await ctx.send("The command is: \n `a/ascii <arg> <arg>` --> Send an image by adding a comment.\n \n The different arguments you can add are: \n Character: \n     -`simple`: simple character in ASCII \n     -`complex`: more character in ASCII \n \n Background color: \n     -`black`: the background color is black \n     -`white`: the background color is white \n \n Arguments are optional, by default argument is `simple` and `white`.", delete_after=30)

@bot.command()
async def ascii(ctx, arg="simple", arg2="white"): #ascii command to convert an image
    dir = ctx.author.id

    if ctx.message.attachments: #Check the attachements
    
#Replace argument in the correct variable
        if arg != arg2:
            if arg == "white" or arg =="black" and arg2 == "simple" or arg2 == "complex":
                arg,arg2 = arg2,arg
    
            elif arg == "white" or arg=="black":
                arg2 = arg
                arg = "simple"
                
#Check if the arguments is correct  
            if arg == "simple" or arg == "complex":
                if arg2 == "white" or arg2 == "black":
                
#Initialization of the ASCII generator
                    def get_args():
                        parser = argparse.ArgumentParser("Image to ASCII")
                        parser.add_argument("--input", type=str, default=f"{dir}/input.jpg", help="Path to input image")
                        parser.add_argument("--output", type=str, default=f"{dir}/output.jpg", help="Path to output text file")
                        parser.add_argument("--mode", type=str, default="simple", choices=["simple", "complex"],
                                help="10 or 70 different characters")
                        parser.add_argument("--background", type=str, default="white", choices=["black", "white"],
                            help="background's color")
                        parser.add_argument("--num_cols", type=int, default=200, help="number of character for output's width")
                        parser.add_argument("--scale", type=int, default=2, help="upsize output")
                        args = parser.parse_args()
                        return args

#Create the user folder and download the image   
                    async with ctx.typing():
                        files = []
                        os.system(f"mkdir {dir}")
                        for i in ctx.message.attachments:
                            files.append(i)
                            await i.save(f"{path}{dir}/{i.filename}")
                        os.system(f'mv {path}{dir}/{i.filename} {path}{dir}/input.jpg')

#ASCII conversion on user folder
                        def main(opt):
                            if arg == "simple":
                                CHAR_LIST = '@%#*+=-:. '
                            else:
                                    CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
                            if arg2 == "white":
                                bg_code = 255
                            else:
                                bg_code = 0
                            font = ImageFont.truetype(f"{path}fonts/DejaVuSansMono-Bold.ttf", size=10 * opt.scale)
                            num_chars = len(CHAR_LIST)
                            num_cols = opt.num_cols
                            image = cv2.imread(opt.input)
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            height, width = image.shape
                            cell_width = width / opt.num_cols
                            cell_height = 2 * cell_width
                            num_rows = int(height / cell_height)
                            if num_cols > width or num_rows > height:
                                print("Too many columns or rows. Use default setting")
                                cell_width = 6
                                cell_height = 12
                                num_cols = int(width / cell_width)
                                num_rows = int(height / cell_height)
                            char_width, char_height = font.getsize("A")
                            out_width = char_width * num_cols
                            out_height = 2 * char_height * num_rows
                            out_image = Image.new("L", (out_width, out_height), bg_code)
                            draw = ImageDraw.Draw(out_image)
                            for i in range(num_rows):
                                line = "".join([CHAR_LIST[min(int(np.mean(image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                                                        int(j * cell_width):min(int((j + 1) * cell_width),
                                                                                                width)]) * num_chars / 255), num_chars - 1)]
                                                for j in
                                                range(num_cols)]) + "\n"
                                draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)

                            if arg2 == "white":
                                cropped_image = ImageOps.invert(out_image).getbbox()
                            else:
                                cropped_image = out_image.getbbox()
                            out_image = out_image.crop(cropped_image)
                            out_image.save(opt.output)

                        if __name__ == '__main__':
                            opt = get_args()
                            main(opt)
            
#Send of the ASCII image, deletion of the user folder and its contents 
                        os.system(f"mv {path}{dir}/output.jpg {path}{dir}/{i.filename}")
                        await ctx.message.channel.send(file=discord.File(f"{path}{dir}/{i.filename}"))
                        os.system(f'rm -r {dir}')
    
                    await ctx.message.delete(delay=None)
#Error messages
                else:
                    await ctx.message.delete(delay=None)
                    await ctx.send("You used a bad argument. a/help to see valid arguments.", delete_after=10)
            else:
                await ctx.message.delete(delay=None)
                await ctx.send("You used a bad argument. a/help to see valid arguments.", delete_after=10)
        else:
            await ctx.message.delete(delay=None)
            await ctx.send("Don't repeat the same argument twice.", delete_after=10)
    else:
        await ctx.message.delete(delay=None)
        await ctx.send("You must send an image with this command.",delete_after=10)

bot.run(TOKEN)
