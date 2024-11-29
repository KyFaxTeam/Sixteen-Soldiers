import os
from agents.base_agent import BaseAgent
from models.assets.index import Assets
import random
import customtkinter as ctk
from typing import Optional, Dict
from store.store import Store
from utils.const import Soldier
from views.base_view import BaseView
from utils.const import AGENT_DIR
from PIL import Image
import logging
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
        else:
            logger.warning("Store not provided. PlayerView will not be able to update.")
        

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
            text="⏱️",
            font=ctk.CTkFont(size=14)
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
        
        self.pieces_icon = ctk.CTkLabel(
            self.pieces_frame,
            text="♟️",
            font=ctk.CTkFont(size=14)
        )
        self.pieces_icon.pack(side="left", padx=(0, 5))

        self.pieces_label = ctk.CTkLabel(
            self.pieces_frame,
            text=str(initial_soldier_count),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.pieces_label.pack(side="left")
        
        # Player name
        agent_info = self.store.get_agent_info(self.soldier_value)
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text=agent_info.get('name', 'Select an agent'),
            font=ctk.CTkFont(size=12)
        )
        self.name_label.pack(pady=5)
        
        # Agent selection dropdown (initially hidden)
        self.agent_dropdown = None
        self.confirm_button = None  # New confirm button
        
        # Select button
        self.select_button = ctk.CTkButton(
            self.info_frame,
            text="Select",
            font=ctk.CTkFont(size=10),
            width=100,
            height=32,
            corner_radius=6,
            command=self.toggle_agent_dropdown
        )
        self.select_button.pack(pady=10)
        
    
    def get_agent_list(self):
        """Get list of available agents from the agents directory"""
        
        agents_dir = AGENT_DIR
        self.logger.debug(f"Recherche des agents dans le répertoire: {agents_dir}")
        # chercher la liste des fichiers existants dans agent_dir
        if os.path.exists(agents_dir):
            agents = [f.replace('.py', '') for f in os.listdir(agents_dir) if f.endswith('.py')]
            
            # vérifier si ces fichiers sont des agents valides contiennent la classe Agent en utilisant import
            for agent in agents:
                try:
                    module = __import__(f'agents.{agent}', fromlist=['Agent'])
                    agent_class = getattr(module, 'Agent')
                    if not issubclass(agent_class, BaseAgent):
                        agents.remove(agent)
                except Exception as e:
                    agents.remove(agent)
                    self.logger.info(f"File  {agent} does not match to an agent: {str(e)}")
            self.logger.debug(f"Agents trouvés: {agents}")
            return sorted(agents)
        
        
        return []
        
    def toggle_agent_dropdown(self):
        self.logger.debug("Basculement du menu déroulant des agents")
        """Toggle the agent selection dropdown"""
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
        self.logger.debug(f"Agent sélectionné: {team_name}")
        """Handle agent selection"""
        # Enable confirm button when an agent is selected
        if self.confirm_button:
            self.confirm_button.configure(state="normal")
        # Store the selected agent temporarily
        self._selected_agent = team_name
            
    def confirm_agent_selection(self):
        self.logger.debug("Confirmation de la sélection de l'agent")
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
            print(f"Loading avatar image from: {avatar_path}")  # Debugging line
            try:
                image = Image.open(avatar_path).convert('RGBA')
                return image
            except Exception as e:
                print(f"Error loading image: {e}")
                return None
        else:
            self.logger.debug("Aucun fichier d'avatar trouvé")
            print("No avatar images found in the directory.")  # Debugging line
            # Fallback if no images are found
            fallback_image = Image.new('RGBA', (60, 60), (200, 200, 200, 255))  # Gray placeholder

            return fallback_image

    def update(self, state: dict):

        ## Vérifier le statr 
        self.logger.debug("Mise à jour de PlayerView avec le nouvel état")
        """Updates the interface with new state"""
        self.store.state = state
        try:
            info_index = state["agents_info_index"].get(self.soldier_value)
            
            logger.debug(f"Updating player view for {self.soldier_value.name}")
            if info_index is None:
                self.logger.debug("No agent selected")
                self.name_label.configure(text="Select an agent")
                self.select_button.configure(text="No team")
            else:
                agent_data = state["agents"][info_index]
                pseudo = agent_data.get("pseudo", "")
                self.name_label.configure(text=pseudo)

                name = agent_data.get("name", None)
                if name:
                    self.select_button.configure(text=agent_data["name"])
                
            # Update timer
            if 'time_manager' in state:
                remaining_time = state['time_manager'].get_remaining_time(self.soldier_value)
                remaining_time *= 1000  # Convert to milliseconds
                self.logger.debug(f"Updating timer: {remaining_time}s")
                self.timer_label.configure(text=f"{int(remaining_time)}ms")
            
            # Update pieces count
            if 'board' in state:
                soldier_count = sum(1 for value in state['board'].soldiers.values() 
                                if value ==self.soldier_value)
                self.logger.debug(f"Updating piece count: {soldier_count}")
                self.pieces_label.configure(text=str(soldier_count))
            
            
        except Exception as e:
            self.logger.error(f"Error in update: {str(e)}")