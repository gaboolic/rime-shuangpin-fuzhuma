-- 参考魔然https://github.com/ksqsf/rime-moran/blob/main/lua/moran_quick_code_hint.lua
-- 参考星空键道https://github.com/xkjd27/rime_jd27c/blob/e38a8c5d010d5a3933e6d6d8265c0cf7b56bfcca/rime/lua/jd27_hint.lua
-- 当用户用全码"womf"输入“我们”时，回显简码提示"wm"
-- doing
local Module = {}

function Module.init(env)
   local dict = "moqi_single"
   -- 这里必须先在build文件夹下构建一个 xxx.reverse.bin二进制文件，用txt自定义短语不行
   env.custom_phrase_reverse = ReverseLookup(dict)
end

function Module.fini(env)
   env.custom_phrase_reverse = nil
end

function Module.func(translation, env)
   log.info("jianma_show Module.func")
   for cand in translation:iter() do
      local gcand = cand:get_genuine()
      local word = gcand.text
      log.info(word)
      if utf8.len(word) == 1 and env.custom_phrase_reverse then
         yield(cand)
      else
         local all_codes = env.custom_phrase_reverse:lookup(word)
         local in_use = false
         if all_codes then
            local codes = {}
            for code in all_codes:gmatch("%S+") do
               log.info(code)
               if #code < 4 then
                  if code == cand.preedit then
                     in_use = true
                  else
                     table.insert(codes, code)
                  end
               end
            end
            if #codes == 0 and not in_use then
               goto continue
            end
            local codes_hint = table.concat(codes, " ")
            local comment = ""
            comment = gcand.comment .. "! " .. codes_hint
            gcand.comment = comment
         end
         ::continue::
         yield(cand)
      end
   end
end

return Module
