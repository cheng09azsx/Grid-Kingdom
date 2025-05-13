"""
项目安装脚本
"""
from setuptools import setup, find_packages

setup(
    name="grid_kingdom",
    version="0.1.0",
    description="一款基于Pygame的策略性方格世界建造游戏",
    author="开发者",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "grid-kingdom=main:main",
        ],
    },
)
