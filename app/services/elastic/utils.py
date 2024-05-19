import asyncio
import aiofiles


def normalize(word):
    import re
    word_ = re.sub(r'[^а-яёА-ЯЁa-zA-Z0-9\s-]', '', word)
    return word_.strip()


async def get_records(file_path):
    res = []
    async with aiofiles.open(file_path, mode='r') as f:
        async for line in f:
            id_, name = line.strip().split(';')

            res.append(
                {
                    'id': int(id_),
                    'name': name,
                    "name_normalized": normalize(name)
                }
            )
    return res
