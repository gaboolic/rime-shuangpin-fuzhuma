-- doing 末码为/时，候选项如果唯一，则自动上屏
-- @gaboolic


local M = {}

function M.init(env)
  
end


function M.func(input,env)
    log.info("slach_pop M.func")
    local context = env.engine.context
    -- lua文档 https://github.com/hchunhui/librime-lua/wiki/Scripting
    if input == 'uiui/' and context:has_menu() then
        context:confirm_current_selection()
        if not is_buffered then
        context:commit()
        end
        success = true
    end
end

return M
