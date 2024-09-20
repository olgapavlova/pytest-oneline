![line-schema](https://github.com/user-attachments/assets/2d0d1d6d-55c2-4403-b1aa-97dba3ca78a3)

# OneLine • pytest-online
Зародыш плагина для кастомизации строчек отчётов в **[pytest](https://docs.pytest.org/)**.

## Как использовать
1. Скопируйте содержимое каталога [pytest-oneline](pytest-oneline/) в каталог с тестами вашего проекта.
2. Если файл _conftest.py_ у вас уже есть — объедините его с одноимённым файлом плагина.
3. После этого отчёты **pytest** в терминале начнут выглядеть по новому.

![Как выглядит отчёт pytest после включения плагина](https://github.com/user-attachments/assets/9368babb-93dd-4a43-b12b-849fc7dcb197)

## Как адаптировать под себя
90% настроек можно указать напрямую в датаклассе ```OneLinePreset``` (файл [conftest.py](pytest-oneline/conftest.py)).
Для остального есть рецепты в [статье](https://habr.com/ru/articles/844728/).

## Ограничения
У всех тестирующих функций должны быть docstrings.

Возможны и другие сюрпризы. Пожалуйста, [создавайте issues в проекте](https://github.com/olgapavlova/pytest-oneline/issues).

## Детали реализации
См. [статью на Хабре](https://habr.com/ru/articles/844728/).

## Полезное
1. Шпаргалка по хукам **pytest** в форматах [PDF](schema/OneLine.pdf) и [Figma](schema/OneLine.fig).
2. Экспериментальные скрипты в каталоге [research](research/) и подкаталогах.

![Шпаргалка по хукам](https://github.com/user-attachments/assets/7db3fccd-d7d1-414d-9224-f5b2cc3275b1)
