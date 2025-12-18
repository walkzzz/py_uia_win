# 简单测试脚本，验证重构后的库能否正常导入和使用

from rf_win import RFWin

def test_library_import():
    """测试库能否正常导入"""
    print("Testing library import...")
    
    # 创建库实例
    library = RFWin()
    print("✓ Library instance created successfully")
    
    # 检查关键字是否存在
    assert hasattr(library, "start_application"), "start_application keyword not found"
    assert hasattr(library, "connect_application"), "connect_application keyword not found"
    assert hasattr(library, "close_application"), "close_application keyword not found"
    assert hasattr(library, "get_current_application"), "get_current_application keyword not found"
    assert hasattr(library, "switch_application"), "switch_application keyword not found"
    assert hasattr(library, "is_application_running"), "is_application_running keyword not found"
    
    print("✓ All keywords found successfully")
    print("✓ Library import test passed!")
    return True

if __name__ == "__main__":
    test_library_import()
