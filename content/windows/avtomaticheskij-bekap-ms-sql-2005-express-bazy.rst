Автоматический бэкап MS SQL 2005 Express базы
#############################################
:date: 2009-06-01 16:31
:author: gigimon
:category: Всякое
:tags: backup, express, mssql, бд, бэкап, скрипт
:slug: avtomaticheskij-bekap-ms-sql-2005-express-bazy

При переходе на новую программу на работе, перешли и на использование
MS SQL Server, заместо FirebirdSQL и встал вопрос резервного копирования
базы данных. Для этих целей в полной версии MS SQL используется
встроенный планировщик, к сожалению, в Express версии его нету, поэтому
пришлось использовать внешние средства Windows (планировщик) и командную
строку с интерфейсом к MS SQL.
Весь процесс создания бэкапа разделен на 2 файла: backup.bat с
командами Windows и MS SQL скрипт backup.sql, который содержит команды
для бэкапа нашей базы.
Файл backup.sql содержит:

.. code-block:: sql

    DECLARE @pathName NVARCHAR(512) 
    SET @pathName = 'D:mssqlbackupdb_backup_' + Convert(varchar(8), GETDATE(), 112) + '.bak' 
    BACKUP DATABASE [db_name] TO DISK = @pathName WITH NOFORMAT, NOINIT, NAME = N'db_backup', SKIP, NOREWIND, NOUNLOAD, STATS = 10

где @pathName указывает путь сохранения, а также имя файла. В нашем
случае, будет создаваться файл с именем db\_backup\_20082009 (если
создавать бэкап 20 числа 8 месяца 2009 года), db\_name - имя вашей базы

Файлик backup.bat:

.. code-block:: batch

    sqlcmd -S SERVER -U USER -P PASSWORD -i backup.sql
    "c:Program FilesWinRARRar.exe" a -m2 d:mssqlbackupdb_backup_%date%.rar d:mssqlbackupdb_backup_*.bak
    del d:mssqlbackupdb_backup_*.bak

где, SERVER - адрес сервера, USER - пользователь для подключения,
PASSWORD - собственно пароль :)

Также, данный скрипт архивирует базу и оставляет только архив, убивая
.bak

После создания этих двух файликов, кидаем их куда-нибудь вместе и в
Windows планировщике создаем задание, раз в сутки (ну или когда хотите)
запускать backup.bat
