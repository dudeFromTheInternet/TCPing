# TCPing

Простой сетевой инструмент для проверки доступности хоста с использованием TCP с SYN/ACK.

## Как использовать

1. Установите библиотеку Scapy с помощью следующей команды:

    ```bash
    pip install scapy
    ```

2. Сохраните код скрипта в файл с расширением `.py` (например, `tcping_synack.py`).

3. Запустите скрипт из командной строки, указав целевой хост и порт:

    ```bash
    python tcping.py example.com 80
    ```

    Где `example.com` - это целевой хост, а `80` - порт, который вы хотите проверить.

## Дополнительные параметры

- `-n` или `--num-pings`: Укажите количество пингов для отправки (по умолчанию - один).
- `-t` или `--timeout`: Задайте таймаут ожидания для каждого пинга в секундах (по умолчанию - 5).
- `-i` или `--interval`: Установите интервал между пингами в секундах (по умолчанию - 1).

Примеры использования:

```bash
python tcping.py www.google.com:80
python tcping.py 8.8.8.8:53 -n 3 -t 2 -i 1
python tcping.py 8.8.8.8:53 8.8.4.4:53
```

## Автор

Автор: Илья Ратушный
