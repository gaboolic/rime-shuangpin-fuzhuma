-- 2码 3码时tab上屏词 置顶到第一候选的comment中
-- @gaboolic

local M = {}

function M.init(env)
  -- 提升 count 个词语，插入到第 idx 个位置，默认 2、4。
  local config = env.engine.schema.config
  env.name_space = env.name_space:gsub("^*", "")
  env.fixed = {}
  M.count = config:get_int(env.name_space .. "/count") or 2
  M.idx = config:get_int(env.name_space .. "/idx") or 4
  M.input_str = env.engine.context.input

  local path_1 = rime_api.get_user_data_dir() .. ("/custom_phrase/custom_phrase_super_1jian.txt")
  local path_2 = rime_api.get_user_data_dir() .. ("/custom_phrase/custom_phrase_super_2jian.txt")
  local path_3 = rime_api.get_user_data_dir() .. ("/custom_phrase/custom_phrase_super_3jian.txt")
  local paths = {
    path_1,
    path_2,
    path_3
  }
  -- 遍历表中的每个路径
  for _, path in ipairs(paths) do
    -- 尝试打开文件
    local file = io.open(path, "r")
    if not file then
      log.info("stick path not file")
      return
    end
    for line in file:lines() do
      if string.sub(line, 1, 1) == "#" then
        goto continue
      end
      ---@type string, string
      local code, content = line:match("([^\t]+)\t([^\t]+)")
      if not content or not code then
        goto continue
      end
      content = string.sub(content, 1, -2)
      env.fixed[content] = code
      ::continue::
    end
    file:close()
  end
end

function isAllLetters(str)
    return not (string.find(str, "[^%a]"))
end

function M.func(input,env)
  -- log.info("stick M.func")
  local first_cand = nil
  for cand in input:iter() do
    local preedit_str = cand.preedit
    local preedit_len = utf8.len(preedit_str)
    if first_cand == nil then
      first_cand = cand
      if preedit_len <=3 and isAllLetters(preedit_str) then
        local stick_phrase = env.fixed[preedit_str] or ""
        if stick_phrase ~= nil and first_cand.text ~= stick_phrase then
          first_cand.comment=stick_phrase
        end
        yield(first_cand)
      end
    end
    yield(cand)
  end
end

return M
