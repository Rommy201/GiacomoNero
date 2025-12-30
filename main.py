from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import platform
import json
import os

from card_counter import CardCounter
from strategy import BlackjackStrategy

# Imposta dimensione solo su desktop, non su Android
if platform != 'android':
    Window.size = (420, 850)
Window.clearcolor = (0.059, 0.078, 0.098, 1)  # #0f1419

# Dizionario traduzioni
TRANSLATIONS = {
    'it': {
        # UI principale
        'dealer': 'Banco',
        'player': 'Io',
        'table': 'Tavolo',
        'hand': 'MANO',
        'action': 'AZIONE',
        'hand_num': 'Mano',
        'deck_cards': 'carte rimaste',
        'decks': 'mazzi',
        'bet_label': 'Puntata €:',
        'suggested_bet': 'Scommessa suggerita:',
        'leave_table': 'ESCI (Conteggio troppo basso)',
        'min_bet': 'Minima del tavolo',
        'high_count': 'Conteggio alto',
        
        # Bottoni risultato
        'won': 'VINTO',
        'push': 'PAREGGIO',
        'lost': 'PERSO',
        'blackjack': 'BJ',
        'double_win': '2x WIN',
        'double_loss': '2x LOSS',
        'surrender': 'ARRESA',
        'insurance_loss': 'ASS. PERSA',
        'skip': 'SKIP (Osserva)',
        
        # Bottoni modalità
        'dealer_mode': 'BANCO',
        'player_mode': 'IO',
        'table_mode': 'TAVOLO',
        'clear': 'Cancella',
        'split': 'SPLIT',
        
        # Menu
        'setup': 'Setup',
        'stats': 'Statistiche',
        'save': 'Salva',
        'load': 'Carica',
        'reset': 'Reset',
        
        # Toast/messaggi
        'hand_won': 'Mano {0} vinta! +€{1:.0f}',
        'hand_lost': 'Mano {0} persa. -€{1:.0f}',
        'hand_push': 'Mano {0} in pareggio (€0)',
        'hand_blackjack': 'Mano {0} BLACKJACK! +€{1:.0f}',
        'hand_double_win': 'Mano {0} 2x vinto! +€{1:.0f}',
        'hand_double_loss': 'Mano {0} 2x perso. -€{1:.0f}',
        'hand_surrender': 'Mano {0} arresa. -€{1:.0f}',
        'hand_already_registered': 'Mano {0} già registrata!',
        'all_hands_completed': 'Tutte le mani completate!',
        'register_hand': 'Registra Mano {0}/{1}',
        'insurance_lost': 'Assicurazione persa. -€{0:.0f}',
        'hand_skipped': 'Mano skippata (solo osservazione)',
        'invalid_bet': 'Puntata non valida',
        'card_added': 'Aggiunto {0}',
        'card_deleted': 'Cancellato {0} da {1}',
        'split_activated': 'SPLIT! Ora hai {0} mani',
        'max_hands': 'Massimo {0} mani',
        'playing_hand': 'Giocando Mano {0}/{1}',
        'new_shoe': 'Nuovo shoe! Conteggio azzerato',
        'table_settings': 'Tavolo: Bankroll €{0:.2f}, Min €{1:.0f}',
        'invalid_values': 'Valori non validi',
        'game_saved': 'Partita salvata!',
        'save_error': 'Errore durante il salvataggio',
        'game_loaded': 'Partita caricata!',
        'load_error': 'Errore durante il caricamento',
        'session_reset': 'Sessione resettata!',
        'no_cards_dealer': 'Nessuna carta nel BANCO',
        'no_cards_player': 'Nessuna carta nelle tue mani',
        'no_cards_table': 'Nessuna carta nel TAVOLO',
        'invalid_deck_number': 'Numero mazzi non valido',
        'new_shoe_msg': 'Nuova shoe ({0:.0f} mazzi)',
        'reset_complete': 'Reset completo',
        
        # Welcome screen
        'welcome_title': 'BENVENUTO SU BLACKJACK PRO',
        'welcome_subtitle': 'Configura il tuo tavolo',
        'start_playing': 'INIZIA A GIOCARE',
        
        # Setup popup
        'setup_title': 'Impostazioni',
        'bankroll_setup': 'Bankroll iniziale:',
        'min_bet_setup': 'Puntata minima:',
        'num_decks': 'Numero mazzi:',
        'language': 'Lingua:',
        'reset_decks': 'RESET MAZZI',
        'reset_money': 'RESET SOLDI',
        'reset_hand': 'RESET MANO',
        'reset_all': 'RESET TUTTO',
        'close_btn': 'CHIUDI',
        'apply': 'Applica',
        'cancel': 'Annulla',
        
        # Stats popup
        'stats_title': 'Statistiche Sessione',
        'hands_played': 'Mani giocate',
        'hands_won_stat': 'Vinte',
        'hands_lost_stat': 'Perse',
        'hands_pushed_stat': 'Pareggiate',
        'winrate': 'Win Rate',
        'current_bankroll': 'Bankroll corrente',
        'profit': 'Profitto',
        'close': 'Chiudi',
        
        # Riepilogo mani
        'hands_summary': 'Mani: [color=10B981]W:{0}[/color] | [color=EF4444]L:{1}[/color] | [color=9895F3]D:{2}[/color]',
    },
    'en': {
        # UI principale
        'dealer': 'Dealer',
        'player': 'Me',
        'table': 'Table',
        'hand': 'HAND',
        'action': 'ACTION',
        'hand_num': 'Hand',
        'deck_cards': 'cards left',
        'decks': 'decks',
        'bet_label': 'Bet €:',
        'suggested_bet': 'Suggested bet:',
        'leave_table': 'LEAVE (Count too low)',
        'min_bet': 'Table minimum',
        'high_count': 'High count',
        
        # Bottoni risultato
        'won': 'WON',
        'push': 'PUSH',
        'lost': 'LOST',
        'blackjack': 'BJ',
        'double_win': '2x WIN',
        'double_loss': '2x LOSS',
        'surrender': 'SURRENDER',
        'insurance_loss': 'INS. LOST',
        'skip': 'SKIP (Watch)',
        
        # Bottoni modalità
        'dealer_mode': 'DEALER',
        'player_mode': 'ME',
        'table_mode': 'TABLE',
        'clear': 'Cancel',
        'split': 'SPLIT',
        
        # Menu
        'setup': 'Setup',
        'stats': 'Statistics',
        'save': 'Save',
        'load': 'Load',
        'reset': 'Reset',
        
        # Toast/messaggi
        'hand_won': 'Hand {0} won! +€{1:.0f}',
        'hand_lost': 'Hand {0} lost. -€{1:.0f}',
        'hand_push': 'Hand {0} push (€0)',
        'hand_blackjack': 'Hand {0} BLACKJACK! +€{1:.0f}',
        'hand_double_win': 'Hand {0} 2x won! +€{1:.0f}',
        'hand_double_loss': 'Hand {0} 2x lost. -€{1:.0f}',
        'hand_surrender': 'Hand {0} surrendered. -€{1:.0f}',
        'hand_already_registered': 'Hand {0} already registered!',
        'all_hands_completed': 'All hands completed!',
        'register_hand': 'Register Hand {0}/{1}',
        'insurance_lost': 'Insurance lost. -€{0:.0f}',
        'hand_skipped': 'Hand skipped (observation only)',
        'invalid_bet': 'Invalid bet',
        'card_added': 'Added {0}',
        'card_deleted': 'Deleted {0} from {1}',
        'split_activated': 'SPLIT! You now have {0} hands',
        'max_hands': 'Maximum {0} hands',
        'playing_hand': 'Playing Hand {0}/{1}',
        'new_shoe': 'New shoe! Count reset',
        'table_settings': 'Table: Bankroll €{0:.2f}, Min €{1:.0f}',
        'invalid_values': 'Invalid values',
        'game_saved': 'Game saved!',
        'save_error': 'Error saving game',
        'game_loaded': 'Game loaded!',
        'load_error': 'Error loading game',
        'session_reset': 'Session reset!',
        'no_cards_dealer': 'No cards in DEALER',
        'no_cards_player': 'No cards in your hands',
        'no_cards_table': 'No cards on TABLE',
        'invalid_deck_number': 'Invalid deck number',
        'new_shoe_msg': 'New shoe ({0:.0f} decks)',
        'reset_complete': 'Complete reset',
        
        # Welcome screen
        'welcome_title': 'WELCOME TO BLACKJACK PRO',
        'welcome_subtitle': 'Configure your table',
        'start_playing': 'START PLAYING',
        
        # Setup popup
        'setup_title': 'Settings',
        'bankroll_setup': 'Initial bankroll:',
        'min_bet_setup': 'Minimum bet:',
        'num_decks': 'Number of decks:',
        'language': 'Language:',
        'reset_decks': 'RESET DECKS',
        'reset_money': 'RESET MONEY',
        'reset_hand': 'RESET HAND',
        'reset_all': 'RESET ALL',
        'close_btn': 'CLOSE',
        'apply': 'Apply',
        'cancel': 'Cancel',
        
        # Stats popup
        'stats_title': 'Session Statistics',
        'hands_played': 'Hands played',
        'hands_won_stat': 'Won',
        'hands_lost_stat': 'Lost',
        'hands_pushed_stat': 'Pushed',
        'winrate': 'Win Rate',
        'current_bankroll': 'Current bankroll',
        'profit': 'Profit',
        'close': 'Close',
        
        # Riepilogo mani
        'hands_summary': 'Hands: [color=10B981]W:{0}[/color] | [color=EF4444]L:{1}[/color] | [color=9895F3]D:{2}[/color]',
    }
}


class RoundedButton(Button):
    """Button con angoli arrotondati"""
    def __init__(self, radius=10, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.background_normal = ''
        self.background_down = ''
        
        # Colore di default se non specificato
        if 'background_color' not in kwargs:
            self.background_color = (0.2, 0.2, 0.2, 1)
        
        with self.canvas.before:
            self.rect_color = Color(*self.background_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_background_color(self, instance, value):
        if hasattr(self, 'rect_color'):
            self.rect_color.rgba = value


class ToastWidget(BoxLayout):
    """Widget per notifiche toast"""
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (0.85, 0.065)
        self.pos_hint = {'center_x': 0.5, 'top': 0.96}
        self.padding = [15, 10]
        
        with self.canvas.before:
            Color(0.078, 0.106, 0.176, 0.98)  # #141B2D con alpha
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        label = Label(
            text=message,
            color=(1, 1, 1, 1),
            font_size='14sp',
            bold=True,
            markup=True
        )
        self.add_widget(label)
    
    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class BlackjackApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = self.load_language()  # Carica lingua salvata o default italiano
    
    def load_language(self):
        """Carica la lingua salvata dalle preferenze"""
        try:
            lang_file = os.path.join(os.path.expanduser('~'), '.giacomonero_lang.json')
            if os.path.exists(lang_file):
                with open(lang_file, 'r') as f:
                    data = json.load(f)
                    return data.get('language', 'it')
        except:
            pass
        return 'it'  # Default italiano
    
    def save_language(self, lang):
        """Salva la lingua nelle preferenze"""
        try:
            lang_file = os.path.join(os.path.expanduser('~'), '.giacomonero_lang.json')
            with open(lang_file, 'w') as f:
                json.dump({'language': lang}, f)
        except:
            pass
    
    def t(self, key, *args):
        """Helper per traduzione con supporto formattazione"""
        text = TRANSLATIONS.get(self.language, TRANSLATIONS['it']).get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def make_rounded_button(self, btn, radius=8):
        """Aggiunge angoli arrotondati a un bottone esistente"""
        with btn.canvas.before:
            btn.rect_color = Color(*btn.background_color)
            btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[radius])
        
        def update_rect(*args):
            btn.rect.pos = btn.pos
            btn.rect.size = btn.size
        
        def update_color(instance, value):
            btn.rect_color.rgba = value
        
        btn.bind(pos=update_rect, size=update_rect)
        btn.bind(background_color=update_color)
        return btn
    
    def build(self):
        # Inizializza il contatore
        self.card_counter = CardCounter()
        
        # Inizializza con valori default temporanei
        self.card_counter.set_bankroll(100)
        self.card_counter.set_table_minimum(5)
        self.strategy = BlackjackStrategy(self.language)
        
        # Crea lo ScreenManager
        self.screen_manager = ScreenManager()
        
        # Mostra sempre la welcome screen
        welcome_screen = self.build_welcome_screen()
        self.screen_manager.add_widget(welcome_screen)
        
        return self.screen_manager
    
    def build_welcome_screen(self):
        """Costruisce la schermata di benvenuto iniziale"""
        screen = Screen(name='welcome')
        
        # Container principale
        root = FloatLayout()
        content = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        # Logo/Icona (placeholder con canvas)
        logo_container = BoxLayout(size_hint_y=0.18)
        logo = Widget()
        
        def draw_logo(instance, value):
            logo.canvas.before.clear()
            with logo.canvas.before:
                # Cerchio esterno - carta da gioco
                Color(0.45, 0.65, 0.70, 1)
                from kivy.graphics import Ellipse, Line
                center_x = logo.center_x
                center_y = logo.center_y
                size = min(logo.width, logo.height) * 0.5
                
                Ellipse(pos=(center_x - size/2, center_y - size/2), size=(size, size))
                
                # Simbolo A (Asso)
                Color(0.059, 0.078, 0.098, 1)
                from kivy.graphics import Triangle
                # Triangolo A
                tri_height = size * 0.4
                tri_base = size * 0.3
                Triangle(points=[
                    center_x, center_y + tri_height/2,
                    center_x - tri_base/2, center_y - tri_height/2,
                    center_x + tri_base/2, center_y - tri_height/2
                ])
        
        logo.bind(pos=draw_logo, size=draw_logo)
        logo_container.add_widget(logo)
        content.add_widget(logo_container)
        
        # Titolo
        title = Label(
            text=f'[b]{self.t("welcome_title")}[/b]',
            markup=True,
            color=(0.45, 0.65, 0.70, 1),
            font_size='20sp',
            size_hint_y=0.10,
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        # Sottotitolo
        subtitle = Label(
            text=self.t('welcome_subtitle'),
            color=(0.7, 0.7, 0.7, 1),
            font_size='15sp',
            size_hint_y=0.06,
            halign='center',
            valign='middle'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        content.add_widget(subtitle)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.02))
        
        # Input mazzi
        decks_box = BoxLayout(orientation='horizontal', size_hint_y=0.09, spacing=10)
        decks_label = Label(
            text=self.t('num_decks'),
            color=(1, 1, 1, 1),
            font_size='15sp',
            size_hint_x=0.5,
            halign='left',
            valign='middle'
        )
        decks_label.bind(size=decks_label.setter('text_size'))
        self.welcome_decks_input = TextInput(
            text='6',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.5,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 6]
        )
        decks_box.add_widget(decks_label)
        decks_box.add_widget(self.welcome_decks_input)
        content.add_widget(decks_box)
        
        # Input bankroll
        bankroll_box = BoxLayout(orientation='horizontal', size_hint_y=0.09, spacing=10)
        bankroll_label = Label(
            text=self.t('bankroll_setup'),
            color=(1, 1, 1, 1),
            font_size='15sp',
            size_hint_x=0.5,
            halign='left',
            valign='middle'
        )
        bankroll_label.bind(size=bankroll_label.setter('text_size'))
        self.welcome_bankroll_input = TextInput(
            text='100',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.5,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 6]
        )
        bankroll_box.add_widget(bankroll_label)
        bankroll_box.add_widget(self.welcome_bankroll_input)
        content.add_widget(bankroll_box)
        
        # Input minimo tavolo
        min_bet_box = BoxLayout(orientation='horizontal', size_hint_y=0.09, spacing=10)
        min_bet_label = Label(
            text=self.t('min_bet_setup'),
            color=(1, 1, 1, 1),
            font_size='15sp',
            size_hint_x=0.5,
            halign='left',
            valign='middle'
        )
        min_bet_label.bind(size=min_bet_label.setter('text_size'))
        self.welcome_min_bet_input = TextInput(
            text='5',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.5,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 6]
        )
        min_bet_box.add_widget(min_bet_label)
        min_bet_box.add_widget(self.welcome_min_bet_input)
        content.add_widget(min_bet_box)
        
        # Selezione lingua
        lang_box = BoxLayout(orientation='horizontal', size_hint_y=0.09, spacing=10)
        lang_label = Label(
            text=self.t('language'),
            color=(1, 1, 1, 1),
            font_size='15sp',
            size_hint_x=0.5,
            halign='left',
            valign='middle'
        )
        lang_label.bind(size=lang_label.setter('text_size'))
        
        lang_buttons_box = BoxLayout(orientation='horizontal', spacing=5, size_hint_x=0.5)
        
        self.welcome_lang_it_btn = ToggleButton(
            text='IT',
            group='welcome_language',
            state='down' if self.language == 'it' else 'normal',
            background_color=(0.35, 0.60, 0.50, 1) if self.language == 'it' else (0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='15sp',
            bold=True
        )
        self.welcome_lang_it_btn.bind(on_press=lambda x: self.change_welcome_language('it'))
        self.make_rounded_button(self.welcome_lang_it_btn, radius=8)
        
        self.welcome_lang_en_btn = ToggleButton(
            text='EN',
            group='welcome_language',
            state='down' if self.language == 'en' else 'normal',
            background_color=(0.35, 0.60, 0.50, 1) if self.language == 'en' else (0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.welcome_lang_en_btn.bind(on_press=lambda x: self.change_welcome_language('en'))
        self.make_rounded_button(self.welcome_lang_en_btn, radius=8)
        
        lang_buttons_box.add_widget(self.welcome_lang_it_btn)
        lang_buttons_box.add_widget(self.welcome_lang_en_btn)
        
        lang_box.add_widget(lang_label)
        lang_box.add_widget(lang_buttons_box)
        content.add_widget(lang_box)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.08))
        
        # Bottone start
        start_btn = Button(
            text=self.t('start_playing'),
            background_color=(0.35, 0.60, 0.50, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True,
            size_hint_y=0.11
        )
        start_btn.bind(on_press=lambda x: self.start_app_from_welcome())
        self.make_rounded_button(start_btn, radius=12)
        content.add_widget(start_btn)
        
        # Spazio finale
        content.add_widget(Label(size_hint_y=0.08))
        
        root.add_widget(content)
        screen.add_widget(root)
        return screen
    
    def change_welcome_language(self, lang):
        """Cambia la lingua nella schermata di benvenuto"""
        if lang != self.language:
            self.language = lang
            # Aggiorna colori bottoni
            self.welcome_lang_it_btn.background_color = (0.35, 0.60, 0.50, 1) if lang == 'it' else (0.2, 0.22, 0.25, 1)
            self.welcome_lang_en_btn.background_color = (0.35, 0.60, 0.50, 1) if lang == 'en' else (0.2, 0.22, 0.25, 1)
            # Ricostruisci la schermata con la nuova lingua
            self.screen_manager.clear_widgets()
            welcome_screen = self.build_welcome_screen()
            self.screen_manager.add_widget(welcome_screen)
    
    def start_app_from_welcome(self):
        """Avvia l'app principale dalla welcome screen"""
        try:
            # Leggi valori dagli input
            decks = float(self.welcome_decks_input.text)
            bankroll = float(self.welcome_bankroll_input.text)
            min_bet = float(self.welcome_min_bet_input.text)
            
            # Valida i valori
            if decks <= 0 or bankroll <= 0 or min_bet <= 0:
                return
            
            # Salva solo la lingua
            self.save_language(self.language)
            
            # Configura il card counter
            self.card_counter.set_bankroll(bankroll)
            self.card_counter.set_table_minimum(min_bet)
            self.card_counter.decks_remaining = decks
            self.card_counter.total_decks = decks
            self.strategy = BlackjackStrategy(self.language)
            
            # Rimuovi la welcome screen e aggiungi la main screen
            self.screen_manager.clear_widgets()
            main_screen = self.build_main_screen()
            self.screen_manager.add_widget(main_screen)
            
        except ValueError:
            pass  # Valori non validi
    
    def build_main_screen(self):
        """Costruisce la schermata principale del gioco"""
        screen = Screen(name='main')
        
        self.mode = "banco"
        
        # Gestione mani localmente
        self.dealer_cards = []
        self.player_hands = [[]]  # Lista di mani del giocatore (supporta split multipli)
        self.table_cards = []  # Carte altri giocatori
        
        # Gestione split multipli
        self.current_hand_index = 0  # Indice della mano corrente
        self.max_hands = 4  # Massimo 4 mani (come nei casinò reali)
        self.hand_results = []  # Risultati registrati per ogni mano (None = non ancora registrato)
        
        # Container principale - FloatLayout per supportare toast
        root = FloatLayout()
        
        # BoxLayout per il contenuto principale
        content = BoxLayout(orientation='vertical', padding=0, spacing=0, size_hint=(1, 1))

        
        # === HEADER FISSO CON BOTTONE SETUP ===
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.05,
            padding=[10, 6],
            spacing=5
        )
        with header.canvas.before:
            Color(0.102, 0.122, 0.180, 1)  # #1a1f2e
            self.header_bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(self.header_bg, 'pos', i.pos),
                    size=lambda i, v: setattr(self.header_bg, 'size', i.size))
        
        title = Label(
            text='[b]BLACKJACK PRO[/b]',
            markup=True,
            color=(1, 1, 1, 1),
            font_size='19sp',
            size_hint_x=0.7
        )
        
        self.setup_btn = Button(
            text='SETUP',
            background_color=(0.3, 0.8, 0.77, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True,
            size_hint_x=0.3
        )
        self.setup_btn.bind(on_press=lambda x: self.open_setup())
        self.make_rounded_button(self.setup_btn, radius=10)
        
        header.add_widget(title)
        header.add_widget(self.setup_btn)
        content.add_widget(header)
        
        # Layout principale con altezze flessibili per adattarsi a schermi diversi
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=6)
        
        # === CONTATORI E BANKROLL (2 colonne) ===
        count_section = BoxLayout(
            orientation='vertical',
            size_hint_y=0.11,
            padding=[10, 8],
            spacing=6
        )
        
        # Prima riga: Contatori compatti
        counters_row = BoxLayout(orientation='horizontal', size_hint_y=0.35, spacing=6)
        
        self.rc_label = Label(
            text='RC: [b]0[/b]',
            markup=True,
            color=(1, 1, 1, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.tc_label = Label(
            text='TC: [b]0.0[/b]',
            markup=True,
            color=(0.45, 0.65, 0.70, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.cards_label = Label(
            text='[b]312[/b] carte',
            markup=True,
            color=(0.50, 0.70, 0.75, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.viste_label = Label(
            text='[b]0[/b] viste',
            markup=True,
            color=(0.55, 0.60, 0.70, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.decks_label = Label(
            text='[b]6.0[/b] mazzi',
            markup=True,
            color=(0.75, 0.65, 0.50, 1),
            font_size='12sp',
            halign='center'
        )
        
        counters_row.add_widget(self.rc_label)
        counters_row.add_widget(self.tc_label)
        counters_row.add_widget(self.cards_label)
        counters_row.add_widget(self.decks_label)
        
        # Seconda riga: Bankroll e profitto
        bankroll_row = BoxLayout(orientation='horizontal', size_hint_y=0.32, spacing=8)
        
        self.bankroll_label = Label(
            text='[b]€100[/b]',
            markup=True,
            color=(0.40, 0.70, 0.50, 1),
            font_size='16sp',
            halign='left',
            valign='middle',
            size_hint_x=0.28
        )
        self.bankroll_label.bind(size=self.bankroll_label.setter('text_size'))
        
        self.profit_label = Label(
            text='(+€0)',
            color=(0.75, 0.65, 0.50, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_x=0.22
        )
        self.profit_label.bind(size=self.profit_label.setter('text_size'))
        
        self.suggested_bet_label = Label(
            text='Sugg: [b]€10[/b]',
            markup=True,
            color=(0.75, 0.65, 0.50, 1),
            font_size='11sp',
            halign='right',
            valign='middle',
            size_hint_x=0.5
        )
        self.suggested_bet_label.bind(size=self.suggested_bet_label.setter('text_size'))
        
        bankroll_row.add_widget(self.bankroll_label)
        bankroll_row.add_widget(self.profit_label)
        bankroll_row.add_widget(self.suggested_bet_label)
        
        # Terza riga: Riepilogo mani
        stats_row = BoxLayout(orientation='horizontal', size_hint_y=0.25, spacing=4)
        
        self.hands_summary_label = Label(
            text='Mani: [color=10B981]W:0[/color] | [color=EF4444]L:0[/color] | [color=9895F3]D:0[/color]',
            markup=True,
            color=(0.7, 0.7, 0.7, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_x=0.7
        )
        self.hands_summary_label.bind(size=self.hands_summary_label.setter('text_size'))
        
        self.winrate_label = Label(
            text='WR: 0%',
            color=(0.7, 0.7, 0.7, 1),
            font_size='12sp',
            halign='right',
            valign='middle',
            size_hint_x=0.3
        )
        self.winrate_label.bind(size=self.winrate_label.setter('text_size'))
        
        stats_row.add_widget(self.hands_summary_label)
        stats_row.add_widget(self.winrate_label)
        
        count_section.add_widget(counters_row)
        count_section.add_widget(bankroll_row)
        count_section.add_widget(stats_row)
        main_layout.add_widget(count_section)
        
        # === CARTE + BOTTONI MODALITÀ ===
        cards_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.24,
            padding=[10, 8],
            spacing=10
        )
        
        # Bottoni modalità + Cancella (verticale, sinistra)
        mode_buttons = BoxLayout(orientation='vertical', size_hint_x=0.24, spacing=5)
        
        self.mode_banco_btn = ToggleButton(
            text='BANCO',
            group='mode',
            state='down',
            background_color=(0.35, 0.60, 0.50, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.25
        )
        self.mode_banco_btn.bind(on_press=lambda x: self.set_mode('banco'))
        self.make_rounded_button(self.mode_banco_btn, radius=8)
        
        self.mode_mio_btn = ToggleButton(
            text='MIO',
            group='mode',
            background_color=(0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.25
        )
        self.mode_mio_btn.bind(on_press=lambda x: self.set_mode('mio'))
        self.make_rounded_button(self.mode_mio_btn, radius=8)
        
        self.mode_tavolo_btn = ToggleButton(
            text='TAVOLO',
            group='mode',
            background_color=(0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.25
        )
        self.mode_tavolo_btn.bind(on_press=lambda x: self.set_mode('tavolo'))
        self.make_rounded_button(self.mode_tavolo_btn, radius=8)
        
        self.cancel_btn = Button(
            text='CANCELLA',
            background_color=(0.70, 0.35, 0.35, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.25
        )
        self.cancel_btn.bind(on_press=lambda x: self.delete_last_card())
        self.make_rounded_button(self.cancel_btn, radius=8)
        
        mode_buttons.add_widget(self.mode_banco_btn)
        mode_buttons.add_widget(self.mode_mio_btn)
        mode_buttons.add_widget(self.mode_tavolo_btn)
        mode_buttons.add_widget(self.cancel_btn)
        
        # Griglia carte 4x4 (13 carte)
        cards_grid = GridLayout(cols=4, spacing=5, size_hint_x=1)
        
        card_data = [
            ('A', (0.75, 0.45, 0.45, 1)),
            ('2', (0.35, 0.60, 0.50, 1)),
            ('3', (0.35, 0.60, 0.50, 1)),
            ('4', (0.35, 0.60, 0.50, 1)),
            ('5', (0.35, 0.60, 0.50, 1)),
            ('6', (0.35, 0.60, 0.50, 1)),
            ('7', (0.65, 0.60, 0.45, 1)),
            ('8', (0.65, 0.60, 0.45, 1)),
            ('9', (0.65, 0.60, 0.45, 1)),
            ('10', (0.75, 0.45, 0.45, 1)),
            ('J', (0.75, 0.45, 0.45, 1)),
            ('Q', (0.75, 0.45, 0.45, 1)),
            ('K', (0.75, 0.45, 0.45, 1)),
        ]
        
        for card, color in card_data:
            btn = Button(
                text=card,
                background_color=color,
                background_normal='',
                color=(1, 1, 1, 1),
                font_size='18sp',
                bold=True
            )
            btn.bind(on_press=lambda x, c=card: self.add_card(c))
            self.make_rounded_button(btn, radius=8)
            cards_grid.add_widget(btn)
        
        cards_section.add_widget(mode_buttons)
        cards_section.add_widget(cards_grid)
        main_layout.add_widget(cards_section)
        
        # === MANO + AZIONE (2 colonne) ===
        game_info = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.18,
            padding=[10, 8],
            spacing=10
        )
        
        # MANO (sinistra)
        hand_box = BoxLayout(orientation='vertical', size_hint_x=0.5, padding=[5, 3], spacing=2)
        with hand_box.canvas.before:
            Color(0.118, 0.141, 0.184, 1)  # Leggermente più scuro
            self.hand_bg = Rectangle(pos=hand_box.pos, size=hand_box.size)
        hand_box.bind(pos=lambda i, v: setattr(self.hand_bg, 'pos', i.pos),
                     size=lambda i, v: setattr(self.hand_bg, 'size', i.size))
        
        self.hand_title = Label(
            text='[b]MANO[/b]',
            markup=True,
            color=(0.40, 0.70, 0.50, 1),
            font_size='12sp',
            size_hint_y=0.12,
            halign='center',
            valign='top'
        )
        self.hand_title.bind(size=self.hand_title.setter('text_size'))
        
        self.dealer_label = Label(
            text='Banco: -',
            color=(0.75, 0.45, 0.45, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_y=0.13
        )
        self.dealer_label.bind(size=self.dealer_label.setter('text_size'))
        
        self.player_label = Label(
            text='Io: -',
            color=(0.45, 0.65, 0.70, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_y=0.24
        )
        self.player_label.bind(size=self.player_label.setter('text_size'))
        
        # Label per seconda mano (split)
        self.player_split_label = Label(
            text='Mano 2: -',
            color=(0.50, 0.70, 0.75, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_y=0.12
        )
        self.player_split_label.bind(size=self.player_split_label.setter('text_size'))
        
        self.table_label = Label(
            text='Tavolo: -',
            color=(0.6, 0.6, 0.6, 1),
            font_size='12sp',
            halign='left',
            valign='top',
            size_hint_y=0.35
        )
        self.table_label.bind(size=self.table_label.setter('text_size'))
        
        # Bottoni split e navigazione
        split_buttons = BoxLayout(orientation='horizontal', size_hint_y=0.16, spacing=2)
        
        self.activate_split_btn = Button(
            text='SPLIT',
            background_color=(0.40, 0.50, 0.65, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        self.activate_split_btn.bind(on_press=lambda x: self.activate_split())
        self.make_rounded_button(self.activate_split_btn, radius=6)
        
        # Bottone freccia sinistra per mano precedente
        self.prev_hand_btn = Button(
            text='<',
            background_color=(0.35, 0.55, 0.70, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='14sp',
            bold=True,
            size_hint_x=0.25
        )
        self.prev_hand_btn.bind(on_press=lambda x: self.navigate_hands(-1))
        self.make_rounded_button(self.prev_hand_btn, radius=6)
        
        # Bottone freccia destra per mano successiva
        self.next_hand_btn = Button(
            text='>',
            background_color=(0.35, 0.55, 0.70, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='14sp',
            bold=True,
            size_hint_x=0.25
        )
        self.next_hand_btn.bind(on_press=lambda x: self.navigate_hands(1))
        self.make_rounded_button(self.next_hand_btn, radius=6)
        
        split_buttons.add_widget(self.prev_hand_btn)
        split_buttons.add_widget(self.activate_split_btn)
        split_buttons.add_widget(self.next_hand_btn)
        
        hand_box.add_widget(self.hand_title)
        hand_box.add_widget(self.dealer_label)
        hand_box.add_widget(self.player_label)
        hand_box.add_widget(self.table_label)
        hand_box.add_widget(split_buttons)
        
        # Nascondi bottoni navigazione all'inizio
        self.prev_hand_btn.opacity = 0
        self.prev_hand_btn.disabled = True
        self.next_hand_btn.opacity = 0
        self.next_hand_btn.disabled = True
        self.activate_split_btn.opacity = 0
        self.activate_split_btn.disabled = True
        
        # AZIONE (destra)
        action_box = BoxLayout(orientation='vertical', size_hint_x=0.5, padding=[5, 3], spacing=2)
        with action_box.canvas.before:
            Color(0.118, 0.141, 0.184, 1)
            self.action_bg = Rectangle(pos=action_box.pos, size=action_box.size)
        action_box.bind(pos=lambda i, v: setattr(self.action_bg, 'pos', i.pos),
                       size=lambda i, v: setattr(self.action_bg, 'size', i.size))
        
        self.action_title = Label(
            text='[b]AZIONE[/b]',
            markup=True,
            color=(0.75, 0.65, 0.50, 1),
            font_size='12sp',
            size_hint_y=0.12,
            halign='center',
            valign='top'
        )
        self.action_title.bind(size=self.action_title.setter('text_size'))
        
        self.strategy_label = Label(
            text='Inserisci carte',
            color=(1, 1, 1, 1),
            font_size='13sp',
            bold=True,
            halign='center',
            valign='middle',
            markup=True
        )
        self.strategy_label.bind(size=self.strategy_label.setter('text_size'))
        
        action_box.add_widget(self.action_title)
        action_box.add_widget(self.strategy_label)
        
        game_info.add_widget(hand_box)
        game_info.add_widget(action_box)
        main_layout.add_widget(game_info)
        
        # === RISULTATI CON INPUT SCOMMESSA ===
        results_section = BoxLayout(
            orientation='vertical',
            size_hint_y=0.27,
            padding=[10, 12, 10, 10],
            spacing=8
        )
        
        # Input scommessa con controlli rapidi
        bet_input_box = BoxLayout(orientation='horizontal', size_hint_y=0.18, spacing=3, padding=[0, 0])
        
        self.bet_label = Label(
            text='Puntata €:',
            color=(0.75, 0.65, 0.50, 1),
            font_size='12sp',
            bold=True,
            size_hint_x=0.22,
            halign='right',
            valign='middle'
        )
        self.bet_label.bind(size=self.bet_label.setter('text_size'))
        
        initial_bet = self.card_counter.get_bet_multiplier()['bet_amount']
        self.bet_input = TextInput(
            text=f'{initial_bet:.0f}',
            multiline=False,
            font_size='13sp',
            size_hint_x=0.20,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.45, 0.65, 0.70, 1),
            padding=[8, 6],
            halign='center'
        )
        
        # Radio buttons per modalità + o -
        self.bet_mode_plus = ToggleButton(
            text='+',
            group='bet_mode',
            state='down',
            background_color=(0.35, 0.60, 0.50, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True,
            size_hint_x=0.10
        )
        self.bet_mode_plus.bind(on_press=lambda x: self.update_bet_mode_colors())
        self.make_rounded_button(self.bet_mode_plus, radius=6)
        
        self.bet_mode_minus = ToggleButton(
            text='-',
            group='bet_mode',
            background_color=(0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True,
            size_hint_x=0.10
        )
        self.bet_mode_minus.bind(on_press=lambda x: self.update_bet_mode_colors())
        self.make_rounded_button(self.bet_mode_minus, radius=6)
        
        bet5_btn = Button(
            text='5',
            background_color=(0.35, 0.55, 0.70, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True,
            size_hint_x=0.12
        )
        bet5_btn.bind(on_press=lambda x: self.adjust_bet_value(5))
        self.make_rounded_button(bet5_btn, radius=6)
        
        bet10_btn = Button(
            text='10',
            background_color=(0.35, 0.55, 0.70, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True,
            size_hint_x=0.12
        )
        bet10_btn.bind(on_press=lambda x: self.adjust_bet_value(10))
        self.make_rounded_button(bet10_btn, radius=6)
        
        bet20_btn = Button(
            text='20',
            background_color=(0.35, 0.55, 0.70, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True,
            size_hint_x=0.12
        )
        bet20_btn.bind(on_press=lambda x: self.adjust_bet_value(20))
        self.make_rounded_button(bet20_btn, radius=6)
        
        bet_input_box.add_widget(self.bet_label)
        bet_input_box.add_widget(self.bet_input)
        bet_input_box.add_widget(self.bet_mode_plus)
        bet_input_box.add_widget(self.bet_mode_minus)
        bet_input_box.add_widget(bet5_btn)
        bet_input_box.add_widget(bet10_btn)
        bet_input_box.add_widget(bet20_btn)
        
        # Bottoni risultato
        row1 = BoxLayout(orientation='horizontal', spacing=4, size_hint_y=0.41)
        
        self.win_btn = Button(
            text='VINTO',
            background_color=(0.35, 0.60, 0.50, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.win_btn.bind(on_press=lambda x: self.record_result('win'))
        self.make_rounded_button(self.win_btn, radius=8)
        
        self.push_btn = Button(
            text='PAREGGIO',
            background_color=(0.45, 0.50, 0.60, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.push_btn.bind(on_press=lambda x: self.record_result('push'))
        self.make_rounded_button(self.push_btn, radius=8)
        
        self.lose_btn = Button(
            text='PERSO',
            background_color=(0.70, 0.35, 0.35, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.lose_btn.bind(on_press=lambda x: self.record_result('lose'))
        self.make_rounded_button(self.lose_btn, radius=8)
        
        # Bottone blackjack (nella stessa riga)
        self.bj_btn = Button(
            text='BJ',
            background_color=(0.65, 0.60, 0.45, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.bj_btn.bind(on_press=lambda x: self.record_result('blackjack'))
        self.make_rounded_button(self.bj_btn, radius=8)
        
        row1.add_widget(self.win_btn)
        row1.add_widget(self.push_btn)
        row1.add_widget(self.lose_btn)
        row1.add_widget(self.bj_btn)
        
        # Seconda riga: Double e Surrender
        row2 = BoxLayout(orientation='horizontal', spacing=4, size_hint_y=0.41)
        
        self.double_win_btn = Button(
            text='2x WIN',
            background_color=(0.30, 0.50, 0.40, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.double_win_btn.bind(on_press=lambda x: self.record_result('double_win'))
        self.make_rounded_button(self.double_win_btn, radius=8)
        
        self.double_loss_btn = Button(
            text='2x LOSS',
            background_color=(0.60, 0.30, 0.30, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.double_loss_btn.bind(on_press=lambda x: self.record_result('double_loss'))
        self.make_rounded_button(self.double_loss_btn, radius=8)
        
        self.surrender_btn = Button(
            text='ARRESA',
            background_color=(0.40, 0.45, 0.50, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.surrender_btn.bind(on_press=lambda x: self.record_result('surrender'))
        self.make_rounded_button(self.surrender_btn, radius=8)
        
        # Bottone assicurazione persa
        self.insurance_loss_btn = Button(
            text='ASS. PERSA',
            background_color=(0.65, 0.55, 0.45, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        self.insurance_loss_btn.bind(on_press=lambda x: self.record_insurance_loss())
        self.make_rounded_button(self.insurance_loss_btn, radius=8)
        
        row2.add_widget(self.double_win_btn)
        row2.add_widget(self.double_loss_btn)
        row2.add_widget(self.surrender_btn)
        row2.add_widget(self.insurance_loss_btn)
        
        # Terza riga: Skip per osservazione
        row3 = BoxLayout(orientation='horizontal', spacing=4, size_hint_y=0.41)
        
        self.skip_btn = Button(
            text='SKIP (Osserva)',
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        self.skip_btn.bind(on_press=lambda x: self.skip_hand())
        self.make_rounded_button(self.skip_btn, radius=8)
        
        row3.add_widget(self.skip_btn)
        
        results_section.add_widget(bet_input_box)
        results_section.add_widget(row1)
        results_section.add_widget(row2)
        results_section.add_widget(row3)
        main_layout.add_widget(results_section)
        
        # Aggiungi main_layout direttamente al content
        content.add_widget(main_layout)
        
        # Aggiungi content al root FloatLayout
        root.add_widget(content)
        
        # Salva riferimento al root per i toast
        self.root = root
        
        # Inizializza gli input del setup (creati nel popup)
        self.decks_input = None
        self.bankroll_input = None
        self.min_bet_input = None
        
        # Aggiorna display per sincronizzare tutto con i valori corretti
        self.update_display()
        
        screen.add_widget(root)
        return screen
    
    def show_toast(self, message):
        """Mostra toast notification"""
        # Trova il root widget della schermata corrente
        try:
            current_screen = self.screen_manager.get_screen(self.screen_manager.current)
            root = current_screen.children[0] if current_screen.children else None
            
            if not root:
                return
            
            if hasattr(self, 'toast_widget') and self.toast_widget:
                try:
                    root.remove_widget(self.toast_widget)
                except:
                    pass
            
            self.toast_widget = ToastWidget(message)
            root.add_widget(self.toast_widget)
            
            Clock.schedule_once(lambda dt: self._remove_toast(root), 2)
        except:
            pass
    
    def _remove_toast(self, root):
        """Rimuove il toast widget"""
        try:
            if hasattr(self, 'toast_widget') and self.toast_widget:
                root.remove_widget(self.toast_widget)
        except:
            pass

    
    def change_language(self, lang):
        """Cambia la lingua dell'interfaccia"""
        if lang != self.language:
            self.language = lang
            # Aggiorna anche la lingua della strategia
            self.strategy.language = lang
            # Aggiorna i colori dei bottoni lingua
            if hasattr(self, 'lang_it_btn'):
                self.lang_it_btn.background_color = (0.35, 0.60, 0.50, 1) if lang == 'it' else (0.2, 0.22, 0.25, 1)
                self.lang_en_btn.background_color = (0.35, 0.60, 0.50, 1) if lang == 'en' else (0.2, 0.22, 0.25, 1)
            # Aggiorna tutti i testi UI
            self.update_ui_texts()
            # Chiudi e riapri il setup per aggiornare le traduzioni
            if hasattr(self, 'setup_popup'):
                self.setup_popup.dismiss()
            Clock.schedule_once(lambda dt: self.open_setup(), 0.1)
            # Aggiorna display principale
            self.update_display()
    
    def update_ui_texts(self):
        """Aggiorna tutti i testi dell'interfaccia con la lingua corrente"""
        if not hasattr(self, 'mode_banco_btn'):
            return  # UI non ancora creata
        
        # Bottoni modalità
        self.mode_banco_btn.text = self.t('dealer_mode')
        self.mode_mio_btn.text = self.t('player_mode')
        self.mode_tavolo_btn.text = self.t('table_mode')
        self.cancel_btn.text = self.t('clear').upper()
        
        # Titoli sezioni mano/azione
        self.hand_title.text = f'[b]{self.t("hand")}[/b]'
        self.action_title.text = f'[b]{self.t("action")}[/b]'
        
        # Bottoni split
        self.activate_split_btn.text = self.t('split')
        
        # Label puntata
        self.bet_label.text = self.t('bet_label')
        
        # Bottoni risultato
        self.win_btn.text = self.t('won')
        self.push_btn.text = self.t('push')
        self.lose_btn.text = self.t('lost')
        self.bj_btn.text = self.t('blackjack')
        self.double_win_btn.text = self.t('double_win')
        self.double_loss_btn.text = self.t('double_loss')
        self.surrender_btn.text = self.t('surrender')
        self.insurance_loss_btn.text = self.t('insurance_loss')
        self.skip_btn.text = self.t('skip')
        
        # Bottoni menu (solo setup esiste attualmente)
        self.setup_btn.text = self.t('setup').upper()
    
    def open_setup(self):
        """Apre il popup di setup"""
        # Contenuto del popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        # Titolo
        title = Label(
            text=f'[b]{self.t("setup_title").upper()}[/b]',
            markup=True,
            color=(0.45, 0.65, 0.70, 1),
            font_size='14sp',
            size_hint_y=0.08
        )
        content.add_widget(title)
        
        # Mazzi rimasti
        decks_box = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=10)
        decks_label = Label(
            text=self.t('num_decks'),
            color=(1, 1, 1, 1),
            font_size='12sp',
            size_hint_x=0.45
        )
        self.decks_input = TextInput(
            text=f'{self.card_counter.decks_remaining:.1f}' if hasattr(self.card_counter, 'decks_remaining') else '6',
            multiline=False,
            font_size='13sp',
            size_hint_x=0.55,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 8]
        )
        decks_box.add_widget(decks_label)
        decks_box.add_widget(self.decks_input)
        content.add_widget(decks_box)
        
        # Bankroll
        bankroll_box = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=10)
        bankroll_label = Label(
            text=self.t('bankroll_setup'),
            color=(1, 1, 1, 1),
            font_size='12sp',
            size_hint_x=0.45
        )
        initial_bankroll = getattr(self.card_counter, 'initial_bankroll', 100)
        self.bankroll_input = TextInput(
            text=f'{initial_bankroll:.2f}',
            multiline=False,
            font_size='13sp',
            size_hint_x=0.55,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 8]
        )
        bankroll_box.add_widget(bankroll_label)
        bankroll_box.add_widget(self.bankroll_input)
        content.add_widget(bankroll_box)
        
        # Minimo tavolo
        min_bet_box = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=10)
        min_bet_label = Label(
            text=self.t('min_bet_setup'),
            color=(1, 1, 1, 1),
            font_size='12sp',
            size_hint_x=0.45
        )
        table_minimum = getattr(self.card_counter, 'table_minimum', 5)
        self.min_bet_input = TextInput(
            text=f'{table_minimum:.0f}',
            multiline=False,
            font_size='13sp',
            size_hint_x=0.55,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 8]
        )
        min_bet_box.add_widget(min_bet_label)
        min_bet_box.add_widget(self.min_bet_input)
        content.add_widget(min_bet_box)
        
        # Lingua
        lang_box = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=10)
        lang_label = Label(
            text=self.t('language'),
            color=(1, 1, 1, 1),
            font_size='12sp',
            size_hint_x=0.45
        )
        
        lang_buttons_box = BoxLayout(orientation='horizontal', spacing=5, size_hint_x=0.55)
        
        self.lang_it_btn = ToggleButton(
            text='IT',
            group='language',
            state='down' if self.language == 'it' else 'normal',
            background_color=(0.35, 0.60, 0.50, 1) if self.language == 'it' else (0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.lang_it_btn.bind(on_press=lambda x: self.change_language('it'))
        self.make_rounded_button(self.lang_it_btn, radius=6)
        
        self.lang_en_btn = ToggleButton(
            text='EN',
            group='language',
            state='down' if self.language == 'en' else 'normal',
            background_color=(0.35, 0.60, 0.50, 1) if self.language == 'en' else (0.2, 0.22, 0.25, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        self.lang_en_btn.bind(on_press=lambda x: self.change_language('en'))
        self.make_rounded_button(self.lang_en_btn, radius=6)
        
        lang_buttons_box.add_widget(self.lang_it_btn)
        lang_buttons_box.add_widget(self.lang_en_btn)
        
        lang_box.add_widget(lang_label)
        lang_box.add_widget(lang_buttons_box)
        content.add_widget(lang_box)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.03))
        
        # 1. Bottone imposta mazzi
        new_shoe_btn = Button(
            text=self.t('reset_decks'),
            background_color=(0.35, 0.55, 0.70, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.10
        )
        new_shoe_btn.bind(on_press=lambda x: self.new_shoe())
        self.make_rounded_button(new_shoe_btn, radius=10)
        content.add_widget(new_shoe_btn)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.02))
        
        # 2. Bottone reset soldi
        set_table_btn = Button(
            text=self.t('reset_money'),
            background_color=(0.35, 0.60, 0.50, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.10
        )
        set_table_btn.bind(on_press=lambda x: self.set_table_settings())
        self.make_rounded_button(set_table_btn, radius=10)
        content.add_widget(set_table_btn)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.02))
        
        # 3. Bottone reset mano corrente
        reset_hand_btn = Button(
            text=self.t('reset_hand'),
            background_color=(0.65, 0.60, 0.45, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.10
        )
        reset_hand_btn.bind(on_press=lambda x: self.reset_current_hand())
        self.make_rounded_button(reset_hand_btn, radius=10)
        content.add_widget(reset_hand_btn)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.02))
        
        # 4. Bottone reset tutto
        reset_all_btn = Button(
            text=self.t('reset_all'),
            background_color=(0.70, 0.35, 0.35, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.10
        )
        reset_all_btn.bind(on_press=lambda x: self.reset_all())
        self.make_rounded_button(reset_all_btn, radius=10)
        content.add_widget(reset_all_btn)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.02))
        
        # 5. Bottone chiudi
        close_btn = Button(
            text=self.t('close_btn'),
            background_color=(0.45, 0.50, 0.60, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.10
        )
        self.make_rounded_button(close_btn, radius=8)

        
        # Crea popup
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.6),
            background_color=(0.059, 0.078, 0.098, 1),
            separator_color=(0.45, 0.65, 0.70, 1)
        )
        
        # Salva riferimento al popup per chiuderlo dalle azioni
        self.setup_popup = popup
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()
    
    def set_mode(self, mode):
        """Cambia modalità"""
        self.mode = mode
        
        # Colore verde brillante per selezionato, grigio scuro per non selezionati
        selected_color = (0.35, 0.60, 0.50, 1)
        unselected_color = (0.2, 0.22, 0.25, 1)
        
        if mode == 'banco':
            self.mode_banco_btn.background_color = selected_color
            self.mode_mio_btn.background_color = unselected_color
            self.mode_tavolo_btn.background_color = unselected_color
        elif mode == 'mio':
            self.mode_banco_btn.background_color = unselected_color
            self.mode_mio_btn.background_color = selected_color
            self.mode_tavolo_btn.background_color = unselected_color
        else:  # tavolo
            self.mode_banco_btn.background_color = unselected_color
            self.mode_mio_btn.background_color = unselected_color
            self.mode_tavolo_btn.background_color = selected_color
    
    def update_bet_mode_colors(self):
        """Aggiorna colori dei bottoni +/- in base alla selezione"""
        selected_color = (0.35, 0.60, 0.50, 1)  # Verde tenue
        unselected_color = (0.2, 0.22, 0.25, 1)  # Grigio scuro
        
        if self.bet_mode_plus.state == 'down':
            self.bet_mode_plus.background_color = selected_color
            self.bet_mode_minus.background_color = unselected_color
        else:
            self.bet_mode_plus.background_color = unselected_color
            self.bet_mode_minus.background_color = selected_color
    
    def add_card(self, card):
        """Aggiunge carta"""
        # Aggiungi alla lista appropriata
        if self.mode == "banco":
            self.dealer_cards.append(card)
        elif self.mode == "mio":
            # Aggiungi alla mano corrente
            self.player_hands[self.current_hand_index].append(card)
        else:  # tavolo
            self.table_cards.append(card)
        
        # Aggiungi al contatore
        self.card_counter.add_card(card)
        
        self.update_display()
    
    def activate_split(self):
        """Attiva modalità split - crea una nuova mano dalla carta corrente"""
        current_hand = self.player_hands[self.current_hand_index]
        
        # Controlla se possiamo splittare
        if len(current_hand) == 2 and len(self.player_hands) < self.max_hands:
            # Prendi una carta e crea una nuova mano
            card = current_hand.pop()
            self.player_hands.append([card])
            
            # Inizializza i risultati se è il primo split
            if len(self.hand_results) == 0:
                self.hand_results = [None] * len(self.player_hands)
            else:
                self.hand_results.append(None)
            
            # Mostra bottoni navigazione
            self.prev_hand_btn.opacity = 1
            self.prev_hand_btn.disabled = False
            self.next_hand_btn.opacity = 1
            self.next_hand_btn.disabled = False
            
            self.update_display()
            total_hands = len(self.player_hands)
            self.show_toast(self.t('split_activated', total_hands))
        elif len(self.player_hands) >= self.max_hands:
            self.show_toast(self.t('max_hands', self.max_hands))
    
    def navigate_hands(self, direction):
        """Naviga tra le mani (-1 per precedente, +1 per successiva)"""
        new_index = self.current_hand_index + direction
        
        # Verifica limiti
        if 0 <= new_index < len(self.player_hands):
            self.current_hand_index = new_index
            self.update_display()
            self.show_toast(self.t('playing_hand', self.current_hand_index + 1, len(self.player_hands)))
    
    def get_card_value(self, card):
        """Ottiene il valore numerico di una carta per il confronto"""
        if card in ['J', 'Q', 'K']:
            return 10
        elif card == 'A':
            return 11
        else:
            return int(card)
    
    def calculate_hand_value(self, cards):
        """Calcola il valore della mano e se è soft (con asso contato come 11)"""
        total = 0
        aces = 0
        
        for card in cards:
            if card in ['J', 'Q', 'K']:
                total += 10
            elif card == 'A':
                aces += 1
                total += 11
            else:
                total += int(card)
        
        # Gestione assi
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        soft = (aces > 0 and total <= 21)
        return total, soft
    
    def update_display(self):
        """Aggiorna display"""
        # Contatori (con markup)
        rc = self.card_counter.running_count
        tc = self.card_counter.get_true_count()
        self.rc_label.text = f'RC: [b]{rc}[/b]'
        self.tc_label.text = f'TC: [b]{tc:.1f}[/b]'
        
        # Carte rimanenti e viste
        cards_remaining = self.card_counter.get_cards_remaining()
        cards_seen = self.card_counter.cards_seen
        self.cards_label.text = f'[b]{cards_remaining}[/b] {self.t("deck_cards")}'
        
        # Mazzi rimanenti
        decks_remaining = getattr(self.card_counter, 'decks_remaining', 6)
        decks_used = cards_seen / 52
        decks_left = max(decks_remaining - decks_used, 0)
        self.decks_label.text = f'[b]{decks_left:.1f}[/b] {self.t("decks")}'
        
        # Mano banco
        if self.dealer_cards:
            dealer_total, dealer_soft = self.calculate_hand_value(self.dealer_cards)
            if dealer_soft:
                self.dealer_label.text = f"{self.t('dealer')}: {', '.join(self.dealer_cards)} ({dealer_total})"
            else:
                self.dealer_label.text = f"{self.t('dealer')}: {', '.join(self.dealer_cards)} ({dealer_total})"
        else:
            self.dealer_label.text = f"{self.t('dealer')}: -"
        
        # Mano giocatore (mostra solo la mano corrente)
        current_hand = self.player_hands[self.current_hand_index]
        total_hands = len(self.player_hands)
        
        if current_hand:
            player_total, player_soft = self.calculate_hand_value(current_hand)
            cards_text = ', '.join(current_hand)
            
            if total_hands > 1:
                # Con split: mostra "Mano X/Y: carte (totale)" + indicatore se completata
                status_indicator = ""
                if len(self.hand_results) > self.current_hand_index and self.hand_results[self.current_hand_index] is not None:
                    status_indicator = " [OK]"  # Mano completata
                hand_display = f"{self.t('hand_num')} {self.current_hand_index + 1}/{total_hands}{status_indicator}: {cards_text} ({player_total})"
            else:
                # Senza split: mostra "Io: carte (totale)"
                hand_display = f"{self.t('player')}: {cards_text} ({player_total})"
        else:
            if total_hands > 1:
                hand_display = f"{self.t('hand_num')} {self.current_hand_index + 1}/{total_hands}: -"
            else:
                hand_display = f"{self.t('player')}: -"
        
        self.player_label.text = hand_display
        
        self.table_label.text = f"{self.t('table')}: {', '.join(self.table_cards) if self.table_cards else '-'}"
        
        # Strategia basata sulla mano corrente - solo se il giocatore ha almeno 2 carte
        if self.dealer_cards and current_hand and len(current_hand) >= 2:
            player_total, is_soft = self.calculate_hand_value(current_hand)
            # Controlla coppia: due carte con stesso valore (es: 10 e Q sono una coppia)
            is_pair = (len(current_hand) == 2 and 
                      self.get_card_value(current_hand[0]) == self.get_card_value(current_hand[1]))
            true_count = self.card_counter.get_true_count()
            
            suggestion = self.strategy.get_suggestion(
                player_total,
                self.dealer_cards[0],
                is_soft,
                is_pair,
                true_count,
                len(current_hand)  # Passa il numero di carte
            )
            
            # Costruisci il testo da mostrare
            action_text = f"[b][size=18sp]{suggestion['action']}[/size][/b]"
            
            # Aggiungi descrizione dettagliata
            description = suggestion.get('description', '')
            if description:
                # Rimuovi le parti già presenti nell'action (per evitare ripetizioni)
                # e formatta il testo
                lines = description.split('\n')
                detail_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(suggestion['action']):
                        # Evidenzia le informazioni importanti
                        if line.startswith('ASSICURAZIONE:'):
                            detail_lines.append(f"[color=F59E0B]{line}[/color]")
                        elif 'TC=' in line or 'Strategia modificata' in line:
                            detail_lines.append(f"[color=10B981][size=11sp]{line}[/size][/color]")
                        elif 'Se non puoi' in line:
                            detail_lines.append(f"[size=11sp]{line}[/size]")
                        else:
                            detail_lines.append(f"[size=12sp]{line}[/size]")
                
                if detail_lines:
                    action_text += '\n' + '\n'.join(detail_lines)
            
            self.strategy_label.text = action_text
        else:
            self.strategy_label.text = "Inserisci carte"
        
        # Bankroll e statistiche
        bankroll = getattr(self.card_counter, 'current_bankroll', getattr(self.card_counter, 'bankroll', 100))
        initial_bankroll = getattr(self.card_counter, 'initial_bankroll', 100)
        profit = bankroll - initial_bankroll
        
        self.bankroll_label.text = f"[b]€{bankroll:.2f}[/b]"
        
        # Colora profitto
        if profit > 0:
            profit_color = (0.28, 0.73, 0.44, 1)  # verde
            self.profit_label.text = f"(+€{profit:.2f})"
        elif profit < 0:
            profit_color = (0.90, 0.24, 0.24, 1)  # rosso
            self.profit_label.text = f"(€{profit:.2f})"
        else:
            profit_color = (0.6, 0.6, 0.6, 1)  # grigio
            self.profit_label.text = "(+€0.00)"
        self.profit_label.color = profit_color
        
        # Statistiche mani
        hands_played = getattr(self.card_counter, 'hands_played', 0)
        hands_won = getattr(self.card_counter, 'hands_won', 0)
        hands_lost = getattr(self.card_counter, 'hands_lost', 0)
        hands_pushed = getattr(self.card_counter, 'hands_pushed', 0)
        
        # Riepilogo mani con colori
        self.hands_summary_label.text = self.t('hands_summary', hands_won, hands_lost, hands_pushed)
        
        if hands_played > 0:
            winrate = (hands_won / hands_played) * 100
            self.winrate_label.text = f"{self.t('winrate')}: {winrate:.0f}%"
        else:
            self.winrate_label.text = f"{self.t('winrate')}: 0%"
        
        # Puntata suggerita (con markup)
        bet_info = self.card_counter.get_bet_multiplier()
        suggested = bet_info['bet_amount']
        
        # Testo suggerimento con azione
        sugg_text = f"{self.t('suggested_bet')} "
        if bet_info['action'] == 'LEAVE':
            sugg_text = f"{sugg_text}{self.t('leave_table')}"
            sugg_color = (0.90, 0.24, 0.24, 1)  # rosso
        elif bet_info['action'] == 'MIN_BET':
            sugg_text = f"{sugg_text}[b]€{suggested:.0f} ({self.t('min_bet')})[/b]"
            sugg_color = (0.96, 0.68, 0.35, 1)  # arancione
        else:  # BET
            sugg_text = f"{sugg_text}[b]€{suggested:.0f} ({self.t('high_count')})[/b]"
            sugg_color = (0.93, 0.79, 0.29, 1)  # oro
        
        self.suggested_bet_label.text = sugg_text
        self.suggested_bet_label.color = sugg_color
        
        # Aggiorna bet input solo all'inizio mano (nessuna mano in gioco)
        all_hands_empty = all(len(hand) == 0 for hand in self.player_hands)
        if all_hands_empty and not self.dealer_cards and not self.table_cards:
            self.bet_input.text = f"{suggested:.0f}"
        
        # Mostra/nascondi bottone split
        if len(current_hand) == 2 and len(self.player_hands) < self.max_hands:
            # Controlla se è una coppia (stesso valore)
            if self.get_card_value(current_hand[0]) == self.get_card_value(current_hand[1]):
                self.activate_split_btn.opacity = 1
                self.activate_split_btn.disabled = False
            else:
                self.activate_split_btn.opacity = 0
                self.activate_split_btn.disabled = True
        else:
            self.activate_split_btn.opacity = 0
            self.activate_split_btn.disabled = True
        
        # Abilita/disabilita bottoni navigazione
        if total_hands > 1:
            # Mostra sempre i bottoni quando ci sono più mani
            self.prev_hand_btn.opacity = 1
            self.next_hand_btn.opacity = 1
            
            # Disabilita freccia sinistra se siamo alla prima mano
            self.prev_hand_btn.disabled = (self.current_hand_index == 0)
            # Disabilita freccia destra se siamo all'ultima mano
            self.next_hand_btn.disabled = (self.current_hand_index == total_hands - 1)
        else:
            # Nascondi i bottoni se c'è solo una mano
            self.prev_hand_btn.opacity = 0
            self.prev_hand_btn.disabled = True
            self.next_hand_btn.opacity = 0
            self.next_hand_btn.disabled = True
    
    def adjust_bet_value(self, amount):
        """Aggiunge o toglie un valore alla scommessa in base alla modalità selezionata (+/-)"""
        try:
            current = float(self.bet_input.text.strip())
            
            # Controlla quale modalità è selezionata
            if self.bet_mode_plus.state == 'down':
                # Modalità +: aggiungi
                new_bet = current + amount
            else:
                # Modalità -: togli
                new_bet = current - amount
            
            # Minimo 1€
            new_bet = max(1, new_bet)
            self.bet_input.text = f"{new_bet:.0f}"
        except:
            pass
    
    def record_result(self, result):
        """Registra risultato della mano corrente"""
        try:
            bet = float(self.bet_input.text.strip())
        except:
            self.show_toast(self.t('invalid_bet'))
            return
        
        total_hands = len(self.player_hands)
        
        # Controlla se questa mano ha già un risultato registrato
        if len(self.hand_results) > self.current_hand_index and self.hand_results[self.current_hand_index] is not None:
            self.show_toast(self.t('hand_already_registered', self.current_hand_index + 1))
            return
        
        # Registra il risultato per la mano corrente
        if result == 'win':
            self.card_counter.record_hand_result('win', bet)
            toast_msg = self.t('hand_won', self.current_hand_index + 1, bet)
        elif result == 'lose':
            self.card_counter.record_hand_result('loss', bet)
            toast_msg = self.t('hand_lost', self.current_hand_index + 1, bet)
        elif result == 'push':
            self.card_counter.record_hand_result('push', bet)
            toast_msg = self.t('hand_push', self.current_hand_index + 1)
        elif result == 'blackjack':
            self.card_counter.record_hand_result('blackjack', bet)
            blackjack_win = bet * 1.5
            toast_msg = self.t('hand_blackjack', self.current_hand_index + 1, blackjack_win)
        elif result == 'double_win':
            self.card_counter.record_hand_result('win', bet * 2)
            toast_msg = self.t('hand_double_win', self.current_hand_index + 1, bet * 2)
        elif result == 'double_loss':
            self.card_counter.record_hand_result('loss', bet * 2)
            toast_msg = self.t('hand_double_loss', self.current_hand_index + 1, bet * 2)
        elif result == 'surrender':
            self.card_counter.record_hand_result('loss', bet * 0.5)
            toast_msg = self.t('hand_surrender', self.current_hand_index + 1, bet * 0.5)
            toast_msg = f"Mano {self.current_hand_index + 1} arresa. -€{bet * 0.5:.0f}"
        
        # Salva il risultato
        if len(self.hand_results) == 0:
            self.hand_results = [None] * total_hands
        self.hand_results[self.current_hand_index] = result
        
        # Mostra il risultato
        self.show_toast(toast_msg)
        
        # Controlla se ci sono altre mani da completare
        all_completed = all(r is not None for r in self.hand_results[:total_hands])
        
        if not all_completed:
            # Cerca la prossima mano non completata
            next_hand = None
            for i in range(self.current_hand_index + 1, total_hands):
                if self.hand_results[i] is None:
                    next_hand = i
                    break
            
            if next_hand is None:
                # Cerca dall'inizio
                for i in range(0, self.current_hand_index):
                    if self.hand_results[i] is None:
                        next_hand = i
                        break
            
            if next_hand is not None:
                # Passa alla prossima mano
                self.current_hand_index = next_hand
                self.update_display()
                self.show_toast(self.t('register_hand', next_hand + 1, total_hands))
        else:
            # Tutte le mani completate - reset completo
            self.show_toast(self.t('all_hands_completed'))
            self._complete_hand_reset()
    
    def _complete_hand_reset(self, *args):
        """Reset completo dopo aver registrato tutte le mani"""
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        self.hand_results = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        self.prev_hand_btn.opacity = 0
        self.prev_hand_btn.disabled = True
        self.next_hand_btn.opacity = 0
        self.next_hand_btn.disabled = True
        
        self.update_display()
    
    def record_insurance_loss(self):
        """Registra la perdita dell'assicurazione (metà della puntata)"""
        try:
            bet = float(self.bet_input.text.strip())
        except:
            self.show_toast(self.t('invalid_bet'))
            return
        
        insurance_amount = bet * 0.5
        # Sottrai l'assicurazione dal bankroll senza resettare la mano
        self.card_counter.current_bankroll -= insurance_amount
        
        self.show_toast(self.t('insurance_lost', insurance_amount))
        
        # Aggiorna solo il display, senza resettare le carte
        self.update_display()
    
    def skip_hand(self):
        """Salta/osserva la mano senza registrare risultati (mantiene il conteggio delle carte)"""
        # Reset mani
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        self.hand_results = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        self.prev_hand_btn.opacity = 0
        self.prev_hand_btn.disabled = True
        self.next_hand_btn.opacity = 0
        self.next_hand_btn.disabled = True
        
        self.show_toast(self.t('hand_skipped'))
        self.update_display()
    
    def delete_last_card(self):
        """Cancella l'ultima carta inserita della sezione selezionata (BANCO, MIO o TAVOLO)"""
        card_to_remove = None
        section_name = ""
        
        # Determina quale sezione cancellare in base alla modalità selezionata
        if self.mode == 'banco':
            if self.dealer_cards:
                card_to_remove = self.dealer_cards.pop()
                section_name = "BANCO"
            else:
                self.show_toast(self.t('no_cards_dealer'))
                return
        elif self.mode == 'mio':
            # Cancella dall'ultima mano che contiene carte
            for i in range(len(self.player_hands) - 1, -1, -1):
                if self.player_hands[i]:
                    card_to_remove = self.player_hands[i].pop()
                    section_name = f"MIO (Mano {i+1})"
                    
                    # Rimuovi la mano se è vuota e non è la prima
                    if not self.player_hands[i] and len(self.player_hands) > 1:
                        self.player_hands.pop(i)
                        # Aggiusta l'indice se necessario
                        if self.current_hand_index >= len(self.player_hands):
                            self.current_hand_index = len(self.player_hands) - 1
                        # Nascondi bottoni navigazione se rimane solo una mano
                        if len(self.player_hands) == 1:
                            self.prev_hand_btn.opacity = 0
                            self.prev_hand_btn.disabled = True
                            self.next_hand_btn.opacity = 0
                            self.next_hand_btn.disabled = True
                    break
            
            if card_to_remove is None:
                self.show_toast("Nessuna carta nelle tue mani")
                return
        else:  # tavolo
            if self.table_cards:
                card_to_remove = self.table_cards.pop()
                section_name = "TAVOLO"
            else:
                self.show_toast("Nessuna carta nel TAVOLO")
                return
        
        # Rimuovi dal contatore
        if card_to_remove:
            self.card_counter.remove_card(card_to_remove)
            self.update_display()
            self.show_toast(f"Cancellato {card_to_remove} da {section_name}")
    
    def set_table_settings(self):
        """Imposta bankroll e minima tavolo (cambio tavolo)"""
        try:
            bankroll = float(self.bankroll_input.text) if self.bankroll_input else 100
            min_bet = float(self.min_bet_input.text) if self.min_bet_input else 5
        except:
            self.show_toast("Valori non validi")
            return
        
        self.card_counter.set_bankroll(bankroll)
        self.card_counter.set_table_minimum(min_bet)
        
        # Reset mani correnti
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        self.hand_results = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        if hasattr(self, 'prev_hand_btn'):
            self.prev_hand_btn.opacity = 0
            self.prev_hand_btn.disabled = True
        if hasattr(self, 'next_hand_btn'):
            self.next_hand_btn.opacity = 0
            self.next_hand_btn.disabled = True
        if hasattr(self, 'activate_split_btn'):
            self.activate_split_btn.opacity = 0
            self.activate_split_btn.disabled = True
        
        self.update_display()
        self.show_toast(self.t('table_settings', bankroll, min_bet))
        
        # Chiudi popup setup
        if hasattr(self, 'setup_popup'):
            self.setup_popup.dismiss()
    
    def new_shoe(self):
        """Nuova shoe (resetta solo il conteggio, mantiene bankroll)"""
        try:
            decks = float(self.decks_input.text) if self.decks_input else 6
        except:
            self.show_toast(self.t('invalid_deck_number'))
            return
        
        # Salva i valori da mantenere
        current_bankroll = getattr(self.card_counter, 'current_bankroll', 100)
        initial_bankroll = getattr(self.card_counter, 'initial_bankroll', 100)
        table_minimum = getattr(self.card_counter, 'table_minimum', 5)
        betting_unit = getattr(self.card_counter, 'betting_unit', 10)
        hands_played = getattr(self.card_counter, 'hands_played', 0)
        hands_won = getattr(self.card_counter, 'hands_won', 0)
        hands_lost = getattr(self.card_counter, 'hands_lost', 0)
        hands_pushed = getattr(self.card_counter, 'hands_pushed', 0)
        
        # Resetta solo conteggio carte
        self.card_counter.running_count = 0
        self.card_counter.cards_seen = 0
        self.card_counter.decks_remaining = decks
        self.card_counter.total_cards = decks * 52
        self.card_counter._init_card_tracking()
        
        # Ripristina tutti i valori da mantenere
        self.card_counter.current_bankroll = current_bankroll
        self.card_counter.initial_bankroll = initial_bankroll
        self.card_counter.table_minimum = table_minimum
        self.card_counter.betting_unit = betting_unit
        self.card_counter.hands_played = hands_played
        self.card_counter.hands_won = hands_won
        self.card_counter.hands_lost = hands_lost
        self.card_counter.hands_pushed = hands_pushed
        
        # Reset mani correnti
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        self.hand_results = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        if hasattr(self, 'prev_hand_btn'):
            self.prev_hand_btn.opacity = 0
            self.prev_hand_btn.disabled = True
        if hasattr(self, 'next_hand_btn'):
            self.next_hand_btn.opacity = 0
            self.next_hand_btn.disabled = True
        if hasattr(self, 'activate_split_btn'):
            self.activate_split_btn.opacity = 0
            self.activate_split_btn.disabled = True
        
        self.update_display()
        self.show_toast(self.t('new_shoe_msg', decks))
        
        # Chiudi popup setup
        if hasattr(self, 'setup_popup'):
            self.setup_popup.dismiss()
    
    def reset_all(self):
        """Reset completo (tutto da zero)"""
        try:
            bankroll = float(self.bankroll_input.text) if self.bankroll_input else 100
            decks = float(self.decks_input.text) if self.decks_input else 6
            min_bet = float(self.min_bet_input.text) if self.min_bet_input else 5
        except:
            self.show_toast(self.t('invalid_values'))
            return
        
        # Reset completo
        self.card_counter = CardCounter()
        self.card_counter.set_decks(decks)
        self.card_counter.initial_bankroll = bankroll
        self.card_counter.current_bankroll = bankroll
        self.card_counter.set_table_minimum(min_bet)
        self.strategy = BlackjackStrategy(self.language)
        
        # Reset mani correnti
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        self.hand_results = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        if hasattr(self, 'prev_hand_btn'):
            self.prev_hand_btn.opacity = 0
            self.prev_hand_btn.disabled = True
        if hasattr(self, 'next_hand_btn'):
            self.next_hand_btn.opacity = 0
            self.next_hand_btn.disabled = True
        if hasattr(self, 'activate_split_btn'):
            self.activate_split_btn.opacity = 0
            self.activate_split_btn.disabled = True
        
        self.update_display()
        self.show_toast(self.t('reset_complete'))
        
        # Chiudi popup setup
        if hasattr(self, 'setup_popup'):
            self.setup_popup.dismiss()
    
    def reset_current_hand(self):
        """Resetta solo la mano corrente, rimuovendo le carte dal conteggio"""
        # Rimuovi tutte le carte della mano corrente dal conteggio
        for card in self.dealer_cards:
            self.card_counter.remove_card(card)
        for hand in self.player_hands:
            for card in hand:
                self.card_counter.remove_card(card)
        for card in self.table_cards:
            self.card_counter.remove_card(card)
        
        # Reset mani correnti
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        if hasattr(self, 'prev_hand_btn'):
            self.prev_hand_btn.opacity = 0
            self.prev_hand_btn.disabled = True
        if hasattr(self, 'next_hand_btn'):
            self.next_hand_btn.opacity = 0
            self.next_hand_btn.disabled = True
        if hasattr(self, 'activate_split_btn'):
            self.activate_split_btn.opacity = 0
            self.activate_split_btn.disabled = True
        
        self.update_display()
        self.show_toast("Mano resettata")
        
        # Chiudi popup setup
        if hasattr(self, 'setup_popup'):
            self.setup_popup.dismiss()


if __name__ == '__main__':
    BlackjackApp().run()
