local function filter(t_input, env)
   for cand in t_input:iter() do
      cand.comment = cand.comment .. tostring(cand.type) .. " " .. tostring(cand.quality)
      yield(cand)
   end
end
return filter
