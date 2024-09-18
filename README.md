# OneLine • pytest-online
Зародыш плагина для кастомизации строчек отчётов в [pytest](https://docs.pytest.org/).

![Как выглядит отчёт pytest после включения плагина](https://github.com/user-attachments/assets/9368babb-93dd-4a43-b12b-849fc7dcb197)

## Как использовать
1. Скопируйте содержимое каталога [pytest-oneline](pytest-oneline/) в каталог с тестами вашего проекта.
2. Если файл _conftest.py_ у вас уже есть — объедините его с одноимённым файлом плагина.
3. После этого отчёты в терминале поменяются.

## Как адаптировать под себя
90% настроек можно указать напрямую в датаклассе ```OneLinePreset``` (файл [conftest.py](pytest-oneline/conftest.py)).
Для остального есть рецепты в статье.

## Ограничения
1. У всех тестирующих функций должны быть docstrings.
2. Ключ ```-q``` работает недостаточно компактно.

Возможны и другие сюрпризы. Пожалуйста, создавайте issues в проекте.

## Детали реализации
См. статью на Хабре.

## Полезное
1. Шпаргалка по хукам ```pytest``` в форматах PDF и Figma.
2. Экспериментальные скрипты в каталоге [research](research/) и подкаталогах.
3. 
![Шпаргалка по хукам](https://github.com/user-attachments/assets/7db3fccd-d7d1-414d-9224-f5b2cc3275b1)
