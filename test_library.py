# 简单测试脚本，验证重构后的库能否正常导入和使用

from rf_win import RFWinLibrary

def test_library_import():
    """测试库能否正常导入"""
    print("Testing library import...")
    
    # 创建库实例
    library = RFWinLibrary()
    print("✓ Library instance created successfully")
    
    # 检查关键字是否存在
    assert hasattr(library, "start_application"), "start_application keyword not found"
    assert hasattr(library, "attach_to_application"), "attach_to_application keyword not found"
    assert hasattr(library, "close_application"), "close_application keyword not found"
    assert hasattr(library, "get_main_window"), "get_main_window keyword not found"
    assert hasattr(library, "locate_window"), "locate_window keyword not found"
    assert hasattr(library, "activate_window"), "activate_window keyword not found"
    assert hasattr(library, "find_element"), "find_element keyword not found"
    assert hasattr(library, "click_element"), "click_element keyword not found"
    assert hasattr(library, "type_text"), "type_text keyword not found"
    assert hasattr(library, "capture_screenshot"), "capture_screenshot keyword not found"
    
    print("✓ All keywords found successfully")
    print("✓ Library import test passed!")
    return True

if __name__ == "__main__":
    test_library_import()
