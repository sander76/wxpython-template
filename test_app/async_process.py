import asyncio
import logging

import sys

LOGGER = logging.getLogger("__name__")



async def start_process(logger):
    pth = r"C:\Users\sander\Dropbox\data\aptana\wxpython-template\test_app\long_running_process.py"

    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            pth,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except Exception as err:
        LOGGER.exception(err)

    else:
        try:
            while not process.stdout.at_eof():
                line = await process.stdout.readline()
                logger(line.decode("ascii"))
            code = await process.wait()
            logger("finished with {}".format(code))
        except Exception as err:
            LOGGER.exception(err)

async def start_process_and_return():
    pth = r"C:\Users\sander\Dropbox\data\aptana\wxpython-template\test_app\long_running_process.py"

    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            pth,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except Exception as err:
        LOGGER.exception(err)
    else:
        return process


async def process_manager(process, logger):
    try:
        while not process.stdout.at_eof():
            line = await process.stdout.readline()
            logger(line.decode("ascii"))
        code = await process.wait()
        logger("finished with {}".format(code))
    except Exception as err:
        LOGGER.exception(err)


# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(
#         asyncio.WindowsProactorEventLoopPolicy())
#
# date = asyncio.run(start_process())
