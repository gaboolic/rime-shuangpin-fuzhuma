-- 参考魔然https://github.com/rimeinn/rime-moran/blob/main/lua/moran_hint_filter.lua
-- 参考星空键道https://github.com/xkjd27/rime_jd27c/blob/e38a8c5d010d5a3933e6d6d8265c0cf7b56bfcca/rime/lua/jd27_hint.lua
-- 当用户用全码"womf"输入"我们"时，回显简码提示"wm"
-- doing
local Module = {}

function Module.init(env)
   local dict = "moqi_single"  -- 回到使用 moqi_single 词典，这是墨奇音形的核心词典
   log.info("jianma_show Module.init: initializing with dict " .. dict)
   -- 这里必须先在build文件夹下构建一个 xxx.reverse.bin二进制文件，用txt自定义短语不行
   local reverse_lookup = ReverseLookup(dict)
   if reverse_lookup then
      log.info("jianma_show Module.init: ReverseLookup created successfully for " .. dict)
      env.custom_phrase_reverse = reverse_lookup
   else
      -- 由于reverse_lookup为nil，我们不能调用log.warn，而是使用更安全的方式
      env.custom_phrase_reverse = nil  -- 明确设置为nil，以便在func中检测
      log.warn("jianma_show Module.init: Failed to create ReverseLookup for " .. dict)
      log.warn("jianma_show Module.init: Make sure moqi_single.reverse.bin exists in build folder")
   end
end

function Module.fini(env)
   log.info("jianma_show Module.fini")
   env.custom_phrase_reverse = nil
end

function Module.func(translation, env)
   log.info("jianma_show Module.func: start processing translation")
   if not env.custom_phrase_reverse then
      log.warn("jianma_show Module.func: custom_phrase_reverse is nil, skipping processing")
      for cand in translation:iter() do
         yield(cand)
      end
      return
   end
   
   for cand in translation:iter() do
      log.info("jianma_show processing candidate: " .. (cand.text or "nil") .. ", type: " .. (cand.type or "nil") .. ", preedit: " .. (cand.preedit or "nil"))
      local gcand = cand:get_genuine()
      local word = gcand.text
      local word_len = utf8.len(word)
      log.info("jianma_show word: " .. (word or "nil") .. ", length: " .. (word_len or "nil"))
      
      -- 检查当前输入的编码长度是否>=4
      local current_input_length = 0
      if cand.preedit then
         current_input_length = #cand.preedit
      end
      
      log.info("jianma_show current input length: " .. current_input_length)
      
      if word_len == 1 then
         log.info("jianma_show skipping single character: " .. word)
         yield(cand)
      elseif word_len >= 2 and word_len <= 4 and current_input_length >= 4 then
         log.info("jianma_show looking up reverse codes for multi-character word: " .. word)
         local all_codes = env.custom_phrase_reverse:lookup(word)
         if all_codes then
            log.info("jianma_show found codes: " .. all_codes)
            local in_use = false
            local codes = {}
            local short_codes = {}  -- 专门存储简码（长度小于等于2的码）
            local extracted_short_codes = {} -- 存储提取的简码
            
            for code in all_codes:gmatch("%S+") do
               log.info("jianma_show checking code: " .. code .. ", length: " .. #code)
               if #code <= 2 then
                  -- 长度小于等于2的码作为简码处理
                  log.info("jianma_show short code found (length <= 2): " .. code)
                  table.insert(short_codes, code)
               elseif #code < 4 then
                  log.info("jianma_show code length 3: " .. code .. ", comparing with preedit: " .. (cand.preedit or "nil"))
                  if cand.preedit and code == cand.preedit then
                     log.info("jianma_show code matches preedit, marking as in use")
                     in_use = true
                  else
                     log.info("jianma_show adding code to suggestion: " .. code)
                     table.insert(codes, code)
                  end
               else
                  log.info("jianma_show code length >= 4, skipping: " .. code)
                  -- 尝试从长码中提取简码，例如从'eibd'中提取'ei'或'i'
                  -- 对于"差不多"（三个字），可以提取首字母或其他有意义的简码
                  if word_len == 3 and #code == 4 then
                     -- 尝试提取可能的简码
                     local first_two = code:sub(1, 2)  -- 取前两位，如 ei
                     local last_two = code:sub(3, 4)   -- 取后两位，如 bd
                     local mixed = code:sub(1, 1) .. code:sub(3, 3)  -- 取第1和第3位，如 eb
                     local mid_char = code:sub(2, 2)  -- 取中间字符，如 i
                     
                     log.info("jianma_show extracting short codes from 4-char code: " .. code .. 
                             ", first_two: " .. first_two .. 
                             ", last_two: " .. last_two .. 
                             ", mixed: " .. mixed ..
                             ", mid_char: " .. mid_char)
                     
                     -- 根据墨奇输入法的特点，我们尝试添加一些可能的简码
                     -- 比如对于"差不多"，我们可能希望显示"i"（中间字符）
                     if mid_char ~= "" then
                        table.insert(extracted_short_codes, mid_char)
                     end
                  elseif word_len == 2 and #code == 4 then
                     -- 对于两字词，可能提取前两位或首字母
                     local first_two = code:sub(1, 2)
                     local first_chars = code:sub(1, 1) .. code:sub(3, 3)  -- 第1和第3位
                     
                     log.info("jianma_show extracting short codes from 2-char word 4-char code: " .. code .. 
                             ", first_two: " .. first_two .. 
                             ", first_chars: " .. first_chars)
                     
                     if first_chars ~= "" then
                        table.insert(extracted_short_codes, first_chars)
                     end
                  end
               end
            end
            
            -- 优先显示真正的简码（长度≤2的码）
            if #short_codes > 0 then
               local short_codes_hint = table.concat(short_codes, " ")
               log.info("jianma_show true short codes hint: " .. short_codes_hint)
               local comment = ""
               if gcand.comment and #gcand.comment > 0 then
                  comment = gcand.comment .. "! " .. short_codes_hint
               else
                  comment = short_codes_hint
               end
               log.info("jianma_show setting comment with true short codes: " .. comment)
               gcand.comment = comment
            elseif #extracted_short_codes > 0 then
               -- 如果没有真正的简码，但有提取的简码，则显示提取的简码
               local extracted_codes_hint = table.concat(extracted_short_codes, " ")
               log.info("jianma_show extracted short codes hint: " .. extracted_codes_hint)
               local comment = ""
               if gcand.comment and #gcand.comment > 0 then
                  comment = gcand.comment .. "! " .. extracted_codes_hint
               else
                  comment = extracted_codes_hint
               end
               log.info("jianma_show setting comment with extracted short codes: " .. comment)
               gcand.comment = comment
            elseif #codes > 0 then
               -- 如果没有简码但有其他长度为3的码，也显示它们
               local codes_hint = table.concat(codes, " ")
               log.info("jianma_show 3-char codes hint: " .. codes_hint)
               local comment = ""
               if gcand.comment and #gcand.comment > 0 then
                  comment = gcand.comment .. "! " .. codes_hint
               else
                  comment = codes_hint
               end
               log.info("jianma_show setting comment with 3-char codes: " .. comment)
               gcand.comment = comment
            end
         else
            log.warn("jianma_show no codes found for word: " .. word)
         end
         yield(cand)
      elseif word_len >= 2 and word_len <= 4 and current_input_length < 4 then
         -- 当前输入长度不足4个字符时，不处理简码提示
         log.info("jianma_show current input length < 4, skipping short code hint for: " .. word)
         yield(cand)
      else
         -- 4个字以上的词也可以处理
         log.info("jianma_show looking up reverse codes for longer word: " .. word)
         local all_codes = env.custom_phrase_reverse:lookup(word)
         if all_codes then
            log.info("jianma_show found codes: " .. all_codes)
            local short_codes = {}  -- 专门存储简码（长度小于等于2的码）
            for code in all_codes:gmatch("%S+") do
               log.info("jianma_show checking code: " .. code .. ", length: " .. #code)
               if #code <= 2 then
                  -- 长度小于等于2的码作为简码处理
                  log.info("jianma_show short code found (length <= 2): " .. code)
                  table.insert(short_codes, code)
               end
            end
            -- 显示简码（长度≤2的码）
            if #short_codes > 0 then
               local short_codes_hint = table.concat(short_codes, " ")
               log.info("jianma_show short codes hint: " .. short_codes_hint)
               local comment = ""
               if gcand.comment and #gcand.comment > 0 then
                  comment = gcand.comment .. "! " .. short_codes_hint
               else
                  comment = short_codes_hint
               end
               log.info("jianma_show setting comment with short codes for long word: " .. comment)
               gcand.comment = comment
            end
         else
            log.warn("jianma_show no codes found for word: " .. word)
         end
         yield(cand)
      end
   end
   log.info("jianma_show Module.func: finished processing translation")
end

return Module