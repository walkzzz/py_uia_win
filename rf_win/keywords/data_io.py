#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据IO关键字模块
提供读写文本、JSON、CSV、Excel文件的关键字
"""

from .. import keyword, library
from ..modules.data_io import DataIO
from ..utils.logger import logger

@library(scope='GLOBAL', version='1.0.0')
class DataIOKeywords:
    """数据IO关键字类
    
    提供读写文本、JSON、CSV、Excel文件的关键字，用于Robot Framework测试用例
    """
    
    def __init__(self):
        """初始化数据IO实例"""
        self.data_io = DataIO()
    
    @keyword(name='读取文本文件', tags=['数据IO'])
    def read_text_file(self, file_path, encoding='utf-8'):
        """读取文本文件
        
        读取指定路径的文本文件内容
        
        参数:
            file_path: 文件路径
            encoding: 文件编码，默认为utf-8
        
        返回:
            文件内容
        
        示例:
            | ${content} | 读取文本文件 | C:/test.txt |
            | ${content} | 读取文本文件 | C:/test.txt | 编码=gbk |
        """
        logger.info(f"读取文本文件: {file_path}, 编码: {encoding}")
        return self.data_io.read_text_file(file_path, encoding)
    
    @keyword(name='写入文本文件', tags=['数据IO'])
    def write_text_file(self, file_path, content, encoding='utf-8', append=False):
        """写入文本文件
        
        向指定路径的文本文件写入内容
        
        参数:
            file_path: 文件路径
            content: 要写入的内容
            encoding: 文件编码，默认为utf-8
            append: 是否追加写入，默认为False（覆盖写入）
        
        示例:
            | 写入文本文件 | C:/test.txt | Hello World |
            | 写入文本文件 | C:/test.txt | Append Text | 追加=True |
        """
        logger.info(f"写入文本文件: {file_path}, 编码: {encoding}, 追加: {append}")
        return self.data_io.write_text_file(file_path, content, encoding, append)
    
    @keyword(name='读取 JSON 文件', tags=['数据IO'])
    def read_json_file(self, file_path, encoding='utf-8'):
        """读取JSON文件
        
        读取指定路径的JSON文件内容
        
        参数:
            file_path: 文件路径
            encoding: 文件编码，默认为utf-8
        
        返回:
            JSON数据
        
        示例:
            | ${data} | 读取 JSON 文件 | C:/test.json |
        """
        logger.info(f"读取JSON文件: {file_path}, 编码: {encoding}")
        return self.data_io.read_json_file(file_path, encoding)
    
    @keyword(name='写入 JSON 文件', tags=['数据IO'])
    def write_json_file(self, file_path, data, encoding='utf-8', indent=4):
        """写入JSON文件
        
        向指定路径的JSON文件写入内容
        
        参数:
            file_path: 文件路径
            data: 要写入的数据
            encoding: 文件编码，默认为utf-8
            indent: 缩进空格数，默认为4
        
        示例:
            | 写入 JSON 文件 | C:/test.json | ${data} | 缩进=2 |
        """
        logger.info(f"写入JSON文件: {file_path}, 编码: {encoding}, 缩进: {indent}")
        return self.data_io.write_json_file(file_path, data, encoding, indent)
    
    @keyword(name='读取 CSV 文件', tags=['数据IO'])
    def read_csv_file(self, file_path, encoding='utf-8', delimiter=',', header=True):
        """读取CSV文件
        
        读取指定路径的CSV文件内容
        
        参数:
            file_path: 文件路径
            encoding: 文件编码，默认为utf-8
            delimiter: 分隔符，默认为逗号
            header: 是否包含表头，默认为True
        
        返回:
            CSV数据
        
        示例:
            | ${data} | 读取 CSV 文件 | C:/test.csv |
            | ${data} | 读取 CSV 文件 | C:/test.csv | 分隔符=; | 表头=False |
        """
        logger.info(f"读取CSV文件: {file_path}, 编码: {encoding}, 分隔符: {delimiter}, 表头: {header}")
        return self.data_io.read_csv_file(file_path, encoding, delimiter, header)
    
    @keyword(name='写入 CSV 文件', tags=['数据IO'])
    def write_csv_file(self, file_path, data, encoding='utf-8', delimiter=',', header=True):
        """写入CSV文件
        
        向指定路径的CSV文件写入内容
        
        参数:
            file_path: 文件路径
            data: 要写入的数据
            encoding: 文件编码，默认为utf-8
            delimiter: 分隔符，默认为逗号
            header: 是否包含表头，默认为True
        
        示例:
            | 写入 CSV 文件 | C:/test.csv | ${data} | 分隔符=; |
        """
        logger.info(f"写入CSV文件: {file_path}, 编码: {encoding}, 分隔符: {delimiter}, 表头: {header}")
        return self.data_io.write_csv_file(file_path, data, encoding, delimiter, header)
    
    @keyword(name='读取 Excel 文件', tags=['数据IO'])
    def read_excel_file(self, file_path, sheet_name=None, row_limit=None, col_limit=None):
        """读取Excel文件
        
        读取指定路径的Excel文件内容
        
        参数:
            file_path: 文件路径
            sheet_name: 工作表名称，如果为None则读取第一个工作表
            row_limit: 读取的最大行数
            col_limit: 读取的最大列数
        
        返回:
            Excel数据
        
        示例:
            | ${data} | 读取 Excel 文件 | C:/test.xlsx |
            | ${data} | 读取 Excel 文件 | C:/test.xlsx | 工作表名=Sheet2 | 行限制=10 |
        """
        logger.info(f"读取Excel文件: {file_path}, 工作表名: {sheet_name}, 行限制: {row_limit}, 列限制: {col_limit}")
        return self.data_io.read_excel_file(file_path, sheet_name, row_limit, col_limit)
    
    @keyword(name='写入 Excel 文件', tags=['数据IO'])
    def write_excel_file(self, file_path, data, sheet_name='Sheet1', append=False):
        """写入Excel文件
        
        向指定路径的Excel文件写入内容
        
        参数:
            file_path: 文件路径
            data: 要写入的数据
            sheet_name: 工作表名称，默认为Sheet1
            append: 是否追加写入，默认为False（覆盖写入）
        
        示例:
            | 写入 Excel 文件 | C:/test.xlsx | ${data} | 工作表名=Sheet2 |
            | 写入 Excel 文件 | C:/test.xlsx | ${data} | 追加=True |
        """
        logger.info(f"写入Excel文件: {file_path}, 工作表名: {sheet_name}, 追加: {append}")
        return self.data_io.write_excel_file(file_path, data, sheet_name, append)
