import logging
from datetime import datetime

from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask import current_app

from api import API

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.logger.setLevel(logging.DEBUG)

dmhyAPI = API()
unknown_subgroup_id = -1
unknown_subgroup_name = "未知字幕组"


@app.route("/")
def read_root():
    return jsonify(Hello="Welcome to use DanDanPlaySearchService")


@app.route("/subgroup")
def subgroup():
    _, data = dmhyAPI.get_types_and_subgroups()
    soup = BeautifulSoup(data, 'html.parser')
    options = soup.find(id='AdvSearchTeam')
    subgroups = [{'Id': int(option.get('value')), 'Name': option.text} for option in options.contents]
    subgroups.append({'Id': unknown_subgroup_id, 'Name': unknown_subgroup_name})
    return jsonify(Subgroups=subgroups)


@app.route("/type")
def type():
    _, data = dmhyAPI.get_types_and_subgroups()
    soup = BeautifulSoup(data, 'html.parser')
    options = soup.find(id='AdvSearchSort')
    types = [{'Id': int(option.get('value')), 'Name': option.text} for option in options.contents]
    return jsonify(Types=types)


@app.route("/list")
def list():
    keyword = request.args.get('keyword')
    sort_id = request.args.get('sort_id')
    team_id = request.args.get('team_id')
    r = request.args.get('r')
    sort_id = int(sort_id) if sort_id else 0
    team_id = int(team_id) if team_id else 0
    _, data = dmhyAPI.search(keyword=keyword, sort_id=sort_id, team_id=team_id)

    has_more = False
    resources = []
    try:
        soup = BeautifulSoup(data, 'html.parser')
        trs = soup.find(id='topic_list').find_all('tr')[1:]
        has_more = True if any(['下一頁' in getattr(div.find('a'), 'text', '') for div in
                                soup.find_all('div', class_='nav_title')]) else False

        for tr in trs:
            has_subgroup_info = (len(tr.find_all('td')[2].find_all('a')) == 2)
            try:
                resource = {
                    'Title': tr.find_all('td')[2].find_all('a')[-1].text.strip(),
                    'TypeId': int(tr.find_all('td')[1].a.get('href').split('/')[-1]),
                    'TypeName': tr.find_all('td')[1].a.text.strip(),
                    'SubgroupId': int(tr.find_all('td')[2].find_all('a')[0].get('href').split('/')[
                                          -1]) if has_subgroup_info else unknown_subgroup_id,
                    'SubgroupName': tr.find_all('td')[2].find_all('a')[
                        0].text.strip() if has_subgroup_info else unknown_subgroup_name,
                    'Magnet': tr.find_all('td')[3].a.get('href'),
                    'PageUrl': dmhyAPI.base_uri + tr.find_all('td')[2].find_all('a')[-1].get('href'),
                    'FileSize': tr.find_all('td')[4].text.strip(),
                    'PublishDate': datetime.strptime(
                        tr.find_all('td')[0].span.text.strip(), '%Y/%m/%d %H:%M'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                }
                resources.append(resource)
            except ValueError:
                pass
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.error(tr.pretty())
    except Exception as e:
        current_app.logger.error(e)
        current_app.logger.error("无法解析结果")
    finally:
        return jsonify(HasMore=has_more, Resources=resources)
