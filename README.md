# coingecko_parser
parser for www.coingecko.com

Notes:
1. before start exec "pip install -r (path_to_script_folder)/requirements.txt"
2. before start check and edit row #6 in "tables_creator.py", you need to check username, password, host and datebase name
3. if datebase is not existas - you need to create it manualy
4. before start create file /etcsystemd/system/parser.service and writedown next rows:
[Unit]
Description=parser
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /{path_to_"parser.py"}/parser.py

[Install]
WantedBy=multi-user.target

P.S.
Ограничил количество монет и рынков до 40, также установил sleep(65), так как в текущей реализации API количество запросов
ограничено до 50 в минуту. Если брать весь объем данных - не уложиться, сервер блокирует запросы. В оф. документации пишут,
что в будущем предоставят инструмен с большей производительностью, но пока так. Возможно, если подойти с точки зрения финансовой аналитики, можно брать информацию не обо всех сущностях, а выбрать наиболее интересные (многие коины не имеют рыночного движения месяцами) - можно обойти ограничение в запросах. Часть информации скопом не получить (так уж реализован АПИ)