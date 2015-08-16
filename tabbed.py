# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:56:00 2014

@author: aduri
"""

#Simple example
'''
TabbedPanel
============

Test of the widget TabbedPanel.
'''

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.knob import Knob
from kivy.garden.gauge import Gauge
from kivy.graphics.vertex_instructions import Line
from random import randint
from kivy.clock import Clock
Builder.load_string("""

<Test>:
    size_hint: 2, 2
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False

    TabbedPanelItem:
        text: 'first tab'  
		size_hint: 20,20
        BoxLayout:
            canvas:
        	    Rectangle:
                    source: 'images/InfineonBackground.jpg'
                	pos: self.pos
                	size: self.size
            Label:
				text:'OIKOS Demo Board'
				pos_hint: {'center_x':.5,'top':1}
				size_hint:None, None
				font_name: 'DroidSans'
				color: (0,.1,1,1)
        Knob:
        	id: knob_value
			size: 75,75
			value: 0
			min:-50
			max:50
			pos_hint: {'x':.1,'y':.7}
			show_label: True
			show_marker: True
			font_size: '18dp'
			font_color:(1,0,0,2)
			knobimg_source: "img/knob_metal.png"
			show_marker: False
        
    TabbedPanelItem:
        text: 'tab2'
        BoxLayout:
            Label:
                text: 'Second tab content area'
            Button:
                text: 'Button that does nothing'
    TabbedPanelItem:
        text: 'tab3'
        RstDocument:
            text: '\\n'.join(("Hello world", "-----------", "You are in the third tab."))

""")

class Test(TabbedPanel):
    pass

class TabbedPanelApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    TabbedPanelApp().run()