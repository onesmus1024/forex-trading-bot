import unittest
import pandas as pd
import talib as ta
from mt5_global import settings
from technical_analysis.patterns.morning_evening_star import MorningEveningStar
from technical_analysis.patterns.morning_evening_doji_star import MorningEveningDoji
from technical_analysis.patterns.piercing_dark_cloud import PiercingDarkCloud
from technical_analysis.patterns.shooting_start_inverted_hammer import ShootingStartInvertedHammer
from technical_analysis.patterns.hammer_hanging_man import HammerHangingMan
from technical_analysis.patterns.bearish_bullish_engulfing import BearishBullishEnglufing
from technical_analysis.patterns.belt_hold import BeltHold
from technical_analysis.patterns.counter_attack import CounterAttack
from technical_analysis.patterns.doji import Doji
from technical_analysis.patterns.harami import Harami
from technical_analysis.patterns.threeblackcrows_threeadvancingsolders import ThreeBlackCrowsThreeAdvancingSolders
from technical_analysis.patterns.unique3river import Unique3River
from technical_analysis.patterns.upsidegap2crows import UpsideGap2Crows
pattern_not_found=0
class TestPattern(
    unittest.TestCase,
    MorningEveningStar,
    MorningEveningDoji,
    PiercingDarkCloud,
    ShootingStartInvertedHammer,
    HammerHangingMan,
    BearishBullishEnglufing,
    BeltHold,
    CounterAttack,
    Doji,
    Harami,
    ThreeBlackCrowsThreeAdvancingSolders,
    Unique3River,
    UpsideGap2Crows
    ):

    def test_morning_star(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        morning_star_index = 0
        for i in range(len(df)):
            if df['morning_star'][i] == 100 and i>settings.period:
                morning_star_index = i
                break
        if morning_star_index == 0:
            print('morning star not found')
            pattern_not_found += 1
            self.assertEqual(morning_star_index, 0)
        else:
            df = df[morning_star_index+1-settings.period:morning_star_index+1]
            self.check_morning_evening_star(df)
            self.assertEqual(self.morning_star[-1], 100)
            self.assertEqual(self.evening_star[-1], 0)
    def test_evening_star(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        evening_star_index = 0
        for i in range(len(df)):
            if df['evening_star'][i] == 100 and i>settings.period:
                evening_star_index = i
                break
        if evening_star_index == 0:
            print('evening star not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(evening_star_index, 0)
        else:
            df = df[evening_star_index+1-settings.period:evening_star_index+1]
            self.check_morning_evening_star(df)
            self.assertEqual(self.morning_star[-1], 0)
            self.assertEqual(self.evening_star[-1], 100)
    def test_morning_doji_star(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        morning_doji_star_index = 0
        for i in range(len(df)):
            if df['morning_doji_star'][i] == 100 and i>settings.period:
                morning_doji_star_index = i
                break
        if morning_doji_star_index == 0:
            print('morning doji star not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(morning_doji_star_index, 0)
        else:
            df = df[morning_doji_star_index+1-settings.period:morning_doji_star_index+1]
            self.check_moring_evining_doji(df)
            self.assertEqual(self.morning_doji_star[-1], 100)
            self.assertEqual(self.evening_doji_star[-1], 0)
    def test_evening_doji_star(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        evening_doji_star_index = 0
        for i in range(len(df)):
            if df['evening_doji_star'][i] == 100 and i>settings.period:
                evening_doji_star_index = i
                break
        if evening_doji_star_index == 0:
            print('evening doji star not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(evening_doji_star_index, 0)
        else:
            df = df[evening_doji_star_index+1-settings.period:evening_doji_star_index+1]
            self.check_moring_evining_doji(df)
            self.assertEqual(self.morning_doji_star[-1], 0)
            self.assertEqual(self.evening_doji_star[-1], 100)
    def test_piercing(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        piercing_index = 0
        for i in range(len(df)):
            if df['piercing'][i] == 100 and i>settings.period:
                piercing_index = i
                break
        if piercing_index == 0:
            print('piercing not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(piercing_index, 0)
        else:
            df = df[piercing_index+1-settings.period:piercing_index+1]
            self.check_piercing_dark_cloud(df)
            self.assertEqual(self.piercing[-1], 100)
            self.assertEqual(self.dark_cloud[-1], 0)
    def test_dark_cloud(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        dark_cloud_index = 0
        for i in range(len(df)):
            if df['dark_cloud'][i] == 100 and i>settings.period:
                dark_cloud_index = i
                break
        if dark_cloud_index == 0:
            print('dark cloud not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(dark_cloud_index, 0)
        else:
            df = df[dark_cloud_index+1-settings.period:dark_cloud_index+1]
            self.check_piercing_dark_cloud(df)
            self.assertEqual(self.piercing[-1], 0)
            self.assertEqual(self.dark_cloud[-1], 100)
    def test_shooting_star(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        shooting_star_index = 0
        for i in range(len(df)):
            if df['shooting_star'][i] == 100 and i>settings.period:
                shooting_star_index = i
                break
        if shooting_star_index == 0:
            print('shooting star not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(shooting_star_index, 0)
        else:
            df = df[shooting_star_index+1-settings.period:shooting_star_index+1]
            self.check_shooting_start_inverted_hammer(df)
            self.assertEqual(self.shooting_star[-1], 100)
            self.assertEqual(self.inverted_hammer[-1], 0)
    def test_inverted_hammer(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        inverted_hammer_index = 0
        for i in range(len(df)):
            if df['inverted_hammer'][i] == 100 and i>settings.period:
                inverted_hammer_index = i
                break
        if inverted_hammer_index == 0:
            print('inverted hammer not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(inverted_hammer_index, 0)
        else:
            df = df[inverted_hammer_index+1-settings.period:inverted_hammer_index+1]
            self.check_shooting_start_inverted_hammer(df)
            self.assertEqual(self.shooting_star[-1], 0)
            self.assertEqual(self.inverted_hammer[-1], 100)
    def test_hammer(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        
        hammer_index = 0
        for i in range(len(df)):
            if df['hammer'][i] == 100 and i>settings.period:
                hammer_index = i
                break
        if hammer_index == 0:
            print('hammer not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(hammer_index, 0)
        else:
            df = df[hammer_index+1-settings.period:hammer_index+1]
            self.check_hammer_hanging_man(df)
            self.assertEqual(self.hammer[-1], 100)
            self.assertEqual(self.hanging_man[-1], 0)
    def test_hanging_man(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        hanging_man_index = 0
        for i in range(len(df)):
            if df['hanging_man'][i] == 100 and i>settings.period:
                hanging_man_index = i
                break
        if hanging_man_index == 0:
            print('hanging man not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(hanging_man_index, 0)
        else:
            df = df[hanging_man_index+1-settings.period:hanging_man_index+1]
            self.check_hammer_hanging_man(df)
            self.assertEqual(self.hammer[-1], 0)
            self.assertEqual(self.hanging_man[-1], 100)
    def test_belthold_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        belthold_index = 0
        for i in range(len(df)):
            if df['belt_hold'][i] == 100 and i>settings.period:
                belthold_index = i
                break
        if belthold_index == 0:
            print('belthold buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(belthold_index, 0)
        else:
            df = df[belthold_index+1-settings.period:belthold_index+1]
            self.check_belt_hold(df)
            self.assertEqual(self.belt_hold[-1], 100)
    def test_belthold_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        belthold_index = 0
        for i in range(len(df)):
            if df['belt_hold'][i] == -100 and i>settings.period:
                belthold_index = i
                break
        if belthold_index == 0:
            print('belthold sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(belthold_index, 0)
        else:
            df = df[belthold_index+1-settings.period:belthold_index+1]
            self.check_belt_hold(df)
            self.assertEqual(self.belt_hold[-1], -100)
    def test_counterattack_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        counterattack_index = 0
        for i in range(len(df)):
            if df['counter_attack'][i] == 100 and i>settings.period:
                counterattack_index = i
                break
        if counterattack_index == 0:
            print('counterattack buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(counterattack_index, 0)
        else:
            df = df[counterattack_index+1-settings.period:counterattack_index+1]
            self.check_counter_attack(df)
            self.assertEqual(self.counter_attack[-1], 100)
    def test_counterattack_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        counterattack_index = 0
        for i in range(len(df)):
            if df['counter_attack'][i] == -100 and i>settings.period:
                counterattack_index = i
                break
        if counterattack_index == 0:
            print('counterattack sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(counterattack_index, 0)
        else:
            df = df[counterattack_index+1-settings.period:counterattack_index+1]
            self.check_counter_attack(df)
            self.assertEqual(self.counter_attack[-1], -100)
    def test_doji_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        doji_index = 0
        for i in range(len(df)):
            if df['doji'][i] == 100 and i>settings.period:
                doji_index = i
                break
        if doji_index == 0:
            print('doji buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(doji_index, 0)
        else:
            df = df[doji_index+1-settings.period:doji_index+1]
            self.check_doji(df)
            self.assertEqual(self.doji[-1], 100)
    def test_doji_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        doji_index = 0
        for i in range(len(df)):
            if df['doji'][i] == -100 and i>settings.period:
                doji_index = i
                break
        if doji_index == 0:
            print('doji sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(doji_index, 0)
        else:
            df = df[doji_index+1-settings.period:doji_index+1]
            self.check_doji(df)
            self.assertEqual(self.doji[-1], -100)
    def test_engulfing_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        engulfing_index = 0
        for i in range(len(df)):
            if df['bullish_engulfing'][i] == 100 and i>settings.period:
                engulfing_index = i
                break
        if engulfing_index == 0:
            print('engulfing buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(engulfing_index, 0)
        else:
            df = df[engulfing_index+1-settings.period:engulfing_index+1]
            self.check_bullish_bearish_engulfing(df)
            self.assertEqual(self.bullish_engulfing[-1], 100)
    def test_engulfing_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        engulfing_index = 0
        for i in range(len(df)):
            if df['bullish_engulfing'][i] == -100 and i>settings.period:
                engulfing_index = i
                break
        if engulfing_index == 0:
            print('engulfing sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(engulfing_index, 0)
        else:
            df = df[engulfing_index+1-settings.period:engulfing_index+1]
            self.check_bullish_bearish_engulfing(df)
            self.assertEqual(self.bearish_engulfing[-1], -100)
    def test_harami_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        harami_index = 0
        for i in range(len(df)):
            if df['harami'][i] == 100 and i>settings.period:
                harami_index = i
                break
        if harami_index == 0:
            print('harami buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(harami_index, 0)
        else:
            df = df[harami_index+1-settings.period:harami_index+1]
            self.check_harami(df)
            self.assertEqual(self.harami[-1], 100)
    def test_harami_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        harami_index = 0
        for i in range(len(df)):
            if df['harami'][i] == -100 and i>settings.period:
                harami_index = i
                break
        if harami_index == 0:
            print('harami sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(harami_index, 0)
        else:
            df = df[harami_index+1-settings.period:harami_index+1]
            self.check_harami(df)
            self.assertEqual(self.harami[-1], -100)
    def test_harami_cross_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        harami_cross_index = 0
        for i in range(len(df)):
            if df['harami_cross'][i] == 100 and i>settings.period:
                harami_cross_index = i
                break
        if harami_cross_index == 0:
            print('harami_cross buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(harami_cross_index, 0)
        else:
            df = df[harami_cross_index+1-settings.period:harami_cross_index+1]
            self.check_harami(df)
            self.assertEqual(self.harami_cross[-1], 100)
    def test_harami_cross_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        harami_cross_index = 0
        for i in range(len(df)):
            if df['harami_cross'][i] == -100 and i>settings.period:
                harami_cross_index = i
                break
        if harami_cross_index == 0:
            print('harami_cross sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(harami_cross_index, 0)
        else:
            df = df[harami_cross_index+1-settings.period:harami_cross_index+1]
            self.check_harami(df)
            self.assertEqual(self.harami_cross[-1], -100)
    def test_three_white_soldiers(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        three_white_soldiers_index = 0
        for i in range(len(df)):
            if df['three_white_soldiers'][i] == 100 and i>settings.period:
                three_white_soldiers_index = i
                break
        if three_white_soldiers_index == 0:
            print('three_white_soldiers not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(three_white_soldiers_index, 0)
        else:
            df = df[three_white_soldiers_index+1-settings.period:three_white_soldiers_index+1]
            self.check_three_black_crows_three_advancing_solders(df)
            self.assertEqual(self.three_advancing_solders[-1], 100)
    def test_three_black_crows(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        three_black_crows_index = 0
        for i in range(len(df)):
            if df['three_black_crows'][i] == -100 and i>settings.period:
                three_black_crows_index = i
                break
        if three_black_crows_index == 0:
            print('three_black_crows not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(three_black_crows_index, 0)
        else:
            df = df[three_black_crows_index+1-settings.period:three_black_crows_index+1]
            self.check_three_black_crows_three_advancing_solders(df)
            self.assertEqual(self.three_black_crows[-1], -100)
    def test_advancing_block_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        advancing_block_index = 0
        for i in range(len(df)):
            if df['advancing_block'][i] == 100 and i>settings.period:
                advancing_block_index = i
                break
        if advancing_block_index == 0:
            print('advancing_block buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(advancing_block_index, 0)
        else:
            df = df[advancing_block_index+1-settings.period:advancing_block_index+1]
            self.check_three_black_crows_three_advancing_solders(df)
            self.assertEqual(self.advancing_block[-1], 100)
    def test_advancing_block_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        advancing_block_index = 0
        for i in range(len(df)):
            if df['advancing_block'][i] == -100 and i>settings.period:
                advancing_block_index = i
                break
        if advancing_block_index == 0:
            print('advancing_block sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(advancing_block_index, 0)
        else:
            df = df[advancing_block_index+1-settings.period:advancing_block_index+1]
            self.check_three_black_crows_three_advancing_solders(df)
            self.assertEqual(self.advancing_block[-1], -100)
    def test_stalled_pattern_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        stalled_pattern_index = 0
        for i in range(len(df)):
            if df['stalled_pattern'][i] == 100 and i>settings.period:
                stalled_pattern_index = i
                break
        if stalled_pattern_index == 0:
            print('stalled_pattern buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(stalled_pattern_index, 0)
        else:
            df = df[stalled_pattern_index+1-settings.period:stalled_pattern_index+1]
            self.check_three_black_crows_three_advancing_solders(df)
            self.assertEqual(self.stalled_pattern[-1], 100)
    def test_stalled_pattern_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        stalled_pattern_index = 0
        for i in range(len(df)):
            if df['stalled_pattern'][i] == -100 and i>settings.period:
                stalled_pattern_index = i
                break
        if stalled_pattern_index == 0:
            print('stalled_pattern sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(stalled_pattern_index, 0)
        else:
            df = df[stalled_pattern_index+1-settings.period:stalled_pattern_index+1]
            self.check_three_black_crows_three_advancing_solders(df)
            self.assertEqual(self.stalled_pattern[-1], -100)
    def test_unique_three_river_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        unique_three_river_index = 0
        for i in range(len(df)):
            if df['unique_three_river'][i] == 100 and i>2600:
                unique_three_river_index = i
                break
        if unique_three_river_index == 0:
            print('unique_three_river buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(unique_three_river_index, 0)
        else:
            df = df[unique_three_river_index+1-2600:unique_three_river_index+1]
            self.check_unique_three_river(df)
            self.assertEqual(self.unique_three_river[-1], 100)
    def test_unique_three_river_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        unique_three_river_index = 0
        for i in range(len(df)):
            if df['unique_three_river'][i] == -100 and i>settings.period:
                unique_three_river_index = i
                break
        if unique_three_river_index == 0:
            print('unique_three_river sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(unique_three_river_index, 0)
        else:
            df = df[unique_three_river_index+1-settings.period:unique_three_river_index+1]
            self.check_unique_three_river(df)
            self.assertEqual(self.unique_three_river[-1], -100)
    def test_upside_gap_two_crows_buy(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        upside_gap_two_crows_index = 0
        for i in range(len(df)):
            if df['upside_gap_two_crows'][i] == 100 and i>settings.period:
                upside_gap_two_crows_index = i
                break
        if upside_gap_two_crows_index == 0:
            print('upside_gap_two_crows buy not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(upside_gap_two_crows_index, 0)
        else:
            df = df[upside_gap_two_crows_index+1-settings.period:upside_gap_two_crows_index+1]
            self.check_upside_gap_2_crows(df)
            self.assertEqual(self.upside_gap_two_crows[-1], 100)
    def test_upside_gap_two_crows_sell(self):
        df = pd.read_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')
        upside_gap_two_crows_index = 0
        for i in range(len(df)):
            if df['upside_gap_two_crows'][i] == -100 and i>settings.period:
                upside_gap_two_crows_index = i
                break
        if upside_gap_two_crows_index == 0:
            print('upside_gap_two_crows sell not found')
            global pattern_not_found
            pattern_not_found += 1
            self.assertEqual(upside_gap_two_crows_index, 0)
        else:
            df = df[upside_gap_two_crows_index+1-settings.period:upside_gap_two_crows_index+1]
            self.check_upside_gap_2_crows(df)
            self.assertEqual(self.upside_gap_two_crows[-1], -100)
        print('pattern_not_found', pattern_not_found)
