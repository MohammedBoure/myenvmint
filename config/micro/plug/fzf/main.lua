VERSION = "1.1.2"

local micro = import("micro")
local shell = import("micro/shell")
local config = import("micro/config")
local buffer = import("micro/buffer")

function fzf(bp)
    -- If currently focused on a scratch/filemanager pane, switch to active editor pane
    if bp.Buf.Type.Scratch then
        bp:NextSplit()
        bp = micro.CurPane()
    end

    local output, err = shell.RunInteractiveShell("fzf", false, true)
    if err ~= nil then
        micro.InfoBar():Error(err)
    else
        fzfOutput(output, {bp})
    end
end

function fzfOutput(output, args)
    local bp = args[1]
    local strings = import("strings")
    output = strings.TrimSpace(output)
    if output ~= "" then
        local bftype = config.GetGlobalOption("openbftype")
        if bftype == nil or bftype == "" then
            bftype = config.GetGlobalOption("fzf.openbftype")
        end
        if bftype == "tab" and bp.Buf.Path ~= "" then
            bp:HandleCommand('tab "' .. output .. '"')
        else
            bp:HandleCommand('open "' .. output .. '"')
        end
    end
end

function init()
    config.RegisterGlobalOption("fzf", "openbftype", "tab")
    config.MakeCommand("fzf", fzf, config.NoComplete)
end
