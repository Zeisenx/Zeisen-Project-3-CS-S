
import es
import est
import playerlib
import gamethread
import random
import spe
from spe import HookAction
from spe import HookType
from spe.tools.player import SPEPlayer
from spe.tools import SPEBaseEntity
from spe.tools.weapon import SPEWeapon
import ctypes
import esc
import popuplib
import usermsg
import repeat
import vecmath
from configobj import ConfigObj
from path import path
import re
import iptocountry
import cmdlib
import keyvalues
import os
import time
import math
import serverlib

sv = es.ServerVar
IN_ATTACK = (1 << 0)
IN_JUMP = (1 << 1)
IN_DUCK = (1 << 2)
IN_FORWARD = (1 << 3)
IN_BACK = (1 << 4)
IN_USE = (1 << 5)
IN_CANCEL = (1 << 6)
IN_LEFT = (1 << 7)
IN_RIGHT = (1 << 8)
IN_MOVELEFT = (1 << 9)
IN_MOVERIGHT = (1 << 10)
IN_ATTACK2 = (1 << 11)
IN_RUN = (1 << 12)
IN_RELOAD = (1 << 13)
IN_ALT1 = (1 << 14)
IN_ALT2 = (1 << 15)
IN_SCORE = (1 << 16)   # Used by client.dll for when scoreboard is held down
IN_SPEED = (1 << 17) # Player is holding the speed key
IN_WALK = (1 << 18) # Player holding walk key
IN_ZOOM = (1 << 19 )# Zoom key for HUD zoom
IN_WEAPON1 = (1 << 20) # weapon defines these bits
IN_WEAPON2 = (1 << 21) # weapon defines these bits
IN_BULLRUSH = (1 << 22)
IN_GRENADE1 = (1 << 23) # grenade 1
IN_GRENADE2 = (1 << 24) # grenade 2
IN_ATTACK3 = (1 << 25)

_healthprop = "CBasePlayer.m_iHealth"
_blockprop = "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup"
_speedprop = "CBasePlayer.localdata.m_flLaggedMovementValue"
_moneyprop = "CCSPlayer.m_iAccount"
_gamename = es.getGameName()
_lastgive = es.ServerVar('eventscripts_lastgive')

allprimary = ("weapon_ak47", "weapon_aug", "weapon_awp", "weapon_famas", "weapon_g3sg1", "weapon_galil", "weapon_m249", "weapon_m3", "weapon_m4a1", "weapon_mac10", "weapon_mp5navy", "weapon_p90", "weapon_scout", "weapon_sg550", "weapon_sg552", "weapon_tmp", "weapon_ump45", "weapon_xm1014")
allsecondary = ("weapon_deagle", "weapon_elite", "weapon_fiveseven", "weapon_glock", "weapon_p228", "weapon_usp")
ammo_list = { "weapon_p228":"009", "weapon_deagle":"001", "weapon_m4a1":"003", "weapon_tmp":"006", "weapon_aug":"002", "weapon_smokegrenade":"013", "weapon_mac10":"008", "weapon_m3":"007", "weapon_ak47":"002", "weapon_m249":"004", "weapon_fiveseven":"010", "weapon_xm1014":"007", "weapon_flashbang":"012", "weapon_glock":"006", "weapon_p90":"010", "weapon_usp":"008", "weapon_ump45":"008", "weapon_awp":"005", "weapon_scout":"002", "weapon_elite":"006", "weapon_c4":None, "weapon_famas":"003", "weapon_galil":"003", "weapon_hegrenade":"011", "weapon_mp5navy":"006", "weapon_knife":None, "weapon_g3sg1":"002", "weapon_sg550":"003", "weapon_sg552":"003", }
allweapons = ("weapon_ak47", "weapon_aug", "weapon_awp", "weapon_c4", "weapon_deagle", "weapon_elite", "weapon_famas", "weapon_fiveseven", "weapon_flashbang", "weapon_g3sg1", "weapon_galil", "weapon_glock", "weapon_hegrenade", "weapon_knife", "weapon_m249", "weapon_m3", "weapon_m4a1", "weapon_mac10", "weapon_mp5navy", "weapon_p228", "weapon_p90", "weapon_scout", "weapon_sg550", "weapon_sg552", "weapon_smokegrenade", "weapon_tmp", "weapon_ump45", "weapon_usp", "weapon_xm1014")
Special_Maps = "cs_office, cs_gentech_final, ze_FFVII_Mako_Reactor_v5_3, ze_LOTR_Mines_of_Moria_v6_3, ba_quartzy, de_nightfever, cs_office_FEAR_night, de_season, ze_FFXII_Westersand_v7_2, ze_TESV_Skyrim_v4fix, ze_predator_ultimate_v3"
Versus_Maps = "cs_office, cs_gentech_final"
ACTIVATE_MSG = "#0,255,255§ 규칙 하나 추가"
Levelup_Sound = "ui/achievement_earned.wav"
WEAPON_BOT = ("[Z Rank] Hiraki", "[Z Rank] Kell", "[Z Rank] Zeisen", "[Z Rank] Crizi", "[Human] Scarecrow", "[S Rank] Bakura Ryo", "[C Rank] Bakura Ryo", "[Human] Zed", "[Human] Shark", "[Human] Ruki", "[Human] Mike", "[Human] Hitter", "[Human] Kaga", "[Human] Let Go", "[Human] Zuru", "[Human] Hori", "[Human] Palm", "[C Rank] Zeisen")
TESTER_LIST = "STEAM_0119861059, STEAM_0020172575, STEAM_0155367723, STEAM_0038622202, STEAM_0021059511, BOT"
MVP_OFFSET = 6328 if spe.platform == 'nt' else 6348
OFFSET_MODEL_NAME = 516 if os.name == 'nt' else 536
S_OFFSET = 345 if os.name == 'nt' else 365
CHANGE_NAME = "[C Rank] Bakura Ryo, [S Rank] Bakura Ryo, [B Rank] Pradoster, [A Rank] Kuria, [C Rank] Zeisen, Watcher"
FEMALE_SKIN = "player/reisen/cirno/cirno, player/konata/idol/idol, player/hhp227/miku/miku, player/konata/zatsunemiku/zatsunemiku"
offsets = {}
# is this work for Macintosh too?
if os.name != "nt":
	for key in offsets:
		offsets[key] += 20

class KeyError(Exception): pass

NIPPER_NORMAL_PLAYER_1 = {
	1: {
		'enabled': 0,
		'pos_1': (2094, 3535, 316),
	},
}

NIPPER_NORMAL_PLAYER_4 = {
	1: {
		'enabled': 0,
		'pos_1': (2094, 3535, 316),
		'pos_2': (1897, 3535, 316),
		'pos_3': (2163, 2800, 316),
		'pos_4': (2016, 2800, 316),
	},
	2: {
		'enabled': 0,
		'pos_1': (-688, 2885, 173),
		'pos_2': (-688, 2739, 173),
		'pos_3': (-688, 2593, 173),
		'pos_4': (-688, 2444, 173),
	},
	3: {
		'enabled': 0,
		'pos_1': (928.143615723, 2193.7512207, 41.2312469482),
		'pos_2': (692.946228027, 2186.74511719, 41.2312469482),
		'pos_3': (650.731933594, 2476.74365234, 51.7956542969),
		'pos_4': (842.720825195, 2476.74365234, 51.7956542969),
	},
	4: {
		'enabled': 0,
		'pos_1': (1698.65600586, 2800.18530273, 312.03125),
		'pos_2': (1551.64660645, 2800.00317383, 312.03125),
		'pos_3': (1360.03125, 2914.1940918, 312.03125),
		'pos_4': (1360.03125, 3063.90893555, 312.03125),
	},
	5: {
		'enabled': 0,
		'pos_1': (249.162017822, 2028.26696777, 32.03125),
		'pos_2': (135.142181396, 1827.29101563, 55.7956542969),
		'pos_3': (-38.7100601196, 1827.25622559, 55.7956542969),
		'pos_4': (-205.745025635, 1885.796875, 24.7965393066),
	},
	6: {
		'enabled': 0,
		'pos_1': (704.4921875, 3632.03125, 198.053253174),
		'pos_2': (655.567199707, 4143.96875, 168.03125),
		'pos_3': (1168.13989258, 4143.81298828, 168.03125),
		'pos_4': (1136.17932129, 3632.03125, 198.053253174),
	},
	7: {
		'enabled': 0,
		'pos_1': (-440.101104736, 2991.96875, 48.6022491455),
		'pos_2': (-359.877929688, 3071.71826172, 48.6022491455),
		'pos_3': (-440.693786621, 3152.03125, 48.6022491455),
		'pos_4': (-520.088500977, 3071.91015625, 48.6022491455),
	},
	8: {
		'enabled': 0,
		'pos_1': (1268.03125, 456.03125, 172.03125),
		'pos_2': (1269.39978027, 576.238464355, 172.03125),
		'pos_3': (1268.14233398, 703.653869629, 172.03125),
		'pos_4': (1268.2869873, 815.96875, 172.03125),
	},
	9: {
		'enabled': 0,
		'pos_1': (1268.03125, 456.03125, 172.03125),
		'pos_2': (1269.39978027, 576.238464355, 172.03125),
		'pos_3': (1268.14233398, 703.653869629, 172.03125),
		'pos_4': (1268.2869873, 815.96875, 172.03125),
	},
	10: {
		'enabled': 0,
		'pos_1': (2156.32495117, 1072.99450684, 336.901824951),
		'pos_2': (2031.31176758, 1072.99450684, 336.901824951),
		'pos_3': (1912.23974609, 1072.99450684, 336.901824951),
		'pos_4': (1792.92236328, 1073.06408691, 336.901824951),
	},
	11: {
		'enabled': 0,
		'pos_1': (2031.4675293, 1936.03125, 143.602249146),
		'pos_2': (1919.96875, 1839.40966797, 143.602249146),
		'pos_3': (2031.72351074, 1743.71289063, 143.602249146),
		'pos_4': (2144.03125, 1838.26733398, 143.602249146),
	},
	12: {
		'enabled': 0,
		'pos_1': (2033.34899902, 1414.93884277, 224.03125),
		'pos_2': (1804.99951172, 1662.07543945, 248.03125),
		'pos_3': (2348.52148438, 1662.18249512, 248.03125),
		'pos_4': (2017.38830566, 1838.66760254, 176.03125),
	},
	13: {
		'enabled': 0,
		'pos_1': (1280.7923584, 2722.00854492, 82.1445922852),
		'pos_2': (1512.38769531, 2726.2109375, 129.03125),
		'pos_3': (1773.64245605, 3124.40844727, 271.668212891),
		'pos_4': (1799.22509766, 3046.91259766, 169.03125),
	},
	14: {
		'enabled': 0,
		'pos_1': (1666.08996582, 2835.21191406, 152.835205078),
		'pos_2': (1443.15283203, 2750.55371094, 124.667556763),
		'pos_3': (1022.21563721, 2842.89672852, 32.03125),
		'pos_4': (849.9453125, 2893.20947266, 32.03125),
	},
	15: {
		'enabled': 0,
		'pos_1': (-408.145050049, 1964.99816895, 16.03125),
		'pos_2': (-20.6005516052, 1914.98059082, 32.03125),
		'pos_3': (592.915039063, 2344.54467773, 217.031570435),
		'pos_4': (934.050415039, 2427.78808594, 203.623535156),
	},
	16: {
		'enabled': 0,
		'pos_1': (-79.4667358398, 1110.63598633, 16.03125),
		'pos_2': (-216.904144287, 757.433837891, 16.03125),
		'pos_3': (-74.4473800659, 334.826141357, 11.830493927),
		'pos_4': (-50.6669235229, 306.883422852, 12.6523370743),
	},
}

NIPPER_NORMAL_PLAYER_5 = {
	1: {
		'enabled': 0,
		'pos_1': (121.280380249, 148.360214233, 16.03125),
		'pos_2': (-364.914916992, 563.004394531, 8.03125),
		'pos_3': (-871.873962402, 1032.90466309, 8.03125),
		'pos_4': (-1115.88598633, 2435.42114258, 16.03125),
		'pos_5': (-1088.64416504, 2147.73999023, 16.03125),
	},
	2: {
		'enabled': 0,
		'pos_1': (1029.67700195, 1702.35205078, 32.03125),
		'pos_2': (1102.35852051, 1685.06591797, 32.03125),
		'pos_3': (851.257995605, 1540.671875, 32.03125),
		'pos_4': (764.111083984, 1247.48474121, 32.03125),
		'pos_5': (311.029296875, 1046.8125, 16.03125),
	},
	3: {
		'enabled': 0,
		'pos_1': (778.339355469, 479.806945801, 16.03125),
		'pos_2': (945.794921875, 1012.97033691, 16.03125),
		'pos_3': (902.175537109, 1571.59155273, 38.9113006592),
		'pos_4': (1059.42565918, 1663.72375488, 32.03125),
		'pos_5': (798.688415527, 1115.25964355, 24.03125),
	},
	4: {
		'enabled': 0,
		'pos_1': (1061.46105957, 2655.77368164, 32.03125),
		'pos_2': (1352.15649414, 2695.31860352, 100.835189819),
		'pos_3': (1663.02209473, 3008.56738281, 169.03125),
		'pos_4': (1849.06530762, 3307.5480957, 169.03125),
		'pos_5': (1679.02490234, 3068.59643555, 169.03125),
	},
	5: {
		'enabled': 0,
		'pos_1': (1648.49523926, 2769.6730957, 136.450500488),
		'pos_2': (1072.86474609, 2724.09765625, 32.03125),
		'pos_3': (1105.49609375, 2231.47412109, 32.03125),
		'pos_4': (732.386901855, 1987.20178223, 32.03125),
		'pos_5': (343.876068115, 2040.24401855, 32.03125),
	},
	6: {
		'enabled': 0,
		'pos_1': (-24.6508865356, 844.042480469, 104.146308899),
		'pos_2': (201.074996948, 529.505065918, 8.03125),
		'pos_3': (-209.114059448, 384.241210938, 16.03125),
		'pos_4': (-619.486328125, 1755.84960938, 16.03125),
		'pos_5': (-1027.69750977, 2118.45458984, 16.03125),
	},
	7: {
		'enabled': 0,
		'pos_1': (861.008972168, 438.515563965, 8.82765197754),
		'pos_2': (841.371887207, 271.336669922, 14.0519924164),
		'pos_3': (935.675354004, 124.414505005, 16.03125),
		'pos_4': (1283.79736328, 135.428329468, 55.6564445496),
		'pos_5': (1297.21801758, 404.277648926, 168.03125),
	},
	8: {
		'enabled': 0,
		'pos_1': (336.001525879, 1065.30310059, 16.03125),
		'pos_2': (495.679077148, 1935.96252441, 32.03125),
		'pos_3': (511.347869873, 2246.74145508, 99.40574646),
		'pos_4': (886.28125, 2480.47094727, 168.03125),
		'pos_5': (1036.80114746, 2173.68017578, 168.03125),
	},
	9: {
		'enabled': 0,
		'pos_1': (1703.99804688, 1378.01708984, 142.03125),
		'pos_2': (1443.61767578, 1650.2722168, 168.03125),
		'pos_3': (1243.5534668, 2017.26757813, 168.03125),
		'pos_4': (1108.50073242, 2326.79248047, 168.03125),
		'pos_5': (578.439025879, 2379.25, 185.535644531),
	},
	10: {
		'enabled': 0,
		'pos_1': (-1009.7756958, 2115.33691406, 16.03125),
		'pos_2': (-271.8800354, 1902.99853516, 16.03125),
		'pos_3': (548.601867676, 2239.34985352, 125.922317505),
		'pos_4': (994.789794922, 2416.43994141, 167.03125),
		'pos_5': (815.819030762, 2076.578125, 32.03125),
	},
}
def nipper_swap():
	for nipper_number in NIPPER_NORMAL_PLAYER_4:
		if random.randint(1,4) == 2: NIPPER_NORMAL_PLAYER_4[nipper_number]['enabled'] = 1
		else: NIPPER_NORMAL_PLAYER_4[nipper_number]['enabled'] = 0
	for nipper_number in NIPPER_NORMAL_PLAYER_5:
		if random.randint(1,4) == 2: NIPPER_NORMAL_PLAYER_5[nipper_number]['enabled'] = 1
		else: NIPPER_NORMAL_PLAYER_5[nipper_number]['enabled'] = 0

def zzzz(): es.set("nipper_print_pos", 0)

def print_nipper_location():
	nipper_print_pos = int(sv('nipper_print_pos')) + 1
	es.set("nipper_print_pos", nipper_print_pos)
	userid = es.getUseridList()[0]
	x,y,z = es.getplayerlocation(userid)
	es.msg("		'pos_%s': (%s, %s, %s)," %(nipper_print_pos, x,y,z))

def break_door():
	playsound("doors/latchlocked2.wav")
	gamethread.delayed(1, est.play, ("#h", "doors/latchlocked2.wav"))
	gamethread.delayed(2, est.play, ("#h", "doors/latchlocked2.wav"))
	gamethread.delayed(3, est.play, ("#h", "doors/latchlocked2.wav"))
	gamethread.delayed(4, est.play, ("#h", "doors/latchlocked2.wav"))
	gamethread.delayed(5, est.play, ("#h", "doors/latchlocked2.wav"))
	gamethread.delayed(8, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(10, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(12, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(15, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(18, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(19, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(20, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(21, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(22, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(22.8, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(23, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(23.3, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(24, est.play, ("#h", "doors/heavy_metal_stop1.wav"))
	gamethread.delayed(30, est.play, ("#h", "doors/latchunlocked1.wav"))
	gamethread.delayed(30, est.play, ("#h", "doors/latchunlocked1.wav"))
	gamethread.delayed(30, est.play, ("#h", "doors/latchunlocked1.wav"))
	gamethread.delayed(30, est.play, ("#h", "doors/latchunlocked1.wav"))
	gamethread.delayed(34, est.play, ("#h", "zeisenproject_3/autosounds/footstep.mp3"))
def connection_test():
   	es.set("connect_ok", 1)
	try: 
		serverConnected = serverlib.SourceServer('218.54.46.83', 27019) 
		es.msg(serverConnected)
		serverDetails = serverConnected.getDetails()
		serverConnected.disconnect() 
	except: 
 		es.msg("Connect Failed")
   		es.set("connect_ok", 0)

def patch_msg():
	esc.msg("#0,255,255[Patch Information] BOT Remote Control")

def make_dark():
	es.lightstyle(0, 'b')
	ent = es.createentity("light_dynamic")
	es.entitysetvalue(ent, "brightness", 1)
	es.entitysetvalue(ent, "style", 1)
	es.entitysetvalue(ent, "distance", 9999.0)
	es.entitysetvalue(ent, "spotlight_radius", 9999.0)
	es.spawnentity(ent)
	es.set("what_ent", ent)
	est.setentitycolor(ent, 0, 0, 0, 255)
	es.server.cmd('es_xload gg_ffa_bots')
	playsound("zeisenproject_3/nippersounds/nmhm_houl.wav")

def nipper_start():
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.set("nightfever_time", 9999)
	gamethread.delayed(0.5, est.play, ("#h", "zeisenproject_3/nippersounds/nmhm_load.wav"))
	gamethread.delayed(15, es.set, ("allfade", 1))
	gamethread.delayed(20.5, nipper_begin, ())
	es.server.cmd('bot_chatter off')
	npc_check = es.createentityindexlist('')
	for a in npc_check:
		classname = es.entitygetvalue(a, 'classname')
		if "npc_" in classname: es.remove(classname)

def nipper_begin():
	es.forcevalue("bot_quota", 0)
	es.set("allfade", 0)
	est.stopsound("#h", "zeisenproject_3/nippersounds/nmhm_load.wav")
	playsound("zeisenproject_3/nippersounds/nmh_welcome.wav")
	gamethread.delayed(7.5, npc_msg, ("#125,125,125Nipper", "There's no turning back now."))
	gamethread.delayed(7.5, est.play, ("#h", "zeisenproject_3/nippersounds/nmh_noturningback.wav"))
	gamethread.delayed(7.5, es.server.cmd, ('sv_password nipperz'))
	for a in playerlib.getPlayerList("#human"):
		if int(es.getplayerteam(a.userid)) <= 1:
			if getplayerzeisenid(a.userid) != "STEAM_0021059511":
				if es.getplayername(a.userid) != "Watcher":
					es.server.cmd('kickid %s "Nipper"' %(a.userid))
		usermsg.centermsg(a.userid, "Welcome, Foolish Mortals to The Haunted Mansion.")
		gamethread.delayed(1, usermsg.centermsg, (a.userid, "Welcome, Foolish Mortals to The Haunted Mansion."))
		gamethread.delayed(2, usermsg.centermsg, (a.userid, "Welcome, Foolish Mortals to The Haunted Mansion."))
		gamethread.delayed(3, usermsg.centermsg, (a.userid, "Welcome, Foolish Mortals to The Haunted Mansion."))
	es.remove("weapon_c4")
	es.remove("weapon_c4")
	es.remove("weapon_c4")
	es.remove("weapon_c4")
	es.remove("weapon_c4")

def test424():
	userid = 17
        spe.setLocVal('i', spe.getPlayer(userid) + 365, 3) 

def issac_start():
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/autosounds/issac_start.mp3", 1.0)
		gamethread.delayed(1.79, usermsg.hudhint, (a.userid, "Isaac and his mother lived alone in a small house on a hill.\n아이작과 그의 엄마는 언덕 위의 작은 집에서 살았습니다."))
		gamethread.delayed(7.31, usermsg.hudhint, (a.userid, "Isaac kept to himself drawing pictures and playing with his toys\n아이작은 혼자 그림을 그리거나 장난감을 가지고 놀고있었습니다."))
		gamethread.delayed(11.71, usermsg.hudhint, (a.userid, "as his mom watched Christian broadcasts on the television.\n그의 엄마가 기독교 방송을 보는 동안에 말이죠."))
		gamethread.delayed(16.38, usermsg.hudhint, (a.userid, "Life was simple and they were both happy.\n삶은 단순했고, 그들 둘 다 행복했습니다."))
		gamethread.delayed(20.73, usermsg.hudhint, (a.userid, "That was until the day Isaac's mom heard a voice from above.\n아이작의 엄마가 하늘의 목소리를 듣기 전까지 말이죠."))
		gamethread.delayed(27.22, usermsg.hudhint, (a.userid, "“Your son has become corrupted by sin. He needs to be saved.”\n“너의 아들은 죄로 인해 타락했다. 그는 구원을 받아야한다.”"))
		gamethread.delayed(34.14, usermsg.hudhint, (a.userid, "“I will do my best to save him, my Lord,”\n“그를 구원하기 위해 최선을 다하겠습니다, 주님.”"))
		gamethread.delayed(37.20, usermsg.hudhint, (a.userid, "Isaac's mother replied,\n아이작의 엄마는 대답했고,"))
		gamethread.delayed(38.99, usermsg.hudhint, (a.userid, "rushing into Isaac's room, removing all that was evil from his life.\n아이작의 방으로 급히 간 다음 그의 삶으로부터 악한 것들을 제거했습니다."))
		gamethread.delayed(45.01, usermsg.hudhint, (a.userid, "Again the voice called to her.\n또 다시 목소리가 그녀에게 큰 목소리로 말했습니다."))
		gamethread.delayed(47.79, usermsg.hudhint, (a.userid, "“Isaac's soul is still corrupt.\n“아이작의 영혼은 아직 타락하다."))
		gamethread.delayed(50.23, usermsg.hudhint, (a.userid, "He needs to be cut off from all that is evil in this world\n그는 이 세계의 모든 악에서 고립되어야하고"))
		gamethread.delayed(54.04, usermsg.hudhint, (a.userid, "and confess his sins.”\n그의 죄악을 자백해야 한다.”"))
		gamethread.delayed(57.03, usermsg.hudhint, (a.userid, "“I will follow your instructions, Lord. I have faith in thee,”\n“당신의 지시에 따르겠습니다, 주님. 당신을 믿습니다,”"))
		gamethread.delayed(61.35, usermsg.hudhint, (a.userid, "Isaac's mother replied\n아이작의 엄마는 대답했습니다."))
		gamethread.delayed(63.05, usermsg.hudhint, (a.userid, "as she locked Isaac in his room away from the evils of the world.\n아이작을 세상의 악에서 떨어진 그의 방에 가두면서요."))
		gamethread.delayed(69.13, usermsg.hudhint, (a.userid, "One last time Isaac's mom heard the voice of God calling to her.\n마지막으로 아이작의 엄마는 신이 그녀를 부르는 것을 들었습니다."))
		gamethread.delayed(74.81, usermsg.hudhint, (a.userid, "“You've done as I've asked, but I still question your devotion to me.\n“넌 내가 말한대로 잘 했지만, 너의 헌신에 대해 의심이 된다."))
		gamethread.delayed(79.72, usermsg.hudhint, (a.userid, "To prove your faith, I will ask one more thing of you.”\n너의 믿음을 입증하기 위해, 나는 너에게 한 가지 더 시키겠다.”"))
		gamethread.delayed(84.68, usermsg.hudhint, (a.userid, "“Yes, Lord. Anything,”\n“네, 주님. 무엇이든지요.”"))
		gamethread.delayed(86.35, usermsg.hudhint, (a.userid, "Isaac's mother begged.\n아이작의 엄마가 간청했습니다."))
		gamethread.delayed(88.41, usermsg.hudhint, (a.userid, "“To prove your love and devotion, I require a sacrifice.\n“너의 사랑과 헌신을 입증하기 위해, 희생이 필요하다."))
		gamethread.delayed(93.08, usermsg.hudhint, (a.userid, "Your son, Isaac, will be this sacrifice.\n너의 아들, 아이작이 희생물이 될 것이다."))
		gamethread.delayed(97.10, usermsg.hudhint, (a.userid, "Go into his room and end his life as an offering to me,\n그의 방에 들어가 내가 말한 대로 그의 삶을 끝내라,"))
		gamethread.delayed(101.37, usermsg.hudhint, (a.userid, "to prove you love me above all else.”\n너가 특히 날 사랑한다는 걸 입증하려면 말이다.”"))
		gamethread.delayed(106.52, usermsg.hudhint, (a.userid, "“Yes, Lord,” she replied, grabbing a butchers knife from the kitchen.\n“네, 주님.” 주방에서 식칼을 꺼내들고 그녀가 답변했습니다."))
		gamethread.delayed(112.95, usermsg.hudhint, (a.userid, "Isaac, watching through a crack in his door, trembled in fear.\n아이작은 그의 문에 있는 틈을 통해 보고 있었고, 공포에 휩싸여 있었습니다."))
		gamethread.delayed(118.78, usermsg.hudhint, (a.userid, "Scrambling around his room to find a hiding place,\n숨을 곳을 찾기 위해 허겁지겁 돌아다니다,"))
		gamethread.delayed(122.59, usermsg.hudhint, (a.userid, "he noticed a trapdoor to the basement hidden under his rug.\n그는 지하실로 가는 바닥의 문이 양탄자 밑에 숨겨져 있는 걸 발견했습니다."))
		gamethread.delayed(127.45, usermsg.hudhint, (a.userid, "Without hesitation,\n망설임 없이,"))
		gamethread.delayed(129, usermsg.hudhint, (a.userid, "he flung open the hatch just as his mother burst through his door\n그의 엄마가 문을 불쑥 열었을 때 출입문을 열고"))
		gamethread.delayed(134.12, usermsg.hudhint, (a.userid, "and threw himself down into the unknown depths below...\n밑의 깊은 미지의 공간으로 자신을 내던졌습니다..."))

def issac_end():
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/autosounds/issac_end.mp3", 1.0)
		steamid = getplayerzeisenid(a.userid)
		username = es.getplayername(a.userid)
		keymath(steamid, "player_data", "item27", "+", 1)
		esc.msg("#blue %s 유저#255,255,255님이 이삭의 구속을 클리어하여 #255,255,255성경 책 아이템 1개#255,255,255를 받았습니다." %(username))
		gamethread.delayed(0.01, usermsg.hudhint, (a.userid, "Isaac was cornered.\n아이작은 구석으로 몰렸습니다."))
		gamethread.delayed(2.17, usermsg.hudhint, (a.userid, "His mother, fueled with the desire to serve her god,,was bearing down on Isaac.\n엄마는 신에게 봉사할 욕망으로 들떠있는채, 아이작에게 다가가고 있었습니다."))
		gamethread.delayed(9.6, usermsg.hudhint, (a.userid, "“I will do as I'm told, my Lord! I will love you above all else.”\n“신이시여, 제가 들은 것을 그대로 행하겠나이다! 당신을 무엇보다도 사랑할 겁니다.”"))
		gamethread.delayed(14.35, usermsg.hudhint, (a.userid, "Isaac's mother repeated it to herself.\n아이작의 엄마는 계속 중얼거렸습니다."))
		gamethread.delayed(17.08, usermsg.hudhint, (a.userid, "This was the end of the life for Isaac.\n이것이 아이작 생의 최후였습니다."))
		gamethread.delayed(20.65, usermsg.hudhint, (a.userid, "His mother was far too strong for him.\n그의 엄마는 아이작에 비해 너무나 강했습니다."))
		gamethread.delayed(23.82, usermsg.hudhint, (a.userid, "But just he accepted his fate,\n하지만 아이작이 자신의 운명을 받아들인 순간,"))
		gamethread.delayed(26.73, usermsg.hudhint, (a.userid, "God intervened sending an angel down from a verbe to stop his mother's hand.\n신이 그의 엄마를 막기 위해 성경을 통해서 천사를 내려보냈습니다."))
		gamethread.delayed(33.24, usermsg.hudhint, (a.userid, "And just like that, It was over.\n그리고 그렇게, 갑작스럽게 끝이 났습니다."))

def nipper_ex_1():
	npc_msg("#125,125,255Chain", "니퍼, 넌 여기서 뭘 하는거지?")
	gamethread.delayed(4, npc_msg, ("#125,125,125Chain", "너의 과거를 되찾아라. 너의 지금은 초심을 잃어버렸어."))
	gamethread.delayed(8, npc_msg, ("#125,125,125Chain", "자. #0,255,255이 걸 #default받아."))
	nipper_setting("zeisenproject_3/autosounds/nipper_ex.mp3", 845)

def nipper_hardcore_1():
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_madam.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_madam.wav", 1.0)
	gamethread.delayed(13, nipper_setting, ("zeisenproject_3/autosounds/nipper_hardcore.mp3", 261))

def nipper_start_1():
	nipper_swap()
	es.set("nipper_difficulty", "normal")
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_voice1.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_voice1.wav", 1.0)
	gamethread.delayed(16, nipper_setting, ("zeisenproject_3/nippersounds/nmhm_graveyard2.wav", 400))
	npc_msg("#125,125,125Nipper", "Our library is well-stocked with priceless first editions. Only ghost stories, of course. And marble busts of the greatest ghost writers the literary world has ever known.")

def nipper_start_2():
	nipper_swap()
	es.set("nipper_difficulty", "normal")
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_voice2.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_voice2.wav", 1.0)
	gamethread.delayed(12, nipper_setting, ("zeisenproject_3/nippersounds/nmhm_graveyard1.wav", 350))
	npc_msg("#125,125,125Nipper", "we have 999 happy haunts here, but there's room for a thousand. Any volunteers?")

def nipper_start_3():
	nipper_swap()
	es.set("nipper_difficulty", "normal")
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_svoice1.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_svoice1.wav", 1.0)
	gamethread.delayed(12, nipper_setting, ("zeisenproject_3/nippersounds/nmhm_foyer.wav", 300))
	npc_msg("#125,125,125Nipper", "Our tour begins here in this gallery where you see paintings of some of our guests as they appeared in their corruptible, mortal state.")

def nipper_start_4():
	nipper_swap()
	es.set("nipper_difficulty", "normal")
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_svoice2.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_svoice2.wav", 1.0)
	gamethread.delayed(9, nipper_setting, ("zeisenproject_3/nippersounds/nmhm_piano.wav", 200))
	npc_msg("#125,125,125Nipper", "Is this haunted room actually stretching? Or is it your imagination.")

def nipper_start_5():
	nipper_swap()
	es.set("nipper_difficulty", "normal")
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_svoice3.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_svoice3.wav", 1.0)
	gamethread.delayed(29, nipper_setting, ("zeisenproject_3/nippersounds/nmhm_ballroom.wav", 150))
	npc_msg("#125,125,125Nipper", "And consider this dismaying observation: This chamber has no windows and no doors, which offers you this chilling challenge: to find a way out! Of course, there's always my way.")

def nipper_start_sa2000():
	gamethread.delayed(1, nipper_setting, ("zeisenproject_3/nippersounds/sa2000.mp3", 114))

def nipper_start_super():
	gamethread.delayed(1, nipper_setting, ("zeisenproject_3/autosounds/super.mp3", 159))

def nipper_start_bw():
	nipper_setting("zeisenproject_3/autosounds/clh.mp3", 370)

def nipper_start_ta2000():
	nipper_setting("zeisenproject_3/autosounds/ta2000.mp3", 148)
	es.load("story")
	es.doblock("story/nipper_custom_4")

def nipper_start_6():
	nipper_swap()
	es.set("nipper_difficulty", "normal")
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_voice3.wav", 1.0)
		es.playsound(a.userid, "zeisenproject_3/nippersounds/nmhm_voice3.wav", 1.0)
	gamethread.delayed(15, nipper_setting, ("zeisenproject_3/nippersounds/nmhm_load.wav", 100))
	npc_msg("#125,125,125Nipper", "Ah, there you are, and just in time! There's a little matter I forgot to mention. Beware of hitchhiking ghosts!")

def nipper_setting(music, max_time):
	playsound(music)
	es.set("nipper_maxtime", max_time)
	nipper_timer.start(1, 9999)

def record_note():
	for a in playerlib.getPlayerList("#human"):
		es.playsound(a.userid, "zeisenproject_3/autosounds/man/page.mp3", 1.0)
		guncheck = est.getgun(a.userid)
		if "awp" in guncheck:
			esc.tell(a.userid, "#255,255,255＊ 노트를 기록했다.")
			steamid = getplayerzeisenid(a.userid)
			keymath(steamid, "player_data", "item30", "+", 1)

def recording():
	for a in playerlib.getPlayerList("#human"):
		guncheck = est.getgun(a.userid)
		if "awp" in guncheck:
			es.cexec(a.userid, "r_screenoverlay effects/combine_binocoverlay.vmt")
			usermsg.centermsg(a.userid, "▶ Recording...")
			awp_index = est.getweaponindex(a.userid, "weapon_awp")
			es.setindexprop(awp_index, "CWeaponAWP.baseclass.baseclass.baseclass.LocalWeaponData.m_iPrimaryAmmoType", -1)
		else:
			es.cexec(a.userid, "r_screenoverlay 0")

def nipper_timer():
	nipper_maxtime = svmath("nipper_maxtime", "-", 1)
	for a in playerlib.getPlayerList("#human"):
		usermsg.hudhint(a.userid, "Failed. %s Seconds Left." %(nipper_maxtime))
	if nipper_maxtime == 0:
		nipper_timer.stop()
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("play .")
		es.cexec_all("r_screenoverlay debug/yuv.vmt")
		gamethread.delayed(0.5, est.play, ("#h", "zeisenproject_3/nippersounds/nmhm_exitlaugh.wav"))
		gamethread.delayed(8, es.server.cmd, ("killserver"))
	if nipper_maxtime <= 0:
		es.cexec_all("r_screenoverlay debug/yuv.vmt")
	if str(sv('sv_password')) == "nipperz":
		if int(sv('nipper_maxtime')) > 0:
			get_nipper_count = 0
			for userid in es.getUseridList():
				if es.getplayerteam(userid) == 2:
					get_nipper_count += 1
			if get_nipper_count == 1:
				if str(sv('nipper_difficulty')) == "normal":
					NIPPER_GROUP = NIPPER_NORMAL_PLAYER_1
					for nipper_number in NIPPER_GROUP:
						if NIPPER_GROUP[nipper_number]['enabled'] == 1:
							es.set("nipper_pos_1", 0)
							es.set("nipper_pos_2", 0)
							es.set("nipper_pos_3", 0)
							es.set("nipper_pos_4", 0)
							for userid in es.getUseridList():
								x,y,z = es.getplayerlocation(userid)
								pos_count = 1
								completed = 0
								while pos_count <= get_nipper_count:
									if completed == 0:
										if z_nearcoord_another(x, y, z, NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][0], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][1], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][2], 0.5) == 1:
											es.set("nipper_pos_%s" %(pos_count), 1)
											completed = 1
									pos_count += 1
							complete_count = 1
							complete_users = 0
							while complete_count <= get_nipper_count:
								if sv('nipper_pos_%s' %(complete_count)) == 1:
									complete_users += 1
								complete_count += 1
							if (complete_count - 1) == complete_users:
								nipper_clear()
								break
			if get_nipper_count == 4:
				if str(sv('nipper_difficulty')) == "normal":
					NIPPER_GROUP = NIPPER_NORMAL_PLAYER_4
					for nipper_number in NIPPER_GROUP:
						if NIPPER_GROUP[nipper_number]['enabled'] == 1:
							es.set("nipper_pos_1", 0)
							es.set("nipper_pos_2", 0)
							es.set("nipper_pos_3", 0)
							es.set("nipper_pos_4", 0)
							for userid in es.getUseridList():
								x,y,z = es.getplayerlocation(userid)
								pos_count = 1
								completed = 0
								while pos_count <= get_nipper_count:
									if completed == 0:
										if z_nearcoord_another(x, y, z, NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][0], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][1], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][2], 0.5) == 1:
											es.set("nipper_pos_%s" %(pos_count), 1)
											completed = 1
									pos_count += 1
							complete_count = 1
							complete_users = 0
							while complete_count <= get_nipper_count:
								if sv('nipper_pos_%s' %(complete_count)) == 1:
									complete_users += 1
								complete_count += 1
							if (complete_count - 1) == complete_users:
								nipper_clear()
								break
			if get_nipper_count == 5:
				if str(sv('nipper_difficulty')) == "normal":
					NIPPER_GROUP = NIPPER_NORMAL_PLAYER_5
					for nipper_number in NIPPER_GROUP:
						if NIPPER_GROUP[nipper_number]['enabled'] == 1:
							es.set("nipper_pos_1", 0)
							es.set("nipper_pos_2", 0)
							es.set("nipper_pos_3", 0)
							es.set("nipper_pos_4", 0)
							es.set("nipper_pos_5", 0)
							for userid in es.getUseridList():
								x,y,z = es.getplayerlocation(userid)
								pos_count = 1
								completed = 0
								while pos_count <= get_nipper_count:
									if completed == 0:
										if z_nearcoord_another(x, y, z, NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][0], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][1], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][2], 0.5) == 1:
											es.set("nipper_pos_%s" %(pos_count), 1)
											completed = 1
									pos_count += 1
							complete_count = 1
							complete_users = 0
							while complete_count <= get_nipper_count:
								if sv('nipper_pos_%s' %(complete_count)) == 1:
									complete_users += 1
								complete_count += 1
							if (complete_count - 1) == complete_users:
								nipper_clear()
								break
			if get_nipper_count == 6:
				if str(sv('nipper_difficulty')) == "normal":
					NIPPER_GROUP = NIPPER_NORMAL_PLAYER_5
					for nipper_number in NIPPER_GROUP:
						if NIPPER_GROUP[nipper_number]['enabled'] == 1:
							es.set("nipper_pos_1", 0)
							es.set("nipper_pos_2", 0)
							es.set("nipper_pos_3", 0)
							es.set("nipper_pos_4", 0)
							es.set("nipper_pos_5", 0)
							es.set("nipper_pos_6", 0)
							for userid in es.getUseridList():
								x,y,z = es.getplayerlocation(userid)
								pos_count = 1
								completed = 0
								while pos_count <= get_nipper_count:
									if completed == 0:
										if z_nearcoord_another(x, y, z, NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][0], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][1], NIPPER_GROUP[nipper_number]['pos_%s' %(pos_count)][2], 0.5) == 1:
											es.set("nipper_pos_%s" %(pos_count), 1)
											completed = 1
									pos_count += 1
							complete_count = 1
							complete_users = 0
							while complete_count <= get_nipper_count:
								if sv('nipper_pos_%s' %(complete_count)) == 1:
									complete_users += 1
								complete_count += 1
							if (complete_count - 1) == complete_users:
								nipper_clear()
								break

def clear_zee():
	for a in playerlib.getPlayerList("#human"):
		steamid = getplayerzeisenid(a.userid)
		username = es.getplayername(a.userid)
		if random.randint(1,5) == 3:
			keymath(steamid, "player_data", "item7", "+", 1)
			esc.msg("#blue %s 유저#255,255,255님이 이벤트 맵을 클리어하여 #255,255,25황혼의 마도서 아이템 1개#255,255,255를 받았습니다." %(username))
		else:
			if random.randint(1,3) == 3:
				keymath(steamid, "player_data", "item8", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 이벤트 맵을 클리어하여 #255,255,25닌자의 마도서 아이템 1개#255,255,255를 받았습니다." %(username))
			else:
				keymath(steamid, "player_data", "item9", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 이벤트 맵을 클리어하여 #255,255,25유혹의 마도서 아이템 1개#255,255,255를 받았습니다." %(username))

def clear_ze():
	for a in playerlib.getPlayerList("#human"):
		steamid = getplayerzeisenid(a.userid)
		username = es.getplayername(a.userid)
		if random.randint(1,20) != 7:
			keymath(steamid, "player_data", "item25", "+", 1)
			esc.msg("#blue %s 유저#255,255,255님이 이벤트 맵을 클리어하여 #255,255,255천사의 날개 아이템 1개#255,255,255를 받았습니다." %(username))
		else:
			keymath(steamid, "player_data", "item15", "+", 1)
			esc.msg("#blue %s 유저#255,255,255님이 이벤트 맵을 클리어하여 #255,0,0스칼렛의 날개 아이템 1개#255,255,255를 받았습니다." %(username))

def gunner_story():
	npc_msg("#255,0,0???", "5년 전, 난 눈 깜짝할 사이에 눈앞에서 3만명의 병력을 잃었다. 세상은 빌어먹게도 구경만 하고 있었지.")
	est.play("#h", "zeisenproject_3/autosounds/final_1.wav")
	gamethread.delayed(11.5, npc_msg, ("#255,0,0???", "이제는 더 이상 지원자나 애국자가 필요할 일은 없을거다."))
	gamethread.delayed(11.5, est.play, ("#h", "zeisenproject_3/autosounds/final_1_2.wav"))
	gamethread.delayed(19.5, npc_msg, ("#255,0,0???", "이해했을거라 믿는다."))
	gamethread.delayed(19.5, est.play, ("#h", "zeisenproject_3/autosounds/final_1_3.wav"))
	gamethread.delayed(22.5, est.play, ("#h", "weapons/deagle/deagle-1.wav"))

def nipper_clear():
	es.set("nipper_maxtime", 0)
	nipper_timer.stop()
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	for a in playerlib.getPlayerList("#human"):
		gamethread.delayed(0.25, est.play, (a.userid, "zeisenproject_3/nippersounds/nmh_laugh.wav"))
		if est.isalive(a.userid) == 1:
			steamid = getplayerzeisenid(a.userid)
			username = es.getplayername(a.userid)
			if random.randint(1,10) != 7:
				keymath(steamid, "player_data", "item1", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 니퍼의 시련을 클리어하여 #55,255,255크리스탈 아이템 1개#255,255,255를 받았습니다." %(username))
			else:
				keymath(steamid, "player_data", "item2", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 니퍼의 시련을 클리어하여 #125,255,255파란색 버섯 아이템 1개#255,255,255를 받았습니다." %(username))
def burnman_clear():
	nipper_timer.stop()
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	for a in playerlib.getPlayerList("#human,#alive"):
		est.play(a.userid, "zeisenproject_3/nippersounds/nmh_laugh.wav")
		steamid = getplayerzeisenid(a.userid)
		username = es.getplayername(a.userid)
		keymath(steamid, "player_data", "xp", "+", 10000)
		esc.msg("#blue %s 유저#255,255,255님이 니퍼의 시련을 클리어하여 #55,255,255경험치 10000#255,255,255을 받았습니다." %(username))

def nipper_ex_clear():
	nipper_timer.stop()
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	for a in playerlib.getPlayerList("#human,#alive"):
		est.play(a.userid, "zeisenproject_3/nippersounds/nmh_laugh.wav")
		steamid = getplayerzeisenid(a.userid)
		username = es.getplayername(a.userid)
		if random.randint(1,100) != 7:
			keymath(steamid, "player_data", "item1", "+", 5)
			esc.msg("#blue %s 유저#255,255,255님이 EX 니퍼의 시련을 클리어하여 #55,255,255크리스탈 아이템 5개#255,255,255를 받았습니다." %(username))
		else:
			keymath(steamid, "player_data", "item19", "+", 1)
			esc.msg("#blue %s 유저#255,255,255님이 EX 니퍼의 시련을 클리어하여 #0,0,0암흑 크리스탈 1개#255,255,255를 받았습니다." %(username))

def nipper_hardcore_clear():
	nipper_timer.stop()
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	es.cexec_all("play .")
	for a in playerlib.getPlayerList("#human,#alive"):
		est.play(a.userid, "zeisenproject_3/nippersounds/nmh_laugh.wav")
		steamid = getplayerzeisenid(a.userid)
		username = es.getplayername(a.userid)
		if random.randint(1,100) != 7:
			keymath(steamid, "player_data", "item23", "+", 1)
			esc.msg("#blue %s 유저#255,255,255님이 Hardcore 니퍼의 시련을 클리어하여 #125,125,125수수께끼의 마도서 아이템 1개#255,255,255를 받았습니다." %(username))
		else:
			keymath(steamid, "player_data", "item15", "+", 1)
			esc.msg("#blue %s 유저#255,255,255님이 Hardcore 니퍼의 시련을 클리어하여 #255,0,0스칼렛의 날게 1개#255,255,255를 받았습니다." %(username))

def find_c4():
	userid = 3
	x,y,z = es.getplayerlocation(userid)
	esc.msg("'%s,%s,%s'" %(x,y,z))
	c4_index = es.createentity("weapon_c4")
	es.entitysetvalue(c4_index, 'spawnflags', 1)
	est.entteleport(c4_index, x, y, z)
	es.spawnentity(c4_index)

def waterman_escape():
	npc_msg("#255,255,255Dunn", "그는 죽일수 있는 상대가 아니였다. 우리를 찾고 우리에게 다가올 뿐이다. ")
	gamethread.delayed(5, npc_msg, ("#255,255,255Dunn", "코어들이 말하는것들은 나에게 큰 도움이 되었다."))
	gamethread.delayed(10, npc_msg, ("#255,255,255Dunn", "덕분에 죄책감이 심하게 #125,125,125들었지만... #default살고싶다면, #0,0,255도망쳐라."))
	gamethread.delayed(15, npc_msg, ("#255,255,255Dunn", "술래잡기 게임이다. 들키면 곧바로 죽는다."))
	gamethread.delayed(20, es.server.cmd, ('bot_add_t "[Z Rank] Waterman"'))
	gamethread.delayed(20, create_c4, ())
	es.server.cmd('repeat create a "es_xdoblock rpg/man_start"')
	es.server.cmd('es_xdelayed 20 es_xdoblock rpg/man_start')
	es.server.cmd('es_xdelayed 20 repeat start a 120')
	es.set("core_count", 0)
	es.set("last_c4_origin", "0")
	es.load("wS_Hide_Radar")

def burnman_escape():
	npc_msg("#255,255,255Dunn", "그는 죽일수 있는 상대가 아니였다. 우리를 찾고 우리에게 다가올 뿐이다. ")
	gamethread.delayed(5, npc_msg, ("#255,255,255Dunn", "코어들이 말하는것들은 나에게 큰 도움이 되었다."))
	gamethread.delayed(10, npc_msg, ("#255,255,255Dunn", "덕분에 죄책감이 심하게 #125,125,125들었지만... #default살고싶다면, #255,0,0도망쳐라."))
	gamethread.delayed(15, npc_msg, ("#255,255,255Dunn", "술래잡기 게임이다. 들키면 곧바로 죽는다."))
	gamethread.delayed(20, es.server.cmd, ('bot_add_t "[Z Rank] Burnman"'))
	gamethread.delayed(20, create_c4, ())
	es.server.cmd('repeat create a "es_xdoblock rpg/man_start"')
	es.server.cmd('es_xdelayed 20 es_xdoblock rpg/man_start')
	es.server.cmd('es_xdelayed 20 repeat start a 120')
	es.set("core_count", 0)
	es.set("last_c4_origin", "0")
	es.load("wS_Hide_Radar")


ban_list = ["STEAM_0144184484",
"STEAM_0042167221",
"STEAM_0044191419",
"STEAM_0139569533",
"STEAM_0044059534",
"STEAM_0130570276",
"STEAM_0155725542",
"STEAM_0181553217",
"STEAM_0127683432",
"STEAM_0058782787",
"STEAM_0158772539",
"STEAM_0051300917",
"STEAM_0165916253"]


def create_c4():
	last_c4_origin = str(sv('last_c4_origin'))
	location_list = ['1360.03125,2800.03125,312.03125',
	'496.411804199,2269.16235352,32.03125',
	'702.832580566,975.96875,176.03125',
	'-1127.96875,1523.37915039,32.03125',
	'-180.416854858,1127.96875,168.03125',
	'1188.08752441,2766.86621094,189.422393799',
	'1231.96875,4098.01220703,252.552246094',
	'431.96875,3728.03125,168.03125',
	'-672.03125,2208.03125,168.03125',
	'-817.994628906,867.78137207,220.03125',
	'619.85748291,-871.044555664,186.690994263',
	'-437.183746338,2821.33691406,285.366546631',
	'-1263.97631836,2800.91308594,169.617858887',
	'191.882446289,639.095275879,221.702972412']
	if last_c4_origin != "0": location_list.remove(last_c4_origin)
	choice_origin = random.choice(location_list)
	es.set("last_c4_origin", choice_origin)
	check_origin = choice_origin.split(",")
	c4_index = es.createentity("weapon_c4")
	es.entitysetvalue(c4_index, 'spawnflags', 1)
	est.entteleport(c4_index, check_origin[0], check_origin[1], check_origin[2])
	est.setentitycolor(c4_index, 255, 254, 254, 255)
	es.spawnentity(c4_index)

def keyboard_sound():
	for b in playerlib.getPlayerList("#human"):
		soundf = "ambient/machines/keyboard_fast%s_1second.wav" %(random.randint(1,3))
		es.playsound(b.userid, soundf, 1.0)

def story_start_2():
	keyboard_repeat = repeat.create('keyboard_sound', keyboard_sound, ())
	es.doblock("rpg/keyboard_sound")
	keyboard_repeat.start(1, 8)
	for a in playerlib.getPlayerList("#human"):
		usermsg.centermsg(a.userid, "모 ")
		gamethread.delayed(0.25, usermsg.centermsg, (a.userid, "모르 "))
		gamethread.delayed(0.5, usermsg.centermsg, (a.userid, "모르는 "))
		gamethread.delayed(0.75, usermsg.centermsg, (a.userid, "모르는 것"))
		gamethread.delayed(1, usermsg.centermsg, (a.userid, "모르는 것만"))
		gamethread.delayed(1.25, usermsg.centermsg, (a.userid, "모르는 것만이"))
		gamethread.delayed(1.5, usermsg.centermsg, (a.userid, "모르는 것만이 인"))
		gamethread.delayed(1.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간"))
		gamethread.delayed(2, usermsg.centermsg, (a.userid, "모르는 것만이 인간을"))
		gamethread.delayed(2.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두"))
		gamethread.delayed(2.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵"))
		gamethread.delayed(2.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게"))
		gamethread.delayed(3, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한"))
		gamethread.delayed(3.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단"))
		gamethread.delayed(3.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한"))
		gamethread.delayed(3.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번"))
		gamethread.delayed(4, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이"))
		gamethread.delayed(4.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라"))
		gamethread.delayed(4.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도"))
		gamethread.delayed(4.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인"))
		gamethread.delayed(5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간"))
		gamethread.delayed(5.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이"))
		gamethread.delayed(5.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그"))
		gamethread.delayed(5.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것"))
		gamethread.delayed(6, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에"))
		gamethread.delayed(6.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞"))
		gamethread.delayed(6.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서"))
		gamethread.delayed(6.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아"))
		gamethread.delayed(7, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는"))
		gamethread.delayed(7.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것"))
		gamethread.delayed(7.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이"))
		gamethread.delayed(7.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이 되"))
		gamethread.delayed(8, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이 되기"))
		gamethread.delayed(8.25, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이 되기 전"))
		gamethread.delayed(8.5, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이 되기 전까"))
		gamethread.delayed(8.75, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이 되기 전까지"))
		gamethread.delayed(9, usermsg.centermsg, (a.userid, "모르는 것만이 인간을 두렵게 한다.\n 단 한번이라도 인간이 그것에 맞서 아는 것이 되기 전까지는."))

def story_start_1():
	keyboard_repeat = repeat.create('keyboard_sound', keyboard_sound, ())
	es.doblock("rpg/keyboard_sound")
	keyboard_repeat.start(1, 15)
	for a in playerlib.getPlayerList("#human"):
		usermsg.centermsg(a.userid, "열 ")
		gamethread.delayed(0.25, usermsg.centermsg, (a.userid, "열정 "))
		gamethread.delayed(0.5, usermsg.centermsg, (a.userid, "열정을 "))
		gamethread.delayed(0.75, usermsg.centermsg, (a.userid, "열정을 바 "))
		gamethread.delayed(1, usermsg.centermsg, (a.userid, "열정을 바르 "))
		gamethread.delayed(1.25, usermsg.centermsg, (a.userid, "열정을 바르게 "))
		gamethread.delayed(1.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰 "))
		gamethread.delayed(1.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 "))
		gamethread.delayed(2, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사"))
		gamethread.delayed(2.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람"))
		gamethread.delayed(2.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은"))
		gamethread.delayed(2.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성"))
		gamethread.delayed(3, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공"))
		gamethread.delayed(3.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하"))
		gamethread.delayed(3.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠"))
		gamethread.delayed(3.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지"))
		gamethread.delayed(4, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,"))
		gamethread.delayed(4.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n"))
		gamethread.delayed(4.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그"))
		gamethread.delayed(4.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열"))
		gamethread.delayed(5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정"))
		gamethread.delayed(5.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을"))
		gamethread.delayed(5.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘"))
		gamethread.delayed(5.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못"))
		gamethread.delayed(6, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되"))
		gamethread.delayed(6.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게"))
		gamethread.delayed(6.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴"))
		gamethread.delayed(6.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다"))
		gamethread.delayed(7, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면"))
		gamethread.delayed(7.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n"))
		gamethread.delayed(7.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당"))
		gamethread.delayed(7.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신"))
		gamethread.delayed(8, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은"))
		gamethread.delayed(8.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하"))
		gamethread.delayed(8.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루"))
		gamethread.delayed(8.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종"))
		gamethread.delayed(9, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다"))
		gamethread.delayed(9.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리"))
		gamethread.delayed(9.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를"))
		gamethread.delayed(9.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지"))
		gamethread.delayed(10, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜"))
		gamethread.delayed(10.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보"))
		gamethread.delayed(10.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고"))
		gamethread.delayed(10.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지"))
		gamethread.delayed(11, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나"))
		gamethread.delayed(11.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가"))
		gamethread.delayed(11.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는"))
		gamethread.delayed(11.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사"))
		gamethread.delayed(12, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람"))
		gamethread.delayed(12.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을"))
		gamethread.delayed(12.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질"))
		gamethread.delayed(12.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투"))
		gamethread.delayed(13, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하"))
		gamethread.delayed(13.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는"))
		gamethread.delayed(13.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하"))
		gamethread.delayed(13.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시"))
		gamethread.delayed(14, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히"))
		gamethread.delayed(14.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히메"))
		gamethread.delayed(14.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히메일"))
		gamethread.delayed(14.75, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히메일 뿐"))
		gamethread.delayed(15, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히메일 뿐이"))
		gamethread.delayed(15.25, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히메일 뿐이다"))
		gamethread.delayed(15.5, usermsg.centermsg, (a.userid, "열정을 바르게 쓰는 사람은 성공하겠지만,\n 그 열정을 잘못되게 쓴다면,\n  당신은 하루종일 다리를 지켜보고 지나가는 사람을 질투하는 하시히메일 뿐이다."))

def z_nearcoord_another(xx, yy, zz, x, y, z, allow_distance):
	victim_location = vecmath.vector(x, y, z)
	attacker_location = vecmath.vector(xx, yy, zz)
	distance = vecmath.distance(victim_location, attacker_location) * 0.0254
	if float(distance) <= float(allow_distance):
		return 1
	return 0

def z_nearcoord(loc, x, y, z, allow_distance):
	victim_location = vecmath.vector(x, y, z)
	attacker_location = vecmath.vector(loc)
	distance = vecmath.distance(victim_location, attacker_location) * 0.0254
	if float(distance) <= float(allow_distance):
		return 1
	return 0

def flashbang_detonate(ev):
	userid = ev['userid']
	e_x = ev['x']
	e_y = ev['y']
	e_z = ev['z']
	steamid = getplayerzeisenid(userid)
	if steamid != "BOT":
		if steamid == "STEAM_0119861059" and not "ze_" in map():
			fuck = z_nearcoord((e_x, e_y, e_z), 486, 912, 1100, 3)
			if fuck == 1:
				if str(sv('eventscripts_currentmap')) == "de_losttemple2": est.remove("func_breakable")
			for f_userid in es.getUseridList():
				if es.getplayerteam(f_userid) == int(sv('humanteam')):
					est.god(f_userid, 1)
					gamethread.delayed(0.05, est.god, (f_userid, 0))
			es.server.cmd('es_xgive %s env_explosion' %(userid))
			last_give = int(sv('eventscripts_lastgive'))
			es.entitysetvalue(last_give, "classname", "team_explosion")
			wide = 1250
			damage = 500
			es.server.cmd('es_xfire %s team_explosion addoutput "imagnitude %s\"' % (userid, wide))
			es.server.cmd('es_xfire %s team_explosion addoutput "iradiusoverride %s\"' % (userid, damage))
			et = int(es.getplayerhandle(userid))
			es.setindexprop(last_give, 'CBaseEntity.m_hOwnerEntity', et)
			es.setindexprop(last_give, "CBaseEntity.m_iTeamNum", es.getplayerteam(userid))
			est.entteleport(last_give, e_x, e_y, e_z)
			es.server.cmd('es_xfire %s team_explosion explode' % userid)

def fucker():
	test = es.createentityindexlist('')
	for a in test:
		classname = es.entitygetvalue(a, "classname")
		if not classname in "env_sprite, prop_physics_multiplayer": es.msg(classname)

def grenade_bounce(ev):
	userid = ev['userid']
	e_x = ev['x']
	e_y = ev['y']
	e_z = ev['z']
	steamid = getplayerzeisenid(userid)
	if steamid != "BOT":
		if steamid == "STEAM_0119861059" and not "ze_" in map():
			fuck = es.createentityindexlist("smokegrenade_projectile")
			index = 0
			for f_index in fuck:
				source = es.getindexprop(f_index, "CBaseEntity.m_vecOrigin").split(",")
				if source[0] == e_x:
					if source[1] == e_y:
						if source[2] == e_z:
							index = f_index
			if index > 0:
				for f_userid in es.getUseridList():
					if es.getplayerteam(f_userid) == int(sv('humanteam')):
						est.god(f_userid, 1)
						gamethread.delayed(0.05, est.god, (f_userid, 0))
				es.server.cmd('es_xgive %s env_explosion' %(userid))
				last_give = int(sv('eventscripts_lastgive'))
				es.entitysetvalue(last_give, "classname", "team_explosion")
				wide = 400
				damage = 400
				es.server.cmd('es_xfire %s team_explosion addoutput "imagnitude %s\"' % (userid, wide))
				es.server.cmd('es_xfire %s team_explosion addoutput "iradiusoverride %s\"' % (userid, damage))
				et = int(es.getplayerhandle(userid))
				es.setindexprop(last_give, 'CBaseEntity.m_hOwnerEntity', et)
				es.setindexprop(last_give, "CBaseEntity.m_iTeamNum", es.getplayerteam(userid))
				est.entteleport(last_give, e_x, e_y, e_z)
				es.server.cmd('es_xfire %s team_explosion explode' % userid)
				es.emitsound('entity', index, 'ambient/explosions/explode_%s.wav' % random.randint(1, 8), 1.0, 0.85)

			fuck = es.createentityindexlist("hegrenade_projectile")
			index = 0
			for f_index in fuck:
				source = es.getindexprop(f_index, "CBaseEntity.m_vecOrigin").split(",")
				if source[0] == e_x:
					if source[1] == e_y:
						if source[2] == e_z:
							index = f_index
			if index > 0:
				for f_userid in es.getUseridList():
					if es.getplayerteam(f_userid) == int(sv('humanteam')):
						est.god(f_userid, 1)
						gamethread.delayed(0.05, est.god, (f_userid, 0))
				es.server.cmd('es_xgive %s env_explosion' %(userid))
				last_give = int(sv('eventscripts_lastgive'))
				es.entitysetvalue(last_give, "classname", "team_explosion")
				wide = 400
				damage = 400
				es.server.cmd('es_xfire %s team_explosion addoutput "imagnitude %s\"' % (userid, wide))
				es.server.cmd('es_xfire %s team_explosion addoutput "iradiusoverride %s\"' % (userid, damage))
				et = int(es.getplayerhandle(userid))
				es.setindexprop(last_give, 'CBaseEntity.m_hOwnerEntity', et)
				es.setindexprop(last_give, "CBaseEntity.m_iTeamNum", es.getplayerteam(userid))
				est.entteleport(last_give, e_x, e_y, e_z)
				es.server.cmd('es_xfire %s team_explosion explode' % userid)
				es.emitsound('entity', index, 'ambient/explosions/explode_%s.wav' % random.randint(1, 8), 1.0, 0.85)

NPC_LIST = {
	'npc_1_nightfever': {
		'name': '#255,255,255ZK-417',
		'text': ["수고하셨습니다."],
		'send_popup': "event_1",
	},
	'npc_c_nightfever': {
		'name': '#0,0,125체리',
		'text': ["안녕하세요. 뭔가 이상하지 않아요?"],
		'send_popup': -1,
	},
	'npc_ma_nightfever': {
		'name': '#255,255,255Kasto',
		'text': ["맘에드는게 있나? 음... 오늘 이상하단말이야."],
		'send_popup': "masterymenu",
	},
	'npc_beer_nightfever': {
		'name': '#255,255,255???',
		'text': ["아아.. 무언가 이상해."],
		'send_popup': -1,
	},
	'npc_kuria_nightfever': {
		'name': '#255,255,255Kuria',
		'text': ["123456789"],
		'send_popup': -1,
	},
	'npc_nosay_nightfever': {
		'name': '#0,0,0Oxy',
		'text': ["123456789"],
		'send_popup': -1,
	},
	'npc_reisen_nightfever': {
		'name': '#0,0,255Reisen',
		'text': ["123456789"],
		'send_popup': -1,
	},
	'npc_chall_nightfever': {
		'name': '#125,125,125Dark Teleporter',
		'text': ["무언가 이상하군."],
		'send_popup': -1,
	},
	'npc_monster_nightfever': {
		'name': '#255,55,55Killer',
		'text': ["수상해. 무언가."],
		'send_popup': "monster_1",
	},
	'npc_member1_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["아, 왠일인지 술만 마시니까 기분이 좋군.", "나도 이런 곳에서 살고싶다고 생각됬었어."],
		'send_popup': -1,
	},
	'npc_member2_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["오늘은 내가 한바탕 쏜다! 가자고!", "정말 마음에 들어."],
		'send_popup': -1,
	},
	'npc_member3_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["좋아, 가자!", "무엇이 우리를 기다리고 있을까?"],
		'send_popup': -1,
	},
	'npc_member4_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["여기에 돈을 다 써버렸어, 택시비는 어떻하지...", "이러다 회사에 늦겠는데?"],
		'send_popup': -1,
	},
	'npc_member5_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["정말 취한다, 취해.", "#0,0,255레이센#default이라는 녀석이 있었는데, 오늘은 안보이네..."],
		'send_popup': -1,
	},
	'npc_member6_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["유우타씨를 볼수 있을까?", "오긴 와봤는데, 돈이 없어서 못사겠어. 난 사람들을 구경하고있어."],
		'send_popup': -1,
	},
	'npc_member7_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["다 필요없어! 하하하하!", "정말 놀라운 탄막이로군."],
		'send_popup': -1,
	},
	'npc_member8_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["여기 가끔 #0,0,255체인#default이라는 놈이 와서 도박을 즐겨했지, 늘 지곤했다고.", "정말 여긴 장사가 잘될거같아. 하루에 오는 사람이 몇만명은 넘는곳이지."],
		'send_popup': -1,
	},
	'npc_member9_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["다른 술집에 있는 술들은 싱겁고 맛이 없었지, 하지만 여긴 달라.", "저 도시에 대한 이야기를 알아? 아, #0,255,0안내원#default이 있었는데... 미국으로 갔나봐, 곧 온대."],
		'send_popup': -1,
	},
	'npc_member10_realnightfever': {
		'name': '#0,0,0이자카야 손님',
		'text': ["곧 이 주점도 닫을거 같다. 좀더 즐기고 싶었는데..."],
		'send_popup': -1,
	},
	'npc_len_realnightfever': {
		'name': '#0,0,0???',
		'text': ["으으으으...", "으으으......"],
		'send_popup': -1,
	},
	'npc_beer_realnightfever': {
		'name': '#0,0,0주정뱅이',
		'text': ["유유타씨는 어디에 있을까?", "저 도시가 어떤지 생각해봤어?"],
		'send_popup': -1,
	},
	'npc_junya_realnightfever': {
		'name': '#purpleJunya',
		'text': ["텐지는 나에게 정말 잊지 못할걸 줬지.", "구경하고 싶은걸 마음껏 구경하라고."],
		'send_popup': -1,
	},
	'npc_tenji_realnightfever': {
		'name': '#255,0,0Tenji',
		'text': ["후회는 없을거야, 마음껏 먹어두게."],
		'send_popup': "tenji_1",
	},
}


STET_LIST = {
	'체력': {
		'list': 1,
		'stetname': "health",
		'stet_up': 9,
		'stetmax': -1,
	},
	'근력': {
		'list': 2,
		'stetname': "power",
		'stet_up': 1,
		'stetmax': -1,
	},
	'민첩': {
		'list': 3,
		'stetname': "speed",
		'stet_up': 0.01,
		'stetmax': -1,
	},
	'방어력': {
		'list': 4,
		'stetname': "armor",
		'stet_up': 0.9,
		'stetmax': -1,
	},
	'주문력': {
		'list': 5,
		'stetname': "magic",
		'stet_up': 1,
		'stetmax': -1,
	},
	'지능': {
		'list': 6,
		'stetname': "dollar_regen",
		'stet_up': 1,
		'stetmax': -1,
	},
}

ITEM_LIST = {
	'0': {
		'itemrealname': "CS(Cash)",
		'itemkeyname': "cs",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'1': {
		'itemrealname': "크리스탈",
		'itemkeyname': "item1",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'2': {
		'itemrealname': "파란색 버섯",
		'itemkeyname': "item2",
		'duse': 1,
		'info': "사람들이 찾아오고 애용해오는 아이템이다.",
		'effect_info': "이 아이템을 사용할경우 50％ 확률로 스킬과 스텟이 초기화됩니다.",
		'trade': 1,
	},
	'3': {
		'itemrealname': "요정의 샘물",
		'itemkeyname': "item3",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'4': {
		'itemrealname': "요정의 씨앗",
		'itemkeyname': "item4",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'5': {
		'itemrealname': "황혼주점 티켓",
		'itemkeyname': "item5",
		'duse': 1,
		'info': "이 티켓으로 황혼 이자카야를 갈수 있다고 한다.",
		'effect_info': "이 아이템을 사용할경우 de_nightfever으로 맵 투표를 시작합니다.(투표 실패후 60초 이내에 하면 먹통)\nde_nightfever 맵에 있는 상태에서 사용하면 +60초 폐점 예정 시간이 늘어납니다.",
		'trade': 1,
	},
	'6': {
		'itemrealname': "테이지의 약물",
		'itemkeyname': "item6",
		'duse': 1,
		'info': "테이지의 전용 약물이다, 그녀는 이것을 좋아하지도 않고, 싫어하지도 않는다.",
		'effect_info': "이 아이템을 사용할경우 스텟 변화가 생기게 됩니다.",
		'trade': 1,
	},
	'7': {
		'itemrealname': "황혼의 마도서",
		'itemkeyname': "item7",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'8': {
		'itemrealname': "닌자의 마도서",
		'itemkeyname': "item8",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'9': {
		'itemrealname': "유혹의 마도서",
		'itemkeyname': "item9",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'10': {
		'itemrealname': "양말",
		'itemkeyname': "item10",
		'duse': 1,
		'info': "크리스마스 전용 아이템이다.(12.25~1.13)",
		'effect_info': "랜덤으로 아이템이 나옵니다! (체인의 마도서, ...)",
		'trade': 1,
	},
	'11': {
		'itemrealname': "천사의 마도서",
		'itemkeyname': "item11",
		'duse': 1,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'12': {
		'itemrealname': "맥주",
		'itemkeyname': "item12",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'13': {
		'itemrealname': "적의 목",
		'itemkeyname': "item13",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'14': {
		'itemrealname': "암흑의 마도서",
		'itemkeyname': "item14",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'15': {
		'itemrealname': "스칼렛의 날개",
		'itemkeyname': "item15",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'16': {
		'itemrealname': "이벤트 티켓",
		'itemkeyname': "item16",
		'duse': 0,
		'info': "1",
		'effect_info': "1",
		'trade': 1,
	},
	'17': {
		'itemrealname': "떡국",
		'itemkeyname': "item17",
		'duse': 1,
		'info': "새해 전용 아이템이다.",
		'effect_info': "체력이 +2, 데미지가 +0.5 상승합니다. (확률로 서비스 아이템 제공)",
		'trade': 1,
	},
	'18': {
		'itemrealname': "파트너 계약서",
		'itemkeyname': "item18",
		'duse': 1,
		'info': "파트너를 맺을수 있다.",
		'effect_info': "파트너를 맺을수 있습니다.(자신 제외) 해지도 가능합니다.",
		'trade': 1,
	},
	'19': {
		'itemrealname': "암흑 크리스탈",
		'itemkeyname': "item19",
		'duse': 0,
		'info': "???",
		'effect_info': "???",
		'trade': 1,
	},
	'20': {
		'itemrealname': "체리 코스프레",
		'itemkeyname': "item20",
		'duse': 1,
		'info': "체리 코스프레, 사용하면 다시는 벗을수 없다고 한다.",
		'effect_info': "이 코스프레를 사용하면 적 스피드와 자신 스피드의 데미지에 비례해 데미지를 배로 늘립니다.",
		'trade': 1,
	},
	'21': {
		'itemrealname': "파라노야 코스프레",
		'itemkeyname': "item21",
		'duse': 1,
		'info': "파라노야 코스프레, 사용하면 다시는 벗을수 없다고 한다.",
		'effect_info': "이 코스프레를 사용하면 마스터리 무기로 사살할경우, 고정 +2 마스터리 경험치를 더 지급합니다.",
		'trade': 1,
	},
	'22': {
		'itemrealname': "레이센 코스프레",
		'itemkeyname': "item22",
		'duse': 1,
		'info': "레이센 코스프레, 사용하면 다시는 벗을수 없다고 한다.",
		'effect_info': "이 코스프레를 사용하면 폭발 데미지가 상승합니다.",
		'trade': 1,
	},
	'23': {
		'itemrealname': "수수께끼의 마도서",
		'itemkeyname': "item23",
		'duse': 1,
		'info': "[3?뗥]??[3?뗥]촌儆儆儆?VW뗺딦딶뛑",
		'effect_info': "홇?   甕|  ?숙O5쟤O끟껮 h?   h??\홇?   ?|  ?",
		'trade': 1,
	},
	'24': {
		'itemrealname': "테이지 코스프레",
		'itemkeyname': "item24",
		'duse': 1,
		'info': "테이지 코스프레, 사용하면 다시는 벗을수 없다고 한다.",
		'effect_info': "이 코스프레를 사용하면 스피드 0.2, 칼 데미지 1.5배가 등장합니다",
		'trade': 1,
	},
	'25': {
		'itemrealname': "천사의 날개",
		'itemkeyname': "item25",
		'duse': 0,
		'info': "A",
		'effect_info': "A",
		'trade': 1,
	},
	'26': {
		'itemrealname': "쿠리아 코스프레",
		'itemkeyname': "item26",
		'duse': 1,
		'info': "쿠리아 코스프레, 사용하면 다시는 벗을수 없다고 한다.",
		'effect_info': "이 코스프레를 사용하면 돋보기를 황금 돋보기로 바꿀수 있게 해줍니다..",
		'trade': 1,
	},
	'27': {
		'itemrealname': "성경 책",
		'itemkeyname': "item27",
		'duse': 0,
		'info': "A",
		'effect_info': "A",
		'trade': 1,
	},
	'28': {
		'itemrealname': "A Type",
		'itemkeyname': "item28",
		'duse': 1,
		'info': ".",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'29': {
		'itemrealname': "Camera",
		'itemkeyname': "item29",
		'duse': 1,
		'info': "카메라이다. 저장된 테이프를 찾아 실행시키면...",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'30': {
		'itemrealname': "기록 노트",
		'itemkeyname': "item30",
		'duse': 0,
		'info': "카메라이다. 저장된 테이프를 찾아 실행시키면...",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'31': {
		'itemrealname': "포커 티켓",
		'itemkeyname': "item31",
		'duse': 1,
		'info': "뉴 포커를 할수 있는 포커이다.",
		'effect_info': "사용하면 뉴 포커를 할수 있습니다. 세팅은 당신이 모든것을.",
		'trade': 0,
	},
	'32': {
		'itemrealname': "책",
		'itemkeyname': "item32",
		'duse': 1,
		'info': "뭘까...",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'33': {
		'itemrealname': "맥주",
		'itemkeyname': "item33",
		'duse': 1,
		'info': "황혼주점에서 구입한 맥주이다. 텐지가 말하기를 맛은 아주 끝내준다고.",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'34': {
		'itemrealname': "청주",
		'itemkeyname': "item34",
		'duse': 1,
		'info': "황혼주점에서 구입한 청주이다. 준야가 좋아하는 술 중 하나.",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'35': {
		'itemrealname': "야키토키",
		'itemkeyname': "item35",
		'duse': 1,
		'info': "황혼주점에서 구입한 야키토키이다. 텐지의 말로는 자신이 선보이는 탄막이라고(...)",
		'effect_info': "(스토리 아이템입니다.)",
		'trade': 0,
	},
	'36': {
		'itemrealname': "마초",
		'itemkeyname': "item36",
		'duse': 1,
		'info': "oow : 마초맨",
		'effect_info': "마초를 핍니다..?",
		'trade': 1,
	},
	'37': {
		'itemrealname': "B Type",
		'itemkeyname': "item37",
		'duse': 0,
		'info': ".",
		'effect_info': ".",
		'trade': 1,
	},
	'38': {
		'itemrealname': "페리의 인형",
		'itemkeyname': "item38",
		'duse': 1,
		'info': ".",
		'effect_info': ".",
		'trade': 0,
	},
	'39': {
		'itemrealname': "일렉트로 원소",
		'itemkeyname': "item39",
		'duse': 0,
		'info': ".",
		'effect_info': ".",
		'trade': 1,
	},
	'40': {
		'itemrealname': "스워드 원소",
		'itemkeyname': "item40",
		'duse': 0,
		'info': ".",
		'effect_info': ".",
		'trade': 1,
	},
}

BARI_LIST = {
	'나무통': {
		'model': 'props_c17/woodbarrel001.mdl',
		'cash': 250,
	},
	'탁자': {
		'model': 'props_c17/furnituretable001a.mdl',
		'cash': 2000,
	},
	'나무 상자 (Small)': {
		'model': 'props_junk/wood_crate001a.mdl',
		'cash': 300,
	},
	'나무 상자 (Big)': {
		'model': 'props_junk/wood_crate002a.mdl',
		'cash': 500,
	},
}

MASTERY_SKILLS = {
	'폭발탄': {
		'mastery_what': 1,
		'skillname': "mastery_skill1",
		'need_masteryxp': 600,
		'max': 5,
		'info': '히트에 성공시 확률로 폭발탄이 터집니다.',
		'level_info': '찍을때마다 확률은 1％ 상승합니다.',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'크리티컬': {
		'mastery_what': 1,
		'skillname': "mastery_skill2",
		'need_masteryxp': 600,
		'max': 5,
		'info': '히트에 성공할때의 크리티컬 확률을 증진시켜줍니다.',
		'level_info': '찍을때마다 확률은 1％ 상승합니다.',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'헤드샷 데미지 증가': {
		'mastery_what': 1,
		'skillname': "mastery_skill3",
		'need_masteryxp': 400,
		'max': 5,
		'info': '헤드샷 데미지를 상승시켜줍니다.',
		'level_info': '찍을때마다 헤드샷 데미지는 4％ 상승합니다.',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'피스톨로부터의 구원': {
		'mastery_what': 1,
		'skillname': "mastery_skill4",
		'need_masteryxp': 1000,
		'max': 5,
		'info': '체력이 25 이하 상태일때, 헤드샷으로 사살할경우 확률로 체력을 100％ 회복합니다.',
		'level_info': '찍을때마다 확률은 15％ 상승합니다.',
		'skillbook': 11,
		'nope_skill': ["none"],
	},
	'체력 증가': {
		'mastery_what': 2,
		'skillname': "mastery_skill1",
		'need_masteryxp': 100,
		'max': 20,
		'info': '체력을 증가시켜줍니다.',
		'level_info': '찍을때마다 체력은 +15 상승합니다.',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'체력 리젠': {
		'mastery_what': 2,
		'skillname': "mastery_skill2",
		'need_masteryxp': 500,
		'max': 3,
		'info': '체력을 1초당 리젠시킵니다.',
		'level_info': '찍을때마다 리젠 체력이 +1 증가합니다.',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'익스플로전 소드': {
		'mastery_what': 2,
		'skillname': "mastery_skill3",
		'need_masteryxp': 500,
		'max': 5,
		'info': '히트에 성공했을때, 확률로 폭발검 효과가 나타납니다.',
		'level_info': '찍을때마다 확률이 증가합니다.',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'버서크': {
		'mastery_what': 2,
		'skillname': "mastery_skill4",
		'need_masteryxp': 600,
		'max': 5,
		'info': '자신이 체력이 50％ 이하일때, 칼 데미지가 ％ 수치로 상승합니다.',
		'level_info': '찍을때마다 칼 데미지가 10％ 상승합니다.',
		'skillbook': 7,
		'nope_skill': ["none"],
	},
	'Ammoful': {
		'mastery_what': 3,
		'skillname': "mastery_skill1",
		'need_masteryxp': 500,
		'max': 1,
		'info': '액티브 스킬입니다.(F1) 3000 달러를 지불하고 총알과 방탄복을 채워줍니다.',
		'level_info': '(한번만 찍는 스킬입니다)',
		'skillbook': -1,
		'nope_skill': ["none"],
	},
	'치유': {
		'mastery_what': 3,
		'skillname': "mastery_skill2",
		'need_masteryxp': 400,
		'max': 5,
		'info': '액티브 스킬입니다.(F1) 3000 달러를 지불하고 체력을 회복시켜줍니다.',
		'level_info': '찍을때마다 회복률이 10％ 증가합니다.',
		'skillbook': 25,
		'nope_skill': ["none"],
	},
	'Remote Human': {
		'mastery_what': 3,
		'skillname': "mastery_skill3",
		'need_masteryxp': 1200,
		'max': 1,
		'info': '액티브 스킬입니다.(F1) 5000 달러를 지불하고 아군 봇을 자신의 위치로 모두 소환합니다.',
		'level_info': '.',
		'skillbook': 25,
		'nope_skill': ["none"],
	},
	'Be Doctor': {
		'mastery_what': 3,
		'skillname': "mastery_skill4",
		'need_masteryxp': 1500,
		'max': 1,
		'info': '액티브 스킬입니다.(F1) 6500 달러를 지불하고 죽은 플레이어들을 소생시킵니다.',
		'level_info': '.',
		'skillbook': 25,
		'nope_skill': ["none"],
	},
	'God Save The King': {
		'mastery_what': 3,
		'skillname': "mastery_skill5",
		'need_masteryxp': 3333,
		'max': 1,
		'info': '액티브 스킬입니다.(F1) 15000 달러를 지불하고 죽은 플레이어/아군 봇들을 소생시킵니다.',
		'level_info': '.',
		'skillbook': 11,
		'nope_skill': ["none"],
	},
}

SKILL_TEST = {
	'Big Money': {
		'skillname': "skill1",
		'need_skillp': 1,
		'max': 5,
		'skillbook': -1,
		'info': '데미지를 1 이상 주었을때, 확률로 달러를 지급합니다.',
		'level_info': '익힐때 마다 확률이 1％ 상승하며, +300 달러가 추가됩니다.',
		'nope_skill': ["none"],
	},
	'죽은 자의 역습': {
		'skillname': "skill2",
		'need_skillp': 1,
		'max': 5,
		'skillbook': -1,
		'info': '자신이 죽은 상태에서, 봇에게 데미지를 가할경우 그 데미지는 ％ 수치로 커집니다.',
		'level_info': '익힐때 마다 데미지가 100％ 상승합니다.',
		'nope_skill': ["none"],
	},
	'Flashbang Dominator': {
		'skillname': "skill3",
		'need_skillp': 1,
		'max': 4,
		'skillbook': -1,
		'info': '플래시뱅을 맞출경우 그 데미지는 + 수치로 대폭 상승합니다.',
		'level_info': '익힐때 마다 데미지가 500+ 상승합니다.',
		'nope_skill': ["none"],
	},
	'반격': {
		'skillname': "skill4",
		'need_skillp': 2,
		'max': 5,
		'skillbook': -1,
		'info': '데미지를 받았을때 확률로 반격합니다.',
		'level_info': '익힐때마다 반격 데미지 +100 상승, 확률은 2％ 상승합니다.',
		'nope_skill': ["none"],
	},
	'자폭': {
		'skillname': "skill5",
		'need_skillp': 3,
		'max': 5,
		'skillbook': -1,
		'info': '죽었을때, 20％ 확률로 자폭합니다.',
		'level_info': '익힐때마다 자폭 범위 및 데미지가 커집니다.',
		'nope_skill': ["none"],
	},
	'풀차지 - 무한 발사': {
		'skillname': "skill6",
		'need_skillp': 7,
		'max': 1,
		'skillbook': 7,
		'info': 'Full Charge 상태일때, 탄창 지급을 총알 지급으로 바꿉니다.',
		'level_info': '(1번만 찍는 스킬입니다.)',
		'nope_skill': ["none"],
	},
	'C4 - 닌자의 손놀림': {
		'skillname': "skill7",
		'need_skillp': 2,
		'max': 1,
		'skillbook': 8,
		'info': 'C4를 2.5배 빠르게 설치합니다.',
		'level_info': '(1번만 찍는 스킬입니다.)',
		'nope_skill': ["none"],
	},
	'급소': {
		'skillname': "skill8",
		'need_skillp': 1,
		'max': 5,
		'skillbook': -1,
		'info': '치명타(크리티컬) 데미지를 증가시켜줍니다.',
		'level_info': '익힐때마다 치명타 데미지가 15％씩 데미지가 증가합니다.',
		'nope_skill': ["none"],
	},
	'제이센 총 해킹법': {
		'skillname': "skill9",
		'need_skillp': 999,
		'max': 1,
		'skillbook': 9,
		'info': '제이센의 총(빨간색)의 능력을 사용할수 있게 해줍니다.',
		'level_info': '(1번만 찍는 스킬입니다.)',
		'nope_skill': ["none"],
	},
	'선두주자': {
		'skillname': "skill10",
		'need_skillp': 1,
		'max': 4,
		'skillbook': 8,
		'info': '3초간 스피드가 급속 상승합니다.',
		'level_info': '찍을때마다 급속 스피드가 1 상승합니다.',
		'nope_skill': ["none"],
	},
	'간접 흡혈': {
		'skillname': "skill11",
		'need_skillp': 2,
		'max': 5,
		'skillbook': 7,
		'info': '사살할때마다 체력이 증가합니다.',
		'level_info': '익힐때마다 사살할때의 체력 증가량이 +1 상승합니다.',
		'nope_skill': ["none"],
	},
	'급소 2': {
		'skillname': "skill12",
		'need_skillp': 1,
		'max': 5,
		'skillbook': 7,
		'info': '치명타(크리티컬) 데미지를 증가시켜줍니다.',
		'level_info': '익힐때마다 치명타 데미지가 20％씩 데미지가 증가합니다.',
		'nope_skill': ["none"],
	},
	'구매 확장': {
		'skillname': "skill13",
		'need_skillp': 2,
		'max': 1,
		'skillbook': 9,
		'info': '!buy <무기이름(m4a1, ak47, etc.)> 으로 T/CT 무기 구매가 가능해집니다.',
		'level_info': '(1번만 찍는 스킬입니다.)',
		'nope_skill': ["none"],
	},
	'빛으로의 구원': {
		'skillname': "skill14",
		'need_skillp': 3,
		'max': 1,
		'skillbook': 11,
		'info': '플래시뱅에 맞아도 효과가 나타나지 않습니다.',
		'level_info': '(1번만 찍는 스킬입니다.)',
		'nope_skill': ["none"],
	},
}

def bari_select(userid, choice, popupname):
	if choice != 10:
		cash = int(es.getplayerprop(userid, "CCSPlayer.m_iAccount"))
		bari_cash = int(BARI_LIST[choice]['cash'])
		if cash >= bari_cash:
			if isalive(userid):
				cash -= bari_cash
				es.setplayerprop(userid, 'CCSPlayer.m_iAccount', cash)
				es.prop_physics_create(userid, BARI_LIST[choice]['model'])
				index = int(sv('eventscripts_lastgive'))
				et = es.getplayerhandle(userid)
				#es.setindexprop(index, 'CBaseEntity.m_hOwnerEntity', et)
				if "ze_" in map() and int(sv('round')) >= 5:
					es.entitysetvalue(index, 'classname', 'breaking')
					es.server.cmd('es_xfire %s breaking break' %(userid))

def stet_select(userid, choice, popupname):
	if choice != 10:
		steamid = getplayerzeisenid(userid)
		stetpoint = es.keygetvalue(steamid, "player_data", "stetpoint")
		if int(es.keygetvalue(steamid, "player_data", "stetpoint")) >= 1:
			stetname = STET_LIST[choice]['stetname']
			stet_up = STET_LIST[choice]['stet_up']
			keymath(steamid, "player_data", "stetpoint", "-", 1)
			get_t = float(es.keygetvalue(steamid, "player_data", stetname)) + float(stet_up)
			es.keysetvalue(steamid, "player_data", stetname, get_t)
			esc.tell(userid, "#0,255,255%s 스텟을 익혀 %s 정도의 변화가 일어났습니다." %(choice, stet_up))
			rpgmenu_select(userid, "스텟", rpgmenu)

def learnskill_select(userid, choice, popupname):
	if choice != 10:
		steamid = getplayerzeisenid(userid)
		skillpoint = es.keygetvalue(steamid, "player_data", "skillpoint")
		client_skill = int(es.keygetvalue(steamid, "player_data", SKILL_TEST[choice]['skillname']))
		skill_max = int(SKILL_TEST[choice]['max'])
		need_skillp = int(SKILL_TEST[choice]['need_skillp'])
		sb = int(SKILL_TEST[choice]['skillbook'])
		if sb == -1: ok = 1
		else:
			skillbook_get = int(es.keygetvalue(steamid, "player_data", ITEM_LIST[str(SKILL_TEST[choice]['skillbook'])]['itemkeyname']))
			if skillbook_get >= 1: ok = 2
			else: ok = 0
		for b in SKILL_TEST[choice]['nope_skill']:
			if b != "none":
				if int(es.keygetvalue(steamid, "player_data", b)) > 0: ok = 0
		if skillpoint >= client_skill:
			if skill_max > client_skill:
				if ok >= 1:
					keymath(steamid, "player_data", str(SKILL_TEST[choice]['skillname']), "+", 1)
					keymath(steamid, "player_data", "skillpoint", "-", need_skillp)
					esc.tell(userid, "#0,255,255%s 스킬#255,255,255을 익혔습니다." %(choice))
					rpgmenu_select(userid, "스킬", 0)
					if ok == 2:
						esc.tell(userid, "#gold %s 스킬북 아이템#255,255,255은 소멸되었습니다." %(ITEM_LIST[str(SKILL_TEST[choice]['skillbook'])]['itemrealname']))
						keymath(steamid, "player_data", ITEM_LIST[str(SKILL_TEST[choice]['skillbook'])]['itemkeyname'], "-", 1)
				else: esc.tell(userid, "#255,255,255스킬 북이 없거나 현재 스킬들의 상성에 맞지 않습니다.")
			else: esc.tell(userid, "#255,255,255스킬이 이미 MAX 상태입니다.")
		else: esc.tell(userid, "#255,255,255스킬 포인트가 모자랍니다.")

def learnmskill_select(userid, choice, popupname):
	if choice != 10:
		steamid = getplayerzeisenid(userid)
		skillpoint = es.keygetvalue(steamid, "player_data", "skillpoint")
		client_skill = int(es.keygetvalue(steamid, "player_data", MASTERY_SKILLS[choice]['skillname']))
		skill_max = int(MASTERY_SKILLS[choice]['max'])
		need_skillp = int(MASTERY_SKILLS[choice]['need_masteryxp'])
		sb = int(MASTERY_SKILLS[choice]['skillbook'])
		if sb == -1: ok = 1
		else:
			skillbook_get = int(es.keygetvalue(steamid, "player_data", ITEM_LIST[str(MASTERY_SKILLS[choice]['skillbook'])]['itemkeyname']))
			if skillbook_get >= 1: ok = 2
			else: ok = 0
		for b in MASTERY_SKILLS[choice]['nope_skill']:
			if b != "none":
				if int(es.keygetvalue(steamid, "player_data", b)) > 0: ok = 0
		if skillpoint >= client_skill:
			if skill_max > client_skill:
				if ok >= 1:
					keymath(steamid, "player_data", MASTERY_SKILLS[choice]['skillname'], "+", 1)
					keymath(steamid, "player_data", "mastery_xp", "-", need_skillp)
					esc.tell(userid, "#0,255,255%s 스킬#255,255,255을 익혔습니다." %(choice))
					masterymenu_select(userid, "마스터리 스킬", 0)
					if ok == 2:
						esc.tell(userid, "#gold %s 스킬북 아이템#255,255,255은 소멸되었습니다." %(ITEM_LIST[str(MASTERY_SKILLS[choice]['skillbook'])]['itemrealname']))
						keymath(steamid, "player_data", ITEM_LIST[str(MASTERY_SKILLS[choice]['skillbook'])]['itemkeyname'], "-", 1)
				else: esc.tell(userid, "#255,255,255스킬 북이 없거나 현재 스킬들의 상성에 맞지 않습니다.")
			else: esc.tell(userid, "#255,255,255스킬이 이미 MAX 상태입니다.")
		else: esc.tell(userid, "#255,255,255스킬 포인트가 모자랍니다.")
def none_select(userid, choice, popupname):
	pass

def itemuse_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	username = es.getplayername(userid)
	keyname = ITEM_LIST[choice]['itemkeyname']
	keymath(steamid, "player_data", keyname, "-", 1)
	rpgmenu_select(userid, "인벤토리", 0)
	if str(choice) == "11":
		if not map() != "ba_quartzy":
			keymath(steamid, "player_data", "item11" ,"+", 1)
		if map() == "ba_quartzy":
			if int(sv('event_line')) == 9:
				getid = es.getuserid("[A Rank] Pery")
				est.sethealth(getid, 1)
				est.damage(userid, getid, 9999)
			else:
				keymath(steamid, "player_data", "item11" ,"+", 1)
	if str(choice) == "2":
		level = float(es.keygetvalue(steamid, "player_data", "level")) / 20
		level = est.rounddecimal(level, 0)
		level = level.replace(".0", "")
		level = int(level)
		if random.randint(1,(2 + level)) == 1:
			level = int(es.keygetvalue(steamid, "player_data", "level"))
			es.keysetvalue(steamid, "player_data", "skill1", 0)
			es.keysetvalue(steamid, "player_data", "skill2", 0)
			es.keysetvalue(steamid, "player_data", "skill3", 0)
			es.keysetvalue(steamid, "player_data", "skill4", 0)
			es.keysetvalue(steamid, "player_data", "skill5", 0)
			es.keysetvalue(steamid, "player_data", "skill6", 0)
			es.keysetvalue(steamid, "player_data", "skill7", 0)
			es.keysetvalue(steamid, "player_data", "skill8", 0)
			es.keysetvalue(steamid, "player_data", "skill9", 0)
			es.keysetvalue(steamid, "player_data", "skill10", 0)
			es.keysetvalue(steamid, "player_data", "skill11", 0)
			es.keysetvalue(steamid, "player_data", "skill12", 0)
			es.keysetvalue(steamid, "player_data", "skill13", 0)
			es.keysetvalue(steamid, "player_data", "skill14", 0)
			es.keysetvalue(steamid, "player_data", "skill15", 0)
			es.keysetvalue(steamid, "player_data", "skill16", 0)
			es.keysetvalue(steamid, "player_data", "skill17", 0)
			es.keysetvalue(steamid, "player_data", "skill18", 0)
			es.keysetvalue(steamid, "player_data", "skill19", 0)
			es.keysetvalue(steamid, "player_data", "skill20", 0)
			es.keysetvalue(steamid, "player_data", "skill21", 0)
			es.keysetvalue(steamid, "player_data", "skill22", 0)
			es.keysetvalue(steamid, "player_data", "skill23", 0)
			es.keysetvalue(steamid, "player_data", "skill24", 0)
			es.keysetvalue(steamid, "player_data", "skill25", 0)
			es.keysetvalue(steamid, "player_data", "skill26", 0)
			es.keysetvalue(steamid, "player_data", "skill27", 0)
			es.keysetvalue(steamid, "player_data", "skill28", 0)
			es.keysetvalue(steamid, "player_data", "skill29", 0)
			es.keysetvalue(steamid, "player_data", "skill30", 0)
			es.keysetvalue(steamid, "player_data", "skill31", 0)
			es.keysetvalue(steamid, "player_data", "skill32", 0)
			es.keysetvalue(steamid, "player_data", "skill33", 0)
			es.keysetvalue(steamid, "player_data", "skill34", 0)
			es.keysetvalue(steamid, "player_data", "skill35", 0)
			es.keysetvalue(steamid, "player_data", "skill36", 0)
			es.keysetvalue(steamid, "player_data", "skill37", 0)
			es.keysetvalue(steamid, "player_data", "skill38", 0)
			es.keysetvalue(steamid, "player_data", "skill39", 0)
			es.keysetvalue(steamid, "player_data", "skill40", 0)
			es.keysetvalue(steamid, "player_data", "health", 150)
			es.keysetvalue(steamid, "player_data", "power", 100)
			es.keysetvalue(steamid, "player_data", "speed", 1.0)
			es.keysetvalue(steamid, "player_data", "armor", 0)
			es.keysetvalue(steamid, "player_data", "magic", 0)
			es.keysetvalue(steamid, "player_data", "dollar_regen", 0)
			es.keysetvalue(steamid, "player_data", "skillpoint", level)
			es.keysetvalue(steamid, "player_data", "stetpoint", level)
			esc.msg("#255,255,255 %s : 단맛이 나더니, 온 몸이 시원해진 기분을 느꼈다." %(username))
		else: esc.msg("#255,255,255 %s : 매우 쓴맛을 느꼈다. 낭패를 본 기분이 든다." %(username))
	if str(choice) == "5":
		esc.msg("#blue %s 유저#255,255,255님이 #gold황혼주점 티켓 아이템#255,255,255을 사용하셨습니다." %(username))
		if map() != "de_nightfever":
			es.server.cmd('sm_votemap de_nightfever')
		if map() == "de_nightfever":
			svmath("nightfever_time", "+", 150)
	if str(choice) == "6":
		effe = random.randint(1,5)
		if effe == 1:
			esc.msg("#blue %s 유저#255,255,255님은 #55,255,55테이지의 약물#255,255,255을 마셔 #125,125,255체력이 +5 올랐습니다." %(username))
			keymath(steamid, "player_data", "health", "+", 5)
		if effe == 2:
			esc.msg("#blue %s 유저#255,255,255님은 #55,255,55테이지의 약물#255,255,255을 마셔 #255,125,125체력이 -5 하락했습니다." %(username))
			keymath(steamid, "player_data", "health", "-", 5)
		if effe == 3:
			esc.msg("#blue %s 유저#255,255,255님은 #55,255,55테이지의 약물#255,255,255을 마셔 #125,125,255민첩이 0.02 올랐습니다." %(username))
			speed = float(es.keygetvalue(steamid, "player_data", "speed")) + 0.02
			es.keysetvalue(steamid, "player_data", "speed", speed)
		if effe == 4:
			esc.msg("#blue %s 유저#255,255,255님은 #55,255,55테이지의 약물#255,255,255을 마셔 #255,125,125민첩이 0.02 하락했습니다." %(username))
			speed = float(es.keygetvalue(steamid, "player_data", "speed")) - 0.02
			es.keysetvalue(steamid, "player_data", "speed", speed)
		if effe == 5:
			esc.msg("#blue %s 유저#255,255,255님은 #55,255,55테이지의 약물#255,255,255을 마셔 #255,125,125체력이 -3 하락했습니다." %(username))
			keymath(steamid, "player_data", "health", "-", 3)
	if str(choice) == "10":
		if random.randint(1,100) == 1:
			esc.msg("#blue %s 유저#255,255,255님은 #55,255,55양말#255,255,255을 뜯어 #gold스킬 포인트 10 #255,255,255아이템을 획득했습니다." %(username))
			keymath(steamid, "player_data", "skillpoint", "+", 10)
		else:
			if random.randint(1,25) == 1:
				esc.msg("#blue %s 유저#255,255,255님은 #55,255,55양말#255,255,255을 뜯어 #gold유혹 마도서 1개 #255,255,255아이템을 획득했습니다." %(username))
				keymath(steamid, "player_data", "item9", "+", 1)
			else:
				if random.randint(1,10) == 1:
					esc.msg("#blue %s 유저#255,255,255님은 #55,255,55양말#255,255,255을 뜯어 #gold닌자의 마도서 1개 #255,255,255아이템을 획득했습니다." %(username))
					keymath(steamid, "player_data", "item8", "+", 1)
				else:
					if random.randint(1,5) == 1:
						esc.msg("#blue %s 유저#255,255,255님은 #55,255,55양말#255,255,255을 뜯어 #gold황혼의 마도서 1개 #255,255,255아이템을 획득했습니다." %(username))
						keymath(steamid, "player_data", "item7", "+", 1)
					else:
						esc.msg("#blue %s 유저#255,255,255님은 #55,255,55양말#255,255,255을 뜯어 #gold황혼주점 티켓 2개 #255,255,255아이템을 획득했습니다." %(username))
						keymath(steamid, "player_data", "item5", "+", 2)
	if str(choice) == "17":
		msg = "이번 새해에는 무리하지 말것"
		if random.randint(1,200) == 1: msg = "체리 코스프레로 거짓말 하지 않기"
		if random.randint(1,150) == 1: msg = "파라노야 코스프레로 날뛰어 보기"
		if random.randint(1,300) == 1: msg = "쿠리아 코스프레로 점치기"
		if msg == "쿠리아 코스프레로 점치기": keymath(steamid, "player_data", "item26", "+", 1)
		if msg == "체리 코스프레로 거짓말 하지 않기": keymath(steamid, "player_data", "item20", "+", 1)
		if msg == "파라노야 코스프레로 날뛰어 보기": keymath(steamid, "player_data", "item21", "+", 1)
		esc.msg("#255,255,255 %s : 떡국을 다 먹고나니, 오른쪽에 다음과 같은게 적혀있는 종이가 있었다. #125,125,125'%s'" %(username, msg))
		keymath(steamid, "player_data", "health", "+", 2)
		power = float(es.keygetvalue(steamid, "player_data", "power")) + 0.5
		es.keysetvalue(steamid, "player_data", "power", power)
	if str(choice) == "18":
		event_1 = popuplib.easymenu('p_1_%s' %(userid), None, partner_select)
		event_1.settitle("＠ 파트너 선택")
		event_1.c_endsep = " \n○ 파트너를 선택해주세요.\n "
		event_1.addoption("None", "파트너 해지")
		for a in playerlib.getPlayerList("#human"):
			tusername = es.getplayername(a.userid)
			tsteamid = getplayerzeisenid(a.userid)
			if a.userid != userid:
				event_1.addoption(tsteamid, tusername)
		event_1.send(userid)
		popuplib.delete('p_1_%s' %(userid))
	if str(choice) == "20":
		esc.msg("#0,255,255%s : 체리 코스프레를 장착시켰습니다." %(username))
		es.keysetvalue(steamid, "player_data", "skin", "player/reisen/cirno/cirno")
	if str(choice) == "21":
		esc.msg("#0,255,255%s : 파라노야 코스프레를 장착시켰습니다." %(username))
		es.keysetvalue(steamid, "player_data", "skin", "player/techknow/paranoya/paranoya")
	if str(choice) == "22":
		esc.msg("#0,0,255%s : 레이센 코스프레를 장착시켰습니다." %(username))
		es.keysetvalue(steamid, "player_data", "skin", "player/hhp227/miku/miku")
	if str(choice) == "23":
		esc.msg("#255,255,255%s : 수수께끼의 마도서를 강제로 읽을려고 하자, 사라지고 말았다..." %(username))
	if str(choice) == "24":
		esc.msg("#0,255,255%s : 테이지 코스프레를 장착시켰습니다." %(username))
		es.keysetvalue(steamid, "player_data", "skin", "player/konata/idol/idol")
	if str(choice) == "26":
		esc.msg("#0,0,0%s : 쿠리아 코스프레를 장착시켰습니다." %(username))
		es.keysetvalue(steamid, "player_data", "skin", "player/slow/amberlyn/re5/wesker/slow")
	if str(choice) == "28":
		route = 3
		keymath(steamid, "player_data", "item28" ,"+", 1)
		if int(es.keygetvalue(steamid, "player_data", "item29")) > 0:
			if steamid == "STEAM_0020251844":
				route = 2
				if str(sv('sv_password')) == "nipperz":
					route = 1
			usermsg.centermsg(userid, "▶ Playing...")
			if route == 0:
				gamethread.delayed(3, esc.tell, (userid, "#255,255,255... 그저 노이즈 화면과 소리만 들렸다."))
			if route == 3:
				gamethread.delayed(3, esc.tell, (userid, "#255,255,255... 마담과 페리가 싸우고있었다."))
			if route == 1:
				gamethread.delayed(3, npc_tell, (userid, "#0,0,255Reisen", "아니, 정말이에요?"))
				gamethread.delayed(6, npc_tell, (userid, "#0,0,255Reisen", "정말로... 후회 안해요?"))
				gamethread.delayed(9, esc.tell, (userid, "#255,255,255... 그저 노이즈 화면과 소리만 들렸다."))
			if route == 2:
				gamethread.delayed(3, esc.tell, (userid, "#255,255,255레이센이 카메라쪽으로 서서히 다가오고 있었다."))
				gamethread.delayed(6, esc.tell, (userid, "#255,255,255눈은 보이지 않지만, "))
		else: esc.tell(userid, "#255,255,255카메라 아이템이 존재하지 않습니다.")
	if str(choice) == "29": est.give(userid, "weapon_awp")
	if str(choice) == "31":
		if str(sv('eventscripts_currentmap')) == "de_nightfever" and int(sv('poker_begin')) == 0:
			esc.msg("#255,255,255%s 님이 포커 티켓을 사용하셨습니다. 10초 안에 결정하세요." %(username))
			global poker_begin
			poker_begin = popuplib.create('poker_start')
			poker_begin.addline(" ")
			poker_begin.addline("＊ 뉴 포커가 시작됩니다.")
			poker_begin.addline(" ")
			poker_begin.addline("→ [$시작 자금 : 20000$]")
			poker_begin.addline(" ")
			poker_begin.addline("->1. 뉴 포커 게임에 참가한다.")
			poker_begin.addline("->0. 뉴 포커 게임에 참가하지 않는다.")
			poker_begin.addline(" ")
			poker_begin.menuselect = poker_begin_select
			es.keygroupdelete('poker_info')
			global POKER_CARD_LIST
			global POKER_PLAYER_LIST
			POKER_CARD_LIST = []
			POKER_PLAYER_LIST = []
			es.set("poker_begin", 1)
			for a in playerlib.getPlayerList("#human"):
				poker_begin.send(a.userid)
			gamethread.delayed(10, es.set, ("poker_begin", 2))
			gamethread.delayed(10, poker_begins, ())
			#popuplib.delete('poker_start')
		else: keymath(steamid, "player_data", "item31" ,"+", 1)
	if str(choice) == "32":
		keymath(steamid, "player_data", "item32" ,"+", 1)
		esc.msg("#255,0,0책을 펴보았다.")
		msg = "항상 웃음을 띄우십시오\n \n손으로 어루만져드리십시오\n \n항상 새로운 것을 찾으십시오\n \n아름다운 것을 찾아 즐기십시오\n \n \n감동할 줄 모르는 사람은 창조력을 잃어버린 사람입니다."
		for a in playerlib.getPlayerList("#human"):
			usermsg.hudhint(a.userid, msg)
	if str(choice) == "33":
		tomsg = random.choice(["다 마셨다간 취할거 같다.", "뭔가 머리가 어지럽다."])
		esc.msg("#255,255,255 %s : 맥주를 마셨다. %s" %(username, tomsg))
	if str(choice) == "34":
		tomsg = random.choice(["다 마셨다간 취할거 같다.", "뭔가 머리가 어지럽다."])
		esc.msg("#255,255,255 %s : 청주를 마셨다. %s" %(username, tomsg))
	if str(choice) == "35":
		tomsg = random.choice(["무심코 맛있다 라고 말했다.", "순식간에 음식을 해치워버렸다.(...)"])
		esc.msg("#255,255,255 %s : 맥주를 마셨다. %s" %(username, tomsg))
	if str(choice) == "38":
		tomsg = "#255,0,0페리의 인형을 버렸다."
		esc.msg("#255,255,255 %s : %s" %(username, tomsg))

def inventory_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	skill_menu = popuplib.easymenu('skill_l_%s' %(userid), None, itemuse_select)
	realname = ITEM_LIST[choice]['itemrealname']
	skill_menu.settitle("＠ %s" %(realname))
	info = ITEM_LIST[choice]['info']
	level_info = ITEM_LIST[choice]['effect_info']
	skill_menu.setdescription(" \n%s\n%s" %(info, level_info))
	skill_menu.addoption(choice, "%s 아이템을 사용합니다." %(realname))
	skill_menu.send(userid)
	popuplib.delete('skill_l_%s' %(userid))

def skill_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	skill_menu = popuplib.easymenu('skill_l_%s' %(userid), None, none_select)
	skill_menu.settitle("＠ %s" %(choice))
	client_skill = es.keygetvalue(steamid, "player_data", SKILL_TEST[choice]['skillname'])
	need_skillp = SKILL_TEST[choice]['need_skillp']
	max = SKILL_TEST[choice]['max']
	info = SKILL_TEST[choice]['info']
	level_info = SKILL_TEST[choice]['level_info']
	sb = SKILL_TEST[choice]['skillbook']
	if sb == -1: sbz = "없음"
	else:
		sbz = ITEM_LIST[str(sb)]['itemrealname']
	skill_menu.setdescription(" \n＊ 필요한 스킬북 : %s\n＊ 필요한 스킬 포인트 : %s\n＊ 스킬 현황 : %s / %s\n \n%s\n%s" %(sbz, need_skillp, client_skill, max, info, level_info))
	skill_menu.addoption(choice, "%s 스킬을 익힙니다." %(choice))
	skill_menu.menuselect = learnskill_select
	skill_menu.send(userid)
	popuplib.delete('skill_l_%s' %(userid))


def mskill_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	skill_menu = popuplib.easymenu('skill_l_%s' %(userid), None, none_select)
	skill_menu.settitle("＠ %s" %(choice))
	client_skill = es.keygetvalue(steamid, "player_data", MASTERY_SKILLS[choice]['skillname'])
	need_skillp = MASTERY_SKILLS[choice]['need_masteryxp']
	max = MASTERY_SKILLS[choice]['max']
	info = MASTERY_SKILLS[choice]['info']
	level_info = MASTERY_SKILLS[choice]['level_info']
	sb = MASTERY_SKILLS[choice]['skillbook']
	if sb == -1: sbz = "없음"
	else:
		sbz = ITEM_LIST[str(sb)]['itemrealname']
	skill_menu.setdescription(" \n＊ 필요한 스킬북 : %s\n＊ 필요한 스킬 포인트 : %s\n＊ 스킬 현황 : %s / %s\n \n%s\n%s" %(sbz, need_skillp, client_skill, max, info, level_info))
	skill_menu.addoption(choice, "%s 스킬을 익힙니다." %(choice))
	skill_menu.menuselect = learnmskill_select
	skill_menu.send(userid)
	popuplib.delete('skill_l_%s' %(userid))


def masterymenu_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == "send_mastery_1": mastery_1.send(userid)
	if choice == "send_mastery_2": mastery_2.send(userid)
	if choice == "send_mastery_3": mastery_3.send(userid)
	if choice == "send_mastery_4": mastery_4.send(userid)
	if choice == "send_mastery_5": mastery_5.send(userid)
	if choice == "send_mastery_6": mastery_6.send(userid)
	if choice == "마스터리 스킬":
		skillmenu = popuplib.easymenu('mskill_%s' %(userid), None, mskill_select)
		skillmenu.settitle("＠ 마스터리 스킬 메뉴")
		skillmenu.c_endsep = " \n○ 원하는 마스터리 스킬을 선택하세요\n "
		for a in MASTERY_SKILLS:
			him_mastery = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
			gm_skill = int(MASTERY_SKILLS[a]['mastery_what'])
			if gm_skill == him_mastery:
				get_skill = int(es.keygetvalue(steamid, "player_data", MASTERY_SKILLS[a]['skillname']))
				get_state = 1
				if get_skill >= MASTERY_SKILLS[a]['max']: get_state = 0
				if int(es.keygetvalue(steamid, "player_data", "mastery_xp")) < MASTERY_SKILLS[a]['need_masteryxp']: get_state = 0
				skillmenu.addoption(a, "%s [%s/%s] - %s Mastery XP" %(a, get_skill, MASTERY_SKILLS[a]['max'], MASTERY_SKILLS[a]['need_masteryxp']), get_state)
		skillmenu.send(userid)
		popuplib.delete('mskill_%s' %(userid))

def targetmenu_select(userid, choice, popupname):
	choice_args = choice.split()
	steamid = str(choice_args[0])
	username = es.keygetvalue(steamid, "player_data", "username")
	if choice_args[1] == "스킬":
		skillmenu = popuplib.easymenu('skill_%s' %(userid), None, skill_select)
		skillmenu.settitle("＠ 스킬 메뉴")
		skillmenu.c_endsep = " \n%s님의 스킬\n " %(username)
		for a in SKILL_TEST:
			get_skill = int(es.keygetvalue(steamid, "player_data", SKILL_TEST[a]['skillname']))
			if get_skill > 0:
				skillmenu.addoption(a, "%s [%s/%s]" %(a, get_skill, SKILL_TEST[a]['max']), 0)
		skillmenu.send(userid)
		popuplib.delete('skill_%s' %(userid))
	if choice_args[1] == "스텟":
		skillmenu = popuplib.easymenu('skill_%s' %(userid), None, stet_select)
		skillmenu.settitle("＠ 스텟 메뉴")
		skillmenu.c_endsep = " \n%s님의 스텟\n " %(username)
		get_check = 1
		while get_check <= 6:
			for a in STET_LIST:
				if STET_LIST[a]['list'] == get_check:
					get_check += 1
					get_skill = es.keygetvalue(steamid, "player_data", STET_LIST[a]['stetname'])
					get_state = 1
					if int(es.keygetvalue(steamid, "player_data", "stetpoint")) < 1: get_state = 0
					skillmenu.addoption(a, "%s : %s" %(a, get_skill), get_state)
		skillmenu.send(userid)
		popuplib.delete('skill_%s' %(userid))
	if choice_args[1] == "인벤토리":
		skillmenu = popuplib.easymenu('skill_%s' %(userid), None, inventory_select)
		skillmenu.settitle("＠ 인벤토리 메뉴")
		skillmenu.c_endsep = " \n%s님의 인벤토리\n " %(username)
		for a in ITEM_LIST:
			get_skill = int(es.keygetvalue(steamid, "player_data", ITEM_LIST[a]['itemkeyname']))
			if get_skill > 0:
				get_state = ITEM_LIST[a]['duse']
				name = ITEM_LIST[a]['itemrealname']
				skillmenu.addoption(a, "(%s)%s : %s" %(a, name, get_skill), 0)
		skillmenu.send(userid)
		popuplib.delete('skill_%s' %(userid))

def ranking_select(userid, choice, popupname):
	steamid = choice[1]
	skillmenu = popuplib.easymenu('info_%s' %(userid), None, targetmenu_select)
	skillmenu.settitle("＠ 정보")
	skillmenu.addoption("%s 스킬" %(steamid), "스킬 보기")
	skillmenu.addoption("%s 스텟" %(steamid), "스텟 보기")
	skillmenu.addoption("%s 인벤토리" %(steamid), "인벤토리 보기")
	skillmenu.send(userid)
	popuplib.delete('info_%s' %(userid))

def rpgmenu_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == "스킬":
		skillmenu = popuplib.easymenu('skill_%s' %(userid), None, skill_select)
		skillmenu.settitle("＠ 스킬 메뉴")
		skillmenu.c_endsep = " \n○ 원하는 스킬을 선택하세요\n "
		for a in SKILL_TEST:
			skillbook = SKILL_TEST[a]['skillbook']
			if skillbook == -1:
				get_skill = int(es.keygetvalue(steamid, "player_data", SKILL_TEST[a]['skillname']))
				get_state = 1
				if get_skill >= SKILL_TEST[a]['max']: get_state = 0
				if int(es.keygetvalue(steamid, "player_data", "skillpoint")) < SKILL_TEST[a]['need_skillp']: get_state = 0
				skillmenu.addoption(a, "%s [%s/%s] - %s SP" %(a, get_skill, SKILL_TEST[a]['max'], SKILL_TEST[a]['need_skillp']), get_state)
			else:
				item_name = ITEM_LIST[str(skillbook)]['itemkeyname']
				skillbook_get = int(es.keygetvalue(steamid, "player_data", item_name))
				if skillbook_get > 0:
					get_skill = int(es.keygetvalue(steamid, "player_data", SKILL_TEST[a]['skillname']))
					get_state = 1
					if get_skill >= SKILL_TEST[a]['max']: get_state = 0
					if int(es.keygetvalue(steamid, "player_data", "skillpoint")) < SKILL_TEST[a]['need_skillp']: get_state = 0
					skillmenu.addoption(a, "%s [%s/%s] - %s SP" %(a, get_skill, SKILL_TEST[a]['max'], SKILL_TEST[a]['need_skillp']), get_state)
		skillmenu.send(userid)
		popuplib.delete('skill_%s' %(userid))
	if choice == "스텟":
		skillmenu = popuplib.easymenu('skill_%s' %(userid), None, stet_select)
		skillmenu.settitle("＠ 스텟 메뉴")
		skillmenu.c_endsep = " \n○ 원하는 스텟을 선택하세요\n "
		get_check = 1
		while get_check <= 6:
			for a in STET_LIST:
				if STET_LIST[a]['list'] == get_check:
					get_check += 1
					get_skill = es.keygetvalue(steamid, "player_data", STET_LIST[a]['stetname'])
					get_state = 1
					if int(es.keygetvalue(steamid, "player_data", "stetpoint")) < 1: get_state = 0
					skillmenu.addoption(a, "%s : %s" %(a, get_skill), get_state)
		skillmenu.send(userid)
		popuplib.delete('skill_%s' %(userid))
	if choice == "인벤토리":
		skillmenu = popuplib.easymenu('skill_%s' %(userid), None, inventory_select)
		skillmenu.settitle("＠ 인벤토리 메뉴")
		skillmenu.c_endsep = " \n○ 사용할 아이템을 선택하세요\n "
		for a in ITEM_LIST:
			get_skill = int(es.keygetvalue(steamid, "player_data", ITEM_LIST[a]['itemkeyname']))
			if get_skill > 0:
				get_state = ITEM_LIST[a]['duse']
				name = ITEM_LIST[a]['itemrealname']
				skillmenu.addoption(a, "(%s)%s : %s" %(a, name, get_skill), get_state)
		skillmenu.send(userid)
		popuplib.delete('skill_%s' %(userid))

def mastery_1_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == 1:
		if item_get(steamid, 'mastery_select') == 0:
			if item_get(steamid, 'item1') >= 75:
				if item_get(steamid, 'level') >= 10:
					keymath(steamid, "player_data", "item1", "-", 75)
					es.keysetvalue(steamid, "player_data", "mastery_select", 1)
					es.keysetvalue(steamid, "player_data", "mastery_list", "glock, usp, p228, deagle, elite, fiveseven")
					name = es.getplayername(userid)
					esc.msg('#blue %s 유저#255,255,255님이#gold 권총 마스터리#255,255,255를 선택하셨습니다.' %(name))

def mastery_2_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == 1:
		if item_get(steamid, 'mastery_select') == 0:
			if item_get(steamid, 'item1') >= 50:
				if item_get(steamid, 'item13') >= 200:
					if item_get(steamid, 'item3') >= 1:
						if item_get(steamid, 'level') >= 10:
							keymath(steamid, "player_data", "item1", "-", 50)
							keymath(steamid, "player_data", "item13", "-", 200)
							keymath(steamid, "player_data", "item3", "-", 1)
							es.keysetvalue(steamid, "player_data", "mastery_select", 2)
							es.keysetvalue(steamid, "player_data", "mastery_list", "knife")
							name = es.getplayername(userid)
							esc.msg('#blue %s 유저#255,255,255님이#gold 소드 마스터리#255,255,255를 선택하셨습니다.' %(name))

def mastery_3_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == 1:
		if item_get(steamid, 'mastery_select') == 0:
			if item_get(steamid, 'item3') >= 12:
				if item_get(steamid, 'item4') >= 12:
					if item_get(steamid, 'item25') >= 8:
						if item_get(steamid, 'level') >= 10:
							keymath(steamid, "player_data", "item3", "-", 12)
							keymath(steamid, "player_data", "item4", "-", 12)
							keymath(steamid, "player_data", "item25", "-", 8)
							es.keysetvalue(steamid, "player_data", "mastery_select", 3)
							es.keysetvalue(steamid, "player_data", "mastery_list", "tmp mac10 mp5navy ump45 p90 m249 awp scout")
							name = es.getplayername(userid)
							esc.msg('#blue %s 유저#255,255,255님이#gold 서포트 마스터리#255,255,255를 선택하셨습니다.' %(name))



def tenji_1_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	choice = int(choice)
	if choice == 1:
		if item_get(steamid, "cs") >= 15:
			keymath(steamid, "player_data", "cs", "-", 15)
			keymath(steamid, "player_data", "item33", "+", 1)
	if choice == 2:
		if item_get(steamid, "cs") >= 30:
			keymath(steamid, "player_data", "cs", "-", 30)
			keymath(steamid, "player_data", "item34", "+", 1)
	if choice == 3:
		if item_get(steamid, "cs") >= 30:
			keymath(steamid, "player_data", "cs", "-", 30)
			keymath(steamid, "player_data", "item35", "+", 1)

def event_1_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	choice = int(choice)
	if choice == 1:
		if item_get(steamid, "item1") >= 10:
			keymath(steamid, "player_data", "item1", "-", 10)
			keymath(steamid, "player_data", "item10", "+", 1)
	if choice == 2:
		if item_get(steamid, "cs") >= 1:
			keymath(steamid, "player_data", "cs", "-", 1)
			keymath(steamid, "player_data", "item17", "+", 1)
	if choice == 3:
		if item_get(steamid, "connect_point") >= 100:
			keymath(steamid, "player_data", "connect_point", "-", 100)
			keymath(steamid, "player_data", "xp", "+", 1)
	if choice == 4:
		if item_get(steamid, "connect_point") >= 1000:
			keymath(steamid, "player_data", "connect_point", "-", 1000)
			keymath(steamid, "player_data", "xp", "+", 15)
	if choice == 5:
		if item_get(steamid, "connect_point") >= 10000:
			keymath(steamid, "player_data", "connect_point", "-", 10000)
			keymath(steamid, "player_data", "xp", "+", 175)
	if choice == 6:
		if item_get(steamid, "cs") >= 10:
			keymath(steamid, "player_data", "cs", "-", 10)
			keymath(steamid, "player_data", "item6", "+", 1)
	if choice == 7:
		if item_get(steamid, "connect_point") >= 100000:
			keymath(steamid, "player_data", "connect_point", "-", 100000)
			keymath(steamid, "player_data", "xp", "+", 2500)
	if choice == 8:
		if item_get(steamid, "cs") >= 15:
			keymath(steamid, "player_data", "cs", "-", 15)
			keymath(steamid, "player_data", "item17", "+", 1)
	if choice == 9:
		if item_get(steamid, "cs") >= 25:
			keymath(steamid, "player_data", "cs", "-", 25)
			keymath(steamid, "player_data", "item18", "+", 1)
	if choice == 10:
		if item_get(steamid, "cs") >= 10:
			keymath(steamid, "player_data", "cs", "-", 10)
			keymath(steamid, "player_data", "item23", "+", 1)
	if choice == 11:
		if item_get(steamid, "cs") >= 25:
			keymath(steamid, "player_data", "cs", "-", 25)
			keymath(steamid, "player_data", "item16", "+", 1)

def monster_menuselect(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == 1:
		if classname_get(steamid, 'classname') == "human":
			if item_get(steamid, 'item19') >= 4:
				if item_get(steamid, 'level') == item_get(steamid, 'stetpoint'):
					keymath(steamid, "player_data", "item19", "-", 4)
					es.keysetvalue(steamid, "player_data", "classname", "monster")
					name = es.getplayername(userid)
					esc.msg('#blue %s 유저#255,255,255님이#255,55,55 요괴#255,255,255로 종족을 변경하셨습니다.' %(name))

def fairy_menuselect(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if choice == 1:
		if classname_get(steamid, 'classname') == "human":
			if item_get(steamid, 'item1') >= 100:
				if item_get(steamid, 'item3') >= 1:
					if item_get(steamid, 'item4') >= 1:
						if item_get(steamid, 'level') == item_get(steamid, 'stetpoint'):
							keymath(steamid, "player_data", "item1", "-", 100)
							keymath(steamid, "player_data", "item3", "-", 1)
							keymath(steamid, "player_data", "item4", "-", 1)
							es.keysetvalue(steamid, "player_data", "classname", "fairy")
							name = es.getplayername(userid)
							esc.msg('#blue %s 유저#255,255,255님이#0,255,255 요정#255,255,255으로 종족을 변경하셨습니다.' %(name))

def chat_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	code = str(es.keygetvalue(steamid, "player_data", "code"))
	level = int(es.keygetvalue(steamid, "player_data", "level"))
	if "chat_cirno_" in popupname:
		if choice == 1:
			if int(es.keygetvalue(steamid, "player_data", "item9")) > 2:
				if int(es.keygetvalue(steamid, "player_data", "classname_skill1")) == 0:
					keymath(steamid, "player_data", "item9", "-", 3)
					keymath(steamid, "player_data", "classname_skill1", "+", 1)
				else: esc.tell(userid, "#255,255,255스킬이 이미 최대치입니다.")
			else:
				es.server.cmd('kickid %s "부정행위 금지"' %(userid))
	if "chat_nosay_" in popupname:
		if choice == 1:
			if int(es.keygetvalue(steamid, "player_data", "item19")) > 0:
				keymath(steamid, "player_data", "item19", "-", 1)
				keymath(steamid, "player_data", "npc_nosay_nightfever_xp", "+", 1)
				esc.tell(userid, "#255,255,255당신이 건넨 암흑 크리스탈을 받고는. 옥시는 감사의 인사를 전했다.")
				esc.tell(userid, "#gold그녀는 당신에 대한 호감도가 올라갔습니다.")
			else:
				es.server.cmd('kickid %s "부정행위 금지"' %(userid))
	if "chat_chall" in popupname:
		if choice == 1:
			if int(es.keygetvalue(steamid, "player_data", "item16")) > 0:
				keymath(steamid, "player_data", "item16", "-", 1)
				npc_msg("#125,125,125Dark Teleporter", "잘 다녀오도록, 친구들.")
				#es.server.cmd('sm_votemap de_season ze_FFVII_Mako_Reactor_v5_3 ze_FFXII_Westersand_v7_2 ze_predator_ultimate_v3')
				es.server.cmd('sm_votemap de_season de_season ze_predator_ultimate_v3 ze_FFXII_Westersand_v7_2')
				es.set("nightfever_time", 999999)
			else: es.server.cmd('kickid %s "부정행위 금지"' %(userid))
		if choice == 2:
			if int(es.keygetvalue(steamid, "player_data", "item16")) > 0:
				keymath(steamid, "player_data", "item16", "-", 1)
				es.set("human_target", userid)
				npc_msg("#125,125,125Dark Teleporter", "잘 다녀오도록, 행운을 빈다.")
				es.server.cmd('sm_votemap cs_gentech_final cs_gentech_final')
				es.set("nightfever_time", 999999)
			else: es.server.cmd('kickid %s "부정행위 금지"' %(userid))
		if choice == 3:
			if int(es.keygetvalue(steamid, "player_data", "item16")) > 0:
				keymath(steamid, "player_data", "item16", "-", 1)
				es.set("human_target", userid)
				npc_msg("#125,125,125Dark Teleporter", "잘 다녀오도록, 행운을 빈다.")
				es.server.cmd('sm_votemap cs_office cs_office')
				es.set("nightfever_time", 999999)
			else: es.server.cmd('kickid %s "부정행위 금지"' %(userid))
	if "chat_reisen" in popupname:
		if choice == 1:
			if int(es.keygetvalue(steamid, "player_data", "item12")) > 0:
				keymath(steamid, "player_data", "item12", "-", 1)
				esc.tell(userid, "#255,255,255당신이 건넨 맥주를 그녀는 거부했다.")
				esc.tell(userid, "#255,255,255강제로 건네려고 하자, 맥주의 병은 산산조각이 나고 말았다.")
				esc.tell(userid, "#255,125,125그녀는 당신에 대한 호감도가 내려갔습니다.")
				keymath(steamid, "player_data", "npc_reisen_nightfever_xp", "-", 1)
			else: es.server.cmd('kickid %s "부정행위 금지"' %(userid))
	if "chat_2" in popupname:
		if choice == 1:
			if int(es.keygetvalue(steamid, "player_data", "item12")) > 0:
				esc.tell(userid, "#255,255,255그는 당신이 건넨 맥주를 거지마냥 벌컥벌컥 마시기 시작했다.")
				esc.tell(userid, "#gold그는 당신에 대한 호감도가 올라갔습니다.")
				keymath(steamid, "player_data", "npc_beer_nightfever_xp", "+", 1)
				keymath(steamid, "player_data", "item12", "-", 1)
				npc_xp = int(es.keygetvalue(steamid, "player_data", "npc_beer_nightfever_xp"))
				if npc_xp > 0:
					esc.tell(userid, "#255,255,255??? :#default 아... 예전 이야기를 들려줄게.")
					esc.tell(userid, "#255,255,255??? :#default 내 외삼춘은 말이지 함자가 영 자. 봉 자야. 영봉이 삼춘이 신의주 어데 살고 있지 않간?")
					esc.tell(userid, "#255,255,255??? :#default 왜 그케 됬냐 하면은, 그때 내 막내 이모가 먹을게 없어 죽지 않았간..?")
					esc.tell(userid, "#255,255,255??? :#default 바람벽 흙을 파먹다 말이지. 그래 외삼춘이 분연히 떨쳐 일어나 말하길")
					esc.tell(userid, "#255,255,255???(외삼촌) :#default 누이, 난 여기서 더는 못살겠소. 나는 강 건너로 갑네다.")
					esc.tell(userid, "#255,255,255??? :#default 하구선 떠났단 말이지. 내가 여길 오기 전에 배가 아주 곤란을 겪고 있을 적인데,")
					esc.tell(userid, "#255,255,255??? :#default 이 이자카야에서 외삼춘을 만났지 않았갔어? 아주 기적이였지이.")
					esc.tell(userid, "#255,255,255??? :#default 수십 차례 보낸 편지 중에 한 편지가 드디어 외삼춘한테 닿았던 거야, 아, 우리 외삼춘두 차암. 하하하.")
			else: es.server.cmd('kickid %s "부정행위 금지"' %(userid))
	if "chat_1_" in popupname:
		if choice == 1:
			esc.tell(userid, "#255,255,255Kuria :#default 코드요? %s아닌가요? 내가 잘못봤나~?" %(code))
def load():
	global lasermodel
	if "_" in map():
		lasermodel = es.precachemodel("effects/laser1.vmt")
	es.set("remote_enable", 0)
	es.set("remote_forwardmove", 0)
	es.set("remote_sidemove", 0)
	es.set("remote_fire", 0)
	es.set("remote_firek", 0)
	es.set("remote_duck", 0)
	es.set("remote_jump", 0)
	es.set("remote_forwardmove2", 0)
	es.set("remote_sidemove2", 0)
	es.set("remote_fire2", 0)
	es.set("remote_firek2", 0)
	es.set("remote_duck2", 0)
	es.set("remote_jump2", 0)
	spe.parseINI("rpg/sig.ini")
	es.set("test", -998)
	es.dbgmsg(0, "dbug")
	#spe.detourFunction("PlayerRunCommand", spe.HookType.Pre, PrePlayerRunCommand)
	#spe.detourFunction("UpKeep", spe.HookType.Pre, PreBotHide)
	#spe.detourFunction("Noise", spe.HookType.Pre, PreNoise)
	#spe.detourFunction("Update", spe.HookType.Pre, PreBotHide)
	global POKER_PLAYER_LIST
	global POKER_CARD_LIST
	POKER_PLAYER_LIST = []
	POKER_CARD_LIST = []
	global monster_1
	monster_1 = popuplib.create('monster_1')
	monster_1.addline(" ")
	monster_1.addline("＠ 요괴")
	monster_1.addline(" ")
	monster_1.addline("＠ 데미지 20％ 증가")
	monster_1.addline("＠ 아이템 '요정' 사용 가능")
	monster_1.addline(" ")
	monster_1.addline("※ 현재 스킬/스텟 초기화된 상태여야함")
	monster_1.addline("※ 종족이 인간이여야함.")
	monster_1.addline(" ")
	monster_1.addline("＊ 암흑 크리스탈 4개 필요")
	monster_1.addline(" ")
	monster_1.addline("->1. 종족을 요괴로 변환합니다.")
	monster_1.addline(" ")
	monster_1.menuselect = monster_menuselect
	global cirno_1
	cirno_1 = popuplib.create('cirno_1')
	cirno_1.addline(" ")
	cirno_1.addline("＠ 요정")
	cirno_1.addline(" ")
	cirno_1.addline("＠ 중력 변화")
	cirno_1.addline("＠ J키로 바리케이드를 건설가능")
	cirno_1.addline(" ")
	cirno_1.addline("※ 현재 스킬/스텟 초기화된 상태여야함")
	cirno_1.addline("※ 종족이 인간이여야함.")
	cirno_1.addline(" ")
	cirno_1.addline("＊ 크리스탈 100개 필요")
	cirno_1.addline("＊ 요정의 씨앗 1개 필요")
	cirno_1.addline("＊ 요정의 샘물 1개 필요")
	cirno_1.addline(" ")
	cirno_1.addline("->1. 종족을 요정으로 변환합니다.")
	cirno_1.addline(" ")
	cirno_1.menuselect = fairy_menuselect
	global mastery_1
	mastery_1 = popuplib.create('mastery_1')
	mastery_1.addline(" ")
	mastery_1.addline("＠ 권총 마스터리")
	mastery_1.addline(" ")
	mastery_1.addline("★ 대표 스킬 : 폭발탄, 크리티컬")
	mastery_1.addline("☆ Glock, Usp, P228, Deagle, Elite, Fiveseven")
	mastery_1.addline("＊ 크리스탈 75개 필요")
	mastery_1.addline("＊ 레벨 10 이상, 마스터리 : 없음 보유")
	mastery_1.addline(" ")
	mastery_1.addline("“권총 마스터리라... 유럽 쪽이 유행하고 있지.”")
	mastery_1.addline("“데미지 하나는 장난 아니야, 운 좋으면 헤드에 2500 데미지, ... 이상해?”")
	mastery_1.addline("- Kasto(마스터리의 재능자)")
	mastery_1.addline(" ")
	mastery_1.addline("->1. 권총 마스터리를 익힌다.")
	mastery_1.addline(" ")
	mastery_1.menuselect = mastery_1_select
	global mastery_2
	mastery_2 = popuplib.create('mastery_2')
	mastery_2.addline(" ")
	mastery_2.addline("＠ 소드 마스터리")
	mastery_2.addline(" ")
	mastery_2.addline("★ 대표 스킬 : 익스플로전 소드")
	mastery_2.addline("☆ Knife")
	mastery_2.addline("＊ 크리스탈 50개, 적의 목 200개, 요정의 샘물 1개 필요")
	mastery_2.addline("＊ 레벨 10 이상, 마스터리 : 없음 보유")
	mastery_2.addline(" ")
	mastery_2.addline("“소드 마스터리? 콱콱 죽이는 재미를 알고있어?”")
	mastery_2.addline("“상남자라면 당연히 추천하지! 한번 상남자라면 해보라고!”")
	mastery_2.addline("- Kasto(마스터리의 재능자)")
	mastery_2.addline(" ")
	mastery_2.addline("->1. 소드 마스터리를 익힌다.")
	mastery_2.addline(" ")
	mastery_2.menuselect = mastery_2_select
	global mastery_3
	mastery_3 = popuplib.create('mastery_3')
	mastery_3.addline(" ")
	mastery_3.addline("＠ 서포트 마스터리")
	mastery_3.addline(" ")
	mastery_3.addline("★ 대표 스킬 : 의사")
	mastery_3.addline("☆ Tmp, Mac10, Mp5navy, Ump45, P90, M249, AWP, Scout")
	mastery_3.addline("＊ 요정의 샘물 12개, 요정의 씨앗 12개, 천사의 날개 8개 필요")
	mastery_3.addline("＊ 레벨 10 이상, 마스터리 : 없음 보유")
	mastery_3.addline(" ")
	mastery_3.addline("“서포트 마스터리, 없으면 안되. 절대로.”")
	mastery_3.addline("“없다면 플레이 하는데 매우 힘들어질거야. 내가 경험했어.”")
	mastery_3.addline("- Kasto(마스터리의 재능자)")
	mastery_3.addline(" ")
	mastery_3.addline("->1. 서포트 마스터리를 익힌다.")
	mastery_3.addline(" ")
	mastery_3.menuselect = mastery_3_select
	#mastery_3.send(280)
	global mastery_4
	mastery_4 = popuplib.create('mastery_4')
	mastery_4.addline(" ")
	mastery_4.addline("＠ 샷건 마스터리")
	mastery_4.addline(" ")
	mastery_4.addline("★ 대표 스킬 : 크리티컬 익스플로전")
	mastery_4.addline("☆ Knife")
	mastery_4.addline("＊ 크리스탈 100개, 암흑 크리스탈 10개")
	mastery_4.addline("＊ 레벨 10 이상, 마스터리 : 없음 보유")
	mastery_4.addline(" ")
	mastery_4.addline("“그냥 분쇄기라고 말하면 말이 편하겠군.”")
	mastery_4.addline("“싹다 갈아버린다고, 싹다.”")
	mastery_4.addline("- Kasto(마스터리의 재능자)")
	mastery_4.addline(" ")
	mastery_4.addline("->1. 샷건 마스터리를 익힌다.")
	mastery_4.addline(" ")
	mastery_4.menuselect = mastery_2_select
	global event_1
	event_1 = popuplib.easymenu('event_1', None, event_1_select)
	event_1.settitle("＠ 아이템 판매 이벤트")
	event_1.c_endsep = " \n○ 곧 아이템이 변경예정입니다.\n "
	event_1.addoption(2, "1 CS → 크리스탈(1.6일까지)", 0)
	event_1.addoption(1, "10 크리스탈 → 양말(1.1일까지)", 0)
	event_1.addoption(3, "100 접속 포인트 → 1 경험치")
	event_1.addoption(4, "1000 접속 포인트 → 15 경험치")
	event_1.addoption(5, "10000 접속 포인트 → 175 경험치")
	event_1.addoption(6, "10 CS → 테이지의 약물")
	event_1.addoption(7, "100000 접속 포인트 → 2500 경험치", 1)
	event_1.addoption(8, "15 CS → 떡국(1.31일까지)")
	event_1.addoption(9, "25 CS → 파트너 계약서")
	event_1.addoption(10, "10 CS → 수수께끼의 마도서(1.12일까지)", 0)
	event_1.addoption(11, "25 CS → 이벤트 티켓")
	global tenji_1
	tenji_1 = popuplib.easymenu('tenji_1', None, tenji_1_select)
	tenji_1.settitle("＠ Tenji")
	tenji_1.c_endsep = " \nTenji : 내가 자랑하는 탄막들이 많지, 마음껏 즐겨보게.\n "
	tenji_1.addoption(1, "15 CS → 맥주", 1)
	tenji_1.addoption(2, "30 CS → 청주", 1)
	tenji_1.addoption(3, "30 CS → 야키토리", 1)
	global rpgmenu
	rpgmenu = popuplib.easymenu('rpgmenu', None, rpgmenu_select)
	rpgmenu.settitle("＠ RPG 메뉴")
	rpgmenu.c_endsep = " \n○ RPG의 기능들을 확인해보세요.\n "
	rpgmenu.addoption("스킬", "스킬")
	rpgmenu.addoption("스텟", "스텟")
	rpgmenu.addoption("인벤토리", "인벤토리")
	global masterymenu
	masterymenu = popuplib.easymenu('masterymenu', None, masterymenu_select)
	masterymenu.settitle("＠ 마스터리 메뉴")
	masterymenu.c_endsep = " \n○ 마스터리의 기능들을 확인해보세요.\n "
	masterymenu.addoption("마스터리 스킬", "마스터리 스킬")
	masterymenu.addoption("send_mastery_1", "권총 마스터리")
	masterymenu.addoption("send_mastery_2", "소드 마스터리")
	masterymenu.addoption("send_mastery_3", "서포트 마스터리", 1)
	masterymenu.addoption("send_mastery_4", "샷건 마스터리", 0)
	es.set("eventscripts_noisy", 0)
	cmdlib.registerServerCommand('r_makechat', makechat, 'eee')
	cmdlib.registerServerCommand('r_unlock', unlock, 'eee')
	cmdlib.registerServerCommand('r_music', fuckmusic, 'eee')
	cmdlib.registerServerCommand('r_giveall', giveall, 'eee')
	cmdlib.registerServerCommand('r_weaponreload', weaponreload, 'eee')
	cmdlib.registerServerCommand('r_weaponswap', weaponswap, 'eee')
	cmdlib.registerServerCommand('r_weaponfire', weaponfire, 'eee')
	cmdlib.registerServerCommand('r_footstep', player_footstep, 'eee')
	cmdlib.registerServerCommand('r_bulletimpact', bulletimpact, 'eee')
	#cmdlib.registerServerCommand('r_bulletimpact', , 'eee')
	cmdlib.registerServerCommand('r_spotted', spotted, 'eee')
	cmdlib.registerServerCommand('r_autobuy', autobuy_command, 'eee')
	cmdlib.registerServerCommand('r_rebuy', rebuy_command, 'eee')
	cmdlib.registerServerCommand('r_givecs', givecs, 'eee')
	cmdlib.registerServerCommand('r_givecode', givecode, 'eee')
	cmdlib.registerServerCommand('r_storymsg', storymsg, 'eee')
	global nipper_timer
	nipper_timer = repeat.create('nipper_timer', nipper_timer, ())
	global zombie_select_timer
	zombie_select_timer = repeat.create('zombie_select_timer', zombie_select, ())
	global keyhint
	keyhint = repeat.create('keyhint', send_keyhint, ())
	keyhint.start(1, 99999999999999999999999999999)
	es.addons.registerTickListener(ticklistener)
	check = es.exists("variable", "level")
	if check == 0: es.set("level", 1)
	check = es.exists("variable", "soundtrack")
	if check == 0: es.set("soundtrack", 0)
	check = es.exists("variable", "allfade")
	if check == 0: es.set("allfade", 0)
	check = es.exists("variable", "event_line")
	if check == 0: es.set("event_line", 0)
	check = es.exists("variable", "zeisen_gun")
	if check == 0: es.set("zeisen_gun", 0)
	check = es.exists("variable", "nightfever_time")
	if check == 0: es.set("nightfever_time", 300)
	check = es.exists("variable", "players_count")
	if check == 0: es.set("players_count", 0)
	check = es.exists("variable", "what_ent")
	if check == 0: es.set("what_ent", 0)
	check = es.exists("variable", "nipper_count")
	if check == 0: es.set("nipper_count", 0)
	check = es.exists("variable", "server_start")
	if check == 0: es.set("server_start", 1)
	check = es.exists("variable", "poker_begin")
	if check == 0: es.set("poker_begin", 0)
	check = es.exists("variable", "poker_blind_min")
	if check == 0: es.set("poker_blind_min", 0)
	check = es.exists("variable", "poker_blind_max")
	if check == 0: es.set("poker_blind_max", 0)
	check = es.exists("variable", "poker_cost")
	if check == 0: es.set("poker_cost", 0)
	es.addons.registerSayFilter(sayFilter)
	global zombie_timer
	zombie_timer = repeat.create('zombie_timer', zombie_select, ())
	spe.registerPreHook('player_hurt', pre_player_hurt)
	es.addons.registerClientCommandFilter(Commander4)
	if "_" in map():
		global knife_model_1
		knife_model_1 = es.precachemodel("models/weapons/w_fire_rapier.mdl")
	check = es.exists("keygroup", "server")
	if check == 0:
		es.keygroupload("server", "|rpg/server_data")
	else:
		es.keygroupsave("server", "|rpg/server_data")
		es.keygroupdelete("server")
		es.keygroupload("server", "|rpg/server_data")
	global sayok
	sayok = {}
	global totaldamage
	totaldamage = {}
	global fdamage
	fdamage = {}
	global fcri
	fcri = {}
	global spec_time
	spec_time = {}
	global max_health
	max_health = {}
	for a in playerlib.getPlayerList("#human"):
		sayok[a.userid] = 1
		fcri[a.userid] = 0
		fdamage[a.userid] = 0
		totaldamage[a.userid] = 0
		spec_time[a.userid] = 0
	for f_userid in es.getUseridList():
		max_health[f_userid] = 0
		max_health[f_userid] = int(sv('max_health_%s' %(f_userid)))

def unload():
	cmdlib.unregisterServerCommand('r_makechat')
	cmdlib.unregisterServerCommand('r_unlock')
	cmdlib.unregisterServerCommand('r_music')
	cmdlib.unregisterServerCommand('r_giveall')
	cmdlib.unregisterServerCommand('r_weaponreload')
	cmdlib.unregisterServerCommand('r_weaponswap')
	cmdlib.unregisterServerCommand('r_weaponfire')
	cmdlib.unregisterServerCommand('r_footstep')
	cmdlib.unregisterServerCommand('r_bulletimpact')
	cmdlib.unregisterServerCommand('r_autobuy')
	cmdlib.unregisterServerCommand('r_rebuy')
	cmdlib.unregisterServerCommand('r_spotted')
	cmdlib.unregisterServerCommand('r_givecs')
	cmdlib.unregisterServerCommand('r_givecode')
	cmdlib.unregisterServerCommand('r_storymsg')
	repeat.delete('keyhint')
	repeat.delete('nipper_timer')
	repeat.delete('zombie_timer')
	es.addons.unregisterSayFilter(sayFilter)
	es.addons.unregisterClientCommandFilter(Commander4)
	es.addons.unregisterTickListener(ticklistener)
	#spe.undetourFunction("PlayerRunCommand", spe.HookType.Pre, PrePlayerRunCommand)
	#spe.undetourFunction("Update", spe.HookType.Pre, PreBotHide)
	#spe.undetourFunction("Noise", spe.HookType.Pre, PreNoise)
	#spe.undetourFunction("UpKeep", spe.HookType.Pre, PreBotHide)
	spe.unregisterPreHook('player_hurt', pre_player_hurt)
	for a in es.getUseridList():
		if es.getplayerteam(a) > 1:
			es.set("max_health_%s" %(a), max_health[a])

def nz():
	get_item(7, "item38", "#255,0,0페리의 인형", 1)

def get_userid_from_handle(ptr):
	for userid in es.getUseridList():
		if es.getplayerhandle(userid) == ptr:
			return userid
	return None

def PreInSameTeam(arguments):
    if str(sv('eventscripts_currentmap')) != "de_nightfever":
        if arguments[0] != arguments[1]:
            userid = get_userid_from_handle(es.gethandlefromindex(spe.getEntityIndex(arguments[0])))
            if es.isbot(userid):
                username = es.getplayername(userid)
                if username == "[Z Rank] Waterman":
                    return spe.HookAction.Override, False
    return spe.HookAction.Continue, 0

def storymsg(args):
	print_msg = "#%s %s" %(args[0], args[1])
	print_msg = print_msg.replace("메리", "#255,0,0메리#%s" %(args[0]))
	print_msg = print_msg.replace("Mary", "#255,0,0Mary#%s" %(args[0]))
	print_msg = print_msg.replace("제이센", "#255,0,0제이센#%s" %(args[0]))
	print_msg = print_msg.replace("텐지", "#255,0,0텐지#%s" %(args[0]))
	print_msg = print_msg.replace("레이센", "#0,0,255레이센#%s" %(args[0]))
	print_msg = print_msg.replace("테이지", "#0,255,0테이지#%s" %(args[0]))
	print_msg = print_msg.replace("어비스", "#0,255,255어비스#%s" %(args[0]))
	print_msg = print_msg.replace("체리", "#0,0,125체리#%s" %(args[0]))
	print_msg = print_msg.replace("준야", "#purple준야#%s" %(args[0]))
	esc.msg(print_msg)

def onGround(userid):
	return int(es.getplayerprop(userid, 'CBasePlayer.m_fFlags') & 1)

def get_userid_from_pointer(ptr):
	for userid in es.getUseridList():
		if spe.getPlayer(userid) == ptr:
			return userid
	return 0

def getuseridfromhandle(handle):
	for userid in es.getUseridList():
		if es.getplayerhandle(userid) == handle: return userid
	return None


def getweaponlistprop(userid, index, classname):
	if classname in allprimary:
		theweapon = "primary"
	if classname in allsecondary:
		theweapon = "secondary"
	if classname == "weapon_knife": theweapon = "knife"
	same_ary = []
	count = 0
	while count <= 47:
		if count <= 9:
			_tprop = "CCSPlayer.baseclass.baseclass.m_hMyWeapons.00%s" %(count)
		else:
			_tprop = "CCSPlayer.baseclass.baseclass.m_hMyWeapons.0%s" %(count)
		theresult = es.getplayerprop(userid, _tprop)
		count_index = es.getindexfromhandle(theresult)
		count_classname = es.entitygetvalue(count_index, "classname")
		count_weapon = "NULL"
		if count_classname in allprimary:
			count_weapon = "primary"
		if count_classname in allsecondary:
			count_weapon = "secondary"
		if count_classname == "weapon_knife": count_weapon = "knife"
		if count_weapon == theweapon:
			if count_classname != classname:
				same_ary.append((count, count_index, count_classname))
			else:
				if count_index != index:
					same_ary.append((count, count_index, count_classname))
		count += 1
	return same_ary

def getnoise():
	userid = es.getuserid("[C Rank] Zeisen")
	pointer = spe.getPlayer(userid)
	noise_check = spe.call("Noise", pointer)
	es.msg(noise_check)

def PreNoise(args):
	userid = get_userid_from_pointer(args[2])
	if userid:
		es.msg(userid)
	if userid == int(sv('zeisen_id')):
		args[0] = 0.0
	return (spe.HookAction.Modified, 0)

def PreBotHide(args):
	userid = get_userid_from_pointer(args[0])
	if int(sv('remote_target')) == userid:
		return (spe.HookAction.Override, 0)
	if int(sv('remote_target2')) == userid:
		return (spe.HookAction.Override, 0)
	return (spe.HookAction.Continue, 0)

def PrePlayerRunCommand(args):
	if "ze_" in map():
		return (spe.HookAction.Continue, 0)
	if int(sv('mp_freezetime')) == 60:
		return (spe.HookAction.Continue, 0)
	if int(sv('round')) == 8: 
		return (spe.HookAction.Continue, 0)
	ucmd = spe.makeObject('CUserCmd', args[0])
	userid = get_userid_from_pointer(args[2])
	if userid > 0:
		steamid = es.getplayersteamid(userid)
		if steamid != "BOT":
			if ucmd.weaponselect:
				select_classname = es.entitygetvalue(ucmd.weaponselect, "classname")
				if select_classname == est.getgun(userid):
					A = getweaponlistprop(userid, ucmd.weaponselect, select_classname)
					for a in A:
						ucmd.weaponselect = a[1]
		if map() == "de_nightfever":
			name = es.getplayername(userid)
			if name == "[Z Rank] Crizi":
				weapon_index = est.getweaponindex(userid, 1)
				if weapon_index <= 0: weapon_index = est.getweaponindex(userid, 2)
				if weapon_index > 0:	
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_fAccuracyPenalty", 0.0)
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_weaponMode", 1)
				est.setclipammo(userid, 1, 9999)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
				if not ucmd.buttons & IN_ATTACK:
					ucmd.buttons += IN_ATTACK
			if name == "[Z Rank] Zeisen":
				weapon_index = est.getweaponindex(userid, 1)
				if weapon_index <= 0: weapon_index = est.getweaponindex(userid, 2)
				if weapon_index > 0:	
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_fAccuracyPenalty", 0.0)
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_weaponMode", 1)
				est.setclipammo(userid, 1, 9999)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
				if not ucmd.buttons & IN_ATTACK:
					ucmd.buttons += IN_ATTACK
			if name == "[Z Rank] Hiraki":
				est.setarmor(userid, 1000)
				weapon_index = est.getweaponindex(userid, 1)
				if weapon_index <= 0: weapon_index = est.getweaponindex(userid, 2)
				if weapon_index > 0:
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_fAccuracyPenalty", 0.0)
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_weaponMode", 1)
				est.setclipammo(userid, 1, 9999)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
		if map() == "de_season":
			if isalive(userid) and steamid == "BOT":
				name = es.getplayername(userid)
				if name == "[S Rank] Bakura Ryo":
					weapon_index = est.getweaponindex(userid, 2)
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_fAccuracyPenalty", 0.0)
					es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_weaponMode", 1)
					es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
					es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
					if not ucmd.buttons & IN_DUCK:
						if not ucmd.buttons & IN_ATTACK:
							if ucmd.forwardmove == 0: ucmd.forwardmove = 300
					if ucmd.buttons & IN_ATTACK:
						ucmd.buttons &= ~IN_ATTACK
					ucmd.buttons += IN_ATTACK
		if not map() in Special_Maps:
			if isalive(userid) and steamid == "BOT":
				name = es.getplayername(userid)
				if "[Human]" in name:
					if ucmd.buttons & IN_ATTACK: ucmd.forwardmove = -300
				if es.getplayername(userid) == "[C Rank] Zeisen":
					if int(sv('aimbot_enable')) == 1:
						player = playerlib.getPlayer(userid)
						target = player.getClosestPlayer(sv('humanteam'))
						if target[0] != None and target[1] != None:
							if target[0] <= 2000:
								if player.isObstructionBetween(target[1]): return
								tp = playerlib.getPlayer(target[1])
								x,y,z = tp.getEyeLocation()
								player.viewCoord((x,y,z-3)) 
								if not ucmd.buttons & IN_ATTACK: ucmd.buttons += IN_ATTACK
				if name == "[E Rank] Kira" or name == "[E Rank] Vex" or "[F Rank]" in name:
					if name == "[E Rank] Kira":
						if not ucmd.buttons & IN_ATTACK2:
							ucmd.buttons += IN_ATTACK
					target = int(sv('my_attacker_%s' %(userid)))
					if target > 0:
						if es.getplayerhandle(target) > 0:
							if not es.isbot(target):
								if isalive(target):
									x,y,z = es.getplayerlocation(target)
									xx,yy,zz = es.getplayerlocation(userid)
									if float(z) > float(zz + 10):
										victim_location = vecmath.vector(x, y, z)
										attacker_location = vecmath.vector(xx, yy, zz)
										distance = vecmath.distance(victim_location, attacker_location) * 0.0254
										if distance <= 9:
											if ucmd.forwardmove == 0:
												ucmd.forwardmove = 300
												ucmd.buttons += IN_JUMP
					if ucmd.forwardmove == 0: ucmd.forwardmove = 300
		if map() == "ba_quartzy":
			if est.isalive(userid):
				if not es.isbot(userid):
					theforward = int(sv('pery_forward'))
					thesidemove = int(sv('pery_sidemove'))
					ucmd.forwardmove *= theforward
					ucmd.sidemove *= thesidemove
		if int(sv('remote_enable')) == 1:
			if es.getplayerteam(userid) == 1:
				if steamid == "STEAM_0:0:210595115":
					target = int(es.getplayerprop(userid, "CCSPlayer.baseclass.m_hObserverTarget"))
					es.set("remote_target", getuseridfromhandle(target))
					ang = es.getplayerprop(userid, 'CBaseEntity.m_angRotation').split(",")
					es.set("ang_1", es.getplayerprop(userid, "CCSPlayer.m_angEyeAngles[0]"))
					es.set("ang_2", ang[1])
					es.set("ang_3", ang[2])
					if est.getgun(userid) != "weapon_knife": est.give(userid, "weapon_knife")
					else:
						index = est.getweaponindex(userid, 3)
						est.setentitycolor(index, 0, 0, 0, 0)
					if ucmd.sidemove > 0:
						es.set("remote_sidemove", 500)
					if ucmd.sidemove < 0:
						es.set("remote_sidemove", -500)
					if ucmd.forwardmove > 0:
						es.set("remote_forwardmove", 500)
					if ucmd.forwardmove < 0:
						es.set("remote_forwardmove", -500)
					if ucmd.buttons & IN_USE:
						es.set("remote_fire", 1)
					if ucmd.buttons & IN_SPEED:
						es.set("remote_jump", 1)
					if ucmd.buttons & IN_RELOAD:
						es.set("remote_duck", 1)
					if ucmd.buttons & IN_WEAPON1:
						remote_target = int(sv('remote_target'))
						theindex = est.getweaponindex(remote_target, 1)
						theclassname = es.entitygetvalue(theindex, "classname")
						es.server.cmd('es_xsexec %s use %s' %(theclassname))
				if steamid == "STEAM_0:0:21059511":
					es.set("me", userid)
					target = int(es.getplayerprop(userid, "CCSPlayer.baseclass.m_hObserverTarget"))
					es.set("remote_target2", getuseridfromhandle(target))
					ang = es.getplayerprop(userid, 'CBaseEntity.m_angRotation').split(",")
					if est.getgun(userid) != "weapon_knife": est.give(userid, "weapon_knife")
					else:
						index = est.getweaponindex(userid, 3)
						est.setentitycolor(index, 0, 0, 0, 0)
					es.set("ang_2_1", es.getplayerprop(userid, "CCSPlayer.m_angEyeAngles[0]"))
					es.set("ang_2_2", ang[1])
					es.set("ang_2_3", ang[2])
					if ucmd.sidemove > 0:
						es.set("remote_sidemove2", 500)
					if ucmd.sidemove < 0:
						es.set("remote_sidemove2", -500)
					if ucmd.forwardmove > 0:
						es.set("remote_forwardmove2", 500)
					if ucmd.forwardmove < 0:
						es.set("remote_forwardmove2", -500)
					if ucmd.buttons & IN_USE:
						es.set("remote_fire2", 1)
					if ucmd.buttons & IN_SPEED:
						es.set("remote_jump2", 1)
					if ucmd.buttons & IN_RELOAD:
						es.set("remote_duck2", 1)
					if ucmd.buttons & IN_ALT1:
						es.set("remote_firek2", 1)
					if ucmd.buttons & IN_WEAPON1:
						remote_target = int(sv('remote_target2'))
						theindex = est.getweaponindex(remote_target, 1)
						theclassname = es.entitygetvalue(theindex, "classname")
						es.server.cmd('es_xsexec %s use %s' %(theclassname))
				if steamid == "BOT":
					if userid == int(sv('remote_target2')):
						if int(sv('remote_fire2')) == 0:
							if ucmd.buttons & IN_ATTACK: ucmd.buttons &= ~IN_ATTACK
						else:
							es.set("remote_fire2", 0)
							if es.getplayername(userid) != "[E Rank] Kira":
								ucmd.buttons += IN_ATTACK
							ucmd.buttons += IN_USE
						if es.getplayername(userid) == "[C Rank] Zeisen":
							es.set("aimbot_enable", 0)
							player = playerlib.getPlayer(userid)
							target = player.getClosestPlayer(sv('humanteam'))
							if target[0] != None and target[1] != None:
								if target[0] <= 2000:
									if player.isObstructionBetween(target[1]): return
									tp = playerlib.getPlayer(target[1])
									x,y,z = tp.getEyeLocation()
									player.viewCoord((x,y,z-3))
								else: es.setang(userid, sv('ang_2_1'), sv('ang_2_2'), sv('ang_2_3'))
							else: es.setang(userid, sv('ang_2_1'), sv('ang_2_2'), sv('ang_2_3'))
						else:
							es.setang(userid, sv('ang_2_1'), sv('ang_2_2'), sv('ang_2_3'))
						ucmd.forwardmove = 0
						ucmd.sidemove = 0
						ucmd.upmove = 0
						ucmd.forwardmove = int(sv('remote_forwardmove2'))
						ucmd.sidemove = int(sv('remote_sidemove2'))
						es.set("remote_forwardmove2", 0)
						es.set("remote_sidemove2", 0)
						if ucmd.buttons & IN_DUCK:
							ucmd.buttons &= ~IN_DUCK
						if ucmd.buttons & IN_SPEED:
							ucmd.buttons &= ~IN_SPEED
						if ucmd.buttons & IN_JUMP:
							ucmd.buttons &= ~IN_JUMP
						if int(sv('remote_duck2')) == 0:
							if ucmd.buttons & IN_DUCK: ucmd.buttons &= ~IN_DUCK
						else:
							es.set("remote_duck2", 0)
							ucmd.buttons += IN_DUCK
						if int(sv('remote_jump2')) == 1:
							es.set("remote_jump2", 0)
							ucmd.buttons += IN_JUMP
						if es.getplayername(userid) != "[E Rank] Kira":
							if int(sv('remote_firek2')) == 1:
								es.set("remote_firek2", 0)
								ucmd.buttons += IN_ATTACK2
					else:
						if userid == int(sv('remote_target')):
							es.setang(userid, sv('ang_1'), sv('ang_2'), sv('ang_3'))
							ucmd.forwardmove = int(sv('remote_forwardmove'))
							ucmd.sidemove = int(sv('remote_sidemove'))
							es.set("remote_forwardmove", 0)
							es.set("remote_sidemove", 0)
							if ucmd.buttons & IN_ATTACK:
								ucmd.buttons &= ~IN_ATTACK
							if ucmd.buttons & IN_DUCK:
								ucmd.buttons &= ~IN_DUCK
							if ucmd.buttons & IN_SPEED:
								ucmd.buttons &= ~IN_SPEED
							if ucmd.buttons & IN_JUMP:
								ucmd.buttons &= ~IN_JUMP
							if int(sv('remote_fire')) == 1:
								es.set("remote_fire", 0)
								if es.getplayername(userid) != "[E Rank] Kira":
									ucmd.buttons += IN_ATTACK
								ucmd.buttons += IN_USE
							if int(sv('remote_duck')) == 1:
								es.set("remote_duck", 0)
								ucmd.buttons += IN_DUCK
							if int(sv('remote_jump')) == 1:
								es.set("remote_jump", 0)
								ucmd.buttons += IN_JUMP
							if es.getplayername(userid) != "[E Rank] Kira":
								if int(sv('remote_firek')) == 1:
									es.set("remote_firek", 0)
									ucmd.buttons += IN_ATTACK2
	return (spe.HookAction.Continue, 0)

def getaimbot_target(zeisen_id):
	player_distance = []
	for userid in es.getUseridList():
		if es.getplayerteam(userid) == int(sv('humanteam')):
			if isalive(userid):
				x1,y1,z1 = es.getplayerlocation(userid)
				x2,y2,z2 = es.getplayerlocation(zeisen_id)
				distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5
				if not getbetween(zeisen_id, userid):
					player_distance.append((distance, userid))
	return min(player_distance) if player_distance else (None, None)

def _getEyeAngle():
   if _gamename in ('cstrike', 'left4dead', 'left4dead2'):
      return 'CCSPlayer.m_angEyeAngles[%s]'
   elif _gamename == 'dod':
      return 'CDODPlayer.m_angEyeAngles[%s]'
   elif _gamename == 'tf':
      return 'CTFPlayer.tfnonlocaldata.m_angEyeAngles[%s]'
   elif _gamename in ('hl2mp', 'ageofchivalry', 'diprip', 'fistful_of_frags', 'gesource',
    'hl2ctf', 'smashball', 'so', 'sourceforts', 'synergy', 'zombie_master', 'zps'):
      return 'CHL2MP_Player.m_angEyeAngles[%s]'
   elif _gamename in ('hl2', 'episodic', 'ep2'):
      return 'CBaseFlex.m_vecViewOffset[%s]'
   elif _gamename == 'portal':
      return 'CPortal_Player.m_angEyeAngles[%s]'
   elif _gamename in ('ag2', 'Jailbreak'):
      return 'CHL2MP_Player.hl2mpnonlocaldata.m_angEyeAngles[%s]'
   elif _gamename == 'dystopia':
      return 'CDYSPlayer.m_angEyeAngles[%s]'
   elif _gamename == 'esmod':
      return 'CESPlayer.m_angEyeAngles[%s]'
   elif _gamename == 'FortressForever':
      return 'CFFPlayer.m_angEyeAngles[%s]'
   elif _gamename in ('empires', 'hidden'):
      return 'CSDKPlayer.m_angEyeAngles[%s]'
   elif _gamename == 'hl1mp':
      return 'CHL1MP_Player.m_angEyeAngles[%s]'
   elif _gamename == 'insurgency':
      return 'CINSPlayer.sensdata.m_angEyeAngles[%s]'
   elif _gamename == 'NeotokyoSource':
      return 'CNEOPlayer.m_angEyeAngles[%s]'
   elif _gamename == 'pvkii':
      return 'CPVK2Player.m_angEyeAngles[%s]'
   elif _gamename == 'sgtls':
      return 'CTLSPlayer.nonlocaldata.m_angEyeAngles[%s]'
   return ''
_eyeangle = _getEyeAngle()

def getViewAngle(userid):
        myRotation  = es.getplayerprop(userid, "CBaseEntity.m_angRotation").split(',')[2]
        myEyeAngle0 = es.getplayerprop(userid, _eyeangle % 0)
        myEyeAngle1 = es.getplayerprop(userid, _eyeangle % 1)
        return (myEyeAngle0, (myEyeAngle1 + 360) if myEyeAngle1 < 0 else myEyeAngle1, float(myRotation))

def getEyeLocation(userid):
        return tuple(es.getplayerprop(userid, 'CBasePlayer.localdata.m_vecViewOffset[' + str(x) + ']') + y for x, y in enumerate(es.getplayerlocation(userid)))

def getViewCoord(userid):
        es.server.cmd('es_xprop_dynamic_create %s blackout.mdl' % userid)
        location = es.getindexprop(_lastgive, 'CBaseEntity.m_vecOrigin')
        es.server.cmd('es_xremove ' + _lastgive)
        return location

def viewCoord(userid, value):
        myLocation  = getEyeLocation(userid)
        myVector    = es.createvectorstring(myLocation[0], myLocation[1], myLocation[2])
        theVector   = es.createvectorstring(value[0], value[1], value[2])
        ourVector   = es.createvectorfrompoints(myVector, theVector)
        ourVector   = es.splitvectorstring(ourVector)
        myViewAngle = getViewAngle(userid)
        ourAtan = math.degrees(math.atan(float(ourVector[1]) / float(ourVector[0])))
        if float(ourVector[0]) < 0:
            RealAngle = ourAtan + 180
        elif float(ourVector[1]) < 0:
            RealAngle = ourAtan + 360
        else:
            RealAngle = ourAtan
        yAngle = RealAngle
        xAngle = 0 - math.degrees(math.atan(ourVector[2] / math.sqrt(math.pow(float(ourVector[1]), 2) + math.pow(float(ourVector[0]), 2))))
        es.server.cmd('es_xsetang %s %s %s %s' % (userid, xAngle, yAngle, myViewAngle[2]))

def lookAt(userid, userid2):
        start_eyeangle2 = getViewAngle(userid2)
	viewCoord(userid, start_eyeangle2)

def getbetween(userid, userid2):
        start_eyeangle = getViewAngle(userid)
        start_location = getEyeLocation(userid)
	end_location = getEyeLocation(userid2)
	x2,y2,z2 = es.getplayerlocation(userid)
	x1,y1,z1 = es.getplayerlocation(userid2)
	distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5
        if distance <= 40:
            return False # If the coordinates are close enough there is no wall between them

        # Force the player to look at the coordinates and then check if the player's view coord is
        # between the start and end locations
        lookAt(userid, userid2)
	gga = getViewCoord(userid)
        view_location = gga.split(",")
        result = True
        for x in (0, 1, 2):
            if not min(start_location[x], end_location[x]) <= view_location[x] <= max(start_location[x], end_location[x]):
                result = False
                break

        # Revert the player's eye angles and return the final result
        es.server.cmd('es_xsetang %s %s %s %s' % ((userid,) + start_eyeangle))
        return result

def check_fun():
	userid = 72
	for f_userid in es.getUseridList():
		ho = isWallBetween(es.getplayerlocation(userid), es.getplayerlocation(f_userid))
		es.msg(ho)

def isWallBetween(vec1, vec2):
 
    
 
    # Allocates both vectors...
 
    vecAbsStart = spe.alloc(12)
 
    spe.setLocVal("f", vecAbsStart, vec1[0])
 
    spe.setLocVal("f", vecAbsStart + 4, vec1[1])
 
    spe.setLocVal("f", vecAbsStart + 8, vec1[2])
 
    
 
    vecAbsEnd = spe.alloc(12)
 
    spe.setLocVal("f", vecAbsEnd, vec2[0])
 
    spe.setLocVal("f", vecAbsEnd + 4, vec2[1])
 
    spe.setLocVal("f", vecAbsEnd + 8, vec2[2])
 
    
 
    # Allocates/Constructs the filter with not entity...
 
    pFilter = spe.alloc(12)
 
    spe.call("TraceFilterSimple", pFilter, 0, 0)
 
    
 
    mask = 0x1 # CONTENTS_SOLID
 
    
 
    # Allocates our trace_t...
 
    ptr = spe.alloc(84)
 
    
 
    # Calls the function...
 
    spe.call("TraceLine", vecAbsStart, vecAbsEnd, mask, pFilter, ptr)
 
    
 
    # Checks if we hited the world...
 
    return_value = spe.getEntityClassName(spe.getLocVal("i", ptr + 76)) == "worldspawn"
 
    
 
    # Deallocate our pointers...
 
    spe.dealloc(vecAbsStart)
 
    spe.dealloc(vecAbsEnd)
 
    spe.dealloc(pFilter)
 
    spe.dealloc(ptr)
 
    
 
    # Returns the value...
 
    return return_value 

def updateradar(args):
	if str(sv('sv_password')) == "nipperz":
		return (spe.HookAction.Override, 0)

def autobuy_command(args):
	userid = int(args[0])
	steamid = getplayerzeisenid(userid)
	mastery_select = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
	event_1 = popuplib.easymenu('skillm_%s' %(userid), None, none_select)
	event_1.settitle("＠ 마스터리 스킬 메뉴")
	event_1.c_endsep = " \n○ 액티브 스킬을 선택하여 시전할수 있습니다.\n "
	userid_cash = int(es.getplayerprop(userid, "CCSPlayer.m_iAccount"))
	if mastery_select == 3:
		skill = int(es.keygetvalue(steamid, "player_data", "mastery_skill1"))
		if skill > 0:
			skill_cash = 1000
			if userid_cash >= skill_cash: state = 1
			else: state = 0
			event_1.addoption("mastery_3_skill1", "Ammoful($%s)" %(skill_cash), state)
		skill = int(es.keygetvalue(steamid, "player_data", "mastery_skill2"))
		if skill > 0:
			skill_cash = 6000
			if userid_cash >= skill_cash: state = 1
			else: state = 0
			event_1.addoption("mastery_3_skill2", "치유($%s)" %(skill_cash), state)
		skill = int(es.keygetvalue(steamid, "player_data", "mastery_skill3"))
		if skill > 0:
			skill_cash = 5000
			if userid_cash >= skill_cash: state = 1
			else: state = 0
			event_1.addoption("mastery_3_skill3", "Remote Human($%s)" %(skill_cash), state)
		skill = int(es.keygetvalue(steamid, "player_data", "mastery_skill4"))
		if skill > 0:
			skill_cash = 6500
			if userid_cash >= skill_cash: state = 1
			else: state = 0
			event_1.addoption("mastery_3_skill4", "Be Doctor($%s)" %(skill_cash), state)
		skill = int(es.keygetvalue(steamid, "player_data", "mastery_skill5"))
		if skill > 0:
			skill_cash = 15000
			if userid_cash >= skill_cash: state = 1
			else: state = 0
			event_1.addoption("mastery_3_skill5", "God Save The King($%s)" %(skill_cash), state)
	event_1.menuselect = masteryskill_select
	event_1.send(userid)

def masteryskill_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	username = es.getplayername(userid)
	userid_cash = int(es.getplayerprop(userid, "CCSPlayer.m_iAccount"))
	if isalive(userid):
		if choice == "mastery_3_skill1":
			if userid_cash >= 1000:
				userid_cash -= 1000
				esc.msg("#blue %s 유저#255,255,255가 #gold서포트 마스터리 스킬#255,255,255 #0,255,255'Ammoful'#255,255,255를 시전하여 총알과 방탄복이 보급되었습니다." %(username))
				est.give("#h", "item_assaultsuit")
				#playsound("zeisenproject_3/autosounds/spsk_active.wav", 0.5)
		if choice == "mastery_3_skill2":
			if userid_cash >= 6000:
				userid_cash -= 6000
				skill = float(es.keygetvalue(steamid, "player_data", "mastery_skill2"))
				skill_print = skill * 10
				skill_math = skill / 10
				playsound("zeisenproject_3/autosounds/spsk_active.wav")
				magic = float(es.keygetvalue(steamid, "player_data", "magic"))
				if map() != "de_nightfever":
					esc.msg("#blue %s 유저#255,255,255가 #gold서포트 마스터리 스킬#255,255,255 #0,255,255'치유'#255,255,255를 시전하여 체력이 %s％ 만큼 상승했습니다." %(username, skill_print))
					for f_userid in es.getUseridList():
						if es.getplayerteam(f_userid) == int(sv('humanteam')):
							mh = int(max_health[f_userid])
							give_health = mh * float(skill_math)
							give_health += magic
							healthadd(f_userid, give_health)
				if map() == "de_nightfever":
					esc.msg("#blue %s 유저#255,255,255가 #gold서포트 마스터리 스킬#255,255,255 #0,255,255'치유'#255,255,255를 시전하여 체력이 %s+ 만큼 상승했습니다." %(username, skill_print))
					for f_userid in es.getUseridList():
						if es.getplayerteam(f_userid) == int(sv('humanteam')):
							give_health = skill_print
							healthadd(f_userid, give_health)
		if choice == "mastery_3_skill3":
			if userid_cash >= 5000:
				userid_cash -= 5000
				esc.msg("#blue %s 유저#255,255,255가 #gold서포트 마스터리 스킬#255,255,255 #0,255,255'Remote Human'#255,255,255을 시전하여 봇들이 소생되었습니다." %(username))
				x,y,z = es.getplayerlocation(userid)
				es.server.cmd('est_effect 10 #a 0 sprites/laser.vmt %s %s %s -10 250 2 10 100 0 5 5 255 255 1' %(x,y,z))
				es.server.cmd('est_effect 11 #a 0 sprites/bluelaser1.vmt %s %s %s 2 8 255' %(x,y,z))
				es.server.cmd('est_effect 11 #a 0 effects/exit1.vmt %s %s %s 2 3 255' %(x,y,z))
				es.emitsound("player", userid, "zeisenproject_3/autosounds/spsk_active.wav", 1.0, 1.0)
				for f_userid in es.getUseridList():
					if es.isbot(f_userid):
						if es.getplayerteam(f_userid) == int(sv('humanteam')):
							spawn(f_userid)
							gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
							gamethread.delayed(0.2, spe.call, ("Follow", spe.getPlayer(f_userid), spe.getPlayer(userid)))
		if choice == "mastery_3_skill4":
			if userid_cash >= 6500:
				userid_cash -= 6500
				esc.msg("#blue %s 유저#255,255,255가 #gold서포트 마스터리 스킬#255,255,255 #0,255,255'Be Doctor'#255,255,255를 시전하여 유저들이 소생되었습니다." %(username))
				x,y,z = es.getplayerlocation(userid)
				es.server.cmd('est_effect 10 #a 0 sprites/laser.vmt %s %s %s -10 250 2 10 100 0 5 5 255 255 1' %(x,y,z))
				es.server.cmd('est_effect 11 #a 0 sprites/bluelaser1.vmt %s %s %s 2 8 255' %(x,y,z))
				es.server.cmd('est_effect 11 #a 0 effects/exit1.vmt %s %s %s 2 3 255' %(x,y,z))
				es.emitsound("player", userid, "zeisenproject_3/autosounds/spsk_active.wav", 1.0, 1.0)
				for f_userid in es.getUseridList():
					if es.isbot(f_userid):
						if es.getplayerteam(f_userid) == int(sv('zombieteam')):
							bot_move(f_userid, x, y, z)
							f_name = es.getplayername(f_userid)
							if f_name == "[C Rank] Zeisen":
								if not isalive(f_userid):
									if random.randint(1,3) == 3:
										spawn(f_userid)
										gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
										esc.msg("#255,0,0※ %s 보스도 소생되었다!" %(f_name))
							if f_name == "[E Rank] Kira":
								if not isalive(f_userid):
									if random.randint(1,4) == 4:
										spawn(f_userid)
										gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
										esc.msg("#255,0,0※ %s 보스도 소생되었다!" %(f_name))
							if f_name == "[E Rank] Vex":
								if not isalive(f_userid):
									if random.randint(1,4) == 4:
										spawn(f_userid)
										gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
										es.server.cmd('es_xdelayed 0.25 es_xsexec %s kill' %(f_userid))
										esc.msg("#255,0,0※ %s 보스도 소생되었다!" %(f_name))
					if not es.isbot(f_userid) and not est.isalive(f_userid):
						if es.getplayerteam(f_userid) == int(sv('humanteam')):
							spawn(f_userid)
							gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
							gamethread.delayed(0.2, est.give, (f_userid, "weapon_mac10"))
		if choice == "mastery_3_skill5":
			if userid_cash >= 15000:
				userid_cash -= 15000
				esc.msg("#blue %s 유저#255,255,255가 #gold서포트 마스터리 스킬#255,255,255 #0,255,255'God Save The King'#255,255,255을 시전하여 봇/아군들이 소생되었습니다." %(username))
				x,y,z = es.getplayerlocation(userid)
				es.server.cmd('est_effect 10 #a 0 sprites/laser.vmt %s %s %s -10 250 2 10 100 0 5 5 255 255 1' %(x,y,z))
				es.server.cmd('est_effect 11 #a 0 sprites/bluelaser1.vmt %s %s %s 2 8 255' %(x,y,z))
				es.server.cmd('est_effect 11 #a 0 effects/exit1.vmt %s %s %s 2 3 255' %(x,y,z))
				es.emitsound("player", userid, "zeisenproject_3/autosounds/spsk_active.wav", 1.0, 1.0)
				for f_userid in es.getUseridList():
					if not es.isbot(f_userid) and not est.isalive(f_userid):
						if es.getplayerteam(f_userid) == int(sv('humanteam')):
							spawn(f_userid)
							gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
							gamethread.delayed(0.2, est.give, (f_userid, "weapon_m249"))
				for f_userid in es.getUseridList():
					if es.isbot(f_userid):
						if es.getplayerteam(f_userid) == int(sv('humanteam')):
							spawn(f_userid)
							gamethread.delayed(0.2, est.teleport, (f_userid, x, y, z))
							gamethread.delayed(0.2, spe.call, ("Follow", spe.getPlayer(f_userid), spe.getPlayer(userid)))
				
	es.setplayerprop(userid, "CCSPlayer.m_iAccount", userid_cash)

def rebuy_command(args):
	a = 1

def spotted(args):
	bot = int(args[0])
	player = int(args[1])

def ticklistener():
	if map() == "de_nightfever":
		if str(sv('sv_password')) == "nipperz":
			zombie_list = es.createentityindexlist("npc_zombie")
			for a in zombie_list:
				leader = es.getindexprop(a, "CHostage.m_leader")
				if leader <= 0:
					userid = random.choice(es.getUseridList())
					id_handle = es.getplayerhandle(userid)
					es.setindexprop(a, "CHostage.m_leader", id_handle)
				if 0 >= int(es.entitygetvalue(a, "health")):
					es.remove(a)
			zombie_list = es.createentityindexlist("npc_soldier")
			for a in zombie_list:
				leader = es.getindexprop(a, "CHostage.m_leader")
				if leader <= 0:
					userid = random.choice(es.getUseridList())
					id_handle = es.getplayerhandle(userid)
					es.setindexprop(a, "CHostage.m_leader", id_handle)
				if 0 >= int(es.entitygetvalue(a, "health")):
					es.remove(a)
			zombie_list = es.createentityindexlist("npc_dog")
			for a in zombie_list:
				leader = es.getindexprop(a, "CHostage.m_leader")
				if leader <= 0:
					userid = random.choice(es.getUseridList())
					id_handle = es.getplayerhandle(userid)
					es.setindexprop(a, "CHostage.m_leader", id_handle)
				if 0 >= int(es.entitygetvalue(a, "health")):
					es.remove(a)
			zombie_list = es.createentityindexlist("npc_headcrab")
			for a in zombie_list:
				leader = es.getindexprop(a, "CHostage.m_leader")
				if leader <= 0:
					userid = random.choice(es.getUseridList())
					id_handle = es.getplayerhandle(userid)
					es.setindexprop(a, "CHostage.m_leader", id_handle)
				if 0 >= int(es.entitygetvalue(a, "health")):
					es.remove(a)
			zombie_list = es.createentityindexlist("npc_synth")
			for a in zombie_list:
				leader = es.getindexprop(a, "CHostage.m_leader")
				if leader <= 0:
					userid = random.choice(es.getUseridList())
					id_handle = es.getplayerhandle(userid)
					es.setindexprop(a, "CHostage.m_leader", id_handle)
				if 0 >= int(es.entitygetvalue(a, "health")):
					es.remove(a)
			zombie_list = es.createentityindexlist("npc_stalker")
			for a in zombie_list:
				if 0 >= int(es.entitygetvalue(a, "health")):
					es.remove(a)

def test4244():
	userid = es.getuserid("[Feast] Zeisen")
	if userid:
		x,y,z = es.getplayerlocation(userid)
		for f_userid in es.getUseridList():
			if es.isbot(f_userid):
				bot_away(f_userid, x, y, z)

def fake_hegrenade_explosion(x, y, z, userid = -1):
        index = es.createentity("hegrenade_projectile")
	es.entitysetvalue(index, 'origin', '%s %s %s' %(x,y,z))
        es.setindexprop(index,"CBaseGrenade.m_flDamage",100)
        es.setindexprop(index,"CBaseGrenade.m_bIsLive",True)
        es.setindexprop(index,"CBaseGrenade.m_DmgRadius",350)
        if userid != -1:
		es.setindexprop(index, "CBaseEntity.m_iTeamNum", es.getplayerteam(userid))
		es.setindexprop(index, "CBaseGrenade.m_hThrower",es.getplayerhandle(userid))
        es.spawnentity(index)
        #es.setindexprop(index, "CBaseCSGrenadeProjectile.baseclass.baseclass.baseclass.baseclass.m_vecOrigin", "%s,%s,%s" %(x,y,z))
        spe.call("Detonate", spe.getEntityOfIndex(index))

def fake_flashbang_explosion(x, y, z, userid = -1):
        index = es.createentity("flashbang_projectile")
	es.entitysetvalue(index, 'origin', '%s %s %s' %(x,y,z))
        es.setindexprop(index,"CBaseGrenade.m_flDamage",100)
        if userid != -1:
		es.setindexprop(index, "CBaseEntity.m_iTeamNum", es.getplayerteam(userid))
		es.setindexprop(index, "CBaseGrenade.m_hThrower",es.getplayerhandle(userid))
        es.spawnentity(index)
        #es.setindexprop(index, "CBaseCSGrenadeProjectile.baseclass.baseclass.baseclass.baseclass.m_vecOrigin", "%s,%s,%s" %(x,y,z))
        spe.call("Detonate", spe.getEntityOfIndex(index))

def test():
	index = es.createentity("hegrenade_projectile")
	location = get_z_max(3).split(",")
	est.entteleport(index, location[0], location[1], location[2])
	es.spawnentity(index)
	pre = es.precachemodel("models/props_combine/headcrabcannister01a.mdl")
	es.entitysetvalue(index, 'modelindex', pre)
	es.setindexprop(index, "CBaseEntity.m_angRotation", "90,0,0")
	handle = es.getplayerhandle(3)
	es.setindexprop(index, "CBaseCSGrenadeProjectile.baseclass.m_hThrower", handle)

def giveall(args):
	itemname = args[0]
	itemrealname = args[1]
	much = args[2]
	esc.msg("#255,255,255모두가 선물로 %s #255,255,255아이템을#gold %s개#255,255,255만큼 받았습니다." %(itemrealname, much))
	for a in playerlib.getPlayerList("#human"):
		steamid = getplayerzeisenid(a.userid)
		keymath(steamid, "player_data", itemname, "+", much)

def givehat(userid, r, g, b, a):
        eyeangle = vecmath.vector(playerlib.getPlayer(userid).getViewAngle())
        eyeangle.x -= 10
        eyeangle.y -= 180
        index = es.createentity("prop_dynamic_override")
	total_name = "hat_%s" %(userid)
        es.setentityname(index, total_name)
        location = es.getplayerlocation(userid)
	est.setentmodel(index, 'models/props_combine/breentp_rings.mdl')
        es.entitysetvalue(index, "origin", '%s %s %s'%(location[0] - .5, location[1], location[2] + 60))
        es.entitysetvalue(index, "solid", 1)
        es.entitysetvalue(index, "angles", eyeangle.getstr(" "))
        es.setindexprop(index, 'CBaseEntity.m_hOwnerEntity', es.getplayerhandle(userid))
        es.server.queuecmd("es_xspawnentity %s"% index)
	es.entitysetvalue(index, 'DefaultAnim', 'idle')
        es.server.queuecmd("es_xfire %s %s %s !activator"% (userid, total_name, 'SetParent'))
	est.setentitycolor(index, r, g, b, a)

def givecs(args):
	userid = int(args[0])
	much = int(args[1])
	steamid = getplayerzeisenid(userid)
	keymath(steamid, "player_data", "cs", "+", much)

def givecode(args):
	userid = int(args[0])
	much = str(args[1])
	steamid = getplayerzeisenid(userid)
	username = es.getplayername(userid)
	if much != "없음 ":
		esc.msg("#0,255,255 %s 님에게 알수없는 영혼이 깃든듯 합니다." %(username))
	else:
		esc.msg("#255,0,0 %s 님에게 저주의 영혼이 깃든듯 합니다." %(username))
	es.keysetvalue(steamid, "player_data", "code", much)

def update_key():
	es.keygroupload("update", "|rpg")
	es.keygroupcreate("STEAM_0178251036")
	es.keygrouprename("STEAM_0117803258", "STEAM_0178251036")
	es.keygroupsave("STEAM_0178251036", "|rpg/player_data")
	es.keygroupdelete("update")
	es.server.cmd("echo All Data Updated Completely")


def backup_player(userid):
	zeisenid = getplayerzeisenid(userid)
	steamid = es.getplayersteamid(userid)
	es.keygroupload("rpg", "|rpg")
	existcheck = es.exists("key", "rpg", steamid)
	if existcheck == 1:
		backup_value(zeisenid, steamid, 'level', 1)
		backup_value(zeisenid, steamid, 'xp', 0)
		backup_value(zeisenid, steamid, 'nextxp', 125)
		backup_value(zeisenid, steamid, 'skillpoint', 1)
		backup_value(zeisenid, steamid, 'stetpoint', 1)
		backup_value(zeisenid, steamid, 'health', 150)
		backup_value(zeisenid, steamid, 'power', 100)
		backup_value(zeisenid, steamid, 'speed', 1.0)
		backup_value(zeisenid, steamid, 'armor', 0)
		backup_value(zeisenid, steamid, 'dollar_regen', 0)
		backup_value(zeisenid, steamid, 'magic', 0)
		backup_value(zeisenid, steamid, 'classname', 'human')
		backup_value(zeisenid, steamid, 'mastery_select', 0)
		backup_value(zeisenid, steamid, 'mastery_xp', 0)
		backup_value(zeisenid, steamid, 'mastery_list', "555555555")
		backup_value(zeisenid, steamid, 'mastery_skill1', 0)
		backup_value(zeisenid, steamid, 'mastery_skill2', 0)
		backup_value(zeisenid, steamid, 'mastery_skill3', 0)
		backup_value(zeisenid, steamid, 'mastery_skill4', 0)
		backup_value(zeisenid, steamid, 'mastery_skill5', 0)
		backup_value(zeisenid, steamid, 'cs', 0)
		backup_value(zeisenid, steamid, 'kill', 0)
		backup_value(zeisenid, steamid, 'death', 0)
		backup_value(zeisenid, steamid, 'connect_point', 0)
		backup_value(zeisenid, steamid, 'npc_kuria_nightfever_xp', 0)
		backup_value(zeisenid, steamid, 'npc_beer_nightfever_xp', 0)
		backup_value(zeisenid, steamid, 'volume', 1.0)
		backup_value(zeisenid, steamid, 'partner', "None")
		backup_value(zeisenid, steamid, 'skin', "None")
		backup_value(zeisenid, steamid, 'code', "없음 ")
		backup_value(zeisenid, steamid, "callname", "#255,255,255ZP3 Player ")
		backup_value(zeisenid, steamid, 'npc_reisen_nightfever_xp', 0)
		backup_value(zeisenid, steamid, "npc_nosay_nightfever_xp", 0)
		backup_value(zeisenid, steamid, "classname_skill1", 0)
		backup_value(zeisenid, steamid, "classname_skill2", 0)
		backup_value(zeisenid, steamid, "classname_skill3", 0)
		backup_value(zeisenid, steamid, "classname_skill4", 0)
		backup_value(zeisenid, steamid, "classname_skill5", 0)
		backup_value(zeisenid, steamid, "classname_skill6", 0)
		backup_value(zeisenid, steamid, "classname_skill7", 0)
		backup_value(zeisenid, steamid, "classname_skill8", 0)
		backup_value(zeisenid, steamid, "classname_skill9", 0)
		backup_value(zeisenid, steamid, "classname_skill10", 0)
		create = 0
		while create < 30:
			create += 1
			backup_value(zeisenid, steamid, 'item%s' %(create), 0)
			backup_value(zeisenid, steamid, 'skill%s' %(create), 0)
		es.keydelete("rpg", steamid)
		es.keygroupsave("rpg", "|rpg")
		esc.tell(userid, "#lightgreen＊ 복구가 완료되었습니다.")
	else: esc.tell(userid, "#lightgreen＊ 데이터가 존재하지 않습니다.")
	es.keygroupdelete("rpg")

def backup_value(zeisenid, steamid, what, no):
	getvalue = es.keygetvalue("rpg", steamid, what)
	es.keysetvalue(zeisenid, "player_data", what, getvalue)

def reset_player(steamid):
	exist = es.exists('key', steamid, "player_data")
	if exist == 1: es.keydelete(steamid, "player_data")
	es.keycreate(steamid, "player_data")
	es.keysetvalue(steamid, "player_data", 'level', 1)
	es.keysetvalue(steamid, "player_data", 'xp', 0)
	es.keysetvalue(steamid, "player_data", 'nextxp', 125)
	es.keysetvalue(steamid, "player_data", 'skillpoint', 1)
	es.keysetvalue(steamid, "player_data", 'stetpoint', 1)
	es.keysetvalue(steamid, "player_data", 'health', 150)
	es.keysetvalue(steamid, "player_data", 'power', 100)
	es.keysetvalue(steamid, "player_data", 'speed', 1.0)
	es.keysetvalue(steamid, "player_data", 'armor', 0)
	es.keysetvalue(steamid, "player_data", 'dollar_regen', 0)
	es.keysetvalue(steamid, "player_data", 'magic', 0)
	es.keysetvalue(steamid, "player_data", 'money', 0)
	es.keysetvalue(steamid, "player_data", 'human_xp', 0)
	es.keysetvalue(steamid, "player_data", 'bp', 0)
	es.keysetvalue(steamid, "player_data", 'classname', 'human')
	es.keysetvalue(steamid, "player_data", 'mastery_select', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_xp', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_list', "555555555")
	es.keysetvalue(steamid, "player_data", 'mastery_skill1', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill2', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill3', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill4', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill5', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill6', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill7', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill8', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill9', 0)
	es.keysetvalue(steamid, "player_data", 'mastery_skill10', 0)
	es.keysetvalue(steamid, "player_data", 'cs', 0)
	es.keysetvalue(steamid, "player_data", 'kill', 0)
	es.keysetvalue(steamid, "player_data", 'death', 0)
	es.keysetvalue(steamid, "player_data", 'connect_point', 0)
	es.keysetvalue(steamid, "player_data", 'npc_kuria_nightfever_xp', 0)
	es.keysetvalue(steamid, "player_data", 'npc_beer_nightfever_xp', 0)
	es.keysetvalue(steamid, "player_data", 'volume', 1.0)
	es.keysetvalue(steamid, "player_data", 'partner', "None")
	es.keysetvalue(steamid, "player_data", 'skin', "None")
	es.keysetvalue(steamid, "player_data", 'code', "없음 ")
	es.keysetvalue(steamid, "player_data", 'say', "남긴말이 없습니다.")
	es.keysetvalue(steamid, "player_data", "callname", "#255,255,255평범한 ")
	es.keysetvalue(steamid, "player_data", 'npc_reisen_nightfever_xp', 0)
	es.keysetvalue(steamid, "player_data", "npc_nosay_nightfever_xp", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill1", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill2", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill3", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill4", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill5", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill6", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill7", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill8", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill9", 0)
	es.keysetvalue(steamid, "player_data", "classname_skill10", 0)
	es.keysetvalue(steamid, "player_data", "level_color", "255,255,255")
	create = 0
	while create < 60:
		create += 1
		es.keysetvalue(steamid, "player_data", 'item%s' %(create), 0)
		if create <= 40: es.keysetvalue(steamid, "player_data", 'skill%s' %(create), 0)
	es.keysetvalue(steamid, "player_data", "update_ver", 6)

def player_disconnect(ev):
	userid = int(ev['userid'])
	steamid = ev['networkid'].replace(":", "")
	username = str(es.keygetvalue(steamid, "player_data", "username"))
	reason = str(ev['reason'])
	reason = reason.replace('"', '')
	if steamid != "BOT":
		if username != "None":
			if not "kicked from server" in reason.lower():
				esc.msg("#blue %s#255,255,255님이 퇴장했습니다. (%s)" %(username, reason))
				for a in playerlib.getPlayerList('#human'):
					usermsg.centermsg(a.userid, "%s님이 퇴장했습니다.\n(%s)" %(username, reason))
					es.playsound(a.userid, "npc/overwatch/radiovoice/stabilizationjurisdiction.wav", 1.0)
	if str(ev['networkid']) != "BOT":
		fofo = int(sv('players_count')) - 1
		es.set("players_count", fofo)
		if str(sv('sv_password')) != "nipperz":
			es.keygroupsave(steamid, "|rpg/player_data")
		es.keygroupdelete(steamid)


def player_connect(ev):
	userid = int(ev['userid'])
	steamid = str(ev['networkid'])
	if str(ev['networkid']) != "BOT":
		fofo = int(sv('players_count')) + 1
		es.set("players_count", fofo)
		username = str(ev['name'])
		if username != "None":
			esc.msg("#blue %s#255,255,255님이 제이센 프로젝트 3에 참가중입니다!" %(username))
		if not str(ev['networkid']) in "STEAM_0:0:21059511, STEAM_0027045397":
			if fofo >= 15: es.server.cmd('kickid %s "부정행위 금지"' %(userid))

def Commander4(userid, args):
	steamid = getplayerzeisenid(userid)
	username = es.getplayername(userid)
	if steamid != "BOT":
		if steamid == "STEAM_0021059511":
			if args[0] == "helicopter_clear":
				est.stopsound("#h", "ambient/machines/heli_pass_quick1.wav")
				est.stopsound("#h", "npc/attack_helicopter/aheli_rotor_loop1.wav")
				est.remove("helicopter")
				est.remove("npc_dog")
				est.remove("npc_zombie")
				est.remove("npc_headcrab")
				est.remove("npc_synth")
				est.remove("npc_soldier")
				est.remove("car")
			if args[0] == "helicopter_down":
				est.play("#h", "ambient/machines/spindown.wav")
				est.stopsound("#h", "ambient/machines/heli_pass_quick1.wav")
				est.stopsound("#h", "npc/attack_helicopter/aheli_rotor_loop1.wav")
				est.remove("helicopter")
				es.server.cmd('r_makechat "#255,255,255Kate" "오 이런, 일단 난 여길 벗어나야겠어!"')
			if args[0] == "here":
				x,y,z = es.getplayerlocation(userid)
				for a in playerlib.getPlayerList("#bot"):
					bot_move(a.userid, x, y, z)
			if args[0] == "heree":
				x,y,z = es.getplayerlocation(userid)
				for a in playerlib.getPlayerList("#bot,#alive"):
					spe.call("Follow", spe.getPlayer(a.userid), spe.getPlayer(userid))
					bot_move(a.userid, x, y, z)
			if args[0] == "support_come":
				est.play("#h", "ambient/machines/heli_pass_quick1.wav")
			if args[0] == "helicopter":
				est.play("#h", "ambient/machines/heli_pass_quick1.wav")
				gamethread.delayed(6, est.play, ("#h", "npc/attack_helicopter/aheli_rotor_loop1.wav"))
				x,y,z = es.getplayerlocation(userid)
				a = est.makeentity("cycler", "models/combine_helicopter.mdl", x, y, z)
				es.entitysetvalue(a, "classname", "helicopter")
				ang = es.getplayerprop(userid, 'CBaseEntity.m_angRotation')
				es.setindexprop(a, 'CBaseEntity.m_angRotation', ang)
				es.setindexprop(a, "CAI_BaseNPC.m_lifeState", 0)
				es.server.cmd('r_makechat "#255,255,255Kate" "좋아, 나 왔어!"')
				ddd = random.randint(1,2)
				if ddd == 1: es.server.cmd('es_xdelayed 4 r_makechat "#255,255,255Kate" "빨리 달려, 멋쟁이들!"')
				if ddd == 2: es.server.cmd('es_xdelayed 4 r_makechat "#255,255,255Kate" "시간 거의 없어, 서둘러!"')
			if args[0] == "!report_answer":
				gname = "report_steam_%s" %(args[1])
				es.keygroupload(gname, "|rpg/report/msg")
				es.keysetvalue(gname, "report", "answer", args[2])
				es.keygroupsave(gname, "|rpg/report/msg")
				es.keygroupdelete(gname)
				esc.msg("#0,255,255＊ 제보 처리가 되었습니다.(번호 %s)" %(args[1]))
			if args[0] == "!hide_check":
				zeisen_id = int(sv('zeisen_id'))
				check = bot_ishiding(zeisen_id)
				esc.tell(userid, "%s " %(check))
			if args[0] == "!teleport_me":
				es.set("weapon_f", 1)
				for a in playerlib.getPlayerList("#ct"):
					es.setplayerprop(a.userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 2)
				est.teleport(userid, 7554, 4732, -959)
			if args[0] == "!boss_battle_dragon":
				es.set("weapon_f", 1)
				for a in playerlib.getPlayerList("#ct"):
					es.setplayerprop(a.userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 2)
				est.teleport("#c", 2603, -6623, 2112)
				guns = es.createentitylist("weapon_elite")
				for index in guns:
					est.entteleport(index, 2547, -8356, 2104)
			if args[0] == "!guns_me":
				x,y,z = es.getplayerlocation(userid)
				guns = es.createentitylist("weapon_elite")
				for index in guns:
					est.entteleport(index, x, y, z)
			if args[0] == "!boss_battle_knife":
				es.set("weapon_f", 1)
				for a in playerlib.getPlayerList("#ct"):
					es.setplayerprop(a.userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 2)
				est.teleport("#c", -6126, -6121, 5248)
			if args[0] == "!kuria_meet":
				zed_id = es.getuserid("[Human] Zed")
				shark_id = es.getuserid("[Human] Shark")
				es.server.cmd('es_xsexec %s say "아, 그거 들었어? 샤크?"' %(zed_id))
				es.server.cmd('es_xdelayed 4 es_xsexec %s say "왜? 뭔데?"' %(shark_id))
				es.server.cmd('es_xdelayed 8 es_xsexec %s say "요즈음 안내원이 사라지고 있다는 모양이야."' %(zed_id))
				es.server.cmd('es_xdelayed 12 es_xsexec %s say "누가 발견한적이 있었다고 했었는데... 배틀 전장 근처더군."' %(zed_id))
				es.server.cmd('es_xdelayed 16 es_xsexec %s say "뭐야... 그럼... 좋아, 찾아보자!"' %(shark_id))
		if args[0] == "sm":	
			usermsg.echo(userid, 'Unknown command: sm')
			return False
		if args[0] == "drop":
			if es.getplayerteam(userid) == 1:
				if steamid == "STEAM_0018961435":
					es.set("remote_firek2", 1)
					return False
				if steamid == "STEAM_0021059511":
					es.set("remote_firek", 1)
					return False
			if map() == "de_nightfever":
				if est.getgun(userid) == "weapon_awp":
					est.removeweapon(userid, 1)
					keymath(steamid, "player_data", "item29", "+", 1)
					return False
		if args[0] == "nightvision":
			es.server.cmd('es_xsexec %s -sm_entcontrol_grab' %(userid))
			if map() in "de_nightfever":
				alive = isalive(userid)
				if alive == 0:
					if es.getplayerteam(userid) > 1: spawn(userid)
				if alive > 0:
					propid = est.getviewprop(userid)
					npcname = es.entitygetvalue(propid, "classname")
					if "npc" in npcname:
						nl = es.getindexprop(propid, "CBaseEntity.m_vecOrigin").split(",")
						victim_location = vecmath.vector(es.getplayerlocation(userid))
						attacker_location = vecmath.vector(es.getindexprop(propid, "CBaseEntity.m_vecOrigin").split(","))
						distance = vecmath.distance(victim_location, attacker_location) * 0.0254
						if distance <= 2:
							text = random.choice(NPC_LIST[npcname]['text'])
							name = NPC_LIST[npcname]['name']
							if str(text) != "123456789":
								esc.tell(userid, "%s :#default %s" %(name, text))
							popup_s = NPC_LIST[npcname]['send_popup']
							if str(popup_s) != "-1":
								popuplib.unsend(popup_s, userid)
								popuplib.send(popup_s, userid)
							if npcname == "npc_kuria_nightfever":
								npc_xp = int(es.keygetvalue(steamid, "player_data", "%s_xp" %(npcname)))
								npc_msg = 1
								if npc_xp < 0: npc_msg = 0
								if npc_xp >= 10 and npc_xp < 25: npc_msg = 2
								if npc_xp >= 25 and npc_xp < 50: npc_msg = 3
								if npc_msg == 0:
									random_chat = random.choice(["안내해줄 가치가 없군요, 꺼지세요.", "바쁜데 신경쓰이거든? 좀 꺼져줄래?", "참나, 또 당신인가."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 1:
									random_chat = random.choice(["어서오세요! 에에.. 안내원 쿠리아라고 합니다.", "바쁘실텐데 어쩐 용무신지?", "오늘 날이 참 좋네요! 아, 밤이구나."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 2:
									random_chat = random.choice(["다시 오셨군요, 반갑습니다.", "행복한 날을 지내셨으면 좋겠습니다, 아! 전 혼자지만요."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 3:
									random_chat = random.choice(["부탁인데... 이제 그만 와주셨으면 좋겠습니다.", "엄마가 적당한 선까지 그으라고 말씀하셨거든요~", "감사하지만 받는거 다 사양할게요."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								global chat_1
								chat_1 = popuplib.easymenu('chat_1_%s' %(userid), None, chat_select)
								chat_1.settitle("＠ NPC 대화")
								chat_1.addoption(1, "자신의 코드 여부를 물어본다.")
								chat_1.unsend(userid)
								if npc_msg > 0: chat_1.send(userid)
								popuplib.delete('chat_1_%s' %(userid))
							if npcname == "npc_c_nightfever":
								classname = str(es.keygetvalue(steamid, "player_data", "classname"))
								if classname == "human": cirno_1.send(userid)
								if classname == "fairy":
									chat_1 = popuplib.easymenu('chat_cirno_%s' %(userid), None, chat_select)
									chat_1.settitle("＠ 스킬")
									if get_skill(userid, 'item9') > 2:
										chat_1.addoption(1, "The Fairy [유혹의 마도서 3]")
									chat_1.unsend(userid)
									chat_1.send(userid)
									popuplib.delete('chat_cirno_%s' %(userid))
							if npcname == "npc_nosay_nightfever":
								npc_xp = int(es.keygetvalue(steamid, "player_data", "%s_xp" %(npcname)))
								npc_msg = 1
								if npc_xp < 0: npc_msg = 0
								if npc_xp >= 1 and npc_xp < 2: npc_msg = 2
								if npc_xp >= 2 and npc_xp < 3: npc_msg = 3
								if npc_xp >= 3 and npc_xp < 5: npc_msg = 4
								if npc_msg == 0:
									random_chat = random.choice(["....."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 1:
									random_chat = random.choice(["..."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 2:
									random_chat = random.choice(["당신..."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 3:
									random_chat = random.choice(["미안해요..."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 4:
									random_chat = random.choice(["이걸 조금만 더 모으면..."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								chat_1 = popuplib.easymenu('chat_nosay_%s' %(userid), None, chat_select)
								chat_1.settitle("＠ NPC 대화")
								if get_skill(userid, 'item19') > 0:
									chat_1.addoption(1, "당신이 가진 암흑 크리스탈 한개를 그녀에게 건넨다.")
								chat_1.unsend(userid)
								chat_1.send(userid)
								popuplib.delete('chat_nosay_%s' %(userid))
							if npcname == "npc_reisen_nightfever":
								npc_xp = int(es.keygetvalue(steamid, "player_data", "%s_xp" %(npcname)))
								npc_msg = 1
								if npc_xp < 0: npc_msg = 0
								if npc_xp >= 20 and npc_xp < 50: npc_msg = 2
								if npc_msg == 0:
									random_chat = random.choice(["저리 가요!", "오지 말라니까요!", "싫어!"])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								if npc_msg == 1:
									random_chat = random.choice(["누구세요?", "저에게 이상한 관심있으면 사양할게요.", "으으.. 혼자 있고 싶어요."])
									esc.tell(userid, "%s :#default %s" %(name, random_chat))
								chat_1 = popuplib.easymenu('chat_reisen_%s' %(userid), None, chat_select)
								chat_1.settitle("＠ NPC 대화")
								if get_skill(userid, 'item12') > 0:
									chat_1.addoption(1, "당신이 가진 맥주 한개를 그녀에게 건넨다.")
								chat_1.unsend(userid)
								chat_1.send(userid)
								popuplib.delete('chat_reisen_%s' %(userid))
							if npcname == "npc_beer_nightfever":
								chat_1 = popuplib.easymenu('chat_2_%s' %(userid), None, chat_select)
								chat_1.settitle("＠ NPC 대화")
								if get_skill(userid, 'item12') > 0:
									chat_1.addoption(1, "당신이 가진 맥주 한개를 그에게 건넨다.")
								chat_1.unsend(userid)
								chat_1.send(userid)
								popuplib.delete('chat_2_%s' %(userid))
							if npcname == "npc_chall_nightfever":
								chat_1 = popuplib.easymenu('chat_chall_%s' %(userid), None, chat_select)
								chat_1.settitle("＠ NPC 대화")
								if get_skill(userid, 'item16') > 0:
									chat_1.addoption(1, "이벤트 티켓을 사용해 이벤트 맵으로 투표를 시작한다.", 1)
								if get_skill(userid, 'item16') > 0:
									mastery_select = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
									if mastery_select == 2:
										chat_1.addoption(3, "이벤트 티켓을 사용해 Knife와 1:1 배틀을 신청한다.", 1)
									if mastery_select == 3:
										chat_1.addoption(2, "이벤트 티켓을 사용해 Scarecrow와 1:1 배틀을 신청한다.", 1)
								chat_1.unsend(userid)
								chat_1.send(userid)
								popuplib.delete('chat_chall_%s' %(userid))
		if args[0] == "cheer":
			if isalive(userid) == 1:
				if classname_get(steamid, 'classname') == "fairy":
					skillmenu = popuplib.easymenu('bari_%s' %(userid), None, bari_select)
					skillmenu.settitle("＠ 바리게이트 메뉴")
					skillmenu.c_endsep = " \n○ 상황에 맞게 바리케이드를 적극 활용하세요.\n "
					cash = int(es.getplayerprop(userid, 'CCSPlayer.m_iAccount'))
					for a in BARI_LIST:
						gstate = 1
						if cash < int(BARI_LIST[a]['cash']): gstate = 0
						skillmenu.addoption(a, "%s [$%s]" %(a, BARI_LIST[a]['cash']), gstate)
					skillmenu.send(userid)
					popuplib.delete('bari_%s' %(userid))
	return True

def getuseridfromindex(index):
	for userid in es.getUseridList():
		test_index = es.getindexfromhandle(es.getplayerhandle(userid))
		if test_index == index: return userid
	return -1

def getviewplayers(userid):
	es.entsetname(userid, "lookingat")
	for index in es.getEntityIndexes("player"):
 		if es.entitygetvalue(index, "targetname") == "lookingat":
			es.entitysetvalue(index, "targetname", "")
			return es.getUseridList()[index - 1]
	return 0

def send_keyhint():
	if int(sv('remote_enable')) == 0:
		es.set("remote_target", 0)
		es.set("remote_target2", 0)
	es.dbgmsg(0, "[DEBUG] send_keyhint")
	#getid = es.getuserid("Watcher")
	#if getid <= 0:
	#	es.server.cmd('es_xcreatebot "Watcher"')
	if map() in Versus_Maps:
		es.set("level", 6)
	if not map() in Special_Maps:
		zeisen_id = int(sv('zeisen_id'))
		if isalive(zeisen_id):
			for userid in es.getUseridList():
				if es.getplayerteam(userid) == int(sv('humanteam')) and isalive(userid):
					#spe.call("SetBotEnemy", spe.getPlayer(zeisen_id), spe.getPlayer(userid))
					spe.call("Attack", spe.getPlayer(zeisen_id), spe.getPlayer(userid))

	'''
	if "ze_" in map():
		ze_id = es.getuserid("[Helper] ZE")
		x,y,z = es.getplayerlocation(ze_id)
		if ze_id > 0 and isalive(ze_id) and str(z) != "1728.37072754":
			for a in playerlib.getPlayerList("#human,#alive"):
				victim_location = vecmath.vector(es.getplayerlocation(a.userid))
				attacker_location = vecmath.vector(es.getplayerlocation(ze_id))
				distance = vecmath.distance(victim_location, attacker_location) * 0.0254
				if distance <= 5:
					es.server.cmd('damage %s 25 32 %s' %(a.userid, ze_id))]
	'''
	'''
	if not map() in Special_Maps:
		if "cs_" in map():
			hostage_index = es.getentityindex("hostage_entity")
			if hostage_index > 0:
				follower = int(es.getindexprop(hostage_index, "CHostage.m_leader"))
				if follower <= 0:
					loc = es.getindexprop(hostage_index, "CHostage.baseclass.baseclass.baseclass.baseclass.baseclass.m_vecOrigin")
					if str(loc) != str(sv('hostage_loc')):
						es.remove("hostage_entity")
						index = es.createentity("hostage_entity")
						es.spawnentity(index)
						cm = es.precachemodel("models/player/reisenbot/cirno/cirno.mdl")
						es.setindexprop(index, "CBaseEntity.m_nModelIndex", cm)
						est.setentitycolor(index, 255, 255, 255, 255)
						es.setindexprop(index, "CHostage.baseclass.baseclass.baseclass.baseclass.m_flModelScale", 0.75)
						es.setindexprop(index, "CHostage.m_lifeState", 0)
						hostage_locc = str(sv('hostage_loc'))
						hostage_loc = hostage_locc.split(",")
						est.entteleport(index, hostage_loc[0], hostage_loc[1], hostage_loc[2])
						#es.setindexprop(index, "CHostage.baseclass.baseclass.baseclass.baseclass.baseclass.m_vecOrigin", sv('hostage_loc'))
	'''
	if map() == "ba_quartzy":
		getid = es.getuserid("[A Rank] Pery")
		if est.gethealth(getid) <= 175000:
			if random.randint(1,50) == 22:
				pery_forward = int(sv('pery_forward'))
				pery_forward *= -1
				es.set("pery_forward", pery_forward)
				if pery_forward < 0:
					npc_msg("#255,0,0Pery", "포워드 리버스.")
				else:
					npc_msg("#255,0,0Pery", "때론 리버스-리버스가 필요하지.")
		for f_userid in es.getUseridList():
			if not es.isbot(f_userid) and isalive(f_userid):
				if int(sv('event_line')) >= 8:
					for a in playerlib.getPlayerList("#human"):
						x,y,z = es.getplayerlocation(a.userid)
						if float(z) >= 195: est.slay(a.userid)
			if isalive(f_userid) and es.getplayerteam(f_userid) >= 2:
				x,y,z = es.getplayerlocation(f_userid)
				event_x,event_y,event_z = es.getplayerlocation(getid)
				event_z += 30
				v1 = "%s,%s,%s" %(x, y, z)
				v2 = "%s,%s,%s" %(event_x, event_y, event_z)
				lasermodel = es.precachemodel("effects/laser1.vmt")
				es.effect("beam", v1, v2, lasermodel, lasermodel, 0, 0, 0.2, 1, 1, 0, 1, 255, 255, 255, 255, 1)
	if map() == "de_nightfever":
		recording()
		#nt = int(sv('nightfever_time'))
		#if nt > 1 and nt < 999:
		#	if random.randint(1,100) == 1:
		#		nipper_start()
		#		gamethread.delayed(35, nipper_hardcore_1, ())
		#pa = es.createentityindexlist("prop_physics_multiplayer")
		#count = 0
		#for a in pa:
		#	health = es.getindexprop(a, "CBasePlayer.m_iHealth")
		#	if health > 0:
		#		count += 1
		nightfever_time = svmath("nightfever_time", "-", 1)
		if str(sv('sv_password')) == "nipperz":
			est.remove("shotgun")
			recording()
			getid = es.getuserid("[Z Rank] Kell")
			if getid > 0:
				for index in spe.getWeaponIndexList(getid):
					est.setentitycolor(index, 0, 0, 0, 0)
			getid = es.getuserid("[Z Rank] Burnman")
			if getid > 0:
				c4_index = es.getentityindex("weapon_c4")
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0)
				es.emitsound("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0)
				es.emitsound("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0)
				es.emitsound("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0)
				es.emitsound("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0)
				gamethread.delayed(0.25, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.25, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.25, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.25, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.25, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.5, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.5, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.5, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.5, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.5, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.75, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.75, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.75, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.75, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				gamethread.delayed(0.75, es.emitsound, ("player", getid, "zeisenproject_3/autosounds/132.mp3", 1.0, 1.0))
				view_target = est.getviewprop(getid)
				if view_target > 0:
					classname = es.entitygetvalue(view_target, 'classname')
					if classname == "player":
						view_userid = getuseridfromindex(view_target)
						if not es.isbot(view_userid):
							if es.getplayerteam(view_userid) > 1:
								est.setarmor(view_userid, 0)
								est.burn(view_userid, 1)
								victim_location = vecmath.vector(es.getplayerlocation(view_userid))
								attacker_location = vecmath.vector(es.getplayerlocation(getid))
								distance = vecmath.distance(victim_location, attacker_location) * 0.0254
								es.cexec(view_userid, "r_screenoverlay debug/yuv.vmt")
								gamethread.delayed(2, es.cexec, (view_userid, "r_screenoverlay null"))
								es.playsound(view_userid, "zeisenproject_3/autosounds/man/sc%s.mp3" %(random.randint(1,2)), 1.0)
								if distance <= 5: est.sethealth(view_userid, 0)
			getid = es.getuserid("[Z Rank] Waterman")
			if getid > 0:
				c4_index = es.getentityindex("weapon_c4")
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				es.emitsound("entity", c4_index, "ui/buttonclick.wav", 1.0, 1.0)
				view_target = est.getviewprop(getid)
				if view_target > 0:
					classname = es.entitygetvalue(view_target, 'classname')
					if classname == "player":
						view_userid = getuseridfromindex(view_target)
						if not es.isbot(view_userid):
							if es.getplayerteam(view_userid) > 1:
								est.setarmor(view_userid, 0)
								victim_location = vecmath.vector(es.getplayerlocation(view_userid))
								attacker_location = vecmath.vector(es.getplayerlocation(getid))
								distance = vecmath.distance(victim_location, attacker_location) * 0.0254
								es.cexec(view_userid, "r_screenoverlay debug/yuv.vmt")
								gamethread.delayed(2, es.cexec, (view_userid, "r_screenoverlay null"))
								es.playsound(view_userid, "zeisenproject_3/autosounds/man/sc%s.mp3" %(random.randint(1,2)), 1.0)
								if distance <= 5: est.slay(view_userid)
		if str(sv('sv_password')) != "nipperz":
			for a in playerlib.getPlayerList("#human,#alive"):
				steamid = getplayerzeisenid(a.userid)
				x,y,z = es.getplayerlocation(a.userid)
				if steamid != "STEAM_0142954927":
					if str(z) == "384.03125" or str(z) == "430.908081055" or str(z) == "424.03125":
						est.teleport(a.userid, 1865, 2150, 300)
						esc.tell(a.userid, "#255,255,255＊ 이미 그 장소는 누군가의 소유물입니다.")
			if nightfever_time <= 0:
				es.set("nightfever_time", 999)
				esc.msg("#255,255,255황혼주점의 문이 닫혔습니다!")
				es.server.cmd('es_xdelayed 3 changelevel %s' %(sv('nightfever_nextmap')))
			if nightfever_time > 0:
				nextmap = sv('nightfever_nextmap')
				for b in playerlib.getPlayerList("#human"): usermsg.hudhint(b.userid, "＠ 황혼주점(황혼 이자카야)\n \n폐점 예정시간 : %s 초 후\n다음 맵 예정 : %s\n \nN키(나이트 비전 키)를 이용하여 NPC와 대화를 할수 있습니다." %(nightfever_time, nextmap))
	for userid in es.getUseridList():
		if not es.isbot(userid):
			if int(sv('allfade')) == 2:
				est.fade(userid, 1, 0.5, 1.15, 255, 255, 255, 255)
			if int(sv('allfade')) == 1:
				est.fade(userid, 0, 0.15, 1.15, 0, 0, 0, 255)
			steamid = getplayerzeisenid(userid)
			if int(es.getplayerteam(userid)) >= 2:
				keymath(steamid, "player_data", "connect_point", "+", 1)
			else:
				if not steamid in "STEAM_0021059511, STEAM_0077456544, STEAM_0027045397":
					spectime = spec_time[userid] + 1
					spec_time[userid] = spectime
					if int(sv('players_count')) >= 12:
						if int(spectime) >= 301: es.server.cmd('kickid %s "잠수 금지(5분 초과)"' %(userid))
			mastery = mastery_name(steamid)
			classname = getmastery_keyhint(steamid)
			human_xp = get_skill(userid, "human_xp")
			skillpoint = es.keygetvalue(steamid, "player_data", "skillpoint")
			stetpoint = es.keygetvalue(steamid, "player_data", "stetpoint")
			mastery_xp = es.keygetvalue(steamid, "player_data", "mastery_xp")
			xp = get_skill(userid, "xp")
			nextxp = get_skill(userid, "nextxp")
			cs = get_skill(userid, "cs")
			money = get_skill(userid, "money")
			level = get_skill(userid, "level")
			connect_point = get_skill(userid, "connect_point")
			partner = str(es.keygetvalue(steamid, "player_data", "partner"))
			if isalive(userid):
				skill = mastery_skillget(userid, 2, "mastery_skill2")
				if skill > 0:
					another_skill = mastery_skillget(userid, 2, "mastery_skill1")
					maxg_health = int(max_health[userid])
					health = gethealth(userid)
					if float(health) < float(maxg_health):
						healthadd(userid, skill)
			if partner.lower() == "none":
				partner_username = "없음"
				partner_state = "＊"
			else:
				partner = partner.replace(":", "")
				checkm = es.exists("key", partner, "player_data")
				if checkm == 0: es.keygroupload(partner, "|rpg/player_data")
				partner_username = es.keygetvalue(partner, "player_data", "username")
				partner_to_partner = es.keygetvalue(partner, "player_data", "partner")
				if partner_to_partner == steamid:
					partner_state = "♥"
				else:
					partner_state = "♡"
				if checkm == 0: es.keygroupdelete(partner)
			mastery = mastery.replace(" 마스터리", "")
			if map() == "de_nightfever":
				if int(sv('story_kk')) == 1:
					random_x = float(random.randint(0,100)) / 100
					random_y = float(random.randint(0,100)) / 100
					random_msg = random.choice(["더러워. ", "뭐야? ", "저질. ", "이상해. ", "괴물이야. "])
					usermsg.hudmsg(userid, random_msg, x=random_x, y=random_y, b1=0, g1=0)
			if not "ze_" in map(): usermsg.keyhint(userid, "레벨 : %s\n경험치 : %s / %s\n \n파트너(%s) : %s\n특화 마스터리 : %s (%s)\n종족 : %s\n \n스킬 포인트 : %s │ 스텟 포인트 : %s\n인기도 : %s │ Money : %s엔 │ CS : %s\n접속 포인트 : %s" %(level, xp, nextxp, partner_state, partner_username, mastery, mastery_xp, classname, skillpoint, stetpoint, human_xp, money, cs, connect_point))
			if isalive(userid):
				dollar_regen = float(es.keygetvalue(steamid, "player_data", "dollar_regen"))
				if dollar_regen > 0: est.cashadd(userid, (dollar_regen * 1.5))
			if xp >= nextxp:
				keymath(steamid, "player_data", "xp", "-", nextxp)
				level += 1
				if level <= 10: nextxp += 20
				if level > 10 and level <= 20: nextxp += 30
				if level > 20 and level <= 30: nextxp += 50
				if level > 30 and level <= 40: nextxp += 80
				if level > 40 and level <= 50: nextxp += 145
				if level > 50 and level <= 60: nextxp += 205
				if level > 60 and level <= 70: nextxp += 410
				if level > 70 and level <= 80: nextxp += 811
				if level > 80 and level <= 90: nextxp += 1612
				if level > 90 and level <= 99: nextxp += 3244
				if level >= 100: nextxp += 99999
				es.keysetvalue(steamid, "player_data", "nextxp", nextxp)
				es.keysetvalue(steamid, "player_data", "level", level)
				keymath(steamid, "player_data", "skillpoint", "+", 1)
				keymath(steamid, "player_data", "stetpoint", "+", 1)
				playsound(Levelup_Sound)
				esc.msg("#255,255,255＊ #blue %s 유저#255,255,255님이 %s 레벨이 되었습니다." %(es.getplayername(userid), level))
			if str(sv('sv_password')) == "nipperz":
				what_ent = int(sv('what_ent'))
				if what_ent > 0:
					x,y,z = es.getplayerlocation(userid)
					est.entteleport(what_ent, x, y, z)
	getid = es.getuserid("[C Rank] Zeisen")
	if getid > 0:
		if random.randint(1,100) == 50: es.server.cmd('r_sendvoice %s zeisenproject_3/autosounds/zeisen/negative%s.wav' %(getid, random.randint(1,6)))
	for a in WEAPON_BOT:
		zeisen_id = es.getuserid(a)
		if zeisen_id > 0 and es.isbot(zeisen_id) and isalive(zeisen_id):
			if est.getgun(zeisen_id) != "weapon_c4":
				first_check = est.getweaponindex(zeisen_id, 1)
				if first_check > 0:
					weapon_name = es.entitygetvalue(first_check, "classname")
					es.server.cmd('es_xsexec %s use "%s"' %(zeisen_id, weapon_name))
				else:
					first_check = est.getweaponindex(zeisen_id, 2)
					if first_check > 0:
						weapon_name = es.entitygetvalue(first_check, "classname")
						es.server.cmd('es_xsexec %s use "%s"' %(zeisen_id, weapon_name))

def es_map_start(ev):
	es.unload("wS_Hide_Radar")
	#es.doblock("rpg/rank_level_set")
	es.server.cmd('bot_quota 0')
	es.server.cmd('est4css_nosayfilter 1')
	es.server.cmd('est_enable_PerUserKeyEvent 0')
	soundtrack = int(sv('soundtrack')) + 1
	es.set("event_line", 0)
	check = est.fileexists("sound/zeisenproject_3/soundtrack_2/track_%s/battle1.mp3" %(soundtrack))
	if check == 0:
		es.set("soundtrack", 1)
		soundtrack = 1
	else: es.set("soundtrack", soundtrack)
	if "de_" in map():
		es.set("humanteam", 2)
		es.set("zombieteam", 3)
	if "cs_" in map():
		es.set("humanteam", 3)
		es.set("zombieteam", 2)
	if "ze_" in map():
		es.set("humanteam", 3)
		es.set("zombieteam", 2)
	es.server.cmd('es_xunload gg_ffa_bots')
	if map() != "de_nightfever": es.server.cmd('sm plugins unload entcontrol')
	if not "ze_" in map(): es.server.cmd('sm plugins unload zombiereloaded')
	if int(sv('humanteam')) == 2: es.server.cmd('mp_humanteam t')
	if int(sv('humanteam')) == 3: es.server.cmd('mp_humanteam ct')
	if "ze_" in map(): es.server.cmd('mp_humanteam any')
	Soundtrack_Opening = "zeisenproject_3/autosounds/default_opening.mp3"
	Soundtrack_Ending = "zeisenproject_3/autosounds/default_ending.mp3"
	Soundtrack_Mission = "zeisenproject_3/autosounds/default_mission.mp3"
	Soundtrack_Lose = "zeisenproject_3/autosounds/default_lose.mp3"
	Soundtrack_Win = "zeisenproject_3/autosounds/default_win.mp3"
	if map() in Special_Maps:
		if "ze_" in map():
			Soundtrack_Opening = "NULL"
			Soundtrack_Ending = "NULL"
			Soundtrack_Mission = "NULL"
			Soundtrack_Lose = "NULL"
			Soundtrack_Win = "NULL"
			Soundtrack_Battle1 = "NULL"
		if map() == "de_season":
			Soundtrack_Opening = "NULL"
			Soundtrack_Ending = "NULL"
			Soundtrack_Mission = "NULL"
			Soundtrack_Lose = "NULL"
			Soundtrack_Win = "NULL"
			Soundtrack_Battle1 = "NULL"
		if map() == "cs_office_FEAR_night":
			Soundtrack_Opening = "NULL"
			Soundtrack_Ending = "NULL"
			Soundtrack_Mission = "NULL"
			Soundtrack_Lose = "NULL"
			Soundtrack_Win = "NULL"
			Soundtrack_Battle1 = "NULL"
		if map() == "de_nightfever":
			Soundtrack_Opening = "zeisenproject_3/autosounds/nightfever_issac.mp3"
			Soundtrack_Ending = "NULL"
			Soundtrack_Mission = "NULL"
			Soundtrack_Lose = "NULL"
			Soundtrack_Win = "NULL"
			Soundtrack_Battle1 = "NULL"
			es.set("mp_freezetime", 0)
			es.set("nightfever_nextmap", "de_ahoferno_s2")
		if map() == "cs_office":
			es.server.cmd('bot_difficulty 3')
			es.server.cmd('bot_quota 999')
			es.server.cmd('bot_add "[Human] Knife"')
		if map() == "cs_gentech_final":
			es.server.cmd('bot_difficulty 3')
			es.server.cmd('bot_quota 999')
			es.server.cmd('bot_add "[Human] Scarecrow"')
	else:
		es.set("mp_freezetime", 60)
		check = est.fileexists("sound/zeisenproject_3/soundtrack_2/track_%s/opening.mp3" %(soundtrack))
		if check == 1: Soundtrack_Opening = "zeisenproject_3/soundtrack_2/track_%s/opening.mp3" %(soundtrack)
		check = est.fileexists("sound/zeisenproject_3/soundtrack_2/track_%s/ending.mp3" %(soundtrack))
		if check == 1: Soundtrack_Ending = "zeisenproject_3/soundtrack_2/track_%s/ending.mp3" %(soundtrack)
		check = est.fileexists("sound/zeisenproject_3/soundtrack_2/track_%s/mission.mp3" %(soundtrack))
		if check == 1: Soundtrack_Mission = "zeisenproject_3/soundtrack_2/track_%s/mission.mp3" %(soundtrack)
		check = est.fileexists("sound/zeisenproject_3/soundtrack_2/track_%s/lose.mp3" %(soundtrack))
		if check == 1: Soundtrack_Lose = "zeisenproject_3/soundtrack_2/track_%s/lose.mp3" %(soundtrack)
		check = est.fileexists("sound/zeisenproject_3/soundtrack_2/track_%s/win.mp3" %(soundtrack))
		if check == 1: Soundtrack_Win = "zeisenproject_3/soundtrack_2/track_%s/win.mp3" %(soundtrack)
		es.server.cmd('bot_difficulty 3')
		es.server.cmd('bot_quota 999')
		es.server.cmd('bot_add "[Human] Zed"')
		es.server.cmd('bot_add "[Human] Shark"')
	es.set("soundtrack_opening", Soundtrack_Opening)
	es.set("soundtrack_ending", Soundtrack_Ending)
	es.set("soundtrack_mission", Soundtrack_Mission)
	es.set("soundtrack_win", Soundtrack_Win)
	es.set("soundtrack_lose", Soundtrack_Lose)
	es.set("round", 1)
	if int(sv('level')) >= 10:
		es.set("level", 9)

def round_end(ev):
	es.set("hostage_follower", 0)
	if "ze_" in map():
		es.server.cmd('mp_humanteam any')
	es.set("before_zombie_userid", 0)
	if int(sv('zombie_userid')) > 0:
		es.set("before_zombie_userid", sv('zombie_userid'))
	es.set("zombie_userid", 0)
	allstopsound()
	es.remove("weapon_c4")
	winner = int(ev['winner'])
	if winner == 2: est.slay("#c!d")
	if winner == 3: est.slay("#t!d")
	if not map() in Special_Maps:
		if float(sv('mp_roundtime')) >= 3: es.forcevalue("mp_roundtime", 2.5)
	if map() == "de_season":
		if int(sv('event_line')) >= 1:
			es.set("event_line", 1)
	if map() == "cs_office_FEAR_night":
		for a in playerlib.getPlayerList("#bot"):
			if es.getplayername(a.userid) == "[E Rank] Alma": gamethread.delayed(4.95, est.team, (a.userid, 3))
	if winner > 1:
		round = svmath("round", "+", 1)
		if int(sv('mp_freezetime')) >= 11: es.set("mp_freezetime", 10)
	if winner == int(sv('humanteam')):
		gamethread.delayed(0.4, est.play, ("#h", sv('soundtrack_win')))
		level = svmath("level", "+", 1)
		if level >= 10 and round == 8: level = 9
		if round <= 7:
			if level == 10:
				es.forcevalue("mp_roundtime", 7.5)
				es.botsetvalue(sv('zeisen_id'), "name", "[B Rank] Pradoster")
			if level == 11:
				es.set("level", 7)
				endthegame()	
				#es.forcevalue("mp_freezetime", 56)
				#es.botsetvalue(sv('zeisen_id'), "name", "[A Rank] Kuria")
	if winner == int(sv('zombieteam')):
		gamethread.delayed(0.4, est.play, ("#h", sv('soundtrack_lose')))
		level = svmath("level", "-", 1)
		if level <= 0: svmath("level", "=", 1)
		if level >= 9:
			es.set("round", 8)
			es.set("level", 1)
	est.setentitycolor(sv('zeisen_gun'), 255, 255, 255, 255)

def partner_select(userid, choice, popupname):
	steamid = getplayerzeisenid(userid)
	if steamid != choice:
		username = es.getplayername(userid)
		keymath(steamid, "player_data", "item18", "-", 1)
		if choice != "None":
			es.keysetvalue(steamid, "player_data", "partner", choice)	
			partner_name = es.keygetvalue(choice, "player_data", "username")	
			esc.msg("#blue %s 유저#255,255,255가#red %s유저#255,255,255를 파트너로 설정했습니다." %(username, partner_name))
		else:
			es.keysetvalue(steamid, "player_data", "partner", choice)
			esc.msg("#blue %s 유저#255,255,255가 파트너를 해지했습니다." %(username))

def player_say(ev):
	userid = int(ev['userid'])
	if userid == 0:
		text = str(ev['text'])
		if text == "***YOU ARE THE ULTIMATE ZOMBIE ESCAPE MASTER***":
			if int(sv('event_line')) == 0:
				es.set("event_line", 1)
				clear_ze()
				endthegame()
		if text == "***SOMEONE MUST JUMP INTO THE CORE***":
			es.forcevalue("sv_friction", 0.01)
		#if text == "***THE NUKE HAS EXPLODED***":
		#	gamethread.delayed(8, est.slay, ("#t"))
		if text == "** Congratulations - u won [GODMODE] **":
			endthegame()
			for a in playerlib.getPlayerList("#human"):
				if es.getplayerteam(a.userid) > 1:
					steamid = getplayerzeisenid(a.userid)
					username = es.getplayername(a.userid)
					if random.randint(1,10) != 7:
						keymath(steamid, "player_data", "item19", "+", 1)
						esc.msg("#blue %s 유저#255,255,255님이 갓 모드 클리어로 #purple암흑 크리스탈을 1개 받았습니다." %(username))
					else:
						if random.randint(1,2) == 1:
							keymath(steamid, "player_data", "item21", "+", 1)
							esc.msg("#blue %s 유저#255,255,255님이 갓 모드 클리어로 #purple파라노야 코스프레를 1개 받았습니다." %(username))
						else:
							keymath(steamid, "player_data", "item24", "+", 1)
							esc.msg("#blue %s 유저#255,255,255님이 갓 모드 클리어로 #55,255,55테이지 코스프레를 1개 받았습니다." %(username))

def sayFilter(userid, text, teamonly):
	if userid > 1:
		username = es.getplayername(userid)
		steamid = es.getplayersteamid(userid)
		username = username.replace('"', '')
		username = username.replace("‏", "?")
		team = es.getplayerprop(userid, "CBaseEntity.m_iTeamNum")
		text = text[1:-1]
		text = text.replace('"', "''")
		rawtext = text.replace('"', "")
		if steamid != "BOT":
			if sayok[userid] == 1:
				if map() == "ba_quartzy":
					if str(sv('pery_say')) == "-1": est.slay(userid)
				if steamid != "STEAM_0:0:21059511": sayok[userid] = 0
				gamethread.delayed(0.5, say_unblock, (userid))
				rawtext = rawtext.replace("#", "＃")
				rawtext = rawtext.replace("", "")
				rawtext = rawtext.replace("\\", "/")
				rawtext = rawtext.replace("->", "→")
				rawtext = rawtext.replace("<-", "←")
				if not "＃_" in rawtext:
					if int(sv('connect_ok')) == 1:
						serverr = serverlib.SourceServer('218.54.46.83', 27050) # Connect to server (network, port)
						serverr.setRCONPassword('kafkaz') # Submit the RCON password
						serverr.rcon('es_xsoon esc_msg "#red%s :#default %s"' %(username, rawtext)) # Send an RCON command
						serverr.disconnect() # Disconnect from server
				steamid = steamid.replace(":", "")
				level = int(es.keygetvalue(steamid, "player_data", "level"))
				classname = getmastery_saytext(steamid)
				mastery = mastery_name_msg(steamid)
				callname = es.keygetvalue(steamid, "player_data", "callname")
				if es.getplayerteam(userid) <= 1: namecolor = "white"
				if es.getplayerteam(userid) == 2: namecolor = "red"
				if es.getplayerteam(userid) == 3: namecolor = "blue"
				realok = 1
				rawtext_args = rawtext.split()
				if rawtext_args[0] == "!초대":
					if steamid == "STEAM_0134438679":
						id = int(rawtext_args[1])
						est.teleport(id, -1310, 1520, 80)
						realok = 0
                                player_level_color = getlevelcolor(level)
				if realok == 1:
                                        esc.msg("%s%s#%s[Lv.%s %s#%s]#%s %s #default: %s" %(callname, classname, player_level_color, level, mastery, player_level_color, namecolor, username, rawtext))
					classname = classname.replace(" ", "")
					#esc.msg("#255,255,255「%s%s#%s#255,255,255」#%s%s #default: %s" %(callname, classname, player_level_color, namecolor, username, rawtext))
				if rawtext == "!랜덤 러시안 룰렛 25%":
					if userid == 54 or userid == 6:
						esc.msg("#255,255,255%s님이 도박을 시도합니다..." %(username))
						playsound("weapons/deagle/de_clipin.wav")
						playsound("weapons/deagle/de_clipin.wav")
						playsound("weapons/deagle/de_clipin.wav")
						random_max = 4
						if random.randint(1,random_max) == 1:
							gamethread.delayed(5, est.slay, (userid))
							gamethread.delayed(5, est.play, ("#h", "weapons/deagle/deagle-1.wav"))
						else:
							gamethread.delayed(5, est.play, ("#h", "weapons/clipempty_pistol.wav"))
							gamethread.delayed(5, est.play, ("#h", "weapons/clipempty_pistol.wav"))
							gamethread.delayed(5, est.play, ("#h", "weapons/clipempty_pistol.wav"))
							gamethread.delayed(5, est.play, ("#h", "weapons/clipempty_pistol.wav"))
							gamethread.delayed(5, est.play, ("#h", "weapons/clipempty_pistol.wav"))
				if rawtext_args[0] == "!profile_say":
					real_say = rawtext.replace("!profile_say ", "")
					es.keysetvalue(steamid, "player_data", "say", "%s " %(real_say))
				if rawtext == "!정보":
					info_popup = popuplib.easymenu('sinfo_%s' %(userid), None, sinfo_select)
					info_popup.settitle("＠ 플레이어 정보")
					for info_userid in es.getUseridList():
						info_steamid = es.getplayersteamid(info_userid)
						if info_steamid != "BOT":
							info_username = es.getplayername(info_userid)
							info_popup.addoption(info_steamid, info_username)
					info_popup.send(userid)
					popuplib.delete('sinfo_%s' %(userid))
				if rawtext == "!랭킹":
					est.motd_w(userid, "Ranking", ".", "http://boksu.crplab.kr/zeisen/hlstats.php?game=css")
				if rawtext == "!랜덤 계산":
					A = random.randint(1,1999)
					B = random.randint(1,1999)
					esc.msg("#255,255,255＊ 계산 : %s + %s = ?" %(A, B))
				#if rawtext == "!복구받기": backup_player(userid)
				if rawtext == "!세이브":
					if str(sv('sv_password')) != "nipperz": es.keygroupsave(steamid, "|rpg/player_data")
					else: esc.tell(userid, "#255,0,0작동이 중지되었습니다.")
				if rawtext == "!랜덤 포커결과":
					cards = 0
					small_number = 999
					big_number = 0
					small_number_p = 999
					big_number_p = 0
					while cards < 3:
						cards += 1
						numberp = random.randint(1,13)
						if numberp > big_number:
							big_number = numberp
							big_number_p = numberp
							if big_number == 1: big_number_p = "A"
							if big_number == 11: big_number_p = "J"
							if big_number == 12: big_number_p = "Q"
							if big_number == 13: big_number_p = "K"
						if numberp <= small_number:
							small_number = numberp
							small_number_p = numberp
							if small_number == 1: small_number_p = "A"
							if small_number == 11: small_number_p = "J"
							if small_number == 12: small_number_p = "Q"
							if small_number == 13: small_number_p = "K"
						total_numberp = big_number + small_number
					esc.msg("#255,255,255＊ 결과 : %s (%s+%s)" %(total_numberp, big_number_p, small_number_p))
				if rawtext == "!랜덤 포커":
					color = random.choice(["스페이드", "클로버", "하트", "다이아몬드"])
					#JQK
					numberp = random.randint(1,13)
					number_print = numberp
					if number_print == 1: number_print = "A"
					if number_print == 11: number_print = "J"
					if number_print == 12: number_print = "Q"
					if number_print == 13: number_print = "K"
					esc.msg("#255,255,255＊ 카드 결과 : %s %s" %(color, number_print))
				if rawtext == "!랜덤 주사위":
					to = random.randint(1,6)
					esc.msg("#255,255,255＊ 결과 : %s" %(to))
				if rawtext == "!랜덤 홀짝":
					fff = random.randint(1,100)
					if fff <= 50:
						esc.msg("#255,255,255＊ 결과 : 홀")
					else:
						esc.msg("#255,255,255＊ 결과 : 짝")
				#if rawtext == "!motd" or rawtext == "motd": es.server.cmd('es_xsexec %s motd' %(userid))
				if rawtext == "!리스트":
					for a in playerlib.getPlayerList("#human"):
						name = es.getplayername(a.userid)
						name = name.replace('"', '')
						esc.tell(userid, "#255,255,255[%s]#blue %s" %(a.userid, name))
				if rawtext_args[0] == "!볼륨":
					volume = float(rawtext_args[1])
					if volume >= 0 and volume <= 1:
						es.keysetvalue(steamid, "player_data", "volume", volume)
						esc.tell(userid, "#255,255,255성공적으로 BGM, SE 사운드의 볼륨이 변경되었습니다.")
				if rawtext_args[0] == "!buy" or rawtext_args[0] == "buy":
					if int(sv('buy_time')) == 1:
						cost = 0
						weapon = 0
						if "ak" in rawtext_args[1]:
							cost = 2500
							weapon = "weapon_ak47"
						if "m4" in rawtext_args[1]:
							cost = 3100
							weapon = "weapon_m4a1"
						if "tmp" in rawtext_args[1]:
							cost = 1250
							weapon = "weapon_tmp"
						if "mac" in rawtext_args[1]:
							cost = 1400
							weapon = "weapon_mac10"
						if "fiveseven" in rawtext_args[1] or '57' in rawtext_args[1]:
							cost = 750
							weapon = "weapon_fiveseven"
						if "famas" in rawtext_args[1]:
							cost = 2250
							weapon = "weapon_famas"
						if "galil" in rawtext_args[1]:
							cost = 2000
							weapon = "weapon_galil"
						if "aug" in rawtext_args[1]:
							cost = 3500
							weapon = "weapon_aug"
						if "sg552" in rawtext_args[1]:
							cost = 3500
							weapon = "weapon_sg552"
						if "elite" in rawtext_args[1]:
							cost = 800
							weapon = "weapon_elite"
						if int(es.keygetvalue(steamid, "player_data", "skill13")) <= 0:
							esc.tell(userid, "#255,255,255＊ 당신은 구매가 불가능합니다. Skill이 필요합니다.")
							cost = 0
						if int(cost) > 0:
							if int(es.getplayerprop(userid, "CCSPlayer.m_iAccount")) >= int(cost):
								est.cash(userid, "-", cost)
								est.give(userid, weapon)
				if rawtext_args[0] == "!거래":
					wg_id = int(rawtext_args[1])
					keyname = ITEM_LIST[str(rawtext_args[2])]['itemkeyname']
					much = int(rawtext_args[3])
					if int(es.keygetvalue(steamid, "player_data", keyname)) >= much and much > 0:
						trade_enable = ITEM_LIST[str(rawtext_args[2])]['trade']
						if trade_enable:
							check = es.getplayerhandle(wg_id)
							if check > 0 and not es.isbot(wg_id):
								esc.msg("#blue %s 유저#255,255,255가#blue %s 유저#255,255,255에게#gold %s 아이템#255,255,255을#gold %s#255,255,255개 만큼 주었습니다." %(es.getplayername(userid), es.getplayername(wg_id), ITEM_LIST[rawtext_args[2]]['itemrealname'], much))
								wg_steamid = getplayerzeisenid(wg_id)
								keymath(steamid, "player_data", keyname, '-', much)
								keymath(wg_steamid, "player_data", keyname, '+', much)
						else: esc.tell(userid, "#255,255,255＊ 이 아이템은 거래가 불가능합니다.")
				if steamid == "STEAM_0021059511":
					if rawtext == "!helpz":
						esc.tell(userid, "#255,255,255!make_npc 모델 이름 모션")
					if rawtext_args[0] == "!make_npc":
						model = rawtext_args[1]
						if model == "!robot": model = "props/cs_office/vending_machine"
						name = rawtext_args[2]
						seq = rawtext_args[3]
						ang = es.getplayerprop(userid, "CCSPlayer.m_angEyeAngles[1]")
						x,y,z = es.getplayerlocation(userid)
						esc.tell(userid, "create_npc('%s', '%s', %s, %s, %s, %s, 255, 255, 255, 255, %s)" %(model, name, seq, x, y, z, ang))
				if rawtext == "!로켓":
					est.rocket(userid)
				if rawtext == "!스킬": rpgmenu_select(userid, "스킬", 0)
				if rawtext == "!스텟": rpgmenu_select(userid, "스텟", 0)
				if rawtext == "!인벤토리": rpgmenu_select(userid, "인벤토리", 0)
				if rawtext == "!메뉴" or rawtext == "!menu" or rawtext == "rpgmenu": rpgmenu.send(userid)
				if rawtext == "!초기화(경고없음)": reset_player(steamid)
				#if rawtext == "!다음맵" or rawtext == "nextmap": esc.msg("#255,255,255＊ 다음 예정 맵은 %s 입니다." %(sv('override')))
				if rawtext.lower() == "noo": es.server.cmd('es_xsoon r_sendvoice %s bot/noo.wav' %(userid))
				if rawtext == "나이스샷" or rawtext == "샷" or rawtext == "나이스": es.server.cmd('es_xsoon r_sendvoice %s bot/nice_shot.wav' %(userid))
				if rawtext == "굿샷" or rawtext == "굿숏": es.server.cmd('es_xsoon r_sendvoice %s bot/good_shot.wav' %(userid))
				if rawtext == "내눈": es.server.cmd('es_xsoon r_sendvoice %s bot/my_eyes.wav' %(userid))
				if rawtext.lower() == "ltw": es.server.cmd('es_xsoon r_sendvoice %s bot/lead_the_way.wav' %(userid))
				if rawtext.lower() == "clear": es.server.cmd('es_xsoon r_sendvoice %s bot/clear.wav' %(userid))
				if rawtext.lower() == "ok" or rawtext == "오케이" or rawtext == "오케": es.server.cmd('es_xsoon r_sendvoice %s bot/ok.wav' %(userid))
				if rawtext.lower() == "a": es.server.cmd('es_xsoon r_sendvoice %s bot/a.wav' %(userid))
				if rawtext.lower() == "b": es.server.cmd('es_xsoon r_sendvoice %s bot/b.wav' %(userid))
				if rawtext.lower() == "c": es.server.cmd('es_xsoon r_sendvoice %s bot/c.wav' %(userid))
				if rawtext == "a설": playsound("bot/planting_at_a.wav")
				if rawtext == "b설": playsound("bot/planting_at_b.wav")
				if rawtext == "c설": playsound("bot/planting_at_c.wav")
				if rawtext.lower() == "ohmygod": es.server.cmd('es_xsoon r_sendvoice %s bot/oh_my_god.wav' %(userid))
				if rawtext.lower() == "yea": es.server.cmd('es_xsoon r_sendvoice %s bot/yea_baby.wav' %(userid))
				if rawtext.lower() == "na": es.server.cmd('es_xsoon r_sendvoice %s bot/naa.wav' %(userid))
				if rawtext == "YES" or rawtext == "예스": es.server.cmd('es_xsoon r_sendvoice %s bot/yesss2.wav' %(userid))
				if rawtext == "no" or rawtext == "ㄴ": es.server.cmd('es_xsoon r_sendvoice %s bot/no.wav' %(userid))
				if rawtext == "oh": es.server.cmd('es_xsoon r_sendvoice %s bot/oh.wav' %(userid))
				if rawtext == "NOO": es.server.cmd('es_xsoon r_sendvoice %s bot/noo.wav' %(userid))
				if rawtext == "nosir": es.server.cmd('es_xsoon r_sendvoice %s bot/no_sir.wav' %(userid))
				if rawtext.lower() == "hey": es.server.cmd('es_xsoon r_sendvoice %s bot/hey.wav' %(userid))
				if rawtext.lower() == "nnosir": es.server.cmd('es_xsoon r_sendvoice %s bot/nnno_sir.wav' %(userid))
				if rawtext == "negative": es.server.cmd('es_xsoon r_sendvoice %s bot/negative.wav' %(userid))
				if rawtext.lower() == "wow": es.server.cmd('es_xsoon r_sendvoice %s bot/whoo.wav' %(userid))
				if rawtext.lower() == "ohno" or rawtext == "ㅇㄴ": es.server.cmd('es_xsoon r_sendvoice %s bot/oh_no.wav' %(userid))
				if rawtext.lower() == "ohmygod": es.server.cmd('es_xsoon r_sendvoice %s bot/oh_my_god.wav' %(userid))
				if rawtext.lower() == "thisismyhouse" or rawtext == "여긴내집이야": es.server.cmd('es_xsoon r_sendvoice %s bot/this_is_my_house.wav' %(userid))
				if rawtext == "ㅗ" or rawtext == "fuckyou": es.server.cmd('es_xsoon r_sendvoice %s zeisenproject_3/autosounds/saysounds/fuckyou.mp3' %(userid))
				if rawtext == "앙?" or rawtext.lower() == "ang?": es.server.cmd('es_xsoon r_sendvoice %s zeisenproject_3/autosounds/saysounds/ang.mp3' %(userid))
				if rawtext == "오마이숄더": es.server.cmd('es_xsoon r_sendvoice %s zeisenproject_3/autosounds/saysounds/ohmy.mp3' %(userid))
				if rawtext_args[0] == "!report":
					if rawtext_args[1] == "MSG_DELETE":
						gname = "report_%s" %(getplayerzeisenid(userid))
						es.keygroupload(gname, "|rpg/report/msg")
						es.keydelete(gname, "report")
						es.keygroupsave(gname, "|rpg/report/msg")
					if rawtext_args[1] == "MSG_STATUS":
						gname = "report_%s" %(getplayerzeisenid(userid))
						gnumber = gname.replace("report_STEAM_", "")
						es.keygroupload(gname, "|rpg/report/msg")
						print_status = popuplib.create('print_%s' %(userid))
						print_status.addline(" ")
						print_status.addline("%s 님의 신고 현황" %(username))
						print_status.addline("─────────────")
						print_status.addline(" ")
						print_status.addline("＊ 당신의 제보 번호 : %s" %(gnumber))
						print_status.addline("＊ 당신이 보낸 메세지 : %s" %(es.keygetvalue(gname, "report", "message")))
						print_status.addline(" ")
						print_status.addline(" ")
						print_status.addline("＠ 답변 : %s" %(es.keygetvalue(gname, "report", "answer")))
						print_status.addline(" ")
						print_status.addline("─────────────")
						print_status.addline(" ")
						print_status.send(userid)
						popuplib.delete('print_%s' %(userid))
						es.keygroupdelete(gname)
					if rawtext_args[1] == "MSG":
						savetext = "%s " %(rawtext_args[2])
						gname = "report_%s" %(getplayerzeisenid(userid))
						es.keygroupcreate(gname)
						es.keycreate(gname, "report")
						es.keysetvalue(gname, "report", "message", savetext)
						es.keysetvalue(gname, "report", "answer", "없음 ")
						es.keygroupsave(gname, "|rpg/report/msg")
						es.keygroupdelete(gname)
					if rawtext_args[1] == "SKP_ERROR":
						if int(es.keygetvalue(steamid, "player_data", "skillpoint")) < 0:
							itemuse_select(userid, "2", 0)
				if rawtext.startswith("!") or rawtext.startswith("/"):
					return (0, 0, 0)
					if ["cvar", "csay", "msay", "hsay", "admin", "zspawn", "zmenu", "gag", "ungag", "mute", "unmute", "silence", "unsilence", "beacon", "freeze", "timebomb", "freezebomb", "noclip", "who", "help", "ban", "unban", "rcon", "fire", "kick", "map", "cancelvote", "exec", "reloadadmins", "vote", "votemap", "votekick", "voteban", "blind", "drug", "gravity", "voteburn", "votealltalk", "voteff", "votegravity", "voteslay", "slap", "rename"] in rawtext:
						esc.msg("%s#%s[Lv.%s %s]#%s %s #default: %s" %(classname, level_color, level, mastery, namecolor, username, rawtext))
						return (0, 0, 0)
				
		if steamid == "BOT":
			username = es.getplayername(userid)
			userteam = es.getplayerteam(userid)
			if userteam == 2:
				esc.msg("#red %s #default: %s" %(username, rawtext))
			if userteam == 3:
				esc.msg("#blue %s #default: %s" %(username, rawtext))
		return (userid, text, teamonly)

def round_start(ev):
	es.dbgmsg(0, "[DEBUG] ROUND_START")
	es.set("aimbot_enable", 0)
	es.set("aimbot_attack", 0)
	if "ze_" in map():
		if int(sv('round')) == 9:
			endthegame()
		return
	if map() == "ba_quartzy": es.set("event_line", 0)
	es.set("pery_forward", 1)
	es.set("pery_sidemove", 1)
	es.set("pery_fire", 0)
	es.set("pery_say", 0)
	es.forcevalue("sv_friction", 4)
	if "de_" in map(): es.remove("weapon_c4")
	es.set("what_ent", 0)
	es.set("buy_time", 1)
	if map() == "de_piranesi": est.remove("func_breakable")
	if map() == "de_dust":
		es.server.cmd('bot_add_t "[Human] Zed"')
		es.forcevalue("mp_roundtime", 5)
	if map() == "de_season":
		es.server.cmd('bot_add_t "[Human] Zuru"')
		es.server.cmd('bot_add_ct "[C Rank] Bakura Ryo"')
		es.forcevalue("mp_roundtime", 5)
	if map() == "ba_quartzy":
		es.server.cmd('bot_add_ct "[A Rank] Pery"')
		es.forcevalue("mp_roundtime", 6)
	if map() == "cs_office_FEAR_night":
		es.server.cmd('bot_add_t "[F Rank] Life"')
		es.server.cmd('bot_add_ct "[E Rank] Alma"')
		es.server.cmd('bot_add_ct "[Human] Shark"')
		es.forcevalue("mp_roundtime", 6.5)
	es.set("zeisen_gun", 0)
	es.set("hostage_follow_count", 0)
	es.set("weapon_f", 0)
	es.set("mission_allowed", 1)
	if not "ze_" in map():
		global knife_model_1
		knife_model_1 = es.precachemodel("models/weapons/w_fire_rapier.mdl")
	if map() == "de_rush_v2": est.remove('phys_bone_follower')
	esc.msg("#0,255,255[Update Information] %s" %(ACTIVATE_MSG))
	if map() == "de_nightfever":
		es.server.cmd('sv_visiblemaxplayers 15')
		enti = es.getentityindex("point_viewcontrol")
		if enti > 0:
			est.entteleport(enti, 2957.186035, 2425.615234, 8.137392)
			es.setindexprop(enti, "CBaseEntity.m_angRotation", "0,13,0")
	else: es.server.cmd('sv_visiblemaxplayers 37')
	if not map() in Special_Maps:
		es.server.cmd('bot_add "[Human] Ruki"')
	if "cs_" in map():
		cm = es.precachemodel("models/player/reisenbot/cirno/cirno.mdl")
		count = 0
		hostage_list = es.createentityindexlist("hostage_entity")
		for index in hostage_list:
			if count == 0:
				es.setindexprop(index, "CBaseEntity.m_nModelIndex", cm)
				est.setentitycolor(index, 255, 255, 255, 255)
				es.setindexprop(index, "CHostage.baseclass.baseclass.baseclass.baseclass.m_flModelScale", 0.75)
				es.setindexprop(index, "CHostage.m_lifeState", 0)
				count += 1
				#CHostage.m_leader
			else: es.remove(index)
	if not "ze_" in map():
		if int(sv('round')) == 8:
			endthegame()
			playsound("zeisenproject_3/autosounds/game_over.mp3")
			playsound(str(sv('soundtrack_ending')))
			mlist = es.createentityindexlist("cs_team_manager")
	        	for index in mlist:
				index_team = es.getindexprop(index, "CTeam.m_iTeamNum")
				if index_team == int(sv('humanteam')): humant_score = int(es.getindexprop(index, "CTeam.m_iScore"))
				if index_team == int(sv('zombieteam')): zombiet_score = int(es.getindexprop(index, "CTeam.m_iScore"))
			esc.msg("#255,255,255[Game Set] #0,255,0게임이 종료되었습니다. 수고하셨습니다.")
			if humant_score > zombiet_score:
				esc.msg("#255,255,255[Game Set] #0,0,255인간 팀 #255,255,255스코어 :#0,0,255 %s #255,255,255VS#125,125,125 %s #255,255,255: #255,0,0좀비 팀 #255,255,255스코어" %(humant_score, zombiet_score))
				much = 17 * (humant_score - zombiet_score)
				for a in playerlib.getPlayerList("#human,#alive"): give_xp(a.userid, much, "승리")
			else:
				esc.msg("#255,255,255[Game Set] #0,0,255인간 팀 #255,255,255스코어 :#125,125,125 %s #255,255,255VS#255,0,0 %s #255,255,255: #255,0,0좀비 팀 #255,255,255스코어" %(humant_score, zombiet_score))
			if map() in Versus_Maps:
				human_target = int(sv('human_target'))
				human_score = est.getkills(human_target)
				complete = 1
				for tuserid in es.getUseridList():
					if es.getplayerteam(tuserid) == int(sv('humanteam')):
						if es.isbot(tuserid):
							if human_score <= est.getkills(tuserid):
								complete = 0
				if complete == 1:
					if map() == "cs_gentech_final":
						esc.msg("#goldFace-OFF 대전에서 승리했습니다!(VS Scarecrow)")
						esc.msg("#gold플레이어에게 보상 : #55,55,255일렉트로 원소")
						human_steamid = getplayerzeisenid(human_target)
						keymath(human_steamid, "player_data", "item39", "+", 1)
					if map() == "cs_office":
						esc.msg("#goldFace-OFF 대전에서 승리했습니다!(VS Knife)")
						esc.msg("#gold플레이어에게 보상 : #255,255,255스워드 원소")
						human_steamid = getplayerzeisenid(human_target)
						keymath(human_steamid, "player_data", "item40", "+", 1)
def player_team(ev):
	userid = int(ev['userid'])
	if not es.isbot(userid):
		if map() in Versus_Maps:
			if es.getplayerteam(userid) > 1:
				if userid != int(sv('human_target')):
					est.team(userid, 1)
					esc.tell(userid, "#255,255,255당신은 Face-OFF 대전자가 아닙니다.")
	
def zombie_select():
	if not "ze_" in map():
		return
	zombie_list = []
	for a in playerlib.getPlayerList("#human,#alive"):
		if int(sv('before_zombie_userid')) != a.userid:
			zombie_list.append(a.userid)
	zombie_userid = random.choice(zombie_list)
	es.set("zombie_userid", zombie_userid)
	zombie_username = es.getplayername(zombie_userid)
	set_speed("#a", 1)
	for a in playerlib.getPlayerList("#t"):
		if a.userid != zombie_userid:
			gamethread.delayed(0.01, est.team, (a.userid, 3))
	est.team(zombie_userid, 2)
	spawn(zombie_userid)
	esc.msg("#255,0,0%s 유저#255,255,255가 술래입니다." %(zombie_username))
	es.server.cmd('mp_humanteam ct')

def round_freeze_end(ev):
	for userid in es.getUseridList():
		if not es.isbot(userid):
			steamid = getplayerzeisenid(userid)
			es.keygroupsave(steamid, "|rpg/player_data")
	if est.playercount("#h") > 0:
		es.set("mp_freezetime", 5)
		gamethread.delayed(15, es.set, ("buy_time", 0))
	est.stopsound("#h", str(sv('soundtrack_opening')))
	level = int(sv('level'))
	soundtrack = int(sv('soundtrack'))
	round_print = int(sv('round'))
	round = int(sv('round'))
	es.forcevalue("sv_password", sv('mypassword'))
	if round_print == 7: round_print = "Final Round"
	if not map() in Special_Maps:
		es.set("zombie_count", (level * 45))
		if level >= 10: es.set("zombie_count", 0)
		music = "zeisenproject_3/soundtrack_2/track_%s/battle%s.mp3" %(soundtrack, round)
		if level == 10:
			music = "zeisenproject_3/autosounds/stage1.mp3"
			npc_msg('#purplePradoster', '여기까지 온것을. 후회하게 만들어주마.')
			gamethread.delayed(3, npc_msg, ('#purplePradoster', '자, 간다.#gold 絶對休息日 개방#default!'))
			gamethread.delayed(5, npc_msg, ('#purplePradoster', '바빌로니아, #255,255,255月 각인!'))
			round_print = "Vs Pradoster - 月火水木金土日"
			es.set("mission_allowed", 0)
			es.set("weapon_f", 1)
			est.remove("weapon_c4")
			est.remove("hostage_entity")
		if level == 11:
			music = "zeisenproject_3/autosounds/stage___2.mp3"
			es.set("mission_allowed", 0)
			es.set("weapon_f", 1)
			est.remove("weapon_c4")
			est.remove("hostage_entity")
	else:
		es.set("zombie_count", 0)
		if not map() in "de_nightfever": es.forcevalue("sv_password", "pfosme")
		if map() == "ba_quartzy":
			npc_msg("#255,0,0Pery", "어라, 너희들은 어쩐일이야?")
			gamethread.delayed(3, npc_msg, ("#255,0,0Pery", "아, 내 인형이 되겠다고? 그거야 고맙지."))
	if "ze_" in map():
		es.set("weapon_f", 1)
		es.set("mp_maxrounds", 8)
		#zombie_timer.start(20, 1)
	if map() == "cs_gentech_final": music = "zeisenproject_3/autosounds/scarecrow_battle.mp3"
	if map() == "cs_office": music = "zeisenproject_3/autosounds/chain_battle2.mp3"
	if map() == "ba_quartzy": music = "zeisenproject_3/autosounds/mirror.mp3"
	if map() == "de_season":
		if int(sv('event_line')) == 0: music = "zeisenproject_3/autosounds/last_battle.mp3"
		if int(sv('event_line')) > 0: music = "zeisenproject_3/autosounds/last_battle2.mp3"
		npc_msg("#255,0,0Zeisen", "... 내가 생각해봐도, 저렇게 될줄은 상상도 못했어.")
		npc_msg("#255,0,0Zeisen", "나 대신 그 녀석을 억눌러 줄수 있어?")
		es.set("mission_allowed", 0)
		es.set("weapon_f", 1)
		est.remove("weapon_c4")
	if map() == "cs_office_FEAR_night":
		music = "zeisenproject_3/autosounds/fear.mp3"
		npc_msg("#255,255,255Rock", "내가 이 곳에서 용병 레코드 데이터를 발견했다.")
		npc_msg("#255,255,255Rock", "그 용병 레코드 데이터를 보면 거너, 던, 테이지, 내가 있었지..")
		npc_msg("#255,255,255Rock", "그 용병 레코드 데이터는 아마 던의 것이였을거다. 그러니까... 그는 #255,0,0죽었다.")
		npc_msg("#255,255,255Rock", "잘 찾아보면 무언가 있을지도 몰라... 행운을 빈다. 그럼.")
		for a in playerlib.getPlayerList("#bot"):
			if es.getplayername(a.userid) == "[E Rank] Alma": est.team(a.userid, 2)
	if str(sv('eventscripts_currentmap')) == "de_nightfever":
		es.set("nightfever_time", random.randint(30,90))
		music = "zeisenproject_3/autosounds/nightfever_issac.mp3"
		es.doblock("rpg/npc_nightfever")
		es.server.cmd('bot_kick ct all')
		es.server.cmd('bot_add_t "[Human] Ruki"')
		est.remove('func_bomb_target')
	mvp_rand = random.randint(0,150)
	if mvp_rand <= 144: mvp_print = "크리스탈"
	if mvp_rand == 145: mvp_print = "이벤트 티켓"
	if mvp_rand == 146: mvp_print = "유혹의 마도서"
	if mvp_rand == 147: mvp_print = "닌자의 마도서"
	if mvp_rand == 148: mvp_print = "황혼의 마도서"
	if mvp_rand == 149: mvp_print = "황혼주점 티켓"
	if mvp_rand == 150: mvp_print = "파란색 버섯"
	es.set("mvp_bonus", mvp_rand)
	esc.msg("#255,255,255○#255,55,55 BOT Level : %s" %(level))
	esc.msg("#255,255,255○#55,55,255 Round : %s" %(round_print))
	if mvp_print == "크리스탈": esc.msg("#255,255,255○#55,255,55 MVP Bonus : %s" %(mvp_print))
	if mvp_print != "크리스탈": esc.msg("#255,255,255○#purple MVP Bonus : %s" %(mvp_print))
	gamethread.delayed(0.2, playsound, (music))
	for a in playerlib.getPlayerList("#human"):
		skill = get_skill(a.userid, "skill10")
		if skill > 0:
			skill_much = 1 + skill
			myvar99 = es.getplayerprop(a.userid, "CBasePlayer.localdata.m_flLaggedMovementValue")
			es.setplayerprop(a.userid, "CBasePlayer.localdata.m_flLaggedMovementValue", skill_much)
			gamethread.delayed(3, es.setplayerprop, (a.userid, "CBasePlayer.localdata.m_flLaggedMovementValue", myvar99))
	'''
	for a in playerlib.getPlayerList("#bot"):
		if es.getplayerteam(a.userid) == int(sv('zombieteam')):
			gamethread.delayed(2, es.setplayerprop, (a.userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 5))
	'''

def round_mvp(ev):
	if not "ze_" in map(): 
		userid = int(ev['userid'])
		if not es.isbot(userid):
			steamid = getplayerzeisenid(userid)
			username = es.getplayername(userid)
			mvp_bonus = int(sv('mvp_bonus'))
			if mvp_bonus <= 144:
				keymath(steamid, "player_data", "item1", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#gold 크리스탈 아이템#255,255,255을 획득했습니다." %(username))
			if mvp_bonus == 145:
				keymath(steamid, "player_data", "item16", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#purple 이벤트 티켓 아이템#255,255,255을 획득했습니다." %(username))
			if mvp_bonus == 146:
				keymath(steamid, "player_data", "item9", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#purple 유혹의 마도서 아이템#255,255,255을 획득했습니다." %(username))
			if mvp_bonus == 147:
				keymath(steamid, "player_data", "item8", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#purple 닌자의 마도서 아이템#255,255,255을 획득했습니다." %(username))
			if mvp_bonus == 148:
				keymath(steamid, "player_data", "item7", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#purple 황혼의 마도서 아이템#255,255,255을 획득했습니다." %(username))
			if mvp_bonus == 149:
				keymath(steamid, "player_data", "item5", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#purple 황혼주점 티켓 아이템#255,255,255을 획득했습니다." %(username))
			if mvp_bonus == 150:
				keymath(steamid, "player_data", "item2", "+", 1)
				esc.msg("#blue %s 유저#255,255,255님이 #55,255,55MVP 보상#255,255,255으로#purple 파란색 버섯 아이템#255,255,255을 획득했습니다." %(username))
def hostage_follows(ev):
	userid = int(ev['userid'])
	hostage_follow_count = svmath("hostage_follow_count", "+", 1)
	es.set("hostage_follower", userid)
	if hostage_follow_count == 1:
		if not map() in Versus_Maps:
			allstopsound()
			gamethread.delayed(0.25, playsound, (sv('soundtrack_mission')))
		es.set('weapon_f', 1)
		est.give("#c!d", "item_assaultsuit")
		level = int(sv('level'))
		id_xp = 8 + (level * 2)
		if not es.isbot(userid): give_xp(ev['userid'], id_xp, "인질 최초 발견")
		for a in playerlib.getPlayerList("#human"):
			usermsg.centermsg(a.userid, "[Full Charge!] 인질을 발견했습니다.\n \n인질을 구출지점으로 인도하세요.")
	else:
		for f_userid in es.getUseridList():
			if isalive(f_userid) and es.getplayerteam(f_userid) == 2:
				x,y,z = es.getplayerlocation(f_userid)
				bot_move(f_userid, x, y, z)

def bomb_planted(ev):
	userid = int(ev['userid'])
	x,y,z = es.getplayerlocation(userid)
	es.set("c4_loc_x", x)
	es.set("c4_loc_y", y)
	es.set("c4_loc_z", z)
	if not map() in Versus_Maps:
		allstopsound()
		gamethread.delayed(0.25, playsound, (sv('soundtrack_mission')))
	es.set('weapon_f', 1)
	est.give("#t!d", "item_assaultsuit")
	es.set("hostage_follower", 0)
	level = int(sv('level'))
	id_xp = 8 + (level * 2)
	if not es.isbot(userid): give_xp(ev['userid'], id_xp, "폭탄 설치")
	for a in playerlib.getPlayerList("#human"):
		usermsg.centermsg(a.userid, "[Full Charge!] 폭탄이 설치되었습니다.\n \n폭탄이 해제되지 않게 사수하세요.")

def bomb_exploded(ev):
	userid = int(ev['userid'])
	level = int(sv('level'))
	id_xp = 8 + (level * 2)
	if not es.isbot(userid): give_xp(ev['userid'], id_xp, "폭파 성공")

def hostage_rescued(ev):
	userid = int(ev['userid'])
	level = int(sv('level'))
	id_xp = 2 + level
	if not es.isbot(userid): give_xp(ev['userid'], id_xp, "인질 구출")

def player_footstep(args):
	userid = int(args[0])
	steamid = getplayerzeisenid(userid)
	if steamid == "BOT":
		if es.getplayername(userid) == "[Z Rank] Waterman":
			es.server.cmd('es_xgive %s env_splash' %(userid))
			es.entitysetvalue(sv('eventscripts_lastgive'), "Scale", 10.0)
			es.server.cmd('es_xfire %s env_splash Splash' %(userid))
			gamethread.delayed(1, est.remove, ("env_splash"))
def player_blind(ev):
	userid = int(ev['userid'])
	steamid = getplayerzeisenid(userid)
	if steamid != "BOT":
		skill = get_skill(userid, "skill14")
		if skill > 0:
			es.setplayerprop(userid, "CCSPlayer.m_flFlashMaxAlpha", 0)
			es.setplayerprop(userid, "CCSPlayer.m_flFlashDuration", 0)
	if steamid == "BOT":
		username = es.getplayername(userid)
		if username == "[S Rank] Bakura Ryo":
			esc.msg("[SMAC] Bakura Ryo 님의 무적 핵이 의심됩니다.")
			est.god(userid, 1)
			est.setplayercolor(userid, 255, 255, 255, 0, 1)
			gamethread.delayed(8, est.god, (userid, 0))
			gamethread.delayed(8, est.setplayercolor, (userid, 255, 255, 255, 255, 1))
		if username == "[C Rank] Zeisen":
			est.god(userid, 1)
			est.setplayercolor(userid, 255, 255, 255, 0, 1)
			gamethread.delayed(8, est.god, (userid, 0))
			gamethread.delayed(8, est.setplayercolor, (userid, 255, 255, 255, 255, 1))

def player_jump(ev):
	userid = int(ev['userid'])
	if es.isbot(userid):
		est.setgravity(userid, 0.4)
	else:
		steamid = getplayerzeisenid(userid)
		if classname_get(steamid, 'classname') == "fairy":
			if not "ze_" in map(): est.setgravity(userid, 0.45)
	
def bulletimpact(args):
	event_x = args[1]
	event_y = args[2]
	event_z = args[3]
	userid = int(args[0])
	steamid = getplayerzeisenid(userid)
	x,y,z = es.getplayerlocation(userid)
	if es.isbot(userid):
		username = es.getplayername(userid)
		if username == "[C Rank] Zeisen":
			lasermodel = es.precachemodel("effects/laser1.vmt")
			z += 30
			v1 = "%s,%s,%s" %(x, y, z)
			v2 = "%s,%s,%s" %(event_x, event_y, event_z)
			es.effect("beam", v1, v2, lasermodel, lasermodel, 0, 0, 0.2, 1, 1, 0, 1, 255, 0, 0, 255, 1)

def bomb_beginplant(ev):
	userid = int(ev['userid'])
	steamid = getplayerzeisenid(userid)
	if steamid != "BOT":
		skill = item_get(steamid, "skill7")
		if skill > 0:
			weapon_index = est.getweaponindex(userid, "weapon_c4")
			time = getgametime()
			attacktime = float(es.getindexprop(weapon_index, 'CC4.m_fArmedTime'))
			check = 2
			delay = (attacktime - time)
			delay = delay / check
			settime = time + delay * 1.4
			es.setindexprop(weapon_index, "CC4.m_fArmedTime", settime)
			lists = es.createentityindexlist('predicted_viewmodel')
			for a in lists:
				rate = float(es.getindexprop(a, 'CPredictedViewModel.baseclass.m_flPlaybackRate'))
				if rate > 0:
					if es.getplayerhandle(userid) == int(es.getindexprop(a, 'CPredictedViewModel.baseclass.m_hOwner')):
						view_index = a
			rate = float(es.getindexprop(view_index, 'CPredictedViewModel.baseclass.m_flPlaybackRate')) * check
			es.setindexprop(view_index, 'CPredictedViewModel.baseclass.m_flPlaybackRate', rate)

def bomb_begindefuse(ev):
	userid = int(ev['userid'])
	steamid = getplayerzeisenid(userid)
	if steamid == "BOT":
		username = es.getplayername(userid)
		est.give(userid, "item_assaultsuit")
		esc.msg("#255,0,0→ %s 봇#255,255,255이 폭탄을 해체중입니다!" %(username))
		if username == "[C Rank] Zeisen":
			if random.randint(1,3) == 2:
				es.setindexprop(es.getentityindex("planted_c4"), "CPlantedC4.m_flDefuseCountDown", 1)
				esc.msg("#255,255,255→ %s 이#0,255,255 번개해체 #255,255,255스킬을 시전했습니다." %(username))

def fkfk():
	getid = es.getuserid("[Feast] Zeisen")
	if getid:
		x,y,z = es.getplayerlocation(getid)
		createcsseffect("fire_jet_01_flame", x, y, z)

def createcsseffect(effect_name, x, y, z):
    index = es.createentity("info_particle_system")
    es.entitysetvalue(index, "effect_name", effect_name)
    es.entitysetvalue(index, "origin", "%f %f %f" % (x, y, z))
    es.spawnentity(index)
    what = spe.call("GetParticleSystemIndex", effect_name)
    es.msg(what)
    es.setindexprop(index, "CParticleSystem.m_iEffectIndex", 10)
    # Finally we can start the effect...
    es.setentityname(index, index)
    es.fire(es.getuserid(), index, "Start")
    # Returns the index so we can edit/parent it...
    return index 


def fucktest():
	userid = 7
	weapon = est.getgun(userid)
	weapon_index = est.getweaponindex(userid, weapon)
	pointer = spe.getEntityOfIndex(weapon_index)
	es.msg("[DEBUG] Admin Weapon's Pointer : %s" %(pointer))
	spe.call("Update", int(pointer), float(0.0), 0)
	#spe.call("Update", 0, 0, 0, pointer)
	#spe.call("Update", 0.0, pointer, 0)
	#spe.call("Update", pointer, 0.0, 0)
	#es.msg("[DEBUG] CBaseWeapon")
	#es.msg("[DEBUG] Admin Weapon's Weapon Index : %s" %(weapon_index))
	#es.msg("[DEBUG] spe.call(Update, %s, 0.0, 1)" %(pointer))
	#es.msg("*** EventScripts caught an exception:")
	#es.msg("TypeError: an integer is required")

def weaponfire(args):
	userid = int(args[0])
	weapon = str(args[1])
	#es.server.cmd('echo %s' %(args))
	weapon_index = est.getweaponindex(userid, weapon)
	if userid == 2:
		weapon_index = est.getweaponindex(userid, 1)
		if weapon_index <= 0: weapon_index = est.getweaponindex(userid, 2)
		if weapon_index > 0:
			es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_fAccuracyPenalty", 0.0)
			es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_weaponMode", 0)
		est.setclipammo(userid, 1, 9999)
		es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
		es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
		es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
		es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
		es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
	if es.isbot(userid):
		if weapon != "knife":
			if weapon != "hegrenade":
				handle = es.getplayerprop(userid, "CBaseCombatCharacter.m_hActiveWeapon")
				index = es.getindexfromhandle(handle)
				getammoo = int(es.getindexprop(index, "CBaseCombatWeapon.LocalWeaponData.m_iClip1")) + 1
				es.setindexprop(index, "CBaseCombatWeapon.LocalWeaponData.m_iClip1", getammoo)
			username = es.getplayername(userid)
			if username == "[Human] Scarecrow":
				es.server.cmd("es_xtrick dispatcheffect %s ManhackSparks 9999" %(userid))
			if username == "[S Rank] Bakura Ryo":
				if int(sv('event_line')) >= 3:
					es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
					es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
					es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
					es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
					es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
			if username == "[Human] Zed":
				if weapon in "scout, awp":
					es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
					es.setindexprop(weapon_index, "CBaseCombatWeapon.m_fAccuracyPenalty", 0)
					es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
					es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
					es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
			if username == "[Z Rank] Zeisen":
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
				setclipammo(userid, weapon, 99999)
			if username == "[Z Rank] Crizi":
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
				setclipammo(userid, weapon, 99999)
			if username == "[C Rank] Zeisen":
				es.set("zeisen_gun", weapon_index)
				est.setentitycolor(weapon_index, 255, 0, 0, 255)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
				es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_fAccuracyPenalty", 0.0)
				es.setindexprop(weapon_index, "CWeaponCSBaseGun.baseclass.m_weaponMode", 1)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngleVel", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
				setclipammo(userid, weapon, 99999)			
	else:
		if map() == "ba_quartzy":
			if str(sv('pery_fire')) == "-1":
				npc_msg("#255,0,0Pery", "영광이야. 받아줄줄은.")
				est.slay(userid)
				es.set("pery_fire", 0)
		if weapon == "knife":
			es.emitsound("player", userid, "weapons/iceaxe/iceaxe_swing1.wav", 1.0, 1.0)
			es.emitsound("player", userid, "weapons/iceaxe/iceaxe_swing1.wav", 1.0, 1.0)
			es.emitsound("player", userid, "weapons/iceaxe/iceaxe_swing1.wav", 1.0, 1.0)
		if weapon != "knife":
			if est.getweaponindex(userid, weapon) == int(sv('zeisen_gun')) and item_get(getplayerzeisenid(userid), "skill9"):
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", 0)
				es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", 0)
				es.setplayerprop(userid, "CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle", "0,0,0")
				es.setplayerprop(userid, "CCSPlayer.cslocaldata.m_iShotsFired", 0)
			if int(sv('weapon_f')) == 1:
				if not weapon in "hegrenade, flashbang, smokegrenade, knife":
					steamid = getplayerzeisenid(userid)
					skill = item_get(steamid, "skill6")
					if "ze_" in map():
						if random.randint(1,2) == 1: skill = 1
					if skill > 0:
						getammoo = int(getclipammo(userid, weapon)) + 1
						setclipammo(userid, weapon, getammoo)
					else:
						getammoo = int(est.getammo(userid, weapon)) + 1
						setammo(userid, weapon, getammoo)
def weaponswap(args):
	userid = int(args[0])
	weapon_name = "weapon_%s" %(args[1])
	weapon_index = est.getweaponindex(userid, weapon_name)
	if userid == 1:
		time = getgametime()
		attacktime = float(es.getplayerprop(userid, 'CCSPlayer.baseclass.baseclass.bcc_localdata.m_flNextAttack'))
		check = 1.5
		delay = (attacktime - time)
		delay = delay / check
		settime = time + delay
		es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", settime)
		es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", settime)
		es.setplayerprop(userid, "CCSPlayer.baseclass.baseclass.bcc_localdata.m_flNextAttack", settime)
		lists = es.createentityindexlist('predicted_viewmodel')
		for a in lists:
			rate = float(es.getindexprop(a, 'CPredictedViewModel.baseclass.m_flPlaybackRate'))
			if rate > 0:
				if es.getplayerhandle(userid) == int(es.getindexprop(a, 'CPredictedViewModel.baseclass.m_hOwner')):
					view_index = a
		rate = float(es.getindexprop(view_index, 'CPredictedViewModel.baseclass.m_flPlaybackRate')) * check
		es.setindexprop(view_index, 'CPredictedViewModel.baseclass.m_flPlaybackRate', rate)


def weaponreload(args):
	userid = int(args[0])
	weapon_index = int(args[1])
	if userid == 1:
		time = getgametime()
		attacktime = float(es.getindexprop(weapon_index, 'CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack'))
		check = 2
		delay = (attacktime - time) / check
		settime = time + delay
		es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack", settime)
		es.setindexprop(weapon_index, "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextSecondaryAttack", settime)
		es.setplayerprop(userid, "CCSPlayer.baseclass.baseclass.bcc_localdata.m_flNextAttack", settime)
		lists = es.createentityindexlist('predicted_viewmodel')
		for a in lists:
			rate = float(es.getindexprop(a, 'CPredictedViewModel.baseclass.m_flPlaybackRate'))
			if rate > 0:
				if es.getplayerhandle(userid) == int(es.getindexprop(a, 'CPredictedViewModel.baseclass.m_hOwner')):
					view_index = a
		rate = float(es.getindexprop(view_index, 'CPredictedViewModel.baseclass.m_flPlaybackRate')) * check
		es.setindexprop(view_index, 'CPredictedViewModel.baseclass.m_flPlaybackRate', rate)

def getweaponcolor(userid):
        color = es.getindexprop(userid, "CBaseEntity.m_clrRender")
        return tuple(int(x) for x in (color & 0xff, (color & 0xff00) >> 8, (color & 0xff0000) >> 16, (color & 0xff000000) >> 24))

def item_pickup(ev):
	userid = int(ev['userid'])
	weapon = str(ev['item'])
	if es.getplayername(userid) == "[Z Rank] Waterman":
		est.removeweapon(userid, 1)
		est.removeweapon(userid, 2)
	if weapon == "c4":
		burnman = es.getuserid("[Z Rank] Burnman")
		if burnman <= 0:
			burnman = es.getuserid("[Z Rank] Waterman")
		if burnman <= 0:
			if str(sv('sv_password')) == "nipperz":
				est.give("#h", "item_assaultsuit")
				healthadd(userid, 50)
			if int(sv('mission_allowed')) == 0:
				est.removeweapon(userid, "weapon_c4")
			if int(sv('vex_dead')) == 0:
				if es.getplayername(userid) != "[E Rank] Vex":
					est.removeweapon(userid, "weapon_c4")
			else:
				es.set("hostage_follower", userid)
				for f_userid in es.getUseridList():
					if es.isbot(f_userid):
						spe.call("Follow", spe.getPlayer(f_userid), spe.getPlayer(userid))
		else:
			burnman_speed = float(es.getplayerprop(burnman, "CBasePlayer.localdata.m_flLaggedMovementValue")) + 0.11
			es.setplayerprop(burnman, "CBasePlayer.localdata.m_flLaggedMovementValue", burnman_speed)
			c4_index = est.getweaponindex(userid, "weapon_c4")
			r,g,b,a = getweaponcolor(c4_index)
			est.removeweapon(userid, "weapon_c4")
			if g == 254 and b == 254:
				if not es.isbot(userid):
					core_count = svmath("core_count", "+", 1)
					for a in playerlib.getPlayerList("#human"):
						es.playsound(a.userid, "zeisenproject_3/autosounds/man/page.mp3", 1.0)
						usermsg.hudhint(a.userid,"＊ 현재 %s개의 코어를 획득함" %(core_count))
					create_c4()
				else:
					core_count = svmath("core_count", "-", 1)
					esc.msg("#255,0,0코어가 제거되었습니다.")
					for a in playerlib.getPlayerList("#human"):
						usermsg.hudhint(a.userid,"＊ 현재 %s개의 코어를 획득함" %(core_count))
					create_c4()
	if int(sv('zombie_userid')) == userid:
		if weapon != "knife": est.removeweapon(userid, "weapon_%s" %(weapon))
	if es.isbot(userid):
		username = es.getplayername(userid)
		if username == "[E Rank] Kira":
			if weapon == "hegrenade":
				kira_knife = svmath("kira_knife", "+", 1)
				esc.msg("#red %s #255,255,255가 수류탄을 칼에 흡수했습니다. #gold(남은 폭발칼 횟수 : %s)" %(username, kira_knife))
		if username == "[S Rank] Bakura Ryo":
			if weapon != "elite": est.removeweapon(userid, "weapon_%s" %(weapon))

def player_hurt(ev):
	userid = int(ev['userid'])
	attacker = int(ev['attacker'])
	if attacker != 0:
		username = es.getplayername(userid)
		attackername = es.getplayername(attacker)
		steamid = getplayerzeisenid(userid)
		attackersteamid = getplayerzeisenid(attacker)
		userteam = es.getplayerteam(userid)
		dmg_health = int(ev['dmg_health'])
		weapon = str(ev['weapon'])
		es.set("my_attacker_%s" %(userid), attacker)
		gamethread.delayed(0.05, es.set, ("my_attacker_%s" %(userid), 0))
		if "ze_" in map() and int(sv('zombie_userid')) > 0:
			if userteam == 2:
				x, y, z = playerlib.getPlayer(attacker).get('viewvector')
				knockback = dmg_health * 2.5
				es.setplayerprop(userid, 'CBasePlayer.localdata.m_vecBaseVelocity', '%s,%s,%s'%(x * knockback, y * knockback, z * knockback))
		if steamid == "BOT":
			if username == "[Z Rank] Zeisen":
				est.setaim(userid, attacker, 0)
			if username == "[A Rank] Pery":
				if random.randint(1,1000) == 1: est.setaim(userid, attacker, 0)
				if "exp" in weapon:
					es.server.cmd('damage %s 999 32 %s counter' %(attacker, userid))
			if username == "[S Rank] Bakura Ryo":
				est.setaim(userid, attacker, 0)
				health = gethealth(userid)
				est.give(userid, "item_assaultsuit")
				event_line = int(sv('event_line'))
				if event_line == 1:
					if health <= 20000:
						es.set("event_line", 2)
						esc.msg("[SMAC] Bakura Ryo 님의 스피드 핵이 의심됩니다.")
						set_speed(userid, 1.95)
				if event_line == 2:
					if health <= 15000:
						es.set("event_line", 3)
						esc.msg("[SMAC] Bakura Ryo 님의 초연발 핵이 의심됩니다.")
				if event_line == 3:
					if health <= 10000:
						es.set("event_line", 4)
						esc.msg("[SMAC] Bakura Ryo 님의 데미지 핵이 의심됩니다.")
				if event_line == 4:
					if health <= 10000:
						es.set("event_line", 5)
						alist = es.createentityindexlist("prop_door_rotating")
						for a in alist: est.entteleport(a, 999, 999, 9999)
def pre_player_hurt(ev):
	userid = int(ev['userid'])
	attacker = int(ev['attacker'])
	if "ze_" in map():
		if int(sv('zombie_userid')) > 0 and es.getplayerteam(userid) == 2:
			if gethealth(userid) <= 2500: est.sethealth(userid, 9999999)
	if not es.isbot(userid):
		steamid = getplayerzeisenid(userid)
		if es.getplayerteam(userid) == 3:
			if "ze_" in map():
				if str(es.keygetvalue(steamid, "player_data", "skin")) in FEMALE_SKIN:
					es.emitsound("player", userid, "zeisenproject_3/autosounds/female/pain%s.wav" %(random.randint(1,3)), 1.0, 1.0)
		if map() == "de_nightfever":
			if int(sv('mp_friendlyfire')):
				if not es.isbot(attacker):
					attacker = 0
					healthadd(userid, ev['dmg_health'])
			est.fade(userid, 0, 0.05, 0.05, 255, 0, 0, 125)
			if str(es.keygetvalue(steamid, "player_data", "skin")) in FEMALE_SKIN:
				es.emitsound("player", userid, "zeisenproject_3/autosounds/female/pain%s.wav" %(random.randint(1,3)), 1.0, 1.0)
	if attacker > 0:
		username = es.getplayername(userid)
		attackername = es.getplayername(attacker)
		steamid = getplayerzeisenid(userid)
		attackersteamid = getplayerzeisenid(attacker)
		hitgroup = int(ev['hitgroup'])
		dmg_health = int(ev['dmg_health'])
		weapon = str(ev['weapon'])
		pre_damage(userid, "+", dmg_health)
		if weapon == "ump45": dmg_health *= 1.25
		cri = 0
		if es.isbot(attacker):
			if int(sv('level')) >= 8:
				if not map() in Special_Maps:
					if attackername != "[C Rank] Zeisen": dmg_health *= 3
			else:
				if int(sv('level')) >= 4:
					if not map() in Special_Maps:
						if attackername != "[C Rank] Zeisen": dmg_health *= 2
			if attackername == "[Human] Knife":
				if weapon == "knife":
					dmg_health = 99999
					est.god(attacker, 1)
					gamethread.delayed(2, est.god, (attacker, 0))
					make_explosion(userid, attacker, 5000, 5000, "knife_explosion")
			if attackername == "[Human] Scarecrow":
				dmg_health *= 10
			if attackername == "[A Rank] Pery":
				if gethealth(userid) <= 200000: dmg_health *= 2
			if attackername == "[Human] Zed":
				if weapon == "awp": dmg_health *= 6
			if "[F Rank]" in attackername:
				if not es.isbot(userid):
					level = int(es.keygetvalue(steamid, "player_data", "level"))
					if level <= 20: dmg_health *= 0.65
			if attackername == "[E Rank] Vex":
				dmg_health *= 2
			if attackername == "[E Rank] Alma":
				if weapon != "point_hurt": dmg_health = 444
			if attackername == "[A Rank] Kuria":
				if weapon != "point_hurt": dmg_health = 999
			if attackername == "[S Rank] Bakura Ryo":
				if int(sv('event_line')) == 4: dmg_health *= 2
			if attackername == "[B Rank] Pradoster":
				if int(sv('event_line')) == 0:
					dmg_health = 111111111
				if int(sv('event_line')) > 0: 
					dmg_health *= 2
				if int(sv('event_line')) == 1:
					est.burn(userid, 20)
				if int(sv('event_line')) == 2:
					r,g,b,a = getplayercolor(userid)
					est.setplayercolor(userid, 0, 0, 255, 255)
					getspeed = es.getplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue")
					set_speed(userid, 0.2)
					gamethread.delayed(2.25, est.speed, (userid, getspeed))
					gamethread.delayed(2.25, est.setplayercolor, (userid, r, g, b, a))
				if int(sv('event_line')) == 3:
					r,g,b,a = getplayercolor(userid)
					est.setplayercolor(userid, 0, 255, 0, 255)
					getspeed = es.getplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue")
					set_speed(userid, 0)
					gamethread.delayed(2.25, est.speed, (userid, getspeed))
					gamethread.delayed(2.25, est.setplayercolor, (userid, r, g, b, a))
				if int(sv('event_line')) == 6:
					dmg_health = 666666666
					est.burn("#h!d", 10)
			if attackername == "[C Rank] Zeisen":
				level = int(sv('level'))
				plusdamage = 2.5 + (level * 0.1) - 0.1
				thegun = est.getgun(userid)
				if thegun in "weapon_awp, weapon_scout, weapon_knife": plusdamage *= 40
				dmg_health *= plusdamage
			if attackername == "[E Rank] Vex":
				if not "[F Rank]" in username and es.isbot(userid) and es.getplayerteam(userid) == int(sv('zombieteam')): dmg_health = 0
			if attackername == "[E Rank] Kira":
				if weapon == "knife":
					dmg_health += 500
					if int(sv('kira_knife')) > 0:
						svmath("kira_knife", "-", 1)
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								est.god(a.userid, 1)
								gamethread.delayed(0.05, est.god, (a.userid, 0))
						make_explosion(userid, attacker, 9999, 3000, "kira_explosion")
						esc.msg("#red[E Rank] Kira 보스#255,255,255가 #255,0,0폭발칼#255,255,255 스킬을 시전했습니다. #gold(스킬 남은 횟수 : %s회)" %(sv('kira_knife')))
			if not es.isbot(userid):
				if es.getplayername(attacker) != "[C Rank] Zeisen":
					skill = item_get(steamid, "skill4")
					if skill > 0:
						skill_damage = (skill * 100) + skill_magic(steamid, 10)
						skill_p = skill
						if random.randint(1,100) <= int(skill_p):
							esc.tell(userid, "#55,255,55반격 스킬이 발동되었습니다!")
							es.server.cmd('damage %s %s 32 %s' %(attacker, skill_damage, userid))
				armor = float(es.keygetvalue(steamid, "player_data", "armor"))
				if armor > 0:
					total_mini = (100 - armor) / 100
					dmg_health *= total_mini
		else:
			#if "F Rank" in username: est.setarmor(userid, 0)
			if weapon in "sg550, g3sg1":
				dmg_health *= 0.2
				magic = float(es.keygetvalue(attackersteamid, "player_data", "magic"))
				dmg_health = dmg_health + (magic * 1.8)
			if map() == "ba_quartzy":
				if int(sv('event_line')) >= 7:
					if hitgroup == 1: est.slay(attacker)
			skin = str(es.keygetvalue(attackersteamid, "player_data", "skin"))
			if "explosion" in weapon or "hegrenade" in weapon:
				if skin == "player/hhp227/miku/miku": dmg_health *= 4
			if attackersteamid == "STEAM_0038622202":
				if weapon != "knife":
					dmg_health *= 0.3
			if weapon in "awp, scout":
				dmg_health *= 2
			mastery = get_skill(attacker, "mastery_select")
			criticalmax = 100
			if weapon in "awp, scout": criticalmax = 90
			if weapon in str(es.keygetvalue(attackersteamid, "player_data", "mastery_list")):
				if mastery == 1:
					skill = get_skill(attacker, "mastery_skill2")
					if skill > 0:
						criticalmax = criticalmax - skill
			magic = float(es.keygetvalue(attackersteamid, "player_data", "magic"))
			dollar_regen = float(es.keygetvalue(attackersteamid, "player_data", "dollar_regen"))
			if not weapon in "awp, scout":
				criticalmax = criticalmax - dollar_regen * 1.5
			else: criticalmax = criticalmax - dollar_regen
			criticalmax = rounddecimal(criticalmax, 0)
			criticalmax = criticalmax.replace(".0", "")
			criticalmax = int(criticalmax)
			if criticalmax < 1: criticalmax = 1
			if random.randint(1, criticalmax) <= 1:
				cri = 1
				percent = 2
				tw = "weapon_%s" %(weapon)
				if tw in allweapons:
					percent = 1.5
				skill = item_get(attackersteamid, "skill8") + item_get(attackersteamid, "skill8") * 0.5
				skillz = item_get(attackersteamid, "skill12") * 2
				tskill = skill + skillz
				if tskill > 0: percent = percent + (tskill * 0.2)
				dmg_health *= percent
				dmg_health = dmg_health + (dmg_health * magic * 0.02)
				es.server.cmd('es_xtrick dispatcheffect %s Explosion 1' %(userid))
				fcri[attacker] = 1
			classname = str(es.keygetvalue(attackersteamid, "player_data", "classname"))
			if classname == "monster": dmg_health *= 1.2
			if weapon == "hegrenade":
				if username != "[C Rank] Zeisen":
					dmg_health *= 6
			if weapon in "glock usp p228 deagle fiveseven":
				if weapon == "deagle": dmg_health *= 1.5
				else: dmg_health *= 1.15
			if weapon == "knife":
				dmg_health *= 5
				if str(es.keygetvalue(attackersteamid, "player_data", "skin")) == "player/konata/idol/idol":
					dmg_health *= 1.5
				healthcheck = float(max_health[attacker]) / 2
				if float(gethealth(attacker)) <= float(healthcheck):
					if mastery == 2:
						skill = get_skill(attacker, "mastery_skill4")
						if skill > 0:
							skill_d = 0.1 * skill
							dmg_health = dmg_health + (dmg_health * skill_d)
			if weapon == "flashbang":
				skill = get_skill(attacker, "skill3")
				if skill > 0:
					skill_d = (skill * 499) + skill_magic(attackersteamid, 50)
					dmg_health += skill_d
			if username != "[C Rank] Zeisen":
				power = float(es.keygetvalue(attackersteamid, "player_data", "power")) / 100
				tw = "weapon_%s" %(weapon)
				if tw in allweapons:
					dmg_health *= power
					dmg_health *= power
				if str(es.keygetvalue(attackersteamid, "player_data", "skin")) == "player/reisen/cirno/cirno":
					userid_speed = float(es.getplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue"))
					attacker_speed = float(es.getplayerprop(attacker, "CBasePlayer.localdata.m_flLaggedMovementValue"))
					speed_total = attacker_speed - userid_speed
					if float(speed_total) > 0:
						speed_total = 1 + (speed_total * 1.3)
						dmg_health *= speed_total
			if username == "[B Rank] Pradoster":
				if int(sv('event_line')) == 4:
					dmg_health *= 0.4
			if username == "[E Rank] Kira":
				if weapon == "hegrenade":
					dmg_health = dmg_health * 0.1
					kira_knife = svmath("kira_knife", "+", 1)
					esc.msg("#red %s #255,255,255가 수류탄을 칼에 흡수했습니다. #gold(남은 폭발칼 횟수 : %s)" %(username, kira_knife))
				if "explode" in weapon or "explosion" in weapon:
					dmg_health = dmg_health * 0.1
					kira_knife = svmath("kira_knife", "+", 1)
					esc.msg("#red %s #255,255,255가 폭발을 칼에 흡수했습니다. #gold(남은 폭발칼 횟수 : %s)" %(username, kira_knife))
			if not isalive(attacker):
				skill = get_skill(attacker, "skill2")
				if skill > 0:
					skill_d = 1 + (skill) + skill_magic(attackersteamid, 0.03)
					dmg_health *= skill_d
			if weapon in str(es.keygetvalue(attackersteamid, "player_data", "mastery_list")):
				if "ze_" in map(): mastery = 0
				if mastery == 2:
					skill = get_skill(attacker, "mastery_skill3")
					if skill > 0:
						if random.randint(1,100) <= (skill * 5):
							make_explosion(userid, attacker, 500, 250, "pl_attack_explosion")
				if mastery == 1:
					skill = get_skill(attacker, "mastery_skill1")
					if skill > 0:
						dollar_regen = float(es.keygetvalue(attackersteamid, "player_data", "dollar_regen"))
						mathskill = skill
						if dollar_regen >= 15: mathskill += 1
						if dollar_regen >= 25: mathskill += 1
						if dollar_regen >= 35: mathskill += 1
						if dollar_regen >= 45: mathskill += 1
						if dollar_regen >= 55: mathskill += 1
						if dollar_regen >= 65: mathskill += 1
						if dollar_regen >= 75: mathskill += 1
						if dollar_regen >= 85: mathskill += 1
						if dollar_regen >= 95: mathskill += 1
						if dollar_regen >= 100: mathskill += 1
						if random.randint(1,100) <= mathskill:
							wide = 400 + skill_magic(attackersteamid, 7)
							damage = 300 + skill_magic(attackersteamid, 6)
							make_explosion(userid, attacker, wide, damage, "pl_attack_explosion")
				if mastery == 1:
					skill = get_skill(attacker, "mastery_skill3")
					if skill > 0:
						if hitgroup == 1:
							skill_dmg = dmg_health * (skill * 0.04)
							dmg_health += skill_dmg
		if es.isbot(userid):
			if username == "[Human] Knife":
				if random.randint(1,5) <= 4: dmg_health = 0
			if username == "[E Rank] Alma":
				est.setaim(userid, attacker, 0)
			if username == "[E Rank] Kira":
				spe.call("Attack", spe.getPlayer(userid), spe.getPlayer(attacker))
			if username == "[C Rank] Zeisen":
				est.setaim(userid, attacker, 0)
				if "explosion" in weapon:
					healthadd(userid, dmg_health)
				else:
					gamethread.delayed(0.1, healthadd, (userid, dmg_health))
		if dmg_health > 0:
			pre_damage(userid, "-", dmg_health)
			if not es.isbot(attacker) and es.getplayerhandle(attacker) > 0:
				skill = get_skill(attacker, "skill1")
				if skill > 0:
					max = 125
					if weapon in "xm1014, m3": max = 300
					if random.randint(1,max) <= skill:
						skill_will = (skill * 300) + skill_magic(attackersteamid, 50)
						est.cashadd(attacker, skill_will)
				if weapon != "knife": es.playsound(attacker, "weapons/crossbow/hit1.wav", 1.0)
				else:
					es.playsound(attacker, "weapons/crossbow/hitbod%s.wav" %(random.randint(1,2)), 1.0)
				if dmg_health >= 1:
					dmg_health = rounddecimal(dmg_health, 0)
					dmg_health = dmg_health.replace(".0", "")
					totaldamage[attacker] = int(totaldamage[attacker]) + int(dmg_health)
					fdamage[attacker] = int(fdamage[attacker]) + int(dmg_health)
					gamethread.delayed(0.01, damage_reset, (attacker))
					print_health = es.getplayerprop(userid, 'CBasePlayer.m_iHealth')
					usermsg.hudhint(attacker, "＠ Total Damage : %s \n \n＊ %s HP : %s / %s" %(totaldamage[attacker], es.getplayername(userid), print_health, max_health[userid]))
					if cri == 0 and fcri[attacker] == 0:
						usermsg.centermsg(attacker, "- %s HP" %(fdamage[attacker]))
					else:
						es.playsound(attacker, "zeisenproject_3/autosounds/hit.wav", 1.0)
						usermsg.centermsg(attacker, "- %s HP (CRITICAL!)" %(fdamage[attacker]))
				else:
					if cri == 0 and fcri[attacker] == 0:
						usermsg.centermsg(attacker, "- Miss!")
					else:
						pre_damage(userid, "-", 1)
						totaldamage[attacker] = int(totaldamage[attacker]) + 1
						fdamage[attacker] = int(fdamage[attacker]) + 1
						usermsg.centermsg(attacker, "- 1 HP (CRITICAL!)")
					print_health = es.getplayerprop(userid, 'CBasePlayer.m_iHealth')
					usermsg.hudhint(attacker, "＠ Total Damage : %s \n \n＊ %s HP : %s / %s" %(totaldamage[attacker], es.getplayername(userid), print_health, max_health[userid]))
		if es.isbot(userid):
			if username == "[A Rank] Kuria":
				health = gethealth(userid)
				event_line = int(sv('event_line'))
				if event_line == 0:
					if health <= 140000:
						svmath("event_line", "+", 1)
						npc_msg("#255,0,0Kuria", "자 갑니다. 리키나스 레카!")
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('humanteam')):
								est.physpush(a.userid, 0, 0, 500)
								est.burn(a.userid, 5)
								es.server.cmd('damage %s 20 32 %s' %(a.userid, userid))
				if event_line == 1:
					if health <= 120000:
						svmath("event_line", "+", 1)
						npc_msg("#255,0,0Kuria", "자 갑니다. 리키나스 레카!")
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('humanteam')):
								est.physpush(a.userid, 0, 0, 500)
								est.burn(a.userid, 5)
								es.server.cmd('damage %s 20 32 %s' %(a.userid, userid))
				if event_line == 2:
					if health <= 100000:
						svmath("event_line", "+", 1)
						npc_msg("#255,0,0Kuria", "자 갑니다. 리키나스 레카!")
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('humanteam')):
								est.physpush(a.userid, 0, 0, 500)
								est.burn(a.userid, 5)
								es.server.cmd('damage %s 25 32 %s' %(a.userid, userid))
				if event_line == 3:
					if health <= 80000:
						svmath("event_line", "+", 1)
						npc_msg("#255,0,0Kuria", "자 갑니다. 리키나스 레카!")
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('humanteam')):
								est.physpush(a.userid, 0, 0, 500)
								est.burn(a.userid, 5)
								es.server.cmd('damage %s 25 32 %s' %(a.userid, userid))
				if event_line == 4:
					if health <= 60000:
						svmath("event_line", "+", 1)
						npc_msg("#255,0,0Kuria", "자 갑니다. 리키나스 레카!")
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('humanteam')):
								est.physpush(a.userid, 0, 0, 500)
								est.burn(a.userid, 5)
								es.server.cmd('damage %s 50 32 %s' %(a.userid, userid))
				if event_line == 5:
					if health <= 40000:
						svmath("event_line", "+", 1)
						npc_msg("#255,0,0Kuria", "자 갑니다. 리키나스 레카!")
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('humanteam')):
								est.physpush(a.userid, 0, 0, 500)
								est.burn(a.userid, 5)
								es.server.cmd('damage %s 100 32 %s' %(a.userid, userid))
			if username == "[A Rank] Pery":
				if "exp" in weapon: dmg_health = 0
				health = gethealth(userid)
				event_line = int(sv('event_line'))
				if event_line == 0:
					if health <= 240000:
						es.set("event_line", 1)
						npc_msg("#255,0,0Pery", "너희들은 이미 나와 맺어져있어... 그 실이 보여?")
				if event_line == 1:
					if health <= 230000:
						es.set("event_line", 2)
						es.set("pery_forward", -1)
						npc_msg("#255,0,0Pery", "포워드 리버스야.")
				if event_line == 2:
					if health <= 220000:
						es.set("event_line", 3)
						es.set("pery_sidemove", -1)
						npc_msg("#255,0,0Pery", "사이드 리버스야.")
				if event_line == 3:
					if health <= 200000:
						es.set("event_line", 4)
						es.set("pery_fire", -1)
						npc_msg("#255,0,0Pery", "리키나스, 웨폰 리버스.")
				if event_line == 4:
					if health <= 180000:
						es.set("event_line", 5)
						es.set("pery_say", -1)
						npc_msg("#255,0,0Pery", "묵언수행.")
				if event_line == 5:
					if health <= 150000:
						es.set("event_line", 6)
						npc_msg("#255,0,0Pery", "갖고 노는거... 재미있네. 여러명이라 그런가?")
				if event_line == 6:
					if health <= 100000:
						es.set("event_line", 7)
						npc_msg("#255,0,0Pery", "음... 머리를 조심해.")
				if event_line == 7:
					if health <= 30000:
						es.set("event_line", 8)
						npc_msg("#255,0,0Pery", "알고있어...")
						for a in playerlib.getPlayerList("#human"):
							x,y,z = es.getplayerlocation(a.userid)
							if float(z) >= 195: est.slay(a.userid)
				if event_line == 8:
					if health <= 20000:
						es.set("event_line", 9)
						est.sethealth(userid, 9999999)
						npc_msg("#255,0,0Pery", "이미 늦었는걸. 재밌게 놀다 가자..")
			if username == "[B Rank] Pradoster":
				if random.randint(1,25) == 1: est.setaim(userid, attacker, 0)
				health = gethealth(userid)
				event_line = int(sv('event_line'))
				if event_line == 0:
					if health <= 100000:
						npc_msg('#purplePradoster', '바빌로니아, #255,0,0火 각인!')
						es.set("event_line", 1)
						knife_index = est.getweaponindex(userid, 3)
						est.setentitycolor(knife_index, 255, 0, 0, 155)
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								est.god(a.userid, 1)
								gamethread.delayed(0.05, est.god, (a.userid, 0))
						make_explosion(userid, userid, 900, 450, "pradoster_explosion")
				if event_line == 1:
					if health <= 90000:
						npc_msg('#purplePradoster', '바빌로니아, #0,0,255水 각인!')
						es.set("event_line", 2)
						knife_index = est.getweaponindex(userid, 3)
						est.setentitycolor(knife_index, 0, 0, 255, 155)
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								est.god(a.userid, 1)
								gamethread.delayed(0.05, est.god, (a.userid, 0))
						make_explosion(userid, userid, 900, 4950, "pradoster_explosion")
				if event_line == 2:
					if health <= 80000:
						npc_msg('#purplePradoster', '바빌로니아, #0,255,0木 각인!')
						es.set("event_line", 3)
						knife_index = est.getweaponindex(userid, 3)
						est.setentitycolor(knife_index, 0, 255, 0, 155)
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								est.god(a.userid, 1)
								gamethread.delayed(0.05, est.god, (a.userid, 0))
						make_explosion(userid, userid, 900, 4509, "pradoster_explosion")
				if event_line == 3:
					if health <= 70000:
						npc_msg('#purplePradoster', '바빌로니아, #gold金 각인!')
						es.set("event_line", 4)
						knife_index = est.getweaponindex(userid, 3)
						est.setentitycolor(knife_index, 255, 215, 0, 155)
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								est.god(a.userid, 1)
								gamethread.delayed(0.05, est.god, (a.userid, 0))
						make_explosion(userid, userid, 9090, 4509, "pradoster_explosion")
				if event_line == 4:
					if health <= 60000:
						set_speed(userid, 2.5)
						npc_msg('#purplePradoster', '바빌로니아, #brown土 각인!')
						es.set("event_line", 5)
						knife_index = est.getweaponindex(userid, 3)
						est.setentitycolor(knife_index, 165, 42, 42, 155)
						for a_userid in es.getUseridList():
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								if not est.isalive(userid): est.spawn(a_userid)
				if event_line == 5:
					if health <= 50000:
						npc_msg('#purplePradoster', '바빌로니아, #255,0,0日 각인!')
						es.set("event_line", 6)
						knife_index = est.getweaponindex(userid, 3)
						est.setentitycolor(knife_index, 255, 0, 0, 255)
						for a in playerlib.getPlayerList("#all,#alive"):
							if es.getplayerteam(a.userid) == int(sv('zombieteam')):
								est.god(a.userid, 1)
								gamethread.delayed(0.05, est.god, (a.userid, 0))
						make_explosion(userid, attacker, 9999, 9999, "pradoster_explosion")
		if not es.isbot(userid):
			if dmg_health >= 1:
				dmg_health = rounddecimal(dmg_health, 0)
				dmg_health = dmg_health.replace(".0", "")
				usermsg.centermsg(userid, "+ %s HP" %(dmg_health))
def awe_patch():
	npc_msg("#255,0,0Reisen", "용서 못해! 복수해주겠어... 모두에게!")
	gamethread.delayed(4, npc_msg, ("#255,255,255Rock", "하... 씨발. 저거 대체 어떻게하란거야?"))
	gamethread.delayed(8, npc_msg, ("#255,255,255Shark", "진정해, 케이트에게서 들은 정보다. 잘 들어."))
	gamethread.delayed(12, npc_msg, ("#255,255,255Shark", "저 녀석은 지금 레이센의 육체에 들어간 상태다."))
	gamethread.delayed(16, npc_msg, ("#255,255,255Shark", "그래서 저건 죽여도 안되는 존재다. 빼낼 다른 방법이 필요하다."))
	gamethread.delayed(20, npc_msg, ("#255,255,255Gunner", "죽여도 안된다고? 제기랄!"))
	gamethread.delayed(24, npc_msg, ("#255,255,255Zed", "프렌 박사한테 들었었는데, 레이센의 육체는 #255,0,0수수께끼의 능력이 없는걸로 추정됬다."))
	gamethread.delayed(28, npc_msg, ("#255,255,255Zed", "바즈 능력 못씀 ㅋㅋㅋㅋㅋㅋ"))
	gamethread.delayed(32, npc_msg, ("#255,255,255Rock", "ㅋㅋㅋㅋ"))
def player_death(ev):
	userid = int(ev['userid'])
	es.remove("hat_%s" %(userid))
	attacker = int(ev['attacker'])
	if userid <= 0: return
	if attacker <= 0: return
	est.deathadd(userid, -1)
	est.killadd(userid, -1)
	if userid != attacker and attacker > 0:
		if not es.isbot(userid): keymath(getplayerzeisenid(userid), "player_data", "death", "+", 1)
		if not es.isbot(attacker): keymath(getplayerzeisenid(attacker), "player_data", "kill", "+", 1)
	username = es.getplayername(userid)
	attackername = es.getplayername(attacker)
	weapon = str(ev['weapon'])
	headshot = int(ev['headshot'])
	#if username == "[Helper] ZE":
	#	if attacker > 0: es.server.cmd('sm_map ze_TESV_Skyrim_v4fix')
	zombie_count = 0
	last_id = 0
	for useridf in es.getUseridList():
		if es.getplayerteam(useridf) == int(sv('zombieteam')) and isalive(useridf):
			last_id = useridf
			zombie_count += 1
	if int(sv('level')) <= 9:
		if zombie_count == 1:
			if int(sv('aimbot_enable')) == 0:
				if last_id == int(sv('zeisen_id')):
					es.set("aimbot_enable", 1)
					npc_msg("#255,0,0Zeisen", "나 혼자인가, 좋아... #255,0,0아주 좋아! 하하하하!")
	if username == "[C Rank] Zeisen":
		es.server.cmd('es_xdelayed 1.5 r_sendvoice %s zeisenproject_3/autosounds/zeisen/teamkill1.wav' %(userid))
	if attackername == "[C Rank] Zeisen":
		if not es.isbot(userid):
			es.server.cmd('r_sendvoice %s zeisenproject_3/autosounds/zeisen/teamkill%s.wav' %(attacker, random.randint(2,3)))
	if is_human(userid):
		if int(sv('hostage_follower')) == userid: es.set("hostage_follower", 0)
		if not map() in Special_Maps:
			ds = "zeisenproject_3/autosounds/death.mp3"
			if attackername == "[E Rank] Kira": ds = "weapons/crossbow/bolt_skewer1.wav"
			playsound(ds)
		if not es.isbot(userid):
			steamid = getplayerzeisenid(userid)
			skill = item_get(steamid, "skill5")
			if "ze_" in map(): skill = 0 
			if skill > 0:
				if random.randint(1,5) == 2:
					wide = 300 + (skill * 100) + skill_magic(steamid, 5)
					damage = 200 + (skill * 150) + skill_magic(steamid, 5)
					make_explosion(userid, userid, wide, damage, "player_explosion")
	#if attackername == "[Human] Scarecrow": est.est.killadd(attacker, 1)
	if es.isbot(userid):
		if "[F Rank]" in username:
			if int(sv('zombie_count')) > 0:
				zombie_count = svmath("zombie_count", "-", 1)
				gamethread.delayed(0.1, spawn, (userid))
		if not es.isbot(attacker) and es.getplayerteam(attacker) != es.getplayerteam(userid):
			mastery = get_skill(attacker, "mastery_select")
			attackersteamid = getplayerzeisenid(attacker)
			xp = int(sv('level'))
			if "[S Rank]" in username: xp *= 2000
			if "[A Rank]" in username: xp *= 1000
			if "[B Rank]" in username: xp *= 750
			if "[C Rank]" in username: xp *= 5
			if "[D Rank]" in username: xp *= 4
			if "[E Rank]" in username: xp *= 3
			if "[F Rank]" in username: xp += 1
			level = get_skill(attacker, "level")
			if xp <= 100:
				if level <= 10: xp *= 5
				if level >= 11 and level <= 25: xp *= 3
			if username == "[S Rank] Bakura Ryo": xp = 20000
			if username == "[A Rank] Pery":
				xp = 20000
				endthegame()
				npc_msg("#255,0,0Pery", "... 재밌었는데, 약속한대로 돌려주지. 알겠어?")
			if headshot == 1: keymath(attackersteamid, "player_data", "item13", "+", 1)
			if weapon == "knife":
				keymath(attackersteamid, "player_data", "item13", "+", 1)
			if attackersteamid == "STEAM_0088073563":
				if int(sv('item_allow')) == 1:
					es.set("item_allow", 0)
					get_item(attacker, "item10", "#55,255,55양말", 1)
			if rank_number(username) > 2:
				if random.randint(1,100) == 1:
					get_item(attacker, "item7", "#purple황혼의 마도서", 1)
				if random.randint(1,25) == 1:
					get_item(attacker, "item2", "#85,85,255파란색 버섯", 1)
			if rank_number(username) > 1:
				if random.randint(1,10) == 1:
					get_item(attacker, "item1", "#125,125,255크리스탈", 1)
			if map() == "de_museum_remake_b6":
				if rank_number(username) == 0:
					if random.randint(1,50) == 20:
						get_item(attacker, "item1", "#125,125,255크리스탈", 1)
			if rank_number(username) >= 0:
				if random.randint(1,5000) == 1:
					get_item(attacker, "item10", "#55,255,55양말", 1)
				if random.randint(1,2000) == 1:
					get_item(attacker, "item4", "#55,55,255요정의 씨앗", 1)
				if random.randint(1,2000) == 1:
					get_item(attacker, "item3", "#55,55,255요정의 샘물", 1)
			give_xp(attacker, xp, "%s 사살" %(username))
			partner = es.keygetvalue(attackersteamid, "player_data", "partner")
			for get_id in es.getUseridList():
				if getplayerzeisenid(get_id) == get_id:
					partner_id = get_id
					if int(es.getplayerteam(partner_id)) > 1:
						partner_xp = int(xp) / 2
						partner_xp = rounddecimal(partner_xp, 0)
						partner_xp = partner_xp.replace(".0", "")
						partner_xp = int(partner_xp)
						if partner_xp <= 0: partner_xp = 1
						give_xp(partner_id, partner_xp, "%s 사살(파트너)" %(username))
			skill = get_skill(attacker, "skill11")
			if skill > 0:
				healthadd(attacker, skill)
			if weapon in str(es.keygetvalue(attackersteamid, "player_data", "mastery_list")):
				keymath(attackersteamid, "player_data", "mastery_xp", "+", xp)
				if str(es.keygetvalue(attackersteamid, "player_data", "skin")) == "player/techknow/paranoya/paranoya": keymath(attackersteamid, "player_data", "mastery_xp", "+", 2)
				if headshot == 1:
					if mastery == 1:
						skill = get_skill(attacker, "mastery_skill4")
						if skill > 0:
							if gethealth(attacker) <= 25:
								s_percent = skill * 15
								if random.randint(1,100) <= s_percent:
									na = es.getplayername(attacker)
									esc.msg("#blue%s 유저#255,255,255님의 #0,255,255피스톨로의 구원 #255,255,255스킬이 발동되어 체력이 회복되었습니다." %(na))
									health = int(es.keygetvalue(attackersteamid, "player_data", "health"))
									es.setplayerprop(attacker, _healthprop, health)
		if not "[F Rank]" in username:
			es.server.cmd('es_xsexec %s enemydown' %(attacker))
			if username == "[C Rank] Bakura Ryo":
				es.botsetvalue(userid, 'name', '[S Rank] Bakura Ryo')
				esc.msg("[SMAC] Bakura Ryo 님은 에임핵으로 의심됩니다.")
				es.set("event_line", 1)
			if username == "[E Rank] Vex":
				x,y,z = es.getplayerlocation(userid)
				z -= 50
				es.server.cmd('est_effect 10 #a 0 sprites/bluelight1.vmt %s %s %s 50 2000 1 30 100 1 255 50 255 255 5' %(x,y,z))
				es.server.cmd('es_xdelayed 0.4 est_effect 10 #a 0 sprites/bluelight1.vmt %s %s %s 50 2000 1 30 100 1 255 50 255 255 5' %(x,y,z))
				es.server.cmd('es_xdelayed 0.8 est_effect 10 #a 0 sprites/bluelight1.vmt %s %s %s 50 2000 1 30 100 1 255 50 255 255 5' %(x,y,z))
				es.server.cmd('es_xdelayed 1.2 est_effect 10 #a 0 sprites/bluelight1.vmt %s %s %s 50 2000 1 30 100 1 255 50 255 255 5' %(x,y,z))
				es.server.cmd('es_xdelayed 1.6 est_effect 10 #a 0 sprites/bluelight1.vmt %s %s %s 50 2000 1 30 100 1 255 50 255 255 5' %(x,y,z))
				es.server.cmd('es_xdelayed 2 est_effect 10 #a 0 sprites/bluelight1.vmt %s %s %s 50 2000 1 30 100 1 255 50 255 255 5' %(x,y,z))
				esc.msg("#255,0,0＊ %s 가 자폭을 시도하고 있습니다!" %(username))
				if es.getplayerteam(userid) == 3:
					esc.msg("#0,0,255＊ %s 가 C4를 떨어트렸습니다." %(username))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
					es.server.cmd('es_xgive %s weapon_c4' %(userid))
				playsound("zeisenproject_3/autosounds/vex_pain.wav")
				gamethread.delayed(2, make_explosion, (userid, userid, 2000, 2000, "vex_explosion", 0))
				gamethread.delayed(2.25, est.dissolve, ("cs_ragdoll"))
				es.set("vex_dead", 1)
	else:
		if str(sv('sv_password')) == "nipperz":
			es.server.cmd('kickid %s' %(userid))
			playsound("zeisenproject_3/nippersounds/nmhm_scare%s.wav" %(random.randint(1,3)))

def player_changename(ev):
	userid = int(ev['userid'])
	if not es.isbot(userid):
		name = es.getplayername(userid)
		if name in CHANGE_NAME: es.server.cmd('kickid %s "남용 금지"' %(userid))

def player_spawn(ev):
	userid = int(ev['userid'])
	steamid = getplayerzeisenid(userid)
	userteam = es.getplayerteam(userid)
	if userteam < 2: return
	if "ze_" in map():
		if userteam == 2 and int(sv('zombie_userid')) != 0:
			est.removeweapon(userid, 1)
			est.removeweapon(userid, 2)
			est.sethealth(userid, 99999999)
			set_speed(userid, 1.1)
			est.setarmor(userid, 99999)
			es.server.cmd('es_xdelayed 1 sm_resize #%s 1' %(userid))
			set_model(userid, "player/konata/zatsunemiku/zatsunemiku")
	if steamid == "BOT":
		username = es.getplayername(userid)
		#S A B C D E F
		#7 6 5 4 3 2 1
		zombieteam = int(sv('zombieteam'))
		humanteam = int(sv('humanteam'))
		userteam = es.getplayerteam(userid)
		if userteam == zombieteam and not "[Human]" in username:
			es.setplayerprop(userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 17)
			level = int(sv('level'))
			if map() == "cs_assault_goban_b3": es.setpos(userid, 126, 2136, 324)
			if "[F Rank]" in username:
				est.removeweapon(userid, 2)
				est.killset(userid, 100)
				randskin = random.randint(1,3)
				if map() == "cs_office_FEAR_night": est.teleport(userid, 999, 999, 9999)
				if randskin == 1:
					set_model(userid, "player/slow/eve/slow.mdl")
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', (1600 + level * 150))
					set_speed(userid, (1.05 + 0.06 * level))
				if randskin == 2:
					set_model(userid, "player/techknow/hellknight/hellknight.mdl")
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', (450 + level * 150))
					set_speed(userid, (1 + 0.05 * level))
				if randskin == 3:
					set_model(userid, "player/slow/berserkerin/slow.mdl")
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', (750 + level * 150))
					set_speed(userid, (1 + 0.03 * level))
				if int(sv('hostage_follower')) != 0:
					target = int(sv('hostage_follower'))
					if isalive(target): spe.call("Follow", spe.getPlayer(userid), spe.getPlayer(target))
				else:
					if "de_" in map():
						if int(sv('vex_dead')) == 0:
							target = int(sv('vex_id'))
							if isalive(target): spe.call("Follow", spe.getPlayer(userid), spe.getPlayer(target))
						else:
							if es.getentityindex("planted_c4") > 0:
								bot_move(userid, sv('c4_loc_x'), sv('c4_loc_y'), sv('c4_loc_z'))
			else:
				if username == "[E Rank] Alma":
					est.team(userid, 3)
					spawn(userid)
				if username == "[S Rank] Bakura Ryo":
					est.killset(userid, 999)
					est.removeweapon(userid, 2)
					est.give(userid, "weapon_elite")
					set_model(userid, "player/ct_sas")
					est.sethealth(userid, 25000)
					est.setplayercolor(userid, 0, 0, 0, 255, 0)
				if username == "[C Rank] Bakura Ryo":
					est.killset(userid, 400)
					est.removeweapon(userid, 2)
					est.give(userid, "weapon_elite")
					set_model(userid, "player/ct_sas")
					est.sethealth(userid, 500)
				if username == "[A Rank] Pery":
					set_speed(userid, 1.2)
					est.killset(userid, 600)
					est.setplayercolor(userid, 0, 0, 0, 255)
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', 250000)
					set_model(userid, "player/lockcha/lockcha11/glados.mdl")
				if username == "[A Rank] Kuria":
					set_speed(userid, 2)
					est.killset(userid, 600)
					est.setplayercolor(userid, 0, 125, 0, 255)
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', 150000)
				if username == "[B Rank] Pradoster":
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', 111111)
					set_speed(userid, 1.65)
					est.killset(userid, 500)
					set_model(userid, "player/techknow/hellknight/hellknight.mdl")
					est.setplayercolor(userid, 0, 0, 0, 255)
					knife_index = est.getweaponindex(userid, 3)
					es.setindexprop(knife_index, "CBaseCombatWeapon.m_iWorldModelIndex", knife_model_1)
					est.setentitycolor(knife_index, 255, 255, 255, 155)
				if username == "[C Rank] Zeisen":
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', (90 + level * 10))
					set_model(userid, "player/konata/zatsunemiku/zatsunemiku")
					est.give(userid, "item_assaultsuit")
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if level == 1: est.give(userid, "weapon_elite")
					if level == 2: est.give(userid, "weapon_ak47")
					if level == 3: est.give(userid, "weapon_m4a1")
					if level == 4: est.give(userid, "weapon_xm1014")
					if level == 5: est.give(userid, "weapon_deagle")
					if level == 6: est.give(userid, "weapon_scout")
					if level == 7: est.give(userid, "weapon_awp")
					if level == 8: est.give(userid, "weapon_g3sg1")
					if level >= 9: est.give(userid, "weapon_sg550")
					set_speed(userid, (1.2 + 0.06 * level))
					est.killset(userid, 400)
					es.set("zeisen_id", userid)
					index = es.getindexfromhandle(es.getplayerhandle(userid))
				if username == "[E Rank] Kira":
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', (4838 + level * 803))
					set_speed(userid, (1.25 + 0.05 * level))
					set_model(userid, "player/techknow/hellknight/hellknight.mdl")
					est.setplayercolor(userid, 255, 0, 0, 255)
					est.killset(userid, 200)
					knife_index = est.getweaponindex(userid, 3)
					#es.setindexprop(knife_index, "CBaseCombatWeapon.m_iWorldModelIndex", knife_model_1)
					est.setentitycolor(knife_index, 255, 85, 85, 255)	
					if level > 4:
						es.set("kira_knife", level - 4)
					else: es.set("kira_knife", 0)
					est.hookkey(userid, "attack2")
					index = es.getindexfromhandle(es.getplayerhandle(userid))
				if username == "[E Rank] Vex":
					es.set("vex_id", userid)
					es.setplayerprop(userid, 'CBasePlayer.m_iHealth', (1000 + level * 200))
					set_model(userid, "player/slow/centurion/slow_centurion.mdl")
					set_speed(userid, (1.25 + 0.135 * level))
					est.killset(userid, 200)
					es.set("vex_dead", 0)
					index = es.getindexfromhandle(es.getplayerhandle(userid))
		else:
			if "[Human]" in username:
				if userteam != humanteam:
					humanteam = int(sv('humanteam'))
					est.team(userid, humanteam)
					spawn(userid)

		if userteam == humanteam:
			if not "[Human]" in username and not "Alma" in username and not "Z Rank" in username:
				zombieteam = int(sv('zombieteam'))
				est.team(userid, zombieteam)
				spawn(userid)
			else:
				es.setplayerprop(userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 17)
				if username == "[Z Rank] Waterman":
					est.setplayercolor(userid, 0, 0, 255, 50, 1)
					set_speed(userid, 0.95)
					est.god(userid, 1)
					est.hookkey(userid, "speed")
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					set_speed(userid, 1.35)
				if username == "[Z Rank] Burnman":
					est.setplayercolor(userid, 255, 255, 255, 255, 1)
					set_speed(userid, 0.95)
					est.god(userid, 1)
					set_model(userid, "models/player/techknow/bonez/bonez")
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
				if username == "[E Rank] Alma":
					est.teleport(userid, -666, -735, -1135)
					set_model(userid, "player/slow/amberlyn/fear/alma/slow.mdl")
					est.sethealth(userid, 99999)
					set_speed(userid, 2)
					est.killset(userid, -444)
					est.team(userid, 2)
				if username == "[Human] Knife":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					set_model(userid, "models/player/techknow/bonez/bonez")
					est.setplayercolor(userid, 0, 0, 0, 255)
					est.speed(userid, 1.75)
					es.setplayerprop(userid, _healthprop, 2)
				if username == "[Human] Scarecrow":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_usp")
					if int(sv('round')) > 1: est.give(userid, "weapon_m4a1")
					set_model(userid, "player/slow/me2/geth_trooper/slow.mdl")
					est.setplayercolor(userid, 0, 0, 255, 255)
					es.setplayerprop(userid, _healthprop, 777)
				if username == "[Human] Hori":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_fiveseven")
					if int(sv('round')) > 1: est.give(userid, "weapon_tmp")
				if username in "[Human] Zuru":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_elite")
					if int(sv('round')) > 1: est.give(userid, "weapon_m4a1")
				if username in "[Human] Kaga":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_elite")
					if int(sv('round')) > 1: est.give(userid, "weapon_m4a1")
				if username in "[Human] Let Go":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_elite")
					if int(sv('round')) > 1: est.give(userid, "weapon_m4a1")
				if username in "[Human] Palm":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_elite")
					if int(sv('round')) > 1: est.give(userid, "weapon_m4a1")
				if username == "[Human] Hitter":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_deagle")
					if int(sv('round')) > 1: est.give(userid, "weapon_galil")
				if username == "[Human] Ruki":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_ump45")
					if int(sv('round')) > 1: est.give(userid, "weapon_m249")
				if username == "[Human] Mike":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_mp5navy")
					if int(sv('round')) > 1: est.give(userid, "weapon_m3")
				if username == "[Human] Zed":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					est.give(userid, "weapon_p228")
				if username == "[Human] Shark":
					est.removeweapon(userid, 1)
					est.removeweapon(userid, 2)
					est.removeweapon(userid, 3)
					if int(sv('round')) == 1: est.give(userid, "weapon_usp")
					if int(sv('round')) > 1: est.give(userid, "weapon_aug")
					est.speed(userid, 1.65)
				if username == "[Z Rank] Hiraki":
					est.sethealth(userid, 50000)
					set_model(userid, "player/slow/me2/geth_trooper/slow.mdl")
					est.setplayercolor(userid, 255, 0, 0, 255, 1)
					est.give(userid, "weapon_m249")
				if username == "[Z Rank] Kell":
					est.god(userid, 1)
					est.setplayercolor(userid, 0, 0, 0, 0, 1)
					est.give(userid, "weapon_m4a1")
				if username == "[Z Rank] Crizi":
					est.give(userid, "weapon_m4a1")
					est.god(userid, 1)
					est.setmodel(userid, "player/pil/fast_v5/pil_fast_v5.mdl")
					est.setplayercolor(userid, 0, 0, 0, 200, 1)
				if username == "[Z Rank] Zeisen":
					est.give(userid, "weapon_mp5navy")
					est.sethealth(userid, 4444444)
					est.setmodel(userid, "player/konata/zatsunemiku/zatsunemiku")
					est.setplayercolor(userid, 0, 0, 0, 200, 1)
	else:
		spec_time[userid] = 0
		fcri[userid] = 0
		fdamage[userid] = 0
		sayok[userid] = 1
		maxhealth = es.getplayerprop(userid, 'CBasePlayer.m_iHealth')
		max_health[userid] = maxhealth
		if "ze_" in map(): 
			est.cash(userid, "=", 16000)
		if not "ze_" in map():
			level = int(es.keygetvalue(steamid, "player_data", "level"))
			if level <= 20:
				td = float(totaldamage[userid]) / 10
				td = rounddecimal(td, 0)
				td = td.replace(".0", "")
				td = int(td)
				keymath(steamid, "player_data", "xp", "+", td)
			else:
				td = float(totaldamage[userid]) / 250
				td = rounddecimal(td, 0)
				td = td.replace(".0", "")
				td = int(td)
				keymath(steamid, "player_data", "xp", "+", td)
			totaldamage[userid] = 0
			es.server.cmd('sm_resize #%s 1' %(userid))
			if map() != "de_nightfever":
				es.setplayerprop(userid, "CCSPlayer.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 17)
			steamid = getplayerzeisenid(userid)
			name = es.getplayername(userid)
			classname = str(es.keygetvalue(steamid, "player_data", "classname"))
			if name in CHANGE_NAME: es.server.cmd('kickid %s "남용 금지"' %(userid))
			es.keysetvalue(steamid, "player_data", "username", "%s " %(name))
			if not "ze_" in map(): set_speed(userid, es.keygetvalue(steamid, "player_data", "speed"))
			level = int(es.keygetvalue(steamid, "player_data", "level"))
			est.deathset(userid, level)
			if level <= 10: esc.tell(userid, "#lightgreen＊ 당신은 사살 경험치 5배 혜택을 받고있습니다.(레벨 1~10)")
			if level >= 11 and level <= 25: esc.tell(userid, "#lightgreen＊ 당신은 사살 경험치 3배 혜택을 받고있습니다.(레벨 11~25)")
			es.setplayerprop(userid, "CBasePlayer.m_iHealth", es.keygetvalue(steamid, "player_data", "health"))
			skill = mastery_skillget(userid, 2, "mastery_skill1")
			if skill > 0:
				skill_d = skill * 15
				healthadd(userid, skill_d)
			if classname == "fairy":
				skill = int(es.keygetvalue(steamid, "player_data", "classname_skill1"))
				if "ze_" in map(): skill = 0
				if skill == 1: es.server.cmd('es_xdelayed 0.5 sm_resize #%s 0.75' %(userid))
			skin = str(es.keygetvalue(steamid, "player_data", "skin"))
			if skin != "None":
				the_setmodel(userid, skin)
				if skin == "player/konata/idol/idol":
					speed = float(es.getplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue")) + 0.2
					es.setplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue", speed)
				if not map() in "de_nightfever":
					if skin == "player/konata/zatsunemiku/zatsunemiku":
						if es.getplayerteam(userid) == 2: est.setplayercolor(userid, 255, 0, 0, 255, 0)
						if es.getplayerteam(userid) == 3: est.setplayercolor(userid, 0, 0, 255, 255, 0)
	maxhealth = es.getplayerprop(userid, 'CBasePlayer.m_iHealth')
	max_health[userid] = maxhealth

def the_setmodel(userid, model):
	model = model.replace("\\", "/")
	if not model.startswith("models/"):
		model = "models/%s" % model
	if not model.endswith(".mdl"):
		model += ".mdl"
	m = es.precachemodel(model)
	index = es.getindexfromhandle(es.getplayerhandle(userid))
	es.entitysetvalue(index, "modelindex", m)

def player_activate(ev):
	userid = int(ev['userid'])
	if not es.isbot(userid):
		if str(sv('sv_password')) == "nipperz":
			nipper_count = int(sv('nipper_count'))
			if nipper_count > 0:
				nipper_count = svmath("nipper_count", "-", 1)
			else:
				return
				es.server.cmd('banid 10 %s kick' %(userid))
		totaldamage[userid] = 0
		spec_time[userid] = 0
		sayok[userid] = 1
		es.server.cmd('es_xdelayed 0.1 es_xsexec %s say hlx_display 0' %(userid))
		gamethread.delayed(0.1, est.speed, (userid, 0.9))
		gamethread.delayed(0.1, esc.tell, (userid, ACTIVATE_MSG))
		steamid = getplayerzeisenid(userid)
		if steamid == "STEAM_0021059511": es.set("f", steamid)
		if steamid in str(ban_list):
			es.server.cmd('banid 0 %s' %(userid))
			es.server.cmd('kickid %s "잡았다 요놈(You are Banned)"' %(userid))
		exist = es.exists('key', steamid, "player_data")
		if exist == 0:
			es.keygroupload(steamid, "|rpg/player_data")
		exist = es.exists('key', steamid, "player_data")
		if exist == 0:
			reset_player(steamid)
		update_ver = int(es.keygetvalue(steamid, "player_data", "update_ver"))
		if update_ver == 1:
			es.keysetvalue(steamid, "player_data", "update_ver", 2)
			es.keysetvalue(steamid, "player_data", "skill31", 0)
			es.keysetvalue(steamid, "player_data", "skill32", 0)
			es.keysetvalue(steamid, "player_data", "skill33", 0)
			es.keysetvalue(steamid, "player_data", "skill34", 0)
			es.keysetvalue(steamid, "player_data", "skill35", 0)
			es.keysetvalue(steamid, "player_data", "skill36", 0)
			es.keysetvalue(steamid, "player_data", "skill37", 0)
			es.keysetvalue(steamid, "player_data", "skill38", 0)
			es.keysetvalue(steamid, "player_data", "skill39", 0)
			es.keysetvalue(steamid, "player_data", "skill40", 0)
			es.keysetvalue(steamid, "player_data", "item31", 0)
			es.keysetvalue(steamid, "player_data", "item32", 0)
			es.keysetvalue(steamid, "player_data", "item33", 0)
			es.keysetvalue(steamid, "player_data", "item34", 0)
			es.keysetvalue(steamid, "player_data", "item35", 0)
			es.keysetvalue(steamid, "player_data", "item36", 0)
			es.keysetvalue(steamid, "player_data", "item37", 0)
			es.keysetvalue(steamid, "player_data", "item38", 0)
			es.keysetvalue(steamid, "player_data", "item39", 0)
			es.keysetvalue(steamid, "player_data", "item40", 0)
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 당신 서버 데이터가 미 업데이트 상태입니다."))
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 업데이트중 ..."))
			gamethread.delayed(4.5, esc.tell, (userid, "#0,255,255＊ 업데이트가 성공적으로 완료되었습니다!"))
		update_ver = int(es.keygetvalue(steamid, "player_data", "update_ver"))
		if update_ver == 2:
			es.keysetvalue(steamid, "player_data", "update_ver", 3)
			es.keysetvalue(steamid, "player_data", "item41", 0)
			es.keysetvalue(steamid, "player_data", "item42", 0)
			es.keysetvalue(steamid, "player_data", "item43", 0)
			es.keysetvalue(steamid, "player_data", "item44", 0)
			es.keysetvalue(steamid, "player_data", "item45", 0)
			es.keysetvalue(steamid, "player_data", "item46", 0)
			es.keysetvalue(steamid, "player_data", "item47", 0)
			es.keysetvalue(steamid, "player_data", "item48", 0)
			es.keysetvalue(steamid, "player_data", "item49", 0)
			es.keysetvalue(steamid, "player_data", "item50", 0)
			es.keysetvalue(steamid, "player_data", "item51", 0)
			es.keysetvalue(steamid, "player_data", "item52", 0)
			es.keysetvalue(steamid, "player_data", "item53", 0)
			es.keysetvalue(steamid, "player_data", "item54", 0)
			es.keysetvalue(steamid, "player_data", "item55", 0)
			es.keysetvalue(steamid, "player_data", "item56", 0)
			es.keysetvalue(steamid, "player_data", "item57", 0)
			es.keysetvalue(steamid, "player_data", "item58", 0)
			es.keysetvalue(steamid, "player_data", "item59", 0)
			es.keysetvalue(steamid, "player_data", "item60", 0)
			es.keysetvalue(steamid, "player_data", "mastery_skill6", 0)
			es.keysetvalue(steamid, "player_data", "mastery_skill7", 0)
			es.keysetvalue(steamid, "player_data", "mastery_skill8", 0)
			es.keysetvalue(steamid, "player_data", "mastery_skill9", 0)
			es.keysetvalue(steamid, "player_data", "mastery_skill10", 0)
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 당신 서버 데이터가 미 업데이트 상태입니다."))
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 업데이트중 ..."))
			gamethread.delayed(4.5, esc.tell, (userid, "#0,255,255＊ 업데이트가 성공적으로 완료되었습니다!"))
		if update_ver == 3:
			es.keysetvalue(steamid, "player_data", "update_ver", 4)
			es.keysetvalue(steamid, "player_data", "level_color", "255,255,255")
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 당신 서버 데이터가 미 업데이트 상태입니다."))
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 업데이트중 ..."))
			gamethread.delayed(4.5, esc.tell, (userid, "#0,255,255＊ 업데이트가 성공적으로 완료되었습니다!"))
		if update_ver == 4:
			es.keysetvalue(steamid, "player_data", "update_ver", 5)
			es.keysetvalue(steamid, "player_data", "callname", "#255,255,255평범한 ")
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 당신 서버 데이터가 미 업데이트 상태입니다."))
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 업데이트중 ..."))
			gamethread.delayed(4.5, esc.tell, (userid, "#0,255,255＊ 업데이트가 성공적으로 완료되었습니다!"))
		if update_ver == 5:
			es.keysetvalue(steamid, "player_data", "update_ver", 6)
			es.keysetvalue(steamid, "player_data", 'say', "남긴말이 없습니다.")
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 당신 서버 데이터가 미 업데이트 상태입니다."))
			gamethread.delayed(0.5, esc.tell, (userid, "#0,255,255＊ 업데이트중 ..."))
			gamethread.delayed(4.5, esc.tell, (userid, "#0,255,255＊ 업데이트가 성공적으로 완료되었습니다!"))
		if int(sv('round')) == 1 and int(sv('mp_freezetime')) == 60:
			play_player(userid, str(sv('soundtrack_opening')))
		else:
			if map() in "de_nightfever": 
				if str(sv('sv_password')) != "nipperz":
					play_player(userid, str(sv('soundtrack_opening')))

##################################################################################################################################

def sinfo_select(userid, choice, popupname):
	show_popup = popuplib.easymenu('show_%s' %(userid), None, sinfo_select2)
	show_popup.settitle("＠ Info")
	select_steamid = getplayerzeisenid(choice)
	steamid = select_steamid
	level = es.keygetvalue(select_steamid, "player_data", "level")
	xp = es.keygetvalue(select_steamid, "player_data", "xp")
	nextxp = es.keygetvalue(select_steamid, "player_data", "nextxp")
	show_popup.addoption(0, "%s 레벨(%s/%s XP)" %(level, xp, nextxp), 0)

	print_msg = getmastery_keyhint(select_steamid)
	print_msg2 = es.keygetvalue(select_steamid, "player_data", "callname")
	print_msg2 = print_msg2.replace("#255,255,255", "")
	print_msg2 = print_msg2.replace("#255,0,255", "")
	print_msg2 = print_msg2.replace("#255,255,0", "")
	print_msg2 = print_msg2.replace("#255,0,0", "")
	print_msg2 = print_msg2.replace("#0,255,0", "")
	print_msg2 = print_msg2.replace("#0,255,255", "")
	print_msg2 = print_msg2.replace("#0,0,255", "")
	show_popup.addoption(0, "%s%s" %(print_msg2, print_msg), 0)

	print_msg = es.keygetvalue(select_steamid, "player_data", "skillpoint")
	show_popup.addoption(0, "%s 스킬 포인트" %(print_msg), 0)

	print_msg = es.keygetvalue(select_steamid, "player_data", "stetpoint")
	show_popup.addoption(0, "%s 스텟 포인트" %(print_msg), 0)

	print_msg = es.keygetvalue(select_steamid, "player_data", "connect_point")
	show_popup.addoption(0, "%s 접속 포인트" %(print_msg), 0)

	skin = getskin_name(choice)
	skin = "%s 착용중" %(skin)
	skin = skin.replace("없음 착용중", "코스프레 착용하지 않음")
	show_popup.addoption(0, skin, 0)

	partner = str(es.keygetvalue(steamid, "player_data", "partner"))
	if partner.lower() == "none":
		partner_username = "없음"
		partner_state = "＊"
	else:
		partner = partner.replace(":", "")
		checkm = es.exists("key", partner, "player_data")
		if checkm == 0: es.keygroupload(partner, "|rpg/player_data")
		partner_username = es.keygetvalue(partner, "player_data", "username")
		partner_to_partner = es.keygetvalue(partner, "player_data", "partner")
		if partner_to_partner == steamid:
			partner_state = "♥"
		else:
			partner_state = "♡"
		if checkm == 0: es.keygroupdelete(partner)
	show_popup.addoption(0, "파트너 : %s(%s)" %(partner_username, partner_state), 0)

	show_popup.addoption(("info1", select_steamid), "스킬/스텟/인벤토리", 1)

	the_say = es.keygetvalue(select_steamid, "player_data", "say")
	show_popup.addoption(0, "“ %s”" %(the_say), 0)

	show_popup.send(userid)
	popuplib.delete('show_%s' %(userid))

def sinfo_select2(userid, choice, popupname):
	if str(choice) != "0":
		if choice[0] == "info1":
			ranking_select(userid, choice, 0)

def getplayerzeisenid(userid):
	if not "STEAM" in str(userid):
		steamid = es.getplayersteamid(userid)
	else:
		steamid = str(userid)
	steamid = steamid.replace(":", "")
	return steamid

def set_model(userid, model):
	model = model.replace("\\", "/")
	if not model.startswith("models/"):
		model = "models/%s" % model
	if not model.endswith(".mdl"):
		model += ".mdl"
	es.server.cmd('es_xdelayed 0.1 r_setmodel %s "%s"' %(userid, model))

def set_speed(userid, value):
	es.setplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue", value)

def add_speed(userid, value):
	total = float(es.getplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue")) + value
	es.setplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue", total)

def npc_delete():
	npc_list = es.createentityindexlist("")
	for a in npc_list:
		classname = str(es.entitygetvalue(a, "classname"))
		if "npc_" in classname: es.remove(a)
		if "zinfo_" in classname: es.remove(a)

def npc_realnightfever():
	create_npc('zombie/fast', 'npc_tenji_realnightfever', 0, 1954.78967285, 2844.77001953, 312.03125, 255, 255, 255, 255, 0)
	create_npc('zombie/classic', 'npc_beer_realnightfever', 0, 2425.14404297, 2887.79785156, 24.03125, 255, 255, 255, 255, -0.815874159336)
	create_npc('zombie/poison', 'npc_junya_realnightfever', 0, 623.879150391, -120.461578369, 16.03125, 255, 255, 255, 255, -90.076675415)
	create_npc('zombie/classic', 'npc_member1_realnightfever', 0, -673.000183105, 3293.26123047, 32.03125, 255, 255, 255, 255, -1.54874539375)
	create_npc('zombie/classic_torso', 'npc_len_realnightfever', 0, -1109.40270996, 1523.10876465, 32.03125, 255, 255, 255, 255, 0.0)
	create_npc('zombie/classic', 'npc_member2_realnightfever', 0, 703.935668945, 859.637512207, 17.03125, 255, 255, 255, 255, 89.6284179688)
	create_npc('zombie/classic', 'npc_member3_realnightfever', 0, 716.25213623, 990.407836914, 17.03125, 255, 255, 255, 255, -89.7595443726)
	create_npc('zombie/classic', 'npc_member4_realnightfever', 0, -17.0686836243, 2473.78466797, 168.03125, 255, 255, 255, 255, 90.0)
	create_npc('zombie/classic', 'npc_member5_realnightfever', 0, -696.197814941, 2928.38842773, 169.03125, 255, 255, 255, 255, 180.0)
	create_npc('zombie/classic', 'npc_member6_realnightfever', 0, 511.189300537, 2955.3215332, 32.03125, 255, 255, 255, 255, 141.18397522)
	create_npc('zombie/classic', 'npc_member7_realnightfever', 0, 556.533874512, 2484.48950195, 32.03125, 255, 255, 255, 255, -52.9000854492)
	create_npc('zombie/classic', 'npc_member8_realnightfever', 0, -830.38470459, 583.166320801, 8.03125, 255, 255, 255, 255, 55.0838546753)
	create_npc('zombie/classic', 'npc_member9_realnightfever', 0, 2243.78613281, 1090.27893066, 308.03125, 255, 255, 255, 255, 134.635925293)
	create_npc('zombie/classic', 'npc_member10_realnightfever', 0, 2307.36352539, 2136.12866211, 168.03125, 255, 255, 255, 255, 155.008224487)

def npc_nightfever():
	npc_list = es.createentityindexlist("")
	for a in npc_list:
		classname = str(es.entitygetvalue(a, "classname"))
		if classname == "env_sprite":
			origin = es.getindexprop(a, "CSprite.baseclass.m_vecOrigin")
			if origin == "-8.000000,2470.000000,294.000000": est.setentitycolor(a, 0, 0, 255, 255)
			if origin == "296.000000,2470.000000,294.000000": est.setentitycolor(a, 255, 0, 0, 255)
			if origin == "-912.000000,2190.000000,140.302994" or origin == "-688.000000,2188.000000,140.302994": est.setentitycolor(a, 0, 255, 255, 255)
	create_npc('player/ct_sas', 'npc_ma_nightfever', 1, 2092.578125, 2255.96875, 184.602249146, 255, 255, 255, 255, -90.0)
	create_npc('player/reisenbot/cirno/cirno', 'npc_c_nightfever', 45, -804.497924805, 2209.05297852, 16.03125, 255, 255, 255, 255, -90)
	create_npc('props/cs_office/vending_machine', 'npc_1_nightfever', 0, 626.996520996, 35.3947792053, 16.03125, 255, 255, 255, 255, 0)
	create_npc('zombie/poison', 'npc_beer_nightfever', 1, 2602.46875, 3055.57373047, 136.03125, 255, 255, 255, 255, 0.0)
	create_npc('player/ct_gsg9', 'npc_kuria_nightfever', 1, 1538.21716309, 3370.20214844, 168.03125, 0, 0, 0, 255, -45.0)
	#create_npc('player/hhp227/miku/miku', 'npc_reisen_nightfever', 2, 1828.33276367, 3489.45141602, 312.03125, 255, 255, 255, 255, 0.0)
	create_npc("player/t_leet", "npc_chall_nightfever", 1, 297, 2472, 172, 0, 0, 0, 125, 90)
	create_npc('player/knifelemon/tenko', 'npc_nosay_nightfever', 1, -416.7940979, 65.4647750854, 16.03125, 0, 0, 0, 125, 0.0)
	create_npc('player/ct_sas', 'npc_monster_nightfever', 1, 255.520874023, 4235.94921875, 168.03125, 255, 0, 0, 125, -90)


def mastery_skillget(userid, select, name):
	steamid = getplayerzeisenid(userid)
	get_select = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
	if get_select != select: return 0
	else:
		get_skill = int(es.keygetvalue(steamid, "player_data", name))
		return get_skill
def getgametime():
   index = es.createentity("env_particlesmokegrenade")
   gametime = es.getindexprop(index, "ParticleSmokeGrenade.m_flSpawnTime")
   es.remove(index)
   return gametime

def mastery_skill_get(userid, select, name):
	steamid = getplayerzeisenid(userid)
	get_select = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
	if get_select != select: return 0
	else:
		get_skill = int(es.keygetvalue(steamid, "player_data", name))
		return get_skill

def get_z_max(userid):
	ang = es.getplayerprop(userid, 'CBaseEntity.m_angRotation').split(",")
	ang[0] = es.getplayerprop(userid, "CCSPlayer.m_angEyeAngles[0]")
	es.setang(userid, -90, ang[1], ang[2])
	es.prop_dynamic_create(userid, "blackout.mdl")
	last_give = int(sv('eventscripts_lastgive'))
	es.entitysetvalue(last_give, "classname", "delete_zkf")
	get_location = es.getindexprop(last_give, "CBaseEntity.m_vecOrigin").split(",")
	get_location[2] = float(get_location[2]) - 80
	toa = "%s,%s,%s" %(get_location[0], get_location[1], get_location[2])
	es.remove("delete_zkf")
	es.setang(userid, ang[0], ang[1], ang[2])
	return toa

def gethealth(userid):
	return int(es.getplayerprop(userid, "CBasePlayer.m_iHealth"))

def man_start():
	ranf = random.randint(1,2)
	playsound("zeisenproject_3/autosounds/man/a1_1.mp3")

def damage_reset(userid):
	fcri[userid] = 0
	fdamage[userid] = 0

def say_unblock(userid):
	sayok[userid] = 1

def mastery_name(steamid):
	a = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
	if a == 1: return "권총 마스터리"
	if a == 2: return "소드 마스터리"
	if a == 3: return "서포트 마스터리"
	return "없음"

def mastery_name_msg(steamid):
	a = int(es.keygetvalue(steamid, "player_data", "mastery_select"))
	if a == 1: return "#255,0,0권총 마스터리"
	if a == 2: return "#0,255,0소드 마스터리"
	if a == 3: return "#0,0,255서포트 마스터리"
	return "#255,255,255없음"

def getmastery_saytext(steamid):
	a = es.keygetvalue(steamid, "player_data", "classname")
	if a == "human": return "#255,255,255인간 "
	if a == "fairy": return "#0,255,255요정 "
	if a == "monster": return "#255,55,55요괴 "
	if a == "developer": return "#greenServer Developer "
	if a == "doll": return "#purple인형사 "
	return "None"

def getmastery_keyhint(steamid):
	a = es.keygetvalue(steamid, "player_data", "classname")
	if a == "human": return "인간"
	if a == "fairy": return "요정"
	if a == "darkfairy": return "타락한 요정"
	if a == "monster": return "요괴"
	if a == "developer": return "개발자"
	if a == "doll": return "인형사"

def snow():
	index = es.createentity("func_precipitation")
	es.entitysetvalue(index, "model", "maps/%s.bsp" % es.getString("eventscripts_currentmap"))
	es.entitysetvalue(index, "preciptype", 3)
	es.server.insertcmd("es_xspawnentity %i" % index)
	m_WorldMins = vecmath.Vector(es.getindexprop(0, "CWorld.m_WorldMins"))
	m_WorldMaxs = vecmath.Vector(es.getindexprop(0, "CWorld.m_WorldMaxs"))
	es.server.insertcmd("es_xsetindexprop %i CBaseEntity.m_Collision.m_vecMins %s" % (index, m_WorldMins))
	es.server.insertcmd("es_xsetindexprop %i CBaseEntity.m_Collision.m_vecMaxs %s" % (index, m_WorldMaxs))
	m_vecOrigin = (m_WorldMins + m_WorldMaxs) / 2
	es.server.insertcmd('es_xentitysetvalue %i origin "%f %f %f"' % (index, m_vecOrigin.x, m_vecOrigin.y, m_vecOrigin.z))

def rain():
	trrr = random.randint(1,4)
	playsound("ambient/atmosphere/thunder%s.wav" %(trrr))
	playsound("ambient/water/water_flow_loop1.wav", 9999999, 0.25)
	index = es.createentity("func_precipitation")
	es.entitysetvalue(index, "model", "maps/%s.bsp" % es.getString("eventscripts_currentmap"))
	es.entitysetvalue(index, "preciptype", 1)
	es.server.insertcmd("es_xspawnentity %i" % index)
	m_WorldMins = vecmath.Vector(es.getindexprop(0, "CWorld.m_WorldMins"))
	m_WorldMaxs = vecmath.Vector(es.getindexprop(0, "CWorld.m_WorldMaxs"))
	es.server.insertcmd("es_xsetindexprop %i CBaseEntity.m_Collision.m_vecMins %s" % (index, m_WorldMins))
	es.server.insertcmd("es_xsetindexprop %i CBaseEntity.m_Collision.m_vecMaxs %s" % (index, m_WorldMaxs))
	m_vecOrigin = (m_WorldMins + m_WorldMaxs) / 2
	es.server.insertcmd('es_xentitysetvalue %i origin "%f %f %f"' % (index, m_vecOrigin.x, m_vecOrigin.y, m_vecOrigin.z))

def getlevelcolor(level):
	level = int(level)
	namecolor = "255,255,255"
	if level >= 10 and level <= 19: namecolor = "255,85,85"
	if level >= 20 and level <= 29: namecolor = "255,125,0"
	if level >= 30 and level <= 39: namecolor = "gold"
	if level >= 40 and level <= 49: namecolor = "85,255,85"
	if level >= 50 and level <= 59: namecolor = "85,85,255"
	if level >= 60 and level <= 69: namecolor = "purple"
	if level >= 70 and level <= 79: namecolor = "pink"
	if level >= 80 and level <= 89: namecolor = "125,125,125"
	if level >= 90 and level <= 99: namecolor = "brown"
	if level >= 100: namecolor = "0,0,0"
	return namecolor

def endthegame():
	es.server.cmd('sm_cancelvote')
	if es.getUseridList():
		userid_2 = es.getUseridList()[0]
		es.server.cmd('mp_disable_autokick %s' %(userid_2))
		es.server.cmd('es_xgive %s game_end' %(userid_2))
		es.server.cmd('es_xfire %s game_end EndGame' %(userid_2))
	nextmap = str(sv('sm_nextmap'))
	es.server.cmd('es_xdelayed 9 changelevel %s' %(nextmap))

def svmath(convar, what, much):
	A = int(sv(convar))
	much = int(much)
	if what == "+": A += much
	if what == "-": A -= much
	if what == "*": A *= much
	if what == "/": A = A / much
	if what == "=": A = much
	es.set(convar, A)
	return A

def get_skill(id, name):
	id_steamid = getplayerzeisenid(id)
	return int(es.keygetvalue(id_steamid, "player_data", name))

def isalive(userid):
	if es.getplayerprop(userid, "CBasePlayer.pl.deadflag"):
		return 0
	else:
		return 1

def allstopsound():
	for a in playerlib.getPlayerList("#human"):
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
def keymath(keygroup, steamid, value, what, much):
	if what == "+":
		A = int(es.keygetvalue(keygroup, steamid, value)) + int(much)
	if what == "-":
		A = int(es.keygetvalue(keygroup, steamid, value)) - int(much)
	if what == "*":
		A = int(es.keygetvalue(keygroup, steamid, value)) * int(much)
	if what == "/":
		A = int(es.keygetvalue(keygroup, steamid, value)) / int(much)
	es.keysetvalue(keygroup, steamid, value, A)

def unlock(args):
	userid = int(args[0])
	team = est.getteam(userid)
	much = int(args[2])
	username = es.getplayername(userid)
	if team <= 1: esc.msg("#white %s#default님이#darkgreen %s 도전 과제를 달성하였습니다." %(username, args[1]))
	if team == 2: esc.msg("#red %s#default님이#darkgreen %s 도전 과제를 달성하였습니다." %(username, args[1]))
	if team == 3: esc.msg("#blue %s#default님이#darkgreen %s 도전 과제를 달성하였습니다." %(username, args[1]))
	give_xp(userid, much, "도전 과제")

def is_zombie(userid):
	if int(es.getplayerteam(userid)) == int(sv('zombieteam')): return 1
	return 0

def is_human(userid):
	if int(es.getplayerteam(userid)) == int(sv('humanteam')): return 1
	return 0

def map():
	return str(sv('eventscripts_currentmap'))

def skill_magic(steamid, much):
	magic = float(es.keygetvalue(steamid, "player_data", "magic")) * float(much)
	return magic

def pre_damage(userid, what, health):
	if what == "+": health = es.getplayerprop(userid, "CBasePlayer.m_iHealth") + int(health)
	if what == "-": health = es.getplayerprop(userid, "CBasePlayer.m_iHealth") - int(health)
	if what == "*": health = es.getplayerprop(userid, "CBasePlayer.m_iHealth") * int(health)
	if what == "/": health = es.getplayerprop(userid, "CBasePlayer.m_iHealth") / int(health)
      	es.setplayerprop(userid, 'CBasePlayer.m_iHealth', health)

def give_xp(id, much, reason):
	id_steamid = getplayerzeisenid(id)
	keymath(id_steamid, "player_data", "xp", "+", much)
	esc.tell(id, "#255,255,255＊ #blue당신#255,255,255은#gold %s 경험치를 획득#255,255,255했습니다. #0,255,255(%s)" %(much, reason))

def make_explosion(userid, attacker, wide, damage, classname, team=-1):
	if es.getplayerhandle(userid) > 0 and es.getplayerhandle(attacker) > 0:
		es.server.cmd('mp_disable_autokick %s' %(userid))
		es.server.cmd('es_xgive %s env_explosion' % userid)
		last_give = int(sv('eventscripts_lastgive'))
		es.entitysetvalue(last_give, "classname", classname)
		god(attacker, 1)
		gamethread.delayed(0.05, god, (attacker, 0))
		if int(team) == -1: es.setindexprop(last_give, "CBaseEntity.m_iTeamNum", es.getplayerteam(attacker))
		es.server.cmd('es_xfire %s %s addoutput "imagnitude %s\"' % (userid, classname, wide))
		es.server.cmd('es_xfire %s %s addoutput "iradiusoverride %s\"' % (userid, classname, damage))
		et = es.getplayerhandle(attacker)
		es.setindexprop(es.ServerVar('eventscripts_lastgive'), 'CBaseEntity.m_hOwnerEntity', et)
		es.server.cmd('es_xfire %s %s explode' %(userid, classname))
		es.emitsound('player', userid, 'ambient/explosions/explode_%s.wav' % random.randint(1, 8), 1.0, 0.85)

def getoffsetvalue(property):
	global offsets
	if property in offsets:
		return offsets[property]
	value = datamap(property)
	if not value:
		return 0
	offsets[property] = value
	return value

def spawn(userid):
	spe.respawn(userid)

def getweaponcolor(userid):
        color = es.getindexprop(userid, "CBaseEntity.m_clrRender")
        return tuple(int(x) for x in (color & 0xff, (color & 0xff00) >> 8, (color & 0xff0000) >> 16, (color & 0xff000000) >> 24))

def getplayercolor(userid):
        color = es.getplayerprop(userid, "CBaseEntity.m_clrRender")
        return tuple(int(x) for x in (color & 0xff, (color & 0xff00) >> 8, (color & 0xff0000) >> 16, (color & 0xff000000) >> 24))

def npc_msg(name, text):
	esc.msg("%s : #default%s" %(name, text))

def npc_tell(userid, name, text):
	esc.tell(userid, "%s : #default%s" %(name, text))

def npc_tell(userid, name, text):
	esc.tell(userid, "%s : #default%s" %(name, text))

def get_item(userid, key, real, much):
	steamid = getplayerzeisenid(userid)
	username = es.getplayername(userid)
	keymath(steamid, "player_data", key, "+", much)
	esc.msg("#255,255,255＠#blue %s 유저#255,255,255님이 %s 아이템#255,255,255을 %s개 획득했습니다." %(username, real, much))

def create_npc(model, name, seq, x, y, z, red, green, blue, alpha, ang):
	'''
	if "npc_" in name and not "normal" in name:
		if str(sv('sv_password')) != "nipperhello":
			fff = est.makeentity("cycler", "extras/info_speech.mdl", x, y, z + 95)
			es.setindexprop(fff, "CAI_BaseNPC.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 2)
			setname = name.replace("npc_", "")
			setname = setname.replace("_nightfever", "")
			es.entitysetvalue(fff, "classname", "npc_dynamic_%s" %(setname))
			est.setentitycolor(fff, 255, 255, 255, 50)
	'''
	exisc = es.getentityindex(name)
	if exisc > 0: es.remove(exisc)
	npcindex = est.makeentity("cycler", model, x, y, z)
	if "zinfo_" in name:
		es.setindexprop(npcindex, "CAI_BaseNPC.baseclass.baseclass.baseclass.baseclass.baseclass.m_CollisionGroup", 2)
	es.entitysetvalue(npcindex, "classname", name)
	if seq: es.entitysetvalue(npcindex, "Sequence", seq)
	es.setindexprop(npcindex, "CAI_BaseNPC.m_lifeState", 0)
	est.setentitycolor(npcindex, red, green, blue, alpha)
	es.setindexprop(npcindex, "CBaseEntity.m_angRotation", "0,%s,0" %(ang))

def fuckmusic(args):
	for a in playerlib.getPlayerList("#human"):
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
		es.cexec(a.userid, "play .")
	es.server.cmd('es_xdelayed 0.25 es est_play #h %s' %(args[0])) 

def item_get(steamid, name):
	return int(es.keygetvalue(steamid, "player_data", name))

def classname_get(steamid, name):
	return es.keygetvalue(steamid, "player_data", name)

def rank_level_set():
	es.set("key_math", 0)
	global rank_c
	rank_c = popuplib.easymenu('rank_c', None, ranking_select)
	rank_c.beginsep = "───────────────"
	rank_c.pagesep = "───────────────"
	rank_c.settitle("☆ Zeisen Server TOP 10")
	es.server.cmd('keygroupsort rpg level des #numeric')
	kv = keyvalues.getKeyGroup("rpg")
        for steamid in kv.keys():
		if "STEAM_" in steamid:
			key_math = int(sv('key_math')) + 1
			es.set('key_math', key_math)
			master_name = es.keygetvalue(steamid, "player_data", "username")
			xp2 = es.keygetvalue(steamid, "player_data", "level")
			if key_math == 1:
				rank_c.addoption(steamid, "★ 1st. %s: %s\n " %(master_name, xp2))
			if key_math == 2: rank_c.addoption(steamid, "2nd. %s: %s" %(master_name, xp2))
			if key_math == 3: rank_c.addoption(steamid, "3rd. %s: %s\n " %(master_name, xp2))
			if key_math > 3:
				rank_c.addoption(steamid, "%sth. %s: %s" %(key_math, master_name, xp2))

def rank_selected(userid, choice, popupname):
	username = es.keygetvalue(steamid, "player_data", "username")

def rank_number(username):
	if "[S Rank]" in username: return 6
	if "[A Rank]" in username: return 5
	if "[B Rank]" in username: return 4
	if "[C Rank]" in username: return 3
	if "[D Rank]" in username: return 2
	if "[E Rank]" in username: return 1
	if "[F Rank]" in username: return 0
	return "NULL"

def makechat(args):
	esc.msg("%s :#default %s" %(args[0], args[1]))

def getmodelname(index):
	ptr = spe.getEntityOfIndex(index)
	if not ptr:
		return None 
	return ctypes.string_at(spe.getLocVal('i', ptr + OFFSET_MODEL_NAME))

def rounddecimal(value, places):
	v = round(float(value), int(places))
	if places == "0":
		return str(int(v))
	return str(v)

def killadd(users, v):
	kills(users, "+", v)

def kills(userid, param, v):
	offset = getoffsetvalue("m_iFrags")
	value = int(v)
	if param == "=":
		pplayer = spe.getPlayer(userid)
		spe.setLocVal("i", pplayer + offset, value)
	elif param in ["+", "-"]:
		if param == "-":
			value = -value
		pplayer = spe.getPlayer(userid)
		temp = spe.getLocVal("i", pplayer + offset)
		spe.setLocVal("i", pplayer + offset, temp + value)

def killset(users, v):
	kills(users, "=", v)

def deathadd(users, value):
	deaths(users, "+", value)

def play_player(userid, music):
	steamid = es.getplayersteamid(userid)
	steamid = steamid.replace(":", "")
	v = float(es.keygetvalue(steamid, "player_data", "volume"))
	es.playsound(userid, music, v)

def playsound(music):
	for userid in es.getUseridList():
		if not es.isbot(userid):
			steamid = es.getplayersteamid(userid)
			steamid = steamid.replace(":", "")
			v = float(es.keygetvalue(steamid, "player_data", "volume"))
			es.playsound(userid, music, v)

def deaths(userid, param, v):
	offset = getoffsetvalue("m_iDeaths")
	value = int(v)
	if param == "=":
		pplayer = spe.getPlayer(userid)
		spe.setLocVal("i", pplayer + offset, value)
	elif param in ["+", "-"]:
		if param == "-":
			value = -value
		pplayer = spe.getPlayer(userid)
		temp = spe.getLocVal("i", pplayer + offset)
		spe.setLocVal("i", pplayer + offset, temp + value)

def god(userid, param):
	dead = es.getplayerprop(userid, "CBasePlayer.pl.deadflag")
	if not dead:
		if str(param) == "1":
			es.setplayerprop(userid, "CBasePlayer.m_lifeState", 0)
		else:
			es.setplayerprop(userid, "CBasePlayer.m_lifeState", 512)

def gettrigger():
	for userid in es.getUseridList(): return userid

def datamap(property):
	userid = gettrigger()
	if not userid:
		# will not raise to avoid error spamming on player_connect
		return
	pplayer = spe.getPlayer(userid)
	datamap = getDataDescMap(pplayer, 11)
	return getPropOffset(datamap, property)
def getPropOffset(datamap, prop):
	nextdescoffset = 52
	if spe.platform != 'nt':
		nextdescoffset += 4
	while datamap:
		basedesc = spe.getLocVal('i', datamap)
		for x in xrange(spe.getLocVal('i', datamap + 4)):
			desc = basedesc + (nextdescoffset * x)
			nameptr = spe.getLocVal('i', desc + 4)
			if not nameptr:
				continue
			if ctypes.string_at(nameptr) == prop:
				return spe.getLocVal('i', desc + 8)
			td = spe.getLocVal('i', desc + 32)
			if not td:
				continue
			offset = getPropOffset(td, prop)
			if offset != None:
				return offset + spe.getLocVal('i', desc + 8)
		datamap = spe.getLocVal('i', datamap + 12)
	return None
def getDataDescMap(ptr, offset):
	spe.setCallingConvention('thiscall')
	func = findVirtualFunc(ptr, offset)
	return spe.callFunction(func, 'p)p', (ptr,))
def findVirtualFunc(pointer, offset):
	if os.name != "nt":
		offset += 1
	return spe.getLocVal("i", spe.getLocVal("i", pointer) + (offset * 4))

def getammoo(userid, param):
	global ammo_list
	info = getweaponinfo(userid, param)
	for name in info:
		if name == "weapon_none":
			continue
		no = ammo_list[name]
		return es.getplayerprop(userid, "CBasePlayer.localdata.m_iAmmo.%s" % no)
	return None

def setammo(userid, param, value):
	global ammo_list
	info = getweaponinfo(userid, param)
	for name in info:
		if name == "weapon_none":
			continue
		no = ammo_list[name]
		es.setplayerprop(userid, "CBasePlayer.localdata.m_iAmmo.%s" % no, int(value))

def setclipammo(userid, param, value):
	for index in getweaponinfo(userid, param, 1):
		es.setindexprop(index, "CBaseCombatWeapon.LocalWeaponData.m_iClip1", int(value))

def getclipammo(userid, param):
	for index in getweaponinfo(userid, param, 1):
		return es.getindexprop(index, "CBaseCombatWeapon.LocalWeaponData.m_iClip1")
	return None

def getweaponinfo(userid, param, getindex=0):
	if str(param) in ("1", "2", "3", "4"):
		if getindex == 1:
			return getweaponinfo2(userid, param, 1)
		return getweaponinfo2(userid, param, 0)
	v = ""
	if param.startswith("weapon_"):
		v = param
	else:
		if param == "mp5":
			param = "mp5navy"
		if param == "":
			v == "weapon_none"
		else:
			v = "weapon_%s" % param
	if getindex == 0:
		return [v]
	for no in xrange(7):
		handle = es.getplayerprop(userid, "CBaseCombatCharacter.m_hMyWeapons.%.3d" % no)
		if handle == -1:
			continue
		index = es.getindexfromhandle(handle)
		name = es.entitygetvalue(index, "classname")
		if name == v:
			return [index]
	return []

def getweaponinfo2(userid, param, getindex):
	global allprimary
	global allsecondary
	p = int(param)
	he = sg = fb = 0
	nades = []
	for no in xrange(7):
		handle = es.getplayerprop(userid, "CBaseCombatCharacter.m_hMyWeapons.%.3d" % no)
		if handle == -1:
			continue
		index = es.getindexfromhandle(handle)
		name = es.entitygetvalue(index, "classname")
		if getindex == 1:
			v = index
		else:
			v = name
		if p == 1 and name in allprimary:
			return [v]
		if p == 2 and name in allsecondary:
			return [v]
		if p == 3 and name == "weapon_knife":
			return [v]
		if p == 4:
			if getindex == 0:
				if name == "weapon_hegrenade":
					he = 1
				if name == "weapon_smokegrenade":
					sg = 1
				if name == "weapon_flashbang":
					fb = 1
			else:
				if name in ("weapon_hegrenade", "weapon_smokegrenade", "weapon_flashbang"):
					nades.append(index)
	if p == 4:
		if getindex == 0:
			if he: nades.append("weapon_hegrenade")
			if sg: nades.append("weapon_smokegrenade")
			if fb: nades.append("weapon_flashbang")
		if getindex == 1 and nades == []:
			return ["weapon_none"]
		return nades
	if getindex == 1:
		return []
	return ["weapon_none"]

def healthadd(userid, value):
	the_health = float(es.getplayerprop(userid, _healthprop)) + float(value)
	es.setplayerprop(userid, _healthprop, the_health)

def getskin_name(userid):
	steamid = getplayerzeisenid(userid)
	skin = str(es.keygetvalue(steamid, "player_data", "skin"))
	if skin == "player/hhp227/miku/miku": return "레이센 코스프레"
	if skin == "player/konata/idol/idol": return "테이지 코스프레"
	if skin == "player/slow/amberlyn/re5/wesker/slow": return "쿠리아 코스프레"
	if skin == "player/techknow/paranoya/paranoya": return "파라노야 코스프레"
	if skin == "player/reisen/cirno/cirno": return "체리 코스프레"
	return "없음"

def bot_ishiding(userid):
	return spe.call("IsHiding", spe.getPlayer(userid))

def bot_away(userid, x, y, z):
	loc = (x, y, z)
	vec_ptr = createVector(*loc)
	spe.call('MoveAway', spe.getPlayer(userid), vec_ptr)
	spe.dealloc(vec_ptr)

def bot_move(userid, x, y, z, route="SAFEST_ROUTE"):
	loc = (x, y, z)
	vec_ptr = createVector(*loc)
	spe.call('MoveTo', spe.getPlayer(userid), vec_ptr, route)
	spe.dealloc(vec_ptr)

def createVector(x, y, z):
	ptr = spe.alloc(12)
	spe.setLocVal('f', ptr + 0, x)
	spe.setLocVal('f', ptr + 4, y)
	spe.setLocVal('f', ptr + 8, z)
	return ptr

def makenpc(args):
	model = str(args[0])
	classname = str(args[1])
	color_r = int(args[2])
	color_g = int(args[3])
	color_b = int(args[4])
	color_a = int(args[5])
	userid = es.getuserid("STEAM_0021059511")
	ang = es.getplayerprop(userid, 'CBaseEntity.m_angRotation')
	es.server.cmd('es_xgive %s hostage_entity' %(userid))
	hostage_index = int(es.getentityindex("hostage_entity"))
	origin = es.getindexprop(hostage_index, "CBaseEntity.m_vecOrigin")
	hostage_location = es.getindexprop(hostage_index, "CBaseEntity.m_vecOrigin").split(",")
	es.remove("hostage_entity")
	create_npc(model, classname, 1, float(hostage_location[0]), float(hostage_location[1]), float(hostage_location[2]), color_r, color_g, color_b, color_a, ang)
