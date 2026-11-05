# /// script
# dependencies = [
#   "numpy",
# ]
# ///
import numpy
import asyncio
import pygame

pygame.init()

from sq_src.window import Window


async def main():
    # Let the browser finish mounting the game archive before loading assets.
    await asyncio.sleep(0)
    window = Window()
    await window.run()


asyncio.run(main())
