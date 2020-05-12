# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import collections
import sys

sys.path.append('/data/backend/apihome-service/')
import re
import time
import datetime
import csv
import json
import os
import platform
import xmltodict
import hashlib
from sqlalchemy import create_engine, between
from sqlalchemy.orm import sessionmaker
from locust import HttpLocust, TaskSet, task, between
import requests
from urllib3.exceptions import InsecureRequestWarning
import random
import queue
from PFLocust.locustAssert import tryJson, WechatEncrypt, JD_3DES, KFQ_AES, locust_jjxt_postUrl, locust_jjxt_getUrl, \
    pf_getdata_byRe, pfassert_string_re, pfassert_level, pfassert, pf_level_value, my_replace

requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告


class AppAPIUser:

    def __init__(self):
        self.app = {
            'app_key': 'ho2dxs9g',
            'encrypt_key': 'i2yrl3kj',
            'version': '4.4.8',
            'token': '320216DB-4E9D-457C-832C-B7FB2FFFD781',
            'device': 'iPhoneX'
        }
        self.uid = 0
        self.sk = ''
        self.account = ''

    def signature(self, data):
        ret = collections.OrderedDict(sorted(data.items()))
        str_value = ""
        for k, v in ret.items():
            str_value += str(k)
            str_value += str(v)
        str_value += self.app['encrypt_key']
        # print(str_value)
        m = hashlib.md5()
        m.update(str_value.encode('utf-8'))
        md5value = m.hexdigest()
        return md5value

    def add_common_entry(self, data, uid, sk):
        ret = data
        ret['app_key'] = self.app['app_key']
        ret['v'] = '4.0'
        ret['token'] = self.app['token']
        ret['app_version'] = self.app['version']
        ret['device'] = self.app['device']
        if uid:
            ret['uid'] = uid
        if sk:
            ret['sk'] = sk

        return ret

    def sig_dict(self, query, uid, sk):
        data = self.add_common_entry(query, uid, sk)
        sig = self.signature(data)
        data['sig'] = sig
        return data

    def sig_post_json(self, body, query, uid, sk):
        bodystr = json.dumps(body)
        tm = int(time.time() * 1000)

        tempbody = {}
        tempbody['x-hx-timestamp'] = str(tm)
        tempbody['x-hx-app-key'] = self.app['app_key']
        tempbody['x-hx-token'] = self.app['token']
        tempbody['x-hx-app-version'] = self.app['version']
        tempbody['x-hx-device'] = self.app['device']
        tempbody['x-hx-sk'] = sk

        tempbody['body'] = bodystr
        tempbody = self.add_common_entry(tempbody, uid, sk)

        sig = self.signature(tempbody)

        headers = {
            'x-hx-timestamp': tempbody['x-hx-timestamp'],
            'x-hx-app-key': tempbody['x-hx-app-key'],
            'x-hx-token': tempbody['x-hx-token'],
            'x-hx-app-version': tempbody['x-hx-app-version'],
            'x-hx-device': tempbody['x-hx-device'],
            'x-hx-sk': tempbody['x-hx-sk'],
            'x-hx-sig': sig
        }

        retquery = self.add_common_entry(query, uid, sk)
        retquery['sig'] = self.signature(retquery)

        return retquery, headers


app = AppAPIUser()


class WebsiteTasks(TaskSet):

    def on_start(self):

        try:
            self.gd = self.locust.queueData.get()

        except:
            exit(0)

        self.gd['ucenter'] = 'http://ucenter1.highso.com.cn'
        self.gd['k2'] = 'http://api.k2.reg.highso.com.cn'
        self.gd['end'] = 'http://t1.highso.com.cn'
        self.gd['crm_cx'] = 'http://cx1.highso.com.cn'
        self.gd['www_web'] = 'http://w1.highso.com.cn'
        self.gd['antd'] = 'http://antd.k2.reg.highso.com.cn/redirect'
        self.gd['haixue_app_api'] = 'http://a1.highso.com.cn'
        self.gd['H5_api'] = 'http://api-marketing-activities.reg.highso.com.cn'
        self.gd['haxiue_app'] = 'http://a1.highso.com.cn'

        self.haixueAPPLogin()
        self.WWWLogin()

    # 嗨学课堂登录ios登录
    def haixueAPPLogin(self):
        url = self.gd['haxiue_app'] + '/customer/v1/login.do'
        data = app.sig_dict({'userName': self.gd['app_username'], 'password': '123456'}, 0, '')
        with self.client.post(url, data=data, name='嗨学课堂appIOS登录', catch_response=True) as res:
            if res.status_code == 200:
                resp = res.text
                try:
                    resdata = tryJson(resp)
                except:
                    resdata = resp
                check = '{"m":"ok"}'
                try:
                    pfassert(resdata=resdata, assertRule='contains', check=check)
                    res.success()
                except Exception as e:
                    res.failure(
                        'Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>', '&gt;') + '断言:' + check)
                    return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return
        # 全局变量
        try:
            self.gd['uid'] = res.json()['data']['uid']
            self.gd['sk'] = res.json()['data']['sk']
        except:
            self.gd['uid'] = ''
            self.gd['sk'] = ''

    def WWWLogin(self):
        j_username = self.gd.get('www_username')
        j_password = '123456'
        params = {"j_username": j_username, "j_password": j_password, "_spring_security_remember_me": "off"}
        data = None
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        with self.client.post('http://w1.highso.com.cn/doLogin.do', params=params, headers=headers, data=data,
                              name='WWW主站登录', catch_response=True) as res:
            # 断言
            if res.status_code == 200:
                resp = res.text
                try:
                    resdata = tryJson(resp)
                except:
                    resdata = resp
                check = "{'success': True}"
                try:
                    pfassert(resdata=resdata, assertRule='contains', check=check)
                    res.success()
                except Exception as e:
                    res.failure(
                        'Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>', '&gt;') + '断言:' + check)
                    return
            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

    @task(10)
    def test1(self):

        url = 'http://a1.highso.com.cn/outline/v1/showOutlinePage.do'
        data = '["420429","128813"]'
        data = tryJson(data)
        query, headers = app.sig_post_json(data, {}, self.gd.get('uid'), self.gd.get('sk'))
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        with self.client.post(url=url, json=data, params=query, name='app-/outline/v1/showOutlinePage.do',
                              headers=headers, catch_response=True) as res:

            if res.status_code == 200:
                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

    @task(4)
    def test2(self):

        url = 'http://a1.highso.com.cn/newexam/v1/getExams.do'
        data = '{"module":101,"includeAnalysis":true,"includeExam":true,"examQuestions":[{"questionId":505303,"questionRecordDetailId":2677541919902748672,"materialId":53859},{"questionId":505305,"questionRecordDetailId":2677599122273685504,"materialId":53861},{"questionRecordDetailId":2677599122311434240,"questionId":305367},{"questionRecordDetailId":2677599122328211456,"questionId":305371},{"questionRecordDetailId":2677599122424680448,"questionId":305373}],"includeFavorite":true,"includeOutline":true,"includeQa":true}'
        data = tryJson(data)
        query, headers = app.sig_post_json(data, {}, self.gd.get('uid'), self.gd.get('sk'))
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        with self.client.post(url=url, params=query, json=data, name='app-/newexam/v1/getExams.do', headers=headers,
                              catch_response=True) as res:

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

        # 全局变量

    @task(3)
    def test3(self):

        url = 'http://a1.highso.com.cn/goods/v2/getModuleDetail.do'
        query = {'goodsCatalogId': 1920673, 'goodsId': 75351, 'moduleId': 205581}
        params = app.sig_dict(query, self.gd.get('uid'), self.gd.get('sk'))
        with self.client.get(url=url, params=params, name='app-/goods/v2/getModuleDetail.do', headers={},
                             catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

        # 全局变量

    @task(2)
    def test4(self):

        url = 'http://a1.highso.com.cn/survey/v1/getNpsInfo.do'
        query = {}
        params = app.sig_dict(query, self.gd.get('uid'), self.gd.get('sk'))
        with self.client.get(url=url, params=params, name='app-/survey/v1/getNpsInfo.do', headers={},
                             catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

        # 全局变量

    @task(2)
    def test5(self):

        url = 'http://a1.highso.com.cn/exam/v1/getExamStatistics.do'
        query = {'categoryId': 9, 'subjectId': 1}
        params = app.sig_dict(query, self.gd.get('uid'), self.gd.get('sk'))
        with self.client.get(url=url, params=params, name=' app-/exam/v1/getExamStatistics.do', headers={},
                             catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

    #
    # 全局变量

    @task(1)
    def test6(self):

        url = 'http://w1.highso.com.cn/study/app/live/v1/list?categoryId=9&startTime=1585411200000&endTime=1588348800000'
        url = my_replace(g_data=self.gd, strs=url)
        with self.client.get(url=url, name=' web-/study/app/live/v1/list', headers={}, catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

        # 全局变量

    @task(1)
    def test7(self):

        url = 'http://w1.highso.com.cn/study/app/plan/v1/plan?categoryId=9'
        url = my_replace(g_data=self.gd, strs=url)

        with self.client.get(url=url, name='web-/study/app/plan/v1/plan', headers={}, catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '"{\\"m\\": \\"ok\\"}"', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

    #
    #     #全局变量

    @task(2)
    def test8(self):

        url = 'http://w1.highso.com.cn/study/pc/goodsmodule/findbyid?goodsModuleId=8533'
        url = my_replace(g_data=self.gd, strs=url)

        with self.client.get(url=url, name='web-/study/pc/goodsmodule/findbyid', headers={},
                             catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '{"code":200}', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

        # 全局变量

    @task(2)
    def test9(self):

        url = 'http://w1.highso.com.cn/study/pc/customerServices/isCanZhuanfu?categoryId=9'
        with self.client.get(url=url, name='web-/study/pc/customerServices/isCanZhuanfu', headers={},
                             catch_response=True) as res:
            # 断言

            if res.status_code == 200:

                resp = res.text
                assertList = [{'assertName': 'contains', 'assertContent': '{"code":200}', 'assertionItem': ''}]
                for avalues in assertList:
                    if avalues.get('assertName'):
                        assertContent = avalues.get('assertContent')
                        try:
                            assertContent = tryJson(assertContent)
                        except:
                            pass
                        check = assertContent

                        if avalues.get('assertName') == '正则':
                            try:
                                pfassert_string_re(resdata=resp, regulars=avalues.get('assertionItem'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return
                        else:
                            try:
                                # 识别断言项，算出目标数据
                                resdata = pfassert_level(resp, avalues.get('assertionItem'))
                                pfassert(resdata=resdata, assertRule=avalues.get('assertName'), check=check)
                            except Exception as e:
                                res.failure('Failed!断言失败' + '接口返回:' + resp.replace('<', '&lt;').replace('>',
                                                                                                        '&gt;') + '断言:' + str(
                                    check))
                                return

            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    queueData = queue.Queue()
    v = [{'app_username': '18781001008', 'www_username': '18798011037'},
         {'app_username': '13890909988', 'www_username': '13137114977'},
         {'app_username': '18044445555', 'www_username': '13887302571'},
         {'app_username': '15777778888', 'www_username': '18007227768'},
         {'app_username': '16888888888', 'www_username': '13850808145'},
         {'app_username': '17723444423', 'www_username': '13005030040'},
         {'app_username': '17723444422', 'www_username': '13636281899'},
         {'app_username': '17723444421', 'www_username': '13594386276'},
         {'app_username': '17723444420', 'www_username': '15729891192'},
         {'app_username': '17318888888', 'www_username': '18510693115'},
         {'app_username': '18550298027', 'www_username': '18854906633'},
         {'app_username': '15828000039', 'www_username': '13055773261'},
         {'app_username': '15828000038', 'www_username': '15838055528'},
         {'app_username': '15828000037', 'www_username': '15773434119'},
         {'app_username': '15828000036', 'www_username': '18761485238'},
         {'app_username': '15828000035', 'www_username': '13295175072'},
         {'app_username': '15881012345', 'www_username': '13679486696'},
         {'app_username': '15828000034', 'www_username': '18713403427'},
         {'app_username': '13880448888', 'www_username': '18281703130'},
         {'app_username': '13880449999', 'www_username': '18523267507'},
         {'app_username': '17800000067', 'www_username': '13084442581'},
         {'app_username': '17800000066', 'www_username': '15515433480'},
         {'app_username': '18781001003', 'www_username': '15930978960'},
         {'app_username': '18781001002', 'www_username': '15802554064'},
         {'app_username': '18781001001', 'www_username': '13859420243'},
         {'app_username': '18781001000', 'www_username': '13170101808'},
         {'app_username': '18780003233', 'www_username': '15009978325'},
         {'app_username': '18780003236', 'www_username': '13754581681'},
         {'app_username': '16662777003', 'www_username': '15846568680'},
         {'app_username': '16662777004', 'www_username': '18523356000'},
         {'app_username': '19198238053', 'www_username': '17363806512'},
         {'app_username': '18780006008', 'www_username': '13855226652'},
         {'app_username': '18780006007', 'www_username': '15348192239'},
         {'app_username': '18780006006', 'www_username': '15823290162'},
         {'app_username': '18780006005', 'www_username': '13902064801'},
         {'app_username': '15632382010', 'www_username': '18201822105'},
         {'app_username': '18300019705', 'www_username': '18120881669'},
         {'app_username': '15736833901', 'www_username': '13703147648'},
         {'app_username': '19934572187', 'www_username': '18873004018'},
         {'app_username': '17723444437', 'www_username': '13989833739'},
         {'app_username': '17723444436', 'www_username': '18569826146'},
         {'app_username': '17555550300', 'www_username': '15029206403'},
         {'app_username': '18428385839', 'www_username': '18600085705'},
         {'app_username': '17723444435', 'www_username': '13607548081'},
         {'app_username': '17368473724', 'www_username': '13825047174'},
         {'app_username': '15890909900', 'www_username': '18313159793'},
         {'app_username': '17723444434', 'www_username': '13439606349'},
         {'app_username': '17723444433', 'www_username': '18616352430'},
         {'app_username': '18788883333', 'www_username': '17756970829'},
         {'app_username': '18780005556', 'www_username': '13779028602'},
         {'app_username': '17723444432', 'www_username': '13484814238'},
         {'app_username': '17723444431', 'www_username': '13653971107'},
         {'app_username': '17723444430', 'www_username': '18733529907'},
         {'app_username': '13990909900', 'www_username': '13724102245'},
         {'app_username': '18111261128', 'www_username': '13375871325'},
         {'app_username': '15828000032', 'www_username': '15088641877'},
         {'app_username': '18513449912', 'www_username': '13616339316'},
         {'app_username': '18212340101', 'www_username': '13738252708'},
         {'app_username': '18983318371', 'www_username': '15974190429'},
         {'app_username': '18312341006', 'www_username': '15883707755'},
         {'app_username': '18312341005', 'www_username': '15972066847'},
         {'app_username': '18312341004', 'www_username': '13558617651'},
         {'app_username': '18312341003', 'www_username': '13855252880'},
         {'app_username': '18312341002', 'www_username': '15546336313'},
         {'app_username': '18312341001', 'www_username': '13698752642'},
         {'app_username': '18550298731', 'www_username': '13952397943'},
         {'app_username': '15889998888', 'www_username': '13581349988'},
         {'app_username': '18512341112', 'www_username': '18853905566'},
         {'app_username': '18701542234', 'www_username': '13970157307'},
         {'app_username': '18883991123', 'www_username': '13831010987'},
         {'app_username': '19934309961', 'www_username': '15166727202'},
         {'app_username': '18512340112', 'www_username': '15233230773'},
         {'app_username': '13730683222', 'www_username': '18393534992'},
         {'app_username': '13552802528', 'www_username': '15008205693'},
         {'app_username': '18215646473', 'www_username': '15911809705'},
         {'app_username': '18911112229', 'www_username': '15836769596'},
         {'app_username': '18881486058', 'www_username': '18573116008'},
         {'app_username': '18881486059', 'www_username': '15776745021'},
         {'app_username': '18911112227', 'www_username': '18205683916'},
         {'app_username': '18911112225', 'www_username': '15803444928'},
         {'app_username': '18911112223', 'www_username': '13307779856'},
         {'app_username': '18200020001', 'www_username': '18507076999'},
         {'app_username': '13392985533', 'www_username': '15195130451'},
         {'app_username': '17141885862', 'www_username': '15087334286'},
         {'app_username': '19822001843', 'www_username': '13603970687'},
         {'app_username': '14562509272', 'www_username': '18611572750'},
         {'app_username': '15932630568', 'www_username': '15981884118'},
         {'app_username': '17316848035', 'www_username': '18726676888'},
         {'app_username': '18200331113', 'www_username': '13337468010'},
         {'app_username': '18200331112', 'www_username': '13709476304'},
         {'app_username': '18200331110', 'www_username': '18095686832'},
         {'app_username': '18033344455', 'www_username': '13161172391'},
         {'app_username': '13628255798', 'www_username': '15220612128'},
         {'app_username': '18512340133', 'www_username': '13631641994'},
         {'app_username': '13628255749', 'www_username': '13941498626'},
         {'app_username': '17720000001', 'www_username': '15665843061'},
         {'app_username': '13989898790', 'www_username': '15185024425'},
         {'app_username': '18780000099', 'www_username': '15038337349'},
         {'app_username': '13989894546', 'www_username': '13536837616'},
         {'app_username': '13989867655', 'www_username': '13514762892'},
         {'app_username': '18989898889', 'www_username': '13464612322'},
         {'app_username': '13989897878', 'www_username': '18033380972'},
         {'app_username': '18311113365', 'www_username': '18989510086'},
         {'app_username': '18055533321', 'www_username': '18041091267'},
         {'app_username': '18055533322', 'www_username': '13225013160'},
         {'app_username': '18884252590', 'www_username': '18270838461'},
         {'app_username': '18884252519', 'www_username': '13084120582'},
         {'app_username': '18884252515', 'www_username': '15046271603'},
         {'app_username': '18884252514', 'www_username': '13913295240'},
         {'app_username': '18884252513', 'www_username': '13249180204'},
         {'app_username': '18787879985', 'www_username': '18579132448'},
         {'app_username': '18885860011', 'www_username': '18653227817'},
         {'app_username': '18885860010', 'www_username': '13071218835'},
         {'app_username': '18885860009', 'www_username': '18369797363'},
         {'app_username': '15810486000', 'www_username': '15199656237'},
         {'app_username': '17555550201', 'www_username': '15193470535'},
         {'app_username': '15810480000', 'www_username': '15378406763'},
         {'app_username': '15810480001', 'www_username': '15955708375'},
         {'app_username': '13736999499', 'www_username': '13754580681'},
         {'app_username': '18885851117', 'www_username': '18163802330'},
         {'app_username': '18885851001', 'www_username': '15201521263'},
         {'app_username': '18885851116', 'www_username': '15156982563'},
         {'app_username': '18600260642', 'www_username': '15201578965'},
         {'app_username': '13377772244', 'www_username': '15011532011'},
         {'app_username': '13500333331', 'www_username': '13311520165'},
         {'app_username': '13500222221', 'www_username': '13988794506'},
         {'app_username': '18885851114', 'www_username': '15127939983'},
         {'app_username': '15828000031', 'www_username': '13764701832'},
         {'app_username': '13800888881', 'www_username': '15955870863'},
         {'app_username': '13800777771', 'www_username': '15135970826'},
         {'app_username': '13122222225', 'www_username': '18797338368'},
         {'app_username': '13800666661', 'www_username': '15753759677'},
         {'app_username': '13800555551', 'www_username': '13504298589'},
         {'app_username': '13800444441', 'www_username': '13728764728'},
         {'app_username': '13800333331', 'www_username': '13554081112'},
         {'app_username': '15828000030', 'www_username': '15354408897'},
         {'app_username': '13800222221', 'www_username': '18612275938'},
         {'app_username': '18291924742', 'www_username': '15870179722'},
         {'app_username': '18550298779', 'www_username': '17605032873'},
         {'app_username': '13754458309', 'www_username': '13215822253'},
         {'app_username': '18030339596', 'www_username': '15977647219'},
         {'app_username': '17373660553', 'www_username': '18353913233'},
         {'app_username': '15836682964', 'www_username': '15929292470'},
         {'app_username': '18584855016', 'www_username': '18740452755'},
         {'app_username': '18550298782', 'www_username': '17856125789'},
         {'app_username': '18811221160', 'www_username': '18817443729'},
         {'app_username': '17723444499', 'www_username': '15008205692'},
         {'app_username': '18818181888', 'www_username': '15245954600'},
         {'app_username': '18200020002', 'www_username': '18875716116'},
         {'app_username': '17318689978', 'www_username': '15119580819'},
         {'app_username': '17318689988', 'www_username': '15231033141'},
         {'app_username': '17818689978', 'www_username': '13926045562'},
         {'app_username': '17800004322', 'www_username': '13948201293'},
         {'app_username': '17800004321', 'www_username': '13136105769'},
         {'app_username': '17886668686', 'www_username': '15065231560'},
         {'app_username': '17555550173', 'www_username': '15000001119'},
         {'app_username': '17555550172', 'www_username': '15120133502'},
         {'app_username': '17555550171', 'www_username': '13509846791'},
         {'app_username': '18510163055', 'www_username': '13679446898'},
         {'app_username': '17844678913', 'www_username': '13224383275'},
         {'app_username': '13987766770', 'www_username': '13869224422'},
         {'app_username': '18550298805', 'www_username': '18295371721'},
         {'app_username': '18700070007', 'www_username': '13514233458'},
         {'app_username': '17566524309', 'www_username': '18857713600'},
         {'app_username': '13812573875', 'www_username': '18355326226'},
         {'app_username': '17555550170', 'www_username': '18389793969'},
         {'app_username': '17555550169', 'www_username': '13963507886'},
         {'app_username': '17555550168', 'www_username': '15812172472'},
         {'app_username': '17555550166', 'www_username': '15838662558'},
         {'app_username': '17555550165', 'www_username': '15801027545'},
         {'app_username': '18380475716', 'www_username': '13931275135'},
         {'app_username': '17689217032', 'www_username': '15142800582'},
         {'app_username': '13478931043', 'www_username': '13608526022'},
         {'app_username': '17380330132', 'www_username': '18093583371'},
         {'app_username': '18312340032', 'www_username': '15245786468'},
         {'app_username': '13608228110', 'www_username': '18585343412'},
         {'app_username': '18312340028', 'www_username': '15839730025'},
         {'app_username': '13086278196', 'www_username': '18730813518'},
         {'app_username': '18380475707', 'www_username': '13796288680'},
         {'app_username': '19145775699', 'www_username': '17695525348'},
         {'app_username': '14738326321', 'www_username': '18255415572'},
         {'app_username': '18131779217', 'www_username': '18953427519'},
         {'app_username': '15812164901', 'www_username': '18445534955'},
         {'app_username': '18028722096', 'www_username': '13158903600'},
         {'app_username': '17652248180', 'www_username': '13468586399'},
         {'app_username': '18890584439', 'www_username': '13879502888'},
         {'app_username': '15734851472', 'www_username': '13637777106'},
         {'app_username': '13546910794', 'www_username': '13583738652'},
         {'app_username': '13840390702', 'www_username': '17862913683'},
         {'app_username': '15157594823', 'www_username': '13752938957'},
         {'app_username': '13093732655', 'www_username': '17631122590'},
         {'app_username': '19148214438', 'www_username': '13987916323'},
         {'app_username': '16689541064', 'www_username': '18560053570'},
         {'app_username': '13549354850', 'www_username': '15848094584'},
         {'app_username': '15152668999', 'www_username': '13143656797'},
         {'app_username': '14770558854', 'www_username': '15809799296'},
         {'app_username': '18570197010', 'www_username': '18531100896'},
         {'app_username': '14965926635', 'www_username': '17519461955'},
         {'app_username': '17115090764', 'www_username': '13989891288'},
         {'app_username': '19884503769', 'www_username': '13999307633'},
         {'app_username': '13719090593', 'www_username': '13989415637'},
         {'app_username': '19135299160', 'www_username': '13948429884'},
         {'app_username': '13857132975', 'www_username': '18729253502'},
         {'app_username': '17548904065', 'www_username': '13863890659'},
         {'app_username': '13493799200', 'www_username': '15041734743'},
         {'app_username': '17760304803', 'www_username': '13614393776'},
         {'app_username': '17765636405', 'www_username': '17310541290'},
         {'app_username': '15674312127', 'www_username': '18515667465'},
         {'app_username': '15738844523', 'www_username': '15398020080'},
         {'app_username': '17523945761', 'www_username': '18972208365'},
         {'app_username': '13378602507', 'www_username': '13927283922'},
         {'app_username': '13796946003', 'www_username': '18686447200'},
         {'app_username': '18868243679', 'www_username': '13569796227'},
         {'app_username': '16662895745', 'www_username': '15670026196'},
         {'app_username': '18921513643', 'www_username': '18229420181'},
         {'app_username': '14934578735', 'www_username': '15110312828'},
         {'app_username': '15510777919', 'www_username': '13895114597'},
         {'app_username': '14754784340', 'www_username': '15012985601'},
         {'app_username': '15650796576', 'www_username': '17716629466'},
         {'app_username': '13290135197', 'www_username': '13588503996'},
         {'app_username': '17216086110', 'www_username': '18981573587'},
         {'app_username': '18073315110', 'www_username': '15190183081'},
         {'app_username': '13473929324', 'www_username': '18024903783'},
         {'app_username': '17314756902', 'www_username': '13111213982'},
         {'app_username': '16599210232', 'www_username': '15922678951'},
         {'app_username': '18385672724', 'www_username': '15858701870'},
         {'app_username': '18550062462', 'www_username': '13611140068'},
         {'app_username': '15041539887', 'www_username': '15373137151'},
         {'app_username': '13263296601', 'www_username': '18149066281'},
         {'app_username': '15288469903', 'www_username': '15896589679'},
         {'app_username': '15682814083', 'www_username': '13511645547'},
         {'app_username': '15057113156', 'www_username': '15912559656'},
         {'app_username': '19881825377', 'www_username': '15881446680'},
         {'app_username': '16627435027', 'www_username': '13626355794'},
         {'app_username': '14692391392', 'www_username': '15851745616'},
         {'app_username': '15212964768', 'www_username': '13341062371'},
         {'app_username': '18038698064', 'www_username': '13628700919'},
         {'app_username': '19832689813', 'www_username': '13270358290'},
         {'app_username': '15573856763', 'www_username': '13633197953'},
         {'app_username': '19183735412', 'www_username': '13655004283'},
         {'app_username': '18898308114', 'www_username': '15987243387'},
         {'app_username': '19825465029', 'www_username': '18847029519'},
         {'app_username': '14613852999', 'www_username': '18104845090'},
         {'app_username': '17355759275', 'www_username': '18326986129'},
         {'app_username': '15738432240', 'www_username': '15884865745'},
         {'app_username': '18390494405', 'www_username': '18302446512'},
         {'app_username': '17384500688', 'www_username': '13880889355'},
         {'app_username': '13160887453', 'www_username': '13405172937'},
         {'app_username': '18718493410', 'www_username': '17777416393'},
         {'app_username': '13397683193', 'www_username': '13514928225'},
         {'app_username': '17542964605', 'www_username': '13807233135'},
         {'app_username': '13465247416', 'www_username': '15992404373'},
         {'app_username': '15587709534', 'www_username': '15011652380'},
         {'app_username': '15585125162', 'www_username': '18253877758'},
         {'app_username': '14969883124', 'www_username': '18428343559'},
         {'app_username': '18881011225', 'www_username': '13335630276'},
         {'app_username': '15745505595', 'www_username': '18626345864'},
         {'app_username': '18638952626', 'www_username': '15389694567'},
         {'app_username': '19884058038', 'www_username': '15946030494'},
         {'app_username': '17538539665', 'www_username': '18561062550'},
         {'app_username': '19133680690', 'www_username': '13315013316'},
         {'app_username': '18013491569', 'www_username': '15849483451'},
         {'app_username': '15369864505', 'www_username': '18404254260'},
         {'app_username': '18236659673', 'www_username': '13600827476'},
         {'app_username': '17681764617', 'www_username': '15379789611'},
         {'app_username': '17751449037', 'www_username': '18608082804'},
         {'app_username': '15199937550', 'www_username': '13403101936'},
         {'app_username': '17743578742', 'www_username': '13720043025'},
         {'app_username': '18777987374', 'www_username': '18672110466'},
         {'app_username': '14992548774', 'www_username': '13785212583'},
         {'app_username': '13349896878', 'www_username': '13695905193'},
         {'app_username': '18139089633', 'www_username': '18883782939'},
         {'app_username': '18829556703', 'www_username': '13427015702'},
         {'app_username': '13593860876', 'www_username': '15094630521'},
         {'app_username': '13233364095', 'www_username': '13947103356'},
         {'app_username': '13387021663', 'www_username': '13642585666'},
         {'app_username': '16584189768', 'www_username': '17688152556'},
         {'app_username': '18832010736', 'www_username': '15250422245'},
         {'app_username': '13436302401', 'www_username': '18175613938'},
         {'app_username': '13292800117', 'www_username': '15135164765'},
         {'app_username': '14733225509', 'www_username': '13868011144'},
         {'app_username': '13925860941', 'www_username': '13250804960'},
         {'app_username': '15095682164', 'www_username': '13546297627'},
         {'app_username': '18747486342', 'www_username': '18211963920'},
         {'app_username': '19917974474', 'www_username': '15230072521'},
         {'app_username': '17644022951', 'www_username': '18731530015'},
         {'app_username': '16697446557', 'www_username': '13984128387'},
         {'app_username': '18180342670', 'www_username': '17801092731'},
         {'app_username': '18734687577', 'www_username': '18809838501'},
         {'app_username': '18036865181', 'www_username': '15206292987'},
         {'app_username': '18181337724', 'www_username': '13569898188'},
         {'app_username': '18248035207', 'www_username': '13947645010'},
         {'app_username': '18039710164', 'www_username': '13152993860'},
         {'app_username': '18256993299', 'www_username': '14794416986'},
         {'app_username': '15895732871', 'www_username': '18749156297'},
         {'app_username': '13081886332', 'www_username': '13957958419'},
         {'app_username': '13787142006', 'www_username': '15280072468'},
         {'app_username': '14592133351', 'www_username': '18772515857'},
         {'app_username': '18037400138', 'www_username': '18329368123'},
         {'app_username': '13243257187', 'www_username': '18863072288'},
         {'app_username': '18860982145', 'www_username': '13908491987'},
         {'app_username': '17633636872', 'www_username': '18163682520'},
         {'app_username': '18285581852', 'www_username': '15330261975'},
         {'app_username': '15941030623', 'www_username': '15723296316'},
         {'app_username': '18244808352', 'www_username': '15543958901'},
         {'app_username': '18696378227', 'www_username': '18658265559'},
         {'app_username': '15239488433', 'www_username': '18707789906'},
         {'app_username': '15922562630', 'www_username': '15810348100'},
         {'app_username': '13456287581', 'www_username': '15310697017'},
         {'app_username': '19159187241', 'www_username': '15835574767'},
         {'app_username': '16695586660', 'www_username': '18889140179'},
         {'app_username': '17886701278', 'www_username': '13113883226'},
         {'app_username': '18144012417', 'www_username': '15247652604'},
         {'app_username': '18374147576', 'www_username': '13154778542'},
         {'app_username': '15332797832', 'www_username': '13850733766'},
         {'app_username': '18911272159', 'www_username': '15096625969'},
         {'app_username': '13975117009', 'www_username': '18291099248'},
         {'app_username': '19841467263', 'www_username': '15037965339'},
         {'app_username': '18636737734', 'www_username': '15262267891'},
         {'app_username': '15352500209', 'www_username': '13015787589'},
         {'app_username': '13534877442', 'www_username': '13828291204'},
         {'app_username': '15256633572', 'www_username': '13467099223'},
         {'app_username': '17521001456', 'www_username': '13890499731'},
         {'app_username': '13722305573', 'www_username': '13885093331'},
         {'app_username': '18384028141', 'www_username': '13101319597'},
         {'app_username': '19853879284', 'www_username': '18749302931'},
         {'app_username': '14796716923', 'www_username': '15134674916'},
         {'app_username': '17152893510', 'www_username': '18193332003'},
         {'app_username': '13827620749', 'www_username': '13608276659'},
         {'app_username': '14779041863', 'www_username': '13669178630'},
         {'app_username': '17515642529', 'www_username': '18978172932'},
         {'app_username': '13612215401', 'www_username': '13529252404'},
         {'app_username': '15021877229', 'www_username': '13383561658'},
         {'app_username': '19110606228', 'www_username': '18636595503'},
         {'app_username': '15526228068', 'www_username': '13330695446'},
         {'app_username': '16532568830', 'www_username': '18697998220'},
         {'app_username': '15047565100', 'www_username': '15058195417'},
         {'app_username': '16527071548', 'www_username': '18671911001'},
         {'app_username': '17741757538', 'www_username': '13386404001'},
         {'app_username': '15213922735', 'www_username': '13878623218'},
         {'app_username': '14740438097', 'www_username': '13595741905'},
         {'app_username': '18138937442', 'www_username': '17376391975'},
         {'app_username': '15785045994', 'www_username': '15972395766'},
         {'app_username': '16571737409', 'www_username': '13795246880'},
         {'app_username': '13098803628', 'www_username': '13410893676'},
         {'app_username': '16550800545', 'www_username': '13075076853'},
         {'app_username': '13861209202', 'www_username': '13509983297'},
         {'app_username': '17332502473', 'www_username': '18662287436'},
         {'app_username': '13484242164', 'www_username': '18227922261'},
         {'app_username': '14712234125', 'www_username': '13835186458'},
         {'app_username': '15194276659', 'www_username': '18799633086'},
         {'app_username': '18947992085', 'www_username': '15874639069'},
         {'app_username': '17134879750', 'www_username': '18870907595'},
         {'app_username': '19967564131', 'www_username': '13639705752'},
         {'app_username': '17373248803', 'www_username': '18733375726'},
         {'app_username': '15169073745', 'www_username': '15850726973'},
         {'app_username': '18920507862', 'www_username': '13849264776'},
         {'app_username': '14619410561', 'www_username': '13011078524'},
         {'app_username': '13053254862', 'www_username': '18955693329'},
         {'app_username': '13413036168', 'www_username': '18762802337'},
         {'app_username': '15145174884', 'www_username': '15881586377'},
         {'app_username': '14939946025', 'www_username': '13913591384'},
         {'app_username': '18450223616', 'www_username': '18560684529'},
         {'app_username': '18471745313', 'www_username': '13552557132'},
         {'app_username': '18961865854', 'www_username': '18928894775'},
         {'app_username': '17815483358', 'www_username': '13279079033'},
         {'app_username': '15323369825', 'www_username': '15282841273'},
         {'app_username': '13923434713', 'www_username': '13550499899'},
         {'app_username': '18812828995', 'www_username': '15929176121'},
         {'app_username': '17397561784', 'www_username': '13399118121'},
         {'app_username': '18041530359', 'www_username': '18891102235'},
         {'app_username': '15120304980', 'www_username': '13570051235'},
         {'app_username': '13814690248', 'www_username': '15900263420'},
         {'app_username': '17327072721', 'www_username': '18631320182'},
         {'app_username': '16642980673', 'www_username': '17736291164'},
         {'app_username': '15284237946', 'www_username': '18201181776'},
         {'app_username': '13459031386', 'www_username': '18328378113'},
         {'app_username': '14979691457', 'www_username': '18368812562'},
         {'app_username': '17793142076', 'www_username': '13545909598'},
         {'app_username': '19877259638', 'www_username': '18709110181'},
         {'app_username': '17267091860', 'www_username': '18036392776'},
         {'app_username': '14941169139', 'www_username': '18907767566'},
         {'app_username': '17738208376', 'www_username': '13943187055'},
         {'app_username': '13448624435', 'www_username': '18388476295'},
         {'app_username': '13483919479', 'www_username': '13770172777'},
         {'app_username': '16643019107', 'www_username': '13976533182'},
         {'app_username': '13740738945', 'www_username': '15923318959'},
         {'app_username': '17157655647', 'www_username': '13510441203'},
         {'app_username': '15135217805', 'www_username': '13837120200'},
         {'app_username': '15337109233', 'www_username': '18152176232'},
         {'app_username': '15367383203', 'www_username': '13920945822'},
         {'app_username': '17749090231', 'www_username': '15183892702'},
         {'app_username': '16565138883', 'www_username': '15085086165'},
         {'app_username': '13576179636', 'www_username': '13804721384'},
         {'app_username': '13364273793', 'www_username': '18811345596'},
         {'app_username': '17735300408', 'www_username': '18854759729'},
         {'app_username': '19915370123', 'www_username': '18187459171'},
         {'app_username': '18292228522', 'www_username': '15249089899'},
         {'app_username': '16618331611', 'www_username': '13250628012'},
         {'app_username': '14529658253', 'www_username': '15730448751'},
         {'app_username': '15210507273', 'www_username': '13511986440'},
         {'app_username': '13664250677', 'www_username': '13804794961'},
         {'app_username': '16612761560', 'www_username': '15962734466'},
         {'app_username': '18082494532', 'www_username': '15828326478'},
         {'app_username': '18280177000', 'www_username': '13946011413'},
         {'app_username': '17142236550', 'www_username': '13599418081'},
         {'app_username': '18239791893', 'www_username': '13513229119'},
         {'app_username': '14941073247', 'www_username': '18960264115'},
         {'app_username': '19875232798', 'www_username': '11112350807'},
         {'app_username': '17357066417', 'www_username': '15137936714'},
         {'app_username': '17821858018', 'www_username': '13895069900'},
         {'app_username': '14974999799', 'www_username': '13882302380'},
         {'app_username': '15892481449', 'www_username': '15652962319'},
         {'app_username': '16696740873', 'www_username': '18601315373'},
         {'app_username': '17688485926', 'www_username': '18733159859'},
         {'app_username': '18368012932', 'www_username': '13209166126'},
         {'app_username': '17266775675', 'www_username': '18786710216'},
         {'app_username': '15158013989', 'www_username': '13322556699'},
         {'app_username': '17658566485', 'www_username': '13883603588'},
         {'app_username': '17170616372', 'www_username': '15883006360'},
         {'app_username': '17794170569', 'www_username': '18745976887'},
         {'app_username': '15249854303', 'www_username': '13992490359'},
         {'app_username': '15190770096', 'www_username': '17863907526'},
         {'app_username': '18873652662', 'www_username': '15563699995'},
         {'app_username': '18825920884', 'www_username': '15913769718'},
         {'app_username': '18026962499', 'www_username': '13354072297'},
         {'app_username': '18957363999', 'www_username': '18729180260'},
         {'app_username': '15135408236', 'www_username': '13476473789'},
         {'app_username': '17673947312', 'www_username': '13962364652'},
         {'app_username': '18186928136', 'www_username': '18246824807'},
         {'app_username': '18058599958', 'www_username': '15695315170'},
         {'app_username': '13124125133', 'www_username': '15072876058'},
         {'app_username': '18772548330', 'www_username': '13643479671'},
         {'app_username': '18813390715', 'www_username': '13810859837'},
         {'app_username': '18100010002', 'www_username': '13703695083'},
         {'app_username': '15610244533', 'www_username': '13606555728'},
         {'app_username': '13465477535', 'www_username': '13596206882'},
         {'app_username': '13112928474', 'www_username': '15202205820'},
         {'app_username': '18158624248', 'www_username': '15031050561'},
         {'app_username': '15192071626', 'www_username': '13804180368'},
         {'app_username': '16648650389', 'www_username': '13558983817'},
         {'app_username': '18100010001', 'www_username': '18662676911'},
         {'app_username': '15854578322', 'www_username': '18706769841'},
         {'app_username': '14926595540', 'www_username': '13386315682'},
         {'app_username': '14993231900', 'www_username': '13876893210'},
         {'app_username': '18687515487', 'www_username': '15829566657'},
         {'app_username': '13348255840', 'www_username': '15082648856'},
         {'app_username': '17343181675', 'www_username': '15907093804'},
         {'app_username': '16624697162', 'www_username': '15696789666'},
         {'app_username': '13144554783', 'www_username': '15707602281'},
         {'app_username': '15182966384', 'www_username': '13674920996'},
         {'app_username': '15961525558', 'www_username': '13573196458'},
         {'app_username': '16665261477', 'www_username': '13879276616'},
         {'app_username': '15282512532', 'www_username': '13944181986'},
         {'app_username': '18373455855', 'www_username': '18635015543'},
         {'app_username': '17820027236', 'www_username': '18996966401'},
         {'app_username': '19824826325', 'www_username': '15106661739'},
         {'app_username': '14632850160', 'www_username': '15140061273'},
         {'app_username': '13482864062', 'www_username': '13281901333'},
         {'app_username': '17594385332', 'www_username': '15212408877'},
         {'app_username': '17191859991', 'www_username': '13364300282'},
         {'app_username': '15572653335', 'www_username': '18163088757'},
         {'app_username': '14550757996', 'www_username': '15029271100'},
         {'app_username': '15572409234', 'www_username': '13709017375'},
         {'app_username': '14716257919', 'www_username': '13959930812'},
         {'app_username': '17654457317', 'www_username': '13684041755'},
         {'app_username': '15835848450', 'www_username': '13198762345'},
         {'app_username': '17616325166', 'www_username': '18239466801'},
         {'app_username': '13199498369', 'www_username': '13722164055'},
         {'app_username': '15898987974', 'www_username': '15016724685'},
         {'app_username': '13635209199', 'www_username': '13562393908'},
         {'app_username': '13767862523', 'www_username': '13146177432'},
         {'app_username': '15047580678', 'www_username': '15528360371'},
         {'app_username': '13474854962', 'www_username': '15556528272'},
         {'app_username': '13059236575', 'www_username': '17752858197'},
         {'app_username': '17749841790', 'www_username': '13908351796'},
         {'app_username': '15841560208', 'www_username': '18613838139'},
         {'app_username': '14796775528', 'www_username': '15172820219'},
         {'app_username': '16557803326', 'www_username': '13682627647'},
         {'app_username': '15298804386', 'www_username': '13333064718'},
         {'app_username': '18578545777', 'www_username': '13842570208'},
         {'app_username': '18452809376', 'www_username': '13616151555'},
         {'app_username': '13911372687', 'www_username': '18518042420'},
         {'app_username': '13915499078', 'www_username': '13784573583'},
         {'app_username': '18113487836', 'www_username': '15678971447'},
         {'app_username': '16576924507', 'www_username': '15176858651'},
         {'app_username': '18055604841', 'www_username': '15198824864'},
         {'app_username': '17395107321', 'www_username': '15053276592'},
         {'app_username': '15756403058', 'www_username': '15378107877'},
         {'app_username': '17387310659', 'www_username': '13077707771'},
         {'app_username': '16665542801', 'www_username': '15299008922'},
         {'app_username': '13565169121', 'www_username': '18819481005'},
         {'app_username': '15019281523', 'www_username': '18774730090'},
         {'app_username': '17125071419', 'www_username': '15270071417'},
         {'app_username': '19937866776', 'www_username': '18690789050'},
         {'app_username': '13770754518', 'www_username': '15085924582'},
         {'app_username': '13415324121', 'www_username': '18625862737'},
         {'app_username': '18598150434', 'www_username': '15842230438'},
         {'app_username': '17655147133', 'www_username': '13419125081'},
         {'app_username': '15780396414', 'www_username': '15739521733'},
         {'app_username': '15295800824', 'www_username': '15825857496'},
         {'app_username': '15776278343', 'www_username': '18720903891'},
         {'app_username': '15121001471', 'www_username': '18952628109'},
         {'app_username': '15532694240', 'www_username': '13623692221'},
         {'app_username': '13122548290', 'www_username': '13503527019'},
         {'app_username': '16663890755', 'www_username': '13515757397'},
         {'app_username': '13360548443', 'www_username': '13822721603'},
         {'app_username': '13433170166', 'www_username': '15063497400'},
         {'app_username': '17525370747', 'www_username': '13549007521'},
         {'app_username': '13746512804', 'www_username': '13076130193'},
         {'app_username': '14745321799', 'www_username': '15884553713'},
         {'app_username': '15978044456', 'www_username': '15853770249'},
         {'app_username': '14592561648', 'www_username': '18133861245'},
         {'app_username': '14746258775', 'www_username': '15332715137'},
         {'app_username': '15142900846', 'www_username': '15671682690'},
         {'app_username': '17897123828', 'www_username': '18387119255'},
         {'app_username': '16538112284', 'www_username': '15853438566'},
         {'app_username': '17222220254', 'www_username': '18859154942'},
         {'app_username': '15594703338', 'www_username': '18702112313'},
         {'app_username': '15235956548', 'www_username': '18908348601'},
         {'app_username': '18249875049', 'www_username': '15804736366'},
         {'app_username': '14987037662', 'www_username': '18728018925'},
         {'app_username': '17276599342', 'www_username': '18834361358'},
         {'app_username': '17880114109', 'www_username': '13137124976'},
         {'app_username': '17558066179', 'www_username': '13880566951'},
         {'app_username': '15331762757', 'www_username': '15620988017'},
         {'app_username': '16632115198', 'www_username': '18245592876'},
         {'app_username': '13877211851', 'www_username': '18247301790'},
         {'app_username': '18249768409', 'www_username': '18804268753'},
         {'app_username': '13649703319', 'www_username': '18997190281'},
         {'app_username': '15326167494', 'www_username': '15062424800'},
         {'app_username': '15975035271', 'www_username': '13095553375'},
         {'app_username': '15048811447', 'www_username': '18627976027'},
         {'app_username': '13077882591', 'www_username': '13183831676'},
         {'app_username': '13551192495', 'www_username': '18408249275'},
         {'app_username': '18826658902', 'www_username': '18804003068'},
         {'app_username': '13433669894', 'www_username': '18191338810'},
         {'app_username': '13784344786', 'www_username': '15000571526'},
         {'app_username': '18554802924', 'www_username': '15965047641'},
         {'app_username': '17287483135', 'www_username': '13643665383'},
         {'app_username': '14666904534', 'www_username': '13668527500'},
         {'app_username': '18866892424', 'www_username': '15950231877'},
         {'app_username': '18936983928', 'www_username': '15833415596'},
         {'app_username': '14691817673', 'www_username': '18656695843'},
         {'app_username': '13188577882', 'www_username': '17718117825'},
         {'app_username': '16658312657', 'www_username': '15226197050'},
         {'app_username': '17368768148', 'www_username': '18504318592'},
         {'app_username': '13161863646', 'www_username': '13468268672'},
         {'app_username': '17719095783', 'www_username': '13558439959'},
         {'app_username': '16575140130', 'www_username': '13258665585'},
         {'app_username': '15513483913', 'www_username': '15885987024'},
         {'app_username': '18084079347', 'www_username': '13276453467'},
         {'app_username': '19947835884', 'www_username': '18567620540'},
         {'app_username': '13916974704', 'www_username': '13322212122'},
         {'app_username': '16680183375', 'www_username': '13795424003'},
         {'app_username': '15524189995', 'www_username': '15139846981'},
         {'app_username': '19825148229', 'www_username': '13991977081'},
         {'app_username': '13639228380', 'www_username': '15225875729'},
         {'app_username': '15977316105', 'www_username': '17710399880'},
         {'app_username': '17878099992', 'www_username': '18020910670'},
         {'app_username': '15664158570', 'www_username': '18647649339'},
         {'app_username': '15144388183', 'www_username': '15281778388'},
         {'app_username': '15750359487', 'www_username': '15025536063'},
         {'app_username': '13274145821', 'www_username': '13143701539'},
         {'app_username': '13654541901', 'www_username': '17770874657'},
         {'app_username': '15360198483', 'www_username': '18611718734'},
         {'app_username': '17275143364', 'www_username': '17603451132'},
         {'app_username': '18751241753', 'www_username': '18394158984'},
         {'app_username': '13459755937', 'www_username': '18119689828'},
         {'app_username': '17795826673', 'www_username': '15084992901'},
         {'app_username': '17380153239', 'www_username': '18627774572'},
         {'app_username': '13718258726', 'www_username': '18255121205'},
         {'app_username': '13929193009', 'www_username': '15939082160'},
         {'app_username': '19116487862', 'www_username': '13305409707'},
         {'app_username': '16671023160', 'www_username': '18785666451'},
         {'app_username': '15829725896', 'www_username': '18729020459'},
         {'app_username': '18799972728', 'www_username': '15757939743'},
         {'app_username': '13025271992', 'www_username': '13457684620'},
         {'app_username': '15776334968', 'www_username': '15815788897'},
         {'app_username': '15568887696', 'www_username': '18793141698'},
         {'app_username': '18392911056', 'www_username': '15148991196'},
         {'app_username': '18154638179', 'www_username': '13323810218'},
         {'app_username': '19183622130', 'www_username': '15869396852'},
         {'app_username': '15364190267', 'www_username': '15866717606'},
         {'app_username': '17827866982', 'www_username': '18223053815'},
         {'app_username': '17592529875', 'www_username': '13977417905'},
         {'app_username': '14556476489', 'www_username': '18807257218'},
         {'app_username': '18358377863', 'www_username': '15109989533'},
         {'app_username': '15510818841', 'www_username': '15823248797'},
         {'app_username': '15984495035', 'www_username': '15385367693'},
         {'app_username': '13137308609', 'www_username': '18980347380'},
         {'app_username': '15610561784', 'www_username': '15270941505'},
         {'app_username': '14595538003', 'www_username': '15563646001'},
         {'app_username': '14652614290', 'www_username': '18685489332'},
         {'app_username': '13796994380', 'www_username': '15195752971'},
         {'app_username': '13573270516', 'www_username': '18956623863'},
         {'app_username': '18854815125', 'www_username': '13005980835'},
         {'app_username': '13038125211', 'www_username': '15011480351'},
         {'app_username': '13331527699', 'www_username': '18230820613'},
         {'app_username': '15268655903', 'www_username': '13370350212'},
         {'app_username': '15277380949', 'www_username': '18682442715'},
         {'app_username': '18827774936', 'www_username': '18095236985'},
         {'app_username': '13735956261', 'www_username': '13879760606'},
         {'app_username': '14616641296', 'www_username': '15353512469'},
         {'app_username': '17198469362', 'www_username': '13877005045'},
         {'app_username': '17891373529', 'www_username': '18756805291'},
         {'app_username': '13241640936', 'www_username': '13847735928'},
         {'app_username': '15145983380', 'www_username': '13908760070'},
         {'app_username': '13240228744', 'www_username': '15507534913'},
         {'app_username': '16689691444', 'www_username': '13507659608'},
         {'app_username': '13133440722', 'www_username': '15270568901'},
         {'app_username': '13531197549', 'www_username': '13795012320'},
         {'app_username': '18671254321', 'www_username': '13033960790'},
         {'app_username': '16692771182', 'www_username': '13663757077'},
         {'app_username': '13233711079', 'www_username': '18647325518'},
         {'app_username': '19856692605', 'www_username': '13512648861'},
         {'app_username': '17772023467', 'www_username': '15620600123'},
         {'app_username': '13489034124', 'www_username': '18230956402'},
         {'app_username': '18877791888', 'www_username': '18866838085'},
         {'app_username': '17743145811', 'www_username': '13635026891'},
         {'app_username': '18841666895', 'www_username': '13287771265'},
         {'app_username': '19919558676', 'www_username': '17736519013'},
         {'app_username': '15889345640', 'www_username': '18166302320'},
         {'app_username': '19927811045', 'www_username': '15214237361'},
         {'app_username': '13130563164', 'www_username': '13820712256'},
         {'app_username': '18917049013', 'www_username': '13434169784'},
         {'app_username': '13410817526', 'www_username': '13598717981'},
         {'app_username': '18631363593', 'www_username': '13258832378'},
         {'app_username': '18716588836', 'www_username': '15823453883'},
         {'app_username': '17781260000', 'www_username': '13381018581'},
         {'app_username': '14630962109', 'www_username': '13947682769'},
         {'app_username': '18228881253', 'www_username': '18201412105'},
         {'app_username': '13130370361', 'www_username': '18143240114'},
         {'app_username': '16691888314', 'www_username': '18870801844'},
         {'app_username': '19198920860', 'www_username': '13623311607'},
         {'app_username': '15590755070', 'www_username': '13167892825'},
         {'app_username': '17226450276', 'www_username': '15810776563'},
         {'app_username': '18287415047', 'www_username': '18560887121'},
         {'app_username': '18417703638', 'www_username': '15587088469'},
         {'app_username': '13171216510', 'www_username': '18930179265'},
         {'app_username': '14973413588', 'www_username': '18577206208'},
         {'app_username': '15248504134', 'www_username': '13590263207'},
         {'app_username': '13776007161', 'www_username': '18642160339'},
         {'app_username': '18040415536', 'www_username': '15650569554'},
         {'app_username': '14544257570', 'www_username': '13573039092'},
         {'app_username': '13768095399', 'www_username': '15074842085'},
         {'app_username': '17237000436', 'www_username': '13279183095'},
         {'app_username': '15111211274', 'www_username': '13718828090'},
         {'app_username': '13989380496', 'www_username': '13558711946'},
         {'app_username': '13493473620', 'www_username': '15179169289'},
         {'app_username': '17616423521', 'www_username': '18699095151'},
         {'app_username': '16625416608', 'www_username': '15563041456'},
         {'app_username': '13673158712', 'www_username': '15269875896'},
         {'app_username': '17369562445', 'www_username': '18639815289'},
         {'app_username': '18312340027', 'www_username': '13897109271'},
         {'app_username': '14784880614', 'www_username': '13569457834'},
         {'app_username': '19174664552', 'www_username': '13768931728'},
         {'app_username': '13926151190', 'www_username': '18763625851'},
         {'app_username': '15193099900', 'www_username': '18252738453'},
         {'app_username': '13217416956', 'www_username': '13139600112'},
         {'app_username': '15567248597', 'www_username': '15871760727'},
         {'app_username': '13242243272', 'www_username': '15831361005'},
         {'app_username': '14933736909', 'www_username': '15511875559'},
         {'app_username': '13750331869', 'www_username': '13378749128'},
         {'app_username': '14596787516', 'www_username': '13837506290'},
         {'app_username': '17153655192', 'www_username': '15210122596'},
         {'app_username': '15342388778', 'www_username': '15596361528'},
         {'app_username': '18331827163', 'www_username': '13972771685'},
         {'app_username': '15138553069', 'www_username': '13353833215'},
         {'app_username': '16565519889', 'www_username': '13969507997'},
         {'app_username': '14765565112', 'www_username': '13667935383'},
         {'app_username': '17824719616', 'www_username': '15191025097'},
         {'app_username': '15966934958', 'www_username': '17611157170'},
         {'app_username': '13337079245', 'www_username': '18983481179'},
         {'app_username': '16560194011', 'www_username': '18439438134'},
         {'app_username': '16636568045', 'www_username': '15110575025'},
         {'app_username': '18580391423', 'www_username': '13982753112'},
         {'app_username': '17813912198', 'www_username': '15804702034'},
         {'app_username': '15950882063', 'www_username': '18251831101'},
         {'app_username': '13525899397', 'www_username': '13660943005'},
         {'app_username': '13347781740', 'www_username': '13721826143'},
         {'app_username': '17137933994', 'www_username': '15204128661'},
         {'app_username': '18243682914', 'www_username': '15938760345'},
         {'app_username': '19952301689', 'www_username': '13899910626'},
         {'app_username': '17123364046', 'www_username': '15885560699'},
         {'app_username': '14718904655', 'www_username': '13808068167'},
         {'app_username': '18946951192', 'www_username': '15927987445'},
         {'app_username': '18579078968', 'www_username': '13546374700'},
         {'app_username': '19863896278', 'www_username': '15734688798'},
         {'app_username': '17195887871', 'www_username': '13382660636'},
         {'app_username': '16524102827', 'www_username': '13643348015'},
         {'app_username': '13299473255', 'www_username': '13306300635'},
         {'app_username': '18852911917', 'www_username': '14787462703'},
         {'app_username': '13745142328', 'www_username': '15738030958'},
         {'app_username': '13823552875', 'www_username': '18631909667'},
         {'app_username': '15135864634', 'www_username': '15540610999'},
         {'app_username': '18937438522', 'www_username': '13777951708'},
         {'app_username': '13282472319', 'www_username': '18661883570'},
         {'app_username': '17389855756', 'www_username': '18003991708'},
         {'app_username': '18364106594', 'www_username': '18522362657'},
         {'app_username': '15229526626', 'www_username': '18725996099'},
         {'app_username': '17527794446', 'www_username': '17331343138'},
         {'app_username': '17724005944', 'www_username': '18213777868'},
         {'app_username': '17177321826', 'www_username': '13335198119'},
         {'app_username': '19139335393', 'www_username': '13368685260'},
         {'app_username': '13188113163', 'www_username': '13369875056'},
         {'app_username': '18164812971', 'www_username': '18039600475'},
         {'app_username': '17728099937', 'www_username': '18085862913'},
         {'app_username': '13838966981', 'www_username': '13928382767'},
         {'app_username': '13955148439', 'www_username': '13407184321'},
         {'app_username': '15915211028', 'www_username': '13519911009'},
         {'app_username': '17886812749', 'www_username': '18280228931'},
         {'app_username': '18914711188', 'www_username': '15712585306'},
         {'app_username': '18796614053', 'www_username': '13330000321'},
         {'app_username': '18280422677', 'www_username': '15878805303'},
         {'app_username': '18476723243', 'www_username': '15914229916'},
         {'app_username': '17631054866', 'www_username': '15983018206'},
         {'app_username': '17710108474', 'www_username': '18351294158'},
         {'app_username': '18970287033', 'www_username': '13230700634'},
         {'app_username': '15072703759', 'www_username': '13785560408'},
         {'app_username': '18986881691', 'www_username': '13508011608'},
         {'app_username': '17273403357', 'www_username': '15977805826'},
         {'app_username': '13028853774', 'www_username': '13732235602'},
         {'app_username': '13272751799', 'www_username': '17781914211'},
         {'app_username': '13886372002', 'www_username': '13791030682'},
         {'app_username': '18011213307', 'www_username': '18560197007'},
         {'app_username': '13443660263', 'www_username': '15270185139'},
         {'app_username': '15541176406', 'www_username': '18210091393'},
         {'app_username': '19937594453', 'www_username': '13656884918'},
         {'app_username': '17126314304', 'www_username': '13456884072'},
         {'app_username': '18774688732', 'www_username': '15181667048'},
         {'app_username': '15669531289', 'www_username': '15036156333'},
         {'app_username': '13193244257', 'www_username': '13680555171'},
         {'app_username': '16659779487', 'www_username': '15803194498'},
         {'app_username': '17552914837', 'www_username': '13480290031'},
         {'app_username': '19117587418', 'www_username': '17005557778'},
         {'app_username': '13918375448', 'www_username': '13577179920'},
         {'app_username': '13753833675', 'www_username': '15169668276'},
         {'app_username': '17290535386', 'www_username': '18856710061'},
         {'app_username': '17169781905', 'www_username': '15866112644'},
         {'app_username': '14946214330', 'www_username': '15362031496'},
         {'app_username': '13864570996', 'www_username': '13588701495'},
         {'app_username': '13060526572', 'www_username': '13964255761'},
         {'app_username': '15940565634', 'www_username': '15039417053'},
         {'app_username': '18380569079', 'www_username': '13676711503'},
         {'app_username': '14977348124', 'www_username': '18043192980'},
         {'app_username': '15067142412', 'www_username': '13728381030'},
         {'app_username': '14583281012', 'www_username': '15577396150'},
         {'app_username': '13273071780', 'www_username': '17712179900'},
         {'app_username': '18535096512', 'www_username': '13321151998'},
         {'app_username': '13137413454', 'www_username': '18816391018'},
         {'app_username': '17243598216', 'www_username': '13653497075'},
         {'app_username': '15332906575', 'www_username': '13287015027'},
         {'app_username': '16673468706', 'www_username': '15368085624'},
         {'app_username': '17688818220', 'www_username': '15562605457'},
         {'app_username': '19149080248', 'www_username': '17756482536'},
         {'app_username': '13822932613', 'www_username': '15923579949'},
         {'app_username': '15982206284', 'www_username': '18502876278'},
         {'app_username': '18534628124', 'www_username': '17779817875'},
         {'app_username': '17530045802', 'www_username': '15994116094'},
         {'app_username': '18467858385', 'www_username': '13847881515'},
         {'app_username': '18117594631', 'www_username': '13896236597'},
         {'app_username': '15078784280', 'www_username': '13567761544'},
         {'app_username': '13167312508', 'www_username': '18208787492'},
         {'app_username': '19147347063', 'www_username': '15367783844'},
         {'app_username': '16594318320', 'www_username': '13878813758'},
         {'app_username': '15945921257', 'www_username': '13648555543'},
         {'app_username': '18324750521', 'www_username': '18109991234'},
         {'app_username': '15836161565', 'www_username': '13661291916'},
         {'app_username': '13445401669', 'www_username': '15001030866'},
         {'app_username': '17168351176', 'www_username': '13075837646'},
         {'app_username': '13857062949', 'www_username': '18866806210'},
         {'app_username': '17683189223', 'www_username': '17709983239'},
         {'app_username': '18998469929', 'www_username': '18844830201'},
         {'app_username': '13461794502', 'www_username': '13587000647'},
         {'app_username': '15367271530', 'www_username': '18708109399'},
         {'app_username': '15728323849', 'www_username': '18076167905'},
         {'app_username': '17669499130', 'www_username': '18081576755'},
         {'app_username': '17744713168', 'www_username': '15245104068'},
         {'app_username': '13170657862', 'www_username': '18974848150'},
         {'app_username': '16568082112', 'www_username': '15525762061'},
         {'app_username': '14937669710', 'www_username': '17775730187'},
         {'app_username': '18369450956', 'www_username': '18809055322'},
         {'app_username': '14940485599', 'www_username': '13609268414'},
         {'app_username': '13633672981', 'www_username': '15969520696'},
         {'app_username': '17630341979', 'www_username': '18562851555'},
         {'app_username': '17183752138', 'www_username': '18691571175'},
         {'app_username': '19130782869', 'www_username': '18049176877'},
         {'app_username': '15299393248', 'www_username': '18503496400'},
         {'app_username': '15231060196', 'www_username': '15064736240'},
         {'app_username': '18173515951', 'www_username': '18553469796'},
         {'app_username': '17751789990', 'www_username': '15617611903'},
         {'app_username': '16649921781', 'www_username': '18030492896'},
         {'app_username': '18065440936', 'www_username': '15932286502'},
         {'app_username': '13488856027', 'www_username': '15854987898'},
         {'app_username': '18457918027', 'www_username': '18235683970'},
         {'app_username': '15145443832', 'www_username': '15524751165'},
         {'app_username': '17873646685', 'www_username': '15730128680'},
         {'app_username': '19888094506', 'www_username': '15117510097'},
         {'app_username': '15794093960', 'www_username': '18501763680'},
         {'app_username': '17846528646', 'www_username': '18252651471'},
         {'app_username': '18293485652', 'www_username': '15305127076'},
         {'app_username': '15517665195', 'www_username': '13322383736'},
         {'app_username': '15611018992', 'www_username': '15214878645'},
         {'app_username': '13941121583', 'www_username': '18870640621'},
         {'app_username': '18339191413', 'www_username': '13853959393'},
         {'app_username': '17826348193', 'www_username': '15192570765'},
         {'app_username': '14665001795', 'www_username': '18939203280'},
         {'app_username': '13887241329', 'www_username': '18156336920'},
         {'app_username': '18283440271', 'www_username': '18790131876'},
         {'app_username': '17216439730', 'www_username': '13550986064'},
         {'app_username': '13873225987', 'www_username': '13781987133'},
         {'app_username': '17792133315', 'www_username': '18661820895'},
         {'app_username': '17171242388', 'www_username': '13667269223'},
         {'app_username': '17657785125', 'www_username': '13036128781'},
         {'app_username': '18115437579', 'www_username': '15091356191'},
         {'app_username': '15961902048', 'www_username': '18378260189'},
         {'app_username': '17234148207', 'www_username': '13500809212'},
         {'app_username': '13432197370', 'www_username': '18852119958'},
         {'app_username': '19152048765', 'www_username': '15064159319'},
         {'app_username': '19828796744', 'www_username': '18603702826'},
         {'app_username': '14958832666', 'www_username': '15036065246'},
         {'app_username': '14734273795', 'www_username': '18130107359'},
         {'app_username': '18554292351', 'www_username': '18916216332'},
         {'app_username': '15815762757', 'www_username': '13291079378'},
         {'app_username': '15069824582', 'www_username': '13013031832'},
         {'app_username': '18649744684', 'www_username': '13999087154'},
         {'app_username': '15082994785', 'www_username': '18945082837'},
         {'app_username': '17580855160', 'www_username': '15998588263'},
         {'app_username': '18482353156', 'www_username': '15150070380'},
         {'app_username': '13747593863', 'www_username': '15969571900'},
         {'app_username': '15349775464', 'www_username': '13600980953'},
         {'app_username': '16665639387', 'www_username': '18775825778'},
         {'app_username': '14549415839', 'www_username': '15661051165'},
         {'app_username': '15073686783', 'www_username': '15835500535'},
         {'app_username': '14924111031', 'www_username': '15892856866'},
         {'app_username': '18257943792', 'www_username': '13567856980'},
         {'app_username': '18922066669', 'www_username': '15852304664'},
         {'app_username': '17733598197', 'www_username': '18435207559'},
         {'app_username': '13294104440', 'www_username': '13898132025'},
         {'app_username': '15811838172', 'www_username': '13970508656'},
         {'app_username': '18165125725', 'www_username': '15069790354'},
         {'app_username': '16697802238', 'www_username': '15677513708'},
         {'app_username': '14664687883', 'www_username': '18620203688'},
         {'app_username': '15168419306', 'www_username': '13675535980'},
         {'app_username': '17849410284', 'www_username': '15283707877'},
         {'app_username': '17126710669', 'www_username': '15647486061'},
         {'app_username': '15399085982', 'www_username': '13022330997'},
         {'app_username': '15897315783', 'www_username': '15577338744'},
         {'app_username': '14739717872', 'www_username': '18812101541'},
         {'app_username': '17226513517', 'www_username': '13128844239'},
         {'app_username': '18496463318', 'www_username': '15246338752'},
         {'app_username': '17379642471', 'www_username': '15117145379'},
         {'app_username': '15269132800', 'www_username': '15855462855'},
         {'app_username': '17764223449', 'www_username': '15099490493'},
         {'app_username': '13360733917', 'www_username': '18298549994'},
         {'app_username': '13299549436', 'www_username': '13982060420'},
         {'app_username': '17677744893', 'www_username': '15956100107'},
         {'app_username': '13715955388', 'www_username': '13660884273'},
         {'app_username': '18514789992', 'www_username': '15009337431'},
         {'app_username': '18678784774', 'www_username': '17791012394'},
         {'app_username': '18238642352', 'www_username': '13877081106'},
         {'app_username': '18986174885', 'www_username': '18568660951'},
         {'app_username': '14621911396', 'www_username': '18200408030'},
         {'app_username': '18141015515', 'www_username': '15286192183'},
         {'app_username': '13495298792', 'www_username': '15132317009'},
         {'app_username': '13331851186', 'www_username': '15176659514'},
         {'app_username': '19111953173', 'www_username': '13768931725'},
         {'app_username': '15597788322', 'www_username': '13993006453'},
         {'app_username': '14570059086', 'www_username': '18715228076'},
         {'app_username': '13645960228', 'www_username': '13614617740'},
         {'app_username': '16524352722', 'www_username': '18881997898'},
         {'app_username': '18061654324', 'www_username': '15963808163'},
         {'app_username': '16678919449', 'www_username': '13568923170'},
         {'app_username': '19855834088', 'www_username': '13886157029'},
         {'app_username': '18671518721', 'www_username': '13893523801'},
         {'app_username': '18839755124', 'www_username': '13610835340'},
         {'app_username': '13874680480', 'www_username': '15128123635'},
         {'app_username': '15232244258', 'www_username': '18301370201'},
         {'app_username': '18962904249', 'www_username': '13504552255'},
         {'app_username': '18438237372', 'www_username': '15073451863'},
         {'app_username': '18781203235', 'www_username': '13624766266'},
         {'app_username': '14679833220', 'www_username': '15121866168'},
         {'app_username': '18484008412', 'www_username': '15599898902'},
         {'app_username': '17280637594', 'www_username': '18378397730'},
         {'app_username': '18448940788', 'www_username': '15712734999'},
         {'app_username': '18314646474', 'www_username': '15910552765'},
         {'app_username': '14653978628', 'www_username': '13009026280'},
         {'app_username': '15813617066', 'www_username': '15710045002'},
         {'app_username': '17571217640', 'www_username': '13977577308'},
         {'app_username': '17771364635', 'www_username': '13637287815'},
         {'app_username': '13344942979', 'www_username': '17732765022'},
         {'app_username': '17769301317', 'www_username': '15076266702'},
         {'app_username': '18158786433', 'www_username': '13633427663'},
         {'app_username': '16660173038', 'www_username': '17732873595'},
         {'app_username': '13018722574', 'www_username': '17319069236'},
         {'app_username': '13560947555', 'www_username': '15333777575'},
         {'app_username': '15056184415', 'www_username': '17703752322'},
         {'app_username': '14693062493', 'www_username': '13803944119'},
         {'app_username': '18588070250', 'www_username': '13978652652'},
         {'app_username': '14658588980', 'www_username': '13905547141'},
         {'app_username': '16528623399', 'www_username': '13260373682'},
         {'app_username': '13822380708', 'www_username': '15292866251'},
         {'app_username': '13267258773', 'www_username': '15294198748'},
         {'app_username': '13122997582', 'www_username': '15989111657'},
         {'app_username': '15081983214', 'www_username': '13955122606'},
         {'app_username': '15170333911', 'www_username': '18273323221'},
         {'app_username': '13536477315', 'www_username': '18314388267'},
         {'app_username': '17365102067', 'www_username': '13815161718'},
         {'app_username': '13397417759', 'www_username': '13607908472'},
         {'app_username': '16584449719', 'www_username': '15160414922'},
         {'app_username': '14977946403', 'www_username': '17096026128'},
         {'app_username': '15971852586', 'www_username': '18519525259'},
         {'app_username': '14616384060', 'www_username': '13810671655'},
         {'app_username': '17374634564', 'www_username': '15338672096'},
         {'app_username': '13771475713', 'www_username': '18231388637'},
         {'app_username': '17826558690', 'www_username': '18607815266'},
         {'app_username': '15321670820', 'www_username': '13960696919'},
         {'app_username': '13986497498', 'www_username': '13928762112'},
         {'app_username': '18699861125', 'www_username': '18336829112'},
         {'app_username': '14632105540', 'www_username': '15910882868'},
         {'app_username': '13513760481', 'www_username': '13840936558'},
         {'app_username': '13076461431', 'www_username': '13678746356'},
         {'app_username': '18690544832', 'www_username': '18319172997'},
         {'app_username': '17150956530', 'www_username': '17729549378'},
         {'app_username': '17833449700', 'www_username': '18946668966'},
         {'app_username': '15223186724', 'www_username': '13367971263'},
         {'app_username': '17887339482', 'www_username': '15244166496'},
         {'app_username': '18425588832', 'www_username': '17748978947'},
         {'app_username': '13418427765', 'www_username': '17783146866'},
         {'app_username': '18674901014', 'www_username': '15124715211'},
         {'app_username': '17298371120', 'www_username': '15306356547'},
         {'app_username': '13367206805', 'www_username': '15970862336'},
         {'app_username': '15643053481', 'www_username': '15690192898'},
         {'app_username': '15667617390', 'www_username': '13079709453'},
         {'app_username': '14962306003', 'www_username': '13416598229'},
         {'app_username': '18215172819', 'www_username': '13966847307'},
         {'app_username': '13929721198', 'www_username': '17816899809'},
         {'app_username': '15375233386', 'www_username': '18368060780'},
         {'app_username': '18250958927', 'www_username': '13355360550'},
         {'app_username': '13810835331', 'www_username': '15553333260'},
         {'app_username': '19162242540', 'www_username': '18534971347'},
         {'app_username': '15525804977', 'www_username': '18753008975'},
         {'app_username': '14966803822', 'www_username': '15955019082'},
         {'app_username': '18696393615', 'www_username': '13434782858'},
         {'app_username': '15214452015', 'www_username': '13585772793'},
         {'app_username': '13210459989', 'www_username': '18610811597'},
         {'app_username': '17557230559', 'www_username': '15151555346'},
         {'app_username': '18958389544', 'www_username': '18690623523'},
         {'app_username': '17894712309', 'www_username': '13851545220'},
         {'app_username': '18179396136', 'www_username': '13434110310'},
         {'app_username': '18562186864', 'www_username': '18364641507'},
         {'app_username': '13912210531', 'www_username': '15895660834'},
         {'app_username': '15263642480', 'www_username': '15995138923'},
         {'app_username': '14522442822', 'www_username': '15387602276'},
         {'app_username': '19180142136', 'www_username': '13984975855'},
         {'app_username': '17243063689', 'www_username': '13689113903'},
         {'app_username': '13846238584', 'www_username': '13999302808'},
         {'app_username': '18575127371', 'www_username': '13683720527'},
         {'app_username': '17618508392', 'www_username': '15277002844'},
         {'app_username': '14756778070', 'www_username': '18132027570'},
         {'app_username': '16678471104', 'www_username': '18038594493'},
         {'app_username': '13118024909', 'www_username': '13098225692'},
         {'app_username': '15952670143', 'www_username': '15199578988'},
         {'app_username': '18238640763', 'www_username': '18947133683'},
         {'app_username': '18248432334', 'www_username': '15104906589'},
         {'app_username': '15237845217', 'www_username': '18383199223'},
         {'app_username': '19187163750', 'www_username': '15672811160'},
         {'app_username': '13198832386', 'www_username': '15237946233'},
         {'app_username': '16679041039', 'www_username': '18903512984'},
         {'app_username': '13870285847', 'www_username': '13911894409'},
         {'app_username': '18959424228', 'www_username': '15104410634'},
         {'app_username': '13316221533', 'www_username': '15220837744'},
         {'app_username': '18089153640', 'www_username': '18335403292'},
         {'app_username': '18339074264', 'www_username': '15388636911'},
         {'app_username': '13282757668', 'www_username': '13853509927'},
         {'app_username': '13130252091', 'www_username': '18978968536'},
         {'app_username': '18822517386', 'www_username': '18364289199'},
         {'app_username': '19149966904', 'www_username': '13761405606'},
         {'app_username': '19118928384', 'www_username': '13968346177'},
         {'app_username': '15071289514', 'www_username': '15963359296'},
         {'app_username': '14520679195', 'www_username': '13821007093'},
         {'app_username': '16537217497', 'www_username': '13937796523'},
         {'app_username': '18984366618', 'www_username': '15107592403'},
         {'app_username': '13217099264', 'www_username': '15535896323'},
         {'app_username': '16536288075', 'www_username': '17731202905'},
         {'app_username': '17121113785', 'www_username': '15080978640'},
         {'app_username': '15754339496', 'www_username': '13350239612'},
         {'app_username': '13674437175', 'www_username': '13126564241'},
         {'app_username': '17750707068', 'www_username': '18904760910'},
         {'app_username': '17739655713', 'www_username': '18669861905'},
         {'app_username': '18057987669', 'www_username': '14790909764'},
         {'app_username': '18472792133', 'www_username': '18764759700'},
         {'app_username': '14676057012', 'www_username': '13890155626'},
         {'app_username': '14979392282', 'www_username': '15666773082'},
         {'app_username': '15931350099', 'www_username': '15157193900'},
         {'app_username': '13860170094', 'www_username': '13280969449'},
         {'app_username': '15281888085', 'www_username': '13945540846'},
         {'app_username': '18990060006', 'www_username': '15245509597'},
         {'app_username': '17517186284', 'www_username': '15642245030'}]
    for i in v:
        queueData.put_nowait(i)
    host = 'http://www.auto.highso.com.cn'
    wait_time = between(0.500, 1.500)
