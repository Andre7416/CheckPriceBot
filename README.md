# CheckPriceBot
Данный телеграм бот был написан в рамках летней практики. С его помощью можно следить за изменением цен товаров на сайтах "www.farfetch.com/ru" и "www.yoox.com/ru" (на данный момент).  
Весь функционал бота основан на библиотеке "aiogram", парсинг сайтов для отслеживания цен был осуществлен с помощью библиотек "requests" и "bs4". Так же предусмотрена возможность подписываться/отписываться от рассылки.  
Взаимодействие с ботом максимально просто, необходимо добавлять интересующие товары с помощью команды. Так же есть команды для удаления ненужных товаров.  
Бот запоминает для каждого пользователя список товаров и, с некоторым интервалом, отправляет уведомления о изменении цен на них.  
Для запуска бота нужно запустить "main.py".
