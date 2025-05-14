# 方格王国 (Grid Kingdom)
## 概述
一款基于Pygame的策略性方格世界建造游戏。玩家通过策略性拼接地块、安装插件、构建自动化生产线，管理资源并应对随机事件，逐步扩张自己的方格王国。
## 特色功能
- **模块化地块拼接** - 自由组合建筑卡牌构建王国版图
- **深度自动化生产** - 建立资源采集、加工、运输的完整产业链
- **卡牌驱动策略** - 通过建筑卡、插件卡、策略卡实现多维发展
- **动态事件系统** - 包含随机事件、剧情事件与抉择事件

- **插件扩展机制** - 通过模块化插件自定义建筑功能
- **极简主义UI设计** - 符号化界面呈现核心信息（注：没有美工哭哭）

## 项目结构
Grid-Kingdom/ (项目根目录)
├── grid_kingdom/       # 主要的游戏逻辑包 (Python Package)
│   ├── core/            # 核心系统 (游戏引擎, 状态机, 事件管理器, 配置等)
│   │   ├── init.py
│   │   ├── engine.py     # 游戏主循环 (处理输入, 更新游戏状态, 渲染)
│   │   ├── game_state_manager.py # 状态机管理游戏状态
│   │   ├── event_manager.py # 事件管理器 (处理游戏内事件)
│   │   └── config_loader.py # 配置加载器 (加载游戏设置)
│   │
│   ├── game_objects/    # 游戏内实体对象 (地块, 建筑, 插件, 卡牌等)
│   │   ├── init.py
│   │   ├── tile.py       # 地块类 (包含位置, 类型, 功能等)
│   │   ├── building.py   # 建筑类 (包含属性, 功能, 插件等)
│   │   ├── plugin.py     # 插件类 (包含功能, 效果等)
│   │   └── card.py       # 卡牌类 (包含属性, 效果等)
│   │
│   ├── systems/         # 负责具体游戏逻辑的系统 (资源, 生产, 科研, UI管理等)
│   │   ├── init.py
│   │   ├── resource_system.py # 资源管理系统
│   │   ├── production_system.py # 生产管理系统
│   │   ├── card_system.py # 卡牌管理系统
│   │   ├── research_system.py # 科研管理系统
│   │   ├── turn_system.py # 回合管理系统
│   │   └── random_event_system.py # 随机事件系统
│   │
│   ├── ui/               # 用户界面相关 (渲染, UI元素, 屏幕管理)
│   │   ├── init.py        
│   │   ├── renderer.py    # 渲染器
│   │   ├── ui_manager.py  # UI管理器
│   │   ├── screens/       # 不同的游戏屏幕 (主菜单, 游戏界面, 游戏结束等)
│   │   └── components/    # 可重用的UI组件 (按钮, 标签, 进度条等)
│   │
│   ├── utils/           # 通用工具函数、常量、枚举等
│   │   ├── init.py
│   │   ├── constants.py  # 常量定义 (如颜色, 资源类型等)
│   │   ├── enums.py      # 枚举定义 (如地块类型, 卡牌类型等)
│   │   ├── logger.py     # 日志工具 (用于记录游戏运行信息)
│   │   └── helpers.py    # 辅助函数 (如坐标转换, 资源计算等)
│   │
│   └── factory/         # 对象创建工厂 (用于解耦对象的创建逻辑)
│       ├── init.py
│       ├── entity_factory.py # 实体对象工厂
│
├── assets/             # 游戏媒体资源 (图片, 声音, 字体)
│   ├── images/
│   ├── sounds/
│   ├── fonts/
│
├── data/               # 游戏数据定义 (JSON, CSV) - 如卡牌属性, 建筑参数等
│   ├── cards/          # 卡牌数据
│   ├── buildings/      # 建筑数据
│   ├── plugins/        # 插件数据
│   └── events/         # 事件数据
│
├── tests/              # 单元测试和集成测试
│   ├── init.py
│   ├── test_core/       # 测试核心系统
│   ├── test_game_objects/ # 测试游戏对象
│   └── test_systems/    # 测试游戏系统
│
├── main.py             # 游戏主入口脚本
├── requirements.txt    # Python依赖列表
├── .gitignore          # Git忽略文件配置
└── README.md           # 本文件

## 玩法简介
在《方格王国》中，您将扮演一位雄心勃勃的王国建造者。从一片空白的方格土地开始，您需要：
1.  **规划布局**：策略性地放置不同功能的地块。
2.  **发展产业**：建造加工厂，将原始资源转化为高级材料。
3.  **驱动创新**：使用插件卡强化建筑，或打出策略卡应对突发状况，甚至改变局势。
4.  **扩展疆域**：通过科研解锁新的建筑和技术，不断向外扩张。
5.  **应对挑战**：处理随机生成的事件，可能是丰收的喜悦，也可能是灾害的考验。
您的目标是建立一个繁荣、高效、可持续发展的自动化王国！


## 安装指南
### 环境要求
- Python 3.12+
- Pygame 2.5+
### 快速开始
```bash
# 克隆仓库
git clone https://github.com/cheng09azsx/Grid-Kingdom
cd grid-kingdom
# 安装依赖
pip install -r requirements.txt
# 启动游戏
python main.py

## 贡献
欢迎提交问题和拉取请求来帮助改进游戏！

## 许可证
本项目使用GAGPL-V3许可证 - 详情见LICENSE文件