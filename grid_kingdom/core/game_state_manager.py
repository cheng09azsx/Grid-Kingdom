# /grid_kingdom/core/game_state_manager.py
"""
游戏状态管理器
负责管理不同的游戏状态（场景）及其切换。
"""
import pygame # 确保 pygame 在文件顶部导入
from typing import Optional, Dict, Type, List, Tuple

from grid_kingdom.utils.logger import logger
from grid_kingdom.utils import constants as C
from grid_kingdom.game_objects.tile import Tile
from grid_kingdom.ui.renderer import Renderer # 导入渲染器
from grid_kingdom.systems.resource_system import ResourceSystem, ResourceType
from grid_kingdom.game_objects.building import Building, ManaWell, WoodcutterHut # 导入建筑类
from grid_kingdom.systems.turn_system import TurnSystem
from grid_kingdom.ui.components.button import Button

class BaseState:
    """
    游戏状态的基类。
    所有具体状态（如开始菜单、游戏主场景）都应继承此类。
    """
    def __init__(self, manager: 'GameStateManager'):
        self.manager = manager
        logger.info(f"State '{self.__class__.__name__}' initialized.")

    def handle_event(self, event) -> None:
        """处理输入事件。"""
        pass

    def update(self, dt: float) -> None:
        """更新游戏逻辑，dt是自上一帧以来的时间（秒）。"""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """将当前状态渲染到屏幕上。"""
        pass

    def on_enter(self, **kwargs) -> None:
        """当进入此状态时调用。kwargs可以传递参数。"""
        logger.info(f"Entering state '{self.__class__.__name__}' with args: {kwargs}")

    def on_exit(self) -> None:
        """当退出此状态时调用。"""
        logger.info(f"Exiting state '{self.__class__.__name__}'.")


class GameStateManager:
    """
    管理游戏状态的切换。
    """
    def __init__(self):
        self.states: Dict[str, Type[BaseState]] = {} # 存储状态类，而不是实例
        self.active_state: Optional[BaseState] = None
        self.active_state_name: Optional[str] = None
        logger.info("GameStateManager initialized.")

    def register_state(self, name: str, state_class: Type[BaseState]) -> None:
        """
        注册一个状态类。
        在实际切换到该状态前，不会实例化。
        """
        if name in self.states:
            logger.warning(f"State '{name}' already registered. Overwriting with {state_class.__name__}.")
        self.states[name] = state_class
        logger.info(f"State class '{state_class.__name__}' registered as '{name}'.")

    def change_state(self, name: str, **kwargs) -> None:
        logger.debug(f"Attempting to change state to '{name}' with kwargs: {kwargs}")
        if self.active_state:
            logger.debug(f"Exiting current state: {self.active_state_name}")
            self.active_state.on_exit()

        if name not in self.states:
            logger.error(f"State '{name}' not registered.")
            return

        state_class_definition = self.states[name]
        logger.debug(f"Found state definition for '{name}': {state_class_definition}")

        new_state_instance = None
        try:
            if callable(state_class_definition): # 应该总是True，因为我们存的是类
                logger.debug(f"Instantiating state '{name}' using callable: {state_class_definition}")
                new_state_instance = state_class_definition(self) # 传入 GameStateManager 实例
                logger.debug(f"Successfully instantiated '{name}': {new_state_instance}")
            else:
                # 这个分支理论上不应该执行，因为 register_state 强制了 Type[BaseState]
                logger.error(f"State definition for '{name}' is not callable: {state_class_definition}")
                self.active_state = None 
                return
        except Exception as e:
            logger.critical(f"Error instantiating state '{name}' from {state_class_definition}: {e}", exc_info=True)
            self.active_state = None
            return

        if not isinstance(new_state_instance, BaseState):
            logger.error(f"Instantiated object for state '{name}' is not a BaseState subclass: {type(new_state_instance)}")
            self.active_state = None
            return

        self.active_state = new_state_instance
        self.active_state_name = name
        logger.info(f"Successfully changed active state to '{self.active_state_name}' (instance: {self.active_state}).")

        try:
            if self.active_state:
                self.active_state.on_enter(**kwargs)
        except Exception as e:
            logger.critical(f"Error during on_enter for state '{self.active_state_name}': {e}", exc_info=True)

    def get_active_state(self) -> Optional[BaseState]:
        return self.active_state

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.active_state:
            self.active_state.handle_event(event)

    def update(self, dt: float) -> None:
        if self.active_state:
            self.active_state.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if self.active_state:
            self.active_state.render(surface)
        else:
            surface.fill((50, 50, 50)) 
            if not pygame.font.get_init(): pygame.font.init()
            try:
                font = pygame.font.SysFont("arial", 24)
                text_surface = font.render("No active state.", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
                surface.blit(text_surface, text_rect)
            except Exception as e:
                logger.error(f"Error rendering no active state message: {e}")


# --- 示例状态 (开始菜单) ---
class PlaceholderState(BaseState):
    """一个占位符状态，用于演示开始菜单。"""
    def __init__(self, manager: GameStateManager, color: tuple = (100, 100, 200), text: str = "Placeholder State"):
        super().__init__(manager)
        self.color = color
        self.text = text
        self.font: Optional[pygame.font.Font] = None

    def on_enter(self, **kwargs) -> None:
        super().on_enter(**kwargs)
        if not pygame.font.get_init(): # 直接使用顶部的 pygame
            pygame.font.init()
        try:
            self.font = pygame.font.SysFont("arial", 48)
        except Exception as e:
            logger.error(f"Failed to load font in PlaceholderState: {e}")

        if 'message' in kwargs:
            self.text = kwargs['message']
            logger.info(f"PlaceholderState received message: {self.text}")

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                logger.info(f"Space pressed in {self.__class__.__name__}. Triggering state change.")
                # 根据当前文本内容决定切换到哪个状态
                if "Start Screen" in self.text: # 简单判断
                    self.manager.change_state("game_main", difficulty="normal")
                else: # 其他情况都返回开始菜单（或特定逻辑）
                     self.manager.change_state("start_menu", message="Welcome Back to Start Screen!")

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        surface.fill(self.color)
        if self.font:
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(text_surface, text_rect)


# --- 主游戏场景状态 ---
class GameMainState(BaseState):
    """
    主游戏场景的状态。
    负责处理游戏核心逻辑的更新和渲染，如网格、建筑、资源等。
    """
    def __init__(self, manager: GameStateManager):
        super().__init__(manager)
        self.renderer: Optional[Renderer] = None
        self.tiles: List[List[Tile]] = []
        self.grid_width_tiles: int = 20
        self.grid_height_tiles: int = 15
        self.tile_size: int = 32
        
        self.font_debug: Optional[pygame.font.Font] = None # 用于调试信息
        self.font_ui_small: Optional[pygame.font.Font] = None # 用于资源、回合等小文本
        self.font_ui_button: Optional[pygame.font.Font] = None # 用于按钮文本
        
        self.hovered_tile: Optional[Tile] = None
        
        initial_player_resources = {
            ResourceType.WOOD: 100, ResourceType.STONE: 50, ResourceType.FOOD: 20,
            ResourceType.GOLD: 0, ResourceType.MANA: 0
        }
        
        self.resource_system = ResourceSystem(initial_resources=initial_player_resources)
        self.resource_system.set_resource_cap(ResourceType.WOOD, 500)
        self.resource_system.set_resource_cap(ResourceType.STONE, 300)
        self.resource_system.set_resource_cap(ResourceType.FOOD, 100)
        
        self.turn_system = TurnSystem(resource_system=self.resource_system, initial_turn=1)
        self.turn_system.register_on_turn_end_callback(self._process_buildings_turn_logic)
        
        self.buildings: List[Building] = []  
        self.available_buildings_to_build: List[Type[Building]] = [WoodcutterHut, ManaWell]
        self.selected_building_type_to_build: Optional[Type[Building]] = None
        self.build_mode: bool = False
        self.placement_valid: bool = False       
        
        self.next_turn_button: Optional[Button] = None
        self.building_selection_buttons: List[Button] = []     

    def _load_font(self, font_path: str, size: int) -> Optional[pygame.font.Font]:
        """尝试加载指定路径的字体，如果失败则尝试备用系统字体。"""
        try:
            return pygame.font.Font(font_path, size)
        except pygame.error as e: # Pygame相关的错误，如字体文件找不到
            logger.error(f"Failed to load font from path '{font_path}' (size {size}): {e}")
            try:
                logger.warning(f"Attempting to load fallback system font '{C.FALLBACK_FONT_NAME}' (size {size}). May not support Chinese.")
                return pygame.font.SysFont(C.FALLBACK_FONT_NAME, size)
            except Exception as sys_e:
                logger.critical(f"Failed to load fallback system font '{C.FALLBACK_FONT_NAME}': {sys_e}")
                return None # 彻底失败
        except Exception as e_gen: # 其他未知错误
            logger.critical(f"An unexpected error occurred while loading font '{font_path}': {e_gen}")
            return None

    def on_enter(self, **kwargs) -> None:
        super().on_enter(**kwargs)
        engine_instance = getattr(self.manager, 'engine_ref', None) 
        screen_width_for_ui, screen_height_for_ui = C.SCREEN_WIDTH, C.SCREEN_HEIGHT
        if engine_instance and hasattr(engine_instance, 'screen'):
            screen_surface = engine_instance.screen
            self.renderer = Renderer(screen_surface.get_width(), screen_surface.get_height())
            screen_width_for_ui = screen_surface.get_width()
            screen_height_for_ui = screen_surface.get_height()
            logger.info("GameMainState: Renderer initialized using engine's screen dimensions.")
        else:
            self.renderer = Renderer(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
            logger.warning("GameMainState: Renderer initialized using constant screen dimensions.")
        
        self._initialize_grid()
        
        if not pygame.font.get_init(): pygame.font.init()
        
        # 加载字体
        self.font_debug = self._load_font(C.DEFAULT_FONT_PATH, 20) # 调试信息用小一点的字
        self.font_ui_small = self._load_font(C.DEFAULT_FONT_PATH, 18) # UI小文本
        self.font_ui_button = self._load_font(C.DEFAULT_FONT_PATH, 20) # 按钮文本
        if not all([self.font_debug, self.font_ui_small, self.font_ui_button]):
            logger.error("One or more fonts failed to load. UI text might not render correctly or at all.")
        self._setup_ui_elements(screen_width_for_ui, screen_height_for_ui)
        logger.info(f"GameMainState entered. Grid: {self.grid_width_tiles}x{self.grid_height_tiles}, TileSize: {self.tile_size}")
        logger.info(f"Initial resources: {self.resource_system.get_all_resources_str()}")
        logger.info(f"Current Turn: {self.turn_system.current_turn}")
        self._create_initial_building_for_test()

    def _setup_ui_elements(self, screen_width: int, screen_height: int) -> None:
        """初始化和设置UI元素，如按钮。"""
        if self.font_ui_button:
            # 结束回合按钮
            btn_end_turn_width = 160 # 增加宽度以容纳中文
            btn_end_turn_height = 40
            btn_end_turn_x = screen_width - btn_end_turn_width - 20
            btn_end_turn_y = screen_height - btn_end_turn_height - 10 # 底部UI条的Y位置
            
            self.next_turn_button = Button(
                rect=pygame.Rect(btn_end_turn_x, btn_end_turn_y, btn_end_turn_width, btn_end_turn_height),
                text=f"{C.TEXT_END_TURN_BUTTON} ({self.turn_system.current_turn})",
                font=self.font_ui_button,
                on_click=self.turn_system.advance_turn,
                bg_color=C.COLOR_DARK_GREY,
                hover_bg_color=C.COLOR_GREY
            )
            logger.info("Next Turn button created.")
            # 建筑选择按钮
            self.building_selection_buttons.clear()
            build_btn_start_x = 20
            build_btn_width = 120 # 调整宽度
            build_btn_height = 30
            build_btn_padding = 10
            # 建筑选择按钮放在底部UI条
            build_btn_y = screen_height - build_btn_height - ( (50 - build_btn_height) // 2 ) - 5 # 50是底部条高度
            for i, building_class in enumerate(self.available_buildings_to_build):
                # 动态获取建筑的中文名 (假设建筑类有 'CHINESE_NAME' 类属性，或者从其他地方获取)
                # 为简单起见，我们暂时硬编码或用一个辅助函数
                building_display_name = getattr(building_class, "CHINESE_NAME", building_class.__name__)
                button = Button(
                    rect=pygame.Rect(build_btn_start_x + i * (build_btn_width + build_btn_padding), 
                                    build_btn_y, build_btn_width, build_btn_height),
                    text=f"[{i+1}] {building_display_name}",
                    font=self.font_ui_button, # 使用按钮字体
                    on_click=lambda bc=building_class: self._select_building_to_build(bc), # 使用lambda传递参数
                    bg_color=C.COLOR_DARK_GREY,
                    hover_bg_color=C.COLOR_GREY
                )
                self.building_selection_buttons.append(button)
            logger.info(f"{len(self.building_selection_buttons)} building selection buttons created.")
        else:
            logger.error("Cannot create UI buttons, UI font not loaded.")
    
    def _select_building_to_build(self, building_class: Type[Building]):
        """处理建筑选择按钮的点击事件。"""
        self.selected_building_type_to_build = building_class
        self.build_mode = True
        # 获取建筑中文名用于日志
        building_display_name = getattr(building_class, "CHINESE_NAME", building_class.__name__)
        logger.info(f"已选择建筑: {building_display_name}. 进入建筑模式.")


    def _create_initial_building_for_test(self):
        test_building_x, test_building_y = 5, 5
        if 0 <= test_building_x < self.grid_width_tiles and \
           0 <= test_building_y < self.grid_height_tiles and \
           not self.tiles[test_building_y][test_building_x].is_occupied:
            
            new_hut = WoodcutterHut(test_building_x, test_building_y, self.tile_size)
            if self.resource_system.spend_multiple_resources(new_hut.build_cost):
                self.buildings.append(new_hut)
                for occ_x, occ_y in new_hut.get_occupied_tiles():
                    self.tiles[occ_y][occ_x].set_occupied(new_hut.id)
                    self.tiles[occ_y][occ_x].set_type(new_hut.building_type)
                logger.info(f"Test building {new_hut.name} created at ({test_building_x},{test_building_y}).")
            else:
                logger.warning(f"Could not afford test building {new_hut.name}. Cost: {new_hut.build_cost}")
        else:
            logger.warning(f"Cannot place test building at ({test_building_x},{test_building_y}), tile might be invalid or occupied.")

    def _initialize_grid(self) -> None:
        logger.info("--- Grid Initialization Started ---")
        self.tiles = [] 
        logger.debug(f"Initializing grid with {self.grid_height_tiles} rows, {self.grid_width_tiles} cols, tile size {self.tile_size}")
        for y_coord in range(self.grid_height_tiles):
            row: List[Tile] = []
            for x_coord in range(self.grid_width_tiles):
                # import random # 如果 random 只在这里用，可以放进来，否则放模块顶部
                tile_type = "empty"
                rand_val = pygame.math.Vector2(x_coord, y_coord).length() * 0.05 # 伪随机，基于坐标
                # 或者使用 random 模块
                import random
                rand_val = random.random()

                if rand_val < 0.2: tile_type = "water"
                elif rand_val < 0.4: tile_type = "grass"
                row.append(Tile(x_coord, y_coord, self.tile_size, tile_type=tile_type))
            self.tiles.append(row)
        
        if self.tiles and self.tiles[0]:
            logger.info(f"Grid re-initialized. Example new tile [0][0] type: {self.tiles[0][0].tile_type}")
        else:
            logger.warning("Grid re-initialization resulted in empty tiles list.")
        logger.info("--- Grid Initialization Finished ---") 

    def _get_tile_at_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Tile]:
        if not self.renderer: return None
        world_x = mouse_pos[0] + self.renderer.camera_offset_x
        world_y = mouse_pos[1]+ self.renderer.camera_offset_y
        grid_x = world_x // self.tile_size
        grid_y = world_y // self.tile_size
        if 0 <= grid_x < self.grid_width_tiles and 0 <= grid_y < self.grid_height_tiles:
            try:
                return self.tiles[grid_y][grid_x]
            except IndexError:
                logger.warning(f"IndexError in _get_tile_at_mouse_pos for grid ({grid_x},{grid_y}).")
                return None
        return None

    def _can_place_building_at(self, building_class: Type[Building], grid_x: int, grid_y: int) -> bool:
        if not (0 <= grid_x < self.grid_width_tiles and 0 <= grid_y < self.grid_height_tiles):
            return False
        target_tile = self.tiles[grid_y][grid_x]
        if target_tile.is_occupied:
            return False
        return True

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        mouse_pos = pygame.mouse.get_pos()
        # 事件传递给所有按钮
        if self.next_turn_button: self.next_turn_button.handle_event(event)
        for btn in self.building_selection_buttons: btn.handle_event(event)
        
        # 检查是否有按钮处理了点击，避免后续逻辑冲突
        # 注意：Button 的 on_click 在 MOUSEBUTTONUP 时触发，所以这里我们主要避免在按钮区域的 MOUSEDOWN 触发地块逻辑
        clicked_on_a_button = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.next_turn_button and self.next_turn_button.rect.collidepoint(mouse_pos):
                clicked_on_a_button = True
            if not clicked_on_a_button:
                for btn in self.building_selection_buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        clicked_on_a_button = True
                        break
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.build_mode:
                    self.build_mode = False
                    self.selected_building_type_to_build = None
                    logger.info("建筑模式已取消.")
                else:
                    self.manager.change_state("start_menu", message="已返回开始菜单!")
            elif event.key == pygame.K_r: 
                logger.info("按下 R 键. 重新初始化网格和建筑.")
                self._initialize_grid()
                self.buildings.clear() 
                self._create_initial_building_for_test() 
            # 移除通过数字键1,2选择建筑的逻辑，现在通过按钮点击
            #elif event.key == pygame.K_n: # 移除N键回合，由按钮控制
            #    self.turn_system.advance_turn() # 改为由按钮的on_click调用
        if event.type == pygame.MOUSEMOTION:
            self.hovered_tile = self._get_tile_at_mouse_pos(mouse_pos)
            if self.build_mode and self.selected_building_type_to_build and self.hovered_tile:
                self.placement_valid = self._can_place_building_at(
                    self.selected_building_type_to_build,
                    self.hovered_tile.grid_x,
                    self.hovered_tile.grid_y
                )
            else:
                self.placement_valid = False
        if event.type == pygame.MOUSEBUTTONDOWN and not clicked_on_a_button: # 只有当没点到按钮时
            clicked_tile = self._get_tile_at_mouse_pos(mouse_pos)
            if event.button == 1: # Left-click
                if self.build_mode and self.selected_building_type_to_build and clicked_tile:
                    if self.placement_valid:
                        building_class = self.selected_building_type_to_build
                        # 获取建筑中文名
                        building_display_name = getattr(building_class, "CHINESE_NAME", building_class.__name__)
                        temp_building_for_cost = building_class(clicked_tile.grid_x, clicked_tile.grid_y, self.tile_size)
                        
                        if self.resource_system.spend_multiple_resources(temp_building_for_cost.build_cost):
                            new_building = building_class(clicked_tile.grid_x, clicked_tile.grid_y, self.tile_size)
                            self.buildings.append(new_building)
                            for occ_x, occ_y in new_building.get_occupied_tiles():
                                self.tiles[occ_y][occ_x].set_occupied(new_building.id)
                                self.tiles[occ_y][occ_x].set_type(new_building.building_type)
                            logger.info(f"成功建造 {new_building.name} 于 ({clicked_tile.grid_x},{clicked_tile.grid_y}).") # new_building.name 已经是中文
                            self.build_mode = False
                            self.selected_building_type_to_build = None
                        else:
                            logger.warning(f"建造 {building_display_name} 失败. 资源不足. 所需: {temp_building_for_cost.build_cost}")
                    else:
                        logger.warning("此处无法建造 (已被占据或无效位置).")
                elif clicked_tile: 
                    logger.info(f"点击地块: {clicked_tile} (非建筑模式).")
                    found_building_on_tile = next((b for b in self.buildings if (b.grid_x, b.grid_y) == (clicked_tile.grid_x, clicked_tile.grid_y)), None)
                    if found_building_on_tile:
                        logger.info(f"点击已有建筑: {found_building_on_tile.name}")
                        refund_ratio = 0.5
                        for res, amount in found_building_on_tile.build_cost.items():
                            self.resource_system.add_resource(res, int(amount * refund_ratio))
                        self.buildings.remove(found_building_on_tile)
                        for occ_x, occ_y in found_building_on_tile.get_occupied_tiles():
                            self.tiles[occ_y][occ_x].set_vacant()
                            self.tiles[occ_y][occ_x].set_type("empty")
                        logger.info(f"已拆除 {found_building_on_tile.name}. 部分资源已返还.")
                else:
                    logger.info("左键点击网格外部.")
            elif event.button == 3: # Right-click
                if self.build_mode:
                    self.build_mode = False
                    self.selected_building_type_to_build = None
                    logger.info("建筑模式已通过右键取消.")


    def _process_buildings_turn_logic(self): # 重命名以区分于TurnSystem的全局处理
        """处理本回合所有建筑的生产和维护。这是注册到TurnSystem的回调。"""
        logger.debug("--- GameMainState: Processing buildings turn logic ---")
        produced_this_turn: Dict[ResourceType, int] = {}
        for building in list(self.buildings): 
            if building.is_active:
                produced = building.update_production()
                if produced:
                    for res_type, amount in produced.items():
                        self.resource_system.add_resource(res_type, amount)
                        produced_this_turn[res_type] = produced_this_turn.get(res_type, 0) + amount
        if produced_this_turn: logger.info(f"Total building production this turn: {produced_this_turn}")
        
        for building in self.buildings: building.pay_maintenance(self.resource_system)
        logger.debug("--- GameMainState: Buildings turn logic processed ---")
        # 全局资源消耗现在由 TurnSystem._process_global_turn_effects 处理
    

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.next_turn_button: # 更新结束回合按钮文本
            self.next_turn_button.set_text(f"{C.TEXT_END_TURN_BUTTON} ({self.turn_system.current_turn})")
        
        # 更新建筑选择按钮的状态 (例如，高亮当前选中的)
        for btn in self.building_selection_buttons:
            # 假设按钮的文本格式是 "[key] Name"
            # 我们需要从按钮的on_click回调中绑定的建筑类来判断
            # 这部分可以在 Button 类中增加一个 id 或 data 属性来简化
            # 或者在创建按钮时就保存其对应的建筑类
            # 简陋的判断：
            # is_selected_button = False
            # if self.selected_building_type_to_build and btn.text.endswith(self.selected_building_type_to_build.CHINESE_NAME if hasattr(self.selected_building_type_to_build, "CHINESE_NAME") else self.selected_building_type_to_build.__name__):
            #    is_selected_button = True
            #
            # (更稳健的方式是在 _setup_ui_elements 中给按钮关联建筑类，然后在 Button 类中处理高亮)
            # 目前Button类没有直接支持基于外部状态的高亮，我们可以在这里手动改颜色，但不推荐
            # 最好是 Button 类有 set_highlighted(bool) 之类的方法
            pass

    def _draw_resource_ui(self, surface: pygame.Surface) -> None:
        if not self.font_ui_small: return
        start_x, y_pos, padding = 10, 10, 15
        
        resource_map = { # 将枚举映射到中文文本
            ResourceType.WOOD: C.TEXT_WOOD, ResourceType.STONE: C.TEXT_STONE,
            ResourceType.FOOD: C.TEXT_FOOD, ResourceType.GOLD: C.TEXT_GOLD,
            ResourceType.MANA: C.TEXT_MANA
        }
        resource_order = [ResourceType.WOOD, ResourceType.STONE, ResourceType.FOOD, ResourceType.GOLD, ResourceType.MANA]
        for res_type in resource_order:
            amount = self.resource_system.get_resource_amount(res_type)
            cap = self.resource_system.get_resource_cap(res_type)
            cap_str = f"/{cap}" if cap is not None else ""
            res_name = resource_map.get(res_type, res_type.name) # 获取中文名
            text = f"{res_name}: {amount}{cap_str}"
            text_surface = self.font_ui_small.render(text, True, C.COLOR_LIGHT_GREY)
            logger.debug(f"Rendered resource text '{text}': Surface={text_surface}, Size={text_surface.get_size() if text_surface else 'None'}")
            surface.blit(text_surface, (start_x, y_pos))
            start_x += text_surface.get_width() + padding
            
    def _draw_turn_info_ui(self, surface: pygame.Surface) -> None:
        if not self.font_ui_small: return 
        turn_text = f"{C.TEXT_TURN}: {self.turn_system.current_turn}"
        text_surface = self.font_ui_small.render(turn_text, True, C.COLOR_LIGHT_GREY)
        # 显示在资源区右侧
        resource_ui_end_x = 10 # 估算资源区宽度，或动态计算
        for res_type in [ResourceType.WOOD, ResourceType.STONE, ResourceType.FOOD, ResourceType.GOLD, ResourceType.MANA]:
            res_name = getattr(C, f"TEXT_{res_type.name}", res_type.name)
            amount = self.resource_system.get_resource_amount(res_type)
            cap = self.resource_system.get_resource_cap(res_type)
            cap_str = f"/{cap}" if cap is not None else ""
            text = f"{res_name}: {amount}{cap_str}"
            resource_ui_end_x += self.font_ui_small.size(text)[0] + 15
            
        text_rect = text_surface.get_rect(topleft=(resource_ui_end_x + 30, 10)) # 资源区右边30像素
        surface.blit(text_surface, text_rect)

    def _draw_build_preview(self, surface: pygame.Surface):
        """绘制建筑放置预览。"""
        if self.build_mode and self.selected_building_type_to_build and self.hovered_tile:
            preview_color = (0, 255, 0, 100) if self.placement_valid else (255, 0, 0, 100)
            
            preview_rect = pygame.Rect(
                self.hovered_tile.pixel_x - (self.renderer.camera_offset_x if self.renderer else 0),
                self.hovered_tile.pixel_y - (self.renderer.camera_offset_y if self.renderer else 0),
                self.tile_size,
                self.tile_size
            )
            temp_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            temp_surface.fill(preview_color)
            surface.blit(temp_surface, (preview_rect.x, preview_rect.y))
            
            # 可以在预览上显示建筑名称或图标
            if self.font_ui_small: # <--- 修改这里：使用 self.font_ui_small
                try:
                    # 尝试获取建筑类的中文名或普通名，然后取首字母
                    building_name_source = getattr(self.selected_building_type_to_build, "CHINESE_NAME", None)
                    if not building_name_source: # 如果没有CHINESE_NAME，尝试普通name
                        building_name_source = getattr(self.selected_building_type_to_build, "name", None)
                    if not building_name_source: # 如果连name都没有（不太可能），用类名
                        building_name_source = self.selected_building_type_to_build.__name__
                    
                    building_name_char = building_name_source[0] if building_name_source else "?"
                except (AttributeError, IndexError): # 捕获可能发生的错误
                    building_name_char = "?"
                    logger.warning(f"Could not determine preview char for {self.selected_building_type_to_build}")
                try:
                    text_s = self.font_ui_small.render(building_name_char, True, C.COLOR_WHITE) # <--- 修改这里
                    text_r = text_s.get_rect(center=preview_rect.center)
                    surface.blit(text_s, text_r)
                except pygame.error as e: # 防御字体渲染错误
                    logger.error(f"Error rendering build preview text char '{building_name_char}': {e}")
            elif not self.font_ui_small: # 如果字体未加载，记录一个警告
                logger.warning("_draw_build_preview: font_ui_small not loaded, cannot draw preview text.")


    def _draw_building_selection_ui(self, surface: pygame.Surface):
        """绘制底部的建筑选择UI条和按钮。"""
        if not self.font_ui_button: return
        ui_bar_height = 50
        ui_bar_y = surface.get_height() - ui_bar_height
        pygame.draw.rect(surface, C.COLOR_VERY_DARK_GREY, (0, ui_bar_y, surface.get_width(), ui_bar_height))
        for btn in self.building_selection_buttons:
            # 更新按钮高亮状态 (如果当前选中且在建筑模式)
            is_this_button_selected = False
            # 我们需要一种方式从按钮实例判断它代表哪个建筑类
            # 修改：在 _select_building_to_build 中直接设置按钮高亮，或按钮有active状态
            # 暂时简单处理，如果按钮的文本包含已选中建筑的名称，则高亮（不完美）
            if self.selected_building_type_to_build and self.build_mode:
                # 假设按钮文本是 "[key] Name"
                # 这需要确保按钮文本中的Name与建筑类的CHINESE_NAME一致
                expected_name_in_btn_text = getattr(self.selected_building_type_to_build, "CHINESE_NAME", self.selected_building_type_to_build.__name__)
                if expected_name_in_btn_text in btn.text: # 简单判断
                    btn.bg_color = C.COLOR_YELLOW # 用一个不同的高亮色
                    btn.hover_bg_color = C.COLOR_YELLOW
                else:
                    btn.bg_color = C.COLOR_DARK_GREY
                    btn.hover_bg_color = C.COLOR_GREY
            else: # 非建筑模式或无选中，所有按钮恢复默认色
                btn.bg_color = C.COLOR_DARK_GREY
                btn.hover_bg_color = C.COLOR_GREY
            btn.draw(surface)

    def _draw_turn_info_ui(self, surface: pygame.Surface) -> None:
        """在屏幕上绘制当前回合数信息。"""
        if not self.font_ui_small: return # 使用与按钮相同的字体或特定UI字体
        turn_text = f"Turn: {self.turn_system.current_turn}"
        text_surface = self.font_ui_small.render(turn_text, True, (220, 220, 220))
        # 显示在按钮上方或屏幕其他合适位置
        if self.next_turn_button:
            text_rect = text_surface.get_rect(midbottom=(self.next_turn_button.rect.centerx, self.next_turn_button.rect.top - 10))
        else: # 如果按钮不存在，显示在右下角备用位置
            text_rect = text_surface.get_rect(bottomright=(surface.get_width() - 20, surface.get_height() - 80))
        surface.blit(text_surface, text_rect)

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        if not self.renderer:
            surface.fill(C.COLOR_VERY_DARK_GREY)
            if self.font_debug: # 使用 font_debug 绘制错误信息
                text_surf = self.font_debug.render("渲染器未初始化!", True, C.COLOR_RED)
                surface.blit(text_surf, (50,50))
            return
        surface.fill((20, 20, 20)) 
        self.renderer.draw_tiles(surface, self.tiles)
        self.renderer.draw_grid(surface, self.grid_width_tiles, self.grid_height_tiles, self.tile_size)
        
        # 绘制所有建筑，并传递字体
        font_for_building_char = self.font_ui_small # 选择一个合适的已加载字体
        if not font_for_building_char:
            logger.warning("GameMainState.render: font_ui_small not loaded, building chars may not render correctly.")
            # 可以选择一个备用字体，或者让 Building.draw 内部处理 font_for_char 为 None 的情况
        for building_obj in self.buildings:
            building_obj.draw(surface, 
                              font_for_building_char, # <--- 传递字体
                              self.renderer.camera_offset_x, 
                              self.renderer.camera_offset_y)