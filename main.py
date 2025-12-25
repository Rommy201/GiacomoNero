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
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import platform

from card_counter import CardCounter
from strategy import BlackjackStrategy

# Imposta dimensione solo su desktop, non su Android
if platform != 'android':
    Window.size = (420, 850)
Window.clearcolor = (0.059, 0.078, 0.098, 1)  # #0f1419


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
        self.size_hint = (None, None)
        self.size = (360, 55)
        self.pos_hint = {'center_x': 0.5, 'top': 0.96}
        
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
        # Inizializza con default 100 euro bankroll e 5 euro minima
        self.card_counter.set_bankroll(100)
        self.card_counter.set_table_minimum(5)
        self.strategy = BlackjackStrategy()
        self.mode = "banco"
        
        # Gestione mani localmente
        self.dealer_cards = []
        self.player_hands = [[]]  # Lista di mani del giocatore (supporta split multipli)
        self.table_cards = []  # Carte altri giocatori
        
        # Gestione split multipli
        self.current_hand_index = 0  # Indice della mano corrente
        self.max_hands = 4  # Massimo 4 mani (come nei casinò reali)
        
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
            font_size='16sp',
            size_hint_x=0.7
        )
        
        setup_btn = Button(
            text='SETUP',
            background_color=(0.3, 0.8, 0.77, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='13sp',
            bold=True,
            size_hint_x=0.3
        )
        setup_btn.bind(on_press=lambda x: self.open_setup())
        self.make_rounded_button(setup_btn, radius=10)
        
        header.add_widget(title)
        header.add_widget(setup_btn)
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
            color=(0.3, 0.8, 0.77, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.cards_label = Label(
            text='[b]312[/b] carte',
            markup=True,
            color=(0.58, 0.88, 0.83, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.viste_label = Label(
            text='[b]0[/b] viste',
            markup=True,
            color=(0.60, 0.59, 0.95, 1),
            font_size='13sp',
            halign='center'
        )
        
        self.decks_label = Label(
            text='[b]6.0[/b] mazzi',
            markup=True,
            color=(0.965, 0.616, 0.043, 1),
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
            color=(0.28, 0.73, 0.44, 1),
            font_size='16sp',
            halign='left',
            valign='middle',
            size_hint_x=0.35
        )
        self.bankroll_label.bind(size=self.bankroll_label.setter('text_size'))
        
        self.profit_label = Label(
            text='(+€0)',
            color=(0.96, 0.68, 0.35, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_x=0.35
        )
        self.profit_label.bind(size=self.profit_label.setter('text_size'))
        
        self.suggested_bet_label = Label(
            text='Sugg: [b]€10[/b]',
            markup=True,
            color=(0.93, 0.79, 0.29, 1),
            font_size='11sp',
            halign='right',
            valign='middle',
            size_hint_x=0.3
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
            font_size='11sp',
            halign='left',
            valign='middle',
            size_hint_x=0.7
        )
        self.hands_summary_label.bind(size=self.hands_summary_label.setter('text_size'))
        
        self.winrate_label = Label(
            text='WR: 0%',
            color=(0.7, 0.7, 0.7, 1),
            font_size='11sp',
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
        
        # Bottoni modalità + Annulla (verticale, sinistra)
        mode_buttons = BoxLayout(orientation='vertical', size_hint_x=None, width=85, spacing=5)
        
        self.mode_banco_btn = ToggleButton(
            text='BANCO',
            group='mode',
            state='down',
            background_color=(0.90, 0.24, 0.24, 1),
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
            background_color=(0.12, 0.35, 0.23, 1),
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
            background_color=(0.55, 0.42, 0.12, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True,
            size_hint_y=0.25
        )
        self.mode_tavolo_btn.bind(on_press=lambda x: self.set_mode('tavolo'))
        self.make_rounded_button(self.mode_tavolo_btn, radius=8)
        
        # Bottone ANNULLA sotto i radio
        undo_btn = Button(
            text='UNDO',
            background_color=(0.3, 0.8, 0.77, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=0.25
        )
        undo_btn.bind(on_press=lambda x: self.undo_hand())
        self.make_rounded_button(undo_btn, radius=8)
        
        mode_buttons.add_widget(self.mode_banco_btn)
        mode_buttons.add_widget(self.mode_mio_btn)
        mode_buttons.add_widget(self.mode_tavolo_btn)
        mode_buttons.add_widget(undo_btn)
        
        # Griglia carte 4x4 (13 carte)
        cards_grid = GridLayout(cols=4, spacing=5, size_hint_x=1)
        
        card_data = [
            ('A', (0.90, 0.24, 0.24, 1)),
            ('2', (0.22, 0.63, 0.41, 1)),
            ('3', (0.22, 0.63, 0.41, 1)),
            ('4', (0.22, 0.63, 0.41, 1)),
            ('5', (0.22, 0.63, 0.41, 1)),
            ('6', (0.22, 0.63, 0.41, 1)),
            ('7', (0.93, 0.79, 0.29, 1)),
            ('8', (0.93, 0.79, 0.29, 1)),
            ('9', (0.93, 0.79, 0.29, 1)),
            ('10', (0.90, 0.24, 0.24, 1)),
            ('J', (0.90, 0.24, 0.24, 1)),
            ('Q', (0.90, 0.24, 0.24, 1)),
            ('K', (0.90, 0.24, 0.24, 1)),
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
            size_hint_y=0.25,
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
        
        hand_title = Label(
            text='[b]MANO[/b]',
            markup=True,
            color=(0.28, 0.73, 0.44, 1),
            font_size='11sp',
            size_hint_y=0.12,
            halign='center',
            valign='top'
        )
        hand_title.bind(size=hand_title.setter('text_size'))
        
        self.dealer_label = Label(
            text='Banco: -',
            color=(0.90, 0.24, 0.24, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            size_hint_y=0.13
        )
        self.dealer_label.bind(size=self.dealer_label.setter('text_size'))
        
        self.player_label = Label(
            text='Io: -',
            color=(0.3, 0.8, 0.77, 1),
            font_size='10sp',
            halign='left',
            valign='middle',
            size_hint_y=0.24
        )
        self.player_label.bind(size=self.player_label.setter('text_size'))
        
        # Label per seconda mano (split)
        self.player_split_label = Label(
            text='Mano 2: -',
            color=(0.58, 0.88, 0.83, 1),
            font_size='10sp',
            halign='left',
            valign='middle',
            size_hint_y=0.12
        )
        self.player_split_label.bind(size=self.player_split_label.setter('text_size'))
        
        self.table_label = Label(
            text='Tavolo: -',
            color=(0.6, 0.6, 0.6, 1),
            font_size='11sp',
            halign='left',
            valign='top',
            size_hint_y=0.35
        )
        self.table_label.bind(size=self.table_label.setter('text_size'))
        
        # Bottoni split e navigazione
        split_buttons = BoxLayout(orientation='horizontal', size_hint_y=0.16, spacing=2)
        
        self.activate_split_btn = Button(
            text='SPLIT',
            background_color=(0.50, 0.35, 0.84, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='10sp',
            bold=True
        )
        self.activate_split_btn.bind(on_press=lambda x: self.activate_split())
        self.make_rounded_button(self.activate_split_btn, radius=6)
        
        # Bottone freccia sinistra per mano precedente
        self.prev_hand_btn = Button(
            text='<',
            background_color=(0.26, 0.60, 0.88, 1),
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
            background_color=(0.26, 0.60, 0.88, 1),
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
        
        hand_box.add_widget(hand_title)
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
        
        action_title = Label(
            text='[b]AZIONE[/b]',
            markup=True,
            color=(0.96, 0.68, 0.35, 1),
            font_size='11sp',
            size_hint_y=0.12,
            halign='center',
            valign='top'
        )
        action_title.bind(size=action_title.setter('text_size'))
        
        self.strategy_label = Label(
            text='Inserisci carte',
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True,
            halign='center',
            valign='middle'
        )
        self.strategy_label.bind(size=self.strategy_label.setter('text_size'))
        
        action_box.add_widget(action_title)
        action_box.add_widget(self.strategy_label)
        
        game_info.add_widget(hand_box)
        game_info.add_widget(action_box)
        main_layout.add_widget(game_info)
        
        # === RISULTATI CON INPUT SCOMMESSA ===
        results_section = BoxLayout(
            orientation='vertical',
            size_hint_y=0.20,
            padding=[10, 12, 10, 10],
            spacing=8
        )
        
        # Input scommessa
        bet_input_box = BoxLayout(orientation='horizontal', size_hint_y=0.22, spacing=6, padding=[0, 0])
        
        bet_label = Label(
            text='Puntata:',
            color=(0.96, 0.68, 0.35, 1),
            font_size='12sp',
            bold=True,
            size_hint_x=0.28,
            halign='right',
            valign='middle'
        )
        bet_label.bind(size=bet_label.setter('text_size'))
        
        initial_bet = self.card_counter.get_bet_multiplier()['bet_amount']
        self.bet_input = TextInput(
            text=f'{initial_bet:.0f}€',
            multiline=False,
            font_size='13sp',
            size_hint_x=0.55,
            background_color=(0.146, 0.168, 0.231, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.8, 0.77, 1),
            padding=[10, 6],
            halign='center'
        )
        
        bet_input_box.add_widget(bet_label)
        bet_input_box.add_widget(self.bet_input)
        bet_input_box.add_widget(Label(size_hint_x=0.17))  # Spacer
        
        # Bottoni risultato
        row1 = BoxLayout(orientation='horizontal', spacing=4, size_hint_y=0.39)
        
        win_btn = Button(
            text='VINTO',
            background_color=(0.28, 0.73, 0.44, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        win_btn.bind(on_press=lambda x: self.record_result('win'))
        self.make_rounded_button(win_btn, radius=8)
        
        push_btn = Button(
            text='PAREGGIO',
            background_color=(0.6, 0.59, 0.95, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        push_btn.bind(on_press=lambda x: self.record_result('push'))
        self.make_rounded_button(push_btn, radius=8)
        
        lose_btn = Button(
            text='PERSO',
            background_color=(0.90, 0.24, 0.24, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True
        )
        lose_btn.bind(on_press=lambda x: self.record_result('lose'))
        self.make_rounded_button(lose_btn, radius=8)
        
        # Bottone blackjack (nella stessa riga)
        bj_btn = Button(
            text='BJ',
            background_color=(0.93, 0.79, 0.29, 1),
            background_normal='',
            color=(0.1, 0.1, 0.1, 1),
            font_size='12sp',
            bold=True
        )
        bj_btn.bind(on_press=lambda x: self.record_result('blackjack'))
        self.make_rounded_button(bj_btn, radius=8)
        
        row1.add_widget(win_btn)
        row1.add_widget(push_btn)
        row1.add_widget(lose_btn)
        row1.add_widget(bj_btn)
        
        # Seconda riga: Double e Surrender
        row2 = BoxLayout(orientation='horizontal', spacing=4, size_hint_y=0.39)
        
        self.double_win_btn = Button(
            text='2x WIN',
            background_color=(0.18, 0.37, 0.18, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        self.double_win_btn.bind(on_press=lambda x: self.record_result('double_win'))
        self.make_rounded_button(self.double_win_btn, radius=8)
        
        self.double_loss_btn = Button(
            text='2x LOSS',
            background_color=(0.49, 0.18, 0.18, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        self.double_loss_btn.bind(on_press=lambda x: self.record_result('double_loss'))
        self.make_rounded_button(self.double_loss_btn, radius=8)
        
        self.surrender_btn = Button(
            text='ARRESA',
            background_color=(0.37, 0.35, 0.47, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        self.surrender_btn.bind(on_press=lambda x: self.record_result('surrender'))
        self.make_rounded_button(self.surrender_btn, radius=8)
        
        row2.add_widget(self.double_win_btn)
        row2.add_widget(self.double_loss_btn)
        row2.add_widget(self.surrender_btn)
        
        results_section.add_widget(bet_input_box)
        results_section.add_widget(row1)
        results_section.add_widget(row2)
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
        
        return root
    
    def show_toast(self, message):
        """Mostra toast notification"""
        if hasattr(self, 'toast_widget') and self.toast_widget:
            self.root.remove_widget(self.toast_widget)
        
        self.toast_widget = ToastWidget(message)
        self.root.add_widget(self.toast_widget)
        
        Clock.schedule_once(lambda dt: self.root.remove_widget(self.toast_widget), 2)
    
    def open_setup(self):
        """Apre il popup di setup"""
        # Contenuto del popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        # Titolo
        title = Label(
            text='[b]SETUP[/b]',
            markup=True,
            color=(0.3, 0.8, 0.77, 1),
            font_size='14sp',
            size_hint_y=0.10
        )
        content.add_widget(title)
        
        # Mazzi rimasti
        decks_box = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=10)
        decks_label = Label(
            text='Mazzi rimasti:',
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
            text='Bankroll €:',
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
            text='Minimo tavolo €:',
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
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.2))
        
        # Bottone per impostare tavolo
        set_table_btn = Button(
            text='IMPOSTA TAVOLO',
            background_color=(0.28, 0.73, 0.44, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=None,
            height=45
        )
        set_table_btn.bind(on_press=lambda x: self.set_table_settings())
        self.make_rounded_button(set_table_btn, radius=10)
        content.add_widget(set_table_btn)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.1))
        
        # Bottone reset mano corrente
        reset_hand_btn = Button(
            text='↺ RESET MANO',
            background_color=(0.965, 0.616, 0.043, 1),  # Amber
            background_normal='',
            color=(0.039, 0.055, 0.102, 1),  # Dark text
            font_size='12sp',
            bold=True,
            size_hint_y=0.16
        )
        reset_hand_btn.bind(on_press=lambda x: self.reset_current_hand())
        self.make_rounded_button(reset_hand_btn, radius=10)
        content.add_widget(reset_hand_btn)
        
        # Spazio
        content.add_widget(Label(size_hint_y=0.1))
        
        # Bottoni azioni
        actions_row = BoxLayout(orientation='horizontal', size_hint_y=0.16, spacing=8)
        
        new_shoe_btn = Button(
            text='NUOVA SHOE',
            background_color=(0.3, 0.8, 0.77, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        new_shoe_btn.bind(on_press=lambda x: self.new_shoe())
        self.make_rounded_button(new_shoe_btn, radius=8)
        
        reset_all_btn = Button(
            text='RESET TUTTO',
            background_color=(0.90, 0.24, 0.24, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='11sp',
            bold=True
        )
        reset_all_btn.bind(on_press=lambda x: self.reset_all())
        self.make_rounded_button(reset_all_btn, radius=8)
        
        actions_row.add_widget(new_shoe_btn)
        actions_row.add_widget(reset_all_btn)
        content.add_widget(actions_row)
        
        # Bottone chiudi
        close_btn = Button(
            text='CHIUDI',
            background_color=(0.6, 0.59, 0.95, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='12sp',
            bold=True,
            size_hint_y=None,
            height=40
        )
        self.make_rounded_button(close_btn, radius=8)
        
        # Crea popup
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.6),
            background_color=(0.059, 0.078, 0.098, 1),
            separator_color=(0.3, 0.8, 0.77, 1)
        )
        
        # Salva riferimento al popup per chiuderlo dalle azioni
        self.setup_popup = popup
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()
    
    def set_mode(self, mode):
        """Cambia modalità"""
        self.mode = mode
        
        # Colori scuri per non selezionati, brillanti per selezionato
        if mode == 'banco':
            self.mode_banco_btn.background_color = (0.90, 0.24, 0.24, 1)
            self.mode_mio_btn.background_color = (0.12, 0.35, 0.23, 1)
            self.mode_tavolo_btn.background_color = (0.55, 0.42, 0.12, 1)
        elif mode == 'mio':
            self.mode_banco_btn.background_color = (0.49, 0.13, 0.13, 1)
            self.mode_mio_btn.background_color = (0.22, 0.63, 0.41, 1)
            self.mode_tavolo_btn.background_color = (0.55, 0.42, 0.12, 1)
        else:  # tavolo
            self.mode_banco_btn.background_color = (0.49, 0.13, 0.13, 1)
            self.mode_mio_btn.background_color = (0.12, 0.35, 0.23, 1)
            self.mode_tavolo_btn.background_color = (0.93, 0.79, 0.29, 1)
    
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
            
            # Mostra bottoni navigazione
            self.prev_hand_btn.opacity = 1
            self.prev_hand_btn.disabled = False
            self.next_hand_btn.opacity = 1
            self.next_hand_btn.disabled = False
            
            self.update_display()
            total_hands = len(self.player_hands)
            self.show_toast(f"SPLIT! Ora hai {total_hands} mani")
        elif len(self.player_hands) >= self.max_hands:
            self.show_toast(f"Massimo {self.max_hands} mani")
    
    def navigate_hands(self, direction):
        """Naviga tra le mani (-1 per precedente, +1 per successiva)"""
        new_index = self.current_hand_index + direction
        
        # Verifica limiti
        if 0 <= new_index < len(self.player_hands):
            self.current_hand_index = new_index
            self.update_display()
            self.show_toast(f"Giocando Mano {self.current_hand_index + 1}/{len(self.player_hands)}")
    
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
        self.cards_label.text = f'[b]{cards_remaining}[/b] carte'
        
        # Mazzi rimanenti
        decks_remaining = getattr(self.card_counter, 'decks_remaining', 6)
        decks_used = cards_seen / 52
        decks_left = max(decks_remaining - decks_used, 0)
        self.decks_label.text = f'[b]{decks_left:.1f}[/b] mazzi'
        
        # Mano banco
        if self.dealer_cards:
            dealer_total, dealer_soft = self.calculate_hand_value(self.dealer_cards)
            if dealer_soft:
                self.dealer_label.text = f"Banco: {', '.join(self.dealer_cards)} ({dealer_total})"
            else:
                self.dealer_label.text = f"Banco: {', '.join(self.dealer_cards)} ({dealer_total})"
        else:
            self.dealer_label.text = "Banco: -"
        
        # Mano giocatore (mostra solo la mano corrente)
        current_hand = self.player_hands[self.current_hand_index]
        total_hands = len(self.player_hands)
        
        if current_hand:
            player_total, player_soft = self.calculate_hand_value(current_hand)
            cards_text = ', '.join(current_hand)
            
            if total_hands > 1:
                # Con split: mostra "Mano X/Y: carte (totale)"
                hand_display = f"Mano {self.current_hand_index + 1}/{total_hands}: {cards_text} ({player_total})"
            else:
                # Senza split: mostra "Io: carte (totale)"
                hand_display = f"Io: {cards_text} ({player_total})"
        else:
            if total_hands > 1:
                hand_display = f"Mano {self.current_hand_index + 1}/{total_hands}: -"
            else:
                hand_display = "Io: -"
        
        self.player_label.text = hand_display
        
        self.table_label.text = f"Tavolo: {', '.join(self.table_cards) if self.table_cards else '-'}"
        
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
            
            self.strategy_label.text = f"{suggestion['action']}"
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
        self.hands_summary_label.text = f'Mani: [color=10B981]W:{hands_won}[/color] | [color=EF4444]L:{hands_lost}[/color] | [color=9895F3]D:{hands_pushed}[/color]'
        
        if hands_played > 0:
            winrate = (hands_won / hands_played) * 100
            self.winrate_label.text = f"WR: {winrate:.0f}%"
        else:
            self.winrate_label.text = "WR: 0%"
        
        # Puntata suggerita (con markup)
        bet_info = self.card_counter.get_bet_multiplier()
        suggested = bet_info['bet_amount']
        
        # Testo suggerimento con azione
        if bet_info['action'] == 'LEAVE':
            sugg_text = f"ESCI! [b]€{suggested:.0f}[/b]"
            sugg_color = (0.90, 0.24, 0.24, 1)  # rosso
        elif bet_info['action'] == 'MIN_BET':
            sugg_text = f"Min: [b]€{suggested:.0f}[/b]"
            sugg_color = (0.96, 0.68, 0.35, 1)  # arancione
        else:  # BET
            sugg_text = f"Sugg: [b]€{suggested:.0f}[/b]"
            sugg_color = (0.93, 0.79, 0.29, 1)  # oro
        
        self.suggested_bet_label.text = sugg_text
        self.suggested_bet_label.color = sugg_color
        
        # Aggiorna bet input solo all'inizio mano (nessuna mano in gioco)
        all_hands_empty = all(len(hand) == 0 for hand in self.player_hands)
        if all_hands_empty and not self.dealer_cards and not self.table_cards:
            self.bet_input.text = f"{suggested:.0f}€"
        
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
    
    def record_result(self, result):
        """Registra risultato"""
        try:
            bet = float(self.bet_input.text.replace('€', '').strip())
        except:
            self.show_toast("Puntata non valida")
            return
        
        if result == 'win':
            self.card_counter.record_hand_result('win', bet)
            self.show_toast(f"Mano vinta! +€{bet:.0f}")
        elif result == 'lose':
            self.card_counter.record_hand_result('loss', bet)
            self.show_toast(f"Mano persa. -€{bet:.0f}")
        elif result == 'push':
            self.card_counter.record_hand_result('push', bet)
            self.show_toast("= Pareggio (€0)")
        elif result == 'blackjack':
            self.card_counter.record_hand_result('blackjack', bet)
            blackjack_win = bet * 1.5
            self.show_toast(f"BLACKJACK! +€{blackjack_win:.0f}")
        elif result == 'double_win':
            self.card_counter.record_hand_result('win', bet * 2)
            self.show_toast(f"Raddoppio vinto! +€{bet * 2:.0f}")
        elif result == 'double_loss':
            self.card_counter.record_hand_result('loss', bet * 2)
            self.show_toast(f"Raddoppio perso. -€{bet * 2:.0f}")
        elif result == 'surrender':
            self.card_counter.record_hand_result('loss', bet * 0.5)
            self.show_toast(f"Arresa. -€{bet * 0.5:.0f}")
        
        # Reset mani
        self.dealer_cards = []
        self.player_hands = [[]]
        self.table_cards = []
        
        # Reset navigazione split
        self.current_hand_index = 0
        self.prev_hand_btn.opacity = 0
        self.prev_hand_btn.disabled = True
        self.next_hand_btn.opacity = 0
        self.next_hand_btn.disabled = True
        
        self.update_display()
    
    def undo_hand(self):
        """Annulla ultima mano"""
        # Rimuovi l'ultima carta aggiunta dalla mano corrente
        current_hand = self.player_hands[self.current_hand_index]
        if current_hand:
            last_card = current_hand.pop()
            self.card_counter.remove_card(last_card)
        elif self.dealer_cards:
            last_card = self.dealer_cards.pop()
            self.card_counter.remove_card(last_card)
        elif self.table_cards:
            last_card = self.table_cards.pop()
            self.card_counter.remove_card(last_card)
        
        self.update_display()
        self.show_toast("<- Annullato")
    
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
        self.show_toast(f"Tavolo: Bankroll €{bankroll:.2f}, Min €{min_bet:.0f}")
        
        # Chiudi popup setup
        if hasattr(self, 'setup_popup'):
            self.setup_popup.dismiss()
    
    def new_shoe(self):
        """Nuova shoe (resetta solo il conteggio, mantiene bankroll)"""
        try:
            decks = float(self.decks_input.text) if self.decks_input else 6
        except:
            self.show_toast("Numero mazzi non valido")
            return
        
        # Mantieni il bankroll attuale
        current_bankroll = getattr(self.card_counter, 'current_bankroll', 100)
        
        # Resetta conteggio
        self.card_counter.set_decks(decks)
        self.card_counter.running_count = 0
        
        # Ripristina bankroll
        self.card_counter.current_bankroll = current_bankroll
        
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
        self.show_toast(f"Nuova shoe ({decks:.0f} mazzi)")
        
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
            self.show_toast("Valori non validi")
            return
        
        # Reset completo
        self.card_counter = CardCounter()
        self.card_counter.set_decks(decks)
        self.card_counter.initial_bankroll = bankroll
        self.card_counter.current_bankroll = bankroll
        self.card_counter.set_table_minimum(min_bet)
        self.strategy = BlackjackStrategy()
        
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
        self.show_toast("Reset completo")
        
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
