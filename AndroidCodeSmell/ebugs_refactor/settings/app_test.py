#!/usr/bin/python3

"""
Application testing settings.
"""

"""
Whether or not the previous result files should be replaced. 
If set to 'False', an application test will only run and produce 
results if there are no results for it yet.
If set to 'True', every test will run and replace any existing 
result files.
"""
cs_replace_test_results = False

"""
Number of times that a test is repeated.
"""
cs_measure_repeats = 1

"""
The time, in millinseconds, that monkey needs to wait between 
injecting events.
"""
cs_throttle = 500  # 0.5 second

"""
Threshold time value, in milliseconds, for how long the Android 
device can be running tests without stopping. 
@Deprecated
"""
cs_phone_usage_threshold = 18000  # 5 hours

"""
The amount of time, in milliseconds, that the Android device 
stays idle before running tests again, after reaching the 
@cs_phone_usage_threshold.
"""
cs_recover_time = 600  # 15 minutes

## Monkey-related constants

"""
List of seeds used for the tests.
"""
cs_monkey_seeds = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25
]

_old_cs_monkey_seeds = [
    29,  #
    317,  #
    401,  #
    659,  #
    983  #
]

"""
Number of events simulated in each monkey test.
"""
cs_monkey_events = 20  # 100

"""
Percentage of simulated events related to activity change.
"""
cs_pct_activity_events = 30

"""
Mapping between each monkey event id and a description of 
what it actually does. 
"""
cs_monkey_events_info = {
    "0": "Touch events: down-up event in a single place on the screen.",
    "1": "Motion events: down event somewhere on the screen, a series of pseudo-random movements, and an up event.",
    "2": "Zoom events.",
    "3": "Trackball events: one or more random movements, sometimes followed by a click.",
    "4": "Rotation events: event that rotates the screen a random number of degrees.",
    "5": "Permission events (Unknown)",
    "6": "Basic navigation events: up/down/left/right, as input from a directional input device.",
    "7": "Major navigation events: events that will typically cause actions within the UI, such as the center button in a 5-way pad, the back key, or the menu key.",
    "8": "System events: keys generally reserved system use, such as Home, Back, Start Call, End Call, or Volume controls.",
    "9": "Activity launches: events that issue a `startActivity()` call at random intervals.",
    "10": "Flip events.",
    "11": "Other events: all other types of events, such as keypresses, other less-used buttons on the device, and so forth."
}

"""
Timeout value, in milliseconds, of each monkey test.
If a monkey test last longer than this value, the 
framework will force it to stop.
"""
cs_monkey_timeout = 300  # 5 minutes

# Alternative: use pre-defined sequence of events for each
# test to be injected through `adb shell input `

"""
Pre-defined sequence of events.
"""
_events_1 = ["swipe 470 965 990 1749 1223", "swipe 470 965 990 1749 1223", "tap 113 216", "tap 113 216",
             "swipe 832 1074 832 1074 161", "swipe 470 965 990 1749 1223", "swipe 470 965 990 1749 1223",
             "swipe 832 1074 832 1074 161", "tap 113 216", "tap 50 1156", "tap 242 1636", "tap 242 1636",
             "swipe 832 1074 832 1074 161", "tap 242 1636", "tap 113 216", "tap 242 1636",
             "swipe 832 1074 832 1074 161", "tap 113 216", "tap 113 216", "swipe 832 1074 832 1074 161",
             "swipe 470 965 990 1749 1223", "swipe 101 985 676 273 951", "tap 50 1156", "swipe 101 985 676 273 951",
             "swipe 101 985 676 273 951"]
_events_2 = ["tap 283 605", "tap 1062 1309", "swipe 248 1526 248 1526 1307", "tap 283 605",
             "swipe 275 1517 419 939 219", "swipe 275 1517 419 939 219", "swipe 248 1526 248 1526 1307",
             "tap 1062 1309", "tap 1062 1309", "tap 329 1058", "tap 329 1058", "swipe 248 1526 248 1526 1307",
             "tap 1062 1309", "tap 283 605", "tap 329 1058", "tap 283 605", "tap 329 1058", "tap 329 1058",
             "swipe 248 1526 248 1526 1307", "swipe 248 1526 248 1526 1307", "swipe 248 1526 248 1526 1307",
             "tap 1062 1309", "tap 1062 1309", "swipe 701 759 886 1499 618", "swipe 275 1517 419 939 219"]
_events_3 = ["swipe 407 1232 204 1452 508", "tap 756 80", "tap 864 1581", "swipe 325 1703 48 125 237",
             "swipe 325 1703 48 125 237", "tap 864 1581", "tap 756 80", "tap 756 80", "swipe 325 1703 48 125 237",
             "tap 1066 132", "swipe 407 1232 204 1452 508", "swipe 429 498 429 498 653", "swipe 325 1703 48 125 237",
             "swipe 325 1703 48 125 237", "tap 864 1581", "tap 1066 132", "swipe 407 1232 204 1452 508",
             "swipe 429 498 429 498 653", "tap 864 1581", "tap 864 1581", "swipe 429 498 429 498 653", "tap 1066 132",
             "swipe 407 1232 204 1452 508", "tap 1066 132", "swipe 407 1232 204 1452 508"]
_events_4 = ["tap 418 581", "swipe 306 1225 694 540 490", "swipe 306 1225 694 540 490", "tap 418 581", "tap 29 149",
             "swipe 385 757 385 757 1097", "tap 29 149", "swipe 385 757 385 757 1097", "tap 29 149", "tap 418 581",
             "swipe 133 194 277 1184 853", "tap 418 581", "swipe 385 757 385 757 1097", "tap 29 149", "tap 773 1325",
             "tap 773 1325", "swipe 306 1225 694 540 490", "tap 29 149", "swipe 385 757 385 757 1097", "tap 418 581",
             "swipe 306 1225 694 540 490", "swipe 385 757 385 757 1097", "swipe 306 1225 694 540 490", "tap 418 581",
             "swipe 133 194 277 1184 853"]
_events_5 = ["swipe 226 1441 553 255 167", "swipe 10 1031 567 1412 1017", "tap 658 1374", "swipe 10 1031 567 1412 1017",
             "tap 658 1374", "tap 658 1374", "tap 658 1374", "swipe 226 1441 553 255 167", "tap 658 1374",
             "tap 658 1374", "swipe 964 1593 964 1593 730", "tap 391 1103", "tap 658 1374",
             "swipe 964 1593 964 1593 730", "tap 423 1735", "swipe 964 1593 964 1593 730", "tap 658 1374",
             "swipe 10 1031 567 1412 1017", "tap 423 1735", "swipe 964 1593 964 1593 730", "tap 391 1103",
             "swipe 226 1441 553 255 167", "swipe 226 1441 553 255 167", "tap 423 1735", "swipe 10 1031 567 1412 1017"]
_events_6 = ["tap 476 1404", "swipe 718 1206 599 438 780", "tap 12 236", "swipe 547 319 275 732 159",
             "swipe 547 319 275 732 159", "tap 476 1404", "swipe 718 1206 599 438 780", "tap 476 1404",
             "swipe 718 1206 599 438 780", "tap 476 1404", "tap 476 1404", "swipe 547 319 275 732 159", "tap 150 94",
             "swipe 7 825 7 825 856", "swipe 547 319 275 732 159", "swipe 718 1206 599 438 780", "tap 12 236",
             "swipe 718 1206 599 438 780", "swipe 7 825 7 825 856", "swipe 547 319 275 732 159", "tap 476 1404",
             "tap 150 94", "swipe 547 319 275 732 159", "tap 150 94", "swipe 7 825 7 825 856"]
_events_7 = ["swipe 494 1158 818 773 1369", "swipe 1017 1606 195 1543 1199", "swipe 870 395 870 395 1168",
             "swipe 1017 1606 195 1543 1199", "tap 708 1138", "tap 708 1138", "tap 751 1221",
             "swipe 494 1158 818 773 1369", "tap 751 1221", "swipe 870 395 870 395 1168",
             "swipe 1017 1606 195 1543 1199", "swipe 870 395 870 395 1168", "tap 708 1138", "tap 751 1221",
             "tap 751 1221", "tap 751 1221", "tap 1071 1191", "tap 1071 1191", "tap 708 1138",
             "swipe 870 395 870 395 1168", "swipe 494 1158 818 773 1369", "tap 1071 1191",
             "swipe 494 1158 818 773 1369", "tap 1071 1191", "swipe 870 395 870 395 1168"]
_events_8 = ["swipe 720 260 921 1208 1181", "swipe 720 260 921 1208 1181", "tap 313 258", "tap 412 618", "tap 412 618",
             "tap 313 258", "tap 489 1273", "tap 313 258", "swipe 720 260 921 1208 1181", "tap 489 1273",
             "swipe 720 260 921 1208 1181", "swipe 813 1191 813 1191 534", "tap 313 258", "swipe 813 1191 813 1191 534",
             "tap 412 618", "tap 412 618", "swipe 720 260 921 1208 1181", "tap 489 1273", "swipe 813 1191 813 1191 534",
             "tap 489 1273", "tap 412 618", "swipe 720 260 921 1208 1181", "tap 313 258", "swipe 155 957 138 1265 1163",
             "swipe 813 1191 813 1191 534"]
_events_9 = ["swipe 376 721 499 1108 411", "swipe 376 721 499 1108 411", "tap 454 1769", "tap 1012 559", "tap 1012 559",
             "swipe 376 721 499 1108 411", "swipe 1016 484 1016 484 1043", "tap 591 1611", "swipe 376 721 499 1108 411",
             "tap 454 1769", "tap 454 1769", "tap 591 1611", "tap 591 1611", "tap 591 1611",
             "swipe 152 490 305 448 915", "tap 1012 559", "swipe 152 490 305 448 915", "swipe 376 721 499 1108 411",
             "swipe 376 721 499 1108 411", "tap 1012 559", "tap 454 1769", "swipe 1016 484 1016 484 1043",
             "swipe 152 490 305 448 915", "swipe 376 721 499 1108 411", "tap 591 1611"]
_events_10 = ["swipe 886 1059 368 1393 1491", "tap 121 880", "tap 901 597", "tap 263 317", "tap 901 597", "tap 901 597",
              "swipe 529 1078 529 1078 199", "swipe 529 1078 529 1078 199", "tap 121 880", "tap 121 880", "tap 901 597",
              "swipe 1051 830 391 83 385", "tap 901 597", "tap 121 880", "tap 263 317", "swipe 1051 830 391 83 385",
              "tap 901 597", "tap 901 597", "tap 901 597", "swipe 1051 830 391 83 385", "tap 263 317", "tap 121 880",
              "tap 121 880", "tap 263 317", "tap 263 317"]
_events_11 = ["swipe 445 1155 538 1256 454", "swipe 441 594 441 594 178", "tap 538 1105", "swipe 445 1155 538 1256 454",
              "swipe 445 1155 538 1256 454", "swipe 441 594 441 594 178", "swipe 456 1524 185 464 755",
              "swipe 441 594 441 594 178", "swipe 441 594 441 594 178", "tap 770 662", "swipe 445 1155 538 1256 454",
              "tap 538 1105", "swipe 445 1155 538 1256 454", "tap 770 662", "swipe 441 594 441 594 178",
              "swipe 445 1155 538 1256 454", "tap 538 1105", "tap 69 1323", "swipe 445 1155 538 1256 454",
              "swipe 441 594 441 594 178", "tap 538 1105", "tap 538 1105", "swipe 441 594 441 594 178",
              "swipe 441 594 441 594 178", "swipe 441 594 441 594 178"]
_events_12 = ["tap 236 676", "swipe 702 586 702 586 496", "tap 286 610", "tap 236 676", "tap 365 153",
              "swipe 702 586 702 586 496", "swipe 702 586 702 586 496", "tap 236 676", "tap 365 153", "tap 286 610",
              "tap 365 153", "tap 236 676", "tap 286 610", "tap 236 676", "tap 286 610", "swipe 702 586 702 586 496",
              "tap 286 610", "tap 286 610", "tap 365 153", "swipe 422 1139 242 1145 646", "swipe 422 1139 242 1145 646",
              "swipe 702 586 702 586 496", "tap 365 153", "swipe 702 586 702 586 496", "swipe 702 586 702 586 496"]
_events_13 = ["swipe 302 1115 428 743 922", "tap 412 1552", "swipe 430 728 893 1177 402", "swipe 430 728 893 1177 402",
              "tap 412 1552", "swipe 302 1115 428 743 922", "swipe 430 728 893 1177 402", "tap 267 1465",
              "swipe 302 1115 428 743 922", "swipe 430 728 893 1177 402", "swipe 757 970 757 970 326",
              "swipe 757 970 757 970 326", "tap 412 1552", "swipe 757 970 757 970 326", "swipe 302 1115 428 743 922",
              "swipe 302 1115 428 743 922", "tap 267 1465", "tap 412 1552", "tap 27 1611", "swipe 430 728 893 1177 402",
              "swipe 302 1115 428 743 922", "tap 412 1552", "tap 412 1552", "tap 27 1611", "swipe 302 1115 428 743 922"]
_events_14 = ["tap 558 1567", "tap 558 1567", "swipe 844 418 305 1108 689", "tap 427 1077", "tap 558 1567",
              "swipe 487 1507 90 1121 1392", "swipe 487 1507 90 1121 1392", "tap 427 1077",
              "swipe 487 1507 90 1121 1392", "tap 465 1227", "tap 465 1227", "swipe 487 1507 90 1121 1392",
              "tap 427 1077", "tap 465 1227", "tap 465 1227", "swipe 369 1763 369 1763 236", "tap 427 1077",
              "tap 427 1077", "swipe 844 418 305 1108 689", "tap 558 1567", "swipe 844 418 305 1108 689",
              "swipe 844 418 305 1108 689", "tap 465 1227", "tap 427 1077", "tap 558 1567"]
_events_15 = ["tap 553 960", "tap 1048 1617", "swipe 156 774 211 1274 731", "swipe 156 774 211 1274 731",
              "swipe 473 1015 473 1015 163", "tap 553 960", "tap 872 539", "tap 1048 1617", "tap 1048 1617",
              "tap 1048 1617", "swipe 473 1015 473 1015 163", "swipe 156 774 211 1274 731",
              "swipe 473 1015 473 1015 163", "tap 553 960", "tap 872 539", "tap 1048 1617",
              "swipe 156 774 211 1274 731", "swipe 29 339 713 1350 1121", "tap 872 539", "tap 872 539", "tap 553 960",
              "tap 553 960", "tap 1048 1617", "swipe 473 1015 473 1015 163", "tap 872 539"]
_events_16 = ["swipe 40 1534 1072 431 1167", "swipe 1042 996 1042 996 313", "swipe 1042 996 1042 996 313",
              "tap 451 1179", "swipe 40 1534 1072 431 1167", "swipe 902 82 412 962 1455", "tap 585 674", "tap 585 674",
              "tap 220 899", "swipe 40 1534 1072 431 1167", "swipe 40 1534 1072 431 1167",
              "swipe 1042 996 1042 996 313", "swipe 1042 996 1042 996 313", "swipe 1042 996 1042 996 313",
              "swipe 902 82 412 962 1455", "swipe 902 82 412 962 1455", "tap 585 674", "swipe 1042 996 1042 996 313",
              "tap 451 1179", "swipe 1042 996 1042 996 313", "swipe 902 82 412 962 1455", "tap 451 1179",
              "swipe 1042 996 1042 996 313", "tap 585 674", "tap 220 899"]
_events_17 = ["tap 847 492", "swipe 672 787 707 1449 768", "tap 1027 374", "swipe 863 1292 863 1292 106",
              "swipe 863 1292 863 1292 106", "tap 804 1715", "tap 804 1715", "tap 847 492",
              "swipe 863 1292 863 1292 106", "tap 1027 374", "tap 804 1715", "tap 847 492", "tap 847 492",
              "swipe 872 176 196 265 1005", "swipe 872 176 196 265 1005", "tap 847 492", "swipe 872 176 196 265 1005",
              "tap 847 492", "tap 804 1715", "tap 847 492", "tap 1027 374", "tap 1027 374", "tap 1027 374",
              "swipe 872 176 196 265 1005", "tap 1027 374"]
_events_18 = ["swipe 599 850 1007 1235 1124", "swipe 1055 928 941 798 529", "swipe 1055 928 941 798 529",
              "swipe 483 627 483 627 551", "tap 588 1485", "tap 588 1485", "swipe 483 627 483 627 551",
              "swipe 1055 928 941 798 529", "tap 234 1058", "tap 588 1485", "swipe 483 627 483 627 551",
              "swipe 599 850 1007 1235 1124", "swipe 599 850 1007 1235 1124", "swipe 483 627 483 627 551",
              "swipe 599 850 1007 1235 1124", "swipe 483 627 483 627 551", "swipe 1055 928 941 798 529", "tap 588 1485",
              "swipe 599 850 1007 1235 1124", "tap 588 1485", "tap 588 1485", "swipe 599 850 1007 1235 1124",
              "tap 234 1058", "swipe 1055 928 941 798 529", "swipe 599 850 1007 1235 1124"]
_events_19 = ["tap 717 1029", "tap 303 1677", "swipe 1070 1438 399 687 731", "swipe 448 1630 187 1377 719",
              "swipe 1070 1438 399 687 731", "swipe 637 308 637 308 429", "tap 303 1677", "swipe 1070 1438 399 687 731",
              "swipe 448 1630 187 1377 719", "swipe 1070 1438 399 687 731", "swipe 637 308 637 308 429", "tap 717 1029",
              "tap 166 819", "swipe 1070 1438 399 687 731", "swipe 637 308 637 308 429", "tap 717 1029",
              "swipe 448 1630 187 1377 719", "tap 166 819", "tap 303 1677", "swipe 448 1630 187 1377 719",
              "tap 166 819", "tap 717 1029", "swipe 1070 1438 399 687 731", "tap 166 819",
              "swipe 448 1630 187 1377 719"]
_events_20 = ["tap 190 652", "swipe 1017 564 721 309 576", "swipe 499 267 499 267 425", "swipe 499 267 499 267 425",
              "tap 146 159", "swipe 1017 564 721 309 576", "swipe 1017 564 721 309 576", "tap 190 652",
              "swipe 499 267 499 267 425", "tap 504 1020", "swipe 78 431 631 1591 1414", "tap 146 159", "tap 504 1020",
              "tap 504 1020", "swipe 1017 564 721 309 576", "swipe 1017 564 721 309 576", "swipe 499 267 499 267 425",
              "swipe 78 431 631 1591 1414", "swipe 499 267 499 267 425", "tap 504 1020", "tap 146 159", "tap 146 159",
              "swipe 1017 564 721 309 576", "swipe 1017 564 721 309 576", "tap 146 159"]
_events_21 = ["swipe 683 1690 111 1026 1263", "tap 365 275", "tap 112 1592", "tap 112 1592", "tap 365 275",
              "swipe 683 1690 111 1026 1263", "swipe 697 1158 1040 1608 178", "swipe 683 1690 111 1026 1263",
              "swipe 888 1154 888 1154 128", "tap 173 1280", "tap 112 1592", "tap 112 1592", "tap 365 275",
              "swipe 683 1690 111 1026 1263", "swipe 697 1158 1040 1608 178", "tap 365 275",
              "swipe 683 1690 111 1026 1263", "tap 365 275", "tap 365 275", "swipe 683 1690 111 1026 1263",
              "tap 173 1280", "swipe 888 1154 888 1154 128", "swipe 697 1158 1040 1608 178", "tap 173 1280",
              "tap 112 1592"]
_events_22 = ["swipe 731 978 179 1483 220", "tap 1057 211", "swipe 51 1181 847 1397 911", "swipe 51 1181 847 1397 911",
              "tap 50 1150", "swipe 51 1181 847 1397 911", "swipe 731 978 179 1483 220", "tap 50 1150", "tap 50 1150",
              "tap 50 1150", "swipe 478 806 478 806 142", "tap 50 1150", "swipe 478 806 478 806 142", "tap 1057 211",
              "swipe 478 806 478 806 142", "swipe 51 1181 847 1397 911", "swipe 478 806 478 806 142", "tap 1057 211",
              "swipe 478 806 478 806 142", "swipe 731 978 179 1483 220", "tap 50 1150", "swipe 51 1181 847 1397 911",
              "swipe 731 978 179 1483 220", "tap 1057 211", "swipe 731 978 179 1483 220"]
_events_23 = ["tap 722 1184", "tap 285 1624", "swipe 1025 487 1025 487 386", "swipe 241 606 549 1380 740",
              "tap 722 1184", "tap 722 1184", "tap 285 1624", "swipe 965 1740 504 514 619",
              "swipe 241 606 549 1380 740", "swipe 241 606 549 1380 740", "swipe 1025 487 1025 487 386",
              "swipe 1025 487 1025 487 386", "tap 285 1624", "swipe 241 606 549 1380 740", "swipe 241 606 549 1380 740",
              "swipe 1025 487 1025 487 386", "swipe 965 1740 504 514 619", "tap 85 906", "tap 722 1184", "tap 722 1184",
              "swipe 965 1740 504 514 619", "swipe 241 606 549 1380 740", "swipe 241 606 549 1380 740", "tap 722 1184",
              "swipe 241 606 549 1380 740"]
_events_24 = ["tap 115 1766", "tap 115 1766", "tap 115 1766", "swipe 367 806 367 806 904", "tap 115 1766",
              "swipe 275 1501 970 544 1002", "swipe 948 561 142 1547 890", "swipe 275 1501 970 544 1002",
              "swipe 275 1501 970 544 1002", "swipe 367 806 367 806 904", "tap 115 1766", "tap 115 1766",
              "tap 115 1766", "tap 459 259", "swipe 367 806 367 806 904", "swipe 275 1501 970 544 1002", "tap 459 259",
              "tap 115 1766", "tap 115 1766", "tap 220 186", "swipe 367 806 367 806 904", "swipe 275 1501 970 544 1002",
              "tap 459 259", "tap 220 186", "swipe 948 561 142 1547 890"]
_events_25 = ["tap 715 1314", "tap 333 1030", "tap 333 1030", "swipe 489 133 840 963 950", "tap 715 1314",
              "swipe 591 993 1018 627 648", "tap 669 395", "tap 333 1030", "swipe 489 133 840 963 950", "tap 333 1030",
              "swipe 489 133 840 963 950", "tap 333 1030", "swipe 987 1401 987 1401 1138", "swipe 489 133 840 963 950",
              "swipe 591 993 1018 627 648", "swipe 987 1401 987 1401 1138", "tap 715 1314", "tap 669 395",
              "tap 333 1030", "tap 333 1030", "swipe 591 993 1018 627 648", "swipe 987 1401 987 1401 1138",
              "tap 333 1030", "tap 333 1030", "tap 333 1030"]

"""
Mapping between monkey seeds and respective pre-defined 
sequence of events.
"""
cs_monkey_seeds_events = {
    1: _events_1,
    2: _events_2,
    3: _events_3,
    4: _events_4,
    5: _events_5,
    6: _events_6,
    7: _events_7,
    8: _events_8,
    9: _events_9,
    10: _events_10,
    11: _events_11,
    12: _events_12,
    13: _events_13,
    14: _events_14,
    15: _events_15,
    16: _events_16,
    17: _events_17,
    18: _events_18,
    19: _events_19,
    20: _events_20,
    21: _events_21,
    22: _events_22,
    23: _events_23,
    24: _events_24,
    25: _events_25
}
