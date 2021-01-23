#!/usr/bin/python3

import pyautogui as pag
import pytesseract as ptt
import pyscreenshot as pss
import time

import threading

class ClickThread(threading.Thread):
  def __init__(self, click_on):
   super(ClickThread, self).__init__()
   self.click_on = click_on

  def run(self):
   pag.click(self.click_on)


def build_map():
    d = {str(hex(k))[2:]: None for k in range(16**2)}
    for k in d:
        binary_str = str(bin(int('0x'+k, 16)))[2:]
        binary_str = '0'*(8-len(binary_str)) + binary_str
        d[k] = [i for i,e in enumerate(binary_str) if e=='1']
    return d

def build_pmap(bits_position):
    dp = {str(hex(k))[2:]: [] for k in range(16**2)}
    for k in dp:
     binary_str = str(bin(int('0x'+k, 16)))[2:]
     binary_str = '0'*(8-len(binary_str)) + binary_str
     dp[k] = [ClickThread(bits_position[l]) for l in (i for i,e in enumerate(binary_str) if e=='1')]
    return dp


def what_to_shoot(origin):
    screen = pss.grab(bbox=(origin[0], origin[1]-600, origin[0]+470, origin[1]))
    found = ptt.image_to_string(screen, lang='eng', config='-oem 0 -c tessedit_char_whitelist=0123456789ABCDEF')
    print(found)
    screen.show()

def click_on_hex(bits_positions, base_pos, hex_str):
    binary_str = str(bin(int(hex_str, 16)))[2:]
    binary_str = '0'*(8-len(binary_str)) + binary_str
    places_to_click = [i for i,e in enumerate(binary_str) if e=='1']
    for p in places_to_click:
        pag.click(bits_positions[p])
    pag.click(bits_positions[binary_str.find('1')])
    pag.click(bits_positions[7])
    pag.click(base_pos)

def fast_click_on_hex(bits_positions, base_pos, d, hex_str):
    click_on = d[hex_str]
    pag.click(bits_positions[7])
    time.sleep(0.05)
    pag.click(bits_positions[7])
    for p in click_on:
        pag.click(bits_positions[p])
    #pag.click(bits_positions[click_on[0]])
    #pag.click(bits_positions[7])
    pag.click(base_pos)


def parallel_click_on_hex(base_pos, dp, hex_str):
    for t in dp[hex_str]:
      t.start()
    for t in dp[hex_str]:
      t.join()
    dp['1'][0].start()
    dp['1'][0].join()
    pag.click(base_pos)

def key_conv():
    return {'q':'a', 'w':'b', 'e':'c', 'r':'d','t':'e','y':'f'}

script_mouse_pos = pag.position()
click_area = pag.locateOnScreen('click_on_these.png', grayscale=False, confidence=.7)
if click_area is None:
    print('cant find the game in screen')
    exit(1)
print('found: ',click_area.left)
#what_to_shoot((click_area.left,click_area.top))
#exit(0)
#leftmost_bit = (click_area.left+90, click_area.top + click_area.height/2.0) leftmost_bit = (click_area.left, click_area.top + click_area.height/2.0)
leftmost_bit = (click_area.left+30, click_area.top + click_area.height/2.0)
leftmost_bit = (245, click_area.top + click_area.height/2.0)
bits_positions = [(leftmost_bit[0]+i*60, leftmost_bit[1]) for i in range(8)]
print(bits_positions)
d=build_map()
dp =build_pmap(bits_positions)
pag.PAUSE = 0.059
while True:
    hex_str = input("enter the hex:")
    if len(hex_str)<=2:
        #a,b = hex_str[0], hex_str[1]
        #a = d[a] if a in d else a
        #b = d[b] if b in d else b
        #click_on_hex(bits_positions, script_mouse_pos, hex_str)
        fast_click_on_hex(bits_positions, script_mouse_pos, d, hex_str)
        #parallel_click_on_hex(script_mouse_pos, dp, a+b)
print('done')


