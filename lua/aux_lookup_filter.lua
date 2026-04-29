-- 句中任意辅助码候选筛选滤镜。
--
-- 用法：
--   在方案的 filters 中加入：
--
--     - lua_filter@*aux_lookup_filter
--
--   组合态输入触发键和 1-2 位辅助码后，会按候选中的任意字筛选候选：
--
--     shishi`b  -> 事实 / 实施 / 实时 ...
--     ni`rx     -> 你 / 伱
--
-- 配置：
--
--   aux_lookup_filter:
--     trigger_key: "`"
--     aux_type: flypy
--
-- aux_type 默认读取 pro_comment_format/fuzhu_type；是否启用默认跟随
-- pro_comment_format/fuzhu_code。码表从 cn_dicts/8105.dict.yaml 和
-- cn_dicts/41448.dict.yaml 读取，因此会匹配当前方案使用的辅助码类型。

local M = {}

local AUX_INDEX = {
    moqi = 2,
    flypy = 3,
    zrm = 4,
    jdh = 5,
    cj = 6,
    tiger = 7,
    wubi = 8,
    hx = 9,
}

local DICT_FILES = {
    "/cn_dicts/8105.dict.yaml",
    "/cn_dicts/41448.dict.yaml",
}

local function escape_pattern(s)
    return (s:gsub("(%W)", "%%%1"))
end

local function pass_through(input)
    for cand in input:iter() do
        yield(cand)
    end
end

local function split_fields(code)
    local fields = {}
    for field in (code .. ";"):gmatch("([^;]*);") do
        fields[#fields + 1] = field
    end
    return fields
end

local function add_aux_code(aux_table, ch, code)
    if not ch or ch == "" or not code or code == "" then
        return
    end

    local codes = aux_table[ch]
    if not codes then
        codes = {}
        aux_table[ch] = codes
    end
    codes[#codes + 1] = code
end

local function load_dict_aux(aux_table, path, aux_index)
    local file = io.open(path, "r")
    if not file then
        return
    end

    local in_header = false
    for line in file:lines() do
        if line == "---" then
            in_header = true
        elseif line == "..." then
            in_header = false
        elseif not in_header and line ~= "" and line:sub(1, 1) ~= "#" then
            local ch, code = line:match("^([^\t]+)\t([^\t]+)")
            if ch and code then
                local fields = split_fields(code)
                add_aux_code(aux_table, ch, fields[aux_index])
            end
        end
    end

    file:close()
end

local function load_aux_table(env)
    local aux_type = env.aux_type or "moqi"
    M.aux_tables = M.aux_tables or {}
    if M.aux_tables[aux_type] then
        return M.aux_tables[aux_type]
    end

    local aux_index = AUX_INDEX[aux_type] or AUX_INDEX.moqi
    local aux_table = {}
    local user_dir = rime_api.get_user_data_dir()
    for _, dict_file in ipairs(DICT_FILES) do
        load_dict_aux(aux_table, user_dir .. dict_file, aux_index)
    end

    M.aux_tables[aux_type] = aux_table
    return aux_table
end

local function split_chars(text)
    local chars = {}
    for _, codepoint in utf8.codes(text) do
        chars[#chars + 1] = utf8.char(codepoint)
    end
    return chars
end

local function char_matches_prefix(aux_table, ch, aux)
    local codes = aux_table[ch]
    if not codes then
        return false
    end

    for _, code in ipairs(codes) do
        if code:sub(1, #aux) == aux then
            return true
        end
    end
    return false
end

local function match_subsequence(aux_table, chars, aux)
    local pos = 1
    for i = 1, #chars do
        local code = aux:sub(pos, pos)
        if code == "" then
            return true
        end
        if char_matches_prefix(aux_table, chars[i], code) then
            pos = pos + 1
        end
    end
    return pos > #aux
end

local function candidate_matches(aux_table, text, aux)
    if text == "" or aux == "" then
        return false
    end

    local chars = split_chars(text)
    for i = 1, #chars do
        if char_matches_prefix(aux_table, chars[i], aux) then
            return true
        end
    end

    if #aux > 1 then
        return match_subsequence(aux_table, chars, aux)
    end
    return false
end

local function collect_candidates(input)
    local candidates = {}
    for cand in input:iter() do
        candidates[#candidates + 1] = {
            cand = cand,
            chars = split_chars(cand.text),
        }
    end
    return candidates
end

local function find_variant_positions(candidates)
    local positions = {}
    local max_len = 0
    for i = 1, #candidates do
        if #candidates[i].chars > max_len then
            max_len = #candidates[i].chars
        end
    end

    for pos = 1, max_len do
        local first = nil
        local differs = false
        for i = 1, #candidates do
            local ch = candidates[i].chars[pos]
            if ch then
                if first == nil then
                    first = ch
                elseif ch ~= first then
                    differs = true
                    break
                end
            end
        end
        if differs then
            positions[#positions + 1] = pos
        end
    end
    return positions
end

local function find_variant_group(candidates)
    local groups = {}
    local order = {}
    for i = 1, #candidates do
        local len = #candidates[i].chars
        if len > 0 then
            local group = groups[len]
            if not group then
                group = {}
                groups[len] = group
                order[#order + 1] = len
            end
            group[#group + 1] = candidates[i]
        end
    end

    for i = 1, #order do
        local group = groups[order[i]]
        if #group >= 2 then
            local positions = find_variant_positions(group)
            if #positions > 0 then
                return group, positions
            end
        end
    end
    return nil, nil
end

local function candidate_matches_positions(aux_table, chars, aux, positions)
    for i = 1, #positions do
        local ch = chars[positions[i]]
        if ch and char_matches_prefix(aux_table, ch, aux) then
            return true
        end
    end

    if #aux > 1 then
        local selected = {}
        for i = 1, #positions do
            local ch = chars[positions[i]]
            if ch then
                selected[#selected + 1] = ch
            end
        end
        return match_subsequence(aux_table, selected, aux)
    end
    return false
end

function M.init(env)
    local config = env.engine.schema.config
    env.trigger_key = config:get_string("aux_lookup_filter/trigger_key") or "`"
    env.enabled = config:get_bool("aux_lookup_filter/enabled")
    if env.enabled == nil then
        env.enabled = config:get_bool("pro_comment_format/fuzhu_code") or false
    end
    env.aux_type = config:get_string("aux_lookup_filter/aux_type")
        or config:get_string("pro_comment_format/fuzhu_type")
        or "moqi"

    env.notifier = env.engine.context.select_notifier:connect(function(ctx)
        if not env.enabled then
            return
        end

        local trigger_pos = ctx.input:find(env.trigger_key, 1, true)
        if not trigger_pos then
            return
        end

        local trigger_pattern = escape_pattern(env.trigger_key)
        local input_without_aux = ctx.input:match("^(.-)" .. trigger_pattern)
        if input_without_aux and input_without_aux ~= "" then
            ctx.input = input_without_aux
            ctx:commit()
        end
    end)
end

function M.fini(env)
    if env.notifier then
        env.notifier:disconnect()
    end
end

function M.func(input, env)
    if not env.enabled then
        pass_through(input)
        return
    end

    local input_code = env.engine.context.input
    local trigger_pos = input_code:find(env.trigger_key, 1, true)
    if not trigger_pos then
        pass_through(input)
        return
    end

    local aux = input_code:sub(trigger_pos + #env.trigger_key):match("^([^,']+)") or ""
    aux = aux:sub(1, 2)
    if aux == "" then
        pass_through(input)
        return
    end

    local aux_table = load_aux_table(env)
    local candidates = collect_candidates(input)
    local variant_group, variant_positions = find_variant_group(candidates)
    local yielded = {}
    local has_variant_match = false

    if variant_group and variant_positions then
        for i = 1, #variant_group do
            local item = variant_group[i]
            if candidate_matches_positions(aux_table, item.chars, aux, variant_positions) then
                yielded[item] = true
                has_variant_match = true
                yield(item.cand)
            end
        end
    end

    for i = 1, #candidates do
        local item = candidates[i]
        if not yielded[item] and not has_variant_match then
            if candidate_matches(aux_table, item.cand.text, aux) then
                yield(item.cand)
            end
        end
    end
end

return M
