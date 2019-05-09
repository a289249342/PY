import My_orm
from My_model import User, Blog, Comment
import asyncio


async def test(loop):
    await My_orm.create_pool(loop=loop, user='www-data', password='www-data', db='awesome')
    u = User(name='Test', email='test@example.com', passwd='884443', image='about:blank')
    await u.save()
    await My_orm.destory_pool()


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
