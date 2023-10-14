-- return controls to user
function resetcontrol()
    dataref("LEFTBRAKE", "sim/cockpit2/controls/left_brake_ratio", "writable")
    dataref("RIGHTBRAKE", "sim/cockpit2/controls/right_brake_ratio", "writable")
    LEFTBRAKE = 0
    RIGHTBRAKE = 0
    dataref("BRAKES", "sim/operation/override/override_toe_brakes", "writable")
    BRAKES = 0
    dataref("PARKBRAKES", "sim/flightmodel/controls/parkbrake", "writable")
	PARKBRAKES = 0
end

add_macro("Reset Controls", "resetcontrol()")