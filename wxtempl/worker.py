import asyncio
import sys
from threading import Thread
import logging

LOGGER = logging.getLogger(__name__)


def _get_loop():
    if sys.platform == "win32":
        return asyncio.ProactorEventLoop()
    return asyncio.new_event_loop()


async def start_process_and_return(*args):
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except Exception as err:
        LOGGER.exception(err)
    else:
        return process


class Worker:
    """Worker class.

    Responsible for managing async tasks running inside another thread."""

    _loop = None
    _futures = []
    _worker_thread = None
    _processes = []
    _finish_tasks=[]

    def __init__(self):
        if Worker._loop is None:
            Worker._loop = _get_loop()
        if Worker._worker_thread is None:
            Worker._worker_thread = Thread(target=self._start_worker_loop)
        if not Worker._worker_thread.isAlive():
            Worker._worker_thread.start()

    def _start_worker_loop(self):
        """Start a worker asyncio loop

        This is run inside a separate thread."""
        asyncio.set_event_loop(Worker._loop)
        Worker._loop.run_forever()
        LOGGER.debug("worker loop stopped")
        Worker._loop.close()
        LOGGER.debug("worker loop closed")

    def start_process(self, *args, callback=None):
        fut = self.do_work(start_process_and_return(*args))
        process = fut.result()
        self._processes.append(process)
        return process

    def do_work(self, coro, callback=None):
        fut = asyncio.run_coroutine_threadsafe(coro, Worker._loop)
        if callback:
            fut.add_done_callback(callback)
        Worker._futures.append(fut)
        return fut

    def wait_to_finish(self):
        LOGGER.info("Waiting for worker thread to close.")
        Worker._worker_thread.join()

    def subscribe_to_finish_tasks(self,callback):
        self._finish_tasks.append(callback)

    def stop_worker(self, *args, **kwargs):
        LOGGER.info("Signal to stop worker thread.")
        
        for tasks in self._finish_tasks:
            tasks()
        
        for process in self._processes:
            try:
                process.terminate()
            except ProcessLookupError:
                LOGGER.info(
                    "trying to finish {}. But probably already finished".format(
                        process
                    )
                )
            except Exception as err:
                LOGGER.exception(err)

        Worker._loop.call_soon_threadsafe(self._loop.stop)
