-- 日期与时间翻译器
-- 输入特定的日期时间缩写，输出对应的日期时间字符串

local rime = require "sbxlm.lib"

local function translator(input, seg)
   ---@type (string | osdate)[]
   local datetimes = {}
   if (input == "orq") then
      table.insert(datetimes, os.date("%Y年%m月%d日"))
      table.insert(datetimes, os.date("%Y-%m-%d"))
   elseif (input == "osj") then
      table.insert(datetimes, os.date("%H时%M分%S秒"))
      table.insert(datetimes, os.date("%H:%M:%S"))
   elseif (input == "ors") then
      table.insert(datetimes, os.date("%Y年%m月%d日%H时%M分%S秒"))
      table.insert(datetimes, os.date("%Y-%m-%d %H:%M:%S"))
   end
   for _, entry in ipairs(datetimes) do
      ---@cast entry string
      rime.yield(rime.Candidate("datetime", seg.start, seg._end, entry, ""))
   end
end

return translator
