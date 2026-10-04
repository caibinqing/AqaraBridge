# Aqara Bridge for Home Assistant

基于Aqara开放平台，通过云端api进行设备控制以及订阅

[![version](https://img.shields.io/github/manifest-json/v/caibinqing/AqaraBridge?filename=custom_components%2Faqara_bridge%2Fmanifest.json)](https://github.com/caibinqing/AqaraBridge/releases/latest) [![stars](https://img.shields.io/github/stars/caibinqing/AqaraBridge)](https://github.com/caibinqing/AqaraBridge/stargazers) [![issues](https://img.shields.io/github/issues/caibinqing/AqaraBridge)](https://github.com/caibinqing/AqaraBridge/issues) [![hacs](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)

本仓库 fork 自 [bernard3378/AqaraBridge](https://github.com/bernard3378/AqaraBridge)（更早源自 [meishild](https://github.com/meishild/AqaraBridge)、[niceboygithub](https://github.com/niceboygithub/AqaraBridge) 与 [Aqara 官方](https://github.com/aqara/home-assistant)）。

需要 Home Assistant 2026.7.0 及以上版本。

## 一键添加到HACS
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=caibinqing&repository=AqaraBridge&category=integration)
## 需要开发者账号支持

申请AqaraIOT开发者：[Aqara IoT Cloud](https://developer.aqara.com/register).

* 提示：如果在安装过程中出现此集成不支持通过UI配置，大概率是因为rocketmq的链接库不存在，当前版本仅自动集成了x86和arm64。
* [V2.1.1]已加入更多架构支持，如果还出现类似问题请复制日志信息提Issue
* 当前支持通过hacs商店进行配置，自定义存储库URL: caibinqing/AqaraBridge

重点提示：
* 需要自己申请aqara的开发者账号。
* 申请流程1：[注册账号](https://developer.aqara.com/register)，申请通过以后需要选择个人认证，输入姓名和身份证号进行开发者认证。
* 申请流程2：申请通过以后就会有一个DEMO应用，进入项目管理-->详情-->消息推送-->编辑-->选择中国服务、MQ消息推送、消息密钥默认应该只有一个、全订阅-->保存
* 申请流程3：返回概况，Appid&密钥这个点击展开，找到中国服务，记录appId、appkey（需要点击小眼睛）、keyid，然后将这三个参数填写到插件对应的三个值上。
* 消息查看：如果需要确认消息可以将这个插件的日志级别改成info可以查看对应消息情况。

## 版本修订
当前版本 V2.2.0

V2.2.0
* 需要 Home Assistant 2026.7.0 及以上版本
* 添加集成时选择要接入的设备，之后可在“选项 → 选择接入的设备”中修改；未选中的设备不查询、不订阅，取消勾选的设备会被取消订阅并从 HA 中移除
* 只订阅已接入实体用到的资源（开放平台的调用量包含消息推送，按需订阅可节省额度）
* 令牌有效期改为 30 天，剩余不足 3 天时自动刷新，刷新令牌不再重载集成
* 选项改为菜单：选择接入的设备 / 重新授权
* 按集成自身位置查找自带的 librocketmq，不再依赖 HA 的工作目录
* 只为能加载自带库的架构（x86_64、aarch64）复制 librocketmq，复制失败时记录错误而不是导致集成加载失败
* 修复令牌过期后重启无法加载集成
* 修复 HA 重启时卡住（关闭 RocketMQ 消费者，来自 [geofffranks](https://github.com/geofffranks) 的 PR #33）
* 修复修改选项后重载不生效
* 修复 HA 重启时事件实体误触发一次事件（如门铃响铃）
* 修复重新授权表单出错时报错、填错凭据会影响运行中的集成
* 修复红外遥控发送命令阻塞 HA、红外学习不可用
* 修复事件实体图标被固定为按键图标、收到未知值时报错
* 修复实体 ID 域名错误的警告，以及 CONCENTRATION_PARTS_PER_BILLION 弃用警告
* 日志中不再输出 app_key 和刷新令牌
* 代码质量：展开星号导入、清理无用导入等

- 添加设备：
- - lumi.camera.acn005 - 智能可视门铃 G4（门铃响铃、人脸识别事件；开放平台未开放电量与视频）
- - lumi.switch.acn034 - 集悦妙控屏 S1 Plus（功率、用电量）


V2.1.2
* 优化初始化向导提示
* 优化设备初始化流程
* 优化人体场景传感器FP2状态管理
* 优化人体存在传感器FP1/FP1E移动事件

- 添加设备：
- 网关类：
- - lumi.gateway.acn008 - 网关 M1S（第二代）
- - lumi.gateway.acn012 - 网关 M3

- 摄像机类：
- - lumi.camera.gwpagl01 - 智能摄像机G3（网关版） - 支持手势等事件

- 开关/插座类：
- - lumi.switch.acn048 - 卡农 智能墙壁开关 Z1（单键版）
- - lumi.switch.acn049 - 卡农 智能墙壁开关 Z1（双键版）
- - lumi.switch.acn054 - 卡农 智能墙壁开关 Z1（三键版）
- - lumi.switch.acn055 - 卡农 智能墙壁开关 Z1（四键版）
- - lumi.switch.acn056 - 卡农 智能墙壁开关 Z1 Pro（单键版）
- - lumi.switch.acn057 - 卡农 智能墙壁开关 Z1 Pro（双键版）
- - lumi.switch.acn058 - 卡农 智能墙壁开关 Z1 Pro（三键版）
- - lumi.switch.acn059 - 卡农 智能墙壁开关 Z1 Pro（四键版）
- - lumi.switch.acn040 - 智能墙壁开关 E1（零火线三键版）
- - lumi.switch.acn041 - 智能墙壁开关 J1（单火线单键版）
- - lumi.switch.acn042 - 智能墙壁开关 J1（单火线双键版）
- - lumi.switch.acn043 - 智能墙壁开关 J1（单火线三键版）
- - lumi.switch.acn044 - 智能墙壁开关 J1（零火线单键版）
- - lumi.switch.acn045 - 智能墙壁开关 J1（零火线双键版）
- - lumi.switch.acn046 - 智能墙壁开关 J1（零火线三键版）
- - lumi.switch.acn062 - 智能墙壁开关 Q1（单键版）
- - lumi.switch.acn063 - 智能墙壁开关 Q1（双键版）
- - lumi.switch.acn065 - 智能墙壁开关 Q1（四键版）
- - lumi.switch.acn047 - 双路控制模块 T2
- - lumi.sensor_switch.v1 - 无线开关
- - lumi.sensor_switch.v2 - 无线开关
- - lumi.sensor_switch.aq2 - 无线开关

- 灯控类：（感谢XaoflySho提交的PR）
- - lumi.dimmer.acn003 - 智能灯带驱动器 T1
- - lumi.dimmer.acn004 - 智能灯带驱动器 T1（120W）
- - lumi.dimmer.acn005 - 智能灯带驱动器 T1（240W）

- 空调温控类：
- - aqara.airrtc.acn02 - 温控伴侣 T1（室内机）
- - lumi.airrtc.pcacn2 - 智能温控器 S3
- - lumi.airrtc.pcacn2_thermostat - 智能温控器 S3
- - lumi.airrtc.agl001 - 智能阀式温控器 E1

- 窗帘类：
- - lumi.curtain.vagl02 - 智能管状电机 T1
- - lumi.curtain.acn002 - 智能卷帘伴侣 E1



V2.1.1
* 修复窗帘位置同步不及时问题
* 修改将被HA弃用的函数
* 完善arm64架构rocketmq支持
* 优化初始化时可能创建无法管理的实体的问题
* 优化冷启动向导相关
* 优化支持不完善的设备弹出大量警告问题
* 按钮button改为event类

- 添加设备：
- 晾衣架类：
- - lumi.airer.acn001 - 智能晾衣机H1
- - lumi.airer.acn02 - Aqara智能晾衣机 Lite

V2.1.0 - 修复大部分错误并添加大量设备
* 重写空调控制器类
* 修复rocketmq启动时阻塞HA初始化问题
* 修复了调用某些HA已废弃/将要废弃常量问题
* 修复light设备类颜色映射错误
* 修复button设备类UI按钮问题
* 修复无线场景开关（六键版）型号错误
* 优化Entities载入流程
* 优化多通道设备初始化流程
* 优化设备和Entity自动命名规则

- 添加设备：
- 网关类：
- - lumi.controller.a4acn1 - 集悦智慧面板 S1 

- 开关/插座类： 
- - lumi.switch.n3acn3 - 智能墙壁开关D1（零火线三键版） 
- - lumi.switch.l3acn3 - 智能墙壁开关D1（单火线三键版） 
- - lumi.ctrl_86plug.aq1 - 墙壁插座（Zigbee版） 
- - lumi.relay.c2acn01 - 双路控制器 

- 灯控类： 
- - lumi.light.cbacn1 - Aqara 智能恒流驱动器 T1-1 
- - lumi.light.cwopcn01 - 吸顶灯MX960（可调色温） 
- - lumi.light.acn007 - 轨道格栅灯 H1（6头） 
- - lumi.light.acn008 - 轨道格栅灯 H1（12头） 
- - lumi.light.acn009 - 轨道泛光灯 H1（30cm） 
- - lumi.light.acn010 - 轨道泛光灯 H1（60cm） 
- - lumi.light.acn011 - 轨道吊线灯 H1 
- - lumi.light.acn012 - 轨道折叠格栅灯 H1（6头） 
- - lumi.light.acn013 - 轨道偏光灯 H1（22cm） 
- - lumi.light.cwjwcn02 - 筒灯（可调色温） 
- - lumi.light.acn004 - Aqara 双色温驱动器 T1 Pro 
- - lumi.light.acn006 - 轨道灯 H1 Pro 
- - lumi.light.acn023 - 射灯 T2（15度） 
- - lumi.light.acn024 - 射灯 T2（24度） 
- - lumi.light.acn025 - 射灯 T2（36度） 
- - lumi.light.acn026 - 筒灯 T2（60度） 
- - lumi.light.acn128 - 筒射灯 T3 
- - lumi.light.acn014 - LED灯泡 T1（可调色温） 
- - lumi.light.acn003 - Aqara 吸顶灯 L1-350 
- - lumi.light.acn015 - Aqara光艺晴空灯 H1 
- - lumi.light.acn032 - 幻彩吸顶灯 T1（40W） 
- - lumi.light.acn132 - 流光溢彩灯带 T1 

- 窗帘类：
- - lumi.curtain.v1 - 智能窗帘电机 (Zigbee开合帘版)
- - umi.curtain.acn007 - Aqara智能窗帘电机 T1
- - lumi.curtain.hagl07 - 智能窗帘电机 C2
- - lumi.curtain.hagl08 - Aqara智能窗帘电机A1
- - lumi.curtain.hagl04 - 智能窗帘电机 B1
- - lumi.curtain.acn015 - Aqara智能窗帘电机 T2
- - lumi.curtain.aq2 - 智能管状电机
- - lumi.curtain.hagl04 - 智能窗帘电机 B1
- - lumi.curtain.acn04 - Aqara智能窗帘电机 C3
- - lumi.curtain.acn003 - 智能窗帘伴侣E1

- 空调/地暖类：
- - lumi.aircondition.acn05 - 空调伴侣 P3
- - lumi.airrtc.vrfegl01 - VRF空调控制器
- - lumi.acpartner.aq1 - 空调伴侣
- - lumi.acpartner.v3 - 空调伴侣（升级版）
- - lumi.ctrl_hvac.es1 - 空调温控器
- - lumi.airrtc.tcpco2ecn01 - 空调温控器（CO2）
- - lumi.acpartner.es1 - 空调伴侣
- - lumi.airrtc.tcpecn01 - 空调温控器
- - lumi.airrtc.tcpecn02 - 空调温控器 S2

- 传感器类：
- - lumi.motion.ac02 - 人体传感器 P1
- - umi.motion.agl02 - 人体传感器 T1
- - lumi.motion.acn001 - 人体传感器 E1
- - lumi.motion.agl001 - 人体场景传感器 FP2
- - lumi.sensor_occupy.agl1 - AI智能存在传感器 FP1E
- - lumi.sensor_natgas.v1 - 天然气报警器
- - lumi.sensor_gas.acn02 - Aqara天然气报警器
- - lumi.airmonitor.acn01 - TVOC空气健康伴侣
- - lumi.sen_ill.agl01 - 光照传感器 T1


V2.0.3
* 修复开发者配置问题，可以使用自己开发者信息。


V2.0.2
* 修复错误保存问题，增加启动依赖，需要在homekit启动正常以后。
* 修复flow的option操作错误，可以重新通过手机号刷新失效token，并修复部分错误提示。
* hass图标已经通过，当前可以正常显示组件图标，以及设备厂商图标。
* 修复其他常规错误。

V2.0.1
* 整体合并到master，原有的配置方式需要使用dev分支，该分支不继续维护。
* 修改flow，将多个网关合并到账号，拆分开发者认证信息允许自行配置自己的开发者AK等。
* 修复大部分组件获取状态异常，以及历史状态修改。
* 感谢[银狼](https://bbs.hassbian.com/?62352)新增部分组件配置：支持无线旋钮H1，H1 12头磁吸格栅灯，无线按钮（升级版）。同时墙壁开关拆分为两部分，其中零火的加入了电量监测，led驱动模块加了电力监测。

V1.0.1
* 修复了大部分组件的问题，增加了无线按键。当前的按键都同时事件订阅刷新时间整体速度还不错，不是轮训机制了。
* 增加房间位置获取。
* 增加按键类开关对应按键名称获取。
* 增加arm64的rocketmq动态链接库，除了X86和arm64其他暂时没处理。
* 增加各类的历史数据获取刷新了最后的trigger_time或者last_update_time。
* 增加button类型，将无线开关从传感器上拆分。
* 配置了大部分常见的网关、无线开关、单火/零火开关、温湿度传感器、智能插座、人体传感器等。
* 增加了部分错误提示，至少不会在配置没任何错误了。

V1.0.0

还有我只支持了大部分我有的设备和类似的组件，如果发现有不支持的懂python的修改：
[custom_components/aqara_bridge/core/aiot_mapping.py](https://github.com/caibinqing/AqaraBridge/blob/master/custom_components/aqara_bridge/core/aiot_mapping.py)

