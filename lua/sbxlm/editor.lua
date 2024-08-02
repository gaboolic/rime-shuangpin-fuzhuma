-- 回头补码处理器
-- 适用于：声笔拼音
-- 本处理器实现了声笔拼音的自动回头补码的功能
-- 即在输入 aeiou 时，如果末音节有 3 码，且前面至少还有一个音节，则将这个编码追加到首音节上
-- 注意，这里的音节是 Rime 中的音节概念，在声笔拼音中对应的是压缩拼音 + 笔画形成的最长 5 码的编码组合，不一定只包含读音信息

local rime = require "sbxlm.lib"

local this = {}

---@param env Env
function this.init(env)
end

---@param key_event KeyEvent
---@param env Env
function this.func(key_event, env)
  local context = env.engine.context
  -- 只对无修饰按键生效
  if key_event.modifier > 0 then
    return rime.process_results.kNoop
  end
  local incoming = key_event:repr()
  -- 如果输入为空格或数字，代表着作文即将上屏，此时把 kConfirmed 的片段改为 kSelected
  -- 这解决了 https://github.com/rime/home/issues/276 中的不造词问题
  if rime.match(incoming, "\\d") or incoming == "space" then
    for _, segment in ipairs(context.composition:toSegmentation():get_segments()) do
      if segment.status == rime.segment_types.kConfirmed then
        segment.status = rime.segment_types.kSelected
      end
    end
  end
  -- 只在纯功模式下生效
  if context:get_option("free") or context:get_option("fixed") then
    return rime.process_results.kNoop
  end
  -- 只对 aeiou 和 Backspace 键生效
  -- 如果输入是 aeiou，则添加一个码
  -- 如果输入是 Backspace，则从之前增加的补码中删除一个码
  if not (rime.match(incoming, "[aeiou]") or incoming == "BackSpace") then
    return rime.process_results.kNoop
  end
  -- 判断是否满足补码条件：末音节有 3 码，且前面至少还有一个音节
  -- confirmed_position 是拼音整句中已经被确认的编码的长度，只有后面的部分是可编辑的
  -- current_input 获取的是这部分的编码
  -- 这样，我们就可以在拼音整句中多次应用补码，而不会影响到已经确认的部分
  local confirmed_position = context.composition:toSegmentation():get_confirmed_position()
  local previous_caret_pos = context.caret_pos
  local current_input = context.input:sub(confirmed_position + 1, previous_caret_pos)
  if not rime.match(current_input, ".+[bpmfdtnlgkhjqxzcsrywv][aeiou]{2}") then
    return rime.process_results.kNoop
  end
  -- 如果输入是 Backspace，还要验证是否有补码
  if incoming == "BackSpace" then
    if not rime.match(current_input, "[bpmfdtnlgkhjqxzcsrywv][aeiou]+.+") then
      return rime.process_results.kNoop
    end
  end
  -- 找出补码的位置（第二个音节之前），并添加补码
  local first_char_code_len = current_input:find("[bpmfdtnlgkhjqxzcsrywv]", 2) - 1
  context.caret_pos = confirmed_position + first_char_code_len
  if incoming == "BackSpace" then
    context:pop_input(1)
  else
    context:push_input(incoming)
  end
  -- 如果补码后不到 5 码，则返回当前的位置，使得补码后的输入可以继续匹配词语；
  -- 如果补码后已有 5 码，则不返回，相当于进入单字模式
  if first_char_code_len < 4 then
    context.caret_pos = previous_caret_pos + 1
  end
  return rime.process_results.kAccepted
end

return this
