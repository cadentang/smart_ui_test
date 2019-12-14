### 运行项目
- python版本>=3.7
- 拉取代码：git clone http://git.highso.com.cn:81/haixue-auto-test/haixue-test-ui.git
- 下载drivers，百度网盘：链接：https://pan.baidu.com/s/1pyuOjEkiYu2pTQtobdSazQ 
提取码：k4tu
- 下载allure命令行工具，https://github.com/allure-framework/allure1/releases/download/allure-core-1.5.2/allure-commandline.zip
解压并设置到环境变量

### 项目结构
- business:场景方法封装
- common：通用方法封装
- config：配置文件
- data：测试数据，静态数据、动态数据
- extend：使用到的外部工具包
- pages：页面对象封装
- resource：测试过程中需要使用到的静态资源，如图片、文件等
- script：脚本文件
- service：selenium grid服务、appium服务
- test_case：测试用例
- utils：底层基础工具
- .gitignore：git忽略文件
- conftest.py：pytest测试用例运行前执行的fixture
- pytest.ini：pytest配置文件
- requirements.txt：项目依赖外部包
- run.py：项目依赖的入口文件
- drivers：项目运行依赖的driver
- log：运行的日志
- report：测试报告

### 项目运行架构
