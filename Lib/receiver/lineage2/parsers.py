import re
from Lib.receiver.core.exceptions import InternalException

__author__ = 'bulat.fattahov'

import sys
import lxml.html
import Lib.receiver.core.parsers
from Lib.receiver.core.parsers import  Parser
from Lib.receiver.core.factories import FromDictFactory
from Lib.receiver.lineage2.pageTypes import PageType


class Lineage2ParserFactory(FromDictFactory):
    names = {PageType.LIST_LOG: "ListLogParser",
             PageType.CHANGE_CHARACTER:"ChangeCharacterParser",
             PageType.AMOUNT_BY_ITEM_TYPE_AND_SERVER: "ItemAmountParser"}

    # where we will look for parsers: in defaults and in this file
    whereToSeek = [Lib.receiver.core.parsers,
                   sys.modules[__name__]]

    def getForPage(self, page):
        object = FromDictFactory.getForPage(self, page)
        # provide our default parser if not found
        if not object:
            return Lineage2DefaultParser(page)
        return object

#=====================================================

class Lineage2DefaultParser(Parser):
    lxlmldoc = None
    naviUrl = None

    def __init__(self, page):
        Parser.__init__(self, page)

    def parse(self, page_str):
        Parser.parse(self, page_str)
        self.lxlmldoc = lxml.html.document_fromstring(page_str)

        temp = self.lxlmldoc.xpath('//form/input[@name="__VIEWSTATE"]')
        if temp and len(temp): self.page.setViewState(temp[0].value)

        temp = self.lxlmldoc.xpath('//form/input[@name="actionKey"]')
        if temp and len(temp): self.page.setActionKey(temp[0].value)
        return page_str


class ListLogParser(Lineage2DefaultParser):
    def parse(self, page_str):
        page_str = Lineage2DefaultParser.parse(self, page_str)
        table = self.lxlmldoc.xpath('//*[@id="ListLog"]/table[2]')
        if not self.naviUrl:
            naviUrl = self.lxlmldoc.xpath('//*[@id="navigatorView2_navigation"]/table/tr/td/a[1]')
            if naviUrl:
                url = naviUrl[0].attrib['href']
                self.naviUrl = url
        return page_str


class ItemAmountParser(Lineage2DefaultParser):
    def parse(self, page_str):
        page_str = Lineage2DefaultParser.parse(self, page_str)
        no_result = self.lxlmldoc.xpath('//*[@id="ListItemByType"]/table[2]/tr[3]/td')
        if (no_result and no_result[0].text == 'There is no result.'):
            return 0
        amount = self.lxlmldoc.xpath('//*[@id="ListItemByType"]/table[2]/tr[3]/td[6]')

        if (amount and amount.__len__() and amount[0].text):
            return amount[0].text.replace(',', '')
        return amount


class ChangeCharacterParser(Lineage2DefaultParser):
    def parse(self, page_str):
        page_str = Lineage2DefaultParser.parse(self, page_str)
        try:
            gender = (str)(self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[4]/td[2]/text()')[0])
            for temp in self.lxlmldoc.xpath('//*[@id="gender"]/option'):
                if temp.text == gender:
                    gender = temp.xpath('@value')[0]
                    break

            race = self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[4]/td[4]/text()')[0]
            for temp in self.lxlmldoc.xpath('//*[@id="race"]/option'):
                if temp.text == race:
                    race = temp.xpath('@value')[0]
                    break

            clazz = self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[4]/td[6]/text()')[0]
            for temp in self.lxlmldoc.xpath('//*[@id="cls"]/option'):
                if temp.text == clazz:
                    clazz = temp.xpath('@value')[0]
                    break


            face = self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[6]/td[2]/text()')[0]
            for temp in self.lxlmldoc.xpath('//*[@id="face"]/option'):
                if temp.text == face:
                    face = temp.xpath('@value')[0]
                    break

            hair_style = self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[6]/td[4]/text()')[0]
            for temp in self.lxlmldoc.xpath('//*[@id="hairShape"]/option'):
                if temp.text == hair_style:
                    hair_style = temp.xpath('@value')[0]
                    break

            hair_color = self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[6]/td[6]/text()')[0]
            for temp in self.lxlmldoc.xpath('//*[@id="hairColor"]/option'):
                if temp.text == hair_color:
                    hair_color = temp.xpath('@value')[0]
                    break

            jobGroup = self.lxlmldoc.xpath('//*[@id="ModifyChar"]/table[4]/tr[7]/td[2]/text()')[0]
            if re.search ("fighter", jobGroup, re.I):
                jobGroup = 0
            else:
                jobGroup = 1

            char_name = self.lxlmldoc.xpath('//*[@id="briefCharacterView_charName"]')[0].text

            exp = self.lxlmldoc.xpath('//*[@id="txtHiddenExp"]')[0].value
            sp = self.lxlmldoc.xpath('//*[@id="txtHiddenSp"]')[0].value
            karma = self.lxlmldoc.xpath('//*[@id="txtHiddenAlign"]')[0].value
            pk = self.lxlmldoc.xpath('//*[@id="txtHiddenPk"]')[0].value
            pk_pardon = self.lxlmldoc.xpath('//*[@id="txtHiddenPkPardon"]')[0].value
            duel = self.lxlmldoc.xpath('//*[@id="txtHiddenDuel"]')[0].value
            pre_olympiad = self.lxlmldoc.xpath('//*[@id="txtHiddenpreOlympiad"]')[0].value
            cur_olympiad = self.lxlmldoc.xpath('//*[@id="txtHiddencurOlympiad"]')[0].value
            PC_cafe_point = self.lxlmldoc.xpath('//*[@id="txtHiddenPCcafepoint"]')[0].value
            fame = self.lxlmldoc.xpath('//*[@id="txtHiddenPvpPoint"]')[0].value
            vitality = self.lxlmldoc.xpath('//*[@id="txtHiddenVitalityPoint"]')[0].value
            bot = self.lxlmldoc.xpath('//*[@id="txtHiddenBotPoint"]')[0].value

            return {
                "CharName" : char_name,
                "gender": gender,
                "race": race,
                "cls": clazz,
                "face": face,
                "hairShape": hair_style,
                "hairColor": hair_color,
                "jobGroup": jobGroup,
                "hiddenOriginalExp": exp,
                "expDelta": exp,
#                "DropDownListLevel": "0",
                "spDelta": sp,
                "alignDelta": karma,
                "pkDelta": pk,
                "pkPardonDelta": pk_pardon,
                "duelDelta": duel,
                "preOlympiadDelta": pre_olympiad,
                "curOlympiadDelta": cur_olympiad,
                "PCcafePointDelta": PC_cafe_point,
                "PvPPointDelta": fame,
                "vitalityPointDelta": vitality,
                "botPointDelta": bot,
                "modifyWay": "absolute",
                "update": "Request change",
                "txtHiddenExp": exp,
                "txtHiddenSp": sp,
                "txtHiddenAlign": karma,
                "txtHiddenPk": pk,
                "txtHiddenPkPardon": pk_pardon,
                "txtHiddenDuel": duel,
                "txtHiddenpreOlympiad": pre_olympiad,
                "txtHiddencurOlympiad": cur_olympiad,
                "txtHiddenPCcafepoint": PC_cafe_point,
                "txtHiddenPvpPoint": fame,
                "txtHiddenVitalityPoint": vitality,
                "txtHiddenBotPoint": bot
            }

        except Exception as e:
            print(e)
            raise InternalException(message="Internal error in parser!")


