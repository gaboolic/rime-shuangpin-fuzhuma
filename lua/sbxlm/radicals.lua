-- 飞系部首反查过滤器
-- 适用于：声笔飞码、声笔飞单、声笔飞讯
-- 本过滤器在编码段打上反查标签的时候，给单字候选加注部首信息，以便用户学习
-- 部首信息的数据存放在用户目录下的 radicals.txt

local rime = require "sbxlm.lib"

local this = {}

---@class RadicalsEnv: Env
---@field lookup_tags string[]
---@field radicals { string : string }

---@param env RadicalsEnv
function this.init(env)
  env.radicals = {}
  local path = rime.api.get_user_data_dir() .. "/lua/sbxlm/radicals.txt"
  local file = io.open(path, "r")
  if not file then
    return
  end
  for line in file:lines() do
    ---@type string, string
    local char, radical = line:match("([^\t]+)\t([^\t]+)")
    env.radicals[char] = radical
  end
  file:close()
end

---@param segment Segment
---@param env RadicalsEnv
function this.tags_match(segment, env)
  local tags = rime.get_string_list(env.engine.schema.config, "reverse_lookup/tags")
  for _, value in ipairs(tags) do
    if segment.tags[value] then
      return true
    end
  end
  return false
end

---@param translation Translation
---@param env RadicalsEnv
function this.func(translation, env)
  for candidate in translation:iter() do
    local radical = env.radicals[candidate.text]
    if radical then
      candidate.comment = candidate.comment .. string.format(" [%s]", env.radicals[candidate.text])
    end
    rime.yield(candidate)
  end
  return
end

return this
