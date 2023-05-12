# -*- coding: utf-8 -*-

import pdb
import requests
import time
from enum import Enum


class SmsCountryId(Enum):
    """
    SmsCountryId [summary] 
    日本語からsmshubの国識別番号にコンバート

    Args:
        enum (str): 国の名前
    """
    ロシア = 0
    ウクライナ = 1
    カザフスタン = 2
    中国 = 3
    フィリピン = 4
    ミャンマー = 5
    インドネシア = 6
    マレーシア = 7
    ケニア = 8
    タンザニア = 9
    ベトナム = 10
    キルギスタン = 11
    アメリカ = 12
    イスラエル = 13
    香港 = 14
    ポーランド = 15
    イングランド = 16
    イギリス = 16
    ナイジェリア = 19
    エジプト = 21
    インド = 22
    アイルランド = 23
    カンボジア = 24
    ラオス = 25
    ハイチ = 26
    象牙 = 27
    ガンビア = 28
    セルビア = 29
    イエメン = 30
    南アフリカ = 31
    ルーマニア = 32
    コロンビア = 33
    エストニア = 34
    カナダ = 36
    モロッコ = 37
    ガーナ = 38
    アルゼンチン = 39
    ウズベキスタン = 40
    カメルーン = 41
    チャド = 42
    ドイツ = 43
    リトアニア = 44
    クロアチア = 45
    スウェーデン = 46
    イラク = 47
    オランダ = 48
    ラトビア = 49
    オーストリア = 50
    ベラルーシ = 51
    タイ = 52
    サウジアラビア = 53
    メキシコ = 54
    台湾 = 55
    スペイン = 56
    イラン = 57
    アルジェリア = 58
    バングラデシュ = 60
    セネガル = 61
    七面鳥 = 62
    チェコ = 63
    スリランカ = 64
    ペルー = 65
    パキスタン = 66
    ニュージーランド = 67
    ギニア = 68
    マリ = 69
    ベネズエラ = 70
    モンゴル = 72
    ブラジル = 73
    アフガニスタン = 74
    ウガンダ = 75
    アンゴラ = 76
    キプロス = 77
    フランス = 78
    パプア = 79
    モザンビーク = 80
    ネパール = 81
    モルドバ = 85
    パラグアイ = 87
    ホンジュラス = 88
    チュニジア = 89
    ニカラグア = 90
    ボリビア = 92
    グアテマラ = 94
    アラブ首長国連邦 = 95
    ジンバブエ = 96
    スーダン = 98
    サルバドール = 101
    リビア = 102
    ジャマイカ = 103
    トリニダード = 104
    エクアドル = 105
    ドミニカ = 109
    モーリタニア = 114
    シエラレオネ = 115
    ヨルダン = 116
    ポルトガル = 117
    ベニン = 120
    ブルネイ = 121
    ボツワナ = 123
    ジョージア = 128
    ギリシャ = 129
    ガイアナ = 131
    リベリア = 135
    スリナム = 142
    タジキスタン = 143
    再会 = 146
    アルメニア = 148
    コンゴ = 150
    ブルキナファソ = 152
    レバノン = 153
    ガボン = 154
    モーリシャス = 157
    ブータン = 158
    モルディブ = 159
    トルクメニスタン = 161
    アルバ = 179
    日本 = 182
    フィジー = 189
    韓国 = 190
    バミューダ = 195


class SmsServiceId(Enum):
    """
    SmsServiceId [summary] 
    サービス名からsmshubのサービス識別番号にコンバート

    Args:
        enum (str): サービス名
    """
    WHATSAPP = "wa"
    VIBER = "vi"
    TELEGRAM = "tg"
    WECHAT = "wb"
    GOOGLE = "go"
    AVITO = "av"
    FACEBOOK = "fb"
    TWITTER = "tw"
    UBER = "ub"
    GETT = "gt"
    OLX = "sn"
    INSTAGRAM = "ig"
    HEZZL = "ss"
    MAILRU = "ma"
    MICROSOFT = "mm"
    AIRBNB = "uk"
    LINE = "me"
    YAHOO = "mb"
    HQ = "kp"
    DELIVERY = "dt"
    STEAM = "mt"
    TINDER = "oi"
    MAMBA = "fd"
    DENT = "zz"
    KAKAOTALK = "kt"
    AOL = "pm"
    LINKEDIN = "tn"
    NAVER = "nv"
    NETFLIX = "nf"
    ICQ = "iq"
    ONLINERBY = "ob"
    KUFARBY = "kb"
    IMO = "im"
    MICHAT = "mc"
    DISCORD = "ds"
    SEOSPRINT = "vv"
    MONOBANK = "ji"
    UKRNET = "hu"
    SKOUT = "wg"
    EASYPAY = "rz"
    WOLT = "rr"
    CLIQQ = "fe"
    SSOIDNET = "la"
    ZOHO = "zh"
    TICKETMASTER = "gp"
    AMAZON = "am"
    OLACABS = "ly"
    RAMBLER = "tc"
    PROTONMAIL = "dp"
    CITYMOBIL = "yf"
    MIRATORG = "op"
    PGBONUS = "fx"
    MEGA = "qr"
    CAREEM = "ls"
    MYMUSICTASTE = "mu"
    SNAPCHAT = "fu"
    KEYBASE = "bf"
    OZON = "sg"
    WILDBERRIES = "uu"
    BLABLACAR = "ua"
    ALIBABA = "ab"
    INBOXLV = "iv"
    NTTGAME = "zy"
    SURVEYTIME = "gd"
    MYLOVE = "fy"
    MOSRU = "ce"
    TRUECALLER = "tl"
    GLOBUS = "hm"
    BOLT = "tx"
    SHOPEE = "ka"
    PROM = "cm"
    ALIPAY = "hw"
    KARUSEL = "de"
    IVI = "jc"
    INDRIVER = "rl"
    HAPPN = "df"
    RUTUBE = "ui"
    MAGNOLIA = "up"
    FOODPANDA = "nz"
    WEIBO = "kf"
    BILLMILL = "ri"
    QUIPP = "cc"
    OKTA = "lr"
    JDCOM = "za"
    FIQSY = "ug"
    KUCOINPLAY = "sq"
    PAPARA = "zr"
    WISH = "xv"
    ICRYPEX = "cx"
    PADDYPOWER = "cw"
    BAIDU = "li"
    PAYCELL = "xz"
    LENTA = "rd"
    PAYBERRY = "qb"
    DROM = "hz"
    GLOBALTEL = "gl"
    DELIVEROO = "zk"
    SOCIOS = "ia"
    WMARACI = "xl"
    YEMEKSEPETI = "yi"
    NIKE = "ew"
    MYGLO = "ae"
    YOUSTAR = "gb"
    ROSAKHUTOR = "qm"
    EBAY = "dh"
    GG = "qe"
    GRINDR = "yw"
    OFFGAMERS = "uz"
    HEPSIBURADACOM = "gx"
    COINBASE = "re"
    DBRUA = "tj"
    PAYPAL = "ts"
    HILY = "rt"
    SNEAKERSNSTUFF = "sf"
    DOSTAVISTA = "sv"
    BLIZZARD = "bz"
    EZBUY = "db"
    COINFIELD = "vw"
    AIRTEL = "zl"
    YANDEXGO = "wf"
    MRGREEN = "lw"
    REDIFFMAIL = "co"
    MILOAN = "ey"
    PAYTM = "ge"
    DHANI = "os"
    CMTCUZDAN = "ql"
    MERCADO = "cq"
    DIDI = "xk"
    MONESE = "py"
    KOTAK811 = "rv"
    HOPI = "jl"
    TRENDYOL = "pr"
    JUSTDATING = "pu"
    PAIRS = "dk"
    TOUCHANCE = "fm"
    SNAPPFOOD = "ph"
    NCSOFT = "sw"
    TOSLA = "nr"
    ININAL = "hy"
    PAYSEND = "tr"
    CDKEYS = "pq"
    AVON = "ff"
    DODOPIZZA = "sd"
    MCDONALDS = "ry"
    JKF = "hr"
    MYFISHKA = "qa"
    CRAIGSLIST = "wc"
    FOODY = "kw"
    GRAB = "jg"
    ZALO = "mj"
    LIVESCORE = "eu"
    GAMER = "ed"
    HUYA = "pp"
    WESTSTEIN = "th"
    TANGO = "xr"
    GLOBAL24 = "iz"
    SHEERID = "rx"
    CAIXA = "my"
    OFFERUP = "zm"
    SWVL = "tq"
    HARAJ = "au"
    TAKSHEEL = "ei"
    HAMRAHAVAL = "rp"
    GAMEKIT = "pa"
    GETIR = "ul"
    IRANCELL = "cf"
    ALFA = "bt"
    AGROINFORM = "qu"
    HUMBLEBUNDLE = "un"
    FABERLIC = "rm"
    CAFEBAZAAR = "uo"
    CRYPTOCOM = "ti"
    GITTIGIDIYOR = "nk"
    MZADQATAR = "jm"
    ALGIDA = "lp"
    BITAQATY = "pt"
    AMASIA = "yo"
    DREAM11 = "ve"
    ORIFLAME = "qh"
    BYKEA = "iu"
    IMMOWELT = "ib"
    DIGIKALA = "zv"
    YAAY = "vn"
    GAMEARENA = "wn"
    AUCHAN = "st"
    PICPAY = "ev"
    BLUED = "qn"
    SPOTHIT = "cd"
    BRAND20UA = "vo"
    IQOS = "il"
    POWERKREDITE = "dx"
    BISU = "el"
    PAXFUL = "dn"
    PUREPLATFROM = "lk"
    BANQI = "vc"
    MOBILE01 = "wk"
    AITU = "jj"
    ADIDAS = "an"
    HUMTA = "gv"
    DIVAR = "dw"
    CAROUSELL = "gj"
    MOMO = "hc"
    ENEBA = "uf"
    VERSE = "kn"
    TAOBAO = "qd"
    ONTAXI = "zf"
    HOTLINE = "gi"
    TATNEFT = "uc"
    RRSA = "mn"
    DOUYU = "ak"
    UKLON = "cp"
    MONEYLION = "qo"
    APPLE = "wx"
    CLUBHOUSE = "et"
    NIFTY = "px"
    PINGPONG = "jh"
    BITCLOUT = "lt"
    SKROUTZ = "sk"
    MAPLESEA = "oh"
    ROZETKA = "km"
    GALAXYWIN = "af"
    YUBO = "uh"
    IQIYI = "es"
    GOODS = "be"
    GLOVO = "aq"
    IFOOD = "pd"
    QUACK = "zw"
    MOCOSPACE = "gm"
    DUNDLE = "fi"
    SWITIPS = "hg"
    FACEIT = "qz"
    LYKA = "gz"
    PAYSAFECARD = "jq"
    ONET = "ue"
    LIGHTCHAT = "xf"
    GOFUNDME = "bp"
    META = "vy"
    JAMESDELIVERY = "ea"
    SHELLBOX = "vg"
    REDBOOK = "qf"
    TRIP = "nq"
    BIP = "ww"
    WHOOSH = "qj"
    KAZANEXPRESS = "ol"
    AKULAKU = "tm"
    KEYPAY = "ra"
    BETFAIR = "vd"
    GOJEK = "ni"
    FASTMAIL = "mr"
    ALIEXPRESS = "hx"
    METRO = "bv"
    HANDYPICK = "sj"
    CHAINGEFINANCE = "td"
    IWPLAY = "dm"
    GROUPME = "xs"
    NIMOTV = "kz"
    STRIPE = "nu"
    EYECON = "kr"
    LIDL = "pz"
    TWITCH = "hb"
    GALAXYCHAT = "xe"
    ITI = "ad"
    SETEL = "zg"
    REVOLUT = "ij"
    HERMES = "en"
    KAGGLE = "zo"
    HEYBOX = "vx"
    BAND = "hl"
    POTATO = "lq"
    ROPOSO = "ga"
    WISE = "bo"
    KFC = "fz"
    OKCUPID = "vm"
    POCKET52 = "ch"
    PAYZAPP = "yp"
    AGRIDEVELOP = "cs"
    COURSEHERO = "yg"
    SANTANDER = "lj"
    POSHMARK = "oz"
    TANTAN = "wh"
    IZI = "wt"
    OKKO = "og"
    MPL = "xq"
    OVO = "xh"
    VINTED = "kc"
    SIZEER = "eo"


class CountryTelCode(Enum):
    """
    CountryTelCode [summary] 
    国名から電話の国番号

    Args:
        enum (str): 国の名前
    """
    アフガニスタン = 93
    バーレーン = 973
    バングラデシュ = 880
    ブータン = 975
    ブルネイ = 673
    カンボジア = 855
    中国 = 86
    東ティモール = 670
    香港 = 852
    インド = 91
    インドネシア = 62
    イラン = 98
    イラク = 964
    イスラエル = 972
    日本 = 81
    ヨルダン = 962
    北朝鮮 = 850
    韓国 = 82
    クウェート = 965
    ラオス = 856
    レバノン = 961
    マカオ = 853
    マレーシア = 60
    モルディブ = 960
    モンゴル = 976
    ミャンマー = 95
    ネパール = 977
    オマーン = 968
    パキスタン = 92
    フィリピン = 63
    カタール = 974
    サウジアラビア = 966
    シンガポール = 65
    スリランカ = 94
    シリア = 963
    台湾 = 886
    タイ = 66
    アラブ首長国連邦 = 971
    べトナム = 84
    イエメン = 967
    アメリカ領サモア = 1
    オーストラリア = 61
    クリスマス島 = 61
    ココス諸島 = 61
    クック諸島 = 682
    フィジー = 679
    フランス領ポリネシア = 689
    グアム = 1
    ハワイ = 1
    キリバス = 686
    マーシャル諸島 = 692
    ミクロネシア連邦 = 691
    ナウル = 674
    ニューカレドニア = 687
    ニュージーランド = 64
    ニウエ = 683
    ノーフォーク島 = 672
    パラオ = 680
    パプアニューギニア = 675
    サイパン = 1
    サモア = 685
    ソロモン諸島 = 677
    トケラウ諸島 = 690
    トンガ = 676
    ツバル = 688
    バヌアツ = 678
    ウェーク島 = 1
    アラスカ = 1
    米領バージン諸島 = 1
    アンギラ = 1
    アンティグアバーブーダ = 1
    アルゼンチン = 54
    アルバ = 297
    バハマ = 1
    バルバドス = 1
    ベリーズ = 501
    バミューダ諸島 = 1
    ボリビア = 591
    ブラジル = 55
    英領バージン諸島 = 1
    カナダ = 1
    ケイマン諸島 = 1
    チリ = 56
    コロンビア = 57
    コスタリカ = 506
    キューバ = 53
    ドミニカ国 = 1
    ドミニカ共和国 = 1
    エクアドル = 593
    エルサルバドル = 503
    フォークランド諸島 = 500
    フランス領ギアナ = 594
    グレナダ = 1
    グアドループ島 = 590
    グアテマラ = 502
    ガイアナ = 592
    ハイチ = 509
    ホンジュラス = 504
    ジャマイカ = 1
    マルチニーク島 = 596
    メキシコ = 52
    モンセラット = 1
    オランダ領セントマーティン = 1-721
    オランダ領アンティール = 599
    ニカラグア = 505
    パナマ = 507
    パラグアイ = 595
    ペルー = 51
    プエルトリコ = 1
    セントクリストファーネイビス = 1
    セントルシア = 1
    サンピエール島ミクロン島 = 508
    セントビンセントおよびグレナディーン諸島 = 1
    スリナム = 597
    トリニダードトバゴ = 1
    タークス諸島カイコス諸島 = 1
    アメリカ = 1
    ウルグアイ = 598
    ベネズエラ = 58
    アルバニア = 355
    アンドラ = 376
    アルメニア = 374
    オーストリア = 43
    アゼルバイジャン = 994
    アゾレス諸島 = 351
    ベラルーシ = 375
    ベルギー = 32
    ボスニアヘルツェゴビナ = 387
    ブルガリア = 359
    クロアチア = 385
    キプロス = 357
    チェコ = 420
    デンマーク = 45
    エストニア = 372
    フェロー諸島 = 298
    フィンランド = 358
    フランス = 33
    ジョージア = 995
    ドイツ = 49
    ジブラルタル = 350
    ギリシア = 30
    グリーンランド = 299
    ハンガリー = 36
    アイスランド = 354
    アイルランド = 353
    イタリア = 39
    バチカン = 39
    カザフスタン = 7
    キルギス = 996
    ラトビア = 371
    リヒテンシュタイン = 423
    リトアニア = 370
    ルクセンブルグ = 352
    マケドニア共和国 = 389
    マルタ = 356
    モルドバ = 373
    モナコ = 377
    モンテネグロ = 382
    オランダ = 31
    ノルウェー = 47
    ポーランド = 48
    ポルトガル = 351
    ルーマニア = 40
    ロシア = 7
    サンマリノ = 378
    セルビア = 381
    スロバキア = 421
    スロベニア = 386
    スペイン = 34
    スウェーデン = 46
    スイス = 41
    タジキスタン = 992
    トルコ = 90
    トルクメニスタン = 993
    イギリス = 44
    ウクライナ = 380
    ウズベキスタン = 998
    アルジェリア = 213
    アンゴラ = 244
    アセンション島 = 247
    ベナン = 229
    ボツワナ = 267
    ブルキナファソ = 226
    ブルンジ = 257
    カメルーン = 237
    カナリア諸島 = 34
    カーボベルデ = 238
    中央アフリカ = 236
    チャド = 235
    コモロ = 269
    コンゴ民主共和国 = 243
    コンゴ = 242
    コートジボワール = 225
    ディェゴガルシア島 = 246
    ジブチ = 253
    エジプト = 20
    赤道ギニア = 240
    エリトリア = 291
    エチオピア = 251
    ガボン = 241
    ガンビア = 220
    ガーナ = 233
    ギニア = 224
    ギニアビサウ = 245
    ケニア = 254
    レソト = 266
    リベリア = 231
    リビア = 218
    マダガスカル = 261
    マディラ諸島 = 351
    マラウイ = 265
    マリ = 223
    モーリタニア = 222
    モーリシャス = 230
    マヨット島 = 262
    モロッコ = 212
    モザンビーク = 258
    ナミビア = 264
    ニジェール = 227
    ナイジェリア = 234
    セーシェル = 248
    レユニオン = 262
    ルワンダ = 250
    サントメプリンシペ = 239
    セネガル = 221
    シエラレオネ = 232
    ソマリア = 252
    南アフリカ = 27
    南スーダン = 211
    スペイン領北アフリカ = 34
    セントヘレナ島 = 290
    スーダン = 249
    スワジランド = 268
    タンザニア = 255
    トーゴ = 228
    チュニジア = 216
    ウガンダ = 256
    ザンビア = 260
    ジンバブエ = 263


class CountryEnglish(Enum):
    """
    CountryEnglish [summary]

    国名を日本語から英語に

    Args:
        enum (str): 国の名前
    """
    アフガニスタン = "Afghanistan"
    バーレーン = "Bahrain"
    バングラデシュ = "Bangladesh"
    ブータン = "Bhutan"
    ブルネイ = "Brunei"
    カンボジア = "Cambodia"
    中国 = "China"
    東ティモール = "East Timor"
    香港 = "Hong Kong"
    インド = "India"
    インドネシア = "Indonesia"
    イラン = "Iran"
    イラク = "Iraq"
    イスラエル = "Israel"
    日本 = "Japan"
    ヨルダン = "Jordan"
    北朝鮮 = "Korea(Demo.)"
    韓国 = "Korea(Rep. of)"
    クウェート = "Kuwait"
    ラオス = "Laos"
    レバノン = "Lebanon"
    マカオ = "Macao"
    マレーシア = "Malaysia"
    モルディブ = "Maldives"
    モンゴル = "Mongolia"
    ミャンマー = "Myanmar"
    ネパール = "Nepal"
    オマーン = "Oman"
    パキスタン = "Pakistan"
    フィリピン = "Philippines"
    カタール = "Qatar"
    サウジアラビア = "Saudi Arabia"
    シンガポール = "Singapore"
    スリランカ = "Sri Lanka"
    シリア = "Syria"
    台湾 = "Taiwan"
    タイ = "Thailand"
    アラブ首長国連邦 = "U.A.E."
    べトナム = "Viet Nam"
    イエメン = "Yemen"
    アメリカ領サモア = "American Samoa"
    オーストラリア = "Australia"
    クリスマス島 = "Christmas Is."
    ココス諸島 = "Cocos Keeling Is."
    クック諸島 = "Cook Islands"
    フィジー = "Fiji"
    フランス領ポリネシア = "French Polynesia"
    グアム = "Guam"
    ハワイ = "Hawaii"
    キリバス = "Kiribati"
    マーシャル諸島 = "Marshall Is."
    ミクロネシア連邦 = "Micronesia"
    ナウル = "Nauru"
    ニューカレドニア = "New Caledonia"
    ニュージーランド = "New Zealand"
    ニウエ = "Niue"
    ノーフォーク島 = "Norfolk Island"
    パラオ = "Palau"
    パプアニューギニア = "Papua New Guinea"
    サイパン = "Saipan"
    サモア = "Samoa"
    ソロモン諸島 = "Solomon Is."
    トケラウ諸島 = "Tokelau Is."
    トンガ = "Tonga"
    ツバル = "Tuvalu"
    バヌアツ = "Vanuatu"
    ウェーク島 = "Wake Is."
    アラスカ = "Alaska"
    米領バージン諸島 = "American Virgin Is."
    アンギラ = "Anguilla"
    アンティグアバーブーダ = "Antigua & Barbuda"
    アルゼンチン = "Argentina"
    アルバ = "Aruba"
    バハマ = "Bahamas"
    バルバドス = "Barbados"
    ベリーズ = "Belize"
    バミューダ諸島 = "Bermuda"
    ボリビア = "Bolivia"
    ブラジル = "Brazil"
    英領バージン諸島 = "British Virgin Is."
    カナダ = "Canada"
    ケイマン諸島 = "Cayman Islands"
    チリ = "Chile"
    コロンビア = "Colombia"
    コスタリカ = "Costa Rica"
    キューバ = "Cuba"
    ドミニカ国 = "Dominica"
    ドミニカ共和国 = "Dominican Rep."
    エクアドル = "Ecuador"
    エルサルバドル = "El Salvador"
    フォークランド諸島 = "Falkland Is."
    フランス領ギアナ = "French Guiana"
    グレナダ = "Grenada"
    グアドループ島 = "Guadeloupe"
    グアテマラ = "Guatemala"
    ガイアナ = "Guyana"
    ハイチ = "Haiti"
    ホンジュラス = "Honduras"
    ジャマイカ = "Jamaica"
    マルチニーク島 = "Martinique"
    メキシコ = "Mexico"
    モンセラット = "Montserrat"
    オランダ領セントマーティン = "NETH St. Maarten"
    オランダ領アンティール = "Netherlands Antilles"
    ニカラグア = "Nicaragua"
    パナマ = "Panama"
    パラグアイ = "Paraguay"
    ペルー = "Peru"
    プエルトリコ = "Puerto Rico"
    セントクリストファーネイビス = "St. Christopher & Nevis"
    セントルシア = "St. Lucia"
    サンピエール島ミクロン島 = "St. Pierre & Miquelo"
    セントビンセントおよびグレナディーン諸島 = "St. Vincent & the Grenadines"
    スリナム = "Suriname"
    トリニダードトバゴ = "Trinidad & Tobago"
    タークス諸島カイコス諸島 = "Turks & Caicos Is."
    アメリカ = "U.S.A."
    ウルグアイ = "Uruguay"
    ベネズエラ = "Venezuela"
    アルバニア = "Albania"
    アンドラ = "Andorra"
    アルメニア = "Armenia"
    オーストリア = "Austria"
    アゼルバイジャン = "Azerbaidjan"
    アゾレス諸島 = "Azores Islands"
    ベラルーシ = "Belarus"
    ベルギー = "Belgium"
    ボスニアヘルツェゴビナ = "Bosnia & Herzegovina"
    ブルガリア = "Bulgaria"
    クロアチア = "Croatia"
    キプロス = "Cyprus"
    チェコ = "Czech"
    デンマーク = "Denmark"
    エストニア = "Estonia"
    フェロー諸島 = "Faroe Islands"
    フィンランド = "Finland"
    フランス = "France"
    ジョージア = "Georgia"
    ドイツ = "Germany"
    ジブラルタル = "Gibraltar"
    ギリシア = "Greece"
    グリーンランド = "Greenland"
    ハンガリー = "Hungary"
    アイスランド = "Iceland"
    アイルランド = "Ireland"
    イタリア = "Italy"
    バチカン = "Italy"
    カザフスタン = "Kazakhstan"
    キルギス = "Kyrgyz Rep."
    ラトビア = "Latvia"
    リヒテンシュタイン = "Liechtenstein"
    リトアニア = "Lithuania"
    ルクセンブルグ = "Luxembourg"
    マケドニア共和国 = "Macedonia"
    マルタ = "Malta"
    モルドバ = "Moldova"
    モナコ = "Monaco"
    モンテネグロ = "Montenegro"
    オランダ = "Netherlands"
    ノルウェー = "Norway"
    ポーランド = "Poland"
    ポルトガル = "Portugal"
    ルーマニア = "Romania"
    ロシア = "Russian Fed."
    サンマリノ = "San Marino"
    セルビア = "Serbia"
    スロバキア = "Slovak"
    スロベニア = "Slovenia"
    スペイン = "Spain"
    スウェーデン = "Sweden"
    スイス = "Switzerland"
    タジキスタン = "Tadzhikistan"
    トルコ = "Turkey"
    トルクメニスタン = "Turkmenistan"
    イギリス = "U.K."
    ウクライナ = "Ukraine"
    ウズベキスタン = "Uzbekistan"
    アルジェリア = "Algeria"
    アンゴラ = "Angola"
    アセンション島 = "Ascension"
    ベナン = "Benin"
    ボツワナ = "Botswana"
    ブルキナファソ = "Burkina Faso"
    ブルンジ = "Burundi"
    カメルーン = "Cameroon"
    カナリア諸島 = "Canary Islands"
    カーボベルデ = "Cape Verde"
    中央アフリカ = "Central Africa"
    チャド = "Chad"
    コモロ = "Comoros"
    コンゴ民主共和国 = "Congo (Demo.)"
    コンゴ = "Congo(Rep. of)"
    コートジボワール = "Cote d'lvoire"
    ディェゴガルシア島 = "Diego Garcia"
    ジブチ = "Djibouti"
    エジプト = "Egypt"
    赤道ギニア = "Equatorial Guinea"
    エリトリア = "Eritrea"
    エチオピア = "Ethiopia"
    ガボン = "Gabon"
    ガンビア = "Gambia"
    ガーナ = "Ghana"
    ギニア = "Guinea"
    ギニアビサウ = "Guinea-Bissau"
    ケニア = "Kenya"
    レソト = "Lesotho"
    リベリア = "Liberia"
    リビア = "Libya"
    マダガスカル = "Madagascar"
    マディラ諸島 = "Madeira"
    マラウイ = "Malawi"
    マリ = "Mali"
    モーリタニア = "Mauritania"
    モーリシャス = "Mauritius"
    マヨット島 = "Mayotte"
    モロッコ = "Morocco"
    モザンビーク = "Mozambique"
    ナミビア = "Namibia"
    ニジェール = "Niger"
    ナイジェリア = "Nigeria"
    セーシェル = "Republic Seychelles"
    レユニオン = "Reunion"
    ルワンダ = "Rwanda"
    サントメプリンシペ = "Sao Tome & Principe"
    セネガル = "Senegal"
    シエラレオネ = "Sierra Leone"
    ソマリア = "Somalia"
    南アフリカ = "South Africa"
    南スーダン = "South Sudan"
    スペイン領北アフリカ = "Spanish North Africa"
    セントヘレナ島 = "St. Helena"
    スーダン = "Sudan"
    スワジランド = "Swaziland"
    タンザニア = "Tanzania"
    トーゴ = "Togo"
    チュニジア = "Tunisia"
    ウガンダ = "Uganda"
    ザンビア = "Zambia"
    ジンバブエ = "Zimbabwe"


class CountryCode(Enum):
    """
    CountryCode [summary]

    国の名前から国コードに

    Args:
        enum (str): 国名
    """
    アフガニスタン = "AF"
    アルバニア = "AL"
    アルジェリア = "DZ"
    米国領サモア = "AS"
    アンドラ = "AD"
    アンゴラ = "AO"
    南極 = "AQ"
    アンティグアバーブーダ = "AG"
    アルゼンチン = "AR"
    アルメニア = "AM"
    アルバ = "AW"
    オーストラリア = "AU"
    オーストリア = "AT"
    アゼルバイジャン = "AZ"
    バハマ = "BS"
    バーレーン = "BH"
    バングラディシュ = "BD"
    バルバドス = "BB"
    べラルーシ = "BY"
    ベルギー = "BE"
    ベリーズ = "BZ"
    ベナン = "BJ"
    バミューダ諸島 = "BM"
    ブータン = "BT"
    ボリビア = "BO"
    ボスニアヘルツェゴビナ = "BA"
    ボツワナ = "BW"
    ブーベ島 = "BV"
    ブラジル = "BR"
    イギリス領インド洋領域 = "IO"
    ブルネイダルサラーム = "BN"
    ブルガリア = "BG"
    ブルキナファソ = "BF"
    ブルンジ = "BI"
    カンボジア = "KH"
    カメルーン = "CM"
    カナダ = "CA"
    カーボベルデ = "CV"
    ケイマン諸島 = "KY"
    中央アフリカ共和国 = "CF"
    チャド = "TD"
    チリ = "CL"
    中国 = "CN"
    クリスマス島 = "CX"
    ココス諸島 = "CC"
    コロンビア = "CO"
    コモロ = "KM"
    コンゴ = "CG"
    コンゴ民主共和国 = "CD"
    クック諸島 = "CK"
    コスタリカ = "CR"
    コートジボアール = "CI"
    クロアチア = "HR"
    キューバ = "CU"
    キプロス = "CY"
    チェコ共和国 = "CZ"
    デンマーク = "DK"
    ジブチ = "DJ"
    ドミニカ = "DM"
    ドミニカ共和国 = "DO"
    エクアドル = "EC"
    エジプト = "EG"
    エルサルバドル = "SV"
    赤道ギニア = "GQ"
    エリトリア = "ER"
    エストニア = "EE"
    エチオピア = "ET"
    フォークランド諸島 = "FK"
    フェロー諸島 = "FO"
    フィジー = "FJ"
    フィンランド = "FI"
    フランス = "FR"
    フランス領ギアナ = "GF"
    フランス領ポリネシア = "PF"
    フランス南方領 = "TF"
    ガボン = "GA"
    ガンビア = "GM"
    グルジア = "GE"
    ドイツ = "DE"
    ガーナ = "GH"
    ジブラルタル = "GI"
    ギリシャ = "GR"
    グリーンランド = "GL"
    グレナダ = "GD"
    グアドループ島 = "GP"
    グアム = "GU"
    グアテマラ = "GT"
    ギニア = "GN"
    ギニアビサウ = "GW"
    ガイアナ = "GY"
    ハイチ = "HT"
    ハード島およびマクドナルド諸島 = "HM"
    ホンジュラス = "HN"
    香港 = "HK"
    ハンガリー = "HU"
    アイスランド = "IS"
    インド = "IN"
    インドネシア = "ID"
    イラン = "IR"
    イラク = "IQ"
    アイルランド = "IE"
    イスラエル = "IL"
    イタリア = "IT"
    ジャマイカ = "JM"
    日本 = "JP"
    ヨルダン = "JO"
    カザフスタン = "KZ"
    ケニア = "KE"
    キリバス = "KI"
    北朝鮮 = "KP"
    韓国 = "KR"
    クウェート = "KW"
    キルギスタン = "KG"
    ラオス人民民主共和国 = "LA"
    ラトビア = "LV"
    レバノン = "LB"
    レソト = "LS"
    リベリア = "LR"
    リビア = "LY"
    リヒテンシュタイン = "LI"
    リトアニア = "LT"
    ルクセンブルク = "LU"
    マカオ = "MO"
    マケドニア旧ユーゴスラビア共和国 = "MK"
    マダガスカル = "MG"
    マラウイ = "MW"
    マレーシア = "MY"
    モルディブ = "MV"
    マリ = "ML"
    マルタ = "MT"
    マーシャル諸島 = "MH"
    マルティニーク = "MQ"
    モーリタニア = "MR"
    モーリシャス = "MU"
    マイヨット = "YT"
    メキシコ = "MX"
    ミクロネシア連邦 = "FM"
    モルドバ共和国 = "MD"
    モナコ = "MD"
    モンゴル = "MN"
    モントセラト = "MS"
    モロッコ = "MA"
    モザンビーク = "MZ"
    ミャンマー = "MM"
    ナミビア = "NA"
    ナウル = "NR"
    ネパール = "NP"
    オランダ = "NL"
    オランダ領アンティル = "AN"
    ニューカレドニア = "NC"
    ニュージーランド = "NZ"
    ニカラグア = "NI"
    ニジェール = "NE"
    ナイジェリア = "NG"
    ニウエ = "NU"
    ノーフォーク島 = "NF"
    北マリアナ諸島 = "MP"
    ノルウェー = "NO"
    オマーン = "OM"
    パキスタン = "PK"
    パラオ = "PW"
    パレスチナ自治政府 = "PS"
    パナマ = "PA"
    パプアニューギニア = "PG"
    パラグアイ = "PY"
    ペルー = "PE"
    フィリピン = "PH"
    ピトケアン諸島 = "PN"
    ポーランド = "PL"
    プエルトリコ = "PR"
    カタール = "QA"
    レユニオン島 = "RE"
    ルーマニア = "RO"
    ロシア = "RU"
    ルワンダ = "RW"
    セントヘレナ = "SH"
    セントクリストファーネーヴィス = "KN"
    セントルシア = "LC"
    サンピエールミクロン = "PM"
    セントビンセントおよびグレナディーン諸島 = "VC"
    サモア = "WS"
    サンマリノ = "SM"
    サントメプリンシペ = "ST"
    サウジアラビア = "SA"
    セネガル = "SN"
    セルビアモンテネグロ = "CS"
    セーシェル = "SC"
    シエラレオネ = "SL"
    シンガポール = "SG"
    スロバキア = "SK"
    スロベニア = "SI"
    ソロモン諸島 = "SB"
    ソマリア = "SO"
    南アフリカ = "ZA"
    南ジョージア南サンドイッチ諸島 = "GS"
    スペイン = "ES"
    スリランカ = "LK"
    スーダン = "SD"
    スリナム = "SR"
    スバールバルヤンマイエン諸島 = "SJ"
    スワジランド = "SZ"
    スウェーデン = "SE"
    スイス = "CH"
    シリア = "SY"
    台湾 = "TW"
    タジキスタン = "TJ"
    タンザニア連合共和国 = "TZ"
    タイ = "TH"
    東ティモール = "TL"
    トーゴ = "TG"
    トケラウ = "TK"
    トンガ = "TO"
    トリニダードトバゴ = "TT"
    チュニジア = "TN"
    トルコ = "TR"
    トルクメニスタン = "TM"
    タークスカイコス諸島 = "TC"
    ツバル = "TV"
    ウガンダ = "UG"
    ウクライナ = "UA"
    アラブ首長国連邦 = "AE"
    イギリス = "GB"
    アメリカ = "US"
    アメリカ合衆国外諸島 = "UM"
    ウルグアイ = "UY"
    ウズベキスタン = "UZ"
    バヌアツ = "VU"
    ベネズエラ = "VE"
    ベトナム = "VN"
    イギリス領ヴァージン諸島 = "VG"
    アメリカ領ヴァージン諸島 = "VI"
    ウォリスフツナ諸島 = "WF"
    西サハラ = "EH"
    イエメン = "YE"
    ザンビア = "ZM"
    ジンバブエ = "ZW"


class CountryIsoCode(Enum):
    """
    CountryIsoCode [summary]

    言語の国コードを

    Args:
        enum ([str]): 言語
    """

    アブハジア語 = "ab"
    アファル語 = "aa"
    アフリカーンス語 = "af"
    アルバニア語 = "sq"
    アムハラ語 = "am"
    アラビア語 = "ar"
    アルメニア語 = "hy"
    アッサム語 = "as"
    アイマラ語 = "ay"
    アゼルバイジャン語 = "az"
    バシキール語 = "ba"
    バスク語 = "eu"
    ベンガル語 = "bn"
    ブータン語 = "dz"
    ビハール語 = "bh"
    ビスラマ語 = "bi"
    ブルターニュ語 = "br"
    ブルガリア語 = "bg"
    ビルマ語 = "my"
    ベラルーシ語 = "be"
    カンボジア語 = "km"
    カタラン語 = "ca"
    中国語 = "zh"
    コルシカ語 = "co"
    クロアチア語 = "hr"
    チェコ語 = "cs"
    デンマーク語 = "da"
    オランダ語 = "nl"
    英語 = "en"
    エスペラント語 = "eo"
    エストニア語 = "et"
    フェロー語 = "fo"
    ペルシャ語 = "fa"
    フィジー語 = "fj"
    フィンランド語 = "fi"
    フランス語 = "fr"
    フリジア語 = "fy"
    ガリシア語 = "gl"
    ゲール語 = "gd"
    グルジア語 = "ka"
    ドイツ語 = "de"
    ギリシャ語 = "el"
    グリーンランド語 = "kl"
    グアラニー語 = "gn"
    グジャラート語 = "gu"
    ハウサ語 = "ha"
    ヘブライ語 = "he"
    ヒンディー語 = "hi"
    ハンガリー語 = "hu"
    アイスランド語 = "is"
    インドネシア語 = "id"
    インターリング語 = "ie"
    イヌクティトゥト語 = "iu"
    イヌピア語 = "ik"
    アイルランド語 = "ga"
    イタリア語 = "it"
    日本語 = "ja"
    ジャワ語 = "ja"
    カンナダ語 = "kn"
    カシミール語 = "ks"
    カザフ語 = "kk"
    キヤーワンダ語 = "rw"
    キルギス語 = "ky"
    キルンディ語 = "rn"
    韓国語 = "ko"
    クルド語 = "ku"
    ラオタ語 = "lo"
    ラテン語 = "la"
    ラトビア語 = "lv"
    リンブルク語 = "li"
    リンガラ語 = "ln"
    リトアニア語 = "lt"
    マケドニア語 = "mk"
    マダガスカル語 = "mg"
    マレー語 = "ms"
    マラヤーラム語 = "ml"
    マルタ語 = "mt"
    マオリ語 = "mi"
    マラーティー語 = "mr"
    モルドバ語 = "mo"
    モンゴル語 = "mn"
    ナウル語 = "na"
    ネパール語 = "ne"
    ノルウェー語 = "no"
    オック語 = "oc"
    オリヤー語 = "or"
    オロモ語 = "om"
    パシト語 = "ps"
    ポーランド語 = "pl"
    ポルトガル語 = "pt"
    パンジャブ語 = "pa"
    ケチュア語 = "qu"
    レートロマンス語 = "rm"
    ルーマニア語 = "ro"
    ロシア語 = "ru"
    サモア語 = "sm"
    サングホ語 = "sg"
    サンスクリット語 = "sa"
    セルビア語 = "sr"
    セルボクロアチア語 = "sh"
    セソト語 = "st"
    セツワナ語 = "tn"
    ショナ語 = "sn"
    シンド語 = "sd"
    シンハラ語 = "si"
    スワジ語 = "ss"
    スロバキア語 = "sk"
    スロベニア語 = "sl"
    ソマリ語 = "so"
    スペイン語 = "es"
    スンダ語 = "su"
    スワヒリ語 = "sw"
    スウェーデン語 = "sv"
    タガログ語 = "tl"
    タジク語 = "tg"
    タミル語 = "ta"
    タタール語 = "tt"
    テルグ語 = "te"
    タイ語 = "th"
    チベット語 = "bo"
    チグリニャ語 = "ti"
    トンガ語 = "to"
    ツォンガ語 = "ts"
    トルコ語 = "tr"
    トルクメン語 = "tk"
    トウィ語 = "tw"
    ウイグル語 = "ug"
    ウクライナ語 = "uk"
    ウルドゥー語 = "ur"
    ウズベク語 = "uz"
    ベトナム語 = "vi"
    ヴォラピュック語 = "vo"
    ウェールズ語 = "cy"
    ウォロフ語 = "wo"
    コーサ語 = "xh"
    イディッシュ語 = "yi"
    ヨルバ語 = "yo"
    ズールー語 = "zu"


class CountryExpress:

    @classmethod
    def smshub_id(cls, country):
        return SmsCountryId.__dict__[country].value

    @classmethod
    def smshub_service(cls, service):
        service = service.upper()
        return SmsServiceId.__dict__[service].value

    @classmethod
    def iso(cls, lang):
        return CountryIsoCode.__dict__[lang].value

    @classmethod
    def telcode(cls, country):
        return CountryTelCode.__dict__[country].value

    @classmethod
    def eng(cls, country):
        return CountryEnglish.__dict__[country].value

    @classmethod
    def code(cls, country):
        return CountryCode.__dict__[country].value


class Sms:

    url = "https://smshub.org/stubs/handler_api.php?"

    def __init__(self, apikey):
        self.apikey = apikey
        self.country = ""
        self.country_id = ""
        self.country_code = ""
        self.tel_code = ""
        self.activate_id = ''
        self.sms_number_not_country = ''
        self.pin_code = ''
        self.sms_number = ''
        
    def _balance(self):
        payload = {'api_key': self.apikey, 'action': 'getBalance'}
        response = requests.get(self.url, params=payload)
        print(response.status_code)    # HTTPのステータスコード取得
        print(response.text)    # レスポンスのHTMLを文字列で取得

    def _get(self, service, operator='any', country='any'):
        print(service, operator, country)
        self.country = country
        self.country_id = CountryExpress.smshub_id(country)
        self.country_code = CountryExpress.code(country)
        self.tel_code = CountryExpress.telcode(country)
        self.activate_id = ''
        self.sms_number_not_country = ''
        
        
        payload = {'api_key': self.apikey, 'action': 'getNumber','service': service, 'operator': operator, 'country': self.country_id}
        response = requests.get(self.url, params=payload)
        print(response.status_code)    # HTTPのステータスコード取得
        print(response.text)    # レスポンスのHTMLを文字列で取得
        return response.text

    def _pincode(self, activate_id):
        payload = {'api_key': self.apikey,'action': 'getStatus', 'id': activate_id}
        response = requests.get(self.url, params=payload)
        print(response.status_code)    # HTTPのステータスコード取得
        print(response.text)    # レスポンスのHTMLを文字列で取得
        return response.text

    def _status(self, status, activate_id):
        payload = {'api_key': self.apikey, 'action': 'setStatus',
                   'status': status, 'id': activate_id}
        response = requests.get(self.url, params=payload)
        print(response.status_code)    # HTTPのステータスコード取得
        print(response.text)    # レスポンスのHTMLを文字列で取得
        return response.text

    def _get_id_number(self, res):
        self.activate_id = res.split(':')[1]
        self.sms_number = res.split(':')[2]
        print(self.activate_id)
        print(self.sms_number)
        self.sms_number_not_country = str(self.sms_number).replace(str(self.tel_code), "", 1)
        
        return self.activate_id, self.sms_number_not_country

    def wait_for_pin_activate(self, activate_id, wait_max=30):
        # wait_max = 30  # wait_max ×10秒まで待つ
        status = 1  # sms send
        self._status(status, activate_id)
        for _ in range(1, wait_max):
            res = self._pincode(activate_id)
            if res.startswith('STATUS_OK'):
                self.pin_code = res.split(':')[1]
                status = 6  # sms end
                self._status(status, activate_id)
                return self.pin_code

            print('not pin wait time 10...')
            time.sleep(10)

        status = 8  # sms cancel
        self._status(status, activate_id)
        return None

    def wait_for_pin_activate_next(self, activate_id, wait_max=30):
        # wait_max = 30  # wait_max ×10秒まで待つ
        status = 1  # sms send
        self._status(status, activate_id)
        for ppp in range(1, wait_max):
            res = self._pincode(activate_id)
            if res.startswith('STATUS_OK'):
                self.pin_code = res.split(':')[1]
                status = 3  # sms end
                self._status(status, activate_id)
                return self.pin_code

            print('not pin wait time 10...')
            time.sleep(10)

        status = 3  # sms end
        self._status(status, activate_id)
        return None


# service: Tinder='oi', Google='go'
# 国:USA=12, インド=22
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    # 環境変数を参照
    load_dotenv()
    apikey = os.getenv('SMSHUB_API_KEY')
    service = 'mm'
    country = 0
    sms = Sms(apikey)
    #res = sms._get(service)
    res = sms._get(service, operator='any', country=country)
    activate_id, country_code, sms_number_not_country = sms._get_id_number(res)
    print(activate_id, country_code, sms_number_not_country)

    import pdb;pdb.set_trace()
    

    pin_code = sms.wait_for_pin_activate(activate_id)
    import pdb
    pdb.set_trace()

    response = sms._pincode(activate_id)

    url = "https://smshub.org/stubs/handler_api.php?"
    payload = {'api_key': apikey, 'action': 'getNumbersStatus','country': 182, 'operator': 'any'}
    response = requests.get(url, params=payload)
    print(response.status_code)    # HTTPのステータスコード取得
    print(response.text)    # レスポンスのHTMLを文字列で取得
