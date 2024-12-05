import pygame
import sys
import time
import os
from .tetromino import Tetromino
from .constants import *
from .score_manager import ScoreManager

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        
        self.clock = pygame.time.Clock()
        self.grid = [[None] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score_manager = ScoreManager()
        self.score = 0
        self.game_over = False
        self.fall_time = time.time()
        self.fall_speed = INITIAL_SPEED
        self.show_instructions = True  # 添加游戏说明标志
        self.move_delay = 100  # 添加移动延迟时间（毫秒）
        self.last_move_time = 0  # 记录上次移动时间
        
        # 尝试使用系统自带的中文字体
        try:
            self.font = pygame.font.SysFont("simhei", 24)  # 尝试使用黑体
        except:
            try:
                self.font = pygame.font.SysFont("microsoft yahei", 24)  # 尝试使用微软雅黑
            except:
                try:
                    self.font = pygame.font.SysFont("simsun", 24)  # 尝试使用宋体
                except:
                    self.font = pygame.font.Font(None, 24)  # 如果都失败了，使用默认字体

    def draw_instructions(self):
        instructions = [
            "游戏操作说明：",
            "←→ 方向键：左右移动方块",
            "↓ 方向键：长按加速下落",
            "↑ 方向键：旋转方块",
            "R 键：重新开始游戏",
            "",
            "按任意键开始游戏"
        ]
        
        y = SCREEN_HEIGHT // 3
        for line in instructions:
            try:
                text = self.font.render(line, True, (255, 255, 255), (0, 0, 0))  # 添加黑色背景
            except:
                # 如果渲染失败，尝试使用 UTF-8 编码
                text = self.font.render(line.encode('utf-8').decode('utf-8'), True, (255, 255, 255), (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 40

    def check_collision(self, x_offset=0, y_offset=0, rotated_shape=None):
        shape_to_check = rotated_shape if rotated_shape else self.current_piece.shape
        for y, row in enumerate(shape_to_check):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece.x + x + x_offset
                    new_y = self.current_piece.y + y + y_offset
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def move_piece(self, dx):
        if not self.check_collision(x_offset=dx):
            self.current_piece.x += dx

    def move_piece_down(self):
        if not self.check_collision(y_offset=1):
            self.current_piece.y += 1
            return True
        self.lock_piece()
        return False

    def rotate_piece(self):
        # 保存当前形状
        original_shape = self.current_piece.shape
        # 尝试旋转
        self.current_piece.rotate()
        # 如果旋转后发生碰撞，恢复原来的形状
        if self.check_collision():
            self.current_piece.shape = original_shape

    def lock_piece(self):
        # 检查是否碰到顶部
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece.y + y
                    if grid_y <= 0:  # 修改判定条件，只要有方块在顶部或以上就结束
                        self.game_over = True
                        return
                    self.grid[grid_y][self.current_piece.x + x] = self.current_piece.color
        
        if not self.game_over:
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell for cell in self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [None] * GRID_WIDTH)
            else:
                y -= 1
        
        if lines_cleared:
            points = [0, 100, 300, 500, 800][lines_cleared]
            self.score += points
            self.score_manager.save_high_score(self.score)
            self.fall_speed = max(100, INITIAL_SPEED - (self.score // 1000) * 100)

    def update(self):
        # 如果在显示说明或游戏结束时，不更新游戏状态
        if self.show_instructions or self.game_over:
            return
        
        current_time = time.time()
        if current_time - self.fall_time > self.fall_speed / 1000:
            self.move_piece_down()
            self.fall_time = current_time

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(self.screen, color,
                                   (x * BLOCK_SIZE, y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece.color,
                                   ((piece.x + x + offset_x) * BLOCK_SIZE,
                                    (piece.y + y + offset_y) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if self.show_instructions:
            self.draw_instructions()
            pygame.display.flip()
            return

        # 绘制网格线
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, (50, 50, 50),
                           (x * BLOCK_SIZE, 0),
                           (x * BLOCK_SIZE, SCREEN_HEIGHT))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, (50, 50, 50),
                           (0, y * BLOCK_SIZE),
                           (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))
        
        # 绘制已落下的方块
        self.draw_grid()
        
        # 绘制当前方块
        self.draw_piece(self.current_piece)
        
        # 绘制右侧信息区域
        info_x = GRID_WIDTH * BLOCK_SIZE + 20
        
        # 绘制分数
        try:
            score_text = self.font.render(f'当前分数: {self.score}', True, (255, 255, 255), (0, 0, 0))
            high_score_text = self.font.render(f'最高分数: {self.score_manager.high_score}', True, (255, 255, 255), (0, 0, 0))
            next_text = self.font.render('下一个:', True, (255, 255, 255), (0, 0, 0))
        except:
            # 如果渲染失败，尝试使用 UTF-8 编码
            score_text = self.font.render(f'当前分数: {self.score}'.encode('utf-8').decode('utf-8'), True, (255, 255, 255), (0, 0, 0))
            high_score_text = self.font.render(f'最高分数: {self.score_manager.high_score}'.encode('utf-8').decode('utf-8'), True, (255, 255, 255), (0, 0, 0))
            next_text = self.font.render('下一个:'.encode('utf-8').decode('utf-8'), True, (255, 255, 255), (0, 0, 0))
        
        self.screen.blit(score_text, (info_x, 10))
        self.screen.blit(high_score_text, (info_x, 40))
        self.screen.blit(next_text, (info_x, 90))
        
        # 调整预方块的位置
        preview_x = info_x + 30
        preview_y = 130
        
        # 临时保存下一个方块的位置
        original_x = self.next_piece.x
        original_y = self.next_piece.y
        
        # 将下一个方块移动到预览区域
        self.next_piece.x = preview_x // BLOCK_SIZE
        self.next_piece.y = preview_y // BLOCK_SIZE
        
        # 绘制预览方块
        self.draw_piece(self.next_piece)
        
        # 恢复下一个方块的原始位置
        self.next_piece.x = original_x
        self.next_piece.y = original_y
        
        if self.game_over:
            # 绘制半透明的黑色遮罩
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # 绘制游戏结束信息
            try:
                game_over_text = self.font.render('游戏结束', True, (255, 0, 0))
                score_text = self.font.render(f'最终分数: {self.score}', True, (255, 255, 255))
                restart_text = self.font.render('按←键重新开始', True, (255, 255, 255))
                quit_text = self.font.render('按→键退出游戏', True, (255, 255, 255))
            except:
                # 如果渲染失败，尝试使用 UTF-8 编码
                game_over_text = self.font.render('游戏结束'.encode('utf-8').decode('utf-8'), True, (255, 0, 0))
                score_text = self.font.render(f'最终分数: {self.score}'.encode('utf-8').decode('utf-8'), True, (255, 255, 255))
                restart_text = self.font.render('按←键重新开始'.encode('utf-8').decode('utf-8'), True, (255, 255, 255))
                quit_text = self.font.render('按→键退出游戏'.encode('utf-8').decode('utf-8'), True, (255, 255, 255))
            
            center_y = SCREEN_HEIGHT // 2 - 60
            for text in [game_over_text, score_text, restart_text, quit_text]:
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, center_y))
                self.screen.blit(text, text_rect)
                center_y += 40

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.show_instructions:
                    self.show_instructions = False
                    return
                
                if self.game_over:
                    if event.key == pygame.K_LEFT:  # 按左键重新开始
                        self.game_reset()
                    elif event.key == pygame.K_RIGHT:  # 按右键退出
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_r:  # 游戏进行中按R重新开始
                    self.game_reset()
                elif event.key == pygame.K_UP:
                    self.rotate_piece()

        # 只有在游戏没有结束且不在显示说明时才处理移动控制
        if not (self.game_over or self.show_instructions):
            keys = pygame.key.get_pressed()
            
            # 添加移动延迟，使移动更加平滑
            if current_time - self.last_move_time > self.move_delay:
                moved = False
                if keys[pygame.K_LEFT]:
                    self.move_piece(-1)
                    moved = True
                if keys[pygame.K_RIGHT]:
                    self.move_piece(1)
                    moved = True
                if moved:
                    self.last_move_time = current_time
            
            # 下落键不需要延迟
            if keys[pygame.K_DOWN]:
                self.move_piece_down()

    def game_reset(self):
        """重置游戏状态"""
        self.grid = [[None] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.game_over = False
        self.fall_time = time.time()
        self.fall_speed = INITIAL_SPEED
        self.score_manager.save_high_score(self.score)
