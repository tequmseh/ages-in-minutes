#!/bin/bash
cd "$(dirname "$0")"
python3 ca_scenes.py render 03_the_trading_empire 00a_cold_open 00b_cold_open 05_round_harbour 12a_what_remains 12b_what_remains > log1.txt 2>&1 &
python3 ca_scenes.py render 09_hannibal 08a_the_barcas_in_spain 04a_the_sicilian_wars 04b_the_sicilian_wars > log2.txt 2>&1 &
python3 ca_scenes.py render 01b_the_purple_people 02a_new_city 07a_the_truceless_war 07b_the_truceless_war 01a_the_purple_people 02b_new_city > log3.txt 2>&1 &
python3 ca_scenes.py render 10_the_long_defeat 11_carthage_must_be_destroyed 08b_the_barcas_in_spain 06a_the_first_war_with_rome 06b_the_first_war_with_rome > log4.txt 2>&1 &
wait
