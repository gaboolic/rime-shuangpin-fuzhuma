-- doing 2码 3码时tab上屏词 置顶到第一候选的comment中
-- @gaboolic

local M = {}

function M.init(env)
  -- 提升 count 个词语，插入到第 idx 个位置，默认 2、4。
  local config = env.engine.schema.config
  env.name_space = env.name_space:gsub("^*", "")
  M.fixed = {}
  M.count = config:get_int(env.name_space .. "/count") or 2
  M.idx = config:get_int(env.name_space .. "/idx") or 4
  M.input_str = env.engine.context.input

  local path = get_user_data_dir() .. ("/custom_phrase/custom_phrase_supwer_2jian.txt")
  log.error("stick "+path)
  print("stick "+path)
  local file = io.open(path, "r")
  if not file then
    return
  end
  for line in file:lines() do
    ---@type string, string
    local code, content = line:match("([^\t]+)\t([^\t]+)")
    if not content or not code then
      goto continue
    end
    local words = {}
    for word in content:gmatch("[^%s]+") do
      table.insert(words, word)
    end
    M.fixed[code] = words
    ::continue::
  end
  file:close()
end

function M.func(input,env)
  log.error("stick M.func")
  local first_cand = nil
  for cand in input:iter() do
    local preedit_str = cand.preedit
    local preedit_len = utf8.len(preedit_str)
    if first_cand == nil and preedit_len <=3 then
      first_cand = cand
      -- local fixed_phrases = M.fixed[preedit_str+"|"]
      -- if fixed_phrases != nil then
      --   first_cand.comment=fixed_phrases
      -- end
      yield(first_cand)
    end
    yield(cand)
  end
end

return M
