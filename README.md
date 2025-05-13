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
grid_kingdom/
│
├── assets/              # 游戏资源文件
│   ├── images/          # 图像资源
│   ├── sounds/          # 音效资源
│   └── data/            # 游戏数据定义(JSON/CSV)
│
├── src/                 # 源代码
│   ├── core/            # 核心系统
│   │   ├── __init__.py
│   │   ├── engine.py    # 游戏引擎
│   │   ├── game_state.py # 游戏状态管理
│   │   ├── event_manager.py # 事件管理
│   │   └── config.py    # 配置管理
│   │
│   ├── game_objects/    # 游戏对象
│   │   ├── __init__.py
│   │   ├── tile.py      # 地块类
│   │   ├── building.py  # 建筑基类及子类
│   │   ├── plugin.py    # 插件基类及子类
│   │   └── card.py      # 卡牌基类及子类
│   │
│   ├── systems/         # 游戏系统
│   │   ├── __init__.py
│   │   ├── resource_system.py  # 资源系统
│   │   ├── card_system.py      # 卡牌系统
│   │   ├── research_system.py  # 科研系统
│   │   ├── round_system.py     # 回合系统
│   │   ├── event_system.py     # 事件系统
│   │   └── grid_system.py      # 网格系统
│   │
│   ├── ui/              # 用户界面
│   │   ├── __init__.py
│   │   ├── renderer.py  # 渲染器
│   │   ├── ui_manager.py # UI管理器
│   │   ├── screens/     # 不同场景界面
│   │   └── components/  # UI组件
│   │
│   ├── utils/           # 工具函数
│   │   ├── __init__.py
│   │   ├── constants.py # 常量定义
│   │   ├── logger.py    # 日志工具
│   │   └── helpers.py   # 辅助函数
│   │
│   └── factory/         # 工厂类
│       ├── __init__.py
│       ├── building_factory.py # 建筑工厂
│       ├── card_factory.py     # 卡牌工厂
│       └── plugin_factory.py   # 插件工厂
│
├── tests/               # 单元测试
│   ├── __init__.py
│   ├── test_core/
│   ├── test_game_objects/
│   └── test_systems/
│
├── main.py              # 游戏入口
├── requirements.txt     # 依赖列表
├── setup.py             # 安装脚本
└── README.md            # 项目说明

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