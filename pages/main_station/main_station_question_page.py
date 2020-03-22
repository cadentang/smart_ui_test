# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage
from component.main_station.main_station_question_component import MainStationQuestionComponent
from utils.base_path import RESOURCE_PATH
from utils.get_log import logger
from common.selenium_pages import PageScroll

picture_path = RESOURCE_PATH + "/picture/question_upload_picture/"

class MainStationQuestionPage(MainStationBasePage):
    """问答页面"""
    # 问答导航栏
    _my_question_span = Element(css="li.ant-menu-item.ant-menu-item-selected>span", describe="我的问题")
    _article_question_span = Element(css="li.ant-menu-item.ant-menu-item-selected>span", describe="问答精华")
    _question_input = Element(css="div>span>input", describe="问题、考点输入框")
    _question_button = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="我要提问")

    # 问题筛选
    _question_source_my_question_input = Element(xpath="//span[contains(text(), '我提问的')]/preceding-sibling::span", describe="问题来源-我提问的")
    _question_source_my_collect_input = Element(xpath="//span[contains(text(), '我收藏的')]/preceding-sibling::span", describe="问题来源-我收藏的")
    _question_type_live_input = Element(xpath="//span[contains(text(), '直播回放问题')]/preceding-sibling::span", describe="问题类型-直播回放问题")
    _question_type_video_input = Element(xpath="//span[contains(text(), '视频问题')]/preceding-sibling::span", describe="问题类型-视频问题")
    _question_type_exam_input = Element(xpath="//span[contains(text(), '试题问题')]/preceding-sibling::span", describe="问题类型-试题问题")
    _question_type_textbook_input = Element(xpath="//span[contains(text(), '教材问题')]/preceding-sibling::span", describe="问题类型-教材问题")
    _question_type_kefu_input = Element(xpath="//span[contains(text(), '客服问题')]/preceding-sibling::span", describe="问题类型-客服问题")

    # 看课记录、教材、做题记录列表
    _question_go_course_page_button = Element(xpath="//div/button[contains(text(),'去看看')]", describe="无观看视频点击按钮去个人中心页")
    _question_go_exam_page_button = Element(xpath="//div/button[contains(text(),'去做题')]", describe="无做题记录点击按钮去题库首页")
    _question_go_course_record_div = Element(xpath="//div/div[contains(text(),'课程问题')]", describe="看视频记录列表页")
    _question_go_textbook_div = Element(xpath="//div/div[contains(text(),'教材问题')]", describe="教材列表页")
    _question_go_exam_div = Element(xpath="//div/div[contains(text(),'试题问题')]", describe="做题记录列表页")
    _question_first_course_button = Element(xpath="//ul/li[1]/div/button", describe="看课记录列表中第一条数据")
    _question_first_textbook_button = Element(xpath="//div[2]/div/div/div[1]/div[2]/div[1]/button", describe="教材列表第一条知识点提问按钮")
    _question_1_textbook_div = Element(xpath="//div[2]/div/div/div/div[2]/div/div[1]", describe="打开一级知识点")
    _question_2_textbook_div = Element(xpath="//div[2]/div/div[1]/div[2]/div/div/div[1]/div[1]", describe="打开二级知识点")
    _question_3_textbook_div = Element(xpath="//div[2]/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]", describe="打开三级知识点")
    _question_first_exam_button = Element(xpath="//div[1]/ul/li[1]/div/button", describe="做题记录列表页第一条数据")

    # 提问页面
    _question_page_code_button = Element(css="input[placeholder='页码']", describe="教材页码输入框")
    _question_jiachu_button = Element(css="button[data-title='加粗']", describe="加粗")
    _question_xieti_button = Element(css="button[data-title='斜体']", describe="斜体")
    _question_xiahuaxian_button = Element(css="button[data-title='下划线']", describe="下划线")
    _question_order_list_button = Element(css="button[data-title='有序列表']", describe="有序列表")
    _question_picture_button = Element(css="button[data-title='图片']", describe="图片")
    _question_list_button = Element(css="button[data-title='无序列表']", describe="无序列表")
    _question_link_button = Element(css="button[data-title='链接']", describe="链接")
    _question_cancle_link_button = Element(css="button[data-title='取消链接']", describe="取消链接")
    _question_link_input = Element(css="input[placeholder='输入链接地址']", describe="输入链接地址")
    _question_link_confirm_button = Element(xpath="//button[contains(text(), '确定')]", describe="链接确定按钮")
    _question_link_cancle_button = Element(xpath="//button[contains(text(), '取消')]", describe="链接取消按钮")
    _question_file_input = Element(css="input[type='file']", describe="图片文件输入框")
    _question_picture_confirm_button = Element(xpath="//button[contains(text(), '插入所选项目')]", describe="图片插入所选项目")
    _question_picture_cancle_button = Element(xpath="//button[contains(text(), '取消')]", describe="图片取消按钮")
    _question_input_div = Element(css="div.notranslate.public-DraftEditor-content", describe="问题输入框")
    _question_confire_button = Element(xpath="//div[starts-with(@class,'src-components-HxEditor-index')]/button[contains(text(), '提问')]", describe="提问确定按钮")
    _question_alter_button = Element(xpath="//button/span[contains(text(), '知道了')]", describe="提问确认弹窗")

    # 无权限和超过提问次数权限弹窗
    _question_no_perssion = (By.XPATH, "//div/div[contains(text(),'您未购买课程无法提问，请购买后体验！')]")  # 无提问权限


    # 问题详情页面
    _question_supplementary_span = Element(xpath='//div/span[contains(text(), "补充问题 》")]', describe="补充问题")
    _question_append_span = Element(xpath='//div/span[contains(text(), "继续追问 》")]', describe="追问问题")

    _question_list_component_lis = "//ul[starts-with(@class,'ant-list-item')]/li"  # 定位问题列表组件,有可能有多个
    _question_list_component_detail_div = (By.XPATH, "//div[starts-with(@class, 'src-pages-question-detail-index__detailContent')]")  # 详情页组件

    def get_compent_list(self, index=1):
        """获取列表页的问题组件, 默认返回第一个问题，如果没有则返回false"""

        question_compent_location = (By.XPATH, self._question_list_component_lis + f"[{index}]")
        return MainStationQuestionComponent(self.driver, question_compent_location)

    def get_question_count(self):
        """获取问题列表中有多少条主问题"""
        self.driver.refresh()
        PageScroll(self.driver).js_scroll_end()
        PageScroll(self.driver).js_scroll_top()
        try:
            count = len(self.driver.find_elements_by_xpath(self._question_list_component_lis))
        except NoSuchElementException:
            count = 0
        return count

    def get_append_question_count(self):
        """获取列表中有多少追问问题"""
        self.driver.refresh()
        PageScroll(self.driver).js_scroll_end()
        PageScroll(self.driver).js_scroll_top()
        try:
            count = len(self.driver.find_elements(*MainStationQuestionComponent._question_appent_content_span))
        except NoSuchElementException:
            count = 0
        return count

    def go_question_detail(self):
        """进入问题详情页, 返回问题详情页组件"""
        com = self.get_compent_list()
        com.question_detail()
        return MainStationQuestionComponent(self.driver, self._question_list_component_detail_div)

    @allure.step("对课程提问(默认第一条观看记录，如没有则跳转至个人中心页)")
    def question_for_course(self, content, file=False):
        """file为False不上传图片，为True上传图片"""
        self._question_button.click()
        try:
            self._question_first_course_button.click()
            if file == True:
                self.upload_picture()
            text = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + content +  "【测试自动化课程提问】"
            self._question_input_div =  text
            self._question_confire_button.click()
            ele = self.driver.find_element_by_xpath("//button/span[contains(text(), '知道了')]")
            self.driver.execute_script("arguments[0].click();", ele)
            time.sleep(2)
            self.driver.refresh()
            time.sleep(2)
            return text
        except:
            self._question_go_course_page_button.click()

    @allure.step("对教材提问(默认第一条教材提问)")
    def question_for_textbook(self, content, file=False):
        self._question_button.click()
        self._question_go_textbook_div.click()
        time.sleep(1)
        self._question_1_textbook_div.click()
        time.sleep(1)
        self._question_2_textbook_div.click()
        time.sleep(1)
        self._question_first_textbook_button.click()
        self._question_page_code_button = "12"
        if file == True:
            self.upload_picture()
        text = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + content +  "【测试自动化教材提问】"
        self._question_input_div = text
        self._question_confire_button.click()
        ele = self.driver.find_element_by_xpath("//button/span[contains(text(), '知道了')]")
        self.driver.execute_script("arguments[0].click();", ele)
        time.sleep(2)
        self.driver.refresh()
        return text

    @allure.step("对试题提问(默认第一条做题记录，如没有则跳转至题库做题页面)")
    def question_for_examrecord(self, content, file=False):
        self._question_button.click()
        try:
            self._question_first_exam_button.click()
            if file == True:
                self.upload_picture()
            text = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + content +  "【测试自动化试题提问】"
            self._question_input_div =  text
            self._question_confire_button.click()
            ele = self.driver.find_element_by_xpath("//button/span[contains(text(), '知道了')]")
            self.driver.execute_script("arguments[0].click();", ele)
            time.sleep(2)
            self.driver.refresh()
            return text
        except:
            self._question_go_exam_page_button.click()

    @allure.step("对提的问题补充问题")
    def question_for_supplement(self, supplementary_content, file=False):
        # 先提问，再对提的问题补充问题
        first_content = self.question_for_course(content="测试补充问题", file=True)
        self.driver.refresh()
        com = self.get_compent_list(index=1)
        if com:
            com.question_detail()
            self._question_supplementary_span.click()

            if file == True:
                self.upload_picture()
            text = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + supplementary_content + "【测试自动化试题提问-补充问题】"
            self._question_input_div = text
            self._question_confire_button.click()
        else:
            logger.info("列表中没有问题")

    @allure.step("对老师回复的问题再次追问")
    def question_for_append(self, append_content, file=False):
        # count = self.get_question_count()
        # for i in range(count):
        #     logger.info(f"i:{i}")
        #     com = self.get_compent_list(index=i+1)
        #     logger.info(f"组件文本: {com.get_main_content()}")
            # logger.info(f"组件文本: {com.get_question_id()}")

        # 获取列表中第一个问题，如果已回复则追问，未回复则先回复再追问
        # 只有当主问题已回复且无追问问题或者追问问题已回复才能继续追问
        com = self.get_compent_list()
        result = com.judge_is_answer()
        logger.info(f"com.judge_is_answer()的结果:{result}")
        if result in [2, 3]:
            com.question_detail()
            self._question_append_span.click()
            if file == True:
                self.upload_picture()
            text = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + append_content + "【测试自动化提问-追问】"
            self._question_input_div = text
            self._question_confire_button.click()
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element_by_xpath("//button/span[contains(text(), '知道了')]"))
            self.go_question()
            return text
        else:
            self.question_teacher_replay()
            self.driver.refresh()
            time.sleep(2)
            com.question_detail()
            self._question_append_span.click()
            if file == True:
                self.upload_picture()
            text = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + append_content + "【测试自动化提问-追问】"
            self._question_input_div = text
            self._question_confire_button.click()
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element_by_xpath("//button/span[contains(text(), '知道了')]"))
            self.go_question()
            return text

    @allure.step("对学员提的问题进行回复")
    def question_teacher_replay(self, index=1):
        """默认回复第一个问题，若第一个已回复则依次向下寻找能够回复的问题"""
        # count = self.get_question_count()
        compent = self.get_compent_list(index)
        if compent.judge_is_answer() in [0,1]:
            compent.question_detail()
            self.question_answer(compent.get_question_id())
            self.go_question()
            time.sleep(2)
            self.driver.refresh()
            try:
                if self.get_no_read_question() == "1" or compent.judg_new_mark() == True:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False


    @allure.step("列表页对问题点赞")
    def question_dianzan(self):
        com = self.get_compent_list()
        com.dianzan()

    @allure.step("列表页对问题取消点赞")
    def question_cancel_dianzan(self):
        com = self.get_compent_list()
        com.dianzan()

    @allure.step("列表页对问题收藏")
    def question_collect(self):
        com = self.get_compent_list()
        com.collect()

    @allure.step("列表页对问题取消收藏")
    def question_cancel_collect(self):
        com = self.get_compent_list()
        com.collect()

    @allure.step("列表页对老师评一星+评价")
    def question_appraise_one_star(self, content):
        com = self.get_compent_list()
        com.score_main_question(1, content)

    @allure.step("列表页对老师评四星+评价")
    def question_appraise_four_star(self, content):
        com = self.get_compent_list()
        com.score_main_question(4, content)

    def question_answer(self, question_id):
        """根据question_id回复学生的提问"""
        import requests
        # question-service问答接口
        if "w0" in self.driver.current_url:
            url = "http://192.168.16.250:32000/h/com.haixue.question.api.AnswerApi/saveAnswer"
            create_by = "120425"
        elif "w1" in self.driver.current_url:
            url = "http://192.168.16.247:32000/h/com.haixue.question.api.AnswerApi/saveAnswer"
            create_by = "120751"
        elif "w2" in self.driver.current_url:
            url = "http://123.126.133.237:32000/h/com.haixue.question.api.AnswerApi/saveAnswer"
            create_by = "138725"
        else:
            logger.info("不支持的回复")

        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        answer_request = {
                "questionId": question_id,
                "createBy": create_by,
                "createByName": "tangkun4379",
                "content": "测试正常回答问题12345678",
                "isEssence": "No",
                "isPrivateVisible": "No",
                "outlineInitialIds": 126711
            }

        data = {
            "answerRequest": json.dumps(answer_request)
        }
        re = requests.post(url, headers=header, data=data)
        code = re.json()["code"]
        if code == 204:
            logger.info("回复成功！")
            return True
        else:
            logger.info(f"回复失败，失败信息: {re.json()['msg']}")
            return False

    def check_question(self, content, is_append=False):
        """根据问题内容检查列表是否有该主问题或追问问题"""
        if is_append == False:
            count = self.get_question_count()
            for i in range(count):
                compent_text = self.get_compent_list(index=i+1).get_main_content()
                logger.info(f"提问内容: {content}")
                logger.info(f"列表里面主内容: {compent_text}")
                if compent_text == content:
                    return True
                else:
                    return False
        else:
            count = self.get_append_question_count()
            for i in range(count):
                compent_text = self.get_compent_list(index=i+1).get_append_content()
                if compent_text == compent_text:
                    return True
                else:
                    return False

    def upload_picture(self):
        """上传图片"""
        self._question_picture_button.click()
        time.sleep(1)
        # if isinstance(list, picture_list):
        #     if len(picture_list) > 0:
        #         for i in len(picture_list):
        #             self._question_file_input = picture_list[i]

        self._question_file_input = picture_path + "/png格式.png"
        time.sleep(10)
        ele = self.driver.find_element_by_xpath("//button[contains(text(), '插入所选项目')]")
        time.sleep(5)
        self.driver.execute_script("arguments[0].click();", ele)

    def question_for_no_perssion(self):
        """无提问权限"""
        pass


if __name__ == "__main__":
    driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
    driver.maximize_window()

    driver.get("http://w2.highso.com.cn/v5")
    driver.current_url
    driver.implicitly_wait(10)
    # driver.refresh()
    # driver.find_element_by_css_selector()
    time.sleep(3)
    from pages.main_station.main_station_home_page import MainStationHomePage

    aa = MainStationHomePage(driver)
    bb = aa.go_to_login_page().to_login("haixue", "19983271081", "123456")
    # bb.driver.get("http://w2.highso.com.cn/v5/my/course")
    # aa.get_bottom_list_navigations()
    # aa.logout()
    # bb.go_message()
    time.sleep(1)
    cc = bb.go_question()
    # cc.go_question_detail()
    # dd = cc.driver.current_url
    # t = int(dd.split("/")[-1])
    # cc.question_for_course("追问")
    # print(cc.question_teacher_replay())
    # cc.question_for_append("追问")
    cc.question_for_supplement("这个是补充问题")
    # print(cc.get_compent_list(3).judge_is_answer())
    # cc.question_for_examrecord("222222")



    time.sleep(1)
    # question_list_component_lis = (By.CSS_SELECTOR, "ul.ant-list-items>li")  # 定位问题列表组件,有可能有多个
    # eles = driver.find_elements(*question_list_component_lis)
    # print(eles)
    # print(len(eles))
    # for i in len(eles):
    #     compent = MainStationQuestionComponent(driver, (By.CSS_SELECTOR, f"ul.ant-list-items>li:nth-child({i + 1})"))
    #
    # cc.question_for_course("测试上传图片")
    # cc.get_question_count()
    time.sleep(1)
    # MainStationQuestionPage.question_answer(1460183)
