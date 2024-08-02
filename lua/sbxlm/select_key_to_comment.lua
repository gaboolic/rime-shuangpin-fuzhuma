-- 选择键转注释过滤器
-- 本过滤器将 alternative_select_keys 中定义的选择键添加到候选项的注释中显示
-- Version: 20240125
-- Author: 戴石麟

local rime = require "sbxlm.lib"
local core = require "sbxlm.core"

local this = {}

---@param env Env
function this.init(env)
end

---@param segment Segment
---@param env Env
function this.tags_match(segment, env)
  -- 当前段落需要为标点或为正常输入码且匹配选择注释模式
  local pattern = env.engine.schema.config:get_string("menu/select_comment_pattern") or ""
  local input = rime.current(env.engine.context) or ""
  return (segment:has_tag("abc") and rime.match(input, pattern))
      or segment:has_tag("punct") or segment:has_tag("hypy")
      or input:len() >= 2 and segment:has_tag("bihua") or segment:has_tag("zhlf")
      or segment:has_tag("sbzdy") or segment:has_tag("lua")
end

---@param translation Translation
---@param env Env
function this.func(translation, env)
  local schema_id = env.engine.schema.schema_id
  local input = rime.current(env.engine.context) or ""
  local select_keys = env.engine.schema.select_keys or ""
  local segment = env.engine.context.composition:back()
  if segment:has_tag("hypy") or input:len() >= 2 and segment:has_tag("bihua")
      or segment:has_tag("zhlf") or segment:has_tag("sbzdy") then
    select_keys = "_23789"
  elseif segment:has_tag("lua") then
    select_keys = "_aeuio"
  end
  local i = 0
  local pattern = "[bpmfdtnlgkhjqxzcsrywv][a-z][bpmfdtnlgkhjqxzcsrywv][aeuio23789][aeuio]+"
  for candidate in translation:iter() do
    -- 通过取模运算获取与候选项对应的选择键
    local j = i % select_keys:len() + 1
    local key = select_keys:sub(j, j)
    -- 如果是下划线，说明是首选，无需操作
    if key == "_" then
      goto continue
    end
    -- 如果是单次选重非全码产生的补全选项，无需操作
    if candidate.type == "completion" and core.zici(schema_id) and segment:has_tag("abc") then
      if (input:len() < 7 and core.fx(schema_id) and rime.match(input, pattern)) then
        goto continue
      elseif (core.sp(schema_id)) then
        goto continue
      elseif (input:len() < 6) and not segment:has_tag("sbjm") then
        goto continue
      end
    end
    if candidate.comment:len() > 0 then
      if (schema_id == "sbpy" or schema_id == "sbjp") and segment:has_tag("abc") then
        candidate.comment = key .. candidate.comment
      elseif (input:len() == 7 and core.fx(schema_id) and rime.match(input, pattern)) then
        candidate.comment = key
      else
        candidate.comment = candidate.comment .. ":" .. key
      end
    else
      candidate.comment = key
    end
    ::continue::
    i = i + 1
    rime.yield(candidate)
  end
end

return this
