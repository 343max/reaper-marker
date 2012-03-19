# -*- coding: utf-8 -*-

import urllib;

CURR_PROJ = RPR_EnumProjects(-1, None, 0)

if (RPR_GetPlayState() == 5):
	markerFile = open('/tmp/nextMarker.txt')
	markerName = urllib.quote(markerFile.read())
	markerFile.close()

	markerFile = open('/tmp/nextMarker.txt', 'w')
	markerFile.close

	if (markerName != ''):
			markerName = markerName.replace('%20', ' ')
			playPosition = RPR_GetPlayPosition()

			# RPR_ShowConsoleMsg(markerName)
			# RPR_ShowConsoleMsg(playPosition)

			index = RPR_AddProjectMarker(CURR_PROJ, 0, playPosition, playPosition, markerName, -1)
			RPR_UpdateArrange()
