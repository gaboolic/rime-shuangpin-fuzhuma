-- card_number.lua
-- 支持自动补全并计算校验位, 用途仅限于检查用户输入有没有错误

local function calculate_check_digit(first17)
    local weights = {7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2}
    local check_codes = {"1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"}
    
    local sum = 0
    for i = 1, 17 do
        sum = sum + tonumber(first17:sub(i, i)) * weights[i]
    end
    return check_codes[sum % 11 + 1]
end

local function generate_random_date()
    local year = math.random(1980, 2000)
    local month = math.random(1, 12)
    local max_day = ({
        [2] = (year % 4 == 0 and (year % 100 ~= 0 or year % 400 == 0)) and 29 or 28,
        [4] = 30, [6] = 30, [9] = 30, [11] = 30
    })[month] or 31
    local day = math.random(1, max_day)
    
    return string.format("%04d%02d%02d", year, month, day)
end

local function complete_id_number(partial)
    local completed = partial
    
    if #completed < 6 then
        for i = #completed + 1, 6 do
            completed = completed .. tostring(math.random(0, 9))
        end
    end
    
    if #completed < 14 then
        if #completed <= 6 then
            completed = completed .. generate_random_date()
        else
            local date_part = completed:sub(7)
            if #date_part < 4 then
                date_part = date_part .. string.format("%02d", math.random(1, 12))
                date_part = date_part .. string.format("%02d", math.random(1, 31))
            elseif #date_part < 6 then
                local month = tonumber(date_part:sub(3, 4))
                local max_day = ({
                    [2] = 28, [4] = 30, [6] = 30, [9] = 30, [11] = 30
                })[month] or 31
                date_part = date_part .. string.format("%02d", math.random(1, max_day))
            end
            completed = completed:sub(1, 6) .. date_part
        end
    end
    
    if #completed < 17 then
        for i = #completed + 1, 17 do
            completed = completed .. tostring(math.random(0, 9))
        end
    end
    
    completed = completed:sub(1, 17)
    
    -- 计算校验位
    return completed .. calculate_check_digit(completed)
end

local function card_number(input, seg, env)
    env.card_number_keyword = env.card_number_keyword or
        env.engine.schema.config:get_string('recognizer/patterns/card_number'):sub(2, 2)
    
    if seg:has_tag("card_number") and env.card_number_keyword ~= '' and input:sub(1, 1) == env.card_number_keyword then
        local partial = input:match(env.card_number_keyword .. "(%d+)")
        local id_card
        
        if partial then
            if partial:match("^%d+$") then
                id_card = complete_id_number(partial)
            else
                id_card = complete_id_number("")
            end
        else
            id_card = complete_id_number("")
        end
        
        yield(Candidate("id_card", seg.start, seg._end, id_card, ""))
    end
end

return card_number