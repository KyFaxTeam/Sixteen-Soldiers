import os
from src.agents.base_agent import BaseAgent
from src.models.assets.index import Assets
import random
import customtkinter as ctk
from typing import Optional, Dict
from src.store.store import Store
from src.utils.const import SOLDIER_SIZE_PLAYER, Soldier
from src.views.base_view import BaseView
from src.utils.const import AGENT_DIR
from PIL import Image
import logging

from src.utils.history_utils import get_move_player_count
logger = logging.getLogger(__name__)


class PlayerView(BaseView):
    def __init__(self, master: any, soldier_value: Soldier, store: Optional[any] = None):
        super().__init__(master)
        self.logger = logging.getLogger(__name__)
        
        self.soldier_value = soldier_value
        self.store : Store = store
        
        if store:
            initial_state = store.get_state()
            initial_time = initial_state.get("time_manager", {}).get_remaining_time(self.soldier_value)
            initial_time = int(initial_time*1000)  # Convert to milliseconds
            initial_soldier_count = initial_state["board"].count_soldiers(self.soldier_value)
            move_count = 0   # Get initial move count
        else:
            logger.warning("Store not provided. PlayerView will not be able to update.")
            move_count = 0  # Initialize move count to 0

        self.joueur_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=6
        )
        self.joueur_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.joueur_frame.grid_columnconfigure(0, weight=1)
        
        # Avatar container
        self.avatar_container = ctk.CTkFrame(
            self.joueur_frame,
            fg_color="transparent",
            height=80
        )
        self.avatar_container.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        self.avatar_container.grid_propagate(False)
        
        # Enhanced avatar with random image
        self.avatar_image = self.load_random_avatar()
        if self.avatar_image:
            self.avatar_ctk_image = ctk.CTkImage(
                self.avatar_image,
                size=(60, 60)
            )
            self.avatar = ctk.CTkLabel(
                self.avatar_container,
                text="",
                image=self.avatar_ctk_image
            )
            self.avatar.place(relx=0.5, rely=0.5, anchor="center")
        
        # Info section
        self.info_frame = ctk.CTkFrame(
            self.joueur_frame,
            fg_color="transparent"
        )
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        
        # Stats container
        self.stats_container = ctk.CTkFrame(
            self.info_frame,
            corner_radius=6
        )
        self.stats_container.pack(fill="x", pady=5)
        
        # Timer with icon
        self.timer_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color="transparent"
        )
        self.timer_frame.pack(side="left", padx=10, pady=5)

        self.timer_icon = ctk.CTkLabel(
            self.timer_frame,
            text="",
            image=ctk.CTkImage(
                light_image=Image.open(Assets.horloge),
                dark_image=Image.open(Assets.horloge_1),
                size=(17, 17)
            )
        )
        self.timer_icon.pack(side="left", padx=(0, 5))

        self.timer_label = ctk.CTkLabel(
            self.timer_frame,
            text=f"{initial_time}ms",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.timer_label.pack(side="left")
        
        # Pieces with icon
        self.pieces_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color="transparent"
        )
        self.pieces_frame.pack(side="right", padx=10, pady=5)
        
        self.pieces_icon = self.create_soldier_icon(self.pieces_frame)
        self.pieces_icon.pack(side="left", padx=(0, 5))

        self.pieces_label = ctk.CTkLabel(
            self.pieces_frame,
            text=str(initial_soldier_count),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.pieces_label.pack(side="left")
        
        # Move count with icon
        self.move_count_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color="transparent"
        )
        self.move_count_frame.pack(side="right", padx=10, pady=5)
        

        self.move_count_label = ctk.CTkLabel(
            self.move_count_frame,
            text=str(move_count),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.move_count_label.pack(side="left")
        
        # Player name
        agent_info = self.store.get_agent_info(self.soldier_value)
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text=agent_info.get('pseudo', 'Select an agent'),
            font=ctk.CTkFont(size=12)
        )
        self.name_label.pack(pady=5)
        
        # Agent selection dropdown (initially hidden)
        self.agent_dropdown = None
        self.confirm_button = None  # New confirm button
        
        # Select button
        self.select_button = ctk.CTkButton(
            self.info_frame,
            text= agent_info.get('name', 'Select') ,
            font=ctk.CTkFont(size=10),
            width=100,
            height=32,
            corner_radius=6,
            command=self.toggle_agent_dropdown
        )
        self.select_button.pack(pady=10)
  
        
    def create_soldier_icon(self, master) -> ctk.CTkLabel:
        """
        Crée un label contenant l'icône du soldat et sa valeur
        """
        is_red = self.soldier_value==Soldier.RED 
        red_soldier_icon = ctk.CTkImage(
            light_image=Image.open(Assets.img_red_soldier),
            dark_image=Image.open(Assets.img_red_soldier),
            size=SOLDIER_SIZE_PLAYER
        )
        blue_soldier_icon = ctk.CTkImage(
            light_image=Image.open(Assets.img_blue_soldier),
            dark_image=Image.open(Assets.img_blue_soldier),
            size=SOLDIER_SIZE_PLAYER
        )
        
        label = ctk.CTkLabel(
                master,
                text="",
                image= red_soldier_icon if is_red else blue_soldier_icon
            )
      
        return label
    
    def get_agent_list(self):
        """Get list of available agents from the agents directory"""
        
        agents_dir = AGENT_DIR
        # self.logger.debug(f"Recherche des agents dans le répertoire: {agents_dir}")
        # chercher la liste des fichiers existants dans agent_dir
        if os.path.exists(agents_dir):
            agents = [f.replace('.py', '') for f in os.listdir(agents_dir) if f.endswith('.py')]
            
            # vérifier si ces fichiers sont des agents valides contiennent la classe Agent en utilisant import
            for agent in agents:
                try:
                    module = __import__(f'src.agents.{agent}', fromlist=['Agent'])
                    agent_class = getattr(module, 'Agent')
                    if not issubclass(agent_class, BaseAgent):
                        agents.remove(agent)
                except Exception as e:
                    agents.remove(agent)
                    self.logger.info(f"File  {agent} does not match to an agent: {str(e)}")
            # self.logger.debug(f"Agents trouvés: {agents}")
            return sorted(agents)
        
        
        return []
        
    def can_select_agent(self) -> bool:
        """Check if agent selection is allowed based on game state"""
        state = self.store.get_state()
        # Disable selection in replay mode
        if state.get('game_mode') == 'replay':
            return False
        return (not state.get('is_game_started') or 
                state.get('is_game_paused'))

    def toggle_agent_dropdown(self):
        # self.logger.debug("Basculement du menu déroulant des agents")
        """Toggle the agent selection dropdown"""
        if not self.can_select_agent():
            self.logger.debug("Agent selection not allowed in current game state")
            return

        if self.agent_dropdown is None:
            agents = self.get_agent_list()
            if agents:
                # Hide select button first
                self.select_button.pack_forget()
                
                self.agent_dropdown = ctk.CTkOptionMenu(
                    self.info_frame,
                    values=agents,
                    width=120,
                    height=32,
                    corner_radius=6,
                    command=self.on_agent_selected
                )
                self.agent_dropdown.pack(pady=5)
                
                # Create confirm button
                self.confirm_button = ctk.CTkButton(
                    self.info_frame,
                    text="Confirm",
                    font=ctk.CTkFont(size=10),
                    width=100,
                    height=32,
                    corner_radius=6,
                    command=self.confirm_agent_selection,
                    state="disabled"  # Initially disabled
                )
                self.confirm_button.pack(pady=5)
                
                # Reconfigure and show select button as Cancel
                self.select_button.configure(text="Cancel")
                self.select_button.pack(pady=10)
        else:
            # Hide and destroy dropdown and confirm button
            self.agent_dropdown.destroy()
            self.agent_dropdown = None
            if self.confirm_button:
                self.confirm_button.destroy()
                self.confirm_button = None
            self.select_button.configure(text="Select")
            
    def on_agent_selected(self, team_name: str):
        # self.logger.debug(f"Agent sélectionné: {team_name}")
        """Handle agent selection"""
        # Enable confirm button when an agent is selected
        if self.confirm_button:
            self.confirm_button.configure(state="normal")
        # Store the selected agent temporarily
        self._selected_agent = team_name
            
    def confirm_agent_selection(self):
        # self.logger.debug("Confirmation de la sélection de l'agent")
        """Confirm and apply the agent selection"""
        if hasattr(self, '_selected_agent'):
            if self.store:
                
                self.store.dispatch({
                    'type': 'SELECT_AGENT',
                    'soldier_value': self.soldier_value,
                    'info_index': f'{self._selected_agent}_{self.soldier_value.name}'
                })
                # self.logger.info(f"agents {self.store.state.get("agents_info_index", {})}")
            # Clean up UI
            self.toggle_agent_dropdown()
            delattr(self, '_selected_agent')
        else :
            self.logger.error("No agent selected")  
     
    def load_random_avatar(self):
        self.logger.debug("Chargement d'un avatar aléatoire")
        """Loads a random avatar from the assets/avatar directory"""
        avatar_dir = Assets.dir_avatar
        avatar_files = [f for f in os.listdir(avatar_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.logger.debug(f"Fichiers d'avatar trouvés: {avatar_files}")
        if avatar_files:
            random_avatar = random.choice(avatar_files)
            avatar_path = os.path.join(avatar_dir, random_avatar)
            self.logger.debug(f"Avatar sélectionné: {avatar_path}")
            # print(f"Loading avatar image from: {avatar_path}")  # Debugging line
            try:
                image = Image.open(avatar_path).convert('RGBA')
                return image
            except Exception as e:
                print(f"Error loading image: {e}")
                return None
        else:
            self.logger.debug("Aucun fichier d'avatar trouvé")
            # print("No avatar images found in the directory.")  # Debugging line
            # Fallback if no images are found
            fallback_image = Image.new('RGBA', (60, 60), (200, 200, 200, 255))  # Gray placeholder

            return fallback_image

    def update(self, state: dict):
        """Updates the interface with new state"""
        
        try:
            # Enable/disable select button based on game state
            can_select = self.can_select_agent()
            self.select_button.configure(state="normal" if can_select else "disabled")

            info_index = state["agents_info_index"].get(self.soldier_value)
            
            if info_index is None:
                self.logger.debug("No agent selected")
                self.name_label.configure(text="Select an agent")
                self.select_button.configure(text="No team")
            else:
                agent_data = state["agents"][info_index]
                pseudo = agent_data.get("pseudo", "")
                profile_img = agent_data.get("profile_img")
                self.name_label.configure(text=pseudo)

                name = agent_data.get("name", None)
                if name:
                    self.select_button.configure(text=agent_data["name"])
                if profile_img:
                    try:
                        # Charger l'image avec PIL
                        if os.path.exists(profile_img):             
                            pil_image = Image.open(profile_img).convert('RGBA')
                            # Créer une nouvelle CTkImage
                            new_avatar_image = ctk.CTkImage(
                                light_image=pil_image,
                                dark_image=pil_image,
                                size=(60, 60)
                            )
                            # Mettre à jour l'image du label avec la nouvelle CTkImage
                            self.avatar.configure(image=new_avatar_image)
                            # Garder une référence à la nouvelle image
                            self.avatar_ctk_image = new_avatar_image
                            # Garder une référence à l'image PIL aussi
                            self.avatar_image = pil_image
                    except Exception as e:
                        self.logger.error(f"Error loading profile image: {str(e)}")
            # Update timer
            if 'time_manager' in state:
                remaining_time = state['time_manager'].get_remaining_time(self.soldier_value)
                remaining_time *= 1000  # Convert to milliseconds
                self.timer_label.configure(text=f"{int(remaining_time)}ms")
            
            # Update pieces count
            if 'board' in state:
                
                soldier_count = state['board'].count_soldiers(self.soldier_value)
                self.pieces_label.configure(text=str(soldier_count))

            # Update move count
            if 'history' in state:
                move_count = get_move_player_count(state['history'], self.soldier_value)
                self.move_count_label.configure(text=str(move_count))


            
            
        except Exception as e:
            self.logger.error(f"Error in update: {str(e)}")