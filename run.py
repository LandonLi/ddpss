import logging
from datetime import datetime

from flask import Flask, jsonify, request
from flask import current_app
from lxml import etree

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
    html = etree.HTML(data)
    options = html.xpath('//select[@id="AdvSearchTeam"]/option')
    subgroups = [{'Id': int(option.get('value')), 'Name': option.text} for option in options]
    subgroups.append({'Id': unknown_subgroup_id, 'Name': unknown_subgroup_name})
    return jsonify(Subgroups=subgroups)


@app.route("/type")
def type():
    _, data = dmhyAPI.get_types_and_subgroups()
    html = etree.HTML(data)
    options = html.xpath('//select[@id="AdvSearchSort"]/option')
    types = [{'Id': int(option.get('value')), 'Name': option.text} for option in options]
    return jsonify(Types=types)


@app.route("/list")
def list():
    keyword = request.args.get('keyword')
    sort_id = request.args.get('sort_id')
    team_id = request.args.get('team_id')
    r = request.args.get('r')
    sort_id = int(sort_id) if sort_id else 0
    team_id = int(team_id) if sort_id else 0
    _, data = dmhyAPI.search(keyword=keyword, sort_id=sort_id, team_id=team_id)
    html = etree.HTML(data)
    trs = html.xpath('//table[@id="topic_list"]/tbody/tr')
    has_more = True if html.xpath('//div[@class="nav_title"]/a[contains(text(), "下一頁")]') else False

    resources = []
    for tr in trs:
        has_subgroup_info = (len(tr.xpath('./td[3]//a')) == 2)
        try:
            resource = {
                'Title': ''.join(tr.xpath('./td[3]/a/text()')).strip(),
                'TypeId': int(tr.xpath('./td[2]/a/@href')[0].split('/')[-1]),
                'TypeName': tr.xpath('./td[2]/a/font')[0].text.strip(),
                'SubgroupId': int(
                    tr.xpath('./td[3]/span/a/@href')[0].split('/')[-1]) if has_subgroup_info else unknown_subgroup_id,
                'SubgroupName': tr.xpath('./td[3]/span/a')[
                    0].text.strip() if has_subgroup_info else unknown_subgroup_name,
                'Magnet': tr.xpath('./td[4]/a/@href')[0],
                'PageUrl': dmhyAPI.base_uri + tr.xpath('./td[3]/a/@href')[0],
                'FileSize': tr.xpath('./td[5]')[0].text.strip(),
                'PublishDate': datetime.strptime(tr.xpath('./td[1]/span')[0].text.strip(), '%Y/%m/%d %H:%M').strftime(
                    '%Y-%m-%d %H:%M:%S')
            }
            resources.append(resource)
        except ValueError:
            pass
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(etree.tostring(tr, pretty_print=True))

    return jsonify(HasMore=has_more, Resources=resources)
