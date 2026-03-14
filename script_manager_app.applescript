#!/usr/bin/osascript
-- 域名推广脚本管理器
-- 使用系统对话框选择脚本并运行

set scriptsDir to "/Users/guot/Desktop/杰昊/AI推广/域名推广/Code"
set pythonBin to "/usr/bin/python3"

-- 脚本列表：脚本名 -> 描述
set scriptList to {{"Trust_EN_html.py", "翻译并生成英文HTML"}, {"Translate.py", "翻译脚本"}, {"build_preview_site.py", "构建预览站点"}, {"build_category_indexes.py", "构建分类索引"}, {"build_articles_index.py", "构建文章索引"}, {"delete_chinese_articles.py", "删除中文文章"}}

-- 显示欢迎对话框
display dialog "欢迎使用域名推广脚本管理器！" & return & return & "请选择一个脚本运行：" with title "脚本管理器" buttons {"继续"} default button 1

-- 循环让用户选择脚本
repeat
    -- 构建选择列表
    set scriptNames to {}
    repeat with item in scriptList
        set end of scriptNames to item 1
    end repeat
    
    -- 显示选择对话框
    set chosenScript to choose from list scriptNames with title "选择脚本" with prompt "请选择要运行的脚本：" OK button name "运行" cancel button name "退出"
    
    if chosenScript is false then
        -- 用户取消，退出
        exit repeat
    end if
    
    set selectedScript to item 1 of chosenScript
    
    -- 查找脚本描述
    set scriptDesc to ""
    repeat with item in scriptList
        if item 1 of item is equal to selectedScript then
            set scriptDesc to item 2 of item
            exit repeat
        end if
    end repeat
    
    -- 确认运行
    set confirmRun to display dialog "确定要运行 " & selectedScript & " 吗？" & return & return & "描述：" & scriptDesc with title "确认运行" buttons {"运行", "取消"} default button 2
    
    if button returned of confirmRun is "取消" then
        -- 用户取消，继续循环
    else
        -- 运行脚本
        set scriptPath to scriptsDir & "/" & selectedScript
        set command to pythonBin & " " & scriptPath
        
        -- 显示正在运行
        display dialog "正在运行 " & selectedScript & "..." with title "运行中" buttons {"等待"} giving up after 2
        
        -- 运行脚本并获取输出
        try
            set outputPath to scriptsDir & "/.run_output.txt"
            set fullCommand to "cd " & quoted form of scriptsDir & " && " & pythonBin & " " & quoted form of selectedScript & " > " & quoted form of outputPath & " 2>&1"
            do shell script fullCommand
            
            -- 打开输出文件
            tell application "Finder"
                open POSIX file outputPath
            end tell
            
            display dialog "脚本运行完成！" & return & return & "输出已保存到 .run_output.txt" with title "完成" buttons {"确定"} default button 1
            
        on error errMsg
            display dialog "运行失败：" & return & errMsg with title "错误" buttons {"确定"} default button 1
        end try
    end if
    
end repeat

display dialog "再见！" with title "退出" buttons {"确定"} default button 1