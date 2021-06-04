import _pickle as cPickle
import redis

from app.config import REDIS_URL, REDIS_MAX_CONNECTIONS


class Redis(object):
    def __init__(self):
        self.client = redis.StrictRedis.from_url(
            REDIS_URL, max_connections=REDIS_MAX_CONNECTIONS
        )

    def __getattr__(self, name):
        return getattr(self.client, name)

    def get(self, name):
        r = self.client.get(name)
        if r:
            return cPickle.loads(r)
        else:
            return None

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        v = cPickle.dumps(value)
        return self.client.set(name=name, value=v, ex=ex, px=px, nx=nx, xx=xx)

    def add(self, name, value, expire=0):
        if value is None and expire > 0:
            self.client.expire(name, expire)
            return self.get(name)

        if value:
            r = self._client.incrby(name, value)
            if expire:
                self._client.expire(name, expire)
            return r

    def hgetall(self, key):
        data = self.client.hgetall(key)
        if data:
            data = {name.decode("utf-8"): cPickle.loads(value) for name, value in data.items()}
        return data

    def hmget(self, key, *names):
        data = self.client.hmget(key, names)
        if data:
            data = [cPickle.loads(item) for item in data]
        return data

    def hset(self, key, name=None, value=None, mapping=None):
        if name and value:
            value = cPickle.dumps(value)
            self.client.hset(key, name, value)
        if mapping:
            mapping = {name: cPickle.dumps(value) for name, value in mapping.items()}
            self.client.hmset(key, mapping)

    def lpush(self, name, *values):
        return self.client.lpush(name, *values)

    def lpop(self, name):
        return self.client.pop(name)

    def llen(self, name):
        return self.client.llen(name)

    def lrange(self, name, start, end):
        return self.client.lrange(name, start, end)

    def lrem(self, name, count, value):
        return self.client.lrem(name, count, value)

    def delete(self, *keys):
        if len(keys) < 1:
            return
        return self.client.delete(*keys)

    def flushdb(self):
        self.client.flushdb()

    def delete_pattern(self, pattern, batch_size=2000):
        """
        This method uses Redis's `scan` command to delete all
        keys with given pattern instead of using `keys` command (which
        may introduce performance issues, see http://redis.io/commands/keys).

        Internally this method repeatedly call `scan` until the whole
        collection is scanned.

        This method is not atomic, you should not use this if atomicity is
        vital. (for general cases this method should be ok).

        If the size of database is growing fast enough, this method may never
        terminate. (depends on the `batch_size` parameter and the
        speed of growth)

        :param str pattern: pattern to delete
        :param int batch_size: the batch size to examine, passed to redis as
            `count` parameter.
        """
        cursor = 0
        while True:
            cursor, keys = self.scan(cursor, match=pattern, count=batch_size)
            self.delete(*keys)
            if cursor == 0:
                break

    def get_keys_by_pattern(self, pattern, max_num=1000, batch_size=2000):
        """从 Redis 中获取满足某个 pattern 的 key。
        支持的 pattern 跟 redis keys 命令一样。

        :param str pattern: 要匹配的 pattern
        :param int max_num: 最多获取多少个 key
        :param int batch_size: 每次遍历的 key 的数量，不满足 pattern 的 key 也会计算，因此 \
            每次实际返回的 key 的数量会小于等于 batch_size
        :return: 返回一个匹配的 key 的迭代器
        """
        cursor = 0
        count = 0
        while True:
            cursor, result = self.scan(cursor, match=pattern, count=batch_size)
            count += len(result)
            for key in result:
                yield key
            if count >= max_num:
                return
            if cursor == 0:
                return


cache = Redis()
