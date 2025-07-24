from ib_insync import IB
import functools
import inspect
import os
from dotenv import load_dotenv

load_dotenv()

def with_ib_connection(_func=None):

    host = os.getenv('IB_HOST')
    port = int(os.getenv('IB_PORT'))
    clientId = int(os.getenv('IB_CLIENT_ID'))

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            ib = IB()
            await ib.connectAsync(host, port, clientId=clientId)
            try:
                return await func(ib, *args, **kwargs)
            finally:
                ib.disconnect()
        return wrapper
    if _func and inspect.iscoroutinefunction(_func):
        return decorator(_func)
    
    return decorator