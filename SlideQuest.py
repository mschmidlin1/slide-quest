import asyncio

from sq_src.window import Window


async def main():
    window = Window()
    await window.run()


if __name__ == "__main__":
    asyncio.run(main())