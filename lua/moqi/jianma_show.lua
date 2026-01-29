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
      -- reverse_lookup 为 nil 时记录警告
      env.custom_phrase_reverse = nil  -- 明确设置为nil，以便在func中检测
      log.warning("jianma_show Module.init: Failed to create ReverseLookup for " .. dict)
      log.warning("jianma_show Module.init: Make sure moqi_single.reverse.bin exists in build folder")
   end
end

function Module.fini(env)
   log.info("jianma_show Module.fini")
   env.custom_phrase_reverse = nil
end

function Module.func(translation, env)
   log.info("jianma_show Module.func: start processing translation")
   if not env.custom_phrase_reverse then
      log.warning("jianma_show Module.func: custom_phrase_reverse is nil, skipping processing")
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
            local four_char_codes = {}  -- 专门存储四字词的四码（仅对四字词）
            
            for code in all_codes:gmatch("%S+") do
               log.info("jianma_show checking code: " .. code .. ", length: " .. #code)
               if #code <= 2 then
                  -- 长度小于等于2的码作为简码处理
                  log.info("jianma_show short code found (length <= 2): " .. code)
                  table.insert(short_codes, code)
               elseif #code == 4 and word_len == 4 then
                  -- 对于四字词，长度等于4的码作为四码处理
                  log.info("jianma_show four-char code found for four-word phrase: " .. code)
                  table.insert(four_char_codes, code)
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
                  log.info("jianma_show code length >= 4, skipping (not a four-word phrase): " .. code)
                  -- 不再进行任何提取逻辑
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
            -- 然后显示四字词的四码（仅对四字词）
            elseif #four_char_codes > 0 and word_len == 4 then
               local four_codes_hint = table.concat(four_char_codes, " ")
               log.info("jianma_show four-char codes hint: " .. four_codes_hint)
               local comment = ""
               if gcand.comment and #gcand.comment > 0 then
                  comment = gcand.comment .. "! " .. four_codes_hint
               else
                  comment = four_codes_hint
               end
               log.info("jianma_show setting comment with four-char codes: " .. comment)
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
            log.warning("jianma_show no codes found for word: " .. word)
            -- 没有找到任何编码时，直接跳过
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
            log.warning("jianma_show no codes found for word: " .. word)
         end
         yield(cand)
      end
   end
   log.info("jianma_show Module.func: finished processing translation")
end

return Module