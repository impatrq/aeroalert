-- require("radio")
--sim/GPS/g1000n1_apr
--sim/GPS/g1000n1_hdg
fired = false
firedTwo = false
firedThree = false
firedILS = false
firedRNWY = false
fireACT = false
autolandone = load_WAV_file("Resources/plugins/FlyWithLua/Scripts/autoland1.wav")
set_sound_gain(autolandone, 1.0)
let_sound_loop(autolandone, false)
autolandtwo = load_WAV_file("Resources/plugins/FlyWithLua/Scripts/autoland2.wav")
set_sound_gain(autolandtwo, 1.0)
let_sound_loop(autolandtwo, false)
autolandfour = load_WAV_file("Resources/plugins/FlyWithLua/Scripts/autoland4.wav")
set_sound_gain(autolandfour, 1.0)
let_sound_loop(autolandfour, false)
autolandfive = load_WAV_file("Resources/plugins/FlyWithLua/Scripts/autoland5.wav")
set_sound_gain(autolandfive, 1.0)
let_sound_loop(autolandfive, false)


function safereturn()
    play_sound(autolandone)

    -- squawk 7700 and mode C
    dataref("sqkCode", "sim/cockpit2/radios/actuators/transponder_code", "writable")
    sqkCode = 7700
    dataref("sqkMode", "sim/cockpit2/radios/actuators/transponder_mode", "writable")
    sqkMode = 2

    -- QNH must be accurate
    pilotQNH   = XPLMFindDataRef("sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot")
    actualQNH  = XPLMFindDataRef("sim/weather/barometer_sealevel_inhg")
    XPLMSetDataf(pilotQNH,   XPLMGetDataf(actualQNH))
    
    -- wing level
    command_once("sim/autopilot/wing_leveler")

    -- fd ap on
    command_once("sim/autopilot/fdir_on")
    command_once("sim/autopilot/servos_on")

    -- check we're in GPS mode
    dataref("CDIVLOC", "sim/cockpit2/radios/actuators/HSI_source_select_pilot", "writable")
    CDIVLOC = 0
    command_once("sim/cockpit/autopilot/heading")
    dataref("altitude", "sim/cockpit2/autopilot/altitude_readout_preselector", "writable")
    -- DESCEND ON CURRENT HEADING

    -- set altitude - aim for 1200 but will stop at 1200agl. this should get us in on most glideslopes.
    local ln_alt = dataref_table("sim/cockpit/autopilot/altitude", "writable")
    ln_alt[0] = 1200
    local ln_vs = dataref_table("sim/cockpit/autopilot/vertical_velocity", "writable")
    if altitude < 4200 then
        ln_vs[0] = -1500
    elseif altitude > 4200 then
        if altitude > 7500 then
            ln_vs[0] = -2200
        elseif altitude < 7500 then
            ln_vs[0] = -1800
        end
    end

    -- AT ON
    dataref("ATON", "sim/cockpit2/autopilot/autothrottle_enabled", "writable")
    ATON = 1
    
    -- SET DESCENT SPEED 165KIAS
    dataref("SPEEDSET", "sim/cockpit/autopilot/airspeed", "writable")
    SPEEDSET = 165

    function checkAlt()
        alt = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/y_agl"))
        ground = alt * 3.2808399
        if (ground < 1200 and fired == false) then
            fired = true
            command_once("sim/autopilot/altitude_hold")
            phasetwo()
            command_once("sim/autopilot/vertical_speed_pre_sel")
        end
    end

    do_often("checkAlt()")
end

function phasetwo()
    dataref("FL_CURR_ALT", "sim/cockpit2/autopilot/altitude_readout_preselector")
    inCurr_Alt = math.floor(FL_CURR_ALT)
    -- WHEN DESCENT DONE
    play_sound(autolandtwo)
    -- 128KIAS
    SPEEDSET = 128
    -- put flaps down
    command_once("sim/flight_controls/flaps_down")
    -- gear down
    command_once("sim/flight_controls/landing_gear_down")
    command_once("sim/autopilot/vertical_speed")
    -- check ILS is valid (if not, keep checking) and run distance check
    function checkILS()
        -- get my lat lon
        lat = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/latitude"))
        lon = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/longitude"))
        dataref("altitude", "sim/cockpit2/autopilot/altitude_readout_preselector", "writable")
        local ln_vs = dataref_table("sim/cockpit/autopilot/vertical_velocity", "writable")
        function altitude_check()
            if altitude < 4200 then
                ln_vs[0] = -1500
                if altitude < 3000 then
                    ln_vs[0] = -1000
                elseif altitude < 2000 then
                    ln_vs[0] = -700
                elseif altitude < 1500 then
                    ln_vs[0] = -500
                elseif altitude < 1000 then
                    ln_vs[0] = -150
                end
            elseif altitude > 4200 then
                if altitude > 7500 then
                    ln_vs[0] = -2200
                elseif altitude < 7500 then
                    ln_vs[0] = -1800
                end
            end
        end
        do_often("altitude_check()")
        -- find closest ils and store so we can retrieve freq
        local airport_ILS
        _, _, _, _, _, _, airport_ILS, _ = XPLMGetNavAidInfo( XPLMFindNavAid( nil, nil, lat, lon, nil, xplm_Nav_ILS) )
        -- find closest ILS freq
        local ILS_freq
        one, airLat, airLon, four, ILS_freq, six, seven, _ = XPLMGetNavAidInfo( XPLMFindNavAid( nil, airport_ILS, lat, lon, nil, xplm_Nav_ILS) )
        if (airport_ILS ~= "NTFND" and firedILS == false) then
            firedILS = true
            -- tune radio
            dataref("NAVONE", "sim/cockpit/radios/nav1_freq_hz", "writable")
            dataref("NAVTWO", "sim/cockpit/radios/nav1_stdby_freq_hz", "writable")
            NAVONE = ILS_freq
            NAVTWO = ILS_freq
            -- navigate to the ILS
            XPLMClearFMSEntry(0)
            XPLMSetFMSEntryInfo(0, XPLMFindNavAid( nil, airport_ILS, nil, nil, ILS_freq, xplm_Nav_ILS), 2000)
            XPLMSetDestinationFMSEntry(0)
            command_once("sim/autopilot/NAV")
            logMsg(airport_ILS)
            -- run distance check
            checkDist()
            if (firedILS == true) then
                command_once("sim/GPS/g1000n1_hdg")
            end	
        elseif(airport_ILS == "NTFND") then
            logMsg("ILS Route Not Found")
        end
    end
    do_often("checkILS()")
end

function checkDist ()
    function checker()
        dist = XPLMGetDataf(XPLMFindDataRef("sim/cockpit2/radios/indicators/gps_dme_distance_nm"))
        altland = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/y_agl"))
        groundland = altland * 3.2808399
        dataref("CRS", "sim/cockpit/radios/nav1_course_degm","readonly")
        dataref("HDG", "sim/cockpit/autopilot/heading_mag", "writable")
        dataref("Course", "sim/cockpit/radios/nav1_course_degm", "writable")
        dataref("APP", "sim/private/controls/atc/routing/runway_steep_angle", "writable")
        hdgcounter = 0
        HDG = CRS + 270
        inCrs = math.floor(CRS)
        inNavCrs = math.floor(Course)
        logMsg(inCrs)
        logMsg(inNavCrs)
        logMsg(HDG)
        if 8 > inNavCrs  - inCrs then
            hdgcounter = hdgcounter +1
            if (inNavCrs  - inCrs > 1  and firedRNWY == false) then
                firedRNWY = true
                HDG = CRS
                land()
                logMsg('one')
            end
       elseif firedRNWY == true then
            HDG = CRS 
            land()
            logMsg('onee')
    
       elseif firedRNWY == true and dist < 5 then
            land()
        elseif (dist > 25 and groundland < 1000) then
            caps()
            logMsg("Far away from approach route")
        end
    end
    do_often("checker()")
end

function land()

    -- APPROACH PHASE
    dist = XPLMGetDataf(XPLMFindDataRef("sim/cockpit2/radios/indicators/gps_dme_distance_nm"))
    -- switch to radio beacon nav for ILS
    dataref("SPEEDSET", "sim/cockpit/autopilot/airspeed", "writable")
    CDIVLOC = 0
    ln_alt = dataref_table("sim/cockpit/autopilot/altitude", "writable")
    ln_alt[0] = 1200
    ln_vs = dataref_table("sim/cockpit/autopilot/vertical_velocity", "writable")
    if dist >= 6 then
        SPEEDSET = 110
    elseif dist < 6 then
        SPEEDSET = 85
    end
    -- wait for land
    function checkLand()
        altland = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/y_agl"))
        groundland = altland * 3.2808399
        vertfpm = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/vh_ind_fpm"))
        dist = XPLMGetDataf(XPLMFindDataRef("sim/cockpit2/radios/indicators/gps_dme_distance_nm"))
        dataref("APR", "sim/cockpit2/autopilot/approach_status", "writable")
        APR = 2
        -- all has gone well, cut engine at touchdown
        if (groundland < 75 and firedThree == false) then
            firedThree = true
            rollout()
            logMsg("Great Landing!")
        -- pops chute if near airport but not on GS
        elseif (dist < 1 and groundland >= 1300 and vertfpm > -50 and firedThree == false) then
            firedThree = true
            caps()
            logMsg("Near airport but not on GS")
        -- if it starts flying away from the airport (downwind ils etc)
        elseif (dist > 25 and firedThree == false) then
            firedThree = true
            caps()
            logMsg("Flying away from airport")
        end
    end

    do_often("checkLand()")

end

function caps()

    -- IF WE ARE OFF-GLIDESLOPE CLOSE TO THE ARPT OR APPROACHING RISING TERRAIN BEFORE 5NM OUT, POP THE CHUTE.
    -- REQUIRES MODIFIED .ACF FOR SAFE CAPS LANDING, AS DEFAULT CHUTE IS INEFFECTIVE.

    play_sound(autolandfive)

    -- engines OFF
    dataref("fuelSelector", "sim/cockpit2/fuel/fuel_tank_selector", "writable")
    fuelSelector = 0

    -- deploy CAPS
    dataref("chute", "sim/cockpit2/switches/parachute_deploy", "writable")
    chute = 1

    -- brakes full
    dataref("BRAKES", "sim/operation/override/override_toe_brakes", "writable")
    BRAKES = 1
    dataref("LEFTBRAKE", "sim/cockpit2/controls/left_brake_ratio", "writable")
    dataref("RIGHTBRAKE", "sim/cockpit2/controls/right_brake_ratio", "writable")
    LEFTBRAKE = 1
    RIGHTBRAKE = 1
    logMsg("OFF - GS OR Mountains near approach route")

end

function rollout()

    -- ROLLOUT PHASE
    play_sound(autolandfour)

    -- engines OFF
    altland = XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/y_agl"))
    groundland = altland * 3.2808399
    if groundland < 75 then
        dataref("fuelSelector", "sim/cockpit2/fuel/fuel_tank_selector", "writable")
        fuelSelector = 0
    end
    -- brakes full
    dataref("PARKBRAKES", "sim/flightmodel/controls/parkbrake", "writable")
    PARKBRAKES = 1
    dataref("BRAKES", "sim/operation/override/override_toe_brakes", "writable")
    BRAKES = 1
    dataref("LEFTBRAKE", "sim/cockpit2/controls/left_brake_ratio", "writable")
    dataref("RIGHTBRAKE", "sim/cockpit2/controls/right_brake_ratio", "writable")
    LEFTBRAKE = 1
    RIGHTBRAKE = 1

end
add_macro("Safe Return", "safereturn()")
--Create a command, in order to run the whole script via UDP communication
create_command( "FlyWithLua/ViewPoint/Safe_Return", "Emergency Autoland",
                "safereturn()",
                "checkDist()",
                "phasetwo()")
