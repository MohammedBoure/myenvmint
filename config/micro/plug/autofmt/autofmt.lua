VERSION = "2.0.0"

local micro = import("micro")
local config = import("micro/config")
local shell = import("micro/shell")
local buffer = import("micro/buffer")

-- Re-entrancy guard to prevent recursive loops on save
local isFormatting = false

-- Resolve executable path or fallback to command name
local function getTool(name)
    local home = os.getenv("HOME") or "/home/pluto"
    local candidates = {
        home .. "/.local/bin/" .. name,
        home .. "/.cargo/bin/" .. name,
        "/usr/local/bin/" .. name,
        "/usr/bin/" .. name,
        name
    }
    for _, p in ipairs(candidates) do
        local f = io.open(p, "r")
        if f ~= nil then
            f:close()
            return p
        end
    end
    return name
end

-- Checks if a tool is executable/available
local function toolExists(name)
    local tool = getTool(name)
    local testCmd = "command -v " .. tool .. " >/dev/null 2>&1"
    local res = os.execute(testCmd)
    return (res == 0 or res == true)
end

-- Extracts leading whitespace from a string
local function getLeadingWhitespace(line)
    return line:match("^(%s*)") or ""
end

-- Smart syntax-aware indentation on Enter
function onInsertNewline(bp)
    local enabled = bp.Buf.Settings["autofmt.smartindent"]
    if enabled == false then return end

    local y = bp.Cursor.Y
    if y <= 0 then return end

    local prevLine = bp.Buf:Line(y - 1)
    local curLine = bp.Buf:Line(y)

    local prevWs = getLeadingWhitespace(prevLine)
    local curWs = getLeadingWhitespace(curLine)

    -- If current line is already more indented than previous line (e.g. by autoclose), do nothing
    if curWs:len() > prevWs:len() then
        return
    end

    -- Clean the previous line: strip comments and trailing whitespace
    local clean = prevLine
    local ft = bp.Buf:FileType()
    if ft == "python" or ft == "ruby" or ft == "shell" or ft == "bash" or ft == "yaml" then
        clean = clean:gsub("#.*$", "")
    else
        clean = clean:gsub("//.*$", "")
    end
    clean = clean:match("^(.-)%s*$") or ""
    if clean == "" then return end

    local lastChar = clean:sub(-1)
    local shouldIndent = false

    -- Block opening with braces, parens, brackets (C, C++, Rust, Go, JS, TS, etc.)
    if lastChar == "{" or lastChar == "(" or lastChar == "[" then
        shouldIndent = true
    elseif lastChar == ":" then
        -- Python block triggers
        if ft == "python" then
            if clean:match("^%s*if%s") or
               clean:match("^%s*elif%s") or
               clean:match("^%s*else%s*:") or
               clean:match("^%s*for%s") or
               clean:match("^%s*while%s") or
               clean:match("^%s*def%s") or
               clean:match("^%s*class%s") or
               clean:match("^%s*with%s") or
               clean:match("^%s*try%s*:") or
               clean:match("^%s*except") or
               clean:match("^%s*finally%s*:") or
               clean:match("^%s*match%s") or
               clean:match("^%s*case%s") or
               clean:match("^%s*async%s") then
                shouldIndent = true
            end
        else
            shouldIndent = true
        end
    end

    if shouldIndent then
        bp:IndentLine()
    end
end

-- Formats a selected part of code (lines startLine to endLine)
local function formatRange(bp, startLine, endLine)
    local ft = bp.Buf:FileType()
    local path = bp.Buf.AbsPath
    if path == nil or path == "" then
        path = bp.Buf.Path
    end

    local cmd = nil

    if ft == "c" or ft == "cpp" or ft == "c++" or ft == "csharp" or ft == "java" or ft == "javascript" then
        local clangFmt = getTool("clang-format")
        cmd = clangFmt .. " -i --lines=" .. startLine .. ":" .. endLine .. ' "' .. path .. '"'
    elseif ft == "python" then
        if toolExists("autopep8") then
            local autopep8 = getTool("autopep8")
            cmd = autopep8 .. " --in-place --line-range " .. startLine .. " " .. endLine .. ' "' .. path .. '"'
        elseif toolExists("ruff") then
            local ruff = getTool("ruff")
            cmd = ruff .. ' format "' .. path .. '"'
        elseif toolExists("black") then
            local black = getTool("black")
            cmd = black .. ' -q "' .. path .. '"'
        end
    elseif ft == "rust" then
        if toolExists("rustfmt") then
            local rustfmt = getTool("rustfmt")
            cmd = rustfmt .. ' "' .. path .. '"'
        end
    end

    if cmd == nil then
        micro.InfoBar():Message("No range formatter configured for filetype '" .. ft .. "'")
        return false
    end

    local curLoc = buffer.Loc(bp.Cursor.X, bp.Cursor.Y)
    local exitCode = os.execute(cmd)
    if exitCode == 0 or exitCode == true then
        bp.Buf:ReOpen()
        bp:GotoLoc(curLoc)
        micro.InfoBar():Message("Cleaned & positioned lines " .. startLine .. " - " .. endLine)
        return true
    else
        micro.InfoBar():Error("Formatter command failed: " .. cmd)
        return false
    end
end

-- Formats the entire buffer file
local function formatFile(bp, silent)
    local ft = bp.Buf:FileType()
    local path = bp.Buf.AbsPath
    if path == nil or path == "" then
        path = bp.Buf.Path
    end

    local cmd = nil

    if ft == "python" then
        local pyTool = bp.Buf.Settings["autofmt.python"] or "ruff"
        if pyTool == "ruff" and toolExists("ruff") then
            cmd = getTool("ruff") .. ' format "' .. path .. '"'
        elseif (pyTool == "black" or not toolExists("ruff")) and toolExists("black") then
            cmd = getTool("black") .. ' -q "' .. path .. '"'
        elseif toolExists("autopep8") then
            cmd = getTool("autopep8") .. ' --in-place "' .. path .. '"'
        elseif toolExists("ruff") then
            cmd = getTool("ruff") .. ' format "' .. path .. '"'
        end
    elseif ft == "c" or ft == "cpp" or ft == "c++" or ft == "csharp" or ft == "java" then
        if toolExists("clang-format") then
            cmd = getTool("clang-format") .. ' -i "' .. path .. '"'
        end
    elseif ft == "rust" then
        if toolExists("rustfmt") then
            cmd = getTool("rustfmt") .. ' "' .. path .. '"'
        end
    elseif ft == "go" then
        if toolExists("gofmt") then
            cmd = getTool("gofmt") .. ' -w "' .. path .. '"'
        end
    elseif ft == "javascript" or ft == "typescript" or ft == "json" or ft == "html" or ft == "css" or ft == "markdown" then
        if toolExists("prettier") then
            cmd = getTool("prettier") .. ' --write --log-level silent "' .. path .. '"'
        end
    end

    if cmd == nil then
        if not silent then
            micro.InfoBar():Message("No whole-file formatter found for filetype '" .. ft .. "'")
        end
        return false
    end

    local curLoc = buffer.Loc(bp.Cursor.X, bp.Cursor.Y)
    local exitCode = os.execute(cmd)
    if exitCode == 0 or exitCode == true then
        bp.Buf:ReOpen()
        bp:GotoLoc(curLoc)
        if not silent then
            micro.InfoBar():Message("Formatted " .. bp.Buf.Path)
        end
        return true
    else
        if not silent then
            micro.InfoBar():Error("Formatter failed: " .. cmd)
        end
        return false
    end
end

-- Primary format command (Alt-f or 'format' command)
-- Automatically checks if a part of code is selected:
-- - If selected: auto-sets position / formats only that selection range
-- - If not selected: auto-sets position / formats the entire file
function formatCommand(bp, args)
    if bp.Buf.Path == nil or bp.Buf.Path == "" then
        micro.InfoBar():Error("autofmt: Please save file before formatting")
        return
    end

    -- Ensure buffer is saved to disk so formatter sees latest changes
    bp:Save()

    -- If user forced "file" arg, format entire file
    if args ~= nil and #args > 0 and args[1] == "file" then
        formatFile(bp, false)
        return
    end

    if bp.Cursor:HasSelection() then
        local c = bp.Cursor
        local y1 = c.CurSelection[1].Y
        local y2 = c.CurSelection[2].Y
        local x1 = c.CurSelection[1].X
        local x2 = c.CurSelection[2].X

        local startY = y1
        local endY = y2
        local startX = x1
        local endX = x2

        if y1 > y2 or (y1 == y2 and x1 > x2) then
            startY = y2
            endY = y1
            startX = x2
            endX = x1
        end

        if endX == 0 and endY > startY then
            endY = endY - 1
        end

        local startLine = startY + 1
        local endLine = endY + 1

        formatRange(bp, startLine, endLine)
    else
        formatFile(bp, false)
    end
end

-- Force whole-file format command
function fmtFileCommand(bp, args)
    if bp.Buf.Path == nil or bp.Buf.Path == "" then
        micro.InfoBar():Error("autofmt: Please save file before formatting")
        return
    end
    bp:Save()
    formatFile(bp, false)
end

-- Automatic format on save
function onSave(bp)
    if isFormatting then return end
    if bp.Buf.Settings["autofmt.onsave"] then
        isFormatting = true
        formatFile(bp, true)
        isFormatting = false
    end
end

function init()
    config.RegisterCommonOption("autofmt", "onsave", true)
    config.RegisterCommonOption("autofmt", "smartindent", true)
    config.RegisterCommonOption("autofmt", "python", "ruff")
    config.RegisterCommonOption("autofmt", "c", "clang-format")
    config.RegisterCommonOption("autofmt", "rust", "rustfmt")

    config.MakeCommand("format", formatCommand, config.NoComplete)
    config.MakeCommand("fmt", formatCommand, config.NoComplete)
    config.MakeCommand("fmtfile", fmtFileCommand, config.NoComplete)
end
