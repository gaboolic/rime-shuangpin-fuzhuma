-- 大写字母处理器
-- 适用于：声笔简码、声笔飞码、声笔飞单、声笔飞讯、声笔小鹤、声笔自然
-- 本处理器可以让大写字母发挥顶屏的作用，或者追加到编码中，同时转换为小写字母
-- 具体行为视方案而定

local rime = require "sbxlm.lib"
local core = require "sbxlm.core"

---@param key_event KeyEvent
---@param env Env
local function process(key_event, env)
  if key_event:release() or key_event:alt() or key_event:ctrl() or key_event:caps() then
    return rime.process_results.kNoop
  end
  local keycode = key_event.keycode
  if keycode < 65 or keycode > 90 then
    return rime.process_results.kNoop
  end
  local context = env.engine.context
  if not context:is_composing() then
    return rime.process_results.kNoop
  end
  local id = env.engine.schema.schema_id
  local third_pop = context:get_option("third_pop")
  local pro_char = context:get_option("pro_char")
  local input = context.input
  -- 在飞讯或三顶模式的简码中，大写字母在 sss 格式的编码之后视为追加编码，用于输入 ssss 格式的多字词
  if core.sss(input) and (core.jm(id) and third_pop or core.fx(id)) then
    goto add
  -- 在飞单或单字模式的飞码、双拼中，大写字母在 ss 格式的编码之后视为追加编码，用于输入 ssss 格式的词
  elseif core.ss(input) and (core.fd(id) or (core.fm(id) or core.sp(id)) and pro_char) then
    goto add
  -- 如果当前有 4 码，那么大写字母顶前两码上屏
  elseif rime.match(input, ".{4}") then
    context:pop_input(2)
    context:confirm_current_selection()
    context:commit()
    context:push_input(input:sub(3))
  -- 其他情况下，大写字母作为顶屏键
  else
    context:confirm_current_selection()
    context:commit()
  end
  ::add::
  -- 大写字母自身转换为小写，追加到编码中
  local char = utf8.char(keycode + 32)
  context:push_input(char)
  return rime.process_results.kAccepted
end

return process
