#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rf-win - Windows Desktop Automation Robot Framework Library

setup.py用于定义项目的元数据和依赖项
"""

from setuptools import setup, find_packages

# 读取README.md文件内容
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 定义项目依赖项
install_requires = [
    'robotframework>=5.0',
    'pywinauto>=0.6.8',
    'uiautomation>=2.0.14',
    'pillow>=9.0.0',
    'numpy>=1.21.0',
]

# 定义项目可选依赖项
extras_require = {
    'excel': ['openpyxl>=3.0.0'],
    'dev': [
        'pytest>=7.0.0',
        'pytest-cov>=3.0.0',
        'flake8>=4.0.0',
        'black>=22.0.0',
        'isort>=5.0.0',
    ],
}

# 设置项目信息
setup(
    name='rf-win',
    version='1.0.0',
    description='Windows Desktop Automation Robot Framework Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/rf-win',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Desktop Environment',
    ],
    python_requires='>=3.7',
    keywords='robotframework windows automation desktop test',
    include_package_data=True,
    zip_safe=False,
)
