# -*- coding: utf-8 -*-

import urllib;

if (RPR_GetPlayState() == 5):
	markerFile = open('/tmp/nextMarker.txt')
	markerName = urllib.quote(markerFile.read())
	markerName = markerName.replace('%20', ' ')
	playPosition = RPR_GetPlayPosition()

	RPR_ShowConsoleMsg(markerName)
	RPR_ShowConsoleMsg(playPosition)

	index = RPR_AddProjectMarker(CURR_PROJ, 0, playPosition, playPosition, markerName, -1)
	RPR_UpdateArrange()

