# coding=utf-8
import sys
from Lib.receiver.core.adaptors import Adaptor
from Lib.receiver.core.decorators.log_admin import log_admin
from Lib.receiver.core.exceptions import NotLoggedInException, LoginException, InternalException
from Lib.receiver.core.handlers import Handler
from Lib.receiver.core.initializers import Initializer
from Lib.receiver.core.parsers import Parser
from Lib.receiver.core.receivers import Receiver
from Lib.receiver.core.strategy import Page
from Lib.receiver.core.supports import EuroSupport, RuSupport
from Lib.receiver.core.urlCreators import UrlCreator
from Lib.receiver.lineage2.adaptors import Lineage2AdaptorFactory
from Lib.receiver.lineage2.handlers import Lineage2HandlerFactory
from Lib.receiver.lineage2.initializers import Lineage2InitializerFactory
from Lib.receiver.lineage2.pageTypes import PageType
from Lib.receiver.lineage2.parsers import Lineage2ParserFactory
from Lib.receiver.lineage2.receivers import Lineage2ReceiverFactory
from Lib.receiver.lineage2.urlCreators import Lineage2UrlCreatorFactory

__author__ = 'bulat.fattahov'

#==================================================================================
def tryToLoggedIn():
    def outer(fun):
        def inner(*args, **kwargs):
            try:
            #                пробуем выполнить действие
                return fun(*args, **kwargs)
            #            если не залогинены в админку, то
            except NotLoggedInException:
                # если у объекта-хозяина (L2AdminFacade) есть свойство support, будем использовать его.
                if hasattr(args[0], 'support') and args[0].support is not None:
                    support = args[0].support
                else:
                    raise InternalException(message="Support is not defined!")

                    #            логинимся
                login_page = Page(support, PageType.LOGIN_PAGE)
                try:
                    login_page.get()
                except LoginException as er:
                #                    print("Could not log in L2Admin. Check your params")
                    raise er
                else:
                # пробуем еще раз получить страницу
                    return fun(*args, **kwargs)

        return inner

    return outer

#==================================================================================

class L2AdminFacade():
    logger = None
    support = None

    def __init__(self, support):
        UrlCreator.setFactory(Lineage2UrlCreatorFactory())
        Adaptor.setFactory(Lineage2AdaptorFactory())
        Initializer.setFactory(Lineage2InitializerFactory())
        Receiver.setFactory(Lineage2ReceiverFactory())
        Parser.setFactory(Lineage2ParserFactory())
        Handler.setFactory(Lineage2HandlerFactory())
        self.support = support


    @log_admin()
    def loggable_operation(self, a, b):
        print( a, b)

    # gets adena count
    @tryToLoggedIn()
    def get_adena(self, serverId):
        page = Page(self.support, PageType.AMOUNT_BY_ITEM_TYPE_AND_SERVER)
        params = {
            "keyword": 57,
            "variationType": "includeVariation",
            "viewType": "amountSum",
            "search": "Search",
            "worldList": serverId}
        amount = page.get(params)
        return amount


    @tryToLoggedIn()
    def change_character(self, params):
        """
        Fields if params
            "gender" - 0 - male, 1 - female
            "race" -
                0-Human
                1-Elf
                2-Dark Elf
                3-Orc
                4-Dwarf
                5-Kamael
            "cls"
                0 - Human Fighter
                1 - Warrior
                2 - Gladiator
                3 - Warlord
                4 - Human Knight
                5 - Paladin
                6 - Dark Avenger
                7 - Rogue
                8 - Treasure Hunter
                9 - Hawkeye
                10 - Human Mystic
                11 - Human Wizard
                12 - Sorcerer
                13 - Necromancer
                14 - Warlock
                15 - Cleric
                16 - Bishop
                17 - Prophet
                18 - Elven Fighter
                19 - Elven Knight
                20 - Temple Knight
                21 - Swordsinger
                22 - Elven Scout
                23 - Plainswalker
                24 - Silver Ranger
                25 - Elven Mystic
                26 - Elven Wizard
                27 - Spellsinger
                28 - Elemental Summoner
                29 - Elven Oracle
                30 - Elven Elder
                31 - Dark Fighter
                32 - Palus Knight
                33 - Shillien Knight
                34 - Bladedancer
                35 - Assassin
                36 - Abyss Walker
                37 - Phantom Ranger
                38 - Dark Mystic
                39 - Dark Wizard
                40 - Spellhowler
                41 - Phantom Summoner
                42 - Shillien Oracle
                43 - Shillien Elder
                44 - Orc Fighter
                45 - Orc Raider
                46 - Destroyer
                47 - Monk
                48 - Tyrant
                49 - Orc Mystic
                50 - Orc Shaman
                51 - Overlord
                52 - Warcryer
                53 - Dwarven Fighter
                54 - Scavenger
                55 - Bounty Hunter
                56 - Artisan
                57 - Warsmith
                88 - Duelist
                89 - Dreadnought
                90 - Phoenix Knight
                91 - Hell Knight
                92 - Sagittarius
                93 - Adventurer
                94 - Archmage
                95 - Soultaker
                96 - Arcana Lord
                97 - Cardinal
                98 - Hierophant
                99 - Eva's Templar
                100 - Sword Muse
                101 - Wind Rider
                102 - Moonlight Sentinel
                103 - Mystic Muse
                104 - Elemental Master
                105 - Eva's Saint
                106 - Shillien Templar
                107 - Spectral Dancer
                108 - Ghost Hunter
                109 - Ghost Sentinel
                110 - Storm Screamer
                111 - Spectral Master
                112 - Shillien Saint
                113 - Titan
                114 - Grand Khavatari
                115 - Dominator
                116 - Doomcryer
                117 - Fortune Seeker
                118 - Maestro
                123 - Kamael Soldier(Male)
                124 - Kamael Soldier(Female)
                125 - Trooper
                126 - Warder
                127 - Berserker
                128 - Soul Breaker(Male)
                129 - Soul Breaker(Female)
                130 - Arbalester
                131 - Doombringer
                132 - Soul Hound(Male)
                133 - Soul Hound(Female)
                134 - Trickster
                135 - Inspector
                136 - Judicator
                139 - Sigel Knight
                140 - Tyrr Warrior
                141 - Othell Rogue
                142 - Yul Archer
                143 - Feoh Wizard
                144 - Iss Enchanter
                145 - CT_WYNN_SUMMONER
                146 - Aeore Healer
            "face"
                0 - A
                1 - B
                2 - C
            "hairShape"
                0 - A
                1 - B
                2 - C
                3 - D
                4 - F
                5 - G
            "hairColor"
                0 - A
                1 - B
                2 - C
                3 - D
            "jobGroup"
                0 - Fighter
                1 - Magic
            "expDelta" - exp
            "spDelta" - sp
            "alignDelta" - karma
            "pkDelta" - pk
            "pkPardonDelta" - pkPardon
            "duelDelta" - duel
            "preOlympiadDelta" - previous oly
            "curOlympiadDelta" - current oly
            "PCcafePointDelta" - pc cafe points
            "PvPPointDelta" - fame
            "vitalityPointDelta" - vitality
            "botPointDelta" - bot

            "modifyWay" ("relative" of "absolute")
            "memo" - memo
        """
        page = Page(self.support, PageType.CHANGE_CHARACTER)
        page.get(params)
        return

# params has to contents "job" and "CharId" fields
    @tryToLoggedIn()
    def change_job(self, params):
        page = Page(self.support, PageType.CHANGE_JOB)
        return page.get(params)


# пока не работает
    @tryToLoggedIn()
    def approve_request(self, params):
        page = Page(self.support, PageType.APPROVE_REQUEST)
        return page.get(params)

#support = EuroSupport(login='bulat.fattahov', password='1qaz2wsx')
#support = EuroSupport(login='Approover', password='Lvq8sHY#:h&m')
#l2facade = L2AdminFacade(support)
#print l2facade.approve_request({"id": 112756, "approve": "Approve"})
#print l2facade.change_character({"CharId": 15, "curOlympiadDelta": 1, "modifyWay": "relative", "memo": "test"})
#print l2facade.change_job({"CharId": 170506, "job" : 0})

#