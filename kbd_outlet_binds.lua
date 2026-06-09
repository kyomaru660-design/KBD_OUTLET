-- =============================================================================
-- kbd-outlet - Hyprland keybinds for your second keyboard
--
-- NO MATH REQUIRED. Each code below is ALREADY the Hyprland keycode
-- (the physical key's evdev code + 8, the xkb offset). Just edit the exec.
--
-- Every code maps to a verified-UNASSIGNED kernel keycode: no real keyboard,
-- laptop, or multimedia device emits these, so nothing can conflict.
--
-- Load it from hyprland.conf with:
--   dofile("/home/cody/.local/share/kbd-outlet/kbd_outlet_binds.lua")
--
-- Verify a key with:  wev   (press it, read the 'code' it reports)
-- =============================================================================
hl.bind("code:182", hl.dsp.no_op())
--- Number row ( ` 1 2 3 4 5 6 7 8 9 0 - = Bksp ) ---

hl.bind("code:183", hl.dsp.exec_cmd("code ~/.local/share/kbd-outlet/kbd_outlet_binds.lua"))
hl.bind("code:184", hl.dsp.exec_cmd("notify-send \"1\""))
hl.bind("code:185", hl.dsp.exec_cmd("notify-send \"2\""))
hl.bind("code:186", hl.dsp.exec_cmd("notify-send \"3\""))
hl.bind("code:187", hl.dsp.exec_cmd("notify-send \"4\""))
hl.bind("code:188", hl.dsp.exec_cmd("notify-send \"5\""))
hl.bind("code:189", hl.dsp.exec_cmd("notify-send \"6\""))
hl.bind("code:190", hl.dsp.exec_cmd("notify-send \"7\""))
hl.bind("code:191", hl.dsp.exec_cmd("notify-send \"8\""))
hl.bind("code:192", hl.dsp.exec_cmd("notify-send \"9\""))
hl.bind("code:193", hl.dsp.exec_cmd("notify-send \"0\""))
hl.bind("code:194", hl.dsp.exec_cmd("notify-send \"minus\""))
hl.bind("code:641", hl.dsp.exec_cmd("notify-send \"equal\""))
hl.bind("code:642", hl.dsp.exec_cmd("notify-send \"backspace\""))

--- Top alpha row ( Tab Q W E R T Y U I O P [ ] \ ) ---

hl.bind("code:643", hl.dsp.exec_cmd("notify-send \"tab\""))
hl.bind("code:644", hl.dsp.exec_cmd("notify-send \"Q\""))
hl.bind("code:391", hl.dsp.exec_cmd("notify-send \"W\""))
hl.bind("code:656", hl.dsp.exec_cmd("notify-send \"E\""))
hl.bind("code:657", hl.dsp.exec_cmd("notify-send \"R\""))
hl.bind("code:658", hl.dsp.exec_cmd("notify-send \"T\""))
hl.bind("code:659", hl.dsp.exec_cmd("notify-send \"Y\""))
hl.bind("code:660", hl.dsp.exec_cmd("notify-send \"U\""))
hl.bind("code:661", hl.dsp.exec_cmd("notify-send \"I\""))
hl.bind("code:662", hl.dsp.exec_cmd("notify-send \"O\""))
hl.bind("code:663", hl.dsp.exec_cmd("notify-send \"P\""))
hl.bind("code:664", hl.dsp.exec_cmd("notify-send \"leftbrace\""))
hl.bind("code:665", hl.dsp.exec_cmd("notify-send \"rightbrace\""))
hl.bind("code:666", hl.dsp.exec_cmd("notify-send \"backslash\""))

--- Home row ( Caps A S D F G H J K L ; ' Enter ) ---

hl.bind("code:667", hl.dsp.exec_cmd("notify-send \"capslock\""))
hl.bind("code:668", hl.dsp.exec_cmd("notify-send \"A\""))
hl.bind("code:669", hl.dsp.exec_cmd("notify-send \"S\""))
hl.bind("code:670", hl.dsp.exec_cmd("notify-send \"D\""))
hl.bind("code:671", hl.dsp.exec_cmd("notify-send \"F\""))
hl.bind("code:672", hl.dsp.exec_cmd("notify-send \"G\""))
hl.bind("code:673", hl.dsp.exec_cmd("notify-send \"H\""))
hl.bind("code:674", hl.dsp.exec_cmd("notify-send \"J\""))
hl.bind("code:675", hl.dsp.exec_cmd("notify-send \"K\""))
hl.bind("code:676", hl.dsp.exec_cmd("notify-send \"L\""))
hl.bind("code:677", hl.dsp.exec_cmd("notify-send \"semicolon\""))
hl.bind("code:678", hl.dsp.exec_cmd("notify-send \"apostrophe\""))
hl.bind("code:679", hl.dsp.exec_cmd("notify-send \"enter\""))

--- Bottom alpha row ( LShift Z X C V B N M , . / RShift ) ---

hl.bind("code:680", hl.dsp.exec_cmd("notify-send \"leftshift\""))
hl.bind("code:681", hl.dsp.exec_cmd("notify-send \"Z\""))
hl.bind("code:682", hl.dsp.exec_cmd("notify-send \"X\""))
hl.bind("code:683", hl.dsp.exec_cmd("notify-send \"C\""))
hl.bind("code:684", hl.dsp.exec_cmd("virt-manager"))
hl.bind("code:685", hl.dsp.exec_cmd("notify-send \"B\""))
hl.bind("code:377", hl.dsp.exec_cmd("notify-send \"N\""))
hl.bind("code:378", hl.dsp.exec_cmd("notify-send \"M\""))
hl.bind("code:379", hl.dsp.exec_cmd("notify-send \"comma\""))
hl.bind("code:380", hl.dsp.exec_cmd("notify-send \"dot\""))
hl.bind("code:381", hl.dsp.exec_cmd("notify-send \"slash\""))
hl.bind("code:382", hl.dsp.exec_cmd("notify-send \"rightshift\""))

--- Modifier row + Esc ( LCtrl LMeta LAlt Space RAlt Fn RCtrl Esc ) ---

hl.bind("code:383", hl.dsp.exec_cmd("notify-send \"leftctrl\""))
hl.bind("code:384", hl.dsp.exec_cmd("notify-send \"leftmeta\""))
hl.bind("code:385", hl.dsp.exec_cmd("notify-send \"leftalt\""))
hl.bind("code:386", hl.dsp.exec_cmd("notify-send \"space\""))
hl.bind("code:387", hl.dsp.exec_cmd("notify-send \"rightalt\""))
hl.bind("code:388", hl.dsp.exec_cmd("notify-send \"fn\""))
hl.bind("code:389", hl.dsp.exec_cmd("notify-send \"rightctrl\""))
hl.bind("code:390", hl.dsp.exec_cmd("notify-send \"escape\""))