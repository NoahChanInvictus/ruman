# -*- coding: UTF-8 -*-
import json
import httplib


def get_lat_lng(city_list):
    results = {}
    for city in city_list:
        print 'city:', city
        city_item = city.split('\t')[-1].encode('utf-8')
        print 'city_item:', city_item, type(city_item)
        conn = httplib.HTTPConnection('api.map.baidu.com')
        url_string = 'https://api.map.baidu.com/geocoder/v2/?address='+ city_item + '&output=json&ak=Sz7fnFrQjivoX0u9pnQjXkM05B323EzO'
        conn.request(method='GET', url=url_string)
        response = conn.getresponse()
        res = response.read()
        res_dict = json.loads(res)
        try:
            lng = res_dict['result']['location']['lng']
            lat = res_dict['result']['location']['lat']
        except:
            lag = 0
            lng = 0
        results[city_item] = [lat, lng]
    return results


if __name__=='__main__':
    city_list = [u'北京', u'上海']
    get_lat_lng(city_list)
