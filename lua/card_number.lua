local function generate_region_code(prefix)
    if not prefix or #prefix == 0 then
        local province = string.format("%02d", math.random(11, 65))
        local city = string.format("%02d", math.random(1, 20))
        local county = string.format("%02d", math.random(1, 20))
        return province .. city .. county
    end
    
    -- 处理有前缀的情况
    local len = #prefix
    if len >= 6 then
        return prefix:sub(1, 6)  -- 直接取前6位
    end
    
    -- 补全剩余部分
    local result = prefix
    if len < 2 then
        result = result .. string.format("%02d", math.random(11, 65)):sub(len+1, 2)
    end
    if len < 4 then
        result = result .. string.format("%02d", math.random(1, 20)):sub(math.max(1, len-2+1), 2)
    end
    if len < 6 then
        result = result .. string.format("%02d", math.random(1, 20)):sub(math.max(1, len-4+1), 2)
    end
    
    return result:sub(1, 6)  -- 确保返回6位
end

local function generate_id_card_number(prefix)
    local region_part = generate_region_code(prefix)
    
    local year = tostring(math.random(1980, 2000))
    local month = string.format("%02d", math.random(1, 12))
    local max_days = month == "02" and 28 or 
                     (month == "04" or month == "06" or month == "09" or month == "11") and 30 or 31
    local day = string.format("%02d", math.random(1, max_days))
    
    -- 顺序码 (3位)
    local sequence = string.format("%03d", math.random(0, 999))
    
    -- 组合前17位
    local first17 = region_part .. year .. month .. day .. sequence
    
    -- 计算校验码
    local weights = {7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2}
    local check_codes = {"1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"}
    
    local sum = 0
    for i = 1, 17 do
        sum = sum + tonumber(first17:sub(i, i)) * weights[i]
    end
    local check_code = check_codes[sum % 11 + 1]
    
    return first17 .. check_code
end

local function card_number(input, seg, env)
    env.card_number_keyword = env.card_number_keyword or
        env.engine.schema.config:get_string('recognizer/patterns/card_number'):sub(2, 2)
    if seg:has_tag("card_number") and env.card_number_keyword ~= '' and input:sub(1, 1) == env.card_number_keyword then
        local ucodestr = input:match(env.card_number_keyword .. "(%x+)")
        local id_card = generate_id_card_number(ucodestr)
        yield(Candidate("id_card", seg.start, seg._end, id_card, ""))
    end
end

return card_number