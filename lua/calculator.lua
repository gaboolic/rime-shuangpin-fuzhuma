local M = {}

function M.init(env)
  local config = env.engine.schema.config
  env.name_space = env.name_space:gsub('^*', '')
  M.prefix = config:get_string(env.name_space .. '/trigger') or 'calc'
end

local function startsWith(str, start)
  return string.sub(str, 1, string.len(start)) == start
end

local function truncateFromStart(str, truncateStr)
  return string.sub(str, string.len(truncateStr) + 1)
end

local function replaceMathFunc(express)
  -- 不使用string.gsub(str, "SIN%(([0-9]+)%)", "math.sin(%1)"), 因为无法处理SIN(SIN(x))这种情况
  -- 转大写避免重复替换, 空格是为了给第一个[^A-z]留空间
  local str = " " .. string.upper(express)
  str = string.gsub(str, "([^A-z])ASIN%(", "%1math.asin(")     -- 反正弦
  str = string.gsub(str, "([^A-z])SINH%(", "%1math.sinh(")     -- 双曲正弦
  str = string.gsub(str, "([^A-z])SIN%(", "%1math.sin(")       -- 正弦
  str = string.gsub(str, "([^A-z])ACOS%(", "%1math.acos(")     -- 反余弦
  str = string.gsub(str, "([^A-z])COSH%(", "%1math.cosh(")     -- 双曲余弦
  str = string.gsub(str, "([^A-z])COS%(", "%1math.cos(")       -- 余弦
  str = string.gsub(str, "([^A-z])ATAN2%(", "%1math.atan2(")   -- atan2(y,x). 返回y/x的反正切(以弧度为单位), 但使用两个参数的符号来查找结果的象限.
  str = string.gsub(str, "([^A-z])ATAN%(", "%1math.atan(")     -- 反正切
  str = string.gsub(str, "([^A-z])TANH%(", "%1math.tanh(")     -- 双曲正切
  str = string.gsub(str, "([^A-z])TAN%(", "%1math.tan(")       -- 正切
  str = string.gsub(str, "([^A-z])DEG%(", "%1math.deg(")       -- 以度为单位返回角度x
  str = string.gsub(str, "([^A-z])RAD%(", "%1math.rad(")       -- 以弧度为单位返回角度x
  -- str = string.gsub(str, "([^A-z])FREXP%(", "%1math.frexp(")   -- frexp(x). 返回m,e 使得x = m*2^e
  -- str = string.gsub(str, "([^A-z])LDEXP%(", "%1math.ldexp(")   -- ldexp(m, e). 返回m*2^e
  str = string.gsub(str, "([^A-z])EXP%(", "%1math.exp(")       -- exp(x). e的x次幂
  str = string.gsub(str, "([^A-z])LOG10%(", "%1math.log10(")   -- 以10为底的对数
  str = string.gsub(str, "([^A-z])LOG%(", "%1math.log(")       -- 自然对数(e为底)
  str = string.gsub(str, "([^A-z])RANDOM%(", "%1math.random(") -- random([m[, n]]), m - n 之间的随机数
  str = string.gsub(str, "([^A-z])SQRT%(", "%1math.sqrt(")     -- x的平方根. 等于x^0.5
  str = string.gsub(str, "([^A-z])PI", "%1math.pi")            -- π
  -- 去除第一个字符(手动添加的空格)
  return string.sub(str, 2)
end

-- 简单计算器
-- BUG: 不支持小键盘 + - * /
function M.func(input, seg, env)
  if not startsWith(input, M.prefix) then return end
  -- 提取算式
  local express = truncateFromStart(input, M.prefix)
  -- 算式长度 < 2 直接终止(没有计算意义)
  if (string.len(express) < 2) then return end
  -- pcall()的原因需要控制一下 . 符号的位置
  if (string.match(express, "[^0-9]%.")) then
    yield(Candidate(input, seg.start, seg._end, express, "小数点不能在非数字字符后面"))
    return
  end

  local code = replaceMathFunc(express)
  local success, result = pcall(load("return " .. code))
  if success then
    yield(Candidate(input, seg.start, seg._end, result, ""))
    yield(Candidate(input, seg.start, seg._end, express .. "=" .. result, ""))
  else
    yield(Candidate(input, seg.start, seg._end, express, "解析失败"))
    yield(Candidate(input, seg.start, seg._end, code, "入参"))
    -- TODO: 错误信息记录到日志中
    -- print("express: " .. express)
    -- print("code: " .. code)
    -- print("result: " .. result)
  end
end

return M
