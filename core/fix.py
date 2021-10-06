# (c) @AbirHasan2005

from typing import List


async def FixEnvData(data: List[str]):
    cache_data = data
    if str(cache_data[1]).startswith(" "):
        cache_data[1] = cache_data[1].split(" ", 1)[-1]
    if str(cache_data[2]).startswith(" "):
        cache_data[2] = (
            "" if cache_data[2].isspace() else cache_data[2].split(" ", 1)[-1]
        )
    if (str(cache_data[3]).lower().strip() != "true") and (
        str(cache_data[3]).lower().strip() != "false"
    ):
        cache_data[3] = True
    elif str(cache_data[3]).lower().strip() == "true":
        cache_data[3] = True
    elif str(cache_data[3]).lower().strip() == "false":
        cache_data[3] = False
    if str(cache_data[4]) != "":
        cache_data[4] = "secret"
    return cache_data
