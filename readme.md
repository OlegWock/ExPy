ExPy
====

ExPy (ExpressPython) -- текстовый редактор, написанный с помощью библиотек PyQt4 (GUI) и PyEnchant (проверка орфографии). Редактор отлично работает на linux-системах (тестировалось на Ubuntu 12.04) и предназначен для Python версии 3.x (должно работать и под питоном второй ветки, если выпилить или профиксить print'ы). Использование под другими платформами не тестировалось, хотя работать должно под Windows и MacOS. О всех багах связанных с работой на этих сообщайте мне, особенно будут ценна информация о работе мод MacOS.

### Возможности
На данный момент реализован общий функционал (открыть, сохранить, новый документ), авто сохранение, статистика по документу и проверка орфографии. Еще одной небольшой фичей является то, что все действия доступны по хот-кеям, поэтому не нужно постоянно переключаться на мышь.

### Планы на будущее
:negative_squared_cross_mark: Сохранение на облачные сервисы (DropBox, Yandex.Disk)  
:negative_squared_cross_mark: Конвертирование в Ren'Py скрипт

Из-за того, что новеллы которые я делаю на русском языке, а синтаксис Ren'Py на английском -- приходится часто щелкать переключение раскладки. Поэтому хочу реализовать что-то вроде замены указанных юзером слов на другие. Например, комментарии вместо # будут обозначатся //, персонажи вместо английского обозначения можно будет писать на русском, что очень полезно в диалоге. Например, так:
```
//Это комментарий
|мама| Сына, иди кушать! //А это диалог
|Ян| Сейчас, мам, в Super Mario доиграю и приду.
|отец| Иди скорее, а то остынет.
```
Но это не все фичи, думаю, список будет пополняться. А если у вас есть хорошая идея -- милости прошу.

**Важно:** предложения добавить выравнивание, вставку картинок и прочего, что заставит отказаться от формата .txt -- не принимаются. Главной идеей этого редактора есть **простота и удобство.**