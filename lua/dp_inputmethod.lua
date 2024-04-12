-- Copyright (c) 2024 liudepei. All Rights Reserved.
-- create at 2024/04/08 19:15:05 Monday

local M = {}

local sta, B = pcall(require, 'dp_base')

if not sta then return print('Dp_base is required!', debug.getinfo(1)['source']) end

if B.check_plugins {
      -- 'git@github.com:peter-lyr/dp_init',
      'folke/which-key.nvim',
    } then
  return
end

M.enable = 1
M.lang = nil

function M.change_language(lang)
  vim.g.lang = lang
  vim.g.res = 1
  vim.cmd [[
    python << EOF
import win32api
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST
LANG = {
  "ZH": 0x0804,
  "EN": 0x0409
}
try:
  hwnd = win32gui.GetForegroundWindow()
  language = LANG[vim.eval('g:lang')]
  result = win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, language)
  vim.command(f'let g:res = {result}')
  import time
except Exception as e:
  print('change_language - Exception:', e)
EOF
  ]]
  if vim.g.res ~= 0 then
    B.notify_error 'change language error'
  end
  if lang == 'EN' then
    M.lang = 'EN'
  else
    M.lang = 'ZH'
  end
end

B.aucmd('ModeChanged', 'inputmethod.ModeChanged', {
  callback = function()
    if M.enable then
      B.set_timeout(150, function()
        if B.is_in_tbl(vim.fn.mode(), { 'c', 'i', 't', 'r', 'R', }) then
          M.change_language 'ZH'
        else
          M.change_language 'EN'
        end
      end)
    end
  end,
})

B.aucmd('FocusLost', 'inputmethod.FocusLost', {
  callback = function()
    if M.enable then
      B.set_timeout(100, function()
        M.change_language 'ZH'
      end)
    end
  end,
})

B.aucmd('FocusGained', 'inputmethod.FocusGained', {
  callback = function()
    if M.enable then
      B.set_timeout(50, function()
        if B.is_in_tbl(vim.fn.mode(), { 'c', 'i', 't', 'r', 'R', }) then
          M.change_language 'ZH'
        else
          M.change_language 'EN'
        end
      end)
    end
  end,
})

function M.i_enter()
  M.enable = nil
  vim.cmd [[call feedkeys("\<esc>o")]]
  B.set_timeout(100, function() M.enable = 1 end)
end

function M.toggle_lang_in_cmdline()
  if M.lang == 'EN' then
    M.change_language 'ZH'
  else
    M.change_language 'EN'
  end
end

require 'which-key'.register {
  ['<c-F1>'] = { function() M.toggle_lang_in_cmdline() end, 'toggle: EN/ZH', mode = { 'n', 's', 'v', 'c', 'i', 't', }, silent = true, },
  ['<c-;>'] = { function() M.i_enter() end, 'Enter new empty line', mode = { 'i', }, silent = true, },
}

return M
