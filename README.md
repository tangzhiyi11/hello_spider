# hello_spider
豆瓣租房小组爬虫

#目前进度
2016/9/24
1.吐槽：爬取频率这么低也会被封，也是醉了....


2016/9/23<br />
1.增加post title分析模块，使用jieba进行分词统计<br />
2.部署爬虫，目前爬取频率较低..<br />
3.雏形基本稳定，等待更多数据开发分析模块<br />

2016/9/22<br />
1.完善spider流程，测试spider<br />
2.待解决爬取频率问题，目前爬取一张url list会sleep(5)，ip已经被封<br />
3.修改了post类，去除content字段<br />

2016/9/21<br />
1.Auth类cookie无法保存文件，使用LWPCooieJar保存到disk时，会丢失字段，待解决<br />
2.增加了帖子解析模块，并将帖子信息存入MongoDB中<br />

2016/9/20<br />
增加了用户登录认证模块，需要输入用户的账号密码，需要人工识别验证码（后期考虑自动识别），登录模块在auth.py中，参考[douban_crawler](https://github.com/gt11799/douban_crawler)<br />

2016/9/19<br />
爬取了小组topic id以及最后的回帖时间<br />
