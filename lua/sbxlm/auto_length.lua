-- 自动码长翻译器
-- 适用于：声笔简码、声笔飞码、声笔飞单、声笔飞讯、声笔小鹤、声笔自然

local rime           = require "sbxlm.lib"
local yield          = rime.yield
local core           = require "sbxlm.core"

local this           = {}
local kEncodedPrefix = "\x7fenc\x1f"
local kTopSymbol     = " \xe2\x98\x86 "
local kUnitySymbol   = " \xe2\x98\xaf "

---@class AutoLengthEnv: Env
---@field static_memory Memory
---@field dynamic_memory Memory
---@field reverse ReverseLookup
---@field enable_filtering boolean
---@field forced_selection boolean
---@field single_selection boolean
---@field single_display boolean
---@field lower_case boolean
---@field stop_change boolean
---@field enable_encoder boolean
---@field delete_threshold number
---@field max_phrase_length number
---@field static_patterns string[]
---@field known_candidates { string: number }
---@field third_pop boolean
---@field fast_char boolean
---@field fast_change boolean
---@field is_buffered boolean

---判断输入的编码是否为静态编码
---@param input string
---@param env AutoLengthEnv
local function static(input, env)
  -- 对简码特殊判断
  if env.third_pop and core.sss(input) then
    return false
  end
  if env.fast_char and core.ssb(input) then
    return true
  end
  -- 对双拼特殊判断
  if env.fast_change and core.sxb(input) and core.sp(env.engine.schema.schema_id) then
    return false
  end
  for _, pattern in ipairs(env.static_patterns) do
    if rime.match(input, pattern) then
      return true
    end
  end
  return false
end

---对词组中的每一个字枚举所有可能的构词码，然后排列组合造词
---在 librime 中，这个函数已经被 TableEncoder 实现，但是 lua 无法调用，所以不得不重写一遍
---未来可能有更优雅的实现方式
---@param phrase string 待造词的短语
---@param position number 下一个需要编码枚举的位置
---@param code string[] 已经完成编码枚举的编码
---@param env AutoLengthEnv
local function dfs_encode(phrase, position, code, env)
  -- 如果已经枚举完所有字，就尝试造词
  -- word_rules 可能会失败，如果失败就返回 false
  if position > utf8.len(phrase) then
    local encoded = core.word_rules(code, env.engine.schema.schema_id)
    if encoded then
      local entry = rime.DictEntry()
      entry.text = phrase
      entry.custom_code = encoded .. " "
      -- 如果词典中已经存在，则不必造词
      env.dynamic_memory:dict_lookup(encoded, false, 1)
      for e in env.dynamic_memory:iter_dict() do
        if e.text == entry.text then
          return false
        end
      end
      env.dynamic_memory:update_userdict(entry, 0, kEncodedPrefix)
      return true
    else
      return false
    end
  end
  -- 把 UTF-8 编码的词语拆成单个字符的列表
  local characters = {}
  for _, char in utf8.codes(phrase) do
    table.insert(characters, utf8.char(char))
  end
  -- 对于飞系方案，构词用的编码不一定出现在单字全面中，所以需要单独的构词码
  -- 对于其他方案，调用单字全码即可，可以减少词库的大小
  local translations = env.reverse:lookup_stems(characters[position])
  if translations == "" then
    translations = env.reverse:lookup(characters[position])
  end
  local success = false
  -- 对所有可能的构词码，逐个入栈，然后递归调用，从而实现各字的构词码之间的排列组合
  for stem in string.gmatch(translations, "[^ ]+") do
    -- 如果之前调用的是 reverse:lookup，那么除了单字全码之外，也可能查询到简码
    -- 这里要把它们过滤掉
    if stem:len() < 4 then
      goto continue
    end
    table.insert(code, stem)
    local ok = dfs_encode(phrase, position + 1, code, env)
    success = success or ok
    table.remove(code)
    ::continue::
  end
  return success
end

---由本翻译器生成的候选上屏时的回调函数
---需要完成两个任务：1. 记忆刚上屏的字词 2. 对上屏历史造词
---@param commit CommitEntry
---@param env AutoLengthEnv
local function callback(commit, env)
  if env.stop_change then
    return
  end
  -- 记忆刚上屏的字词
  for _, entry in ipairs(commit:get()) do
    if static(entry.preedit, env) then
      goto continue
    end
    if entry.comment == kTopSymbol then
      goto continue
    end
    -- 如果这个词之前标记为临时词，就消除这个标记，正式进入词库
   if string.find(entry.custom_code, kEncodedPrefix) then
      local new_entry = rime.DictEntry()
      new_entry.text = entry.text
      new_entry.custom_code = entry.custom_code:sub(kEncodedPrefix:len() + 1)
      env.dynamic_memory:update_userdict(new_entry, 1, "")
    else
      env.dynamic_memory:update_userdict(entry, 1, "")
    end
    ::continue::
  end
  if not env.enable_encoder then
    return
  end
  -- 对上屏历史造词
  local phrase = ""
  -- 允许包含的上屏字词类型
  local valid_types = rime.Set({ "table", "user_table", "sentence", "simplified", "uniquified", "raw", "completion" })
  local index = 0
  for _, record in env.engine.context.commit_history:iter() do
    ---@type string[]
    local code = {}
    -- 如果最后一次上屏是标点顶屏，跳过标点查看前面的部分
    if index == 0 and record.type == "punct" then
      goto continue
    end
    index = index + 1
    -- 如果是其他类型，打断造词
    if not valid_types[record.type] then
      break
    end
    -- librime 的 bug：顶字上屏会产生一个空的 raw 记录，这里要跳过
    if record.type == "raw" then
      if record.text == "" then
        goto continue
      else
        break
      end
    end
    -- 对最末一个上屏的候选
    if phrase:len() == 0 then
      phrase = record.text
      if #commit:get() > 1 then
        dfs_encode(phrase, 1, code, env)
      end
      goto continue
    end
    phrase = record.text .. phrase
    -- 如果造词的长度超过了最大长度，就不再造词
    -- 普通模式下，最大长度是 translator/max_phrase_length
    -- 缓冲模式下，最大长度是 12
    if env.is_buffered and utf8.len(phrase) > 12 then
      break
    elseif not env.is_buffered and utf8.len(phrase) > env.max_phrase_length then
      break
    end
    dfs_encode(phrase, 1, code, env)
    ::continue::
  end
end

---@param env AutoLengthEnv
function this.init(env)
  env.static_memory = rime.Memory(env.engine, env.engine.schema)
  env.dynamic_memory = rime.Memory1(env.engine, env.engine.schema, "extended")
  local config = env.engine.schema.config
  env.reverse = core.reverse(env.engine.schema.schema_id)
  env.enable_filtering = config:get_bool("translator/enable_filtering") or false
  env.forced_selection = config:get_bool("translator/forced_selection") or false
  env.single_selection = config:get_bool("translator/single_selection") or false
  env.lower_case = config:get_bool("translator/lower_case") or false
  env.stop_change = config:get_bool("translator/stop_change") or false
  env.enable_encoder = config:get_bool("translator/enable_encoder") or false
  env.delete_threshold = config:get_int("translator/delete_threshold") or 1000
  env.max_phrase_length = config:get_int("translator/max_phrase_length") or 4
  env.static_patterns = rime.get_string_list(config, "translator/disable_user_dict_for_patterns");
  env.dynamic_memory:memorize(function(commit) callback(commit, env) end)
  ---@type { string: number }
  env.known_candidates = {}
  env.is_buffered = env.engine.context:get_option("is_buffered") or false
  env.single_display = env.engine.context:get_option("single_display") or false
end

---涉及到自动码长翻译时，指定对特定类型的输入应该用何种策略翻译
---@enum DynamicCodeType
local dtypes = {
  --- 不适用于自动码长翻译
  invalid = -1,
  --- 该编码是自动码长的起始调整位，返回一个权重最高的候选
  short = 0,
  --- 该编码是基本编码的全码
  base = 1,
  --- 该编码是在基本编码的基础上加上了一个选重键
  select = 2,
  --- 该编码是扩展编码的全码
  full = 3,
  --- 类似于声笔拼音，简单前缀匹配即可
  unified = 4,
}

---判断输入的编码是否为动态编码
---如果是，返回应用自动码长翻译的策略
---@param input string
---@param env AutoLengthEnv
---@return DynamicCodeType
local function dynamic(input, env)
  if env.single_selection then
    return dtypes.unified
  end
  local schema_id = env.engine.schema.schema_id
  -- 对于除了飞讯之外的方案来说，基本编码的长度是 4，扩展编码是 6，在 5 码时选重，此外简码还有一个 3 码时的码长调整位
  -- 因此，将编码的长度减去 3 就分别对应了上述的 short, base, select, full 四种情况
  if core.jm(schema_id) or core.fm(schema_id) or core.fd(schema_id) or core.sp(schema_id) then
    return input:len() - 3
  end
  -- 对于飞讯来说，一般情况下基本编码的长度是 5，扩展编码是 7，在 6 码时选重
  -- 因此，将编码的长度减去 4 就分别对应了上述的 short, base, select, full 四种情况
  -- 但是，如果以 sssS 格式输入多字词，那么基本编码的长度是 4，扩展编码是 6，在 5 码时选重
  -- 另外，如果开启快顶模式，则有一个 3 码时的码长调整位
  -- 以下综合考虑了这些情况
  if core.fx(schema_id) then
    if rime.match(input, "[bpmfdtnlgkhjqxzcsrywv]{4}.*") then
      return input:len() - 3
    end
    if input:len() == 4 and not rime.match(input, ".{3}[23789]") then
      return dtypes.invalid
    end
    return input:len() - 4
  end
  return dtypes.invalid
end

-- 飞讯在快顶模式下的换码操作
local fx_exchange = {
  ["2"] = "a",
  ["3"] = "e",
  ["7"] = "u",
  ["8"] = "i",
  ["9"] = "o"
}

---在进行自动码长检索的时候，统一以输入的前三码来模糊匹配固态词典和用户词典中的编码
---然后再比对检索得到的结果和具体的输入内容来进行精确匹配
---如果匹配成功，返回一个 Phrase 对象，否则返回 nil
---@param entry DictEntry
---@param segment Segment
---@param type string
---@param input string
---@param env AutoLengthEnv
---@return Phrase | nil
local function validate_phrase(entry, segment, type, input, env)
  local schema_id = env.engine.schema.schema_id
  -- 一开始，entry.comment 中放置了 "~xxx" 形式的编码补全内容
  -- 对其取子串，得到真正的编码补全内容
  local completion = entry.comment:sub(2)
  local alt_completion = ""
  local to_match = ""
  if entry.comment == "" then
    goto valid
  end
  -- 处理一些特殊的过滤条件
  if env.enable_filtering then
    -- 1. 简码启用多字词过滤时，三码不显示多字词
    if core.jm(schema_id) and input:len() == 3 and utf8.len(entry.text) > 3 then
      return nil
    end
    -- 2. 飞讯启用多字词过滤时，四码不显示多字词
    if core.fx(schema_id) and input:len() >= 4 and utf8.len(entry.text) > 3
        and rime.match(input, "[bpmfdtnlgkhjqxzcsrywv][a-z][bpmfdtnlgkhjqxzcsrywv][aeuio23789][aeuio]*") then
      return nil
    end
  end
  -- 声笔简码和声笔飞讯的多字词有两种输入方式
  -- 在存储时，简码以 sssbbbs 的格式存储，飞讯以 sssbbbbs 的格式存储
  -- 如果识别到这种编码，需要把它们重排一下，得到另一种编码，即以 ssss 开头的编码，然后再进行匹配
  if rime.match(completion, "[aeiou]{3,4}[bpmfdtnlgkhjqxzcsrywv]") then
    alt_completion = completion:sub(-1, -1) .. completion:sub(-3, -2)
    -- 如果简码没启用 lower_case，就消除掉原来的编码，相当于禁用 sssbbb 这种打法
    if core.jm(schema_id) and (not env.lower_case or not env.third_pop) then
      completion = ""
    end
  end
  if input:len() == 3 then
    goto valid
    -- 如果当前的策略是 select，那么最后一码并不代表有效的编码，而是选择键，可以忽略
  elseif dynamic(input, env) == dtypes.select then
    to_match = input:sub(4, -2)
    -- 如果当前的策略是 base, full 或者 short，那么从 4 码开始的部分都要匹配
  else
    to_match = input:sub(4)
  end
  -- 如果第 4 码是 23789，那么需要把它换成 aeiou
  if fx_exchange[to_match:sub(1, 1)] then
    to_match = fx_exchange[to_match:sub(1, 1)] .. to_match:sub(2)
  end
  -- 如果 completion 和 alt_completion 有一个匹配上了，就认为这是一个有效的候选
  if completion:sub(1, to_match:len()) == to_match then
    goto valid
  elseif alt_completion:sub(1, to_match:len()) == to_match then
    completion = alt_completion
    goto valid
  else
    return nil
  end
  ::valid::
  -- 创建一个新的候选，并且把 preedit 设置成输入的内容
  local phrase = rime.Phrase(env.dynamic_memory, type, segment.start, segment._end, entry)
  phrase.preedit = input
  -- 单次选择模式下，显示编码补全内容；否则清空
  if env.single_selection then
    phrase.comment = completion:sub(input:len() - 2)
  else
    phrase.comment = ""
  end
  -- 如果这个候选来自用户词典，根据不同的情况加上不同的标记
  if entry.custom_code:find(kEncodedPrefix) then
    phrase.comment = phrase.comment .. kUnitySymbol
  elseif entry.custom_code:len() > 0 and entry.custom_code:len() < 6 then
    phrase.comment = phrase.comment .. kTopSymbol
  end
  return phrase
end

---@param input string
---@param segment Segment
---@param env AutoLengthEnv
local function translate_by_split(input, segment, env)
  local memory = env.static_memory
  memory:dict_lookup(input:sub(1, 2), false, 1)
  local text = ""
  for entry in memory:iter_dict() do
    text = text .. entry.text
    break
  end
  memory:dict_lookup(input:sub(3), false, 1)
  for entry in memory:iter_dict() do
    ---@type string
    text = text .. entry.text
    break
  end
  local entry = rime.DictEntry()
  entry.text = text
  entry.custom_code = input
  entry.comment = kTopSymbol
  local phrase = rime.Phrase(env.static_memory, "user_table", segment.start, segment._end, entry)
  phrase.preedit = input
  yield(phrase:toCandidate())
end

---@param input string
---@param segment Segment
---@param env AutoLengthEnv
function this.func(input, segment, env)
  if not segment:has_tag("abc") then
    return
  end
  env.is_buffered = env.engine.context:get_option("is_buffered") or false
  env.third_pop = env.engine.context:get_option("third_pop") or false
  env.fast_char = env.engine.context:get_option("fast_char") or false
  env.fast_change = env.engine.context:get_option("fast_change") or false
  env.single_display = env.engine.context:get_option("single_display") or false
  local schema_id = env.engine.schema.schema_id

  if env.engine.context:get_option("ascii_mode") then
    return
  end
  -- 如果当前编码是静态编码，就只进行精确匹配，并依原样返回结果
  if static(input, env) then
    -- 清空候选缓存
    env.known_candidates = {}
    local is = input
    if core.jm(schema_id) and core.ssb(input) and env.fast_char then
      is = input .. "'"
    end
    env.static_memory:dict_lookup(is, false, 0)
    for entry in env.static_memory:iter_dict() do
      local phrase = rime.Phrase(env.static_memory, "table", segment.start, segment._end, entry)
      phrase.preedit = input
      rime.yield(phrase:toCandidate())
    end
    -- 在一些情况下，需要把三码或者四码的编码拆分成两段分别翻译，这也算是一种静态编码
    -- 1. 编码为 sxs 格式时，只要不是简码的三顶模式，就要拆分成二简字 + 一简字翻译
    -- 2. 飞系方案，编码为 sbsb 格式时，拆分成声笔字 + 声笔字翻译
    -- 3. 飞讯，编码为 sxsb 格式时，拆分成二简字 + 声笔字翻译
    if (core.sxs(input) and not env.third_pop)
        or (core.feixi(schema_id) and core.sbsb(input))
        or (core.fx(schema_id) and core.sxsb(input)) then
      translate_by_split(input, segment, env)
    end
    return
  end
  local memory = env.dynamic_memory
  -- 静态编码都处理完了，现在进入自动码长的动态编码部分
  -- 首先，根据输入的前三码来模糊匹配，依次查询固态词典和用户词典，并且结果都存放到一个列表中
  local lookup_code = input:sub(0, 3)
  ---@type Phrase[]
  local phrases = {}
  ---@type table<string, boolean>
  local known_words = {}
  memory:user_lookup(lookup_code, true)
  for entry in memory:iter_user() do
    local phrase = validate_phrase(entry, segment, "user_table", input, env)
    if phrase then
      table.insert(phrases, phrase)
      known_words[phrase.text] = true
    end
  end
  memory:dict_lookup(lookup_code, true, 0)
  for entry in memory:iter_dict() do
    local phrase = validate_phrase(entry, segment, "table", input, env)
    if phrase and (not known_words[phrase.text]) then
      table.insert(phrases, phrase)
      known_words[phrase.text] = true
    end
  end
  -- 对列表根据置顶与否以及频率进行排序
  table.sort(phrases, function(a, b)
    if a.comment == kTopSymbol and b.comment ~= kTopSymbol then
      return true
    end
    if a.comment ~= kTopSymbol and b.comment == kTopSymbol then
      return false
    end
    return a.weight > b.weight
  end)
  -- 在列表的末尾加上未确认的用户自造词
  memory:user_lookup(kEncodedPrefix .. lookup_code, true)
  for entry in memory:iter_user() do
    local phrase = validate_phrase(entry, segment, "user_table", input, env)
    if phrase and (not known_words[phrase.text]) then
      table.insert(phrases, phrase)
      known_words[phrase.text] = true
    end
  end
-- 如果在快调时声笔自然或声笔小鹤用sxb没检索到单字，则查找静态词组
  if #phrases == 0 and core.sp(schema_id) and core.sxb(input) then
    env.static_memory:dict_lookup(input, false, 0)
    for entry in env.static_memory:iter_dict() do
      local phrase = rime.Phrase(env.static_memory, "table", segment.start, segment._end, entry)
      phrase.preedit = input
      rime.yield(phrase:toCandidate())
    end
    return
  end
  -- 如果在四码时动态编码没有检索到结果，可以尝试拆分编码给出一个候选
  if #phrases == 0 and rime.match(input, "([bpmfdtnlgkhjqxzcsrywv][a-z]){2}") then
    translate_by_split(input, segment, env)
    return
  end
  -- 以下分 4 种情况实现自动码长的翻译策略
  -- 1. 如果输入的编码是一个动态编码的起始调整位，那么返回一个权重最高的候选
  -- 2. 如果输入的编码是基本编码的全码，那么返回所有的候选
  -- 3. 如果输入的编码是在基本编码的基础上加上了一个选重键，那么返回一个特定的候选
  -- 4. 如果输入的编码是扩展编码的全码，那么返回所有的候选
  -- 在情况 1 和 2 下，还要把已经见到的候选放到缓存中，以便在更长码时不重复出现这个候选
  -- 例如，对于声笔简码来说，3 码出现过的字词就不会再出现在 4 码的候选中，4 码出现过的字词就不会再出现在 6 码的候选中
  if dynamic(input, env) == dtypes.short then
    local cand = phrases[1]:toCandidate()
    env.known_candidates[cand.text] = 0
    yield(cand)
  elseif dynamic(input, env) == dtypes.base then
    local count = 1
    for _, phrase in ipairs(phrases) do
      local cand = phrase:toCandidate()
      if (env.known_candidates[cand.text] or inf) < count then
        goto continue
      end
      if count <= 6 then
        env.known_candidates[cand.text] = count
      end
      yield(cand)
      count = count + 1
      ::continue::
    end
  elseif dynamic(input, env) == dtypes.select then
    local last = input:sub(-1)
    local order = string.find(env.engine.schema.select_keys, last)
    for _, phrase in ipairs(phrases) do
      local cand = phrase:toCandidate()
      if env.known_candidates[cand.text] == order then
        yield(cand)
        break
      end
    end
  elseif dynamic(input, env) == dtypes.full then
    for _, phrase in ipairs(phrases) do
      local cand = phrase:toCandidate()
      local rank = env.known_candidates[cand.text]
      -- 如果强制选重，那么无论 rank 是多少都不显示这个候选
      -- 如果不强制选重，那么只有 rank <= 1，即之前出现在首选的才会显示
      if rank and (rank <= 1 or env.forced_selection) then
        goto continue
      end
      yield(cand)
      ::continue::
    end
  elseif dynamic(input, env) == dtypes.unified then
    local count = 1
    for _, phrase in ipairs(phrases) do
      local cand = phrase:toCandidate()
      if (env.known_candidates[cand.text] or inf) < input:len() then
        goto continue
      end
      if count == 1 then
        env.known_candidates[cand.text] = input:len()
        cand.comment = ""
      elseif cand.comment ~= "" then
        cand.type = "completion"
      end
      yield(cand)
      if count == 1 and env.single_display and not env.engine.context:get_option("not_single_display") then
        if (input:len() < 7 and core.fx(schema_id)
          and rime.match(input, "[bpmfdtnlgkhjqxzcsrywv][a-z][bpmfdtnlgkhjqxzcsrywv][aeuio23789][aeuio]+")) then
          break
        elseif (input:len() < 6) then
          break
        end
      end
      count = count + 1
      ::continue::
    end
  end
end

return this
