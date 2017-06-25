---
title: 邮件发送实践经验
date: 2016-03-22 22:16:23 +0800
slug: edm-practices-notes
category: Misc
keywords: edm, mail server, mail best practices, 邮件, 垃圾邮件, 邮件实践, 邮件发送, 邮件经验
description: 邮件发送端实践经验技巧
---

在做邮件发送服务的时候遇到了种种问题，发现邮件发送有很多技术之外的限制。这里把这些时间查资料和实践出来的一些经验总结在这里。

<!-- more -->

## ESP

邮件服务最重要的是把邮件送达给用户，这中间最大的困难是ESP(Email Service Provider)的反垃圾邮件的机制。

据统计互联网90%的邮件是垃圾邮件。

在国内，最饱受垃圾邮件骚扰也是用户量最大的ESP是QQ邮箱，反垃圾最严格的也是QQ邮箱。

## 信誉度

ESP的反垃圾策略是给邮件服务器评信誉度(reputation)。信誉度与邮件服务器的IP和域名都相关。

每个ESP的反垃圾策略都是他们的技术核心，不会向外界泄露。不过反垃圾关注的重点都是类似的。

发邮件的关键在于怎么提高信誉度，多做加分项，少做减分项。下面是几个监控信誉度的要点

* 邮件是否都送达了
* 发送速率是否被ESP限制了
* 邮件是否因为错误地址退回
* 是否被用户标成垃圾邮件或退订
* 用户是否打开邮件，点开里面的链接

## IP地址与发送量

我最终决定把邮件托管到第三方邮件服务(mailgun)，很多事不用操心了。但有一些事要注意。

* 域名和IP要固定，IP最好是IPv4
* 所在IP段要有好的信誉度，因为有些ESP会封整个IP段
* 国内IP很少，大部分IP被列入黑名单了，这一点上用国外IP反而更好

mailgun有共享IP和独立IP。共享IP是指使用的IP是固定的，不过是与其他人一起使用这个IP。独立IP是指这个IP是专用的，不与他人共享。

使用共享IP和独立IP有个平衡点。如果发的量少用共享IP好一些，因为一个IP发送的邮件少，ESP会认为这个IP不是专门的邮件服务。

如果量太大，ESP也会认为是在发送垃圾邮件，这需要使用独立IP，甚至是多个独立IP。

mailgun推荐每周发送超过5万封邮件，应该使用独立IP；每天发送低于5000封，应该使用共享IP。mailgun主要针对的是国外的ESP，国内的需要考证。

共享IP的问题在于用这个IP的其他人的行为是不可控的。出现过共享IP的某个mailgun用户发垃圾邮件给QQ邮箱，导致QQ邮箱拒收我的邮件。反馈后mailgun很快帮我找了IP。

最好不同的业务使用不同的IP，这样低信誉度的业务不会影响到其它业务的发送。

有了一个新的IP，需要先“热身”。先发送低速度的邮件再逐渐增加发送速率。发送过程关注ESP的反馈
。如果一开始就发大量的邮件，ESP会拒收。我刚开始不知道，用10秒一封的速度发400多封邮件，有199封被QQ邮箱拒收了。后来有了换了新的IP，发送速率慢慢从10分钟一封，8分钟一封，5分钟一封地逐步提高，送达率为100%。

网易邮箱的建议是每小时不超过3000封，每天不超过10万封。

## 域名

不要拿主域名发送EDM，因为一但进了ESP黑名单，公司的正常邮件会受到影响。

跟IP一样，不同的业务用不同的子域名，不要互相影响。

邮件服务的域名和`from`字段里的域名最好一致。

DNS托管服务要有良好的信誉。

要设置反解域名。

域名保存的鉴权信息要完善。

WHOIS记录信息要完善。

MX记录要有效

## 鉴权信息

`SPF`，`DKIM`，`DomainKeys`，`SenderID`，这些要设置，增加ESP的信任。

## 邮件列表

尽最大努力保证收件地址是有效的。

要有退订的功能。不然用户在ESP投诉后果很严重。

## ESP反馈

维护邮件服务的信誉度很大程序是在正确处理拒收邮件。

很多ESP会在第一次退信的时候，把你加入灰名单或是对你限速。如果你还在不断向无效地址发邮件，完全不听ESP的反馈，ESP会把你的邮件过滤掉。

QQ邮件可以通过遍历号码来发邮件，所以他们对无效地址控制很严。

QQ邮箱有反馈环，设置好后有人点击举报会反馈给发邮件者。

QQ邮箱有他域互通的功能，在上面可以看到邮件的到达、阅读、删除和投诉的数据。

## 收件人反馈

收件人以下行为是积极的

* 打开邮件
* 转发邮件
* 回复邮件
* 加到白名单
* 加到联系人
* 标星邮件
* 归档邮件
* 打开链接
* 鼠标滚动邮件页面
* 点击显示图片

收件人以下行为是消极的

* 举报垃圾邮件
* 删除邮件
* 移至垃圾箱
* 点击拒收
* 将发件人添加至黑名单
* 不打开邮件

## 邮件内容

* 根据用户个性化邮件内容
* 邮件最好text和html都有
* 链接、图片与文字的比例越小越好
* 不要有错别字
* 不建议用短url，邮件内容的链接域名要和发件人域名对应
* A/B test优化
* 尽量避免发票、促销、免费、河蟹等关键字，奇怪符号，过多的红黄色、超大字体
* 简洁的html代码，td tr布局。不要有js代码，也不要加附件
* 邮件里的链接要安全合法

**发送对用户有价值的内容**是最重要的，其次才是技术问题。

## 工具

Return Path的信誉度查询 https://www.senderscore.org/

黑名单查询 http://mxtoolbox.com/

----

#### 参考

https://documentation.mailgun.com/best_practices.html

http://feedback.mail.163.com/FeedBack/feedback.do?method=index

http://www.zhihu.com/question/19574247

http://www.zhihu.com/question/19883607

