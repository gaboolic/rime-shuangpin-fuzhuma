local M = {}

function M.init(env)
    -- 初始化逻辑，加载固定词典等
    local config = env.engine.schema.config
    env.name_space = env.name_space:gsub("^*", "")
    env.fixed = {}
    M.count = config:get_int(env.name_space .. "/count") or 2  -- 获取配置中的 count 参数，默认值为 2
    M.idx = config:get_int(env.name_space .. "/idx") or 4  -- 获取配置中的 idx 参数，默认值为 4
    M.input_str = env.engine.context.input  -- 获取当前输入的字符串

    -- 定义固定词典文件的路径
    local paths = {
        rime_api.get_user_data_dir() .. "/jm_dicts/custom_phrase_super_1jian.txt",
        rime_api.get_user_data_dir() .. "/jm_dicts/custom_phrase_super_2jian.txt",
        rime_api.get_user_data_dir() .. "/jm_dicts/custom_phrase_super_3jian.txt"
    }

    -- 遍历每个路径，加载固定词典
    for _, path in ipairs(paths) do
        local file = io.open(path, "r")
        if not file then
            log.info("stick path not file")
            return
        end
        -- 逐行读取文件内容
        for line in file:lines() do
            if string.sub(line, 1, 1) == "#" then
                goto continue
            end
            -- 匹配编码和词条内容
            local code, content = line:match("([^\t]+)\t([^\t]+)")
            if content and code then
                content = string.sub(content, 1, -2)  -- 去除词条内容末尾的换行符
                env.fixed[content] = code  -- 将编码和词条内容存储到 env.fixed 表中
            end
            ::continue::
        end
        file:close()  -- 关闭文件
    end
end

-- 检查字符串是否全为字母
local function isAllLetters(str)
    return not (string.find(str, "[^%a]"))
end

-- 创建候选词
local function create_candidate(text, comment)
    return Candidate("word", 0, string.len(text), text, comment)
end

function M.func(input, env)
    local first_cand = nil
    local first_is_all_letters = false
    local candidates = {}

    -- 遍历输入的候选词并存储到表中
    for cand in input:iter() do
        table.insert(candidates, cand)
    end

    if #candidates > 0 then
        first_cand = candidates[1]
        local preedit_str = first_cand.preedit
        first_is_all_letters = isAllLetters(preedit_str)

        if first_is_all_letters then
            local stick_phrase = env.fixed[preedit_str] or ""
            if stick_phrase ~= "" and first_cand.text ~= stick_phrase then
                first_cand.comment = stick_phrase .. "⚡"  -- 在注释后面加上闪电符号，表示快速输入，不想要置空
            end
        end

        -- 输出第一个候选词
        yield(first_cand)

        -- 清空第二到第八个候选词的注释，这个是用来解决翻译模式下总会将第一个候选单词的注释复制到所有的翻译项目，干扰阅读翻译词，这样处理后就实现了兼容，不再反复显示第一个词的注释。
        for i = 2, math.min(8, #candidates) do
            if first_is_all_letters then
                local cand = candidates[i]
                yield(create_candidate(cand.text, ""))  -- 清空注释
            else
                yield(candidates[i])
            end
        end

        -- 输出剩余的候选词
        for i = 9, #candidates do
            yield(candidates[i])
        end
    else
        -- 如果没有找到匹配的候选词，显示固定词典内容作为第一候选词
        local preedit_str = env.engine.context.input
        local stick_phrase = env.fixed[preedit_str] or ""
        if stick_phrase ~= "" then
            yield(create_candidate(stick_phrase, "⚡"))  -- 在注释中加上闪电符号，表示快速输入，不想要置空
        end
    end
end

return M
