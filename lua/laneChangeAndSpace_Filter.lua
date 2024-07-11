-- laneChangeAndSpace_Filter.lua
-- 来自https://github.com/happyDom/dyyRime/tree/master/lua
-- Copyright (C) 2023 yaoyuan.dou <douyaoyuan@126.com>
-- 这个过滤器的作用有二：
-- 1、当候选项的候选词或者注释中出现 <br> 时，将其处理成 \r 以实现换行效果
-- 2、当候选项的候选词或者注释中出现 &nbsp 时，将其处理成空格，以实现空格效果
-- 3、当候选项的注释长度超过限定值时，对其进行截短并添加截断标记

local dbgFlg = true

--comment单行最长长度限制
local maxLenOfComment = 150

--引入 utf8String 处理字符串相关操作
local utf8StringEnable, utf8String = pcall(require, 'utf8String')

local logEnable, log = pcall(require, "runLog")
if logEnable then
	log.writeLog('')
	log.writeLog('log from laneChangeAndSpace_Filter.lua')
	log.writeLog('utf8StringEnable:'..tostring(utf8StringEnable))
end

local utf8Split = utf8String.utf8Split
local utf8Sub = utf8String.utf8Sub
local utf8Len = utf8String.utf8Len
local utf8PunctuationsTrim = utf8String.utf8PunctuationsTrim

--过滤器
local function laneChangeAndSpace_Filter(input, env)
	local candTxt
	local candComment
	local candTxtNewFlg
	local candComment_brExistFlg
	local candCommentNewFlg
	local bottomLineLen
	
	for cand in input:iter() do
		--读取选项候选词
		candTxt = cand.text or ""
		--读取选项注释内容
		candComment = cand.comment or ""
		
		candTxtNewFlg = false
		if nil ~= string.find(candTxt,"<br>") or nil ~= string.find(candTxt,"&nbsp") then
			-- candTxt 存在 <br> 或者 &nbsp
			candTxtNewFlg = true
			candTxt = candTxt: gsub("<br>","\r")
		end
		
		if candTxtNewFlg then
			
			--如果存在新的候选项，则需要生成新的候选词
			yield(Candidate("word", cand.start, cand._end, candTxt, candComment))
		else
			--如果不存在新的候选项且不存在新注释，则抛出原候选项对象
			yield(cand)
		end
	end
end

return laneChangeAndSpace_Filter
