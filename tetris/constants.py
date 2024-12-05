# 颜色定义
COLORS = {
    'I': (0, 240, 240),  # 青色
    'O': (240, 240, 0),  # 黄色
    'T': (160, 0, 240),  # 紫色
    'L': (240, 160, 0),  # 橙色
    'J': (0, 0, 240),    # 蓝色
    'S': (0, 240, 0),    # 绿色
    'Z': (240, 0, 0)     # 红色
}

# 游戏配置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)  # 增加宽度，为右侧信息区域留出空间
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 游戏速度（越小越快）
INITIAL_SPEED = 1000  # 毫秒 