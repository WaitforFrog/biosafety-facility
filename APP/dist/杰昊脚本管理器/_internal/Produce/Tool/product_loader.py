"""
产品参数加载工具
"""
import os


def load_product_parameters(parameters_dir):
    """加载产品参数文件"""
    products_data = {}
    if not os.path.exists(parameters_dir):
        print(f"参数文件夹不存在: {parameters_dir}")
        return products_data

    for filename in os.listdir(parameters_dir):
        if filename.endswith('.md'):
            product_name = filename[:-3]
            file_path = os.path.join(parameters_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    products_data[product_name] = f.read().strip()
                    print(f"  已加载产品参数: {product_name}")
            except Exception as e:
                print(f"  读取文件失败 {filename}: {e}")
    return products_data
