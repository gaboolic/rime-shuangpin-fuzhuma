-- 降低emoji在候选项的位置
local M = {}

function M.init(env)
  local config = env.engine.schema.config
  env.name_space = env.name_space:gsub("^*", "")

  -- 要降低到的位置
  local page_size = config:get_int("menu/page_size") or 5
  if page_size < 3 then
    page_size = 0
  end
  local idx = config:get_int(env.name_space .. "/idx") or 5
  M.idx = math.min(page_size, idx)
end

function M.func(input, env)
  if (M.idx == 0) then
    for cand in input:iter() do
      yield(cand)
    end
    return
  end

  local emoji_cands = {}
  local other_cands = {}
  local prev_text = ""
  local emoji_pos = M.idx
  -- local opencc_db = Opencc("emoji.json")

  for cand in input:iter() do
    if
      (emoji_pos > 1)
      and (cand:get_dynamic_type() == "Shadow")
      and not (cand.text:find("([\228-\233][\128-\191]-)") and cand.text:find("[%a]"))
    then
      table.insert(emoji_cands, { prev_text, cand })
    elseif emoji_pos > 1 then
      yield(cand)
      emoji_pos = emoji_pos - 1
      -- local emoji_tab = opencc_db:convert(cand.text)
      -- if #emoji_tab > 1 and type(emoji_tab) ~= "string" then
      prev_text = cand.text
      -- end
    else
      table.insert(other_cands, cand)
    end
  end

  if #emoji_cands > 0 then
    for _, cand_item in ipairs(emoji_cands) do
      yield(ShadowCandidate(cand_item[2], cand_item[2].type, cand_item[2].text, cand_item[1]))
    end
  end

  for _, cand in ipairs(other_cands) do
    yield(cand)
  end
end

return M
