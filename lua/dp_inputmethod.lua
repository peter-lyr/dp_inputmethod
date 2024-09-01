-- Copyright (c) 2024 liudepei. All Rights Reserved.
-- create at 2024/04/08 19:15:05 Monday

local M = {}

local sta, B = pcall(require, 'dp_base')

if not sta then return print('Dp_base is required!', debug.getinfo(1)['source']) end

M.source = B.getsource(debug.getinfo(1)['source'])
M.input_method_py = B.get_file_under_source(M.source, 'change-input-method.py')

M.lang = nil

function M.change_language(lang)
  M.lang = lang
  B.system_run('start silent', 'python %s %s', M.input_method_py, lang)
end

B.aucmd('ModeChanged', 'inputmethod.ModeChanged', {
  callback = function()
    if B.is_in_tbl(vim.fn.mode(), { 'c', 'i', 't', 'r', 'R', }) then
      M.change_language 'ZH'
    else
      M.change_language 'EN'
    end
  end,
})

B.aucmd('CmdlineLeave', 'inputmethod.CmdlineLeave', {
  callback = function()
    if B.is_in_tbl(vim.fn.mode(), { 'i', 't', 'r', 'R', }) then
      M.change_language 'ZH'
    else
      M.change_language 'EN'
    end
  end,
})

B.aucmd('FocusLost', 'inputmethod.FocusLost', {
  callback = function()
    if B.is_in_tbl(vim.fn.mode(), { 'c', 'i', 't', 'r', 'R', }) then
      B.write_lines_to_file({ '1', }, [[C:\Windows\Temp\nvim-qt.exe-input-method.txt]])
    else
      B.write_lines_to_file({ '0', }, [[C:\Windows\Temp\nvim-qt.exe-input-method.txt]])
    end
  end,
})

return M
