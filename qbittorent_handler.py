from qbittorrent import client
import argparse
import telegram_bot_handler as th
import psutil
import subprocess
from time import sleep


"""
Kullanmak için şu adimlari takip edin:
1-) qBittorrent uygulamasina girin.
2-) Ayarlar içinden "Web Arayüzü" sekmesini bulun.
3-) Giriş bilgilerini:
Kullanici adi: admin
Şifre:
123456
    olacak şekilde düzeneleyin.

4-) Torrent listenize göz atin. İndirilmesini istediğiniz torrentin ismini düzenleyin 
    (örneğin arch linux için sürüm numaralari isme dahildir.)
    Bu size okuma kolayliği sağlayacaktir.
5-) İstediğiniz torrentlerin isimlerini torrent.txt isminde bir metin belgesine her satirda tek torrent olacak şekilde yazin.

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

Uçbirim (terminal) için bayraklar:
-r --resume : torrent
-p --pause  : torrentlerin hepsini durdurur
-S --status : listedeki torrentlerin durumlarini "telegram_bot_handler.py" araciliğiyla telefonunuza gönderir.
-h --help   : Kullanim bilgilerini görüntüler.

Sözdizimi: python.exe /kodun/bulunduğu/yol/qbittorrent_handler.py -S

"""

with open("torrent.txt") as f:
    global target_torrent
    target_torrents = f.readlines()


def is_process_running(process_name):
    for process in psutil.process_iter(["name"]):
        if process.info["name"] == process_name:
            return True
    return False


def qbittorent_kontrol():
    """
    qBittorrent uygulamasinin açik olduğundan emin olur, değilse açar
    """
    if is_process_running("qbittorrent.exe"):
        print("[DEBUG] qBittorrent acik")
        pass
    else:
        print("[DEBUG] qBittorrent kapali")
        subprocess.Popen(
            ["C:/Program Files/qBittorrent/qbittorrent.exe"], close_fds=True
        )
        sleep(6)
        print("[DEBUG] qBittorrent basariyla acildi")


def boyut_formatla(b, factor=1024, suffix="B"):
    """
    byte büyüklükleri daha güzel hale getirir.
    örn:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def bagla(login="admin", passwd="123456"):
    qbittorent_kontrol()
    qb = client.Client("http://127.0.0.1:8080/")
    print("[DEBUG] Baglanti kuruldu")
    qb.login(login, passwd)
    return qb


qb = bagla()
torrents = qb.torrents()


def torrent_listele(istenen=""):
    if istenen == "":
        for torrent in torrents:
            print("Torrent name:", torrent["name"])
            print("hash:", torrent["hash"])
            print("Seeds:", torrent["num_seeds"])
            print("File size:", boyut_formatla(torrent["total_size"]))
            print("Download speed:", boyut_formatla(torrent["dlspeed"]) + "/s")
            print("Amount left:", boyut_formatla(torrent["amount_left"]))
            print(
                "\n-----(\_O_/)-----(\_O_/)-----(\_O_/)-----(\_O_/)-----(\_O_/)-----\n"
            )
    else:
        for torrent in torrents:
            if torrent["name"] == istenen:
                print("Torrent name:", torrent["name"])
                print("hash:", torrent["hash"])
                print("Seeds:", torrent["num_seeds"])
                print("File size:", boyut_formatla(torrent["total_size"]))
                print("Download speed:", boyut_formatla(torrent["dlspeed"]) + "/s")
                print("Amount left:", boyut_formatla(torrent["amount_left"]))
                break


def torrent_devam_et(istenen):
    qbittorent_kontrol()
    torrent = ""
    for i in torrents:
        if i["name"] == istenen:
            torrent = i["hash"]
            break
    if not torrent:
        print("Bruh, torrent is none")
    else:
        qb.resume(torrent)


def torrent_durdur(torrent_listesi=[], hepsi_mi=True):
    qbittorent_kontrol()
    if hepsi_mi:
        qb.pause_all()
    else:
        torrent_hashs = []
        for i in torrents:
            if i["name"] in torrent_listesi:
                torrent_hashs.append(i["hash"])
        qb.pause_multiple(torrent_hashs)


def torrent_bitti_mi(istenen):
    print("[DEBUG] Torrent kontrolü yapılıyor: {} için".format(istenen.strip()))
    qbittorent_kontrol()
    for torrent in torrents:
        if torrent["name"] == istenen:
            if not torrent["amount_left"]:
                th.send_message(f"{istenen} bitti!")
            else:
                total_size = torrent["total_size"]
                remaining_size = torrent["amount_left"]
                downloaded_size = total_size - remaining_size
                progress = (downloaded_size / total_size) * 100
                th.send_message(
                    f"{istenen} için {boyut_formatla(torrent['amount_left'])} kaldı\nİlerleme: {progress:.2f}%\nDurum: {torrent['state']}\nHız: {boyut_formatla(torrent['dlspeed'])}"
                )


def main():
    parser = argparse.ArgumentParser(description="qBittorrent Automation Script")
    parser.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="Resume the torrent that is in the txt file. You have to manually edit it to change torrent starting.",
    )
    parser.add_argument("-p", "--pause", action="store_true", help="Pause all torrents")
    parser.add_argument(
        "-S", "--status", action="store_true", help="Hedef torrent bitmiş mi?"
    )

    args = parser.parse_args()

    if args.resume:
        for i in target_torrents:
            
            torrent_devam_et(i.strip())

    if args.pause:
        for i in target_torrents:

            torrent_durdur(i.strip())

    if args.status:
        for i in target_torrents:
            torrent_bitti_mi(i.strip())


if __name__ == "__main__":
    main()
