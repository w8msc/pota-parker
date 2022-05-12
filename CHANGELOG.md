# Changelog

## Version 0.2.22, May 12, 2022
* Added: Print platform info in debug log
## Version 0.2.21, Feb 4, 2022
* Added: Display QSOs in text widget
* Changed: Display version in title bar

## Version 0.2.20, Jan 29, 2022
* Changed:  Wipe QSO now moves focus to hunter call entry

## Version 0.2.19, Jan 23, 2022
* Added: Enforce only valid characters in callsigns and park references
* Changed: Rename callbacks for trace functions

## Version 0.2.18, Jan 23, 2022
* Added: convert callsigns and parks to upper case
* Changed: Copyright year
* Changed: Tab order for field sequence: Moved their park after their call

## Version 0.2.17, Aug 9, 2021
* Changed: Fix gitignore

## Version 0.2.16, July 29, 2021
* Added: Operator field added for multi-op activations
* Changed: Re-wrote function qsoToStr eliminate if/else and chained together string construction

## Version 0.2.15, May 19, 2021
* Added: License CC BY-NC-ND 3.0
* Removed POTA copyrighted images

## Version 0.2.14, Mar 14, 2021
* Changed: check into POTA github account

## Version 0.2.13, Jan 5, 2021
* Changed: copyright year
* Added: Date/time stamp to log entries
* Fixed: modified callsigns with slash renamed to dash in filename to prevent OS filepath issues 

## Version 0.2.12, Dec 12, 2020
* Added: Entring a valid band or mode into the call text entry will now switch to that mode or band

## Version 0.2.11, Nov 24, 2020
* Changed: Status bar now displays last QSO logged
* Added: Checking import exceptions for errors on import, prevent execution for non python3 invocations
* Changed: Updated warning message

## Version 0.2.10, Nov 22, 2020
* Changed: Swap shortcut key bindings so SHIFT subtracts from fields
* Changed: Moved changes to CHANGELOG.md

## Version 0.2.9, Oct 3, 2020
* Added: Add shortcuts to focus on other station callsign and park (Control-s and Control-p)

## Version 0.2.8, Sept 30, 2020
* Added: Add key bindings to ind/dec day
* Changed: Convert day to Spinbox

## Version 0.2.7, Aug 23, 2020
* Added: Add help messagebox

## Version 0.2.6, Aug 23, 2020
* Added: Add key bindings to inc/dec hour, minute, seconds for mouseless changing of time in manual time entry mode.
* Added: Simple wrapping of individual elements, does not affect other elements

## Version 0.2.5, Aug 16, 2020
* Deleted: Clean up, remove old code

## Version 0.2.4, Aug 16, 2020
* Fixed: Convert hour, minute, second to Spinbox and bound limit values

## Version 0.2.3, May 25, 2020
* Changed: Something

## Version 0.2.2, May 24, 2020
* Fixed: Option menu doesn't scroll when in manual time entry, convert to Entry

## Version 0.2.1, May 24, 2020
* Added: Add key binding for Escape to wipe unfinished QSO
