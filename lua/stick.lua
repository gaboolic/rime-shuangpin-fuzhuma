-- doing 2码 3码时tab上屏词 置顶到第一候选的comment中
-- @gaboolic

local M = {}

function M.init(env)
    -- 提升 count 个词语，插入到第 idx 个位置，默认 2、4。
    local config = env.engine.schema.config
    env.name_space = env.name_space:gsub("^*", "")
    M.count = config:get_int(env.name_space .. "/count") or 2
    M.idx = config:get_int(env.name_space .. "/idx") or 4
    M.input_str = env.engine.context.input
end

function M.func(input)
    local first_cand = nil
    for cand in input:iter() do
      local preedit_str = cand.preedit
      local preedit_len = utf8.len(preedit_str)
      if first_cand == nil and preedit_len <=3 then
        first_cand = cand
        
        first_cand.comment=preedit_str
        yield(first_cand)
      end
      yield(cand)
    end
end

return M
