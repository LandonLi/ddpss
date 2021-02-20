from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import md5
from typing import Optional

import requests
from flask import current_app

cached_datas = dict()


def Cache(uuid_params_slice: str = '[1:]', expire_time: int = 600):
    """
    装饰器，缓存
    :param uuid_params_slice: 用于生成uuid的func的参数列表切片
    :param expire_time: 缓存超时时间
    :return: 调用此装饰器的方法缓存的数据
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 调用装饰器的函数名称
            func_name = func.__name__
            # 传入函数的用于生成uuid的参数列表
            copied_args = list(deepcopy(args))
            kwargs_pairs = [f'{key}={value}' for key, value in kwargs.items()]
            copied_args.extend(kwargs_pairs)
            uuid_params = eval(f'copied_args{uuid_params_slice}')
            # 生成的uuid
            m = md5()
            m.update('_'.join([str(param) for param in uuid_params] or []).encode('utf-8'))
            uuid = m.hexdigest()

            # 查询func上次缓存时间，没有则设置为当前时间
            cached_time = cached_datas.get(func_name, {}).get(uuid, {}).get('time')

            # 缓存超时
            if cached_time is None or cached_time + timedelta(seconds=expire_time) <= datetime.now():
                current_app.logger.info('无缓存/缓存超时')

                # 则重新执行func，更新缓存数据
                datas = func(*args, **kwargs)

                cached_datas[func_name] = {
                    uuid: {
                        'time': datetime.now(),
                        'datas': datas
                    }
                }

                query_time = cached_datas[func_name].get(uuid).get('time').strftime('%Y-%m-%d %H:%M:%S')
                return query_time, datas

            query_time = cached_datas[func_name].get(uuid).get('time').strftime('%Y-%m-%d %H:%M:%S')
            datas = cached_datas.get(func_name, {}).get(uuid, {}).get('datas')
            current_app.logger.info(
                f'命中缓存：<Func:{func.__name__}> {cached_time}，将过期于：{cached_time + timedelta(seconds=expire_time)}')
            return query_time, datas

        return wrapper

    return decorator


class API:
    def __init__(self):
        self.base_uri = 'https://share.dmhy.org'
        self.apis = {
            'types_and_subgroups': f'{self.base_uri}/topics/advanced-search?team_id=0&sort_id=0&orderby=',
            'search': f'{self.base_uri}/topics/list/page/1'
        }
        self.rsession = requests.session()

    def do_get(self, url: str, payload: Optional[dict] = None) -> str:
        """
        通用的get请求
        :param url: 请求的网址
        :param payload: 请求的参数
        :return: 返回的数据
        """
        response = self.rsession.get(url, params=payload, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == requests.codes.ok:
            data = response.text
            return data
        else:
            raise RuntimeError(f'response status code: {response.status_code}')

    @Cache(expire_time=86400)
    def get_types_and_subgroups(self):
        data = self.do_get(self.apis.get('types_and_subgroups'))
        return data

    @Cache()
    def search(self, keyword: str, sort_id: Optional[int] = 0, team_id: Optional[int] = 0, r: Optional[str] = None):
        payload = {
            'order': 'date-desc',
            'keyword': keyword,
            'sort_id': sort_id,
            'team_id': team_id
        }
        if r:
            payload['r'] = r
        data = self.do_get(self.apis.get('search'), payload=payload)
        return data
