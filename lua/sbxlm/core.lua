-- 声笔系列码核心逻辑
-- 存放了一些常用的函数，方便调用

local rime = require "sbxlm.lib"
local match = rime.match
local core = {}

-- 大键盘的所有按键
local s = "[bpmfdtnlgkhjqxzcsrywv]";
-- 小键盘的所有按键
local b = "[aeiou]";
-- 所有按键
local x = "[a-z]";

----------------------------------------
-- 以下为一系列常用的正则匹配函数
-- 用于判断输入是否符合某种格式
-- 例如：core.s(input) 判断输入是否为一个声母

---@param input string
function core.s(input)
  return match(input, s)
end

---@param input string
function core.ss(input)
  return match(input, s .. s)
end

---@param input string
function core.sx(input)
  return match(input, s .. x)
end

---@param input string
function core.sb(input)
  return match(input, s .. b)
end

---@param input string
function core.sxb(input)
  return match(input, s .. x .. b)
end

---@param input string
function core.sss(input)
  return match(input, s .. s .. s)
end

---@param input string
function core.sxs(input)
  return match(input, s .. x .. s)
end

---@param input string
function core.sbsb(input)
  return match(input, s .. b .. s .. b)
end

---@param input string
function core.sxsb(input)
  return match(input, s .. x .. s .. b)
end

---@param input string
function core.ssb(input)
  return match(input, s .. s .. b)
end

---@param input string
function core.ssbb(input)
  return match(input, s .. s .. b .. b)
end

---@param input string
function core.sxbb(input)
  return match(input, s .. x .. b .. b)
end
----------------------------------------
-- 以下为一系列常用的方案判断函数
-- 用于判断当前方案是否为某种方案
-- 例如：core.feixi(id) 判断当前方案是否为飞系方案

---@param id string
function core.feixi(id)
  return id == "sbfd" or id == "sbfm" or id == "sbfx"
end

---@param id string
function core.jm(id)
  return id == "sbjm"
end

---@param id string
function core.fm(id)
  return id == "sbfm"
end

---@param id string
function core.fd(id)
  return id == "sbfd"
end

---@param id string
function core.fx(id)
  return id == "sbfx"
end

---@param id string
function core.sp(id)
  return id == "sbzr" or id == "sbxh"
end

---@param id string
function core.zici(id)
  return id == "sbfd" or id == "sbfm" or id == "sbfx" or id == "sbjm" or id == "sbzr" or id == "sbxh"
end


---判断一个 sb 格式的编码在小鹤、自然双拼方案中是否为无效拼音
---如果是，那么这个编码就是声笔字，需要提示
---@param sb string
function core.invalid_pinyin(sb)
  for _, value in ipairs({ "[bpfw]e", "[gkhfwv]i", "[jqx][aoe]", "ra", "vu" }) do
    if match(sb, value) then
      return true
    end
  end
  return false
end

---执行各方案的实际造词逻辑
---目前在 lua 中没有找到获取组词规则的方法
---因为 TableEncoder 在 librime 里是被 TableTranslator 调用的，没有封装出独立的 API
---所以这里只能用一个大的 if-else 语句来判断，硬编码各个方案的组词规则
---以后如果有更好的方法，再来重构这个函数
---@param code string[]
---@param id string
function core.word_rules(code, id)
  -- 不考虑扩展编码时，词组的基本编码
  local base = ""
  local jm = core.jm(id)
  local fm = core.fm(id) or core.fd(id)
  local sp = core.sp(id)
  local fx = core.fx(id)
  if #code == 2 then
    if jm then           -- s1s2b2b2
      base = code[1]:sub(1, 1) .. code[2]:sub(1, 3)
    elseif fm or sp then -- s1z1s2z2
      base = code[1]:sub(1, 2) .. code[2]:sub(1, 2)
    elseif fx then       -- s1z1s2b2b2
      base = code[1]:sub(1, 2) .. code[2]:sub(1, 1) .. code[2]:sub(3, 4)
    end
  else
    base = code[1]:sub(1, 1) .. code[2]:sub(1, 1) .. code[3]:sub(1, 1)
    if #code == 3 then
      if jm or fm or sp then -- s1s2s3z3
        base = base .. code[3]:sub(2, 2)
      elseif fx then         -- s1s2s3b3b3
        base = base .. code[3]:sub(3, 4)
      end
    elseif #code >= 4 then
      if jm then           -- s1s2s3b0
        base = base .. code[#code]:sub(2, 2)
      elseif fm or sp then -- s1s2s3s0
        base = base .. code[#code]:sub(1, 1)
      elseif fx then       -- s1s2s3b0b0
        base = base .. code[#code]:sub(3, 4)
      end
    else
      return nil
    end
  end
  -- 扩展编码为首字前两笔，但是这个笔在不同方案中有不同的取法
  local extended = ""
  if jm then
    extended = code[1]:sub(2, 3)
  elseif fm or fx or sp then
    extended = code[1]:sub(3, 4)
  end
  -- 全部编码为基本编码加上扩展编码
  local full = base .. extended
  -- 对于简码和飞讯，多字词有两种打法，之前生成的打法没有考虑用 ssss 格式的情况。
  -- 这里，在编码的最后增加一个末字的声母，然后在检索的时候动态判断
  if (jm or fx) and #code >= 4 then
    full = full .. code[#code]:sub(1, 1)
  end
  return full
end

function core.reverse(id)
  --相当于三目运算符a ? b : c
  local dict_name = id == "sbfd" and "sbfm" or id
  --如果不是飞系方案，单字构词码在扩展词库里
  if not core.feixi(id) then
    dict_name = dict_name .. ".extended"
  end
  return rime.ReverseLookup(dict_name)
end

return core
